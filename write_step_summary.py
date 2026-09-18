#!/usr/bin/env python3
"""write_step_summary.py — append the estate route monitor summary to
$GITHUB_STEP_SUMMARY (kept OUT of the workflow YAML to avoid block-scalar
column-1 parsing defects). Reads monitor.json produced by the monitor."""
import json
import os


def main():
    with open("monitor.json") as f:
        d = json.load(f)
    summary = os.environ.get("GITHUB_STEP_SUMMARY", "/tmp/step-summary.txt")
    up = d.get("up", "0/0")
    crit = len(d.get("critical_down", []))
    lines = [f"### Estate Route Monitor — {up} up, {crit} critical down"]
    for r in d.get("routes", []):
        mark = "OK" if r.get("ok") else ("WARN" if not r.get("critical") else "DOWN")
        ms = r.get("ms", "?")
        lines.append(f"- [{mark}] {r['route']}: {r.get('status')} {ms}ms")
    with open(summary, "a") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()