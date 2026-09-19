#!/usr/bin/env python3
"""kali-scan-hook.py — n8n integration hook for the Kali-AEGIS container (v2).
Runs authorized estate scans (nuclei, nmap, wpscan, nikto, ffuf, httpx) and
returns a parsed JSON object n8n can route. Adding tools = add a branch below.

Usage:
  python3 kali-scan-hook.py <target_url> --tools nuclei,nmap,wpscan
  python3 kali-scan-hook.py https://zeusaiintelligence.com --tools all
"""
import argparse
import json
import shutil
import subprocess
import time


def run(cmd, timeout=150):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except FileNotFoundError as e:
        return 127, "", f"tool missing: {e.filename}"


TOOLS = {
    "nuclei": {
        "args": lambda t: ["nuclei", "-u", t, "-silent", "-no-color",
                           "-severity", "low,medium,high,critical"],
        "parse": lambda out: [l.strip()[:300] for l in out.splitlines() if l.strip()],
    },
    "nmap": {
        "args": lambda t: ["nmap", "-sV", "-T4", "--top-ports", "40", "-Pn", t],
        "parse": lambda out: [l.strip() for l in out.splitlines()
                              if re.match(r"^\d+/tcp", l.strip())][:20],
    },
    "wpscan": {
        "args": lambda t: ["wpscan", "--url", t, "--no-banner", "--no-color",
                           "--disable-tls-checks"],
        "parse": lambda out: [l.strip() for l in out.splitlines()
                              if any(k in l for k in ("[!]", "[+]", "Interesting"))][:25],
    },
    "nikto": {
        "args": lambda t: ["nikto", "-h", t, "-nointeractive", "-Tuning", "x"],
        "parse": lambda out: [l.strip() for l in out.splitlines()
                              if "+" in l or "OSVDB" in l][:25],
    },
    "ffuf": {
        "args": lambda t: ["ffuf", "-u", f"{t}/FUZZ", "-w",
                           "/usr/share/wordlists/dirb/common.txt",
                           "-mc", "200,204,301,302,403", "-s", "-t", "20"],
        "parse": lambda out: [l.strip() for l in out.splitlines() if l.strip()][:30],
    },
    "httpx": {
        "args": lambda t: ["httpx", "-u", t, "-sc", "-title", "-silent"],
        "parse": lambda out: [l.strip()[:200] for l in out.splitlines() if l.strip()][:10],
    },
}


def scan(target, tool, timeout):
    spec = TOOLS[tool]
    if not shutil.which(tool):
        return {"tool": tool, "status": "missing", "findings": []}
    code, out, err = run(spec["args"](target), timeout)
    return {"tool": tool, "status": "ok" if code == 0 else f"exit:{code}",
            "findings": spec["parse"](out or "")}


def main():
    import re  # used by parse lambdas above

    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--tools", default="nuclei,nmap",
                    help="comma list or 'all' (nuclei,nmap,wpscan,nikto,ffuf,httpx)")
    ap.add_argument("--timeout", type=int, default=150)
    args = ap.parse_args()

    tools = list(TOOLS) if args.tools == "all" else \
        [t.strip() for t in args.tools.split(",") if t.strip() in TOOLS]

    started = time.time()
    results = [scan(args.target, t, args.timeout) for t in tools]
    payload = {
        "target": args.target,
        "scan_time_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "duration_s": round(time.time() - started, 1),
        "tools_run": tools,
        "results": results,
        "findings_total": sum(len(r["findings"]) for r in results),
        "verdict": "REVIEW" if any(r["findings"] for r in results) else "CLEAN",
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()