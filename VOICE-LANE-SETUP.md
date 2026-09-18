# VOICE-LANE KEY SETUP RUNBOOK
## Deepgram + ElevenLabs — wiring ZEUS's conversational voice lane (18 Sep 2026)

**Status:** OPERATIONAL GUIDE · **Applies to:** flagship (zeusaiintelligence.com) Browser
**Precondition:** ZEUS flagship reachable; the activity log line
`SYS: Speech-speech: say "set deepgram key" and "set elevenlabs key", then "voice lane on"`
is the console's own instruction — this runbook follows it exactly.

---

## 1. WHAT THE VOICE LANE NEEDS

| Service | Purpose | Panel |
|---|---|---|
| **Deepgram** | speech-to-text (hear your commands) | console.deepgram.com |
| **ElevenLabs** | text-to-speech / voice agent (answer out loud) | elevenlabs.io |
| **LANGUAGE · VOICE** | flagship panel where the lane reports state | flagship settings |

The flagship's speech layer is invoked by **spoken commands** (the console told us):
"set deepgram key" → "set elevenlabs key" → "voice lane on".

---

## 2. OBTAIN THE KEYS

### 2.1 Deepgram API key
1. Open **https://console.deepgram.com** → sign in (Google works).
2. Left menu → **API Keys** → **+ Create Key**.
3. Name it `zeus-voice` → scopes: **on-demand** → Create → copy the key
   (starts with a long base64 token).
4. Keep it on your clipboard for step 3.1.

### 2.2 ElevenLabs API key
1. Open **https://elevenlabs.io** → sign in.
2. Top right avatar → **Profile + API key** → **Create API key**.
3. Name it `zeus-voice` → copy the `sk_…` key.
4. Keep it separate from the Deepgram key (they go in different slots).

---

## 3. SET THE KEYS ON THE FLAGSHIP

### 3.1 Deepgram (speech-to-text)
- On the flagship, use the **mic / voice input** and **say**:
  ```
  set deepgram key
  ```
- The console will prompt for the value → **say or paste** the Deepgram key.
- Expect the activity log to confirm the key is stored (no "missing" message).

### 3.2 ElevenLabs (text-to-speech)
- Say:
  ```
  set elevenlabs key
  ```
- Provide the ElevenLabs `sk_…` key → expect confirmation.

### 3.3 Enable the lane
- Say:
  ```
  voice lane on
  ```
- Expected: the activity log no longer shows
  `Speech-speech: say "set deepgram key"…` — it moves to an active-voice state.

---

## 4. VERIFY (green only when proven)

| # | Check | Green when |
|---|---|---|
| 1 | Activity log has no "set deepgram / elevenlabs key" prompt | both keys stored |
| 2 | Say "what's the weather in WEST MIDLANDS" | spoken answer, not "no answer to that sir" |
| 3 | Say "check estate health" | spoken summary of the estate |
| 4 | Interrupt mid-answer | conversation re-aims (voice lane live) |

## 5. TROUBLESHOOTING

| Symptom | Cause | Fix |
|---|---|---|
| "no answer to that sir" persists | keys not set OR Shield blocks the provider origin | complete 3.1–3.3; confirm allowlist has `api.elevenlabs.io` / `api.us.elevenlabs.io` (patch-zeus-fixes.py added them) |
| Key rejected | pasted whole command text | provide ONLY the key value, one line |
| Mic not activating | browser permission | allow mic access in the flagship page |
| External voice API origin blocked | Shield allowlist | re-run patch-zeus-fixes.py (v8.1 contains the +6 origins) |

## 6. SECURITY NOTES
- Keys are stored by the flagship and used for the voice lane; treat the Deepgram
  and ElevenLabs keys like passwords.
- Rotate them periodically from their consoles (Deepgram → API Keys · ElevenLabs →
  Profile + API key); update on the flagship by re-running 3.1–3.3.
- Never paste keys into chat or shared logs — the flagship accepts them via the
  voice/paste prompt, not via this document.

## 7. RELATED
- **Speech-speech note:** the console explicitly says to set both keys THEN enable
  the lane; the order matters (voice lane on without keys stays silent).
- If the voice lane still fails after keys are set, the SHIELD activity log will
  say which origin was blocked — re-run `patch-zeus-fixes.py` and reload.

---
*All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).*