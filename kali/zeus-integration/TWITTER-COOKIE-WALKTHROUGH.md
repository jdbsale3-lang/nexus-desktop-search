# Twitter Cookie Setup — Step-by-Step Walkthrough
Goal: give ZEUS the estate's Twitter lane. Cookie configured is not cookie working —
this walkthrough ends with visible proof.

## Before you start
- Mullvad VPN running (auto-connect on). Mullvad Browser open.
- Droplet terminal available: `root@aegis-api:~#` (SSH or DO console).

---

## STEP 1 — Export the two cookies (Mullvad Browser, x.com logged in)
1. Open [x.com](https://x.com) — ensure you're logged into the account you want ZEUS to use.
2. Press **F12** (devtools) → click the **Application** tab (top bar, maybe under `>>`).
3. Left panel: **Storage → Cookies → https://x.com**.
4. In the cookie table find **`auth_token`**:
   - Click its **Value** cell → copy the full value (long, letters+digits).
5. Find **`ct0`**:
   - Copy its **Value** too.
6. Keep both on a scratchpad (e.g., Notepad). They're session-bound — if the test fails later, re-export fresh.

> Ignore any console "Source map error" — Twitter requests an internal .map file
> that isn't public. It's harmless noise, not a functional or security error.

## STEP 2 — Configure on the droplet
At `root@aegis-api:~#`:
```bash
agent-reach configure twitter-cookies
```
When you see `Value for twitter-cookies:`, paste BOTH values on ONE line, separated by one space:
```
<auth_token_value> <ct0_value>
```
press Enter.

**Accepted formats (the tool is strict):**
1. `AUTH_TOKEN` and `CT0` separated by whitespace  ← use this
2. A Cookie-Editor Header String
The full JSON export is NOT accepted — it rejects with "Could not find auth_token and ct0".

## STEP 3 — PROVE it (the only receipt)
```bash
curl -s https://zeusaiintelligence.com/reach/doctor | python3 -c "
import json,sys
t=json.load(sys.stdin).get('doctor',{}).get('twitter',{})
print('twitter status:', t.get('status'))
print('message:', str(t.get('message'))[:160])
"
```
**PASS:** `twitter status: ok`
**FAIL:** still `warn` → cookies expired or ct0 stale → return to STEP 1, re-export fresh, repeat STEP 2.

## STEP 4 — Live sanity (optional, definitive)
Ask ZEUS to post a harmless test message to Twitter, or use agent-reach's post command.
A real post proves the lane; delete it after if not wanted.

## Troubleshooting quick table
| Symptom | Cause | Fix |
|---|---|---|
| `Could not find auth_token and ct0` | pasted JSON or wrong format | copy VALUES only, space-separated |
| status still warn after config | cookies expired | re-export fresh session |
| 401 on post | token invalidated by x.com | repeat Steps 1–2 |
| Mullvad-blocked page | location blocked by site | switch Mullvad location, keep VPN on |

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).