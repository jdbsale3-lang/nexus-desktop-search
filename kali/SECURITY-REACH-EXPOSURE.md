# SECURITY FINDING — /reach/ endpoints are publicly readable (NOT a compromise)
**Filed:** 22 Sep 2026 · **Severity:** Medium (information disclosure + quota abuse) · **Compromise:** NONE found

---

## YOUR TWO QUESTIONS — ANSWERED WITH EVIDENCE

### Q1: Why is there Chinese writing?
**Because the `agent-reach` tool is a Chinese-market build and its channel catalogue ships zh-CN display names.** Proof, not opinion:
- The strings are **channel display names**, not injected content: `B站视频、字幕和搜索` = "Bilibili videos, subtitles & search", `雪球股票行情与社区动态` = "Xueqiu stock quotes & community feed", `小宇宙播客转文字` = "Xiaoyuzhou podcast transcription".
- The channel SET proves the origin: bilibili, xiaohongshu, xueqiu, **Boss直聘**, 小宇宙 — all Chinese platforms.
- Character test: all **Han, zero kana** → Simplified Chinese, not Japanese.
- They are **not Japanese and not ours**: our own code contains only 4 files with Han characters, and every one is either the platform's real name (`直聘` in the MCP channel list) or a **verbatim quote of the tool's diagnostic message** that I transcribed into `ZEUS-DIAGNOSTIC-REPORT` / `ZEUS-FOUNDATIONS-COMPLETE-TESTED` / `COOKIE-SETUP-RUNBOOK`.
- Fix (cosmetic): `LANG=en_GB.UTF-8` / `LC_ALL` on the bridge — already noted; the CLI's own catalogue may stay zh (it's compiled in), which is harmless.

### Q2: Have we been hacked? — NO EVIDENCE OF COMPROMISE
| Check | Result |
|---|---|
| Skills loaded / broken | **27 / 0** — every skill loads cleanly (an injected module would normally break or appear unexplained) |
| Skills inventory vs repo | **every reported capability is a known repo skill, my 2 new modules, or `estate_status` — NO strangers** |
| Channels | exactly the expected set: github ok · exa ok (our fixes) · twitter/linkedin/xueqiu warn (no creds) · reddit/facebook/instagram/xiaohongshu/boss/xiaoyuzhou off (no backends) — **no unexpected channels** |
| Bridge source | matches our repo; `_auth()` requires `Bearer` + `REACH_TOKEN`; binds **127.0.0.1:8081 (localhost only)** |
| Our code for foreign content | only the 4 legitimate Han occurrences above — **no injected strings, no unknown scripts, no odd cron, no new users** |
| Skills/doctor JSON shape | consistent with the tool's documented schema — no injected keys |

**Verdict: no compromise. The Chinese is tool localisation; the estate's own code is clean.**

---

## BUT — THE REAL FINDING YOUR QUESTION SURFACED
Every `/reach/*` route answers **HTTP 200 without a credential**, including **action routes**:
```
/reach/self 200 · /reach/doctor 200 · /reach/monitor 200 · /reach/metrics 200
/reach/platform 200 · /reach/search?q=… 200 · /reach/gh?q=… 200
```
**Why:** the bridge is Bearer-gated, but **nginx injects the token server-side** for the same-origin `/reach/` location (that's how the Command Centre dashboard reads `/reach/doctor`). Effect: the token gate is bypassed at the edge, so **anyone on the internet can read the estate's internals and burn your Exa/GitHub quota** via `/reach/search` and `/reach/gh`.

**This is an exposure, not a breach** — nothing indicates data was taken or code altered.

### The fix (pick one; #1 recommended)
1. **Cloudflare Access on `/reach/*`** — SSO gate at the edge; the dashboard works for you (logged-in), the world sees 403. Cloudflare dashboard → Zero Trust → Access → Application → path `zeusaiintelligence.com/reach/*` → policy = your email.
2. **Cloudflare WAF rule** — allow only your IP(s) to `/reach/*`, block the rest. Fastest, no code change.
3. **nginx basic auth** on the `/reach/` location — prompts your browser once; breaks scripts that call it headlessly.
4. **Minimal immediate mitigation (no dependency on your CF account):** add an nginx location that blocks the *action* routes while keeping read-only ones for the dashboard:
```nginx
location ~ ^/reach/(search|gh|read|yt|bili|v2ex|rss)$ { return 403; }
```
(keeps `/reach/self|doctor|monitor|metrics|platform` for the dashboard; kills the quota-abuse surface).

### Recommended order, sir
Do **#2 or #1 today** (one Cloudflare screen), then **#4** as belt-and-braces in nginx. Full lockdown to my last token-gate standard can come after the NHS meeting.

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).