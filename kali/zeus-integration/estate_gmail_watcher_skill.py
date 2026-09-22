# ZEUS-SKILL: estate_gmail_watcher.py
# Scheduled trash/critical-sender watcher — any anchored mail that lands in
# trash (or a critical sender anywhere) is surfaced for restore + alert.
import json
import subprocess

SKILL = {
    "name": "estate_gmail_watcher",
    "description": "Watch Gmail trash for critical anchors (regulators, NHS, IONOS, Higgsfield…) and alert",
    "category": "core",
    "inputs": {"mode": "str"},
    "entry": "run_skill",
}

CRITICAL = [
    "ico.org.uk", "informationcommissioner",
    "nhs.net", "nhs.uk", "england.casework", "england.contactus",
    "hmrc.gov.uk", "gov.uk", "companieshouse.gov.uk", "hmcts",
    "ionos", "1&1", "1and1", "ionos.co.uk", "ionos.com",
    "higgsfield.ai", "higgsfield support", "remedy",
    "zeustrust", "zeustrustaegissecurity", "jdb sales", "jdbsale3",
    "stripe.com", "twilio", "digitalocean", "cloudflare",
]

QUERY = ("in:trash (" + " OR ".join(f'from:"{d}"' for d in CRITICAL) + " OR "
         + " OR ".join(f'"{t}"' for t in CRITICAL) + ")")


def run_skill(ctx):
    """mode='config' -> return the watch spec; any other -> report status."""
    mode = (ctx or {}).get("mode", "status")
    if mode == "config":
        return {"ok": True, "anchors": len(CRITICAL), "gmail_query": QUERY,
                "note": "run this query with the Gmail connector; any hit = restore + alert"}
    # status: check the nightly cron wiring
    try:
        cron = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=15).stdout
    except Exception:
        cron = ""
    wired = "estate_gmail_watcher" in cron or "gmail" in cron.lower()
    return {"ok": True, "anchors": len(CRITICAL), "nightly_cron_wired": wired,
            "gmail_query": QUERY[:200] + "…"}