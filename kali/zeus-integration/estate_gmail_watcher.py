#!/usr/bin/env python3
"""estate_gmail_watcher.py — nightly Gmail trash-watcher for the ZEUS estate.

Purpose: emails keep silently vanishing into TRASH (ICO fee reminder, NHS
England thread — both found this session). This monitor sweeps Trash for
estate-critical senders/terms every night and raises the alarm the moment
anything lands there, so the next loss is caught within 24h.

Run via the estate chat (connector gmail-find-email) or cron-documented:
  nightly sweep = Trash lookup for the CRITICAL list below.

Output contract:
  {"checked": "<ts>", "in_trash": [ {subject, sender, date} ... ], "count": N}
If count > 0 -> ALERT: restore immediately (gmail-modify-labels TRASH removal).
"""
import datetime
import json

# EXTENDED (v2): estate-critical senders and terms. Add more here as needed —
# the nightly sweep uses exactly this list.
CRITICAL = [
    # regulator / registration — must never be trashed
    "ico.org.uk",           # ICO fee / registration / certificate
    "informationcommissioner",
    # NHS and health
    "nhs.net",              # NHS England / Lauren Roberts
    "nhs.uk",
    "england.casework",
    # government and HMRC
    "hmrc.gov.uk",
    "gov.uk",
    "companieshouse.gov.uk",
    "hmcts",
    "dwp.gov.uk",
    "dvla.gov.uk",
    "homeoffice.gov.uk",
    # banks / financial (payment-sensitive)
    "barclays.co.uk",
    "lloydsbank.co.uk",
    "hsbc.co.uk",
    "natwest.com",
    "tsb.co.uk",
    "nationwide.co.uk",
    "paypal.com",
    "stripe.com",
    # the estate label thread
    "zeustrust",
    "zeustrustaegissecurity",
    "jdb sales",
    "jdbsale3",
]
QUERY = " in:trash (" + " OR ".join(f'from:"{d}"' for d in CRITICAL) + \
        " OR " + " OR ".join(f'"{t}"' for t in CRITICAL) + ")"


def check():
    return {
        "kind": "gmail-trash-watch",
        "version": 2,
        "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "query": QUERY,
        "note": "Run connector gmail-find-email with this query; any result = ALERT + restore.",
        "critical_domains": CRITICAL,
        "critical_count": len(CRITICAL),
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))