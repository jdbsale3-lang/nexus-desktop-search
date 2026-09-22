#!/usr/bin/env bash
# droplet-urgent-fix-v2.sh — CORRECTED: survives the four races found live.
#  1) Exa key var name: bridge reads REACH_EXA_KEY (not EXA_API_KEY)
#  2) GitHub token: comes from `gh auth token`, NOT the git remote URL
#  3) Locale: en_GB.UTF-8 may not be generated -> use C.UTF-8 (always exists)
#  4) Kit path: zip root is kali/ so files land at /root/kali/kali/... — search both
# Idempotent. Run as root on the DROPLET:  bash droplet-urgent-fix-v2.sh
set -u
echo "═══════ ZEUS DROPLET URGENT FIX v2 ═══════"
ENV=/opt/zeus-reach.env
BRIDGE=/opt/agent-reach-bridge.py
BAK=$BRIDGE.bak-confirm-global
LOGF=/var/log/zeus-reach-setup.log

# --- locate the kit files (zip root is kali/ -> nested kali/kali/) ---
GATE_PY=""
for cand in /root/kali/kali/zeus-integration/confirm-gate-global.py \
            /root/kali/zeus-integration/confirm-gate-global.py \
            /root/kali/kali/confirm-gate-global.py \
            /root/confirm-gate-global.py; do
  [ -f "$cand" ] && GATE_PY="$cand" && break
done

echo "-- 0. pre-flight --"
[ -f "$ENV" ] || { echo "!! $ENV missing"; exit 2; }
echo "   gate patcher: ${GATE_PY:-NOT FOUND (unzip kit v61 into /root/kali)}"

echo "-- 1. locale: use what the box actually has --"
LOCALE_OK=$(locale -a 2>/dev/null | grep -E "^(C|en)(\.|_)|^C$" | head -1)
[ -n "$LOCALE_OK" ] || LOCALE_OK="C.UTF-8"
echo "   using locale: $LOCALE_OK"
grep -q "^LANG=" "$ENV" || echo "LANG=$LOCALE_OK" >> "$ENV"
grep -q "^LC_ALL=" "$ENV" || echo "LC_ALL=$LOCALE_OK" >> "$ENV"

echo "-- 2. GitHub token: gh auth (authoritative) / GH_TOKEN / existing env --"
GHTOK="$(gh auth token 2>/dev/null | head -1)"
if [ -z "$GHTOK" ] && [ -f ~/.config/gh/hosts.yml ]; then
  GHTOK=$(grep -oP '(?<=oauth_token: ).*' ~/.config/gh/hosts.yml 2>/dev/null | head -1)
fi
# keep any token already in the env file
if [ -n "$GHTOK" ]; then
  grep -q "^GITHUB_TOKEN=" "$ENV" || echo "GITHUB_TOKEN=$GHTOK" >> "$ENV"
  grep -q "^GH_TOKEN=" "$ENV" || echo "GH_TOKEN=$GHTOK" >> "$ENV"
  echo "   GITHUB_TOKEN set from gh auth"
else
  echo "   !! no gh token found — paste your fine-grained PAT into /opt/zeus-reach.env as GITHUB_TOKEN= (manual step)"
fi

echo "-- 3. Exa key: the bridge reads REACH_EXA_KEY — ensure BOTH names --"
# if only REACH_EXA_KEY exists, mirror to EXA_API_KEY for doctor-verify-fix; and vice versa
REK=$(grep -oP '(?<=^REACH_EXA_KEY=).*' "$ENV" | head -1)
EAK=$(grep -oP '(?<=^EXA_API_KEY=).*' "$ENV" | head -1)
if [ -n "$REK" ] && [ -z "$EAK" ]; then
  echo "EXA_API_KEY=$REK" >> "$ENV"; echo "   mirrored REACH_EXA_KEY -> EXA_API_KEY"
elif [ -n "$EAK" ] && [ -z "$REK" ]; then
  echo "REACH_EXA_KEY=$EAK" >> "$ENV"; echo "   mirrored EXA_API_KEY -> REACH_EXA_KEY"
elif [ -z "$REK" ] && [ -z "$EAK" ]; then
  echo "   !! no Exa key in $ENV — add REACH_EXA_KEY=<key> manually (it is NOT there yet per live run)"
else
  echo "   both Exa key names present"
fi
echo "   env keys now: $(grep -oE '^(LANG|LC_ALL|GITHUB_TOKEN|GH_TOKEN|REACH_EXA_KEY|EXA_API_KEY)=' "$ENV" | tr '\n' ' ')"

echo "-- 4. source env + prove probes (reads BOTH key names) --"
set -a; . "$ENV" 2>/dev/null; set +a
python3 - <<'PY'
import json, os, urllib.request
def probe_gh():
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN", "")
    if not tok: return {"status":"warn","reason":"no token in env"}
    req = urllib.request.Request("https://api.github.com/user", headers={"Authorization":f"Bearer {tok}","Accept":"application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r: return {"status":"ok" if r.status==200 else "warn","http":r.status}
    except Exception as e: return {"status":"warn","reason":str(e)}
def probe_exa():
    key = os.environ.get("REACH_EXA_KEY") or os.environ.get("EXA_API_KEY","")
    if not key: return {"status":"warn","reason":"no key"}
    body = json.dumps({"query":"zeus ai","numResults":1}).encode()
    req = urllib.request.Request("https://api.exa.ai/search", data=body, headers={"x-api-key":key,"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r: return {"status":"ok" if r.status==200 else "warn","http":r.status}
    except Exception as e: return {"status":"warn","reason":str(e)}
print("   github:", probe_gh())
print("   exa:   ", probe_exa())
PY

echo "-- 5. patch the doctor CLI AND bridge checkers to prefer no-write probes --"
if [ -f /root/kali/kali/zeus-integration/doctor-verify-fix.py ]; then
  python3 /root/kali/kali/zeus-integration/doctor-verify-fix.py 2>&1 | head -4
else
  python3 /root/kali/kali/zeus-integration/doctor-verify-fix.py 2>/dev/null || echo "   doctor-verify-fix.py not found (kit v61)"
fi

echo "-- 6. global confirm gate --"
if [ -n "$GATE_PY" ]; then
  echo "   found: $GATE_PY — running"
  python3 "$GATE_PY"
else
  echo "   !! confirm-gate-global.py not found — unzip kit v61 to /root/kali and rerun"
fi
[ -f "$BAK" ] && echo "   gate backup: $BAK"

echo "-- 7. restart the bridge (correct unit: zeus-reach) --"
systemctl daemon-reload
systemctl enable --now zeus-reach 2>>"$LOGF"
systemctl restart zeus-reach 2>>"$LOGF" || systemctl start zeus-reach 2>>"$LOGF"
systemctl restart zeus-reach-mcp 2>/dev/null || true
systemctl is-active zeus-reach || echo "!! zeus-reach not active — journalctl -u zeus-reach"

echo "-- 8. verify on the wire --"
sleep 2
curl -s https://zeusaiintelligence.com/reach/doctor | python3 -c "
import json,sys
d=json.load(sys.stdin); doc=d.get('doctor',d)
ch=doc.get('channels',{})
if not ch: ch={k:v for k,v in doc.items() if isinstance(v,dict)}
for k in ['github','exa_search','twitter','linkedin','xueqiu','web']:
    v=ch.get(k,{})
    print(f'   {k:10s}', (v.get('status') if isinstance(v,dict) else '?'))
" 2>/dev/null || echo "   /reach/doctor probe failed — check bridge logs"
echo "═══════ v2 done — re-read statuses above ═══════"