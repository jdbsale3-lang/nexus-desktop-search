#!/usr/bin/env bash
# estate-health.sh — POST-DEPLOY health gate. Exits non-zero on any failure so
# CI (and humans) fail loudly after a deploy. Safe to run anywhere with curl+python3.
# Usage: bash estate-health.sh   (droplet or CI)
set -u
FAILS=0
say(){ printf "  %-58s %s\n" "$1" "$2"; }

echo "═══ ZEUS POST-DEPLOY HEALTH GATE ═══"

# 1) surfaces — 200 expected; 401/403 also = alive (auth-gated)
for u in https://zeusaiintelligence.com \
         https://nexus.zeusaiintelligence.com \
         https://apiaegissecurity.tech \
         https://aegis-breach-check.higgsfield.app \
         https://zeusai-intelligence.higgsfield.app ; do
  C=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 "$u")
  if [ "$C" = "200" ] || [ "$C" = "401" ] || [ "$C" = "403" ] || [ "$C" = "302" ]; then
    say "$u" "OK ($C)"
  else
    say "$u" "FAIL ($C)"; FAILS=$((FAILS+1))
  fi
done

# 2) security headers on the flagship (>=3/5)
H=$(curl -sI --max-time 20 https://zeusaiintelligence.com | grep -icE "strict-transport|content-security|x-content-type|referrer-policy|permissions-policy")
if [ "$H" -ge 3 ]; then say "security headers" "OK ($H/5)"; else say "security headers" "FAIL ($H/5)"; FAILS=$((FAILS+1)); fi

# 3) CORS preflight (expect 204)
C=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 -X OPTIONS \
     -H "Origin: https://zeusaiintelligence.com" -H "Access-Control-Request-Method: GET" \
     https://apiaegissecurity.tech/)
if [ "$C" = "204" ]; then say "CORS preflight" "OK (204)"; else say "CORS preflight" "FAIL ($C)"; FAILS=$((FAILS+1)); fi

# 4) reach engine: skills + monitor
S=$(curl -s --max-time 20 https://zeusaiintelligence.com/reach/self | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('skills_loaded'), d.get('skills_broken'))" 2>/dev/null)
LOADED=$(echo "$S" | awk '{print $1}'); BROKEN=$(echo "$S" | awk '{print $2}')
if [ -n "$LOADED" ] && [ "$BROKEN" = "0" ] && [ "$LOADED" -ge 25 ]; then say "reach skills" "OK ($LOADED loaded / $BROKEN broken)"; else say "reach skills" "FAIL ($S)"; FAILS=$((FAILS+1)); fi

M=$(curl -s --max-time 20 https://zeusaiintelligence.com/reach/monitor | grep -o '"alerts": *\[[^]]*\]' | head -1)
if [ "$M" = '"alerts": []' ]; then say "estate monitor" "OK (0 alerts)"; else say "estate monitor" "WARN ($M)"; fi

# 5) doctor channels that MUST be ok after the fix
D=$(curl -s --max-time 25 https://zeusaiintelligence.com/reach/doctor | python3 -c "
import json,sys
d=json.load(sys.stdin); doc=d.get('doctor',d)
print(doc.get('github',{}).get('status'), doc.get('exa_search',{}).get('status'))
" 2>/dev/null)
GH=$(echo "$D" | awk '{print $1}'); EX=$(echo "$D" | awk '{print $2}')
if [ "$GH" = "ok" ]; then say "doctor github" "OK"; else say "doctor github" "WARN ($GH)"; fi
if [ "$EX" = "ok" ]; then say "doctor exa_search" "OK"; else say "doctor exa_search" "WARN ($EX)"; fi

echo "═══ RESULT: $FAILS hard failure(s) ═══"
exit $FAILS