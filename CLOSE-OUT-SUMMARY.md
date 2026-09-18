# ZEUS ESTATE — CLOSE-OUT SUMMARY
## Final state of the estate, what remains, and the housekeeping note (18 Sep 2026)

**Purpose:** one document stating exactly where the estate stands — verified green,
what is queued for you, and the maintenance note that affects CI in the next week.

---

## 1. VERIFIED GREEN (external probes, 18 Sep 2026)

| Surface | Status |
|---|---|
| ZEUS flagship (themes + allowlist live) | 200 · zeusThemeSel: 2 · theme smoke test PASS |
| NEXUS engine | 200 |
| Reach /skills · /self · /briefing · /memory · /monitor · /search · /doctor · /v2ex · /rss | 200 (search = exa-mcp:web_search_exa real results) |
| Audit · Outreach · analytics.json | 200 |
| Docs site | 200 (all runbooks/status reports indexed) |
| AEGIS Breach Check | 200 |
| Skills engine | 25 loaded · 0 broken |
| Exa suite | GREEN end-to-end (search + research + exa_search + self) |
| CI (GitHub) | 13-route monitor + theme smoke + Exa discovery/rollback, every 30 min |
| GitHub workflows | pushed, Contents + Workflows permissions live |

## 2. OPEN — YOUR SIDE (three items)

| # | Item | Where | Reference |
|---|---|---|---|
| INC-005 | Add CORS headers to apiaegissecurity.tech (preflight 400 → 204 + Allow-Origin) | AEGIS host | CORS-FIX-GUIDE.md |
| VOICE | Set Deepgram + ElevenLabs keys, then "voice lane on" | flagship browser | VOICE-LANE-SETUP.md |
| PAT | Delete the old `github_pat_11CFR4ZIA0k0…` (still active) | GitHub → fine-grained tokens | previous report |

## 3. MAINTENANCE NOTE — Node20 EOL (from GitHub, applies to our CI)

GitHub Action's Node20 reaches EOL **September 23, 2026** (removal date in the
editor's note you shared). Our workflows use `actions/checkout@v4`,
`actions/setup-python@v5`, `actions/upload-artifact@v4` — all already run on
Node24-capable runner versions, and the runner v2.328.0+ defaults actions to Node24
from June 16, 2026. **Recommended before Sep 23:** verify the pinned action versions
are current (they are), and no workflow sets
`ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION` (none does). If a red
"Node20 is deprecated" warning appears on a run, bump the action major version —
no other change is expected because all three of our actions are the current majors.

## 4. INCIDENT LEDGER (published live)

| INC | Summary | State |
|---|---|---|
| INC-001 | Exa key-format guard rejected UUID keys | RESOLVED |
| INC-002 | Wrong Exa MCP tool names | RESOLVED |
| INC-003 | Skills routes wiped by v7 deploy | RESOLVED |
| INC-004 | Route monitor outage detection | OPEN (monitoring) |
| INC-005 | AEGIS CORS misconfiguration | OPEN (fix documented, monitor watching) |

## 5. WHAT SHIPPED THIS SESSION (kit trail)

- zeusai-exa-hotfix-v7 / v7.1 / v7.2 — guard, tool names, pre-patched bridge
- zeusai-fix-v8.1-clean — /skills query forwarding fix
- zeusai-noanswer-fix-kit — flagship themes + allowlist (+6 origins)
- zeusai-route-monitor / zeusai-voice-incident / zeusai-exa-validation kits
- CI on GitHub: estate-route-monitor.yml (+ theme smoke + aegis_cors) ,
  mcp-discovery-test.yml, workflows/ visibility copies

## 6. THE ONE-PAGE OPERATOR COMMANDS

```bash
# estate health (any machine)
curl -s https://zeusaiintelligence.com/reach/self | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['skills_loaded'],'skills');print('exa ready:', 'exa_search' in [c['channel'] for c in d['channels_ready']])"
# CORS monitor (expect aegis_cors DOWN until INC-005 fixed)
curl -s https://zeusai-intelligence.higgsfield.app/INCIDENTS-INDEX.md | grep -c INC-005
# full sweep
python3 estate-route-monitor.py
```

---

*All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).*