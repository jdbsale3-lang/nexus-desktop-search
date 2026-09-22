#!/usr/bin/env python3
"""locale-en-fix.py — render the agent-reach channel catalogue in ENGLISH.

The zh-CN display names come from the agent-reach CLI's own catalogue
(e.g. "B站视频、字幕和搜索"). We cannot edit a compiled/market build's strings,
but we CAN translate them at the bridge egress: this patch wraps the bridge's
`_send()` so every JSON payload is localised before it leaves the process —
route-agnostic, so it covers /doctor, /self, /platform, /skills and any future
route. Any value that is not a known channel name is passed through untouched.

Idempotent · backup-first · compile-verified · fixture-tested.

Usage (droplet): python3 locale-en-fix.py
"""
import shutil
from pathlib import Path

TARGET = "/opt/agent-reach-bridge.py"
BAK = TARGET + ".bak-locale-en"

LOCALISER = '''
# === ZEUS-LOCALE-EN (render the channel catalogue in English at egress) ===
_ZH_NAME_EN = {
    "twitter": "Twitter/X posts",
    "youtube": "YouTube videos & subtitles",
    "bilibili": "Bilibili videos, subtitles & search",
    "linkedin": "LinkedIn professional network",
    "v2ex": "V2EX nodes, topics & replies",
    "xueqiu": "Xueqiu stock quotes & community",
    "rss": "RSS/Atom feeds",
    "exa_search": "Exa web search",
    "web": "Any web page",
    "reddit": "Reddit posts & comments",
    "facebook": "Facebook posts, pages & groups",
    "instagram": "Instagram users, pages & posts",
    "xiaohongshu": "Xiaohongshu notes",
    "boss": "Boss Zhipin job search & JDs",
    "xiaoyuzhou": "Xiaoyuzhou podcast transcription",
    "github": "GitHub search",
}
def _has_han(s):
    try:
        return any('\\u4e00' <= c <= '\\u9fff' for c in str(s))
    except Exception:
        return False
def _localize_names(obj):
    """Replace Han-containing display names with English (by channel id)."""
    if isinstance(obj, dict):
        ch = obj.get("channel")
        nm = obj.get("name")
        if isinstance(nm, str) and _has_han(nm) and ch in _ZH_NAME_EN:
            obj["name"] = _ZH_NAME_EN[ch]
        for v in obj.values():
            _localize_names(v)
    elif isinstance(obj, list):
        for v in obj:
            _localize_names(v)
    return obj
'''


def main():
    p = Path(TARGET)
    if not p.exists():
        print(f"!! {TARGET} not found"); return 1
    src = p.read_text(encoding="utf-8", errors="replace")
    if "ZEUS-LOCALE-EN" in src:
        print("  locale-en already wired — verify only")
        compile(src, TARGET, "exec")
        return 0

    # anchor 1: the _send method definition inside the Handler class
    anchor_send = '    def _send(self, obj, status=200, content_type="application/json"):'
    if anchor_send not in src:
        print("!! _send anchor not found"); return 3

    # anchor 2: the class line for module-scope injection
    anchor_cls = "class Handler(BaseHTTPRequestHandler):"
    if anchor_cls not in src:
        print("!! class Handler anchor not found"); return 4

    shutil.copy(TARGET, BAK)

    # 1) module-scope localiser (before the class)
    src = src.replace(anchor_cls, LOCALISER.strip("\n") + "\n\n" + anchor_cls, 1)

    # 2) localise inside _send, right after the body is computed
    old_body = '        body = obj if isinstance(obj, bytes) else json.dumps(obj).encode()'
    new_body = ('        obj = _localize_names(obj)\n'
                '        body = obj if isinstance(obj, bytes) else json.dumps(obj).encode()')
    if old_body in src:
        src = src.replace(old_body, new_body, 1)
    else:
        # fallback anchor: insert as the first statement of _send
        old_alt = anchor_send + "\n"
        src = src.replace(old_alt, anchor_send + "\n        obj = _localize_names(obj)\n", 1)

    try:
        compile(src, TARGET, "exec")
    except SyntaxError as e:
        shutil.copy(BAK, TARGET)
        print(f"!! syntax error ({e}) — restored backup"); return 5

    p.write_text(src, encoding="utf-8")
    print(f"  LOCALE-EN WIRED into {TARGET} (backup {BAK})")
    print(f"  {len(_map_len())} channel names mapped to English")
    return 0


def _map_len():
    import re
    m = re.search(r"_ZH_NAME_EN = \{(.*?)\}", LOCALISER, re.S)
    return re.findall(r'"[a-z_]+":', m.group(1))


if __name__ == "__main__":
    raise SystemExit(main())