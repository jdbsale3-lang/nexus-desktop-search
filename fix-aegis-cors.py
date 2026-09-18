#!/usr/bin/env python3
"""fix-aegis-cors.py — apply the INC-005 CORS fix to the apiaegissecurity.tech
nginx server block ON THE DROPLET. Self-contained: backs up, inserts directives,
tests (nginx -t), reloads, and self-verifies with real preflight + ACAO checks.

Usage (droplet console, root):
  python3 fix-aegis-cors.py
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

HOST = "apiaegissecurity.tech"
ORIGIN = "https://zeusaiintelligence.com"
SITES = "/etc/nginx/sites-enabled"
DIRECTIVES = """    add_header Access-Control-Allow-Origin "https://zeusaiintelligence.com" always;
    add_header Access-Control-Allow-Methods "GET, POST, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Authorization, Content-Type" always;
    add_header Access-Control-Max-Age 86400 always;
    if ($request_method = OPTIONS) { return 204; }
"""


def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def main():
    if not Path(SITES).is_dir():
        print(f"!! {SITES} not found — wrong host?")
        return 1

    # find the config file that mentions the host
    target = None
    for p in sorted(Path(SITES).glob("*")):
        try:
            if HOST in p.read_text(encoding="utf-8", errors="replace"):
                target = p
                break
        except Exception:
            continue
    if target is None:
        print(f"!! no nginx config mentioning {HOST} under {SITES}")
        print(f"   grep -rl {HOST} /etc/nginx/  to locate it; then re-run.")
        return 1
    print(f"config: {target}")

    # already patched?
    text = target.read_text(encoding="utf-8", errors="replace")
    if "zEUS-CORS-FIX" in text:
        print("  already patched — verifying only")
    else:
        backup = f"{target}.bak-inc005"
        shutil.copy(target, backup)
        print(f"backup: {backup}")
        marker = "\n# zEUS-CORS-FIX (INC-005)\n" + DIRECTIVES
        # insert after the server block's opening brace (first { of the block
        # containing HOST)
        idx = text.find(HOST)
        brace = text.rfind("{", 0, idx)
        if brace == -1:
            print("!! server block brace not found — manual edit (see CORS-FIX-GUIDE.md)")
            return 1
        text = text[: brace + 1] + marker + text[brace + 1:]
        target.write_text(text, encoding="utf-8")
        print("  directives inserted")

    t = run("nginx -t 2>&1")
    print(t.stdout.strip() or t.stderr.strip())
    if t.returncode != 0:
        print("!! nginx -t FAILED — restoring backup")
        shutil.copy(f"{target}.bak-inc005", target)
        return 1
    r = run("systemctl reload nginx 2>&1")
    print("  nginx reloaded (or said:", r.stderr.strip()[:80], ")")

    # self-verify
    p = run(f'curl -s -o /dev/null -w "%{{http_code}}" -X OPTIONS '
            f'-H "Origin: {ORIGIN}" -H "Access-Control-Request-Method: GET" '
            f"https://{HOST}/")
    h = run(f'curl -s -D - -o /dev/null -H "Origin: {ORIGIN}" https://{HOST}/ '
            "| grep -i access-control-allow-origin")
    code = p.stdout.strip()
    acao = h.stdout.strip() or ""
    print(f"preflight: HTTP {code}")
    print(f"ACAO:      {acao[:90] if acao else 'MISSING'}")
    ok = code in ("200", "204") and ORIGIN in acao
    print("RESULT:", "PASS — INC-005 resolved" if ok else "FAIL — check config")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())