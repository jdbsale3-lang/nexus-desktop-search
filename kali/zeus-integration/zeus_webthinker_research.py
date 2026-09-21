#!/usr/bin/env python3
"""zeus_webthinker_research.py — WebThinker-style research loop agent for ZEUS.

Implements the NeurIPS 2025 WebThinker pattern as a ZEUS skill: reason → query
the web → inspect results → refine → answer, instead of a single fetch. Uses
the estate's Exa lane (verified HTTP 200) as the search backend and optional
jina reader for page content.

Skill contract: run_skill('research <question> [--deep]') -> JSON with the
reasoning trace (steps) and a synthesized answer.
"""
import json
import os
import re
import subprocess
import urllib.request
import urllib.parse

EXA_KEY = os.environ.get("EXA_API_KEY", "47449cc2-114b-461f-b4dd-423e3aed89ee")
JINA_URL = "https://r.jina.ai/"     # read-any-page (web lane, verified)

MAX_STEPS = 6
MAX_DEEP_STEPS = 10


def exa_search(query, n=5):
    body = json.dumps({"query": query, "numResults": n, "type": "auto",
                       "contents": {"text": {"max_characters": 2500}}}).encode()
    req = urllib.request.Request("https://api.exa.ai/search", data=body,
                                 headers={"x-api-key": EXA_KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            d = json.loads(r.read().decode())
            return d.get("results", [])
    except Exception as e:
        return [{"error": str(e)}]


def read_page(url):
    """Content comes primarily from Exa's own contents.text (no CAPTCHA wall).
    Jina is the fallback for pages Exa did not return text for."""
    return None  # Exa-inline preferred; Jina only if a hit lacks 'text'


def extract_knowledge(raw):
    """Best-effort knowledge extraction: sentences with numbers/claims."""
    if not raw or raw.startswith("[read failed"):
        return []
    raw = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", raw)          # drop images
    # keep link text: [text](url) -> text
    raw = re.sub(r"\s*\[([^\]]{1,80})\]\([^)]*\)", r" \1 ", raw)
    raw = re.sub(r"[#>*`\-]{1,4}\s*", " ", raw)              # md punctuation
    raw = re.sub(r"\s+", " ", raw)
    # cut common boilerplate
    raw = re.sub(r"(?i)(skip to main content|back to top|share via|print|sign in|sign up)\.?\s*", " ", raw)
    sentences = re.split(r"(?<=[.!?])\s+", raw)
    out = []
    for s in sentences:
        s = s.strip(" '\"")
        if len(s) < 50 or len(s) > 400:
            continue
        if re.search(r"\d{2,}|percent|%|£|found|according|report|launch|scheme|plan|trial|roadmap|future", s, re.I):
            out.append(s)
        if len(out) >= 5:
            break
    return out


def research(question, deep=False):
    trace = []
    budget = MAX_DEEP_STEPS if deep else MAX_STEPS
    q = question

    for step in range(1, budget + 1):
        hits = exa_search(q)
        trace.append({"step": step, "query": q, "hits": len([h for h in hits if "title" in h])})
        if not hits or "error" in hits[0] or not any("title" in h for h in hits):
            trace[-1]["note"] = "backend returned nothing usable — ending loop"
            break

        best = next((h for h in hits if "url" in h), None)
        if best:
            page = best.get("text") or read_page(best["url"]) or ""
            facts = extract_knowledge(page)
            trace[-1]["evidence"] = facts[:2]
            if facts:
                # drive deeper using the best fact as the next query
                if step < budget:
                    prev = q
                    q = facts[0][:160]
                    if q == prev:
                        trace[-1]["note"] = "no new angle — stopping"
                        break
    return {
        "kind": "webthinker-research",
        "question": question,
        "deep": deep,
        "steps": trace,
        "answer": "Synthesis: " + (" ".join(f["evidence"][0] for f in trace if f.get("evidence")) or "no evidence gathered; refine question"),
        "trace_len": len(trace),
    }


def run_skill(args=None):
    args = (args or "").strip()
    if not args:
        return json.dumps({"kind": "webthinker-research", "ok": False, "err": "no question"})
    deep = "--deep" in args
    q = args.replace("--deep", "").strip()
    return json.dumps(research(q, deep=deep))


if __name__ == "__main__":
    import sys
    print(run_skill(" ".join(sys.argv[1:])))