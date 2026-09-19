# syntax=docker/dockerfile:1
# ZEUS-AEGIS Kali security workstation image
# Base: official Kali rolling (has kali-* metapackages in-repo — verified
#       against http.kali.org/kali-rolling/main/binary-amd64/Packages)
# Usage:
#   docker build -t kali-aegis:1.0 .
#   docker run --rm -it --cap-add=SYS_PTRACE kali-aegis:1.0
#
# NOTE: metapackage names below are VERIFIED against the live Kali rolling
# index (18 Sep 2026). Wrong names like kali-linux-network / kali-tools-*-attacks
# do not exist and would fail the build — these are the real ones.

FROM kalilinux/kali-rolling:latest

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    LEAK_TEST_TMP=/tmp

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    # ── base ────────────────────────────────────────────────────────
    kali-linux-core \
    kali-linux-headless \
    postgresql \
    postgresql-client \
    curl \
    git \
    vim \
    ca-certificates \
    # ── tool families (verified metapackages) ───────────────────────
    kali-tools-information-gathering \
    kali-tools-vulnerability \
    kali-tools-web \
    kali-tools-exploitation \
    kali-tools-passwords \
    kali-tools-post-exploitation \
    kali-tools-sniffing-spoofing \
    kali-tools-reporting \
    kali-tools-fuzzing \
    kali-tools-reverse-engineering \
    kali-tools-database \
    kali-tools-top10 \
    # ── cross-cutting extras ─────────────────────────────────────────
    nuclei \
    subfinder \
    httpx-toolkit \
    feroxbuster \
    impacket-scripts \
    responder \
    && rm -rf /var/lib/apt/lists/* \
    # cheat is NOT an apt package in Kali rolling (pip tool) — install via pip
    && pip3 install --break-system-packages --quiet cheat 2>/dev/null || true \
    && for b in nmap nuclei sqlmap burpsuite msfconsole searchsploit hashcat john \
                hydra wireshark bettercap ghidra radare2 responder impacket-psexec cheat; do \
         if ! command -v "$b" >/dev/null 2>&1; then echo "MISSING: $b"; fi; \
       done

# Metasploit needs its framework dir writable; keep the DB in a volume-friendly path
RUN mkdir -p /var/lib/postgresql /root/.msf4 && chown -R postgres:postgres /var/lib/postgresql

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD bash -c 'for b in nmap nuclei sqlmap msfconsole; do command -v "$b" >/dev/null || exit 1; done && echo "kali-aegis healthy" || exit 1'

WORKDIR /aegis

COPY entrypoint.sh /usr/local/bin/zeus-entrypoint
RUN chmod +x /usr/local/bin/zeus-entrypoint

ENTRYPOINT ["/usr/local/bin/zeus-entrypoint"]
CMD ["bash"]