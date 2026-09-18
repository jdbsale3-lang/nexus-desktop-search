# ZEUS ESTATE — INCIDENT INDEX
## Every incident, root cause, fix, and postmortem — one ledger

**Maintained by:** ZEUS AI operations · **Established:** 18 Sep 2026
**Monitor:** estate-route-monitor.py probes the estate every 30 min via CI.
**Rule:** an incident is recorded when a live surface regresses or a defect in
ZEUS tooling blocks a production lane. Postmortems are published on the docs site.

---

## INC-001 — Exa key-format guard rejected valid keys (RESOLVED)
- **Date:** 2026-09-18 · **Severity:** Major (blocked Exa integration)
- **Symptom:** every key attempt returned `KEY LOOKS WRONG` or server 403; Exa lane red.
- **Root cause:** `mcp-discovery.py` guard demanded an `sk-` prefix. Exa API keys are
  **UUID-format** — the guard refused valid-format keys before they reached the server.
- **Fix:** guard accepts UUID or `sk-`; proven with synthetic UUID (reaches server).
- **Artifacts:** [HOTFIX-V7-CHANGELOG.md](https://zeusai-intelligence.higgsfield.app/HOTFIX-V7-CHANGELOG.md) · fix shipped in kits v7/v7.1/v7.2.

## INC-002 — Wrong Exa MCP tool names (RESOLVED)
- **Date:** 2026-09-18 · **Severity:** Major (companion to INC-001)
- **Symptom:** bridge tried `web_search`, `search`, `web_search_with_context` — none exist.
- **Root cause:** canonical Exa tools are `web_search_exa` / `web_fetch_exa`; our
  candidate lists predated the docs.
- **Fix:** `web_search_exa` first in `agent-reach-bridge.py` + `zeus-reach-mcp.py`.
- **Artifacts:** HOTFIX-V7-CHANGELOG.md (Defect 2).

## INC-003 — Skills routes wiped by v7 deploy (RESOLVED)
- **Date:** 2026-09-18 · **Severity:** Medium (console routes offline ~1 deploy cycle)
- **Symptom:** `/reach/skills` → 404 after v7 deploy; other routes unaffected.
- **Root cause:** kit v7 shipped the **unpatched** bridge; deploy overwrote the file
  carrying the injected skills routes; deploy block omitted the re-patch step.
- **Detection:** external probe after deploy (QA gate). **Fix:** re-run
  `patch-zeus-skills.py` + restart; kit v7.2 ships the **pre-patched** bridge.
- **Postmortem:** [V72-REGRESSION-POSTMORTEM.md](https://zeusai-intelligence.higgsfield.app/V72-REGRESSION-POSTMORTEM.md)

## INC-004 — External route monitor outage detection (OPEN — monitoring)
- **Date:** 2026-09-18 · **Severity:** Preventive
- **Action:** estate-route-monitor.py added (12 routes, CI every 30 min, gates on
  critical failure). Any future regression is caught within 30 minutes and recorded
  here as INC-00x.

---

## INC-005 — AEGIS API unreachable from flagship: CORS misconfiguration (OPEN)
- **Date:** 2026-09-18 · **Severity:** Major (console flag, repeated)
- **Symptom:** flagship ACTIVITY repeatedly logs `SYS: SHIELD: AEGIS unreachable (CORS/network)`.
- **Diagnosis (verified):** AEGIS API at **apiaegissecurity.tech** is **UP** (GET → 200,
  `{"service":"AEGIS AI Security Platform","version":"1.0.0",...}`), but:
  - OPTIONS preflight → **HTTP 400**
  - No `Access-Control-Allow-Origin` header on responses
  → the flagship browser's cross-origin call is blocked before it starts.
- **Fix (AEGIS host side):** add CORS headers on apiaegissecurity.tech
  (`Access-Control-Allow-Origin: https://zeusaiintelligence.com`, handle
  OPTIONS preflight with 204 + allow-methods/headers), then re-test preflight.
  **Automated fixer:** `python3 fix-aegis-cors.py` on the droplet (self-contained,
  idempotent, backs up config, tests + reloads + self-verifies).
- **Runbook:** [CORS-INCIDENT-RUNBOOK.md](https://zeusai-intelligence.higgsfield.app/CORS-INCIDENT-RUNBOOK.md)
  — detect/diagnose/fix/verify any future cross-origin failure on the estate.
- **Verify:** `curl -X OPTIONS -H "Origin: https://zeusaiintelligence.com" -H "Access-Control-Request-Method: GET" https://apiaegissecurity.tech/` → expect 204/200 + `access-control-allow-origin`.
- **Monitor:** estate route monitor probes the API (200) and `aegis_cors` every
  30 min; a dedicated **cors-audit** CI workflow runs the full preflight+header
  audit daily and files an issue on failure.

## Ledger rules
1. Every incident gets a number, date, severity, symptom, root cause, fix, artifact link.
2. Postmortems are public docs; secrets never appear in index or postmortem.
3. A route down for >30 min without an index entry is a monitoring failure — itself an incident.

*All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).*