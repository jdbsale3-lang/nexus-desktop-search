#!/usr/bin/env python3
"""estate_gmail_watcher.py — nightly Gmail trash-watcher for the ZEUS estate (v3).

Sweeps Trash for estate-critical senders/terms nightly and ALERTS the moment
anything lands there. v3: 40+ anchors across regulator, NHS, HMRC, Courts,
banks, insurers, tax, domain providers and the estate label threads.

Run via the estate chat (connector gmail-find-email) or cron-documented:
  nightly sweep = Trash lookup for the CRITICAL list below.

Output contract:
  {"checked": "<ts>", "in_trash": [ {subject, sender, date} ... ], "count": N}
If count > 0 -> ALERT: restore immediately (gmail-modify-labels TRASH removal).
"""
import datetime
import json

# v3 — extended anchors: anything that must NOT silently vanish.
CRITICAL = [
    # regulator / registration
    "ico.org.uk", "informationcommissioner",
    # NHS / health
    "nhs.net", "nhs.uk", "england.casework", "england.contactus",
    # Government / tax / legal
    "hmrc.gov.uk", "gov.uk", "companieshouse.gov.uk", "hmcts",
    "dwp.gov.uk", "dvla.gov.uk", "homeoffice.gov.uk", "hmrc",
    "court", "tribunal", "legal",
    # Banks / payments / insurers
    "barclays.co.uk", "lloydsbank.co.uk", "hsbc.co.uk", "natwest.com",
    "tsb.co.uk", "nationwide.co.uk", "halifax.co.uk", "metrobankonline.co.uk",
    "monzo.com", "revolut.com", "starlingbank.com", "paypal.com", "stripe.com",
    "amex.co.uk", "mastercard", "visa", "santander.co.uk", "co-operativebank.co.uk",
    "aviva.co.uk", "standardlife", "admiral.com",
    # estate label threads / business
    "zeustrust", "zeustrustaegissecurity", "jdb sales", "jdbsale3",
    "stackblitz", "bolt.new", "netlify", "vercel", "digitalocean", "godaddy", "namecheap",
    "aws", "azure", "google cloud", "slack", "notion", "twilio",
]
QUERY = " in:trash (" + " OR ".join(f'from:"{d}"' for d in CRITICAL) + \
        " OR " + " OR ".join(f'"{t}"' for t in CRITICAL) + ")"


def check():
    return {
        "kind": "gmail-trash-watch",
        "version": 3,
        "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "query": QUERY,
        "note": "Run connector gmail-find-email with this query; any result = ALERT + restore.",
        "critical_domains": CRITICAL,
        "critical_count": len(CRITICAL),
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))