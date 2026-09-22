#!/usr/bin/env bash
# droplet-urgent-fix.sh — ONE command: tokens into the bridge env, doctor flips
# github/exa to ok, global confirm gate wired, locale English, services restarted.
# Idempotent. Run as root on the DROPLET:  bash droplet-urgent-fix.sh
set -u
echo "═══════ ZEUS DROPLET URGENT FIX ═══════"
ENV=/opt/zeus-reach.env
BRIDGE=/opt/agent-reach-bridge.py
BAK=$BRIDGE.bak-confirm-global
LOGF=/var/log/zeus-reach-setup.log

echo "-- 0. pre-flight: env file present? --"
[ -f "$ENV" ] || { echo "!! $ENV missing"; exit 2; }
grep -q "EXA_API_KEY" "$ENV" || echo "   note: no EXA_API_KEY line in $ENV"

echo "-- 1. put LANG/LC_ALL + tokens into the bridge env (English locale) --"
grep -q "^LANG=" "$ENV" || echo "LANG=en_GB.UTF-8" >> "$ENV"
grep -q "^LC_ALL=" "$ENV" || echo "LC_ALL=en_GB.UTF-8" >> "$ENV"
grep -q "^GITHUB_TOKEN=" "$ENV" || echo "GITHUB_TOKEN=$(git -C ~/kali remote get-url origin 2>/dev/null | sed -n 's|.*x-access-token:\([^@]*\)@.*|\1|p')" >> "$ENV"
echo "   env now has: $(grep -oE '^(LANG|LC_ALL|GITHUB_TOKEN|EXA_API_KEY)=' "$ENV" | tr '\n' ' ')"

echo "-- 2. source env for this session + prove probes --"
set -a; . "$ENV"; set +a
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
    key = os.environ.get("EXA_API_KEY","")
    if not key: return {"status":"warn","reason":"no key"}
    body = json.dumps({"query":"zeus ai","numResults":1}).encode()
    req = urllib.request.Request("https://api.exa.ai/search", data=body, headers={"x-api-key":key,"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r: return {"status":"ok" if r.status==200 else "warn","http":r.status}
    except Exception as e: return {"status":"warn","reason":str(e)}
print("   github:", probe_gh())
print("   exa:   ", probe_exa())
PY

echo "-- 3. global confirm gate (download into place if absent) --"
if [ -f /root/kali/zeus-integration/confirm-gate-global.py ]; then
  echo "   patcher present — running"
  python3 /root/kali/zeus-integration/confirm-gate-global.py
elif [ -f /root/kali/confirm-gate-global.py ]; then
  echo "   patcher present (root of kali) — running"
  python3 /root/kali/confirm-gate-global.py
else
  echo "   !! confirm-gate-global.py NOT on droplet — fetch from kit v59/v60 zip first"
  echo "   (URL in chat; unzip, then re-run this script)"
fi
ls -la "$BAK" 2>/dev/null && echo "   gate backup exists: $BAK"

echo "-- 4. restart the bridge (correct service name) --"
systemctl daemon-reload
systemctl enable --now zeus-reach 2>>"$LOGF"
systemctl restart zeus-reach 2>>"$LOGF" || systemctl start zeus-reach 2>>"$LOGF"
systemctl restart zeus-reach-mcp 2>/dev/null || true
systemctl is-active zeus-reach || echo "!! zeus-reach not active — journalctl -u zeus-reach"

echo "-- 5. verify on the wire --"
sleep 2
curl -s https://zeusaiintelligence.com/reach/doctor | python3 -c "
import json,sys
d=json.load(sys.stdin); doc=d.get('doctor',d)
ch=doc.get('channels',{})
if not ch: ch={k:v for k,v in doc.items() if isinstance(v,dict)}
for k in ['github','exa_search','twitter','linkedin','xueqiu','web']:
    v=ch.get(k,{})
    print(f'   {k:10s}', (v.get('status') if isinstance(v,dict) else '?'))
"
echo "═══════ done — re-check /reach/doctor statuses above ═══════"