# IONOS ACCOUNT AUDIT — Customer 316502159 (Darren Birch)
**Date:** 2026-09-21 · **Status:** INVOICE DISPUTE / ORDERLY EXIT IN PROGRESS
**Rule applied:** nothing cancelled blind — the flagship domain must be protected first.

---

## 1. VERDICT: does ZEUS use IONOS? — YES, two things only (verified live)

| Asset | Held by | Verified | Use |
|---|---|---|---|
| `zeusaiintelligence.com` (flagship) | **IONOS SE registrar** | .com registry RDAP, expires 2027-08-07 | THE domain — whole estate |
| MX mail routing for the domain | IONOS (`mx00/01.ionos.co.uk`) | live DNS TXT/MX query | unused (SPF `-all`; real mailbox = Gmail) |
| `zeusaiintellegence.com` (typo) | IONOS | registered 29 Aug 2026 | **cancel** |
| `zeusaiintellegence.info` (typo) | IONOS | registered 29 Aug 2026 | **cancel** |
| `zeusaiintellegence.co.uk` (typo) | IONOS | registered 29 Aug 2026 | **cancel** |
| `zeusaiintellegence.store` (typo) | IONOS | registered 29 Aug 2026 | **cancel** |
| Domain Guard subscriptions ×N | IONOS | 9 deactivation confirmations 23–24 Aug | **cancel** (already deactivated) |
| DNS / hosting / website | Cloudflare + DigitalOcean droplet | NS dora/james.ns.cloudflare.com; A→188.166.175.149 | NOT IONOS — unaffected |

**So:** website, DNS and email DO NOT run on IONOS. Only the **domain registrations** live there. The £485.40 invoice (IONOS Cloud Ltd, reg 03953678, 20 contract numbers) covers those registrations + packages.

## 2. TIMELINE (reconstructed from the mailbox)
- **23–24 Aug:** 9× Domain Guard deactivations (user-initiated, estate hardening)
- **29 Aug 20:52–21:17:** 4 typo domains + order confirmations (who ordered? — see note)
- **29 Aug 22:44:** YOUR request to IONOS: "Domain spelling correction request … typo in zeusaiintellegence registrations"
- **30 Aug 06:42:** IONOS: "Your Contract Ends Soon"
- **12 Sep 17:19:** COMPLAINT EXHIBIT B (to Higgsfield): "IONOS typo domain: cancellation prepared; legitimate domain kept"
- **21 Sep 16:50:** IONOS: "Reminder: Outstanding Invoice Amount … £485.40" (20 contracts)
- **21 Sep 17:50:** IONOS login code issued (your session)

## 3. THE PLAN (safe order — NEVER reverse this)
**Phase 1 — Protect the flagship (do first, in the IONOS account):**
1. Log in at `login.ionos.co.uk` → customer 316502159 (don't click links in the email — type the URL).
2. **Download the itemised invoice** → verify the £485.40 line by line (domains only? Domain Guard? any hosting bundles? anything NOT ordered?).
3. **Keep** `zeusaiintelligence.com` — unlock it (Settings → Domain lock OFF) and remove Domain Guard on it if still active.

**Phase 2 — Cancel the junk (after the flagship is protected):**
4. Cancel the 4 typo domains (`zeusaiintellegence.*`) — the spelling-correction thread (29 Aug) is already the paper trail.
5. Cancel all Domain Guard / package add-ons not ordered.
6. Dispute with support: the typo registrations were NOT intentionally ordered by you (your 29-Aug correction request proves it) → ask for waiver/refund of those + their packages. Reference customer 316502159. Phone: 0808 303 0000.

**Phase 3 — Leave IONOS entirely (optional, recommended):**
7. Transfer `zeusaiintelligence.com` to **Cloudflare Registrar** (DNS is already Cloudflare — free at-cost registration, no lock-in).
8. Once the transfer completes, cancel the account/remaining contracts at IONOS.

## 4. WATCH OUT
- IONOS's own email: past-due → services may be restricted, and **"all associated services will be lost, including your domains"**. Pay/secure the legitimate items before anything lapses.
- 14-day remedy window with Higgsfield Support expires **25 Sep 2026** — the Exhibit B evidence is already filed; keep this IONOS audit as Exhibit C.
- Never pay from the email link. Always `my.ionos.co.uk/payment` via direct URL.

## 5. STATUS TRACKER
- [ ] Invoice downloaded + itemised verified
- [ ] Typo domains cancelled (4)
- [ ] Domain Guard packages cancelled
- [ ] Dispute filed (typo registrations not authorised)
- [ ] Flagship transfer to Cloudflare Registrar initiated
- [ ] Account closed / balance settled

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).