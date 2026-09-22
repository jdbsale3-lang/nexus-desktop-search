#!/usr/bin/env python3
"""wire-built-skills.py v2 — register estate_gmail_watcher + estate_security_probe
into /opt/zeus-skills.py.

Anchor strategy (fixture-corrected round 2):
  PRIMARY: any line containing "estate_status" (quote-agnostic — the earlier
           matched=0 came from searching only single-quote form; the real file,
           where register-into-zeus.py succeeded before, may use double quotes).
  If the primary anchor is absent or ambiguous: print the head of the file for
  diagnosis and REFUSE — never guess-write into an unknown shape.

Backup-first, compile-verified, idempotent. Usage (droplet): python3 wire-built-skills.py
"""
import shutil
import sys

TARGET = "/opt/zeus-skills.py"
BAK = TARGET + ".bak-skills-wire"
NEW_SKILLS = ["estate_gmail_watcher", "estate_security_probe"]


def main():
    try:
        src = open(TARGET).read()
    except FileNotFoundError:
        print(f"!! {TARGET} missing"); return 1
    lines = src.splitlines(keepends=True)

    # PRIMARY: lines mentioning estate_status in any quoting
    hits = [i for i, ln in enumerate(lines) if "estate_status" in ln]
    if len(hits) != 1:
        print(f"!! ANCHOR estate_status matched={len(hits)} — no write.")
        print("  Head of file for diagnosis:")
        for ln in lines[:25]:
            print("   |", ln.rstrip()[:100])
        print("  -> paste this head back to me and I will set the exact anchor.")
        return 3

    i = hits[0]
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