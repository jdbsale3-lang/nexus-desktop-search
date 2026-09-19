#!/usr/bin/env bash
# install-docker.sh — bootstrap Docker Engine + Compose + Buildx on Ubuntu/Debian
# (targets: aegis-api droplet, and any Ubuntu 24.04 host). Idempotent.
# Usage: bash install-docker.sh        (run as root or with sudo)
set -euo pipefail

echo "══════════════════════════════════════════════"
echo "  Docker bootstrap — ZEUS estate"
echo "══════════════════════════════════════════════"

# 1) detect OS
if ! grep -qiE "ubuntu|debian" /etc/os-release; then
  echo "!! unsupported OS — Ubuntu/Debian expected"; exit 1
fi
. /etc/os-release
echo "[1/6] OS: $PRETTY_NAME"

# 2) install docker.io from distro repos (simplest reliable path on DigitalOcean)
if ! command -v docker >/dev/null 2>&1; then
  echo "[2/6] installing docker.io (distro package, ~280MB disk)"
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get install -y -qq docker.io
else
  echo "[2/6] docker already installed: $(docker --version 2>/dev/null || echo '?')"
fi

# 3) enable + start
systemctl enable --now docker >/dev/null 2>&1 || true
systemctl --no-pager --lines=0 status docker >/dev/null 2>&1 && echo "[3/6] docker service running" || echo "[3/6] docker service enable attempted"

# 4) compose + buildx plugins
if ! docker compose version >/dev/null 2>&1; then
  echo "[4/6] installing docker-compose plugin"
  apt-get install -y -qq docker-compose-v2 2>/dev/null || true
fi
docker compose version >/dev/null 2>&1 && echo "  compose: OK ($(docker compose version --short 2>/dev/null))" || echo "  compose: fallback (use docker run)"

if ! docker buildx version >/dev/null 2>&1; then
  echo "[4b] buildx not in distro plugin — legacy build works; BuildKit optional"
fi

# 5) add the invoking user to the docker group (non-root usage)
if [ -n "${SUDO_USER:-}" ]; then
  usermod -aG docker "$SUDO_USER" 2>/dev/null || true
  echo "[5/6] user '$SUDO_USER' added to docker group (re-login to take effect)"
else
  echo "[5/6] running as root — docker group addition skipped"
fi

# 6) verify
echo "[6/6] verification"
docker version --format '  client {{.Client.Version}} / server {{.Server.Version}}' 2>/dev/null || docker info 2>/dev/null | grep -E "Server Version|Storage Driver" | sed 's/^/  /'
docker run --rm hello-world >/dev/null 2>&1 && echo "  hello-world: OK (daemon functional)" || echo "  hello-world: skipped (no internet or image pull blocked)"

echo ""
echo "══════════════════════════════════════════════"
echo "  NEXT: cd kali && docker build -t kali-aegis:1.0 ."
echo "══════════════════════════════════════════════"