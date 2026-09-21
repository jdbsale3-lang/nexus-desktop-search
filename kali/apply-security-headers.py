#!/usr/bin/env python3
"""apply-security-headers.py — insert the five flagship security headers into
the nginx server block for zeusaiintelligence.com, ON THE DROPLET.
Self-contained: locates config, backs up (outside sites-enabled — INC-005
lesson), inserts after server_name, tests, reloads, self-verifies.

Usage (droplet console, root):
  python3 apply-security-headers.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

HOST = "zeusaiintelligence.com"
SITES = "/etc/nginx/sites-enabled"
HEADERS = """    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://cloudflareinsights.com; frame-ancestors 'self'; base-uri 'self'; form-action 'self'" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), interest-cohort=()" always;
    server_tokens off;
"""


def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def main():
    if not Path(SITES).is_dir():
        print(f"!! {SITES} not found — wrong host?")
        return 1

    # locate config(s) mentioning the host
    targets = []
    for p in sorted(Path(SITES).glob("*")):
        try:
            if HOST in p.read_text(encoding="utf-8", errors="replace"):
                targets.append(p)
        except Exception:
            continue
    # keep only real sites (skip backups) — nginx includes every file, so
    # ignore anything not ending in a normal conf-ish suffix list
    targets = [p for p in targets if not p.name.endswith((".bak", ".bak-inc005", "~"))]
    if not targets:
        print(f"!! no config mentioning {HOST} under {SITES}")
        print("   grep -rl zeusaiintelligence /etc/nginx/ to locate it manually")
        return 1

    marker = "# zEUS-SEC-HEADERS (applied 2026-09-21)"
    for target in targets:
        text = target.read_text(encoding="utf-8", errors="replace")
        if marker in text:
            print(f"  {target.name}: already patched — verify only")
            continue
        # backup OUTSIDE sites-enabled (INC-005 lesson: no .bak in include path)
        backup_dir = Path("/root/nginx-backups")
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup = backup_dir / f"{target.name}.sec-headers"
        shutil.copy(target, backup)

        idx = text.find(HOST)
        # find the server_name directive's end; insert the headers right after it
        sn_end = text.find("\n", text.rfind("server_name", 0, idx))
        if sn_end == -1:
            print(f"!! could not anchor server_name in {target.name} — manual edit")
            return 1
        block = f"\n{marker}\n" + HEADERS
        text = text[: sn_end + 1] + block + text[sn_end + 1:]
        target.write_text(text, encoding="utf-8")
        print(f"  {target.name}: headers inserted (backup {backup})")

    t = run("nginx -t 2>&1")
    print(t.stdout.strip() or t.stderr.strip())
    if t.returncode != 0:
        print("!! nginx -t FAILED — restoring backups")
        for target in targets:
            bak = Path("/root/nginx-backups") / f"{target.name}.sec-headers"
            if bak.exists():
                shutil.copy(bak, target)
        return 1

    run("systemctl reload nginx 2>&1")
    print("  nginx reloaded")

    # self-verify from the wire
    out = run("curl -sI https://zeusaiintelligence.com")
    got = 0
    for h in ("strict-transport-security", "content-security-policy",
              "x-content-type-options", "referrer-policy", "permissions-policy"):
        if h in out.stdout.lower():
            got += 1
    print(f"  verified headers on wire: {got}/5")
    print("RESULT:", "PASS — flagships hardened" if got == 5 else f"PARTIAL {got}/5 — check nginx include of the config")
    return 0 if got == 5 else 2


if __name__ == "__main__":
    raise SystemExit(main())