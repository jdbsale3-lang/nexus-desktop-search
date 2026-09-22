# ZEUS-SKILL: estate_security_probe.py
# Live estate probe: surfaces, security headers, CORS preflight, reach engine.
import urllib.request
import urllib.error

SKILL = {
    "name": "estate_security_probe",
    "description": "Probe the estate: surfaces, 5 security headers, CORS preflight, reach self/monitor",
    "category": "security",
    "inputs": {},
    "entry": "run_skill",
}

SURFACES = [
    "https://zeusaiintelligence.com",
    "https://nexus.zeusaiintelligence.com",
    "https://apiaegissecurity.tech",
    "https://aegis-breach-check.higgsfield.app",
    "https://zeusai-intelligence.higgsfield.app",
]
HEADER_KEYS = ["strict-transport-security", "content-security-policy",
               "x-content-type-options", "referrer-policy", "permissions-policy"]


def _get(url, timeout=20, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "ZEUS-Skills/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read(400)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), b""
    except Exception as e:
        return None, {}, str(e).encode()[:120]


def run_skill(ctx):
    out = {"surfaces": {}, "headers": {}, "cors": {}, "reach": {}}

    for u in SURFACES:
        code, _, body = _get(u)
        # alive definition used across the estate: 2xx/3xx/401/403 = alive
        alive = code is not None and (200 <= code < 400 or code in (401, 403))
        out["surfaces"][u] = {"status": code, "alive": alive,
                              "note": "" if code not in (503,) else "app temporarily unavailable"}

    code, hdr, _ = _get("https://zeusaiintelligence.com")
    present = [k for k in HEADER_KEYS if k in {k2.lower() for k2 in hdr}]
    out["headers"] = {"count": f"{len(present)}/5", "present": present}

    # CORS preflight
    try:
        req = urllib.request.Request("https://apiaegissecurity.tech/", method="OPTIONS",
                                     headers={"Origin": "https://zeusaiintelligence.com",
                                              "Access-Control-Request-Method": "GET"})
        with urllib.request.urlopen(req, timeout=20) as r:
            out["cors"] = {"preflight": r.status}
    except urllib.error.HTTPError as e:
        out["cors"] = {"preflight": e.code}
    except Exception as e:
        out["cors"] = {"preflight": None, "error": str(e)[:80]}

    for route in ("self", "monitor"):
        code, _, body = _get(f"https://zeusaiintelligence.com/reach/{route}")
        out["reach"][route] = {"status": code, "body": body[:80].decode("utf-8", "replace")}

    up = sum(1 for v in out["surfaces"].values() if v["alive"])
    return {"ok": True, "surfaces_up": f"{up}/{len(SURFACES)}",
            "headers": out["headers"]["count"], "cors": out["cors"].get("preflight"),
            "reach": {k: v["status"] for k, v in out["reach"].items()},
            "detail": out}