#!/usr/bin/env bash
# estate-security-probe.sh — external security verification probe for the ZEUS
# estate. Runs from ANY machine with internet (sandbox, PC, droplet) — checks the
# estate from the OUTSIDE, exactly as an auditor would. Green only when verified.
# Usage: bash estate-security-probe.sh
set -uo pipefail
PASS=0; FAIL=0
ok(){ printf "  %bOK%b   %s\n" "$(tput setaf 2 2>/dev/null)" "$(tput sgr0 2>/dev/null)" "$1"; PASS=$((PASS+1)); }
bad(){ printf "  %bFAIL%b %s\n" "$(tput setaf 1 2>/dev/null)" "$(tput sgr0 2>/dev/null)" "$1"; FAIL=$((FAIL+1)); }

echo "═══════════ ZEUS estate external security probe ═══════════"
STAMP=$(date -u '+%Y-%m-%d %H:%M:%S')
echo "  probe time UTC: $STAMP"

# 1. estate surfaces alive
for u in \
  https://zeusaiintelligence.com \
  https://nexus.zeusaiintelligence.com \
  https://aegis-breach-check.higgsfield.app \
  https://zeusai-intelligence.higgsfield.app; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 "$u")
  if [ "$code" = "200" ]; then ok "surface 200 $u"; else bad "surface $code $u"; fi
done

# 2. flagship security headers (the INC-005-adjacent hardening checklist)
H=$(curl -sI --max-time 20 https://zeusaiintelligence.com)
for hdr in strict-transport-security content-security-policy x-content-type-options referrer-policy permissions-policy; do
  if echo "$H" | grep -qi "$hdr"; then ok "header $hdr present"; else bad "header $hdr MISSING"; fi
done

# 3. INC-005 CORS preflight on apiaegissecurity.tech
CORS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 -X OPTIONS \
  -H "Origin: https://zeusaiintelligence.com" -H "Access-Control-Request-Method: GET" \
  https://apiaegissecurity.tech/)
if [ "$CORS" = "200" ] || [ "$CORS" = "204" ]; then ok "INC-005 CORS preflight $CORS"; else bad "INC-005 CORS preflight $CORS (expected 200/204)"; fi

# 4. TLS handshake valid
TLS=$(curl -s -o /dev/null -w "%{ssl_verify_result}" --max-time 20 https://zeusaiintelligence.com)
if [ "$TLS" = "0" ]; then ok "TLS certificate valid"; else bad "TLS verify result $TLS"; fi

echo "──────────────────────────────────────────────"
if [ "$FAIL" -eq 0 ]; then
  echo "  ALL CHECKS PASSED ($PASS/$PASS)"
else
  echo "  $FAIL of $((PASS+FAIL)) checks FAILED"
fi
exit $([ "$FAIL" -eq 0 ] && echo 0 || echo 1)