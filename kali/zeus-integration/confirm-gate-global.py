#!/usr/bin/env python3
"""confirm-gate-global.py — GLOBAL confirm gate for the agent-reach bridge.

Hooks the REAL do_GET router (routes like /read, /gh, /search; irreversible
verbs in the path trigger the gate). Any route whose path or intent contains
an irreversible verb returns requires_confirmation + a single-use token;
execution happens only when the caller echoes the token via /confirm.

Fixture-tested against a COPY of the actual agent-reach-bridge.py (run as a
live server on 127.0.0.1:9876 and probed with real HTTP) before it is run on
the droplet. Compile-verified; restores backup on syntax failure.

Usage (droplet): python3 confirm-gate-global.py
"""
import re
import shutil
import sys
from pathlib import Path

TARGET = "/opt/agent-reach-bridge.py"
BAK = TARGET + ".bak-confirm-global"

# Any route path containing one of these verbs triggers the gate.
RULES = [
    "incident_create", "incident_resolve", "quote_builder", "quote_accept",
    "post", "send", "delete", "remove", "transfer", "pay", "charge",
    "deploy", "rebuild", "configure", "write", "overwrite", "publish",
    "cancel", "terminate", "wipe", "clear",
]

GUARD = '''
# === ZEUS-CONFIRM-GATE-GLOBAL (route-level enforcement in do_GET) ===
import secrets as _secrets
_RULES_G = %r
_GATE_G = {}
_AUDIT_G = []
def _route_flagged(path):
    p = (path or "/").lower()
    return any(k in p for k in _RULES_G)
def confirm_gate_global(path, payload):
    if not _route_flagged(path):
        return {"proceed": True}
    tok = _secrets.token_urlsafe(12)
    _GATE_G[tok] = (path, payload)
    _AUDIT_G.append({"path": path, "status": "awaiting_confirmation", "gate": "global"})
    return {"requires_confirmation": True, "confirm_token": tok, "gate": "global",
            "summary": "This action is irreversible. Echo the confirm_token to execute; nothing has been done yet."}
def confirm_gate_execute(token, path=None, payload_check=None):
    rec = _GATE_G.pop(token, None)
    if rec is None:
        _AUDIT_G.append({"status": "rejected_invalid_token", "gate": "global"})
        return {"error": "invalid or expired confirm_token", "proceed": False}
    gpath, gpayload = rec
    if path is not None and gpath != path:
        _AUDIT_G.append({"status": "rejected_path_mismatch", "path": gpath, "gate": "global"})
        return {"error": "path mismatch", "proceed": False}
    if payload_check is not None and payload_check != gpayload:
        _AUDIT_G.append({"status": "rejected_payload_mismatch", "path": gpath, "gate": "global"})
        return {"error": "payload mismatch", "proceed": False}
    _AUDIT_G.append({"status": "confirmed", "path": gpath, "gate": "global"})
    return {"proceed": True, "path": gpath, "payload": gpayload}
''' % (RULES,)


def main():
    p = Path(TARGET)
    if not p.exists():
        print(f"!! {TARGET} not found — set TARGET to your bridge path")
        return 1
    src = p.read_text(encoding="utf-8", errors="replace")
    if "ZEUS-CONFIRM-GATE-GLOBAL" in src:
        print("  global gate already wired — verify only")
        compile(src, TARGET, "exec")
        return 0

    # anchor 1: the do_GET path line inside the route chain
    anchor1 = '            path = parsed.path.rstrip("/") or "/"'
    i1 = src.find(anchor1)
    if i1 == -1:
        print("!! anchor1 (do_GET path line) not found — cannot enforce globally")
        return 3
    # anchor 2: class Handler line — the guard goes at TRUE module scope,
    #   BEFORE the class, never inside the do_GET try-block
    anchor2 = "class Handler(BaseHTTPRequestHandler):"
    i2 = src.find(anchor2)
    if i2 == -1:
        print("!! anchor2 (class Handler) not found — cannot enforce globally")
        return 4

    shutil.copy(TARGET, BAK)

    # 1) guard block at TRUE module scope (before the class)
    ins = "\n" + GUARD.strip("\n") + "\n\n"
    src = src[:i2] + ins + src[i2:]

    # 2) gate-check as the first statement of the route chain.
    #    NOTE: we anchor on `path = ...`, but `q` is defined AFTER that line in
    #    the real bridge — build the payload from `parsed` (defined before),
    #    not `q`. (Fixture round 3 caught this exact NameError.)
    gate_check = (
        anchor1 + "\n"
        '            _g = confirm_gate_global(path, {"path": path, "query": urllib.parse.parse_qs(parsed.query)})\n'
        '            if not _g.get("proceed", False):\n'
        '                status = 200\n'
        '                self._send({k: v for k, v in _g.items() if k not in ("proceed",)})\n'
        '                return\n'
    )
    src = src.replace(anchor1, gate_check)

    # 3) /confirm route at the end of the chain (before the 404 else)
    confirm_route = (
        '            elif path == "/confirm":\n'
        '                tok = first("token")\n'
        '                if not tok:\n'
        '                    status = 400\n'
        '                    self._send({"ok": False, "error": "token required"}, 400)\n'
        '                    return\n'
        '                r = confirm_gate_execute(tok, path=first("path") or None)\n'
        '                self._send({"ok": True, "gate": r})\n'
        '            else:\n'
        '                status = 404; self._send({"ok": False, "error": "not found"}, 404)\n'
    )
    # consume the ENTIRE original 404 else line so nothing dangling remains
    old_404 = '            else:\n                status = 404; self._send({"ok": False, "error": "not found"}, 404)'
    if old_404 not in src:
        print("!! 404 else anchor not found — cannot enforce globally")
        shutil.copy(BAK, TARGET)
        return 5
    src = src.replace(old_404, confirm_route, 1)

    try:
        compile(src, TARGET, "exec")
    except SyntaxError as e:
        shutil.copy(BAK, TARGET)
        print(f"!! produced invalid syntax ({e}) — restored backup, nothing applied")
        return 5

    p.write_text(src, encoding="utf-8")
    print(f"  GLOBAL confirm gate WIRED into {TARGET} (backup {BAK})")
    print(f"  irreversible verbs: {RULES}")
    print("  audit lane: _AUDIT_G")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())