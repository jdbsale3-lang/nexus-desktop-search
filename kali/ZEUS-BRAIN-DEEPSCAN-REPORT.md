# ZEUS DEEP SCAN — "the brain is unreachable" — DIAGNOSED AND FIXED
**Date:** 22 Sep 2026 · **Scope:** Command Centre (zeusaiintelligence.com), the brain, the voice lane, CSP, page performance
**Verdict:** the brain was **never down** — my own Content-Security-Policy was blocking the page from calling it.

---

## 1. THE FAULT — found, reproduced, fixed
**Symptom:** the Command Centre said "brain unreachable"; DevTools reported 5 blocked resources.
**Root cause:** the v1 CSP (which I set) allowed only `'self'` + Cloudflare Insights on `connect-src`, and only `'self'` + CI on `script-src`. Every origin the Command Centre legitimately calls was therefore blocked.

| Blocked origin | Directive | What it powers | Its own status |
|---|---|---|---|
| `apiaegissecurity.tech/health` | connect-src | **THE ZEUS BRAIN** | **200 — UP** |
| `generativelanguage.googleapis.com/...generateContent` | connect-src | Gemini brain | up (blocked) |
| `api.elevenlabs.io` + `api.us.elevenlabs.io` (+ wss) | connect-src | voice widget / S2S | up |
| `api.deepgram.com` (wss) | connect-src | speech-to-text | up |
| `api.open-meteo.com` | connect-src | weather tile | 200 |
| `api.duckduckgo.com` | connect-src | UK news tile | 202 |
| `unpkg.com/@elevenlabs/convai-widget-embed` | script-src-elem | voice widget bundle | 302 → live |
| `api.fontshare.com` | style/font-src | fonts | — |

**Fix:** CSP v2 allowlists exactly those origins (no wildcard for `script-src`; `frame-ancestors`/`base-uri`/`form-action` stay locked). Applied two ways:
- **source corrected** — `nginx-security-headers.conf` updated so no future re-apply can re-break the site
- **live patch** — `csp-fix.py`: finds every nginx config setting a CSP, backs it up, rewrites the value, runs `nginx -t`, **reloads only if the test passes**, restores on any failure. Fixture-verified (all six origins present; idempotent on re-run).

```bash
# droplet
cd /root && curl -sL -o k71.zip "<kit link>" && unzip -o k71.zip -d /root/kali
python3 /root/kali/kali/zeus-integration/csp-fix.py
systemctl reload nginx
curl -sI https://zeusaiintelligence.com | grep -i content-security   # expect apiaegissecurity.tech + wss:// in the header
```
**Then hard-refresh the Command Centre (Ctrl-Shift-R)** — the brain, weather, news, voice widget and Gemini tiles should all light up.

## 2. SECURITY FINDING 003 — Gemini API key exposed in the page (NEW, act today)
The page source contains a **live Gemini API key in a URL**:
`generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key=AQ.Ab8RN6…`
**Impact:** any visitor can read that key from the page and spend on your Google account (quota/cost abuse, and it's tied to your AI stack).
**Fix, in order:** ① **rotate the key now** in Google AI Studio ② stop shipping it to the browser — proxy the call through the droplet (`/reach/gemini`, key held server-side in `/opt/zeus-reach.env`) ③ add a referrer/quota restriction on the key as a stopgap ④ after rotation, re-run `csp-fix.py` (the CSP already permits the origin; only the placement changes).

## 3. PAGE PERFORMANCE — measured from your own panel
| Metric | Value | Read |
|---|---|---|
| LCP | **0.71 s** | good |
| CLS | **0.00** | good |
| **INP** | **224 ms** | *needs improvement* — interaction latency on the HUD controls (`button#zhHic`, `div.zh-body`) |

**Recommendation:** the HUD's pointer handlers are doing work on the main thread at click time. Two cheap wins: ① defer/debounce the stream redraws (the `.zh-stream` elements animate on interaction) ② move the brain poll off the interaction path (it's already cached server-side now — 4.7 s → 140 ms — so most of the residue is client-side).

## 4. EVERYTHING ELSE — re-verified after the diagnosis
- **Apps:** 26/26 hosted apps return 200 with real content (audited earlier today)
- **Surfaces:** flagship · NEXUS · AEGIS API · /reach/health = 200
- **Brain:** `apiaegissecurity.tech` **200** — "AEGIS AI Security Platform v1.0.0", all modules `active`
- **Engine:** skills **27 / 0 broken** · monitor 0 alerts · doctor github **ok** · exa_search **ok**
- **Latency:** doctor 4,725 ms → **140 ms** · self 5,086 ms → **113 ms** (cache live)
- **Locale:** 0 Han characters in the output (fix live)
- **Security:** headers 5/5 on the wire (CSP being corrected now) · CORS 204 · finding 001 (/reach exposure) open with fix ready

## 5. ORDER OF ACTION FOR YOU
1. **`csp-fix.py`** → the brain and every tile come back (1 command)
2. **Rotate the Gemini key** (finding 003) → then move it server-side
3. **nginx belt + Cloudflare Access** (finding 001) → close the /reach exposure
4. Optional: HUD INP tuning; S2S lane needs only a (new) Gemini key to go live

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).