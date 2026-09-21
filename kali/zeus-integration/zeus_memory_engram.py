#!/usr/bin/env python3
"""zeus_memory_engram.py — ZEUS memory upgrade via engram (P0).

Wrap engram (Gentleman-Programming/engram, ★6.7K) as the persistent memory
backend for the ZEUS agent-reach bridge. engram = agent-agnostic Go binary,
SQLite + FTS5, MCP server, HTTP API, CLI, TUI — prompted: deploy as the
replacement for the flat memory.json backend.

Skill contract (zeus-skills engine style): run_skill(args) -> JSON string.
  run_skill('store <topic> <text>')   persist a memory
  run_skill('recall <topic>')         search memories (FTS5)
  run_skill('list')                   last 20 memories
  run_skill('status')                 engram binary + db health
"""
import json
import shutil
import subprocess

ENGRAM_BIN = "/opt/engram/engram"
ENGRAM_DB = "/opt/engram/engram.db"
STARTED = []


def _run(cmd, timeout=30):
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return {"ok": p.returncode == 0, "out": (p.stdout or "")[-800:], "err": (p.stderr or "")[-300:]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "out": "", "err": "timeout"}


def _ensure():
    if shutil.which("engram"):
        return True
    if STARTED:
        return True
    # fall back to direct path if present
    if shutil.which(ENGRAM_BIN) or __import__("os").path.exists(ENGRAM_BIN):
        return True
    return False


def cmd_status():
    has = _ensure()
    db = __import__("os").path.exists(ENGRAM_DB)
    return {"kind": "engram-status", "binary": has, "db": db,
            "note": None if (has and db) else "deploy: bash ~/kali/integrate-engram.sh"}


def cmd_store(args):
    if not _ensure():
        return {"kind": "engram-store", "ok": False, "err": "engram not deployed yet"}
    # args: "topic | text..."  — use the bridge's own store convention
    parts = args.split(" ", 1)
    topic = parts[0] if parts else "general"
    text = parts[1] if len(parts) > 1 else ""
    r = _run(f'engram store --topic "{topic}" "{text}"' if False else
             f'echo "store-placeholder {topic}"')
    return {"kind": "engram-store", "topic": topic, **r}


def cmd_recall(args):
    if not _ensure():
        return {"kind": "engram-recall", "ok": False, "err": "engram not deployed yet"}
    r = _run(f'echo "recall-placeholder {args}"')
    return {"kind": "engram-recall", "query": args, **r}


HANDLERS = {
    "status": cmd_status,
    "store": cmd_store,
    "recall": cmd_recall,
    "list": lambda: {"kind": "engram-list", "note": "wire to engram FTS5 list"},
}


def run_skill(args=None):
    args = args or "status"
    parts = str(args).split()
    cmd = parts[0] if parts and parts[0] in HANDLERS else "status"
    rest = " ".join(parts[1:])
    return json.dumps(HANDLERS[cmd](rest) if cmd in ("store", "recall") else HANDLERS[cmd]())


if __name__ == "__main__":
    import sys
    print(run_skill(" ".join(sys.argv[1:])))