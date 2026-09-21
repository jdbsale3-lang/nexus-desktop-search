# Twitter Cookie Test Runbook — agent-reach twitter-cookies
Purpose: set AND prove Twitter/X works in ZEUS — cookie configured is not cookie working.
All commands on the droplet host (`root@aegis-api`), values from your PC browser.

## Step 1 — export the two cookies (your PC, x.com, logged in)
1. Open x.com **in a logged-in session**.
2. Press **F12** → **Application** tab → **Cookies** → `https://x.com`.
3. Find **`auth_token`** — copy its **Value** (long, alphanumeric).
4. Find **`ct0`** — copy its **Value** (CSRF token).
5. Keep both in a scratchpad; they expire — re-export fresh if the test fails.

## Step 2 — configure (droplet)
```bash
agent-reach configure twitter-cookies
# at "Value for twitter-cookies:" paste BOTH on ONE line, space-separated:
#   <auth_token_value> <ct0_value>
# then Enter
```
**Accepted formats** (verbatim from the tool): (1) AUTH_TOKEN and CT0 separated
by whitespace · (2) a Cookie-Editor Header String. NOT the full JSON export.

## Step 3 — PROVE it (the only receipt that counts)
```bash
curl -s https://zeusaiintelligence.com/reach/doctor | python3 -c "
import json,sys
d=json.load(sys.stdin)
t=d.get('doctor',{}).get('twitter',{})
print('twitter status:', t.get('status'))
print('message:', str(t.get('message'))[:160])
"
```
**PASS:** `twitter status: ok`
**FAIL:** still `warn` → cookies expired or ct0 wrong → repeat Step 1 fresh, Step 2.

## Step 4 — live sanity (optional but definitive)
Ask ZEUS: "post a test to twitter" or use agent-reach's post command — a real
post proves the end-to-end lane, then delete if unwanted.

## Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| `Could not find auth_token and ct0` | pasted JSON or wrong format | Step 1 copy VALUES only, space-separated |
| status warn right after config | cookies expired / browser logged out | re-export fresh session |
| 401 on post | token invalidated by x.com | repeat Steps 1–2 |

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).