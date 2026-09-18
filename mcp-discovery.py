#!/usr/bin/env python3
"""
mcp-discovery.py — automated MCP server discovery test.
Connects to any MCP endpoint: initialize -> tools/list, prints the REAL
tool names + auth result. Settles "tool not found" ambiguity in one run.

Usage (droplet console):
  python3 mcp-discovery.py https://mcp.exa.ai/mcp "$EXA_KEY"
  python3 mcp-discovery.py https://mcp.exa.ai/mcp            # reads EXA_KEY env / prompts
  python3 mcp-discovery.py --list-mcp                        # print protocol notes
"""
import json
import os
import sys
import urllib.request


def post(url, payload, headers):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json",
                 "Accept": "application/json, text/event-stream", **headers},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8", "replace")
            lines = [ln for ln in body.splitlines() if ln.startswith("data:")]
            if lines:
                return json.loads(lines[-1][5:])
            if body.strip():
                return json.loads(body)
            return {"ok": True}
    except Exception as e:
        return {"error": str(e)[:200]}


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("usage: mcp-discovery.py <MCP_URL> [API_KEY]\n")
        sys.exit(1)
    url = sys.argv[1]
    key = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("EXA_KEY", "").strip()
    if not key:
        # interactive prompt ONLY when a terminal exists; CI (no tty, or
        # GITHUB_ACTIONS) must fail cleanly with the actionable message —
        # getpass in a runner crashes with termios/EOFError (seen live).
        import sys as _sys
        interactive = _sys.stdin.isatty()
        if interactive and not os.environ.get("GITHUB_ACTIONS"):
            import getpass
            key = getpass.getpass("EXA API key (sk-...): ").strip()
        else:
            print("== EXA key not provided and no interactive terminal ==")
            print("   CI mode: set the EXA_KEY secret (repo → Settings → Secrets → EXA_API_KEY),")
            print("   or pass the key as argv[2] / EXA_KEY env.")
            sys.exit(3)

    # sanity: Exa API keys are UUID-format (8-4-4-4-12 hex), NOT sk- prefixed.
    # Accept BOTH a UUID and an sk- style key; reject anything else (paste text).
    import re as _re
    _uuid_ok = bool(_re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", key or ""))
    if key and not (_uuid_ok or key.startswith("sk-")):
        print(f"!! KEY LOOKS WRONG: {len(key)} chars, starts with '{(key or '')[:3]}…' "
              f"(Exa keys are UUID-format or sk- + ~40 chars; this looks like paste text). "
              f"Refuse to waste a request — check exa.ai → API Keys.")
        sys.exit(2)

    print(f"== MCP discovery: {url}")
    print(f"== API key present: {'yes (%d chars)' % len(key) if key else 'NO — will 403'}")
    hdr = {"x-api-key": key} if key else {}

    # 1) initialize
    init = post(url, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2024-11-05", "capabilities": {},
        "clientInfo": {"name": "zeus-discovery", "version": "1.0"}}}, hdr)
    if init.get("error") or "error" in (init.get("result") or {}):
        print(f"INIT FAILED: {json.dumps(init)[:220]}")
        print("=> If HTTP 403: the key is invalid/missing — get a real key at exa.ai")
        sys.exit(2)
    inf = (init.get("result") or {})
    sid = (inf.get("_meta") or {}).get("sessionId") or {}
    if sid:
        hdr["Mcp-Session-Id"] = sid
    print(f"INIT OK · server: {inf.get('serverInfo', {}).get('name', '?')} · protocol: {inf.get('protocolVersion', '?')}")

    # 2) tools/list
    tl = post(url, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, hdr)
    tools = ((tl.get("result") or {}).get("tools") or [])
    print(f"TOOLS EXPOSED: {len(tools)}")
    names = []
    for t in tools:
        name = t.get("name")
        names.append(name)
        print(f"   {name:30s} {str(t.get('description') or '')[:70]}")
        schema = t.get("inputSchema", {}).get("properties", {})
        if schema:
            print(f"      args: {', '.join(list(schema.keys())[:6])}")
    if not names:
        print("=> Zero tools: auth gate. Use a REAL sk- key (not a placeholder).")
        sys.exit(3)
    print(f"=> CANDIDATE CALL: mcporter call exa {names[0]} \"query=zeus ai\"")


if __name__ == "__main__":
    main()