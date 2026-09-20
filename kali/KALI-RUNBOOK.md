# ZEUS Kali-AEGIS Workstation — FINAL RUNBOOK
**Status: LIVE** — container `kali-aegis` running on aegis-api (188.166.175.149)
**Image:** `kali-aegis:1.0` (trimmed v8 kit, ~4 GB content, all tools verified)

---

## 1. Launch & daily use (droplet host, `root@aegis-api`)

```bash
docker exec -it kali-aegis bash       # enter Kali (prompt: ┌──(root㉿kali-aegis))
exit                                  # leave; container keeps running
docker ps                             # check health — expect: Up (healthy)
```

## 2. Authorized scanning (inside the container)

```bash
nmap -sV zeusaiintelligence.com
python3 /aegis/work/kali/kali-scan-hook.py https://zeusaiintelligence.com --tools all
```

## 3. Critical configuration (DO NOT change)

| Setting | Value | Why it must stay |
|---|---|---|
| `pull_policy` in docker-compose.yml | `missing` | `build` forces a full rebuild on every `up` (20-60 min, disk risk) |
| `cap_add` | `SYS_PTRACE`, `NET_RAW`, `NET_ADMIN` | `NET_RAW` is REQUIRED for nmap ("Operation not permitted" without it) |
| Image rebuilds | ONLY via `bash build-guard.sh` | Refuses double-builds / <20 GB disk; nohup; verifies image ≥3 GB |

## 4. Rebuilding the image (rare; only for new tooling)

```bash
cd ~/kali && bash build-guard.sh      # safe single build, honest EXIT, size check
docker compose up -d                  # restart with new image
```

## 5. Disk hygiene

```bash
nohup bash /root/kali/disk-monitor.sh loop > /dev/null 2>&1 &   # watchdog: WARN 15G / CRIT 8G
docker system prune -a -f             # reclaim failed-build layers (never while a build runs)
df -h /                               # if < 15G free: DO console → Power off → Resize → 80G → growpart
```

## 6. Incident history (why the runbook exists)

- **INC-001** apt `cheat` missing → pip install (not a Kali apt package)
- **INC-002** `ghidra` not pulled by metapackages → explicit pin in Dockerfile
- **INC-003** `chown: invalid user: postgres` → deterministic `useradd` guard in build + entrypoint
- **INC-004** disk-full at image export (6 attempts) → prune + grow volume + **single** build via guard
- **INC-005** double-build deadlock → guard refuses concurrent builds
- **INC-006** nmap `Operation not permitted` → `NET_RAW`+`NET_ADMIN` caps

## 7. Tool inventory (all verified executing — see tool-smoke-test.sh)

nmap · nuclei · sqlmap · burpsuite · msfconsole · searchsploit · hashcat · john · hydra · wireshark · bettercap · ghidra · radare2 (r2) · responder · impacket-psexec · cheat · ffuf · gobuster · nikto · wpscan · subfinder · httpx

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).