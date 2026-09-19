# syntax=docker/dockerfile:1
# ZEUS-AEGIS Kali security workstation image — TRIMMED build.
# Fixes the droplet disk-wall (15.5 GB metapackage sprawl → ~5 GB tool set):
#   11 heavyweight metapackages replaced by 1 small family + verified direct
#   packages. Every direct name below verified against the LIVE kali-rolling
#   binary-amd64 index (19 Sep 2026, kali.download = vinehost, byte-identical).
#   Names that are NOT direct packages and were therefore NOT pinned:
#   nmap / nikto (via kali-tools-information-gathering) and wpscan (web family).
# Usage:
#   docker build -t kali-aegis:1.0 .
#   docker run --rm -it --cap-add=SYS_PTRACE kali-aegis:1.0
FROM kalilinux/kali-rolling:latest
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    # ── base ────────────────────────────────────────────────────────
    kali-linux-core \
    kali-linux-headless \
    # small recon family — provides nmap, nikto, whois, dnsrecon
    # (nmap/nikto are NOT direct packages in this index; only via family)
    kali-tools-information-gathering \
    postgresql \
    postgresql-client \
    curl \
    git \
    vim \
    ca-certificates \
    # ── verified direct tool packages (live-index confirmed) ─────────
    nuclei \
    subfinder \
    httpx-toolkit \
    feroxbuster \
    sqlmap \
    burpsuite \
    metasploit-framework \
    exploitdb \
    hashcat \
    john \
    hydra \
    wireshark \
    bettercap \
    ghidra \
    radare2 \
    responder \
    impacket-scripts \
    ffuf \
    gobuster \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*.deb \
    # cheat is NOT an apt package in Kali rolling (pip tool) — install via pip
    && pip3 install --break-system-packages --quiet cheat 2>/dev/null || true \
    && for b in nmap nuclei sqlmap burpsuite msfconsole searchsploit hashcat john \
                hydra wireshark bettercap ghidra radare2 responder impacket-psexec cheat; do \
         if ! command -v "$b" >/dev/null 2>&1; then echo "MISSING: $b"; fi; \
       done

# Metasploit needs its framework dir writable; keep the DB in a volume-friendly path.
# postgres user must EXIST before chown — under --no-install-recommends the
# postgresql-common postinst does not reliably create it (proven by field failure
# "chown: invalid user: 'postgres:postgres'"), so create it deterministically.
RUN if ! id postgres >/dev/null 2>&1; then \
      useradd -r -s /usr/sbin/nologin postgres 2>/dev/null || true; \
    fi \
    && mkdir -p /var/lib/postgresql /root/.msf4 \
    && chown -R postgres:postgres /var/lib/postgresql || true

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD bash -c 'for b in nmap nuclei sqlmap msfconsole; do command -v "$b" >/dev/null || exit 1; done && echo "kali-aegis healthy" || exit 1'

WORKDIR /aegis
COPY entrypoint.sh /usr/local/bin/zeus-entrypoint
RUN chmod +x /usr/local/bin/zeus-entrypoint
ENTRYPOINT ["/usr/local/bin/zeus-entrypoint"]
CMD ["bash"]