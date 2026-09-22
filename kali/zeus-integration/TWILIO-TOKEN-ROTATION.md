# TWILIO AUTH TOKEN ROTATION — RUNBOOK (2 minutes)
**Why:** the Twilio auth token appeared on a shared dashboard screenshot (22 Sep 2026) — treat it as exposed and rotate now.

## Steps
1. `console.twilio.com` → log in (account `zeusaiintellegence.com`)
2. Top-right **Admin** dropdown → **API keys & tokens** (or Settings → API keys & tokens)
3. Scroll to **Live credentials → Auth Token** → click the **rotate/refresh** control to generate a new token
4. **Immediately update anything that consumes it** — the estate's incident alerting:
   - Droplet env: `/opt/zeus-reach.env` → `TWILIO_AUTH_TOKEN` (then `systemctl restart agent-reach`)
   - Pipedream Twilio connector: **reconnect** the Twilio connection in the connectors UI with the new token (the current connection has stale creds — that's why live reads fail)
5. Old token dies instantly on rotation — safe to discard

## Proof it worked
```bash
# old behavior (stale): 401
curl -u "<ACCOUNT_SID>:<OLD_AUTH_TOKEN>" \
  "https://api.twilio.com/2010-04-01/Accounts/<ACCOUNT_SID>.json" -o /dev/null -w '%{http_code}\n'
# after rotation: 200
```

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).