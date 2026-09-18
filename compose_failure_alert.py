#!/usr/bin/env python3
"""compose_failure_alert.py — build the GitHub issue body for a route-monitor
workflow FAILURE (job crashed, infra error, action failure — not just a route
down). Reads the env the runner provides and writes issue_body.md.
Kept OUT of the workflow YAML (block-scalar discipline)."""
import os
import pathlib
import time


def main():
    run_id = os.environ.get("GITHUB_RUN_ID", "?")
    run_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "zeusai")
    sha = os.environ.get("GITHUB_SHA", "?")[:8]
    job = os.environ.get("GITHUB_JOB", "monitor")
    body = (
        "Automated from the Estate Route Monitor workflow.\n\n"
        "**The workflow run itself FAILED** (not just a route DOWN).\n\n"
        f"- Run: [{run_id}]({run_url}/{repo}/actions/runs/{run_id})\n"
        f"- Commit: `{sha}` · job: `{job}`\n"
        f"- Time: {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}\n\n"
        "Check the run's job logs for the failing step:\n"
        "- `theme smoke test` — flagship theme system regressed?\n"
        "- `run monitor` — script crash or network block?\n"
        "- `report status` / `alert` — composer script failure?\n\n"
        "A failed run means the estate may be unmonitored — resolve within the "
        "next 30-minute cycle or open a manual incident (incident_create skill)."
    )
    pathlib.Path("issue_body.md").write_text(body)
    print(f"failure alert body written (run {run_id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())