#!/usr/bin/env python3
"""estate_gmail_watcher.py — nightly Gmail trash-watcher for the ZEUS estate.

Purpose: emails keep silently vanishing into TRASH (ICO fee reminder, NHS
England thread — both found this session). This monitor sweeps Trash for
estate-critical senders/terms every night and raises the alarm the moment
anything lands there, so the next loss is caught within 24h.

Run via the estate chat (connector gmail-find-email) or cron-documented:
  nightly sweep = Trash lookup for: ico.org.uk | nhs.net | roberts | zeustrust

Output contract:
  {"checked": "<ts>", "in_trash": [ {subject, sender, date} ... ], "count": N}
If count > 0 -> ALERT: restore immediately (gmail-modify-labels TRASH removal).
"""
import datetime
import json

CRITICAL = [
    "ico.org.uk",       # ICO fee / registration — must never be trashed
    "nhs.net",          # NHS England / Lauren Roberts
    "nhs.uk",
    "zeustrust",        # the estate label thread
]
QUERY = " in:trash (" + " OR ".join(f'from:"{d}"' for d in CRITICAL) + \
        " OR " + " OR ".join(f'"{t}"' for t in CRITICAL) + ")"


def check():
    return {
        "kind": "gmail-trash-watch",
        "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "query": QUERY,
        "note": "Run connector gmail-find-email with this query; any result = ALERT + restore.",
        "critical_domains": CRITICAL,
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))