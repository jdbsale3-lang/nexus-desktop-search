# IONOS INVOICE ITEMISATION — £485.40 · Customer 316502159
**Source (updated 21 Sep):** live invoice overview screenshots — 16 invoices, ALL dated 18/09/2026, MOST marked **"Payment failed"** + the 21 Sep reminder listing.

---

## WHAT THE INVOICE PAGE ACTUALLY SHOWS (your screenshots)
- **16 invoices, every one dated 18/09/2026** → this is ONE collection run: IONOS tried to charge on 18/09, the card **declined**, and the unpaid total is what the reminder quoted (£485.40).
- **Good news:** the payments FAILED — so you don't owe a paid-subscription debt; you owe nothing that's been collected. The dispute must make sure **failed ≠ due**: every line is now a cancellation + waiver target.
- Services that exist on the account (contracts from screenshots + mailbox):

| Service | Contract | Failed amount | Status |
|---|---|---|---|
| IONOS AI Search Manager | 113387976 | £34.80 | Payment failed |
| IONOS AI Search Manager | 113382207 | £34.80 | Payment failed |
| IONOS AI App & Site Builder Starter | 113383319 | £30.00 | Payment failed |
| IONOS Email Marketing Plus | 113389775 | £18.00 | Payment failed |
| IONOS Email Marketing Plus | 113387974 | £18.00 | Payment failed |
| IONOS MyWebsite Now Starter | (from invoice list) | ? | Payment failed |
| IONOS MyWebsite Now Plus | (from invoice list) | ? | Payment failed |
| IONOS MyWebsite Now eCommerce Plus | (from invoice list) | ? | Payment failed |
| IONOS MyWebsite Now eCommerce Starter | (from invoice list) | ? | Payment failed |
| IONOS Email archiving | (from invoice list) | ? | Payment failed |
| IONOS Web Hosting Plus | (from invoice list) | ? | Payment failed |
| IONOS VPS Windows XL+ | 113400130 | ? | Cancel requested 23 Aug (phone-confirm) |
| IONOS GPT | 113271957 | ? | Contract ends 06.09.2026 |
| IONOS Mail Business 5 Lic. | (29 Aug order) | ? | — |
| IONOS Virusscan | (29 Aug order) | ? | — |
| IONOS AI Email Assistant 1u | (29 Aug order) | ? | — |
| IONOS Instant Domain | **112790544** (portal, not email's 113514895) | ? | Cancel flow IN PROGRESS (your screenshot) |
| 4 typo domains `zeusaintellegence.*` | — | — | expiring 29/08/2027, Guard "Order" not active |

## KEY FINDINGS FROM YOUR DOMAIN LIST SCREENSHOT
- The **typo domains are spelled `zeusaintellegence.*`** (missing the 'i') — matching the correction request.
- All 4 typos: **Domain Guard "Order"** (red) = NOT purchased/active — one less thing to fight.
- `zeusaiintelligence.org` → DNS **178.62.46.133** — that's a DIFFERENT DigitalOcean IP than flagship 188.166.175.149. Either an old droplet or an unclaimed record — **decide what `.org` should point at or park it** (candidate to keep: it's the correct spelling).
- `zeusaiintelligence.com` flagship: Domain Guard **"Not active"**, NS = Cloudflare. Transfer-ready once the IONOS lock is off + 60-day wait clears (6 Oct).
- `.info/.co.uk/.store` variants show Domain Guard **"Waiting"** (deactivation pending) — finish those deactivations or they may bill.

## DISPUTE TARGET (updated)
1. **Cluster A (typo, full waiver):** 4× `zeusaintellegence.*` + anything attached. Guard never bought — nothing to pay.
2. **Cluster B (already-cancelled 23 Aug):** VPS 113400130 — stop billing, refund.
3. **Cluster C (never used, cancelled/being cancelled):** MyWebsite Now ×4, AI Search Manager ×2, AI App & Site Builder, Email Marketing ×2, Email archiving, Web Hosting, Mail Business, Virusscan, AI Assistant, Instant Domain 112790544, GPT 113271957, VPS.
4. **Cluster D (legitimately keep):** flagship registration line ONLY.
> Because every collection failed, the £485.40 is **uncollected**, not paid — the dispute stance is: waive A + B + C (nothing was used, most contracts were cancelled within 3 weeks of ordering), pay only D if anything at all is due.

## ACTION STATUS (from your screenshots — continued effort needed)
- [x] Invoice page reached, invoices visible (16× 18/09)
- [x] Cancel flow OPEN for Instant Domain (112790544) — survey page reached; **complete it: tick the awareness checkbox → "Make a note of cancellation now"**
- [ ] Cancel the other 15 products in the same loop (Part 4 of CLICK-PATHS)
- [ ] 4 typo domains: set **do-not-renew** (they expire 29/08/2027; don't renew, don't pay)
- [ ] Domain Guard "Waiting" on `.info/.co.uk/.store`: finish deactivation
- [ ] VPS phone call 0808 189 0625 (already-left deadline)
- [ ] Transfer flagships on/after 6 Oct (auth code received ✅)

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).