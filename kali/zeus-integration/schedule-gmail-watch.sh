#!/usr/bin/env bash
# schedule-gmail-watch.sh — nightly Gmail trash-watch cron for the ZEUS estate.
# Runs on the DROPLET HOST as root. Adds a cron entry:
#   EVERY NIGHT 03:45 UTC: run the estate_gmail_watcher sweep check and log.
# The Gmail query itself executes through the estate chat connector (the
# watcher script emits the query); this cron keeps the sweep scheduled and
# writes a timestamped audit line so the nightly run is provable.
# Usage: bash schedule-gmail-watch.sh
set -uo pipefail
LOG=/var/log/zeus-gmail-watch.log
CRON_LINE="45 3 * * * echo \"\$(date -u +%Y-%m-%dT%H:%M:%SZ) gmail-watch sweep due (query: see estate_gmail_watcher.py)\" >> $LOG && /usr/bin/python3 /root/kali/zeus-integration/estate_gmail_watcher.py >> $LOG 2>&1 && tail -1 $LOG"

if crontab -l 2>/dev/null | grep -q "estate_gmail_watcher"; then
  echo "  gmail-watch cron already installed — skipping"
else
  ( crontab -l 2>/dev/null; echo "$CRON_LINE" ) | crontab -
  echo "  cron installed: nightly 03:45 UTC — gmail trash-watch"
fi
touch "$LOG"
crontab -l 2>/dev/null | grep estate_gmail_watcher || echo "  (none yet)"
echo "  log: $LOG"