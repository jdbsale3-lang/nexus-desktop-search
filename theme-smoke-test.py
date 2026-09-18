#!/usr/bin/env python3
"""theme-smoke-test.py — CI smoke test for the ZEUS flagship theme system.
Fetches the live flagship HTML and asserts:
  1. the theme switcher marker (zeusThemeSel) is present
  2. all 6 theme palettes are defined (arc/ember/ocean/matrix/midnight/aurora)
  3. the apply/persist engine (window.zeusSetTheme + localStorage) is present
Exits non-zero on any missing piece → CI gate fails.
"""
import sys
import urllib.request

FLAGSHIP = "https://zeusaiintelligence.com/"
MARKERS = {
    "switcher select": "id=\"zeusThemeSel\"",
    "apply engine": "window.zeusSetTheme",
    "persist": "localStorage.setItem('zeusTheme'",
}
PALETTES = ["arc", "ember", "ocean", "matrix", "midnight", "aurora"]


def main():
    req = urllib.request.Request(FLAGSHIP, headers={"User-Agent": "ZEUS-ThemeSmoke/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            html = r.read().decode("utf-8", "replace")
    except Exception as e:
        print(f"FAIL: cannot fetch flagship: {str(e)[:120]}")
        return 1

    failures = []
    for label, marker in MARKERS.items():
        if marker not in html:
            failures.append(f"missing: {label} ({marker[:40]})")
        else:
            print(f"  OK  {label}")

    missing_palettes = [p for p in PALETTES if p not in html]
    if missing_palettes:
        failures.append(f"missing palettes: {missing_palettes}")
    else:
        print(f"  OK  {len(PALETTES)} palettes present")

    if failures:
        print("THEME SMOKE TEST FAILED:")
        for f in failures:
            print(f"   - {f}")
        return 1
    print("THEME SMOKE TEST PASSED — flagship theme system intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())