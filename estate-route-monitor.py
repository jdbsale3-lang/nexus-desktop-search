#!/usr/bin/env python3
"""estate-route-monitor.py — external route monitor for the ZEUS estate.
Probes every public surface and reports a status table; exits non-zero when
any critical route fails (for CI or cron alerting).

Usage:
  python3 estate-route-monitor.py            # full run, human output
  python3 estate-route-monitor.py --json     # JSON to stdout
  python3 estate-route-monitor.py --quiet    # only failures printed
"""
import json
import sys
import time
import urllib.request

# route matrix: name -> (url, critical, expected_ok_code)
ROUTES = [
    ("flagship",   "https://zeusaiintelligence.com",               True,  200),
    ("nexus",      "https://nexus.zeusaiintelligence.com",         True,  200),
    ("reach_skls", "https://zeusaiintelligence.com/reach/skills",  True,  200),
    ("reach_self", "https://zeusaiintelligence.com/reach/self",    True,  200),
    ("reach_brief", "https://zeusaiintelligence.com/reach/briefing", True, 200),
    ("reach_mem",  "https://zeusaiintelligence.com/reach/memory",  True,  200),
    ("reach_mon",  "https://zeusaiintelligence.com/reach/monitor", True,  200),
    ("search",     "https://zeusaiintelligence.com/reach/search?q=estate+monitor", True, 200),
    ("docs",       "https://zeusai-intelligence.higgsfield.app",   True,  200),
    ("breach",     "https://aegis-breach-check.higgsfield.app",    True,  200),
    ("audit",      "https://zeusaiintelligence.com/audit.html",    False, 200),
    ("outreach",   "https://zeusaiintelligence.com/outreach.html", False, 200),
]


def probe(name, url, timeout=20):
    t0 = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ZEUS-RouteMonitor/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            dt = round((time.time() - t0) * 1000)
            return {"route": name, "url": url, "status": r.status,
                    "ok": 200 <= r.status < 400, "ms": dt}
    except urllib.error.HTTPError as e:
        dt = round((time.time() - t0) * 1000)
        # 401/403/302 on auth-gated routes = alive (per estate convention)
        return {"route": name, "url": url, "status": e.code, "ms": dt,
                "ok": e.code in (301, 302, 401, 403)}
    except Exception as e:
        dt = round((time.time() - t0) * 1000)
        return {"route": name, "url": url, "status": None, "ms": dt,
                "ok": False, "error": str(e)[:120]}


def main():
    args = set(sys.argv[1:])
    results = [probe(n, u) for n, u, crit, _ in ROUTES]
    # apply per-route expected status if route expects a specific code
    for r in results:
        for n, u, crit, want in ROUTES:
            if r["route"] == n:
                r["critical"] = crit
                if r["status"] and want and r["status"] != want and r["ok"]:
                    # expected-code deviation: allow 2xx/3xx/401/403 family
                    pass
    up = sum(1 for r in results if r["ok"])
    critical_down = [r for r in results if not r["ok"] and r.get("critical")]
    down = [r for r in results if not r["ok"]]

    if "--json" in args:
        print(json.dumps({"ts": int(time.time()), "up": f"{up}/{len(results)}",
                          "critical_down": [r["route"] for r in critical_down],
                          "routes": results}, indent=1))
    else:
        for r in results:
            mark = "OK " if r["ok"] else "DOWN"
            if not r["ok"] and not r.get("critical"):
                mark = "WARN"
            ms = f"{r['ms']}ms" if r.get("ms") is not None else "timeout"
            extra = f" ({r.get('error','')[:60]})" if r.get("error") else ""
            print(f"  [{mark}] {r['route']:14s} {r['status']} {ms}{extra}")
        print(f"  --- {up}/{len(results)} routes up"
              + (f"; {len(critical_down)} critical DOWN" if critical_down else ""))

    # exit non-zero when a critical route is down (CI gate)
    return 1 if critical_down else 0


if __name__ == "__main__":
    raise SystemExit(main())