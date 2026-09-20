#!/usr/bin/env bash
# schedule-estate-scans.sh — install cron for recurring estate hardening scans.
# Runs on the DROPLET HOST as root. Creates ~/kali/scans/ and a cron entry:
#   MON 06:10 UTC: scan flagship, append dated JSON, update LATEST-VERDICT.txt
# Usage: bash schedule-estate-scans.sh
set -uo pipefail

SCAN_DIR="$HOME/kali/scans"
CRON_LINE="10 6 * * 1 docker exec kali-aegis bash -c \"python3 /aegis/work/kali/kali-scan-hook.py https://zeusaiintelligence.com --tools nikto,nmap,ffuf\" | tee -a $SCAN_DIR/scan-\$(date +\\%Y\\%m\\%d).json > /dev/null && grep -o '\"verdict\": \"[A-Z]*\"' $SCAN_DIR/scan-\$(date +\\%Y\\%m\\%d).json | tail -1 > $HOME/kali/LATEST-VERDICT.txt"

mkdir -p "$SCAN_DIR"

# idempotent: only add if not present
if crontab -l 2>/dev/null | grep -q "kali-scan-hook"; then
  echo "  cron already installed — skipping (line exists)"
else
  ( crontab -l 2>/dev/null; echo "$CRON_LINE" ) | crontab -
  echo "  cron installed: Monday 06:10 UTC — estate scan"
fi

echo "  scan dir: $SCAN_DIR"
echo "  current crontab:"
crontab -l 2>/dev/null | grep kali-scan-hook || echo "  (none yet — check above)"
echo ""
echo "  latest verdict file will be at: ~/kali/LATEST-VERDICT.txt"
echo "  (reads CLEAN or REVIEW after each Monday scan)"