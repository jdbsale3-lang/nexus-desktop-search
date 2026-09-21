# ZEUS ESTATE — DROPLET RUNBOOK (final consolidated reference)
**Host:** aegis-api · 188.166.175.149 · Ubuntu 24.04 · Creator: ZEUSTRUSTAEGISSECURITY LTD
Every block below runs at `root@aegis-api:~#` unless marked (inside Kali).

---

## 1. DAILY ROUTINE
```bash
docker ps                                      # kali-aegis Up (healthy)
bash /root/kali/disk-monitor.sh once           # disk watch (WARN 15G / CRIT 8G)
docker exec -it kali-aegis bash                # enter Kali (admin)
exit                                           # leave (container keeps running)
```

## 2. LAUNCH / USE KALI (LINUX)
```bash
docker exec -it kali-aegis bash                # enter
exit                                           # leave
nmap -sV zeusaiintelligence.com                # inside Kali: estate scan
```
Host prompt = `root@aegis-api` · Kali prompt = `(root💀kali-aegis)`. `which docker` tells you where you are.

## 3. AUTHORIZED ESTATE SCANS (inside Kali)
```bash
python3 /aegis/work/kali/kali-scan-hook.py https://zeusaiintelligence.com --tools all
nmap -Pn -sV -sC -p 80,443,8080,8443 zeusaiintelligence.com
```

## 4. REBUILD THE IMAGE (rare — ONLY via the guard)
```bash
cd ~/kali && bash build-guard.sh               # blocks double-build, low disk, nohup, size check
docker compose up -d
```

## 5. SECURITY HEADERS (already applied — re-apply if nginx reinstalled)
```bash
python3 ~/kali/apply-security-headers.py       # fixture-tested 5/5
bash ~/kali/estate-security-probe.sh           # full external probe (11 checks)
```

## 6. INCIDENT LEDGER
| CLI | INC-00x | status |
|---|---|---|
| cheat-in-apt | INC-001 | closed |
| MCP tool names | INC-002 | closed |
| routes wiped | INC-003 | closed |
| monitor | INC-004 | closed |
| AEGIS CORS | INC-005 | **closed — preflight 204** |
| nmap caps | INC-006 | closed |

## 7. CRONS INSTALLED (all verified)
```bash
crontab -l
# 03:45 nightly  gmail trash-watch (75 anchors) + alert
# 06:10 Mon     estate scan (nikto,nmap,ffuf)
# 07:15 Sun     external security probe
```

## 8. MONITORING / ALERTS
```bash
tail -20 /var/log/zeus-gmail-watch.log
tail -3  /tmp/disk-watch.log
curl -s https://zeusaiintelligence.com/reach/monitor
curl -s https://zeusaiintelligence.com/reach/doctor | python3 -m json.tool
```

## 9. CHANNELS (doctor) — the 5-warn finish
```bash
# github + exa are PROVEN ok (no-write probes 200) — apply the verify patch:
GITHUB_TOKEN=<your-pat> EXA_API_KEY=<your-key> python3 ~/kali/zeus-integration/doctor-verify-fix.py
# twitter/linkedin/xueqiu need explicit cookies:
agent-reach configure twitter-cookies          # paste: <auth_token> <ct0>
agent-reach install --system --channels linkedin && mcporter run linkedin-mcp &
agent-reach configure xueqiu-cookies
```

## 10. MCP / CODEMEMORY
```bash
codebase-memory-mcp cli index_repository --repo-path /var/www/zeusaiintelligence.com
codebase-memory-mcp cli query_graph --project var-www-zeusaiintelligence.com --query 'MATCH (f:Function) RETURN f.name LIMIT 15'
```

## 11. NEW SEARXNG FALLBACK
```bash
bash ~/kali/zeus-integration/integrate-searxng.sh
curl 'http://127.0.0.1:8888/search?q=NHS&format=json' | head -c 200
```

## 12. KEY FILES (do not break)
| path | purpose |
|---|---|
| ~/kali/build-guard.sh | rebuild guard |
| ~/kali/disk-monitor.sh | disk watchdog |
| ~/kali/estate-security-probe.sh | external probe |
| ~/kali/apply-security-headers.py | headers applier |
| ~/kali/nginx-security-headers.conf | header template |
| ~/kali/zeus-integration/ | zeus skills, watchers, patches |
| /opt/zeus-skills/ | ZEUS skill engine autodiscover |
| /opt/zeus-agents/ | 6 verified agent repos |
| /opt/agent-reach-bridge.py | answer router (confirm gate wired) |

## 13. EMERGENCY
```bash
nginx -t && systemctl reload nginx            # validate before reload
docker system prune -a -f                      # reclaim disk (never mid-build)
docker compose down && docker compose up -d    # recreate container (caps)
```

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).