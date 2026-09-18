# ESTATE ROUTE MONITOR — CURRENT STATE
## Status snapshot, alerting topology, and the INC-005 item (18 Sep 2026)

**Monitored from:** GitHub Actions CI (independent of the droplet) · **Cadence:** every 30 minutes
**Workflow:** `.github/workflows/estate-route-monitor.yml` (`Estate Route Monitor`, registered **active**)

---

## 1. ROUTE MATRIX — 14 probes

| Route | Target | Critical | Current (19:21 UTC) |
|---|---|---|---|
| flagship | zeusaiintelligence.com | yes | 200 OK |
| flagship_deploy | zeusaiintelligence.com (HTML has `zeusThemeSel`) | yes | 200 OK |
| nexus | nexus.zeusaiintelligence.com | yes | 200 OK |
| reach_skls | /reach/skills | yes | 200 OK |
| reach_self | /reach/self | yes | 200 OK |
| reach_brief | /reach/briefing | yes | 200 OK |
| reach_mem | /reach/memory | yes | 200 OK |
| reach_mon | /reach/monitor | yes | 200 OK |
| search | /reach/search (Exa) | yes | 200 OK |
| docs | zeusai-intelligence.higgsfield.app | yes | 200 OK |
| breach | aegis-breach-check.higgsfield.app | yes | 200 OK |
| `aegis_cors` | apiaegissecurity.tech (OPTIONS preflight + ACAO header) | yes | **DOWN — INC-005** |
| audit | /audit.html | no | 200 OK |
| outreach | /outreach.html | no | 200 OK |

**Live result:** 13/14 up · 1 critical DOWN (`aegis_cors` = INC-005, expected until CORS lands).

## 2. WHAT EACH SPECIAL PROBE VERIFIES

- **flagship_deploy** — fetches the flagship HTML and requires the theme-switcher
  marker (`zeusThemeSel`); catches a reverted patch before users notice.
- **aegis_cors** — sends a real OPTIONS preflight from `https://zeusaiintelligence.com`
  and requires BOTH a 2xx response AND `Access-Control-Allow-Origin` containing
  `zeusaiintelligence.com`. A plain GET 200 proves nothing — this is why the route
  stays red until the nginx CORS header exists.

## 3. ALERTING TOPOLOGY (two distinct lanes)

| Failure class | Job | Trigger | Action |
|---|---|---|---|
| **Route down** (any critical route) | `monitor` → Alert step | `critical_down > 0` | `gh issue create` — ESTATE ALERT: critical route(s) down, evidence attached |
| **Workflow failure** (job crash, infra, action error) | `monitor-failure-alert` | `always() && needs.monitor.result == 'failure'` | `gh issue create` — ESTATE ALERT: route-monitor workflow FAILED, run/commit/job + triage checklist |

Both lanes produce artifacts (monitor_out.txt, issue_body.md) on every run.

## 4. E2E VALIDATION PERFORMED (18 Sep, 19:21 UTC)

Simulated the runner environment exactly (GITHUB_RUN_ID, GITHUB_SHA, GITHUB_JOB,
GITHUB_REPOSITORY) and executed `compose_failure_alert.py`: the issue body
rendered with correct run link, short commit, job name, timestamp, and the
four-step triage list (theme smoke / run monitor / report status / alert).
Job wiring verified on main: `needs: monitor` · `if: always() && needs.monitor.result == 'failure'`
· steps [checkout, Compose failure-body, File failure issue, Upload failure alert body].

## 5. INC-005 — aegis_cors (the single DOWN)

- **Root cause (proven):** `apiaegissecurity.tech` (same droplet 188.166.175.149,
  nginx 1.24.0 Ubuntu) answers GET 200 but OPTIONS preflight 400 with no
  `Access-Control-Allow-Origin` — the flagship browser call is blocked.
- **Fix location:** nginx server block for apiaegissecurity.tech ON THE DROPLET.
- **Complete guide:** CORS-FIX-GUIDE.md (published) — snippet + reload + verify.
- **Green condition:** monitor's `aegis_cors` shows OK automatically after the fix.

## 6. MAINTENANCE NOTES

- **Node24 enforced** (`FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: 'true'` on the workflow);
  run logs confirm actions are forced to Node24 (Node20 EOL Sep 23 2026).
- **Secrets:** `EXA_KEY` (discovery workflow) — not set; see Exa suite status.
- **Token:** old zeusai PAT revoked (401); active `zeus-ci-v2` in use.

---
*All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).*