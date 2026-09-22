#!/usr/bin/env bash
# nginx-reach-belt.sh — close the /reach/ action-route exposure at nginx level.
# Blocks the quota-abuse surface (/search /gh /read /yt /bili /v2ex /rss) while
# leaving the read-only routes the Command Centre dashboard needs.
#
# Safety: backs up the config, tests with `nginx -t`, reloads ONLY on success,
# restores the backup on any failure. Refuses if it cannot find one clear target.
#
# Usage (droplet, root): bash nginx-reach-belt.sh
set -u
echo "═══ ZEUS nginx /reach/ BELT ═══"

# 1) find exactly one nginx config that proxies /reach/
MAPS=$(grep -rl --include="*.conf" -E "location[[:space:]]+/?reach" /etc/nginx/ 2>/dev/null | sort -u)
COUNT=$(echo "${MAPS:-}" | grep -c . )
if [ "$COUNT" -ne 1 ]; then
  echo "  !! found $COUNT candidate config(s) — refusing to guess."
  echo "${MAPS:-  (none)}"
  echo "  Add this inside the server block that proxies /reach/, then reload:"
  cat <<'SNIP'
    location ~ ^/reach/(search|gh|read|yt|bili|v2ex|rss)$ { return 403; }
SNIP
  exit 3
fi
CONF="$MAPS"
echo "  target: $CONF"

# 2) already applied?
if grep -qE "^[[:space:]]*location[[:space:]]+~[[:space:]]+\^/reach/\(search" "$CONF"; then
  echo "  belt already present — verify only"
  nginx -t && echo "  config valid"
  exit 0
fi

BAK="${CONF}.bak-reach-belt"
cp "$CONF" "$BAK"
echo "  backup: $BAK"

# 3) insert the deny rule immediately BEFORE the existing /reach/ location
LINE=$(grep -nE "location[[:space:]]+/?reach" "$CONF" | head -1 | cut -d: -f1)
if [ -z "$LINE" ]; then
  echo "  !! could not locate the /reach/ line — restoring"; cp "$BAK" "$CONF"; exit 4
fi
INDENT=$(sed -n "${LINE}p" "$CONF" | sed -E 's/[^[:space:]].*//')
python3 - "$CONF" "$LINE" "$INDENT" <<'PY'
import sys
conf, line, indent = sys.argv[1], int(sys.argv[2]), sys.argv[3]
rows = open(conf).read().splitlines(keepends=True)
rule = (f"{indent}# ZEUS belt: block the action routes (quota-abuse surface)\n"
        f"{indent}location ~ ^/reach/(search|gh|read|yt|bili|v2ex|rss)$ {{ return 403; }}\n")
rows.insert(line - 1, rule)
open(conf, "w").write("".join(rows))
print("  inserted belt rule before line", line)
PY

# 4) test, then reload only if valid
if nginx -t 2>/tmp/nginx-test.out; then
  systemctl reload nginx && echo "  ✅ nginx reloaded — belt LIVE"
else
  echo "  !! nginx -t failed — restoring backup (nothing changed):"
  sed 's/^/     /' /tmp/nginx-test.out | head -5
  cp "$BAK" "$CONF"
  nginx -t >/dev/null 2>&1 && systemctl reload nginx
  exit 5
fi

# 5) verify on the wire
sleep 1
for r in "search?q=x" "gh?q=x" "self" "doctor"; do
  printf "  /reach/%-12s → HTTP %s\n" "$r" "$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "https://zeusaiintelligence.com/reach/$r")"
done
echo "  expect: search/gh = 403 · self/doctor = 200 (dashboard keeps working)"