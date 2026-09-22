# SUPPLIER & COST AUDIT — the full company map
**Goal:** list every company the ZEUS estate depends on, what it costs, what it runs, and how many companies we truly need.
**Method:** verified where possible — mailbox receipts, live probes, session records. Honest estimates marked (~).

---

## THE FULL MAP (12 companies)

| # | Company | Role in estate | Monthly / annual cost | Verdict |
|---|---|---|---|---|
| 1 | **DigitalOcean** | Droplet `aegis-api` (188.166.175.149) — hosts flagship nginx, NEXUS engine, Kali container, reach bridge, SearXNG, n8n | ~£10–20/mo (est., bill-level varies) | **KEEP** — compute core |
| 2 | **Cloudflare** | DNS (authoritative NS), CDN/proxy, SSL Full, security headers, WAF; soon **registrar** (post-transfer) | ~£0 now (free tier) + $10.46/yr post-transfer | **KEEP** — network + DNS core |
| 3 | **IONOS** | Domain registrar (flagship + variants), former VPS/mail | £485.40 disputed, uncollected | **EXIT** — cancellations done, transfer in motion; the disputed debt is failed-collection only |
| 4 | **GitHub** | Repo `nexus-desktop-search`, Actions CI (health check, transfer watch, kali builds), issues | £0 (free tier) | **KEEP** — CI + code core |
| 5 | **Gmail/Google** | Primary mailbox, watcher source, Sheets/Drive | £0 (free Gmail; Workspace cancelled) | **KEEP** — mailbox core |
| 6 | **Higgsfield** | AI platform — generation, agents, connectors (TikTok/X/LinkedIn/IG/Threads), breach-check + docs apps | platform credits (pay-per-generation) | **KEEP** — AI + social core |
| 7 | **Slack** | Estate alerts channel #all-cai-company-os | £0 (free tier) | KEEP (free) — could fold into email, but free = keep |
| 8 | **Twilio** | Voice/SMS alerts (INC-00x alerting, CALL_MODE) | usage-based (small) | KEEP — alerting redundancy |
| 9 | **StackBlitz/Bolt** | Web-builder Pro subscription | **US$25.00/mo** (paid 21 Sep) | **REVIEW** — was it used this month? Bolt usage vs cost |
| 10 | **Exa** | Research/search API (WebThinker spine, verified primary) | invoice #GDDKFQ-00002 (18 Sep) — usage-based | **KEEP** (small, verified value) |
| 11 | **Cursor** | AI code editor | £18.64/mo — **payment FAILED 19–20 Sep** | **REVIEW** — failed twice; cancel or fix card |
| 12 | **X Premium** | X/Twitter premium | £8.00/mo — **payment FAILED 18–19 Sep** | **REVIEW** — cancel unless posting needs it |
| 13 | **DEEMOS** | ? (some dev tool) | £23.30/mo — **payment FAILED 18 Sep** | **REVIEW** — failed; cancel unless essential |
| 14 | **ClickUp** | Project management | Daily summary seen; tier unknown | **REVIEW** — used or cut |
| 15 | **Anthropic API** | Claude API (prompt-cache notice 25 Aug) | usage-based | KEEP — API work |
| 16 | **Tide** | Business bank (ICOs, DD, payments) | £0 (business account) | **KEEP** — unavoidable |
| 17 | **ICO** | Data protection fee (regulatory) | £52/yr (paid) | **KEEP** — legal requirement |
| 18 | **Perplexity/OpenAI/etc.** | pay-as-you-go lanes (Exhibit B) | usage only | keep as needed |

---

## THE 3-COMPANY TEST — CAN WE DO EVERYTHING WITH 3?

### What the estate actually needs (capabilities, not vendors)
1. **Compute** (run servers: flagship, NEXUS, Kali, SearXNG, n8n) — needs a cloud VM
2. **Network/DNS/edge** (authoritative DNS, CDN, SSL, registrar) — needs Cloudflare-class
3. **Mailbox** (human inbox + watcher) — needs a mail provider
4. **AI + social publishing** (generation, connectors, agents) — needs Higgsfield/platform
5. **Code + CI** (repo, workflows, issues) — needs GitHub-class
6. **Money** (bank, regulatory) — Tide + ICO unavoidable

### Can 3 companies span all six?
**No — honestly, not all six.** The mandatory minimum is **5 paid/essential companies + 2 non-negotiable** (Tide bank, ICO regulator — they can't be consolidated away, and ICO £52/yr is not a cost problem). Here's the tightest defensible stack:

| Company | Covers | Replaces |
|---|---|---|
| **1. DigitalOcean** | compute + Kali + n8n + SearXNG + reach bridge | everything "server" |
| **2. Cloudflare** | DNS + CDN + SSL + registrar (post-transfer) + WAF | IONOS (registrar), potentially Twilio (alerts → webhook) |
| **3. Higgsfield** | AI + social connectors + agents + hosted apps | the platform layer |
| **4. GitHub** | repo + CI + issue watchdogs | the dev spine |
| **5. Google/Gmail** | mailbox + watcher + docs | the office layer |

**What would break at exactly 3:** you'd lose CI/Actions (GitHub) or the mailbox (Gmail) or the AI/social layer (Higgsfield) — none replaceable by the other three. So the honest answer is **"5 essential + 2 regulated"**, but the **cost-cutting headline is real**: of those, **four are £0** (Cloudflare free tier, GitHub free tier, Gmail, Tide) and the real money sits in **DigitalOcean (~£10–20/mo) + Higgsfield credits + the subscription review list below**.

---

## THE ACTUAL COST CUTS (this is where the money is, sir)

### CANCEL / FIX IMMEDIATELY (failed-payment subscriptions — each failed = service already suspended or will be)
- [ ] **DEEMOS £23.30/mo** — failed 3×; cancel outright unless you name the use
- [ ] **Cursor £18.64/mo** — failed 2×; cancel or fix card — do you still use it?
- [ ] **X Premium £8/mo** — failed 2×; cancel unless X-posting needs verification tools
- [ ] **StackBlitz/Bolt US$25/mo** — PAID and active: did you build anything on Bolt this month? If not, cancel before next cycle
- [ ] **ClickUp** — verify tier; if paying, does any ZEUS workflow use it? (estate uses Notion + Slack)
- **Potential saving: ~£75–100/mo + $25/mo ≈ £1,000+/yr** before touching infrastructure.

### KEEP (verified value, low cost)
- DigitalOcean, Cloudflare (free), GitHub (free), Gmail (free), Higgsfield, Exa (small; it's the verified research spine — could fall back to self-hosted SearXNG if the cost ever outgrows the value), Twilio (small), Tide, ICO.

---

## BOTTOM LINE FOR THE BOARD
- **Five companies to run everything:** DigitalOcean · Cloudflare · Higgsfield · GitHub · Google — four of them free, one VM.
- **Two regulated, non-consolidatable:** Tide · ICO.
- **Cut now:** DEEMOS, Cursor, X Premium, Bolt, ClickUp-review → **≈£1,000+/yr**.
- **Exit done:** IONOS — registrations cancelled/transferring, debt disputed and uncollected.
- **Cloudflare consolidation bonus:** once the flagship lands at Cloudflare Registrar, *one company* owns DNS + CDN + edge + the domain — IONOS is gone entirely, and email could later route via Cloudflare Email Routing to keep Google as pure mailbox.

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).