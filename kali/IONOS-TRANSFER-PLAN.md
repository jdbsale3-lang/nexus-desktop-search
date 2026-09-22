# FLAGSHIP DOMAIN TRANSFER — zeusaiintelligence.com → Cloudflare Registrar
**Status (updated 21 Sep, from live registry + your screenshots):**
- ✅ Auth code **received from IONOS** (EPP format verified, 20 chars) — keep it secret, use once
- ✅ Domain Guard on flagship: **Not active** (confirmed in your domain list)
- ❌ Registry status: **`client transfer prohibited`** — IONOS-side lock still ON — must be switched off in portal
- ⛔ **ICANN 60-day lock: transfer CANNOT complete before 2026-10-06** (registered 07 Aug 2026). Any attempt before then is rejected by the .com registry.

---

## WHAT YOU CAN DO RIGHT NOW (entry at Cloudflare)
The transfer is requested at the **gaining** registrar (Cloudflare) — that needs YOUR Cloudflare login, so it's your screen:
1. Cloudflare dashboard → **Registrar** (left menu) → **Register Domains** tab → **Transfer**
2. Enter `zeusaiintelligence.com`
3. Paste the auth code (your 20-char EPP code) into the **Auth code** field
4. Tick the standard confirmations → **Transfer** → pay (~£10–11, adds a year → expires 2028-08-07)
5. **IMPORTANT:** request now = registry holds it until the 60-day lock lifts (6 Oct), then completes automatically over ~5–7 days. OR wait until 6 Oct and request — same result. Recommended: **request the transfer NOW so it queues**, then confirm the registry/Cloudflare approval emails.

## THE TWO LOCKS — clear them in this order
| Lock | Where | How to clear |
|---|---|---|
| 1. **Client transfer prohibited** (IONOS) | Domains & SSL → zeusaiintelligence.com → **Renewal & Transfer** (same page you got the code) | switch **transfer lock OFF** / disable Domain Guard (already off) + confirm on the deactivation email |
| 2. **ICANN 60-day** (.com registry) | outside portal — automatic | clears **06 Oct 2026**; nothing to do but wait |

## AFTER THE REQUEST
- IONOS emails "transfer requested" → **ignore** (do NOT click reject)
- Cloudflare/registry emails approval link → **click it within the window**
- ~5–7 days after 6 Oct: WHOIS registrar flips to Cloudflare → verify:
```bash
curl -s https://dns.google/resolve?name=zeusaiintelligence.com&type=NS   # still Cloudflare
curl -s -o /dev/null -w '%{http_code}' https://zeusaiintelligence.com     # 200 + headers 5/5
```

## MISC FACTS FROM YOUR SCREENSHOTS (logged)
- Your domain list shows **11 domains**: flagship (Cloudflare NS, Guard inactive) + `zeusaiintelligence.org` (DNS→178.62.46.133 — ANOTHER droplet, not 188.166.175.149) + `.info/.co.uk/.store` (Guard "Waiting") + `zeusai.store` + the 4 typos (`zeusaintellegence.*`, expiring 29/08/2027, Guard "Order" — NOT active, good).
- The **Instant Domain** contract in your cancel flow is **112790544** (not 113514895 from the email) — the portal number is authoritative; use it in the dispute.

## TRACKER
- [x] Auth code received
- [x] Domain Guard flagship OFF
- [ ] Transfer lock cleared at IONOS (Renewal & Transfer page)
- [ ] Transfer requested at Cloudflare Registrar (queues until 6 Oct)
- [ ] Approval email clicked
- [ ] WHOIS → Cloudflare; site 200/headers 5/5
- [ ] IONOS account fully closed (after transfer + dispute)

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).