# INC-005 Post-Incident Report — AEGIS CORS Preflight Failure

**Status:** RESOLVED — verified externally 2026-09-20 21:06 UTC
**Severity:** Medium (cross-origin API calls from flagship to apiaegissecurity.tech blocked)
**Ledger ref:** INC-005 (monitor route `aegis_cors`)

---

## 1. Summary

Browser-originated requests from the flagship console to `apiaegissecurity.tech`
failed: the server answered **OPTIONS preflight with HTTP 400** and sent no
`Access-Control-Allow-Origin` header, so no cross-origin call could complete.
Root cause: the nginx server block for the AEGIS API lacked CORS directives.

## 2. Timeline (verified, not estimated)

| Time (UTC) | Event |
|---|---|
| earlier | Monitor flags `aegis_cors`: preflight 400, ACAO missing → INC-005 opened |
| 2026-09-20 ~20:3x | `fix-aegis-cors.py` run on droplet; **field-caught bug**: backup written to `/etc/nginx/sites-enabled/aegis.bak-inc005` — nginx includes every file in sites-enabled regardless of extension → `duplicate listen options for [::]:443` → `nginx -t` failed; restore loop also failed because the stray `.bak` remained |
| 2026-09-20 20:37 | Fix pushed: backups moved to `/root/nginx-backups` (outside nginx include path) + stale-backup relocation; fixture-tested before shipping (four cases) |
| 2026-09-20 21:06 | **External independent probe (this sandbox): preflight 204, PASS** — INC-005 resolved |

## 3. Root Causes

1. **Missing CORS directives** at the origin nginx (original incident).
2. **Fixer backup-path defect** (secondary): backup inside `sites-enabled`
   collided with nginx's include-everything behaviour, blocking `nginx -t`.

## 4. Prevention (now in the estate kit)

- `fix-aegis-cors.py` v2: backups under `/root/nginx-backups/`, relocates stale
  `.bak` files, self-verifies preflight + ACAO, exits non-zero on fail.
- `estate-security-probe.sh`: independent external probe — surfaces, five
  headers, INC-005 preflight, TLS. Green only on verified pass.
- Monitor's `aegis_cors` route stays in the 30-minute sweep.

## 5. Residual state at close

All four estate surfaces **200**; INC-005 preflight **204**; TLS **valid**.
**Open (same campaign):** five flagship security headers not yet on the wire —
probe still reports them MISSING. Not part of INC-005, tracked separately.

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the
Darren & Jill Birch Trust).