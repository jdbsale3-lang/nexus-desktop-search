# Wire Kali/MCP/Personas into ZEUS — install guide

Everything in `zeus-integration/` is the official ZEUS upgrade payload:
- `zeus_kali_ops.py`   — skills-engine module (status / scan / tooltest / mcpindex / launch)
- `ZEUS-KALI-BRIEFING.md` — load into ZEUS memory/context so ZEUS knows Linux exists
- this file — the exact install steps

All commands run on the DROPLET HOST (root@aegis-api), except where noted.

## 1. Kit (already on host if you pulled k12; k13 adds zeus-integration)
```bash
cd ~ && curl -sL -o k13.zip "<KIT13_URL>" && unzip -o k13.zip
```
## 2. Drop the skill module into ZEUS
```bash
# ZEUS skills engine lives in the flagship web root (adjust path to your layout)
cp ~/kali/zeus-integration/zeus_kali_ops.py /var/www/zeusaiintelligence.com/skills/ 2>/dev/null \
  || cp ~/kali/zeus-integration/zeus_kali_ops.py /opt/zeus/skills/ 2>/dev/null
# register in the skills index (zeus-skills.py): add an entry pointing at zeus_kali_ops
grep -q zeus_kali_ops /var/www/zeusaiintelligence.com/zeus-skills.py 2>/dev/null \
  || echo "// add {'name':'kali_ops','entry':'zeus_kali_ops'} to the skills list" >> ~/kali/zeus-integration/REGISTER-NOTE.txt
```
## 3. Load the briefing into ZEUS memory
```bash
cp ~/kali/zeus-integration/ZEUS-KALI-BRIEFING.md /var/www/zeusaiintelligence.com/docs/ 2>/dev/null || true
# then: say "load the kali briefing" — or paste ZEUS-KALI-BRIEFING.md into ZEUS memory
```
## 4. Verify wiring
```bash
cd ~/kali && python3 zeus-integration/zeus_kali_ops.py status
# expect JSON: kind=kali-status ok=true with container Up and image ~5GB
```
## 5. Smoke test — INSIDE the container (tools live there, not the host)
```bash
docker exec kali-aegis bash -c "bash /aegis/work/kali/tool-smoke-test.sh"
# expect: ALL TOOLS EXECUTE — 22/22
```
---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).