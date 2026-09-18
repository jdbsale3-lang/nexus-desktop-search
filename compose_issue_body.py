#!/usr/bin/env python3
"""compose_issue_body.py — build the outage-issue markdown for the CI
rollback job. Reads rollback_probe.txt (if present) and writes issue_body.md.

Usage (inside the rollback-on-failure workflow step or locally):
    python3 compose_issue_body.py
"""
import pathlib

PROBE = "rollback_probe.txt"
OUT = "issue_body.md"

probe = ""
if pathlib.Path(PROBE).exists():
    probe = pathlib.Path(PROBE).read_text(errors="replace")[:4000]

body = (
    "Automated from the mcp-discovery-test workflow.\n\n"
    "**What happened:** the discovery probe against https://mcp.exa.ai/mcp exposed zero tools "
    "(HTTP 403 auth gate or endpoint change).\n\n"
    "**Evidence (probe output):**\n```\n" + probe + "\n```\n\n"
    "**Actions taken:** rollback-on-failure job ran; no self-heal possible.\n"
    "**Required:** verify the Exa API key is live (exa.ai → API Keys) or confirm the "
    "endpoint/tool naming."
)
pathlib.Path(OUT).write_text(body)
print(f"wrote {OUT} ({len(body)} bytes)")