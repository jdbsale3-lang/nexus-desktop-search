# NEXUS 2.4.0 — Release Notes

**Encrypted Vault · Ops Trio · Desktop GUI · NEXUS MAIL**

Verified package: nexus-desktop-search.zip
SHA-256: 892cf7fb58c7ed7cb6b4573122009fc8ae26f5c760cc78ad07fc1fd8b74daaf5
Test suite: 15/15 passing (incl. crypto vault + health endpoint under NEXUS_AUTH=1)

## What's new
- NEXUS Vault — Fernet-encrypted secrets at rest (AES-128-CBC + HMAC), PBKDF2-derived keys, 0600 key file: nexus vault init|status|encrypt|decrypt|rotate
- Mail passwords encrypted at rest (vlt:-sealed) with reveal-on-demand; /api/vault/status
- Ops trio — nexus verify (9-check post-install verification, self-boots a server) · nexus watchdog once|watch (polls /api/health, auto-respawns after N misses) · nexus uninstall --yes --keep-data
- Desktop GUI prototype — nexus gui (Tkinter search box, scope selector, results list, preview pane)
- NEXUS MAIL (IMAP/SMTP, searchable mailbox) · OCR for scanned PDFs · intent-aware query parser · hybrid BM25+vector ranking · bearer auth · Docker + CI
- New /api/health open endpoint (service, version, pid, port, uptime, documents, vault)

## Install
```
pip install -r requirements.txt
pip install -r requirements-optional.txt   # OCR + continuous watching
python -m nexus.cli init
python -m nexus.cli index ~/Documents
python -m nexus.cli serve                   # web UI http://localhost:8765
python -m nexus.cli verify                  # confirm the install
python -m nexus.cli gui                     # desktop GUI
```

## Docs
QUICKSTART.md (end users) · VAULT-ROTATION.md (key rotation runbook) · HAND-OFF.md (developer) · MERGE-ANALYSIS.md · NEXUS-OPS.ps1.txt (Windows ops wrapper) · CHANGELOG.md

*All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).*