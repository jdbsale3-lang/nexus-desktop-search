#!/usr/bin/env bash
# schedule-gmail-watch.sh — nightly Gmail trash-watch cron for the ZEUS estate.
# v3: ALERTING enabled. When the sweep finds estate-critical mail in Trash it
# writes an ALERT line + raises the exit path for the caller, and (if a
# webhook URL is set) fires a notification. Detection is logged with a marker
# that estate monitors can grep.
# Usage: bash schedule-gmail-watch.sh
set -uo pipefail
LOG=/var/log/zeus-gmail-watch.log
ALERT=/var/log/zeus-gmail-watch.alert
WEBHOOK="${GMAIL_WATCH_WEBHOOK:-}"   # optional Slack-compatible webhook URL

# nightly: run watcher, log output, flag if anything found
CRON_LINE="45 3 * * * { echo \"\$(date -u +%Y-%m-%dT%H:%M:%SZ) gmail-watch sweep started\"; \
  /usr/bin/python3 /root/kali/zeus-integration/estate_gmail_watcher.py 2>&1; } >> $LOG && \
  if grep -qi 'ALERT\|in_trash\|\"count\": *[1-9]' $LOG; then \
    echo \"\$(date -u +%Y-%m-%dT%H:%M:%SZ) ALERT: estate-critical mail detected in Trash — restore now\" >> $ALERT; \
    [ -n \"$WEBHOOK\" ] && curl -s -m 20 -H 'Content-Type: application/json' -d '{\"text\":\"ZEUS: estate-critical mail in Gmail Trash — restore now\"}' \"$WEBHOOK\" >/dev/null 2>&1 || true; \
  fi"

if crontab -l 2>/dev/null | grep -q "estate_gmail_watcher"; then
  echo "  gmail-watch cron already installed — skipping"
else
  ( crontab -l 2>/dev/null; echo "$CRON_LINE" ) | crontab -
  echo "  cron installed: nightly 03:45 UTC — gmail trash-watch (alerting ON)"
fi
touch "$LOG" "$ALERT"
crontab -l 2>/dev/null | grep estate_gmail_watcher || echo "  (none yet)"
echo "  log: $LOG   alert file: $ALERT"
echo "  set webhook: export GMAIL_WATCH_WEBHOOK=... before install for push alerts"