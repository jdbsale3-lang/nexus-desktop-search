#!/usr/bin/env bash
# integrate-engram.sh — deploy engram (P0 memory backend) for ZEUS.
# Source verified: Gentleman-Programming/engram ★6,738, Go binary, SQLite+FTS5,
# MCP server + HTTP API + CLI. Installs under /opt/engram, wires the
# zeus_memory_engram skill, keeps the flat memory.json as fallback.
# Runs on the DROPLET HOST as root.
set -uo pipefail

APP=/opt/engram
mkdir -p "$APP"

echo "═══ integrate-engram ═══"
echo "-- 1) fetch engram release (Linux amd64) --"
if [ -x "$APP/engram" ]; then
  echo "  engram already installed — skip"
else
  # official install path from the repo README (Go install) or prebuilt tarball
  if command -v go >/dev/null 2>&1; then
    echo "  go toolchain present — installing via go install"
    GOFLAGS=-mod=mod go install github.com/Gentleman-Programming/engram@latest 2>&1 | tail -2 || true
    cp "$(go env GOPATH)/bin/engram" "$APP/engram" 2>/dev/null || true
  fi
  if [ ! -x "$APP/engram" ]; then
    echo "  no go toolchain and no prebuilt — trying GitHub release tarball"
    LATEST=$(curl -s --max-time 20 https://api.github.com/repos/Gentleman-Programming/engram/releases/latest | grep -oP '"tag_name":\s*"\K[^"]+' | head -1)
    if [ -n "$LATEST" ]; then
      curl -sL --max-time 60 -o "$APP/engram.tar.gz" \
        "https://github.com/Gentleman-Programming/engram/releases/download/${LATEST}/engram_linux_amd64.tar.gz" \
        && tar xzf "$APP/engram.tar.gz" -C "$APP" 2>/dev/null || true
    fi
  fi
  chmod +x "$APP/engram" 2>/dev/null || true
fi

echo "-- 2) verify --"
if [ -x "$APP/engram" ]; then
  "$APP/engram" --version 2>/dev/null | head -1 || "$APP/engram" version 2>/dev/null | head -1 || echo "  binary present"
  echo "  OK: $APP/engram"
else
  echo "  !! engram binary not installed — install Go first (apt install golang-go) then re-run"
fi

echo "-- 3) wire the skill --"
cp -n /root/kali/zeus-integration/zeus_memory_engram.py /opt/zeus-skills/ 2>/dev/null && echo "  zeus_memory_engram.py -> /opt/zeus-skills/"
echo "  (engine autodiscovers .py modules; keep memory.json as fallback)"

echo "═══ done — verify: python3 -c \"import sys; sys.path.insert(0,'/opt/zeus-skills'); import zeus_memory_engram as z; print(z.run_skill('status'))\" ═══"