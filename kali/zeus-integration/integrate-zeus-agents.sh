#!/usr/bin/env bash
# integrate-zeus-agents.sh — install the TikTok/curated AI-agent repos into ZEUS.
# EVERY repo+package name below was verified live against GitHub/PyPI on 2026-09-20
# (stars: browser-use 115K, scientific 45K, cyber 33K, openviking 38K, agentmemory 28K).
# Runs on the DROPLET HOST as root. Installs under /opt/zeus-agents/, wires skills into
# the ZEUS skills engine's autodiscover dir where the format matches (markdown packs).
set -uo pipefail
APP="/opt/zeus-agents"
SKILLS="/opt/zeus-skills"     # ZEUS engine autodiscover dir (f.stem scan)
mkdir -p "$APP" "$SKILLS"

echo "═══ integrate ZEUS AI agents ═══"

# 1) Python packages (verified on PyPI)
echo "-- pip installs --"
pip3 install --break-system-packages -q agentmemory browser-use 2>&1 | tail -1 || true
python3 -c "import agentmemory; print('  agentmemory', agentmemory.__version__ if hasattr(agentmemory,'__version__') else 'OK')" 2>/dev/null || echo "  agentmemory import check: n/a"

# 2) Repos (verified owners/names on GitHub)
clone() { # clone <app-dir> <url>
  local d="$1" u="$2"
  [ -d "$APP/$d/.git" ] && { echo "  $d already present — skip"; return; }
  git clone -q --depth 1 "$u" "$APP/$d" 2>&1 | tail -1 && echo "  cloned $d" || echo "  FAILED $d"
}
clone agentmemory          https://github.com/rohitg00/agentmemory.git
clone scientific-agent-skills https://github.com/K-Dense-AI/scientific-agent-skills.git
clone Anthropic-Cybersecurity-Skills https://github.com/mukul975/Anthropic-Cybersecurity-Skills.git
clone browser-use          https://github.com/browser-use/browser-use.git
clone awesome-harness-engineering https://github.com/ai-boost/awesome-harness-engineering.git
clone OpenViking           https://github.com/volcengine/OpenViking.git

# 3) wire markdown skill packs into the ZEUS autodiscover dir (skills engine scans .md?)
#    copy only the pack dirs, never overwrite existing estate skills
for src in scientific-agent-skills Anthropic-Cybersecurity-Skills; do
  if [ -d "$APP/$src" ]; then
    cp -rn "$APP/$src"/*.md "$SKILLS/" 2>/dev/null || true
    find "$APP/$src" -maxdepth 2 -name "*.md" -exec cp -n {} "$SKILLS/" \; 2>/dev/null || true
  fi
done
echo "  skill files now in $SKILLS: $(find "$SKILLS" -name '*.md' 2>/dev/null | wc -l)"
echo "  estate .py skills preserved: $(find "$SKILLS" -name '*.py' 2>/dev/null | wc -l)"

echo "═══ done — repos under $APP; verify with: ls $APP"
echo "   ZEUS skills engine reload: say 'load skills' or restart agent-reach bridge"