# WALKTHROUGH — Transfer zeusaiintelligence.com to Cloudflare Registrar
Verified 21 Sep 2026 against Cloudflare's official transfer docs + IONOS help. Allow ~30 min active, ~5–10 days total.

## LIVE STATUS (checked 22 Sep 2026 from droplet RDAP)
- registrar: **IONOS SE** (transfer NOT done)
- status: **`client transfer prohibited`** (IONOS lock still ON)
- last registry change: **2026-08-24** — nothing moved since
- → PRESS 1 (unlock at IONOS) must happen before PRESS 2 (enter code at Cloudflare)

---

## BEFORE YOU START — check these (all confirmed except 1 and 2)
| Check | Status |
|---|---|
| Domain is **Active on Cloudflare** (DNS zone) | ✅ your screenshot: "Active", 2.01k visitors |
| Valid **payment method on file** in Cloudflare | ⚠️ confirm in Account → Billing |
| Registration older than **60 days** (ICANN) | ⛔ registered 07 Aug → **eligible 06 Oct 2026** |
| No DNSSEC at IONOS | ✅ not in use (Cloudflare zone has none) |
| No registrant detail change in last 60 days | ✅ (fresh registration, nothing changed) |

---

## STEP 1 — IONOS: UNLOCK the domain (today)
Registry still shows `client transfer prohibited` = IONOS lock ON — this must go first.
1. `https://my.ionos.co.uk` → left menu → **Domains & SSL**
2. Click **zeusaiintelligence.com**
3. Open the **Renewal & Transfer** tab/page
4. Switch **transfer lock / registrar lock OFF** (may trigger a confirmation email → open it → click confirm)
5. Confirm the lock is gone — the registry status checks below prove it

## STEP 2 — IONOS: GET the auth code (when ready to paste — codes expire)
1. Same **Renewal & Transfer** page
2. Click **Show Authorisation Code** (it's the EPP/auth code)
3. Wait — it can take a few minutes to be fetched from the registry
4. Copy it (20 chars, mixed symbols like `-9A|Pvd...`) — you already have one from earlier; if it errors on paste, request a fresh one now

## STEP 3 — CLOUDFLARE: initiate the transfer
1. `https://dash.cloudflare.com` → log in (your account)
2. Left sidebar → **Domains** → **Transfers** (the same menu that shows Overview / Registrations / Transfers)
3. On the **Transfers** page → **Transfer a domain** (or "Transfer to Cloudflare")
4. Type **zeusaiintelligence.com** → click **Next**
5. Paste the **auth code** into the **Authorization code** field
6. Review the cost — `.com` transfers: **~£10–11 incl. +1 year** (expiry 2027-08-07 → **2028-08-07**)
7. Click **Transfer** → charge the payment method on file
8. **Confirm your contact information** (registrant details — Cloudflare redacts them in WHOIS by default; use the same details as IONOS registrant)
9. Tick the registration ToS → **Confirm transfer**

## STEP 4 — APPROVE on the IONOS side
1. IONOS emails you a transfer notice (and Cloudflare sends a **Form of Authorization / FOA email** to the registrant)
2. **Click the approval / confirm link** in the IONOS email (do NOT click any "reject" option)
3. If IONOS asks via dashboard → Domains & SSL → the domain → approve the outgoing transfer

## STEP 5 — WAIT + VERIFY
- Status on Cloudflare **Transfers page**: `Transfer in progress` → `Pending approval` → (after ~5 days) done
- IONOS normally releases in ~5 business days
- **ICANN 60-day lock note:** if initiated now, the registry holds completion until 06 Oct then finalizes; either way, expect the flip in early-mid October
- **Final proof:**
```bash
curl -s https://rdap.verisign.com/com/v1/domain/zeusaiintelligence.com
# registrar: CLOUDFLARE, INC.   ← success
```
- Site stays live through all of it (DNS unchanged — already Cloudflare)

## TROUBLESHOOTING (from Cloudflare's docs)
| Symptom | Cause | Fix |
|---|---|---|
| "Can't enter auth code / page blocked" | zone still **Pending** | wait for **Active** status (yours is Active ✅) |
| Stuck `Transfer in progress` >24h | domain still locked at IONOS | re-check Step 1, disable every lock type |
| `Transfer rejected` | declined at IONOS, or not eligible | click **Retry** → re-run Steps 1–3 |
| Auth code invalid | code expired | request a fresh code in Step 2, re-paste |
| No approval email | registrant email wrong | check the email on the IONOS account contact card; fix then re-initiate |

## REGISTRY STATUS — HOW TO PROVE THE LOCK IS OFF (before starting Step 3)
```bash
curl -s https://rdap.verisign.com/com/v1/domain/zeusaiintelligence.com | grep -o '"status": \[[^]]*\]'
# BEFORE unlock: ["client transfer prohibited"]
# AFTER unlock:  [] (or no clientTransferProhibited)
```
When it returns an empty status list, the IONOS lock is cleared and you're clear for Step 3.

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).