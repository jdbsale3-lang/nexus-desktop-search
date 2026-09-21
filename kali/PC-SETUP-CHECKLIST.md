# ZEUS PC SETUP CHECKLIST — 24/7 AEGIS Protection + Estate Tools
**Purpose:** fully protect your PC and wire its browser session into the estate. Check each box as done.

---

## PART A — Mullvad VPN (24/7 protection) ✅ REQUIRED
- [ ] **Install:** run the downloaded `MullvadVPN-*.exe`, launch Mullvad VPN
- [ ] **Activate:** Log in / Create account → paste your **16-digit account number** (from your Mullvad welcome email — the number IS the login; save it)
- [ ] **Auto-connect at startup:** Settings → **Auto-connect on startup: ON** (this is what makes it 24/7)
- [ ] **Select location:** pick UK (or nearest) → **Connect**
- [ ] **Verify it's real:** visit [mullvad.net/en/check](https://mullvad.net/en/check) → expect green **"You are protected"** and an IP that is NOT your home IP
- [ ] **Leave it running** — closing it disables protection

## PART B — Mullvad Browser (private browsing / cookie export) ✅
- [ ] **Install:** [mullvad.net/en/browser](https://mullvad.net/en/browser) → **Download for Windows** → install → launch
- [ ] (Alternative: VPN app → Settings → Mullvad Browser → Install)
- [ ] **Use with the VPN on** — it's a hardened Firefox fork meant to pair with Mullvad
- [ ] Log into **x.com inside Mullvad Browser** for the cookie export below

## PART C — Twitter cookies for the ZEUS agent (ties PC to estate) ✅
- [ ] x.com logged-in (in Mullvad Browser)
- [ ] **F12 → Application → Cookies → https://x.com**
- [ ] Copy **`auth_token`** value and **`ct0`** value (both)
- [ ] On the droplet: `agent-reach configure twitter-cookies` → paste BOTH space-separated → Enter
- [ ] Verify: doctor shows twitter `status: ok`

## PART D — final estate verification ✅
- [ ] On droplet: `bash ~/kali/droplet-autorun.sh` (runs doctor-verify, confirm-gate, SearXNG, crons, estate probe in one go)
- [ ] Confirm output ends green (no FAILED lines)

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).