# Cookie Setup Runbook — agent-reach social channels (Twitter / LinkedIn / Xueqiu)

Purpose: give the ZEUS Doctor the explicit credentials it needs to flip the
warn channels to ok. All commands run on the droplet host (`root@aegis-api:~#`),
the same Linux bash you are in. Each channel needs a cookie export from the
browser using the Cookie-Editor extension the Doctor already references.

## 0. Install Cookie-Editor (browser, one time)
- Chrome/Edge/Chromium: install the **Cookie-Editor** extension.
- Give it access to the site you're about to export.

## 1. Twitter / X — `agent-reach configure twitter-cookies`
1. Open **x.com** in the browser, logged in.
2. Cookie-Editor → **Export** (JSON format) — this copies a cookie JSON string.
3. On the droplet bash:
   ```bash
   agent-reach configure twitter-cookies
   # when it prompts "Value for twitter-cookies:", paste the exported JSON,
   # then press Enter
   ```
4. Verify: `curl -s https://zeusaiintelligence.com/reach/doctor | grep -A2 twitter`
   → expect `"status": "ok"`.

**Why this is safe:** the Doctor never reads browser cookies itself (its own
README says so — that is the exact warn message we decoded). Pasting the export
is the intended flow.

## 2. LinkedIn — start the MCP service + verify
Doctor's warn: "LinkedIn MCP 已写入 mcporter 配置，但 Doctor 未启动本地服务做连通验证".
Fix = start the local LinkedIn MCP service so Doctor can ping it:
```bash
agent-reach install --system --channels linkedin   # ensures backend installed
mcporter run linkedin-mcp &                        # start local service
sleep 3
curl -s https://zeusaiintelligence.com/reach/doctor | grep -A2 linkedin
```
If it still warns, re-authenticate the OAuth: `agent-reach configure linkedin`.

## 3. Xueqiu — login cookie (HTTP 400 fix)
Doctor's warn: "Xueqiu API 连接失败：HTTP Error 400".
- Log in to xueqiu.com in the browser (it requires login for the API).
- Cookie-Editor → Export.
- On the droplet:
  ```bash
  agent-reach configure xueqiu-cookies
  # paste the exported JSON, Enter
  ```
- Verify: `curl -s https://zeusaiintelligence.com/reach/doctor | grep -A2 xueqiu`.

## 4. Final verification (all five)
```bash
curl -s https://zeusaiintelligence.com/reach/doctor | python3 -c "
import json,sys
d=json.load(sys.stdin)
for k,v in d.get('doctor',{}).items():
    print(k, v.get('status'))
"
```
Expected: github **ok** · exa_search **ok** · twitter **ok** · linkedin **ok** ·
xueqiu **ok** (after the four setups + the doctor-verify-fix for github/exa).

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).