#!/usr/bin/env python3
"""register-into-zeus.py — safe one-shot registration of zeus_kali_ops into
/opt/zeus-skills.py. Backs up first; line-based insertion so output is always
valid Python; only writes when exactly one anchor line for 'estate_status' is
found; otherwise prints context and exits 3 without writing."""
import shutil
import sys

TARGET = "/opt/zeus-skills.py"
BAK = TARGET + ".bak-kali"
NEW = "zeus_kali_ops"

lines = open(TARGET).read().splitlines(keepends=True)
anchor_idx = [i for i, ln in enumerate(lines) if "'estate_status'" in ln or '"estate_status"' in ln]

if len(anchor_idx) != 1:
    sys.stderr.write(f"ANCHOR_AMBIGUOUS matched={len(anchor_idx)} — no write. Context:\n")
    for i in anchor_idx[:3]:
        sys.stderr.write("  " + lines[i].rstrip("\n") + "\n")
    sys.exit(3)

i = anchor_idx[0]
anchor = lines[i].rstrip("\n")
is_dict = ":" in anchor.split("estate_status", 1)[1] if "estate_status" in anchor else False

indent = anchor[: len(anchor) - len(anchor.lstrip())]
is_list = not is_dict

if is_list:
    # ensure the anchor line ends with a comma so appending is always valid
    if not anchor.rstrip().endswith(","):
        lines[i] = anchor + ",\n"
    new_line = f"{indent}'{NEW}',\n"
else:
    new_line = f"{indent}'{NEW}': run_skill,\n"

lines.insert(i + 1, new_line)
result = "".join(lines)

# safety: the modified file must still compile
try:
    compile(result, TARGET, "exec")
except SyntaxError as e:
    sys.stderr.write(f"REFUSED: produced invalid syntax ({e}). No write.\n")
    sys.exit(4)

shutil.copy(TARGET, BAK)
open(TARGET, "w").write(result)
print(f"REGISTERED {NEW} -> {TARGET} (backup: {BAK})")