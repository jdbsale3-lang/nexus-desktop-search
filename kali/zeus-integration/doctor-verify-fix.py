#!/usr/bin/env python3
"""doctor-verify-fix.py — flip github + exa_search to 'ok' in the ZEUS Doctor.

The Doctor currently reports warn because it refuses side-effecting checks
(gh auth status writes device-id; it won't start the mcporter service). Both
channels provably work via no-write probes (verified HTTP 200). This patch
gives the Doctor the read-only verification path.

Usage (on droplet): python3 doctor-verify-fix.py  /  or wire as a doctor probe.
"""
import json
import subprocess
import urllib.request

GITHUB_TOKEN = ""  # leave "" to read from env: GITHUB_TOKEN / GH_TOKEN
EXA_KEY = ""       # leave "" to read from env: EXA_API_KEY


def p_github():
    tok = GITHUB_TOKEN or __import__("os").environ.get("GITHUB_TOKEN") or __import__("os").environ.get("GH_TOKEN", "")
    if not tok:
        return {"status": "warn", "reason": "no token in env or config"}
    req = urllib.request.Request("https://api.github.com/user",
                                 headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return {"status": "ok" if r.status == 200 else "warn", "http": r.status, "reason": "no-write read probe passed"}
    except Exception as e:
        return {"status": "warn", "reason": str(e)}


def p_exa():
    key = EXA_KEY or __import__("os").environ.get("EXA_API_KEY", "")
    if not key:
        return {"status": "warn", "reason": "no exa key in env or config"}
    body = json.dumps({"query": "zeus ai", "numResults": 1}).encode()
    req = urllib.request.Request("https://api.exa.ai/search", data=body,
                                 headers={"x-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return {"status": "ok" if r.status == 200 else "warn", "http": r.status, "reason": "REST ping passed (no side effects)"}
    except Exception as e:
        return {"status": "warn", "reason": str(e)}


if __name__ == "__main__":
    print(json.dumps({"github": p_github(), "exa_search": p_exa()}, indent=2))
