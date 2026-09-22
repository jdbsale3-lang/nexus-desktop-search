#!/usr/bin/env python3
"""doctor-overlay-fix.py — make /reach/doctor report the NO-WRITE probe truth.

The doctor statuses come from the `agent-reach doctor --json` CLI, which
deliberately refuses side-effecting checks (gh auth status writes a device-id;
it won't start the mcporter service). We proved github + exa work via read-only
probes (HTTP 200). This patch overlays those probe results onto the doctor's
channel map so the wire shows ok where ok is provable.

Patch mechanics (same discipline as the other fixers):
  - anchor: the doctor() function's `return json.loads(out)` line
  - before it: inject _doctor_probe_overlay() at module scope
  - replace the return to pass through the overlay
  - compile-verified; restores backup on any syntax failure

Usage (droplet): python3 doctor-overlay-fix.py
"""
import shutil
import sys
from pathlib import Path

TARGET = "/opt/agent-reach-bridge.py"
BAK = TARGET + ".bak-doctor-overlay"

OVERLAY = '''
# === ZEUS-DOCTOR-OVERLAY (no-write truth on /reach/doctor) ===
import json as _json
import os as _os
import urllib.request as _ur
def _probe_github_token():
    tok = _os.environ.get("GITHUB_TOKEN") or _os.environ.get("GH_TOKEN", "")
    if not tok:
        return None
    try:
        req = _ur.Request("https://api.github.com/user",
                          headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"})
        with _ur.urlopen(req, timeout=15) as r:
            return r.status
    except Exception:
        return None
def _probe_exa_key():
    key = _os.environ.get("REACH_EXA_KEY") or _os.environ.get("EXA_API_KEY", "")
    if not key:
        return None
    try:
        body = _json.dumps({"query": "zeus ai", "numResults": 1}).encode()
        req = _ur.Request("https://api.exa.ai/search", data=body,
                          headers={"x-api-key": key, "Content-Type": "application/json"})
        with _ur.urlopen(req, timeout=15) as r:
            return r.status
    except Exception:
        return None
def _doctor_probe_overlay(d):
    if not isinstance(d, dict):
        return d
    ch = d.get("channels")
    if isinstance(ch, dict):
        g = _probe_github_token()
        if g == 200:
            ch["github"] = {"status": "ok", "via": "no-write probe (HTTP 200)"}
        e = _probe_exa_key()
        if e == 200:
            ch["exa_search"] = {"status": "ok", "via": "no-write probe (HTTP 200)"}
    return d
'''


def main():
    p = Path(TARGET)
    if not p.exists():
        print(f"!! {TARGET} not found — set TARGET to your bridge path")
        return 1
    src = p.read_text(encoding="utf-8", errors="replace")
    if "ZEUS-DOCTOR-OVERLAY" in src:
        print("  overlay already wired — verify only")
        compile(src, TARGET, "exec")
        return 0

    anchor = "            return json.loads(out)"
    i = src.find(anchor)
    if i == -1:
        print("!! doctor() return anchor not found — cannot overlay")
        return 3

    shutil.copy(TARGET, BAK)

    # 1) inject overlay helpers BEFORE the doctor() function
    #    (anchor on 'def doctor():')
    d = src.find("def doctor():")
    if d == -1:
        shutil.copy(BAK, TARGET)
        print("!! def doctor() not found — restored backup")
        return 4
    src = src[:d] + OVERLAY.strip("\n") + "\n\n" + src[d:]

    # 2) route doctor()'s success return through the overlay
    src = src.replace(anchor, "            return _doctor_probe_overlay(json.loads(out))", 1)

    try:
        compile(src, TARGET, "exec")
    except SyntaxError as e:
        shutil.copy(BAK, TARGET)
        print(f"!! produced invalid syntax ({e}) — restored backup, nothing applied")
        return 5

    p.write_text(src, encoding="utf-8")
    print(f"  DOCTOR OVERLAY WIRED into {TARGET} (backup {BAK})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())