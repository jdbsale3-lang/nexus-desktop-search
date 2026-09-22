#!/usr/bin/env python3
"""doctor-overlay-fix.py v2 — CORRECTED to the REAL doctor structure.

PROVEN FROM THE LIVE WIRE: /reach/doctor returns {"ok":true,"doctor":{
"github":{...},"exa_search":{...}, ...}} — channels live DIRECTLY under
`doctor`, NOT under a "channels" key. v1 looked for doctor["channels"], so the
overlay silently did nothing (exactly what the droplet showed: overlay WIRED,
wire still warn).

v2 handles BOTH shapes (direct keys, and a nested "channels" dict if present),
so it is correct for this bridge and future-proof.

Usage (droplet): python3 doctor-overlay-fix.py   (idempotent)
"""
import shutil
from pathlib import Path

TARGET = "/opt/agent-reach-bridge.py"
BAK = TARGET + ".bak-doctor-overlay"

OVERLAY = '''
# === ZEUS-DOCTOR-OVERLAY v2 (no-write truth on /reach/doctor) ===
# Live structure: {"ok":true,"doctor":{"github":{...},"exa_search":{...}}}
# Channels are DIRECT keys under doctor (no "channels" wrapper).
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
def _overlay_channels(chmap):
    if not isinstance(chmap, dict):
        return
    g = _probe_github_token()
    if g == 200:
        chmap["github"] = {"status": "ok", "via": "no-write probe (HTTP 200)"}
    e = _probe_exa_key()
    if e == 200:
        chmap["exa_search"] = {"status": "ok", "via": "no-write probe (HTTP 200)"}
def _doctor_probe_overlay(d):
    if not isinstance(d, dict):
        return d
    _overlay_channels(d)                 # v2: channels are direct keys (live shape)
    _overlay_channels(d.get("channels")) # future-proof: nested shape too
    return d
'''


def main():
    p = Path(TARGET)
    if not p.exists():
        print(f"!! {TARGET} not found"); return 1
    src = p.read_text(encoding="utf-8", errors="replace")

    # upgrade an existing v1 overlay in place
    if "ZEUS-DOCTOR-OVERLAY v2" in src:
        print("  overlay v2 already wired — verify only")
        compile(src, TARGET, "exec")
        return 0
    if "ZEUS-DOCTOR-OVERLAY" in src:
        print("  v1 overlay found — upgrading to v2 (structure-correct)")
        # replace the v1 block: from the marker to the end of _doctor_probe_overlay
        start = src.find("# === ZEUS-DOCTOR-OVERLAY")
        end = src.find("def doctor():")
        if start == -1 or end == -1 or end < start:
            print("!! could not locate v1 block bounds"); return 4
        shutil.copy(TARGET, BAK)
        src = src[:start] + OVERLAY.strip("\n") + "\n\n" + src[end:]
        try:
            compile(src, TARGET, "exec")
        except SyntaxError as e:
            shutil.copy(BAK, TARGET)
            print(f"!! syntax error ({e}) — restored"); return 5
        p.write_text(src, encoding="utf-8")
        print(f"  OVERLAY UPGRADED to v2 (backup {BAK})")
        return 0

    anchor = "            return json.loads(out)"
    i = src.find(anchor)
    if i == -1:
        print("!! doctor() return anchor not found"); return 3
    d = src.find("def doctor():")
    if d == -1:
        print("!! def doctor() not found"); return 6

    shutil.copy(TARGET, BAK)
    src = src[:d] + OVERLAY.strip("\n") + "\n\n" + src[d:]
    src = src.replace(anchor, "            return _doctor_probe_overlay(json.loads(out))", 1)
    try:
        compile(src, TARGET, "exec")
    except SyntaxError as e:
        shutil.copy(BAK, TARGET)
        print(f"!! syntax error ({e}) — restored"); return 5
    p.write_text(src, encoding="utf-8")
    print(f"  DOCTOR OVERLAY v2 WIRED (backup {BAK})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())