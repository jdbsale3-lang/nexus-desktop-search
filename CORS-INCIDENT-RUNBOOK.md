# CORS INCIDENT RUNBOOK
## Detect, diagnose, fix, and verify cross-origin failures on the estate

**Version:** 1 · **Date:** 18 Sep 2026 · **Source incident:** INC-005 (AEGIS CORS)
**Applies to:** any estate host behind nginx serving a browser-facing API.

---

## 1. DETECTION (the estate already watches for you)

- **Route monitor** probes `aegis_cors` every 30 minutes: it sends a real OPTIONS
  preflight from `https://zeusaiintelligence.com` and requires **both** a 2xx
  response **and** `Access-Control-Allow-Origin` containing `zeusaiintelligence.com`.
- **Symptom on the flagship:** ACTIVITY logs
  `SYS: SHIELD: <service> unreachable (CORS/network)` while the service itself
  answers (check with curl — it is often *up*; only the browser call is blocked).
- **Green condition:** monitor shows `aegis_cors` OK. No manual check needed.

## 2. DIAGNOSIS (three commands, no guesswork)

```bash
# 1) is the API actually up? (a CORS issue only makes sense if this is 2xx)
curl -s -o /dev/null -w "GET: %{http_code}\n" https://<service>/

# 2) the CORS preflight the browser would send — THE decisive test
curl -s -o /dev/null -w "OPTIONS: %{http_code}\n" -X OPTIONS \
  -H "Origin: https://zeusaiintelligence.com" \
  -H "Access-Control-Request-Method: GET" \
  https://<service>/

# 3) does a normal response carry the ACAO header?
curl -s -D - -o /dev/null -H "Origin: https://zeusaiintelligence.com" https://<service>/ \
  | grep -i "access-control-allow-origin" || echo "NO ACAO HEADER"
```

| Finding | Verdict |
|---|---|
| GET 2xx + OPTIONS 400 + no ACAO | **CORS missing** — proceed to Fix |
| GET 2xx + OPTIONS 200/204 + ACAO present | **CORS is fine** — look elsewhere (network, DNS, Shield allowlist) |
| GET fails (5xx/timeout) | **not CORS** — service down, follow the general outage runbook |

## 3. FIX (nginx — the estate's standard front)

Find the server block, then add:

```nginx
add_header Access-Control-Allow-Origin "https://zeusaiintelligence.com" always;
add_header Access-Control-Allow-Methods "GET, POST, OPTIONS" always;
add_header Access-Control-Allow-Headers "Authorization, Content-Type" always;
add_header Access-Control-Max-Age 86400 always;

# preflight short-circuit (before auth):
if ($request_method = OPTIONS) { return 204; }
```

Apply + verify:
```bash
nginx -t && systemctl reload nginx
curl -s -o /dev/null -w "preflight=%{http_code}\n" -X OPTIONS \
  -H "Origin: https://zeusaiintelligence.com" -H "Access-Control-Request-Method: GET" \
  https://<service>/        # expect 204
```

Non-nginx alternatives (FastAPI/Flask/Express/Cloudflare) — see CORS-FIX-GUIDE.md §3.

## 4. VERIFY (green only when proven)

1. Preflight returns **204/200** (command above).
2. Normal GET with `Origin:` returns `access-control-allow-origin: https://zeusaiintelligence.com`.
3. Load the flagship — the `SYS: SHIELD: … unreachable (CORS/network)` line clears.
4. Next monitor cycle: `aegis_cors` shows **OK** (no manual recheck needed).

## 5. LOG THE INCIDENT

- If a new occurrence: create an entry via the incident skill
  (`/reach/skills?q=incident_create&title=CORS+…&severity=…&symptom=…`) — it issues
  the next INC-00x and auto-raises the Twilio alert lane for critical/major.
- Link the postmortem/guide in the entry. Rule: a route down >30 min without an
  index entry is itself an incident.

## 6. SECURITY (never skip)

- **Allowlist only** `https://zeusaiintelligence.com` — never `*` on a security/API host.
- If other legitimate clients exist, extend the explicit list rather than wildcarding.
- Keep `Access-Control-Allow-Headers` minimal (only what clients actually send).

## 7. RELATED DOCS

- CORS-FIX-GUIDE.md — full snippet library + the INC-005 record
- MONITOR-STATE.md — the 14-route matrix incl. `aegis_cors`
- INCIDENTS-INDEX.md — INC-005 entry and ledger rules

---
*All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).*