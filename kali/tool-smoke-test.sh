#!/usr/bin/env bash
# tool-smoke-test.sh — RUNS INSIDE the kali-aegis container.
# Proves each tool actually executes (not just exists). Run: docker exec -it kali-aegis bash /aegis/work/kali/tool-smoke-test.sh
# (the kit is mounted read-only at /aegis/work via docker-compose)
set -uo pipefail
GREEN=$'\e[32m'; RED=$'\e[31m'; OFF=$'\e[0m'
FAILS=0
ok(){ printf "  %bOK%b  %s\n" "$GREEN" "$OFF" "$1"; }
bad(){ printf "  %bFAIL%b %s — %s\n" "$RED" "$OFF" "$1" "$2"; FAILS=$((FAILS+1)); }

check() { # check <name> <command...>
  local name="$1"; shift
  if timeout 20 "$@" >/dev/null 2>&1; then ok "$name"; else bad "$name" "$*"; fi
}

echo "═══ kali tool smoke test ═══"
check "nmap            " nmap -V
check "nuclei          " nuclei -version
check "sqlmap          " sqlmap --version
check "burpsuite       " burpsuite --version
check "msfconsole      " msfconsole -v
check "searchsploit    " searchsploit --version
check "hashcat         " hashcat --version
check "john            " john --version
check "hydra           " hydra -h
check "wireshark       " wireshark --version
check "bettercap       " bettercap -version
check "ghidra          " ghidra --help
check "radare2         " r2 -v
check "responder       " responder -h
check "impacket-psexec " impacket-psexec -h
check "cheat           " cheat -v
check "ffuf            " ffuf -V
check "gobuster        " gobuster version
check "nikto           " nikto -Version
check "wpscan          " wpscan --version
check "subfinder       " subfinder -version
check "httpx           " httpx -version
echo "────────────────────────────────"
if [ "$FAILS" -eq 0 ]; then echo "  ALL TOOLS EXECUTE"; else echo "  $FAILS tool(s) failed to execute"; fi
exit $([ "$FAILS" -eq 0 ] && echo 0 || echo 1)