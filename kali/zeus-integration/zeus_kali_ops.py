"""zeus_kali_ops — ZEUS skills engine module: Kali/Linux workstation control.

Wire-in for the ZEUS flagship skills engine (zeus-skills.py style).
Run: python3 zeus_kali_ops.py run <command>   (or via loader "entry": "run_skill")
Commands:
  status        -> container + image + health (docker ps / images on the host)
  scan <target> -> kali-scan-hook.py nuclei,nmap against an authorized target
  tooltest      -> tool-smoke-test.sh inside the container
  mcpindex      -> codebase-memory-mcp index_repository on the flagship
  launch        -> docker exec -it kali-aegis bash (message only; interactive)
Authorized asset note: scans are restricted to ZEUS-owned estate targets.
"""
import json
import shutil
import subprocess


def _sh(cmd, timeout=60):
    try:
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return {"ok": p.returncode == 0, "out": (p.stdout or "")[-1200:], "err": (p.stderr or "")[-500:]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "out": "", "err": "timeout"}


def cmd_status():
    r = _sh("docker ps --filter name=kali-aegis --format '{{.Names}} {{.Status}}' && docker images kali-aegis:1.0 --format '{{.Repository}}:{{.Tag}} {{.Size}}'")
    return {"kind": "kali-status", **r}


def cmd_scan(target):
    r = _sh(f"docker exec kali-aegis bash -c \"python3 /aegis/work/kali/kali-scan-hook.py {target} --tools nuclei,nmap\"", 300)
    return {"kind": "kali-scan", "target": target, **r}


def cmd_tooltest():
    r = _sh("docker exec kali-aegis bash -c \"bash /aegis/work/kali/tool-smoke-test.sh\"", 300)
    return {"kind": "kali-tooltest", **r}


def cmd_mcpindex():
    r = _sh("codebase-memory-mcp cli index_repository --repo-path /var/www/zeusaiintelligence.com", 300)
    return {"kind": "kali-mcpindex", **r}


def cmd_launch():
    return {"kind": "kali-launch", "ok": True, "out": "Run interactively: docker exec -it kali-aegis bash"}


HANDLERS = {
    "status": cmd_status,
    "scan": cmd_scan,
    "tooltest": cmd_tooltest,
    "mcpindex": cmd_mcpindex,
    "launch": cmd_launch,
}


def run_skill(args=None):
    args = args or "status"
    parts = str(args).split()
    cmd = parts[0] if parts and parts[0] in HANDLERS else "status"
    rest = " ".join(parts[1:])
    if cmd == "scan" and not rest:
        rest = "https://zeusaiintelligence.com"
    return json.dumps(HANDLERS[cmd](rest) if cmd == "scan" else HANDLERS[cmd]())


if __name__ == "__main__":
    import sys
    print(run_skill(" ".join(sys.argv[1:])))