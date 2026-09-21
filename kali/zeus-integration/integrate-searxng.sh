#!/usr/bin/env bash
# integrate-searxng.sh — deploy estate-owned SearXNG as the WebThinker fallback
# lane. Self-hosted Docker instance on the droplet: no third-party bot walls,
# no API key, estate IP only. Public instances (searx.be / searxng.site /
# paulgo.io) all returned bot/403/timeout from the estate sandbox — self-hosting
# is the reliable path.
# Runs on the DROPLET HOST as root. Usage: bash integrate-searxng.sh
set -uo pipefail

echo "═══ integrate-searxng (estate search fallback lane) ═══"
echo "-- 1) docker present? --"
if ! command -v docker >/dev/null 2>&1; then
  echo "  !! docker not found — run bash ~/kali/install-docker.sh first"
  exit 1
fi

echo "-- 2) run SearXNG (official image, host port 8888) --"
if docker ps --format '{{.Names}}' | grep -q searxng; then
  echo "  searxng already running — skip"
else
  docker run -d --name searxng --restart unless-stopped \
    -p 127.0.0.1:8888:8080 \
    -e SEARXNG_BASE_URL=http://127.0.0.1:8888/ \
    searxng/searxng:latest 2>&1 | tail -1 || \
  docker run -d --name searxng --restart unless-stopped -p 127.0.0.1:8888:8080 searxng/searxng 2>&1 | tail -1
  sleep 8
fi

echo "-- 3) health check --"
curl -s -o /dev/null -w "  searxng health: HTTP %{http_code}\n" \
  "http://127.0.0.1:8888/search?q=NHS&format=json" || echo "  (endpoint not answering yet — give it a few more seconds)"

echo "-- 4) wire into WebThinker (config switch) --"
python3 - <<'PYEOF'
p = "/root/kali/zeus-integration/zeus_webthinker_research.py"
try:
    s = open(p).read()
    if "SEARX_URL" in s:
        print("  webthinker already has SEARX_URL — verify only")
    else:
        s = s.replace('JINA_URL = "https://r.jina.ai/"',
                      'JINA_URL = "https://r.jina.ai/"\nSEARX_URL = "http://127.0.0.1:8888/search"   # estate self-hosted SearXNG lane')
        open(p, "w").write(s)
        print("  SEARX_URL wired into webthinker")
except FileNotFoundError:
    print("  !! webthinker not at expected path — copy from kit first")
PYEOF

echo "═══ done — verify: curl 'http://127.0.0.1:8888/search?q=NHS&format=json' | head -c 200 ═══"