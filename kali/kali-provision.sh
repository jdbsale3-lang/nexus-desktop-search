#!/usr/bin/env bash
# kali-provision.sh — ZEUS estate Kali workstation provisioning.
# Runs on a FRESH Kali install (rolling). Installs the curated metapackage set
# mapped to AEGIS red-team goals + extra tools, then verifies the install.
# Usage: sudo bash kali-provision.sh
set -euo pipefail

echo "════════════════════════════════════════════════════════════"
echo "  KALI PROVISION — ZEUS estate security workstation"
echo "  Target: authorized testing of the ZEUS/AEGIS estate only."
echo "════════════════════════════════════════════════════════════"

# 1) system preflight
if [ "$(id -u)" -ne 0 ]; then echo "!! run as root: sudo bash kali-provision.sh"; exit 1; fi
if ! grep -qi kali /etc/os-release; then echo "!! this script is Kali-specific (see /etc/os-release)"; exit 1; fi
echo "[1/5] preflight OK — Kali detected"

# 2) up to date
apt-get update -qq
apt-get upgrade -y -qq
echo "[2/5] system updated"

# 3) curated metapackages — mapped to the estate security goal
#    (information gathering → vulnerability → web → exploitation →
#     passwords → post-exploitation → sniffing → reporting → fuzzing)
META_PKGS=(
  kali-tools-information-gathering
  kali-tools-vulnerability
  kali-tools-web
  kali-tools-exploitation
  kali-tools-passwords
  kali-tools-post-exploitation
  kali-tools-sniffing-spoofing
  kali-tools-reporting
  kali-tools-fuzzing
  kali-tools-reverse-engineering
)
echo "[3/5] installing metapackages: ${META_PKGS[*]}"
apt-get install -y -qq "${META_PKGS[@]}"

# 4) extra tools that cross several metapackages
EXTRA_PKGS=(
  nuclei
  subfinder
  httpx-toolkit
  feroxbuster
  wpscan
  nikto
  sqlmap
  ffuf
  gobuster
  dirb
  burpsuite
  metasploit-framework
  exploitdb
  searchsploit
  john
  hashcat
  hydra
  netcat-traditional
  impacket-scripts
  responder
  wfuzz
  dradis
  pipal
  cutycapt
  ghidra
  radare2
  gdb
  verbose-httpd
)
# note: cheat is NOT in Kali apt (pip tool) — install via: pip3 install --break-system-packages cheat
echo "[4/5] installing extra tools: ${EXTRA_PKGS[*]}"
apt-get install -y -qq "${EXTRA_PKGS[@]}"

# 5) verify — key binaries must exist
echo "[5/5] verification"
BINS=(nmap nikto nuclei wpscan sqlmap ffuf gobuster metasploit-framework msfconsole john hashcat hydra burpsuite searchsploit wireshark bettercap ghidra radare2 responder impacket-psexec wfuzz dradis cutycapt)
MISSING=0
for b in "${BINS[@]}"; do
  if command -v "$b" >/dev/null 2>&1 || dpkg -s "$b" >/dev/null 2>&1; then
    printf "  [OK] %s\n" "$b"
  else
    printf "  [--] %s (missing)\n" "$b"
    MISSING=1
  fi
done

echo ""
echo "════════════════════════════════════════════════════════════"
if [ "$MISSING" -eq 0 ]; then
  echo "  KALI WORKSTATION READY — authorized estate testing only."
else
  echo "  Some optional binaries not found — install individually if needed."
fi
echo "  Next: sudo msfdb init  (Metasploit database first-run)"
echo "════════════════════════════════════════════════════════════"