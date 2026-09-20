# ZEUS AI — Kali/Linux Capability Briefing (load into ZEUS memory/context)

**What ZEUS now has:** a dedicated Kali Linux security workstation running on
the estate droplet (aegis-api), container `kali-aegis` from image
`kali-aegis:1.0` (trimmed build, ~4 GB, all tools verified). Nmap live and
mapping the flagship (Cloudflare proxy: 80/443/8080/8443).

## Speak to it (host commands; ZEUS drives via zeus_kali_ops skill)

| Intent | Command |
|---|---|
| Is Linux up? | `docker ps --filter name=kali-aegis` |
| Enter Kali | `docker exec -it kali-aegis bash` |
| Authorized estate scan | `docker exec kali-aegis bash -c "python3 /aegis/work/kali/kali-scan-hook.py <target> --tools all"` |
| Verify tools | `docker exec kali-aegis bash -c "bash /aegis/work/kali/tool-smoke-test.sh"` |
| Index flagship code | `codebase-memory-mcp cli index_repository --repo-path /var/www/zeusaiintelligence.com` |

## Rules ZEUS must enforce
- Scans run ONLY against ZEUS-owned estate (flagship, NEXUS, breach-check).
- Never rebuild the image except via `bash ~/kali/build-guard.sh`
  (blocks double-builds, low disk; nohup; verifies ≥3 GB).
- Keep compose `pull_policy: missing`; keep NET_RAW/NET_ADMIN + seccomp/AppArmor
  unconfined (nmap breaks without them).
- Disk watchdog: `bash /root/kali/disk-monitor.sh once` (WARN 15G / CRIT 8G).
- MCP: `codebase-memory-mcp` 0.11.0 installed at /root/.local/bin;
  tools = index_repository, list_projects, search_graph, trace_path, query_graph.

## Personas
279 agency-agents personas installed at /root/.claude/agents (Claude Code);
5 estate-adapted personas in ~/kali/agency-personas.

All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).