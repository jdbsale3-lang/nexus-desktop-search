# ZEUS AI Upgrade Report — Deep GitHub Search
**Date:** 2026-09-21 · Every repo verified live on GitHub (stars current at search time) · Evidence-based, no assumptions.

---

## 0. The goal
Upgrade ZEUS across six lanes: **memory · design · development · intelligence · speed · PhD-level agents.** Repos below are ranked by stars and fit for the ZEUS estate (single-file flagship, agent-reach bridge, /opt/zeus-skills engine).

---

## 1. MEMORY LANE — persistent agent memory

| Repo | Stars | What it gives ZEUS | Verdict |
|---|---|---|---|
| **Gentleman-Programming/engram** | 6,738 (Go) | Agent-agnostic persistent memory system — long-term facts, sessions, embeddings; drop-in for coding agents | **TOP PICK — wire as the bridge memory backend** (replaces flat memory.json) |
| **doobidoo/mcp-memory-service** | 1,952 (Python) | Open-source persistent memory for agent pipelines (LangChain-era but MCP-served) | good — MCP-native, drop-in behind /reach |
| **NirDiamant/Agent_Memory_Techniques** | 1,069 (notebooks) | 30 runnable notebooks covering every agent-memory technique | **tRAINING GRID** — steers which memory pattern ZEUS inscribes |
| **swarmclawai/swarmvault** | 695 (TS) | Local-first LLM Wiki: knowledge-graph memory builder | alt graph store for the flagship |
| **DeusData/codebase-memory-mcp** | 43,950 (C) | **already installed** — flagship indexed 340 nodes / 923 edges | keep (proven) |

**Action:** adopt engram as the memory layer; keep codebase-memory-mcp as code-graph memory.

## 2. DESIGN LANE — brand / product design assets

| Repo | Stars | Fit for ZEUS |
|---|---|---|
| **Gentleman-Programming/gentle-ai** | 7,092 (Go) | Configures the AI coding agents you already use (Claude/Cursor/etc.) — consistent tooling design |
| **ai-boost/awesome-harness-engineering** | 4,407 (list) | **already in /opt/zeus-agents** — orchestration/memory/design patterns catalogue |

**Action:** gentle-ai unifies agent configuration; harness list already local.

## 3. DEVELOPMENT LANE — agent dev workflows

| Repo | Stars | What it gives |
|---|---|---|
| **deepset-ai/haystack** | 26,569 (Python) | Open-source orchestration framework — pipelines, retrievers, agents; the industry-standard dev backbone |
| **microsoft/agent-framework** | 13,679 (Python) | Official framework for building/orchestrating/deploying agents — batteries-included |
| **omnigent-ai/omnigent** | 10,131 (Python) | Meta-harness for agent frameworks — run agents across providers |

**Action:** haystack as the pipeline layer for new ZEUS skills; agent-framework as the multi-agent spine when ZEUS grows beyond single-file.

## 4. INTELLIGENCE LANE — search / research / knowledge

| Repo | Stars | Fit |
|---|---|---|
| **RUC-NLPIR/WebThinker** | 1,468 (Python) | NeurIPS 2025 — WebThinker: large reasoning model with live web interaction → ZEUS research becomes *reasoning-over-the-web* |
| **DavidZWZ/Awesome-Deep-Research** | 864 (list) | ACL 2026 curated deep-research resources — the map of the lane |
| **heurist-network/heurist-agent-framework** | 826 (Python) | Multi-interface agent framework — parallel research + multiple LLM surfaces |

**Action:** WebThinker upgrade path for the research skill (current: Exa-first fetch; future: reasoning loop over results).

## 5. SPEED LANE — inference / serving

| Repo | Stars | Fit |
|---|---|---|
| **vllm-project/vllm** | 92,323 (Python) | High-throughput, memory-efficient inference & serving — the industry standard |
| **jmaczan/tiny-vllm** | 1,125 (C++) | Build-your-own high-performance engine — learning reference |
| **pegainfer-project/pegainfer** | 705 (Rust) | Pure Rust + CUDA inference, no PyTorch — edge deployment path |

**Action (honest):** vllm is for *hosting* a model — ZEUS currently calls hosted platforms. Keep on the radar: if ZEUS ever self-hosts a small model, vllm is the serving layer. Speed gains *today* come from the memory + orchestration lanes (fewer redundant calls).

## 6. PhD-LEVEL AGENT LANE — scientific method / lab-grade agents

| Repo | Stars | Fit |
|---|---|---|
| **K-Dense-AI/scientific-agent-skills** | 45,766 | **already installed** — 1,269 skills; turn ZEUS into an AI scientist |
| **mukul975/Anthropic-Cybersecurity-Skills** | 33,036 | **already installed** — 817 cybersecurity skills |
| **open-agent-science/autonomous-physics-lab** | 4 (Python) | Open agent network for reproducible research — agents design/run/verify experiments |
| **mehdiforoozandeh/crux** | 6 (Python) | Scientific-method lab notebook an AI agent drives — research life-cycle (hypothesis → verify) |

**Action (honest):** the two big PhD-level packs are already in `/opt/zeus-agents` (verified this session). The remaining two are tiny; crux's hypothesis→verify loop is the interesting pattern — build that loop into the research skill regardless of repo size.

---

## 7. Recommended upgrade plan (ranked)

| Priority | Lane | Repo(s) | Effort |
|---|---|---|---|
| P0 | Memory | **engram** (6.7K) | medium — replaces flat memory.json backend |
| P0 | Intelligence | **WebThinker** pattern (1.4K) | medium — research skill upgrade |
| P1 | Development | **haystack** (26K) | large — pipeline backbone for new skills |
| P1 | Memory techniques | **Agent_Memory_Techniques** (1K) | small — training grid for what ZEUS inscribes |
| P2 | Orchestration | **microsoft/agent-framework** (13.6K) | large — multi-agent spine |
| P2 | Speed | **vllm** (92K) — only if self-hosting | conditional |
| P3 | Scientific loop | **crux** pattern (hypothesis→verify) | small — fold into research skill |

**Already aboard (verified):** codebase-memory-mcp · scientific-agent-skills · Anthropic-Cybersecurity-Skills · awesome-harness-engineering.

---

All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).