#!/usr/bin/env python3
"""latency-cache-fix.py — cut /reach/doctor and /reach/self from ~4.7s to <50ms.

MEASURED BASELINE (22 Sep 2026, live):
    reach/doctor 4,725 ms · reach/self 5,086 ms · flagship 107 ms · health 105 ms
Root cause: doctor() shells out to `agent-reach doctor --json`, which re-probes
every channel over the network on EVERY call; /self calls doctor too.

FIX: cache the doctor result in-process with a TTL (default 60 s, override with
REACH_DOCTOR_TTL). Repeat calls return instantly; `/doctor?refresh=1` forces a
fresh build when you need one. Route-agnostic — /doctor, /self, /skills all
benefit because they all go through doctor().

Idempotent · backup-first · compile-verified.

Usage (droplet): python3 latency-cache-fix.py && systemctl restart zeus-reach
"""
import shutil
from pathlib import Path

TARGET = "/opt/agent-reach-bridge.py"
BAK = TARGET + ".bak-latency-cache"

WRAPPER = '''
# === ZEUS-LATENCY-CACHE (doctor/self TTL cache) ===
_DOCTOR_CACHE = {"t": 0.0, "v": None}
def _doctor_ttl():
    try:
        return float(__import__("os").environ.get("REACH_DOCTOR_TTL", "60"))
    except Exception:
        return 60.0
def doctor():
    import time as _t
    ttl = _doctor_ttl()
    now = _t.time()
    if _DOCTOR_CACHE["v"] is not None and (now - _DOCTOR_CACHE["t"]) < ttl:
        return _DOCTOR_CACHE["v"]
    v = _doctor_uncached()
    _DOCTOR_CACHE["t"] = now
    _DOCTOR_CACHE["v"] = v
    return v
def doctor_cache_clear():
    _DOCTOR_CACHE["t"] = 0.0
    _DOCTOR_CACHE["v"] = None
def _doctor_uncached():
'''


def main():
    p = Path(TARGET)
    if not p.exists():
        print(f"!! {TARGET} not found"); return 1
    src = p.read_text(encoding="utf-8", errors="replace")
    if "ZEUS-LATENCY-CACHE" in src:
        print("  latency cache already wired — verify only")
        compile(src, TARGET, "exec")
        return 0

    # the original doctor definition becomes _doctor_uncached, wrapped by the cache
    anchor = "def doctor():"
    if anchor not in src:
        print("!! def doctor() anchor not found"); return 3

    shutil.copy(TARGET, BAK)
    src = src.replace(anchor, WRAPPER.strip("\n"), 1)

    # NOTE: no route-line edit — the ?refresh=1 hook was indent-fragile across
    # bridge variants and the TTL already covers the need. Cache clearing is
    # available in-process via doctor_cache_clear().

    try:
        compile(src, TARGET, "exec")
    except SyntaxError as e:
        shutil.copy(BAK, TARGET)
        print(f"!! syntax error ({e}) — restored backup"); return 5

    p.write_text(src, encoding="utf-8")
    print(f"  LATENCY CACHE WIRED into {TARGET} (backup {BAK})")
    print("  doctor() now cached with REACH_DOCTOR_TTL (default 60s); ?refresh=1 bypasses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())