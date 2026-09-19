# ZEUS Kali-AEGIS Security Workstation — Kit README

Offensive-security Docker image + CI + n8n integration for the ZEUS AI estate.
Built on `kalilinux/kali-rolling` with verified metapackages; ships a full and a
slim image, a GitHub Actions build-test gate, a parametrisable 6-tool scan hook,
and a vulnerability-report template. Root-owned by Darren Birch.

## Contents

```
kali/
  Dockerfile              full image (15 core tools, ~large)
  Dockerfile.slim         ~60% smaller scanner-tool image (9 tools)
  entrypoint.sh           version-agnostic start (pg cluster + msfdb init)
  docker-compose.yml      SYS_PTRACE, host bridge, restart=unless-stopped
  install-docker.sh       bootstrap Docker Engine + Compose + Buildx (Ubuntu/Debian)
  quickstart-test.sh      one-shot environment verification (run after build)
  kali-provision.sh       manual (non-Docker) Kali provisioning template
  kali-scan-hook.py       n8n hook: nuclei/nmap/wpscan/nikto/ffuf/httpx -> JSON
  n8n-kali-scan.workflow.json   importable n8n workflow (4 nodes)
  vulnerability-report-template.md   empty report skeleton
  vulnerability-report-SAMPLE.md    filled example (clearly marked SAMPLE)
.github/workflows/
  kali-build-test.yml     CI gate: builds both images, verifies binaries inside
  kali-image-build.yml    weekly + on-change build pipeline (full+slim, gha cache)
```

## Quick start (droplet / Docker host)

```bash
bash kali/install-docker.sh          # once per host: docker + compose + buildx
cd kali && docker build -t kali-aegis:1.0 .          # full image (takes a while)
docker build -f Dockerfile.slim -t kali-aegis-slim:1.0 .   # slim scanner
bash quickstart-test.sh              # verifies daemon, image, 15 binaries
docker compose up -d                 # start container with zeus-sec bridge
```

## Scan via n8n

1. n8n (localhost:5678) → Workflows → **Import from file** → `n8n-kali-scan.workflow.json`
2. Inside the container: `python3 /aegis/work/kali/kali-scan-hook.py <target> --tools all`
3. Trigger: `POST /webhook/kali-scan` with `{"target":"https://…","tools":"nuclei,nmap"}`

## Reports

Fill `vulnerability-report-template.md` per engagement; see
`vulnerability-report-SAMPLE.md` for a complete filled example. Log any estate
finding as INC-00x in the incident ledger.

## Troubleshooting

- **`Unable to locate package X`** → X is not in Kali rolling's apt index
  (e.g. `cheat` is a pip tool). Remove it from the apt list; install via
  `pip3 install --break-system-packages X` if needed.
- **docker missing** → run `bash install-docker.sh` (needs root/sudo).
- **Container won't start** → check `docker compose logs`; entrypoint is
  version-agnostic (pg_lsclusters + msfdb init) so any Kali-rolling base works.
- **CI fails with MISSING:** → the build-test gate found a binary absent
  inside the image; fix the Dockerfile, push, CI re-verifies automatically.

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the
Darren & Jill Birch Trust).