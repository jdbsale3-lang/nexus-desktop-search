# IONOS — DELETE EVERYTHING, STEP BY STEP (customer 316502159)
**Safest order possible: nothing here can kill `zeusaiintelligence.com` if you follow it top-to-bottom.**
Do these in the IONOS Customer Portal: type `https://login.ionos.co.uk` yourself — never click links in emails.

---

## STEP 0 — PREP (5 minutes)
- [ ] Log in at `login.ionos.co.uk` with your credentials + login code (the 21 Sep code email shows you're in).
- [ ] Open **My account → Invoices** → download the **£485.40 invoice PDF** and save it to `kali/IONOS-INVOICE-2026.pdf`. You'll need it for the dispute.
- [ ] Open **My contracts / Products** — list every contract number. Cross-check against the `IONOS-INVOICE-ITEMISATION.md` table.

## STEP 1 — KEEP THE FLAGSHIP SAFE (prerequisite, do first)
- [ ] In **Domain management → zeusaiintelligence.com**:
  - [ ] **Domain Guard / DomainLock: OFF** (you already requested this 23–24 Aug — confirm it actually went through; the confirmations were *requests*, not completions)
  - [ ] **Auto-renew: ON** (do NOT let it lapse mid-cleanup — expiry 2027-08-07)
  - [ ] Export/note the current **auth code (EPP code)** — you'll need it for the transfer
- [ ] Confirm the domain's DNS still points at Cloudflare (it does): `dora.ns.cloudflare.com` / `james.ns.cloudflare.com`.

## STEP 2 — CANCEL THE SERVICES (in the portal, per product)
In **My contracts**, find each contract and click **Cancel** (Kündigen / Cancel):

| Product | Contract no. | Action | Trap |
|---|---|---|---|
| IONOS VPS Windows XL+ | 113400130 | CANCEL — **phone-confirm it**: call **0808 189 0625** and say "I confirm cancellation of contract 113400130" | email said confirm **within 14 days of 23 Aug** — if lapsed, call anyway; a rep can still process it |
| IONOS GPT | 113271957 | CANCEL (contract ends 06.09.2026 — make sure it doesn't auto-renew) | ends soon; do not let it renew |
| IONOS Mail Business 5 Lic. | (order 29 Aug 21:17) | CANCEL | check if invoice line exists |
| IONOS Virusscan | (order 29 Aug 20:57) | CANCEL | check if invoice line exists |
| IONOS AI Email Assistant 1 user | (order 29 Aug 20:57) | CANCEL | check if invoice line exists |
| IONOS Instant Domain | 113514895 | CANCEL (if it's the typo bundle) | verify which domain it covers first |
| Any Domain Guard packages | — | CANCEL each | already deactivated 23–24 Aug; confirm no residual billing |

## STEP 3 — CANCEL THE TYPO DOMAINS (4)
In **Domain management**, cancel (don't renew / let expire):
- [ ] `zeusaiintellegence.com` (double-L)
- [ ] `zeusaiintellegence.info`
- [ ] `zeusaiintellegence.co.uk`
- [ ] `zeusaiintellegence.store`
> Keep the email "Domain spelling correction request — 29 Aug 22:44" — it's your proof these were unintended. **Do NOT renew them** (each renewal is another charge).

## STEP 4 — DECIDE ON THE OTHER ZEUSAINTELLIGENCE / ZEUS DOMAINS
The Domain Guard deactivation emails (23–24 Aug) also mention these — check each in the portal and decide: keep or cancel.
- [ ] `zeusaiintelligence.org` / `.info` / `.co.uk` / `.store` (correct-spelling variants — worth keeping the .co.uk/.org set? they're cheap; cancel if unused)
- [ ] `zeus-scan-fit.com` (unused project domain — cancel unless it's active)

## STEP 5 — TRANSFER THE FLAGSHIP OUT (then you can delete the account)
> ⚠️ **Timing catch:** `.com` domains are locked from transfer for **60 days after registration** (ICANN rule). `zeusaiintelligence.com` was registered **2026-08-07** → **transfer eligible from 2026-10-06**. Do the Steps 1–4 now, launch the transfer on/after 6 Oct, then:
- [ ] IONOS: unlock domain, collect EPP/auth code
- [ ] Cloudflare: **Registrar → Transfer domain → zeusaiintelligence.com** (DNS already on Cloudflare = zero disruption)
- [ ] Confirm transfer email within 5 days; ~5–7 days total
- [ ] After transfer completes: verify site still live (200 + headers 5/5)

## STEP 6 — CLOSE THE ACCOUNT
- [ ] Pay or dispute the balance FIRST (see DISPUTE message); an unpaid account can't be closed cleanly
- [ ] In portal: **My account → Close account / delete customer data** (GDPR Art. 17 erasure request by email if no UI option: `datenschutz@ionos.co.uk`)
- [ ] Check no Direct Debit/standing order for IONOS remains in Tide → Payments → Recurring

## STEP 7 — PROVE IT'S GONE
```bash
# on the droplet
curl -s https://dns.google/resolve?name=zeusaiintelligence.com&type=NS   # expect Cloudflare
curl -s https://dns.google/resolve?name=zeusaiintellegence.com&type=NS   # expect NXDOMAIN after expiry
```
- [ ] Watcher (v3.2, 80 anchors incl. ionos) will alert if any new IONOS mail arrives — that's the safety net.

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).