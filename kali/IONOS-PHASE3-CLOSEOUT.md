# PHASE-3 CLOSEOUT — IONOS fully gone, estate verified
**When:** triggered by the `[TRANSFER] COMPLETE` GitHub issue (Domain Transfer Watch, every 6h) or the registry flip.
**Goal:** prove the domain is at Cloudflare, the site is healthy, IONOS is fully closed, no money leaks.

## A. REGISTRY PROOF (droplet)
```bash
curl -s https://rdap.verisign.com/com/v1/domain/zeusaiintelligence.com | python3 -c "
import json,sys; j=json.load(sys.stdin)
for e in j.get('entities',[]):
    if 'registrar' in e.get('roles',[]):
        for i in e.get('vcardArray',[[]])[1]:
            if i[0]=='fn': print('registrar:', i[3])
print('status:', j.get('status'))"
```
- [ ] Output shows registrar = **CLOUDFLARE, INC.** and no `client transfer prohibited`

## B. SITE HEALTH (droplet)
```bash
curl -s -o /dev/null -w '%{http_code}\n' https://zeusaiintelligence.com          # 200
curl -sI https://zeusaiintelligence.com | grep -icE "strict-transport|content-security|x-content-type|referrer-policy|permissions-policy"   # ≥3 (5 = full)
curl -s https://zeusaiintelligence.com/reach/self | python3 -c "import json,sys; d=json.load(sys.stdin); print('skills', d.get('skills_loaded'), '/', d.get('skills_broken'), 'broken')"
curl -s https://zeusaiintelligence.com/reach/monitor | grep -o '"alerts": \[[^]]*\]'
```
- [ ] Flagship 200 · NEXUS 200 · headers ≥3/5 · skills 25/0 · alerts []

## C. CLOUDFLARE REGISTRAR VIEW (browser)
- [ ] dash.cloudflare.com → **Domains → Registrations** → `zeusaiintelligence.com` listed **Active**
- [ ] Auto-renew ON · expiry 2028-08-07 · WHOIS privacy shown (Cloudflare default)
- [ ] Billing: no surprise charges (transfer fee settled)

## D. IONOS — FINAL CUT
- [ ] `IONOS-CLOSURE-EMAIL.md` sent (account closure + GDPR erasure + final zero-balance statement)
- [ ] No IONOS products remain in the portal (all lists empty)
- [ ] No further IONOS mail arrives (watcher v3.2 has ionos anchors — it will alert if any does)

## E. MONEY LEAK CHECK
- [ ] Tide → Payments → Recurring: **no IONOS entry** (Direct Debit gone)
- [ ] Card statements: no IONOS charge since the failed 18/09 run
- [ ] Dispute reply received: itemised breakdown, waiver/refund for typo cluster + VPS, settlement (if any) paid and receipted
- [ ] rankingCoach / IONOS marketing mail ceased (unsubscribe + GDPR)

## F. DOCS UPDATED
- [ ] `IONOS-AUDIT.md` marked CLOSED with transfer date + closure date
- [ ] `DROPLET-RUNBOOK.md` notes the registrar is now Cloudflare (no IONOS dependency)
- [ ] Incident ledger: INC-0xx "IONOS exit" — CLOSED
- [ ] Kit: IONOS section consolidated into one archive folder

## G. THE WATCHDOG STAYS
- [ ] Domain Transfer Watch keeps running (6-hourly) — if anything weird happens at the registry it raises an issue
- [ ] CI Health Check keeps the 6-hour estate probe
- [ ] Estate email watcher keeps the IONOS anchors — any resurrection is caught

---
**CLOSEOUT CONDITION:** all boxes in A–F ticked. When they are: paste "PHASE 3 DONE" and I'll record the estate-level close.

All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).