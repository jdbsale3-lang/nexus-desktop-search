# ORPHAN DOMAIN CANCELLATION PLAN — zeusaiintelligence.* variants at IONOS
**Date:** 22 Sep 2026 · **Goal:** every non-essential domain either cancelled or transferred — zero orphan spend.

## THE FULL INVENTORY (verified against registries + your IONOS portal screenshots)

| Domain | Registry status | Expiry | Verdict | Action |
|---|---|---|---|---|
| `zeusaiintelligence.com` | REGISTERED (IONOS, transfer-locked) | 2027-08-07 | **KEEP** — flagship | Transfer to Cloudflare (in progress) |
| `zeusaiintelligence.org` | REGISTERED | 2027-08-07 | **CANCEL** — dead box | The IP it points at (178.62.46.133) has NOTHING listening on 80/443 — verified 22 Sep. No site, no mail, no purpose. |
| `zeusaiintelligence.info` | REGISTERED | 2027-08-07 | **CANCEL** — no content | "Domain not in use" per portal; no DNS records follow it |
| `zeusaiintelligence.co.uk` | probe inconclusive (Nominet RDAP blocked) — confirm in portal | 2027-08-07 | **DECIDE** — cheap UK brand defense | Keep only if you want a UK TLD mirror; otherwise cancel |
| `zeusaiintelligence.store` | 404 on registry probe — confirm in portal list | 2027-08-07 | **CANCEL** | Not used; typos on this TLD already dead |
| `zeusai.store` | 404 on probe — confirm in portal | 2027-08-07 | **CANCEL** | Shorter variant, no use case |
| 4× `zeusaintellegence.*` (typos) | **GONE — verified 404/NXDOMAIN** | — | ✅ DONE | Already deleted by your cancellations |

## HOW TO CANCEL (IONOS portal — per domain, ~30 seconds each)
1. `my.ionos.co.uk` → **Domains & SSL** → click the domain
2. Open **Renewal & transfer** tab → look for **"Do not renew" / cancel** option
3. Confirm the dialog → the domain is set not to renew → it drops at expiry (2027-08-07) with **£0 charged**
4. If the portal offers **early cancellation** ("cancel domain now") — choose it where available
5. Verify after each: the domain list row shows the cancel notice

## THE DECISION RULE
- **Keep:** the flagship `.com` (transferring) and optionally `.co.uk` (UK brand defense, ~£3–8/yr).
- **Cancel (do-not-renew):** `.org`, `.info`, `.store`, `zeusai.store` — they carry no traffic, no mail, no content. Each kept = money to a company you're leaving + unused assets.
- **Never renew:** any typo domain (all already gone).

## AFTER CANCELLATION — 3-CHECK PROOF
```bash
# on the droplet — expect NXDOMAIN / no records for each cancelled domain
for d in zeusaiintelligence.org zeusaiintelligence.info zeusaiintelligence.store zeusai.store; do
  echo "$d → $(curl -s --max-time 8 https://dns.google/resolve?name=$d&type=NS | python3 -c "import json,sys; d=json.load(sys.stdin); print('HAS NS' if (d.get('Answer') or d.get('Authority')) else 'no records')")"
done
```
- [ ] All four cancelled at IONOS (do-not-renew set)
- [ ] Registry/DNS shows no delegated records for the cancelled set
- [ ] No renewal lines on any future IONOS invoice

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).