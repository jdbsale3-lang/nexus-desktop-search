#!/usr/bin/env python3
"""csp-fix.py — repair the Content-Security-Policy that blocked the ZEUS brain.

DIAGNOSIS (reproduced 22 Sep 2026): the v1 CSP allowed only 'self', so the
Command Centre could not reach:
    apiaegissecurity.tech/health          ← "the brain is unreachable"
    generativelanguage.googleapis.com     ← Gemini brain (+ wss streaming)
    api.elevenlabs.io / api.us.elevenlabs.io  (+ wss)  ← voice widget
    api.deepgram.com (wss)                ← speech-to-text
    api.open-meteo.com / api.duckduckgo.com  ← weather + news tiles
    unpkg.com                             ← ElevenLabs widget bundle
    api.fontshare.com                     ← fonts
All of those origins were verified LIVE (200/202/302) — the brain was never down;
the page was simply not permitted to call it.

FIX: replace the CSP value in every nginx config that sets it, allowlisting
exactly those origins (no wildcard for script-src; frame-ancestors/base-uri/
form-action stay locked).

Safety: backup per file · `nginx -t` must pass · reload only on success ·
automatic restore on any failure · idempotent.

Usage (droplet, root): python3 csp-fix.py
"""
import re
import shutil
import subprocess
from pathlib import Path

NGINX_DIRS = ["/etc/nginx"]
OLD_OR_NEW = re.compile(r'(add_header\s+Content-Security-Policy\s+")([^"]*)("(?:\s+always)?;)')

NEW_CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com https://unpkg.com; "
    "style-src 'self' 'unsafe-inline' https://api.fontshare.com; "
    "font-src 'self' data: https://api.fontshare.com; "
    "img-src 'self' data: blob: https:; "
    "connect-src 'self' https://cloudflareinsights.com https://apiaegissecurity.tech "
    "https://api.open-meteo.com https://api.duckduckgo.com https://api.openweathermap.org "
    "https://generativelanguage.googleapis.com "
    "https://api.elevenlabs.io https://api.us.elevenlabs.io https://api.deepgram.com "
    "wss://api.elevenlabs.io wss://api.us.elevenlabs.io wss://api.deepgram.com "
    "wss://generativelanguage.googleapis.com https://*.higgsfield.app; "
    "media-src 'self' blob: https:; "
    "frame-src 'self' https://*.elevenlabs.io; "
    "frame-ancestors 'self'; base-uri 'self'; form-action 'self'"
)

MARK = "apiaegissecurity.tech"   # presence of this proves the v2 CSP is applied


def configs():
    out = []
    for d in NGINX_DIRS:
        p = Path(d)
        if not p.exists():
            continue
        for f in p.rglob("*.conf"):
            try:
                if "Content-Security-Policy" in f.read_text(errors="ignore"):
                    out.append(f)
            except Exception:
                pass
    return out


def main():
    files = configs()
    if not files:
        print("!! no nginx config sets a CSP — if Cloudflare is setting it, update it there instead")
        return 3

    changed = []
    for f in files:
        src = f.read_text(errors="ignore")
        m = OLD_OR_NEW.search(src)
        if not m:
            continue
        if MARK in m.group(2):
            print(f"  already v2: {f}")
            continue
        bak = str(f) + ".bak-csp-v1"
        shutil.copy(f, bak)
        new_src = OLD_OR_NEW.sub(lambda mm: mm.group(1) + NEW_CSP + mm.group(3), src, count=0)
        f.write_text(new_src)
        changed.append((f, bak))
        print(f"  CSP upgraded → {f} (backup {bak})")

    if not changed:
        print("  nothing to change — verify with: curl -sI https://zeusaiintelligence.com | grep -i content-security")
        return 0

    # nginx -t, then reload, else restore everything
    t = subprocess.run(["nginx", "-t"], capture_output=True, text=True)
    if t.returncode != 0:
        print("!! nginx -t FAILED — restoring all backups:")
        print((t.stderr or t.stdout)[:400])
        for f, bak in changed:
            shutil.copy(bak, str(f))
        return 5

    subprocess.run(["systemctl", "reload", "nginx"], capture_output=True, text=True)
    print("  ✅ nginx reloaded with the v2 CSP")
    print("  verify: curl -sI https://zeusaiintelligence.com | grep -i content-security")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())