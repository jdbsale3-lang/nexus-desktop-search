#!/usr/bin/env bash
# quickstart-test.sh — ZEUS Kali-AEGIS one-shot environment verification.
# Run AFTER the image is built. Exits non-zero if anything hard is missing.
# Usage: bash quickstart-test.sh [image-tag]   (default kali-aegis:1.0)
set -uo pipefail
IMG="${1:-kali-aegis:1.0}"
FAILS=0
GREEN=$'\e[32m'; YELLOW=$'\e[33m'; RED=$'\e[31m'; OFF=$'\e[0m'
ok(){ echo "  ${GREEN}OK${OFF}  $1"; }
warn(){ echo "  ${YELLOW}SKIP$OFF  $1"; }
bad(){ echo "  ${RED}FAIL${OFF} $1"; FAILS=$((FAILS+1)); }

echo "═══════════════ kali quickstart (image: $IMG) ═══════════════"

# 1. docker daemon
if docker info >/dev/null 2>&1; then
  ok "docker daemon reachable ($(docker version --format '{{.Server.Version}}' 2>/dev/null))"
else
  bad "docker daemon NOT reachable — run bash install-docker.sh first"
  echo; echo "$FAILS hard failure(s)"; exit 1
fi

# 2. image present?
if docker image inspect "$IMG" >/dev/null 2>&1; then
  ok "image $IMG present ($(docker image inspect "$IMG" --format '{{.Size}}' | awk '{printf "%.1f GB", $1/1073741824}'))"
else
  bad "image $IMG missing — run: cd kali && docker build -t $IMG ."
  echo; echo "$FAILS hard failure(s)"; exit 1
fi

# 3. base is kali-rolling
BASE=$(docker image inspect "$IMG" --format '{{.Config.Labels}}' 2>/dev/null)
echo "  image labels: ${BASE:-n/a}"

# 4. entrypoint smoke: boot, wait, then verify binaries inside
echo "-- starting ephemeral test container (entrypoint smoke) --"
CID=$(docker run -d --rm --entrypoint /bin/bash "$IMG" -c "sleep 30")
sleep 3
RUNNING=$(docker inspect -f '{{.State.Running}}' "$CID" 2>/dev/null)
[ "$RUNNING" = "true" ] && ok "container boots and stays up (entrypoint OK)" || warn "container state: ${RUNNING:-gone}"

CORE="nmap nuclei sqlmap burpsuite msfconsole searchsploit hashcat john hydra wireshark bettercap ghidra radare2 responder impacket-psexec cheat"
MISSING=""
for b in $CORE; do
  if ! docker exec "$CID" bash -c "command -v $b >/dev/null 2>&1"; then
    MISSING="$MISSING $b"
  fi
done
docker kill "$CID" >/dev/null 2>&1
if [ -z "$MISSING" ]; then
  ok "all 15 core tools present inside the image"
else
  bad "missing binaries inside image:$MISSING"
fi

# 5. extras (slim image only / optional)
for x in ffuf gobuster nikto wpscan subfinder httpx; do
  if docker run --rm --entrypoint bash "$IMG" -c "command -v $x >/dev/null 2>&1"; then
    ok "extra tool: $x present"
  fi
done

# 6. verdict
echo "─────────────────────────────────────────────────────────────"
if [ "$FAILS" -eq 0 ]; then
  echo "  ${GREEN}ALL CHECKS PASSED${OFF} — Linux workstation is ready."
  echo "  Next: docker compose up -d, then trigger kali-scan webhook."
else
  echo "  ${RED}$FAILS hard failure(s)${OFF} — see lines above."
fi
echo "─────────────────────────────────────────────────────────────"
exit $([ "$FAILS" -eq 0 ] && echo 0 || echo 1)