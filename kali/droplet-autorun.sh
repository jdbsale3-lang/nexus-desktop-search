#!/usr/bin/env bash
# droplet-autorun.sh — ONE command to finish every pending droplet fix.
# Idempotent: safe to run repeatedly. Runs on the DROPLET HOST as root.
# Usage: bash droplet-autorun.sh
set -uo pipefail
echo "═══════════ ZEUS droplet auto-run ═══════════"
STAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ'); echo "  time: $STAMP"

# 1) doctor-verify-fix (github + exa -> ok) — tokens pulled from the box
echo "-- 1) doctor verify (github + exa) --"
GITHUB_TOKEN=$(git -C ~/kali remote get-url origin 2>/dev/null | sed -n 's|.*x-access-token:\([^@]*\)@.*|\1|p')
EXA_API_KEY=$(grep -oP '(?<=EXA_API_KEY=).*' /opt/zeus-reach.env 2>/dev/null || echo '')
if [ -n "$GITHUB_TOKEN" ] && [ -n "$EXA_API_KEY" ]; then
  python3 ~/kali/zeus-integration/doctor-verify-fix.py 2>&1 | grep -o '"status": "[a-z]*"' | head -2 | sed 's/^/  /'
elif [ -n "$GITHUB_TOKEN" ]; then
  GITHUB_TOKEN="$GITHUB_TOKEN" EXA_API_KEY="$EXA_API_KEY" \
    python3 ~/kali/zeus-integration/doctor-verify-fix.py 2>&1 | head -8
else
  echo "  !! tokens not found on box — run doctor-verify-fix.py manually with env vars"
fi

# 2) confirm gate (wired if not already)
echo "-- 2) confirm gate --"
python3 ~/kali/zeus-integration/wire-confirm-gate.py 2>&1 | tail -2

# 3) SearXNG fallback lane
echo "-- 3) searxng --"
if command -v docker >/dev/null 2>&1; then
  bash ~/kali/zeus-integration/integrate-searxng.sh 2>&1 | tail -3
else
  echo "  !! docker missing — run install-docker.sh first"
fi

# 4) crons: verify present
echo "-- 4) crons --"
crontab -l 2>/dev/null | grep -cE "gmail|estate|probe|scan" | xargs echo "  cron entries:"

# 5) estate security probe
echo "-- 5) estate probe (11 checks) --"
bash ~/kali/estate-security-probe.sh 2>&1 | tail -6

echo "═══════════ auto-run complete $STAMP ═══════════"