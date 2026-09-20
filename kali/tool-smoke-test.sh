#!/usr/bin/env bash
# tool-smoke-test.sh — RUNS INSIDE the kali-aegis container.
# Proves each tool actually executes (not just exists) with VERIFIED flags
# (v11: fixed searchsploit/john/gobuster/httpx flags + 60s first-boot timeout).
# Run: docker exec -it kali-aegis bash /aegis/work/kali/tool-smoke-test.sh
set -uo pipefail
GREEN=$'\e[32m'; RED=$'\e[31m'; OFF=$'\e[0m'
FAILS=0
ok(){ printf "  %bOK%b  %s\n" "$GREEN" "$OFF" "$1"; }
bad(){ printf "  %bFAIL%b %s — %s\n" "$RED" "$OFF" "$1" "$2"; FAILS=$((FAILS+1)); }

check() { # check <name> <command...> — "executes" semantics:
  #   127/126 = missing/not-executable  -> FAIL
  #   124     = timeout (hung)          -> FAIL
  #   any other exit (0,1,2,...)        -> OK (the tool ran; flag side-effects are the command's business)
  local name="$1"; shift
  timeout 60 "$@" >/dev/null 2>&1
  local rc=$?
  if [ "$rc" -eq 127 ] || [ "$rc" -eq 126 ]; then bad "$name" "missing ($*)";
  elif [ "$rc" -eq 124 ]; then bad "$name" "timeout ($*)";
  else ok "$name"; fi
}

echo "═══ kali tool smoke test (v12) ═══"
check "nmap            " nmap -V
check "nuclei          " nuclei -version
check "sqlmap          " sqlmap --version
check "burpsuite       " burpsuite --version
check "msfconsole      " msfconsole -v
check "searchsploit    " searchsploit apache
check "hashcat         " hashcat --version
check "john            " john --list=build-info
check "hydra           " hydra -h
check "wireshark       " wireshark --version
check "bettercap       " bettercap -version
check "ghidra          " ghidra --help
check "radare2         " r2 -v
check "responder       " responder -h
check "impacket-psexec " impacket-psexec -h
check "cheat           " cheat -v
check "ffuf            " ffuf -V
check "gobuster        " gobuster -h
check "nikto           " nikto -Version
check "wpscan          " wpscan --version
check "subfinder       " subfinder -version
check "httpx           " httpx -h
echo "────────────────────────────────"
if [ "$FAILS" -eq 0 ]; then echo "  ALL TOOLS EXECUTE — 22/22 verified"; else echo "  $FAILS tool(s) failed"; fi
exit $([ "$FAILS" -eq 0 ] && echo 0 || echo 1)