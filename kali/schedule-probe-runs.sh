#!/usr/bin/env bash
# schedule-probe-runs.sh — install cron for recurring estate security probes.
# Runs on the DROPLET HOST as root. Creates ~/kali/probe-history/ and a cron:
#   SUN 07:15 UTC: run estate-security-probe.sh, append log, exit-code archive
# Usage: bash schedule-probe-runs.sh
set -uo pipefail
HIST="$HOME/kali/probe-history"
mkdir -p "$HIST"
CRON_LINE="15 7 * * 0 bash $HOME/kali/estate-security-probe.sh >> $HIST/probe-\$(date +\\%Y\\%m\\%d).log 2>&1; echo exit=\$? >> $HIST/probe-\$(date +\\%Y\\%m\\%d).log"

if crontab -l 2>/dev/null | grep -q "estate-security-probe"; then
  echo "  probe cron already installed — skipping"
else
  ( crontab -l 2>/dev/null; echo "$CRON_LINE" ) | crontab -
  echo "  cron installed: Sunday 07:15 UTC — estate security probe"
fi
echo "  history dir: $HIST"
crontab -l 2>/dev/null | grep estate || echo "  (none yet)"