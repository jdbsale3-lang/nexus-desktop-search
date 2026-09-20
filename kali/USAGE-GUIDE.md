# Kali-AEGIS Linux — Expanded Usage Guide (v15)

The ZEUS estate Linux workstation: live on aegis-api, container `kali-aegis`
(image `kali-aegis:1.0`, trimmed build, ~4 GB, 22/22 tools verified).

---

## 1. Daily rhythm (5 commands, every day)

| You want | Run (on HOST) | Notes |
|---|---|---|
| Enter Kali | `docker exec -it kali-aegis bash` | prompt → `┌──(root㉿kali-aegis)` |
| Leave (keep running) | `exit` | container stays up |
| Re-enter | `docker exec -it kali-aegis bash` | same command, any time |
| Is it healthy? | `docker ps` | expect `Up (healthy)` |
| See resource use | `docker stats kali-aegis` | CPU/RAM live |

## 2. Scanning the estate (authorized targets only)

Inside Kali:
```bash
# quick flagship service scan (Cloudflare proxy: 80/443/8080/8443)
nmap -Pn -sV -sC -p 80,443,8080,8443 zeusaiintelligence.com

# full-port sweep (slow; behind Cloudflare most ports read filtered — a finding in itself)
nmap -Pn -sS -sV -sC -p- --min-rate 1200 zeusaiintelligence.com -oN /root/full-scan.txt
# copy results out to the host kit dir:
docker cp kali-aegis:/root/full-scan.txt ~/kali/

# estate scan hook (structured JSON, CLEAN/REVIEW verdict) — runs inside container
python3 /aegis/work/kali/kali-scan-hook.py https://zeusaiintelligence.com --tools all
```
**Rule:** estate-owned targets only (flagship, NEXUS, breach-check). Any other target needs explicit instruction — the estate's authorized-testing boundary.

## 3. Codebase intelligence (codebase-memory-mcp, 0.11.0)

On the HOST (binary at /root/.local/bin):
```bash
codebase-memory-mcp cli index_repository --repo-path /var/www/zeusaiintelligence.com   # index flagship (~12s)
codebase-memory-mcp cli list_projects --format json
codebase-memory-mcp cli search_graph   --help                      # real flags per tool
codebase-memory-mcp cli query_graph --project var-www-zeusaiintelligence.com \
  --query 'MATCH (f:Function) RETURN f.name LIMIT 15'
```
Already-indexed state: **340 nodes / 923 edges** (verified). The graph answers "what functions touch X", route inventories, dead code — feed results into the audit deck and `vulnerability-report-template.md`.

## 4. Rebuilding the image (rare) — ONLY via the guard

```bash
cd ~/kali && bash build-guard.sh
```
Refuses double-builds, refuses <20 GB free disk, builds nohup (tab-proof, honest EXIT), verifies image ≥3 GB. Never `docker build` directly.

## 5. Disk & health watchdogs

```bash
nohup bash /root/kali/disk-monitor.sh loop > /dev/null 2>&1 &   # WARN 15G / CRIT 8G
bash /root/kali/disk-monitor.sh once                            # one-off check
docker system prune -a -f                                       # reclaim (never during a build)
```

## 6. Personas & skills

- **279 agency-agents personas** → `/root/.claude/agents` (Claude Code on host)
- **5 estate-adapted personas** → `~/kali/agency-personas/` (01 code-reviewer … 05 devops-automator)
- **ZEUS skills:** `zeus_kali_ops` (status/scan/tooltest/mcpindex/launch) registered into
  `/opt/zeus-skills.py`; `estate-codebase-index` skill documented in ZEUS context.
- Speak to ZEUS: "is Linux up", "scan the flagship", "run the tool test", "index the codebase".

## 7. Key files & protection rules (do not change)

| File | Purpose | Must stay |
|---|---|---|
| `~/kali/build-guard.sh` | rebuild guard | used for ALL rebuilds |
| `~/kali/disk-monitor.sh` | disk watchdog | running |
| `~/kali/docker-compose.yml` | container config | `pull_policy: missing`; NET_RAW + NET_ADMIN; seccomp + apparmor unconfined |
| `~/kali/tool-smoke-test.sh` | 22-tool verification | run inside container |
| `~/kali/KALI-RUNBOOK.md` | incident history INC-001…006 | reference |
| `~/kali/TOOLSET-STATUS.md` | tool inventory | reference |

## 8. Troubleshooting

- **nmap "Operation not permitted"** → container lacks caps: recreate via compose (caps are in the file).
- **smoke FAIL missing** → tool absent in image; CI gate (`Kali Build Test`) catches these before shipping.
- **smoke FAIL timeout** → first-run postgres/msfdb init; rerun after 60s.
- **disk < 15G** → prune + consider volume growth (DO console: resize to 80G, then `growpart /dev/vda 1 && resize2fs /dev/vda1`).
- **MCP "unknown tool"** → use real names: `index_repository`, `list_projects`, `search_graph`, `trace_path`, `query_graph`.

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).