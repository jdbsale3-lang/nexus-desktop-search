#!/usr/bin/env bash
# zeus-entrypoint — starts PostgreSQL for Metasploit, initialises msfdb on
# first run, then execs the container command (default: bash).
# Version-agnostic: discovers the installed postgres cluster via pg_lsclusters.
set -euo pipefail

# 0) Ensure the postgres user exists (same deterministic guard as the Dockerfile
#    build step). Under --no-install-recommends the postgresql-common postinst
#    does not reliably create it — without this, runuser below fails at runtime.
if ! id postgres >/dev/null 2>&1; then
  useradd -r -s /usr/sbin/nologin postgres 2>/dev/null || true
fi

# 1) PostgreSQL: start the default cluster if present (Debian/Kali uses
#    pg_ctlcluster; falls back to pg_ctl on the discovered data dir).
if command -v pg_lsclusters >/dev/null 2>&1; then
  VER=$(pg_lsclusters -h 2>/dev/null | awk '{print $1}' | head -1)
  if [ -n "$VER" ]; then
    pg_ctlcluster "$VER" main start >/dev/null 2>&1 || true
  fi
else
  # manual fallback for older images
  for PGBIN in /usr/lib/postgresql/*/bin; do
    PGDATA=$(ls -d /var/lib/postgresql/*/main 2>/dev/null | head -1 || true)
    if [ -n "$PGDATA" ] && [ -x "$PGBIN/pg_ctl" ]; then
      runuser -u postgres -- "$PGBIN/pg_ctl" -D "$PGDATA" -l /tmp/pg.log start >/dev/null 2>&1 || true
      break
    fi
  done
fi

# 2) Metasploit DB init (once, non-fatal)
if [ ! -f /root/.msf4/db.sqlite3 ]; then
  msfdb init >/dev/null 2>&1 || true
fi

# 3) exec the requested command
exec "$@"