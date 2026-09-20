#!/usr/bin/env bash
# build-guard.sh — safe Kali-AEGIS image build wrapper.
# Guards against every failure class this estate has hit:
#   1. DOUBLE-BUILD  : refuses to start if another docker build is running
#   2. LOW DISK      : refuses if free space < MIN_FREE_GB (default 20)
#   3. SILENT DEATH  : runs with nohup + honest EXIT capture (no tee pipe trap)
#   4. FALSE GREEN   : verifies image size + tag after build, not just "exit 0"
# Usage: bash build-guard.sh            (from ~/kali)
set -uo pipefail
MIN_FREE_GB="${MIN_FREE_GB:-20}"
TARGET="${TARGET_IMAGE:-kali-aegis:1.0}"
LOG="${BUILD_LOG:-/tmp/kali-build-guarded.log}"
MIN_IMAGE_GB="${MIN_IMAGE_GB:-3}"   # trimmed image ~5GB; anything <3GB is a skeleton

echo "═══ kali build guard ═══"
# 1) double-build guard
RUNNING=$(pgrep -af "docker build" | grep -v "build-guard\|grep" || true)
if [ -n "$RUNNING" ]; then
  echo "✗ REFUSED: another docker build is running:"
  echo "$RUNNING"
  echo "  Kill it first (kill <pid>), or use a second build only after it ends."
  exit 10
fi
echo "✓ no other build running"

# 2) disk guard
FREE_GB=$(df -BG / | awk 'NR==2 {gsub("G","",$4); print $4}')
echo "  free disk: ${FREE_GB}G (need ≥ ${MIN_FREE_GB}G)"
if [ "${FREE_GB%.*}" -lt "$MIN_FREE_GB" ]; then
  echo "✗ REFUSED: free disk ${FREE_GB}G < ${MIN_FREE_GB}G."
  echo "  Run: docker system prune -a -f  (or grow the volume), then retry."
  exit 11
fi
echo "✓ disk headroom OK"

# 3) build — nohup so a dropped SSH tab cannot kill it; redirect (no tee)
echo "  building ${TARGET} → log ${LOG}"
nohup docker build --no-cache -t "$TARGET" . > "$LOG" 2>&1 &
BUILD_PID=$!
echo "  started PID ${BUILD_PID} — log: tail -f ${LOG}"
echo "BUILD_PID=$BUILD_PID" >> "$LOG"
wait "$BUILD_PID"
EXIT=$?
echo "EXIT=$EXIT" >> "$LOG"

# 4) honest verification — exit 0 is not proof
if [ "$EXIT" -ne 0 ]; then
  echo "✗ build failed (EXIT=$EXIT) — see ${LOG} tail:"
  tail -5 "$LOG"
  exit 12
fi
SIZE_GB=$(docker image inspect "$TARGET" --format '{{.Size}}' 2>/dev/null | awk '{printf "%.1f", $1/1073741824}')
echo "✓ build exit 0 — image ${TARGET} size ${SIZE_GB}G"
if awk "BEGIN{exit !(${SIZE_GB:-0} >= ${MIN_IMAGE_GB})}"; then
  echo "✓ image size verified ≥ ${MIN_IMAGE_GB}G — genuine build, not a skeleton"
else
  echo "✗ image size ${SIZE_GB}G < ${MIN_IMAGE_GB}G — likely a base-only skeleton"
  exit 13
fi
echo "═══ guard PASS — next: docker compose up -d && bash quickstart-test.sh ═══"