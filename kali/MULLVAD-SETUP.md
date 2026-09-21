# Mullvad VPN + Mullvad Browser — PC Setup Guide
**Honest boundary:** this agent cannot install software on your Windows PC — these are your steps, in order. Activate = paste your account number; no email needed.

---

## Part 1 — Mullvad VPN (the app you downloaded)

**Install**
1. Run the downloaded `MullvadVPN-*.exe` (Windows).
2. Let it install; launch **Mullvad VPN**.

**Activate (account number, 16 digits — no email required)**
1. Open the app → select **Log in / Create account**.
2. If you have a **16-digit account number**: paste it → **Log in** → done.
   - Where to find it: your Mullvad welcome email, or mullvad.net → Account.
3. If NEW: the app generates a fresh account number for you — **write it down / save it** (it IS your login; losing it loses the account).

**Connect**
1. Main screen → **Select location** → pick UK (or nearest) → **Connect**.
2. Toggle is active when the padlock shows **Locked / Secured**.

**Verify it's working (not just "connected")**
- Open any browser → visit [mullvad.net/en/check](https://mullvad.net/en/check) →
  expect a green **"You are protected / You are using Mullvad"** banner and an IP
  that is NOT your home IP.
- In-app: **WireGuard** protocol is the default (fast, secure); leave it.

**Keep-on rules**
- Leave the app running for persistent protection.
- If a site blocks your region, switch location (rotates IP), don't disable VPN.

## Part 2 — Mullvad Browser (needs installing — it's a separate download)

**Install**
1. Go to [mullvad.net/en/browser](https://mullvad.net/en/browser) → **Download for
   Windows**.
2. Run the installer (or extract the zip) → launch **Mullvad Browser**.
3. (You can also install it via the VPN app: **Settings → Mullvad Browser → Install**.)

**Use**
- It's a hardened Firefox fork — is intended to be used **with** Mullvad VPN on.
- For ZEUS work: log into X/Twitter in Mullvad Browser when exporting cookies —
  same cookies the droplet agent uses.

## Confirm when complete
Paste me: (1) the mullvad.net/en/check result (protected or not), (2) whether
Mullvad Browser launches. I'll mark both confirmed in the estate log.

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).