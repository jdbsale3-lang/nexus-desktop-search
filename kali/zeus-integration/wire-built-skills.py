#!/usr/bin/env python3
"""wire-built-skills.py — register estate_gmail_watcher + estate_security_probe
into /opt/zeus-skills.py. Mirrors register-into-zeus.py discipline: backup
first, single-anchor line insertion, compile-verified, refuses on ambiguity.
Usage (droplet): python3 wire-built-skills.py
"""
import shutil, sys

TARGET = "/opt/zeus-skills.py"
BAK = TARGET + ".bak-skills-wire"
NEW_SKILLS = ["estate_gmail_watcher", "estate_security_probe"]

def main():
    try:
        src = open(TARGET).read()
    except FileNotFoundError:
        print(f"!! {TARGET} missing"); return 1
    lines = src.splitlines(keepends=True)
    # find the skills registry: look for a line containing "'estate_status'" (existing anchor)
    anchors = [i for i, ln in enumerate(lines) if "'estate_status'" in ln or '"estate_status"' in ln]
    if len(anchors) != 1:
        print(f"!! ANCHOR_AMBIGUOUS matched={len(anchors)} — no write"); return 3
    i = anchors[0]
    indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
    shutil.copy(TARGET, BAK)
    inserted = 0
    for skill in NEW_SKILLS:
        if any(skill in ln for ln in lines):
            print(f"  already present: {skill}"); continue
        lines.insert(i + 1 + inserted, f"{indent}'{skill}',\n")
        inserted += 1
    out = "".join(lines)
    try:
        compile(out, TARGET, "exec")
    except SyntaxError as e:
        shutil.copy(BAK, TARGET)
        print(f"!! syntax error ({e}) — restored backup"); return 4
    open(TARGET, "w").write(out)
    print(f"  wired {inserted} skills (backup {BAK})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
