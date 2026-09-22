# DOMAIN TRANSFER CHECKLIST — zeusaiintelligence.com → Cloudflare Registrar
**Owner action list — every box must be ticked before the transfer is considered done.**
Version 1.0 · updated 22 Sep 2026

## PHASE 0 — IONOS PREP
- [x] Auth code requested (IONOS → Renewal & transfer → Request authorisation code) — code captured
- [ ] **Domain transfer lock DISABLED** (Renewal & transfer → "Domain transfer lock: enabled" → disable)
      - verify: `curl -s https://rdap.verisign.com/com/v1/domain/zeusaiintelligence.com | grep -o '"status": \[[^]]*\]'` → `[]`
- [ ] Confirm no DNSSEC on the zone (none in use — verified earlier)
- [ ] Registrant contact details correct (same email that receives the approval link)

## PHASE 1 — CLOUDFLARE INITIATION
- [ ] Payment method on file in Cloudflare (Account → Billing)
- [ ] Sidebar **Domains → Registrations (+ Transfers)** open
- [ ] **Transfer a domain** → type `zeusaiintelligence.com` → enter **auth code**
- [ ] Confirm price (~£10–11 incl. +1 year → expiry 2028-08-07)
- [ ] **Transfer** → pay → enter contact details → **Confirm transfer**

## PHASE 2 — APPROVALS
- [ ] IONOS email approval link clicked (do NOT click reject)
- [ ] Cloudflare FOA email approved

## PHASE 3 — VERIFY + CLOSE
- [ ] Registry check: registrar → **CLOUDFLARE, INC.**
      `curl -s https://rdap.verisign.com/com/v1/domain/zeusaiintelligence.com | grep '"fn"'`
- [ ] Site live: `https://zeusaiintelligence.com` → 200, headers 5/5
- [ ] Cloudflare **Registrations** lists the domain (Active)
- [ ] IONOS account closure finalised (delete-all guide Steps 6–7)
- [ ] Tide recurring check: no IONOS direct debit

## AUTOMATED WATCH (no manual polling needed)
- [x] `.github/workflows/transfer-tracking.yml` — Verisign RDAP probe every 6h
- [ ] When GitHub issue "TRANSFER COMPLETE" opens → run Phase 3 items same day

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).