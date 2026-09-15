# NEXUS — Private Local-First Search Desk

Search your files, email and the web from one box — private, offline-capable, encrypted. NEXUS 2.4.0.

## Highlights
- Hybrid search: BM25 keyword + vectors + recency + learned behaviour
- Intent-aware queries: `"phrase"`, `filetype:`, `path:`, `past N days`, `scope:local|web|all`
- Extracts text, PDF (incl. scanned via OCR), DOCX, XLSX, PPTX
- Continuous indexing (watch mode) + persistent memory
- **NEXUS MAIL**: IMAP receive / SMTP send with a searchable mailbox
- **NEXUS Vault**: Fernet-encrypted credentials at rest (`NEXUS_ENCRYPTION=1`), 0600 key file, rotation runbook
- Bearer auth, Docker deploy, CI (test + vault + smoke + release), cross-platform smoke tests
- **Desktop GUI prototype**: `python -m nexus.cli gui` (Tkinter)
- Operational tools: `nexus verify` (post-install checks), `nexus watchdog` (health-check + auto-respawn), `nexus uninstall`

## Quick start
```bash
pip install -r requirements.txt
pip install -r requirements-optional.txt   # OCR + continuous watching
python -m nexus.cli init
python -m nexus.cli index ~/Documents
python -m nexus.cli serve                   # web UI at http://localhost:8765
python -m nexus.cli verify                  # 9-check post-install verification
python -m nexus.cli gui                     # desktop GUI prototype
```

Docs in this repo: QUICKSTART.md (end users), VAULT-ROTATION.md (key rotation runbook), HAND-OFF.md (developer hand-off), MERGE-ANALYSIS.md, CHANGELOG.md.

*All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).*