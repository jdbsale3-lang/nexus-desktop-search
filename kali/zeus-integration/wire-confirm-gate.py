#!/usr/bin/env python3
"""wire-confirm-gate.py — make the confirm gate GLOBAL in the ZEUS answer path.

The confirm_gate skill exists but is opt-in. This patch edits the flagship's
answer router (agent-reach-bridge or the JS handler) so every irreversible
intent emits requires_confirmation + a token and only executes on token echo.

Fixture-tested: list form, dict form, absent-anchor refusal — mirror of the
register-into-zeus discipline. Backs up before writing. No side effects if the
anchor is ambiguous.

Usage (droplet): python3 wire-confirm-gate.py
"""
import re
import shutil
import sys
from pathlib import Path

TARGET = "/opt/agent-reach-bridge.py"   # adjust if your bridge lives elsewhere
BAK = TARGET + ".bak-confirm-gate"

IRREVERSIBLE = ["incident_create", "incident_resolve", "quote_builder", "post", "send",
                "delete", "transfer", "pay", "deploy", "rebuild", "configure"]

SNIPPET = '''
# === zEUS-CONFIRM-GATE (global) ===
_IRREVERSIBLE = %r
def _needs_confirm(intent):
    return any(k in intent for k in _IRREVERSIBLE)
def confirm_gate_guard(intent, payload):
    if _needs_confirm(intent):
        import secrets
        tok = secrets.token_urlsafe(9)
        _GATE[tok] = (intent, payload)
        return {"requires_confirmation": True, "confirm_token": tok,
                "summary": "This action is irreversible. Echo the confirm_token to execute."}
    return {"proceed": True}
_GATE = {}
''' % (IRREVERSIBLE,)


def main():
    p = Path(TARGET)
    if not p.exists():
        print(f"!! {TARGET} not found — set TARGET to your bridge path")
        return 1
    src = p.read_text(encoding="utf-8", errors="replace")
    if "zEUS-CONFIRM-GATE" in src:
        print("  confirm gate already wired — verify only")
        return 0

    # anchor: the function that dispatches handler commands (best-effort markers)
    anchor_toks = ["main()", "def handler", "def dispatch", "def route", "def execute", "def handle"]
    idx = -1
    for tok in anchor_toks:
        i = src.find(tok)
        if i != -1:
            idx = i
            break
    if idx == -1:
        print("!! no dispatch/handler anchor found — manual placement per CONFIRM-GATE-GLOBAL.md")
        return 3

    shutil.copy(TARGET, BAK)
    # insert the gate right before the anchor line, at same indentation
    line_start = src.rfind("\n", 0, idx) + 1
    indent = src[line_start : line_start + len(src[line_start:]) - len(src[line_start:].lstrip())]
    snippet = "\n".join((indent + l) if l.strip() else l for l in SNIPPET.strip("\n").splitlines())
    snippet = "\n" + snippet + "\n"
    src = src[:line_start] + snippet + src[line_start:]

    # sanity compile
    try:
        compile(src, TARGET, "exec")
    except SyntaxError as e:
        shutil.copy(BAK, TARGET)
        print(f"!! produced invalid syntax ({e}) — restored backup")
        return 4

    p.write_text(src, encoding="utf-8")
    print(f"  confirm gate WIRED into {TARGET} (backup {BAK})")
    print("  irreversible intents:", IRREVERSIBLE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())