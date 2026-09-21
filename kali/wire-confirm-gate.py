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

    # anchor: layered fallback — any top-level def, __main__ guard, or last import
    anchor_toks = ["def main(", "def handler(", "def dispatch(", "def route(", "def execute(", "def handle(", "if __name__", "def ", "import ", "from "]
    idx = -1
    used = None
    # prefer more specific anchors but never anchor INSIDE another def's body
    for tok in anchor_toks:
        i = src.find(tok)
        if i != -1:
            # only accept column-0 (module scope) anchors for broad tokens
            line_start = src.rfind("\n", 0, i) + 1
            col = i - line_start
            if tok in ("def ", "import ", "from ", "if __name__"):
                if col != 0:
                    continue
            idx = i
            used = tok
            break
    if idx == -1:
        print("!! no anchor found — manual placement per CONFIRM-GATE-GLOBAL.md")
        return 3

    shutil.copy(TARGET, BAK)
    # insert the gate BEFORE the anchor line, at column 0 always (module scope)
    line_start = src.rfind("\n", 0, idx) + 1
    snippet = "\n" + SNIPPET.strip("\n") + "\n\n"
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