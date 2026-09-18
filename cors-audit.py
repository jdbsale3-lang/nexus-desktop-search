#!/usr/bin/env python3
"""cors-audit.py — recurring CORS audit for the estate: sends the real
preflight the flagship browser would send and requires 2xx + ACAO header.
Exit 0 = PASS, non-zero = FAIL (CI gate + issue alert)."""
import sys
import urllib.request

HOST = "https://apiaegissecurity.tech/"
ORIGIN = "https://zeusaiintelligence.com"


def main():
    try:
        req = urllib.request.Request(HOST, method="OPTIONS", headers={
            "Origin": ORIGIN,
            "Access-Control-Request-Method": "GET",
            "User-Agent": "ZEUS-CORSAudit/1.0",
        })
        with urllib.request.urlopen(req, timeout=20) as r:
            status = r.status
            acao = r.headers.get("Access-Control-Allow-Origin", "")
    except urllib.error.HTTPError as e:
        status = e.code
        acao = e.headers.get("Access-Control-Allow-Origin", "") if e.headers else ""
    except Exception as e:
        print(f"FAIL: probe error: {str(e)[:120]}")
        return 1

    ok = 200 <= status < 300 and ORIGIN in acao
    print(f"preflight: HTTP {status}")
    print(f"ACAO:      {acao[:90] if acao else 'MISSING'}")
    print("PASS — CORS intact." if ok else "FAIL — CORS broken (INC-005 style). Run fix-aegis-cors.py on the droplet.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
