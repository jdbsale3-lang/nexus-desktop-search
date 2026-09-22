# IONOS — PRESS-BY-PRESS CLICK GUIDE (customer 316502159)
Every step below uses the exact button names from IONOS's own help pages (checked 2026-09-21).
Open `https://login.ionos.co.uk` yourself — never click links in IONOS emails.

> RULE OF THUMB: the two top menu words you will live in are **"My account"** (top-right, money)
> and **"Domains & SSL"** (left menu, domains). Everything else hangs off those.

---

## PART 0 — LOG IN (once)
1. Browser → `https://login.ionos.co.uk`
2. Type your email/customer number + password → **Log in**
3. If asked: enter the 6-digit **login code** (arrives by email — you've had one: 680858)
4. You land on the dashboard. NOTE the top menu bar and the left menu — don't close this tab.

---

## PART 1 — THE PHONE CALL (DO THIS FIRST — deadline lapsed 6 Sep)
The VPS (contract 113400130) needs a phone-confirm that the email warned about.
1. Dial **0808 189 0625** (IONOS UK, 24/7)
2. Say: **"I confirm cancellation of contract 113400130 — IONOS VPS Windows XL+ — customer 316502159."**
3. Ask the agent to: (a) confirm cancellation in writing by email, (b) prorate/refund since 23 Aug, (c) confirm no further billing.
4. Write down the agent's name + reference number.

---

## PART 2 — DOWNLOAD THE £485.40 INVOICE (before cancelling anything)
1. In the **title bar** (top of page) click **Menu** → **My account**
2. Click the **Invoices & Payment Details** tile → the list of invoices opens
3. Find the latest invoice (≈ £485.40, ~21 Sep) → click it → **Download as PDF** (or use the **Print** button at the bottom to save as PDF)
4. Save it as `IONOS-INVOICE-2026.pdf` — you'll attach it to the dispute
5. Also on this page: note your **Account Number (316502159)** — support will ask for it

---

## PART 3 — SWITCH OFF DOMAIN GUARD (all domains — required before cancellation & transfer)
> Your 23–24 Aug emails were only *requests* — do the real deactivation now.
1. Left menu → **Domains & SSL**
2. In the **Domain Guard column**, find the **green shield** next to each domain
3. Click the **green shield** → dialog opens showing the verification email address
4. Click **Request confirmation email**
5. Open that email → click **Deactivate Domain Guard Now**
6. On the page that opens → click **Disable Domain Guard**
7. Repeat for: `zeusaiintelligence.com` (flagship), `.org`, `.info`, `.co.uk`, `.store`, `zeus-scan-fit.com`, and the 4 typo domains
> Keep the flagship's guard OFF **only while working** — re-enable it if you DON'T transfer by 6 Oct (its Domain Guard blocks hijack).

---

## PART 4 — CANCEL EACH CONTRACT (the big loop — do this for every service)
For **each** contract (VPS if phone failed, GPT, Mail Business, Virusscan, AI Assistant, Instant Domain, Domain Guards):
1. Top **Menu** → **My account**
2. Click tile **Contracts & subscriptions** → the Contracts page opens
3. In the **Service column**, **click the contract's name** → details page opens
4. In the **Details tab**, click **Cancel contract**
5. In the **Cancel this entire contract** tile, click **Select**
6. Pick the **reason** for cancellation → **Next**
7. If asked: choose cancellation date/type → **Next** / **Continue cancellation**
8. On "Important information..." — tick **"I am aware of the effects of my cancellation and confirm that I have backed up all data. Deletion can be performed."**
9. Click **Make a note of cancellation now**
10. ✅ A confirmation with the cancellation date appears + confirmation email arrives — file that email

Products to run through this loop:
| Product | Contract | Note |
|---|---|---|
| IONOS GPT | 113271957 | ends 06.09.2026 — stop renewal |
| Mail Business 5 Lic. | order 29 Aug | |
| Virusscan | order 29 Aug | |
| AI Email Assistant 1u | order 29 Aug | |
| Instant Domain | 113514895 | check which domain |
| VPS XL+ | 113400130 | phone FIRST (Part 1) |

---

## PART 5 — CANCEL THE 4 TYPO DOMAINS
Same loop as Part 4 but in the domain list:
1. Left menu → **Domains & SSL**
2. Click `zeusaiintellegence.com` (double-L one) → **Renewal & Transfer** (or the domain's own cancel path)
3. Choose **do not renew / cancel** → confirm
4. Repeat: `zeusaiintellegence.info`, `.co.uk`, `.store`
> DO NOT renew these. Keep your 29 Aug "spelling correction" email — dispute evidence.

---

## PART 6 — TRANSFER THE FLAGSHIP → CLOUDFLARE (do from 6 Oct — 60-day ICANN lock until then)
1. Left menu → **Domains & SSL** → click `zeusaiintelligence.com`
2. Open **Renewal & Transfer** page
3. Click **Show Authorisation Code** (may take minutes to appear; it's the EPP code — keep it secret)
4. If locked: on the same page disable any **transfer lock** (Domain Guard must be OFF first — Part 3)
5. Go to Cloudflare → **Registrar → Transfer** → paste domain + auth code → pay (~£10–11) → **approve the confirmation email** within the window
6. Verify after ~5–7 days: WHOIS registrar = Cloudflare; site still 200 + headers 5/5

---

## PART 7 — CLOSE THE ACCOUNT (after transfer, after dispute resolved)
1. **Do NOT cancel the account before the transfer** — IONOS's own help: *"If no other contracts exist under your customer number, you will no longer have access to your IONOS account"* — that would block the transfer.
2. Once flagship is at Cloudflare + balance settled/waived:
   - Top **Menu** → **My account** → look for **Close account / Delete customer data** (GDPR)
   - If no button: email `datenschutz@ionos.co.uk` → request account closure + data erasure (Art. 17 UK GDPR)
3. Tide app → **Payments → Recurring** → confirm no IONOS direct debit remains

---

## QUICK REFERENCE
| Task | Where | Button |
|---|---|---|
| Invoices | Menu → My account → Invoices & Payment Details | Download as PDF |
| Contracts | Menu → My account → Contracts & subscriptions | Cancel contract |
| Domain Guard | Domains & SSL → green shield | Disable Domain Guard |
| Auth code | Domains & SSL → Renewal & Transfer | Show Authorisation Code |
| VPS confirm | PHONE 0808 189 0625 | — |
| Close account | My account → Close / GDPR email | — |

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).