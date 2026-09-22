# FLAGSHIP DOMAIN TRANSFER PLAN — zeusaiintelligence.com → Cloudflare Registrar
**Target:** free the flagship from IONOS entirely, land it at Cloudflare (DNS is already there — zero disruption).
**Status:** WAITING FOR TRANSFER ELIGIBILITY (see the lock below).

---

## ⚠️ THE NON-NEGOTIABLE TIMING CATCH
ICANN rules lock every `.com`/`.net`/`.org` domain from transfer for **60 days after initial registration**.
- Registered: **2026-08-07** (per .com registry)
- **Transfer eligible: 2026-10-06** — earliest date
- **Do NOT attempt the transfer before 2026-10-06** — the registry will refuse it.

Until 6 Oct: do Steps 1–3 of the delete-all guide (invoice, cancellations, dispute) — the domain stays safely at IONOS, guarded and renewing.

---

## PHASE A — PREP AT IONOS (from 6 Oct, ~15 min)
1. Log in → **Domain management → zeusaiintelligence.com**
2. **Domain Guard / lock: OFF** (deactivation already requested 23–24 Aug — confirm it actually landed; a locked domain cannot transfer)
3. **Unlock domain transfer** (DomainLock → Transfer lock OFF)
4. **Request the auth code (EPP code)** — button under the domain's settings; IONOS emails it to the registrant address. **Keep it secret** — anyone with it + account access could move the domain.
5. Confirm registrant email address is correct (transfer confirmation goes there).

## PHASE B — AT CLOUDFLARE (~10 min)
1. Log in to your Cloudflare account (the one hosting zeusaiintelligence.com DNS — NS: dora/james.ns.cloudflare.com)
2. **Registrar → Register Domains tab → Transfer** or **Domain Registration → Transfer**
3. Enter `zeusaiintelligence.com` → paste the EPP code
4. Confirm the current DNS (Cloudflare nameservers stay as-is — **no DNS change at all**, the site doesn't blink)
5. Pay the transfer fee (≈ registry price, ~£10–11/1yr; Cloudflare sells at cost, no markup) — this adds 1 year to the current expiry (2027-08-07 → **2028-08-07**)

## PHASE C — COMPLETE (~5–7 days)
1. IONOS sends "transfer requested" email — **ignore it** (do NOT click "reject")
2. Cloudflare/registry sends a confirmation email to the registrant — **click to approve within the window**
3. Transfer completes: WHOIS registrar flips to Cloudflare; verify:
   ```bash
   curl -s https://dns.google/resolve?name=zeusaiintelligence.com&type=NS   # still Cloudflare
   curl -s -o /dev/null -w '%{http_code}' https://zeusaiintelligence.com     # 200, headers 5/5
   ```
4. Enable **Auto-renew ON** at Cloudflare; optionally enable **Dual-factor / Cloudflare lock**

## PHASE D — FINAL CUT WITH IONOS
1. After the transfer completes, the domain disappears from the IONOS portal
2. Finish the cancel/dispute/close steps in `IONOS-DELETE-ALL-GUIDE.md` Steps 2–6
3. Confirm no residual IONOS contracts + no Tide direct debit

## WHY CLOUDFLARE REGISTRAR (not just "another registrar")
- DNS is already Cloudflare → one pane of glass, no NS swap
- At-cost pricing (no IONOS-style markup), free WHOIS privacy
- Same login as your existing zone — fewer credentials in the estate

## RISK TABLE
| Risk | Mitigation |
|---|---|
| Transfer refused before 6 Oct | wait — eligibility date is registry-set |
| EPP code leaked | treat as secret; code is single-use, rotates after transfer |
| Confirm email missed → transfer fails | check registrant inbox daily for 7 days; extend by re-request |
| DNSSEC makes transfer fail | verify no DNSSEC at Cloudflare zone (we don't use it) or transfer with keys exported |
| Site outage during transfer | impossible — DNS unchanged, only registrar changes |

## TRACKER
- [ ] 2026-10-06: unlock + EPP code at IONOS
- [ ] Transfer initiated at Cloudflare Registrar
- [ ] Approve confirmation email
- [ ] WHOIS shows Cloudflare + site 200/headers 5/5
- [ ] IONOS account closed (delete-all Steps 2–6)

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).