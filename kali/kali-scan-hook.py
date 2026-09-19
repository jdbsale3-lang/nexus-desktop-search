#!/usr/bin/env python3
"""kali-scan-hook.py — n8n integration hook for the Kali-AEGIS container.
Called by n8n's Execute Command node. Runs an authorized estate scan with the
Slim toolset and prints JSON for n8n to parse.

Usage (host):  python3 kali-scan-hook.py <target_url> [--tool nuclei|nmap|both]
Example:       python3 kali-scan-hook.py https://zeusaiintelligence.com --tool nuclei
"""
import argparse
import json
import shutil
import subprocess
import time


def run(cmd, timeout=120):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except FileNotFoundError as e:
        return 127, "", f"tool missing: {e.filename}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--tool", choices=["nuclei", "nmap", "both"], default="nuclei")
    ap.add_argument("--timeout", type=int, default=120)
    args = ap.parse_args()

    started = time.time()
    result = {"target": args.target, "tool": args.tool, "findings": []}

    if args.tool in ("nuclei", "both") and shutil.which("nuclei"):
        code, out, err = run(["nuclei", "-u", args.target, "-silent", "-no-color",
                              "-severity", "low,medium,high,critical"], args.timeout)
        for line in (out or "").splitlines():
            if line.strip():
                result["findings"].append({"source": "nuclei", "line": line.strip()[:300]})
        result["nuclei_exit"] = code
        if err:
            result["nuclei_stderr"] = err[:300]

    if args.tool in ("nmap", "both") and shutil.which("nmap"):
        code, out, err = run(["nmap", "-sV", "-p", "80,443,8080,8443", "-T4", "--top-ports", "20", args.target], args.timeout)
        # retain open-port lines only
        for line in (out or "").splitlines():
            if line.strip().startswith(("PORT", "80/", "443/", "8080/", "8443/")):
                result["findings"].append({"source": "nmap", "line": line.strip()[:200]})
        result["nmap_exit"] = code

    result["duration_s"] = round(time.time() - started, 1)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()