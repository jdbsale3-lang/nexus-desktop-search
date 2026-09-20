#!/usr/bin/env bash
# disk-monitor.sh — ZEUS estate droplet disk watchdog.
# Catches the failure class that has cost this estate six builds:
# free space silently dropping to <10G while a build ran.
# Usage:
#   bash disk-monitor.sh once              # single check
#   nohup bash disk-monitor.sh loop > /tmp/disk-monitor.log 2>&1 &   # continuous watch
#   (cron) */5 * * * * bash /root/kali/disk-monitor.sh once >> /tmp/disk-monitor.log 2>&1
set -uo pipefail
WARN_GB="${WARN_GB:-15}"
CRIT_GB="${CRIT_GB:-8}"
STAMP=$(date -u '+%Y-%m-%d %H:%M:%S')
LOG="${DISK_LOG:-/tmp/disk-watch.log}"

check() {
  FREE_GB=$(df -BG / | awk 'NR==2 {gsub("G","",$4); print $4}')
  IMG_GB=$(docker system df 2>/dev/null | awk '$1=="Images"{print $4}' | head -1)
  CONT_GB=$(docker system df 2>/dev/null | awk '$1=="Containers"{print $4}' | head -1)
  LINE="$STAMP free=${FREE_GB}G images=${IMG_GB:-?} containers=${CONT_GB:-?}"
  echo "$LINE" >> "$LOG"
  if [ "${FREE_GB%.*}" -lt "$CRIT_GB" ]; then
    echo "$STAMP CRITICAL: ${FREE_GB}G free (<${CRIT_GB}G) — build will fail at export. Run: docker system prune -a -f" >> "$LOG"
  elif [ "${FREE_GB%.*}" -lt "$WARN_GB" ]; then
    echo "$STAMP WARN: ${FREE_GB}G free (<${WARN_GB}G) — watch it" >> "$LOG"
  fi
}

case "${1:-once}" in
  once) check ;;
  loop) while true; do check; sleep "${POLL_SEC:-300}"; done ;;
  *) echo "usage: disk-monitor.sh once|loop"; exit 1 ;;
esac
tail -3 "$LOG" 2>/dev/null