#!/usr/bin/env python3
"""compose_route_alert.py — build the GitHub issue body for a route-monitor
critical failure. Reads monitor.json, writes issue_body.md. Kept OUT of the
workflow YAML to avoid block-scalar column-1 parsing defects (same class as
write_step_summary.py)."""
import json
import pathlib


def main():
    try:
        with open("monitor.json") as f:
            d = json.load(f)
    except Exception as e:
        pathlib.Path("issue_body.md").write_text(
            f"Route-monitor alert could not read monitor.json: {e}")
        return 1
    down = [r for r in d.get("routes", []) if not r.get("ok") and r.get("critical")]
    names = ", ".join(r["route"] for r in down)
    lines = "\n".join(
        f"- {r['route']}: HTTP {r.get('status')} ({r.get('ms', '?')}ms) {r.get('error', '')}"
        for r in down)
    body = (
        "Automated from the Estate Route Monitor workflow.\n\n"
        "**Critical routes DOWN:** " + names + "\n\n"
        "**Evidence:**\n```\n" + lines + "\n```\n\n"
        "See INCIDENTS-INDEX.md — a route down >30 min without an index entry is itself an incident."
    )
    pathlib.Path("issue_body.md").write_text(body)
    print(names)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())