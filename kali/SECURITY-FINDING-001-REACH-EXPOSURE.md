# SECURITY FINDING 001 — Public read/abuse exposure on `/reach/*`
**Classification:** Medium · **Status:** OPEN (fix ready; one Cloudflare screen) · **Compromise:** NONE
**Found:** 22 Sep 2026 · **Found by:** adversarial review prompted by the user's "have we been hacked?" question
**Owner:** Darren Birch / ZEUSTRUSTAEGISSECURITY LTD · **Asset:** zeusaiintelligence.com (droplet aegis-api 188.166.175.149)

---

## 1. SUMMARY
The ZEUS reach bridge (`127.0.0.1:8081`) enforces a `Bearer` token (`_auth()`), but nginx **injects that token server-side** for the same-origin `/reach/` location so the Command Centre dashboard can read `/reach/doctor`. Net effect: **the token gate is bypassed at the edge** and every `/reach/*` route is readable/usable by anyone on the internet.

## 2. EVIDENCE (reproduced 22 Sep 2026, unauthenticated from the public internet)
```
/reach/self     200      /reach/doctor    200      /reach/monitor  200
/reach/metrics  200      /reach/platform  200
/reach/search?q=… 200    /reach/gh?q=…    200      ← ACTION routes, unauthenticated
```
Sample disclosure: `{"identity":"ZEUS AI Intelligence","host":"aegis-api (188.166.175.149)","skills_loaded":27,…}` — internal host, capability inventory and channel statuses are public.

## 3. IMPACT
| Dimension | Assessment |
|---|---|
| Confidentiality | **Medium** — internal host, skill inventory, channel configuration, health/metrics disclosed |
| Integrity | **None observed** — no write route exposed; no evidence of modification |
| Availability / cost | **Low-Medium** — `/reach/search` and `/reach/gh` consume the estate's **Exa credits and GitHub API quota**; an attacker could burn quota |
| Detection | Not flagged by any prior scan (the routes answer 200, so "healthy" probes passed) |

## 4. ROOT CAUSE
Defence placed at the wrong layer: authentication was enforced *inside* the bridge, then neutralised for browser use by header injection at the proxy. The trust boundary (public internet) has no control.

## 5. REMEDIATION (ordered; #1 recommended)
1. **Cloudflare Access** on `zeusaiintelligence.com/reach/*` — Zero Trust → Access → Applications → Add self-hosted → path `/reach/*` → policy: allow Darren's email. Dashboard keeps working (you're logged in); the world gets 403.
2. **Cloudflare WAF rule** — allow only your IP(s) on `/reach/*`, block the rest (fastest, no code change).
3. **nginx basic auth** on the `/reach/` location (prompts the browser once; breaks headless callers).
4. **Immediate belt (zero dependency):**
```nginx
location ~ ^/reach/(search|gh|read|yt|bili|v2ex|rss)$ { return 403; }
```
keeps read-only routes for the dashboard, kills the quota-abuse surface.

## 6. VERIFICATION AFTER FIX
```bash
curl -s -o /dev/null -w '%{http_code}\n' https://zeusaiintelligence.com/reach/self    # expect 403 (or 302 to Access)
curl -s -o /dev/null -w '%{http_code}\n' https://zeusaiintelligence.com/reach/search?q=x  # expect 403
# and the dashboard must still render /reach/doctor when signed in
```

## 7. RELATED FINDING — 002 (Informational): zh-CN strings in the tool output
The `agent-reach` CLI ships Simplified-Chinese channel display names (`B站视频、字幕和搜索`). **Not an intrusion**: character analysis shows Han-only, no kana; the strings originate in the tool's own catalogue, and our code contains only 4 legitimate Han occurrences (the platform's real name `直聘`, plus verbatim quotes of the tool's diagnostics that we transcribed into reports).
**Fix (implemented):** `locale-en-fix.py` wraps the bridge's `_send()` and renders the channel catalogue in English at egress — fixture-verified (15 mappings; unknown values passed through untouched).

## 8. INTEGRITY ATTESTATION (why this is an exposure, not a breach)
- skills **27 loaded / 0 broken**; every capability maps to a known repo module, my two new modules, or `estate_status` — **no unexplained modules**
- channel set exactly as designed (no unexpected channels)
- bridge source matches our repo; binds **localhost only**
- no injected content, no unexpected cron, no new users, no modified unit files observed

---
**All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).**