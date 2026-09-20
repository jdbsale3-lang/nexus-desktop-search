# Kali-AEGIS Kit v17 — Release Notes

**Tag:** `kali-kit-v17` · **Released:** 2026-09-20 · **Asset:** zeusai-kali-kit-v17.zip (62,405 B, SHA `b49f2819`)
**Download:** https://github.com/jdbsale3-lang/nexus-desktop-search/releases/download/kali-kit-v17/zeusai-kali-kit-v17.zip

## What's in this release

**Estate security stack (complete, verified):**
- Kali Linux workstation — container `kali-aegis`, trimmed ~4 GB image, **22/22 tools verified executing** (tool-smoke-test v12)
- `build-guard.sh` — rebuild guard (blocks double-builds, <20 GB disk, silent death; nohup + honest EXIT; verifies ≥3 GB image)
- `disk-monitor.sh` — disk watchdog (WARN 15 G / CRIT 8 G)
- `nginx-security-headers.conf` — flagship hardening: HSTS (preload) · CSP (estate-tuned) · X-Frame-Options · X-Content-Type-Options · Referrer-Policy · Permissions-Policy · server_tokens off
- `kali-scan-hook.py` v2 (fixed: `import re` top-level — field-caught nmap-parser NameError)
- n8n workflow import (`n8n-kali-scan.workflow.json`)

**Codebase intelligence:**
- codebase-memory-mcp 0.11.0 — flagship indexed: **340 nodes / 923 edges**
- `estate-codebase-index` skill documented

**ZEUS integration:**
- `zeus_kali_ops.py` — skill module (status / scan / tooltest / mcpindex / launch), registered into `/opt/zeus-skills`
- `register-into-zeus.py` — fixture-tested registration helper (refuses to corrupt on ambiguous anchor)
- `ZEUS-KALI-BRIEFING.md` + `INSTALL-INTO-ZEUS.md`

**Documentation (published on zeusai-intelligence.higgsfield.app/docs):**
- `KALI-USAGE-GUIDE.md` (install steps, daily rhythm, scanning, MCP, troubleshooting, screenshots)
- `KALI-RUNBOOK.md` (INC-001…006 history, protection rules)
- `TOOLSET-STATUS.md` · `USAGE-GUIDE.md` · `ESTATE-SCAN-REPORT-2026-09-20.md`

**Personas:** 279 agency-agents + 5 estate-adapted (code-reviewer → devops-automator)

## Baseline scan (for before/after evidence)
2026-09-20 19:39 UTC: **verdict REVIEW · 21 findings** — 5 missing security headers
on the flagship; Cloudflare edge confirmed; no criticals. Hardening config ships in
this release; apply then re-scan to prove the flip to CLEAN.

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).