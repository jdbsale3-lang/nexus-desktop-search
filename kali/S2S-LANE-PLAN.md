# SPEECH-TO-SPEECH LANE PLAN — ZEUS real-time voice
**Goal:** give ZEUS a true real-time spoken loop (listen → think → speak) under the ~800 ms threshold where conversation feels natural, replacing the ASR→LLM→TTS handoff chain for live use.
**Status:** plan + adapter contract ready · one API key away from live.

---

## 1. WHY A NEW LANE (not a faster pipeline)
The estate already does text→speech→text (verified live 22 Sep: TTS produced audio, STT transcribed it back). But the pipeline has **three handoffs** — ASR → LLM → TTS — and each one adds latency plus its own failure mode. Every sub-800 ms conversational system in 2026 either collapses the handoffs into one multimodal model (native S2S) or buys a very fast streaming TTS.

## 2. MEASURED OPTIONS (Sep 2026 research, cited figures)
| Option | Type | First-audio / latency | Languages | Cost signal |
|---|---|---|---|---|
| **Gemini Live API (2.5/3.1 Flash Native Audio)** | native S2S | **0.63 s** (fastest measured) | **97** | ~10× cheaper audio input than OpenAI; free tier |
| OpenAI Realtime (`gpt-realtime-2`) | native S2S | 300–500 ms e2e | dozens | premium, most mature SDK |
| xAI Grok Voice Agent (`grok-voice-latest`) | native S2S | 0.78 s | dozens | mid |
| Cartesia Sonic 2 (streaming TTS) | pipeline TTS | ~90 ms TTFB, 4.7 MOS | many | low |
| ElevenLabs Flash v2.5 | pipeline TTS | ~75 ms TTFB, 4.55 MOS | many | low-mid |
| Piper (self-host CPU) | pipeline TTS | ~30 ms TTFB, free | several | zero |

**Recommendation: Gemini Live API as the primary lane** (fastest measured, cheapest at scale, 97 languages, free tier to prototype), with **OpenAI Realtime as the resilience lane** (best conversational dynamics: barge-in, backchannels, turn-taking). Keep the existing pipeline for batch narration — it works and costs nothing extra.

## 3. LATENCY BUDGET (target < 800 ms)
```
mic capture + VAD/turn detection   ~80–150 ms   (client-side)
transport to the model             ~30–60 ms    (EU region, close to LON1)
model first-audio                  ~600–700 ms  (Gemini Live: 0.63 s measured)
playback start                     ~20–40 ms
------------------------------------------------
budget total                       ~730–950 ms  → inside the natural-conversation band
```
**What kills it:** US-region endpoints (+150–250 ms), non-streaming TTS (OpenAI tts-1-hd >500 ms, Google Studio >500 ms), and re-loading the system prompt per turn.

## 4. ARCHITECTURE IN ZEUS
```
Client (Command Centre / phone)
  └─ WebSocket ─→ /reach/voice  (bridge route)
        ├─ Gemini Live session (audio in/out, native)
        ├─ system prompt = estate context + skill manifest (CACHED, not rebuilt)
        └─ tool calls → existing 27 skills (confirm_gate enforced on irreversible intents)
Fallback chain: Gemini Live → OpenAI Realtime → pipeline (ASR→LLM→TTS)
```
**Skill contract (new module, mirrors the engine schema):**
```python
SKILL = {"name": "live_voice", "description": "Real-time speech-to-speech session (Gemini Live, OpenAI Realtime fallback)",
         "category": "core", "inputs": {"mode": "str"}, "entry": "run_skill"}
```
`mode="start"` opens a session and returns the socket URL + session id; `mode="status"` reports which backend is live and its measured first-audio time; irreversible tool calls inside a session **must** pass the global confirm gate (already enforced at the router).

## 5. ROLLOUT (4 steps, each verifiable)
1. **Key** — add `GEMINI_API_KEY` (or `OPENAI_API_KEY`) to `/opt/zeus-reach.env`; restart `zeus-reach`.
2. **Adapter** — install `live_voice.py` into `/opt/zeus-skills/`; `/reach/self` should read **28** skills, 0 broken.
3. **Live test** — speak a 5-word phrase, measure first-audio on the wire; record the real number (the plan's figures are vendor-measured, ours must be proven).
4. **Wire to the Command Centre** — a push-to-talk tile calling `/reach/voice`; keep the pipeline as the fallback and A/B on real traffic.

## 6. RISKS & CONTROLS
| Risk | Control |
|---|---|
| Runaway API cost on an open socket | per-session cap + idle timeout; log usage per session |
| Irreversible action spoken by accident | global confirm gate at the router (already live) |
| Echo / self-hearing | client-side echo cancellation; half-duplex during playback if needed |
| Vendor outage | automatic fallback chain (Gemini → OpenAI → pipeline) |
| Language mismatch | pin the session language; Gemini covers 97 |
| Privacy (health/NHS context) | keep sessions ephemeral, no transcript persistence without consent; DPIA note required before any NHS-facing voice use |

## 7. WHAT'S NEEDED FROM YOU
One key, sir: **Gemini API key** (recommended) or OpenAI key → into `/opt/zeus-reach.env`. Everything else in this plan is code I can build the moment the key exists.

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).