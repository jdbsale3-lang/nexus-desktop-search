# Kali-AEGIS Toolset Status — 2026-09-20

Authorized estate security workstation, live on aegis-api. Image `kali-aegis:1.0`
(trimmed v8+ kit), container `kali-aegis`, all scans restricted to ZEUS-owned
assets. Status column = verified via `tool-smoke-test.sh` (v11 flags).

## Core scanning (nmap layer fixed: NET_RAW + seccomp + apparmor unconfined)

| Tool | Verdict | Flags verified | Estate use |
|---|---|---|---|
| nmap | ✅ | `-V`, real scan ran (Cloudflare proxy on 80/443/8080/8443) | port/service audit |
| nuclei | ✅ | `-version` | CVE template scans |
| sqlmap | ✅ | `--version` | webapp SQLi testing |
| burpsuite | ✅ | `--version` | manual web testing |

## Exploitation & credentials

| Tool | Verdict | Verified flag | Estate use |
|---|---|---|---|
| msfconsole | ✅ | `-v` | Metasploit framework |
| searchsploit | ✅ | term search (`apache`) | exploit-db lookup |
| hashcat | ✅ | `--version` | hash cracking |
| john | ✅ | `--list=build-info` | hash cracking |
| hydra | ✅ | `-h` | login brute-force |
| responder | ✅ | `-h` | LLMNR/NBT-NS poisoning |
| impacket-psexec | ✅ | `-h` | windows lateral movement |

## Network & RE

| Tool | Verdict | Verified flag | Estate use |
|---|---|---|---|
| wireshark | ✅ | `--version` | packet capture |
| bettercap | ✅ | `-version` | MITM/network attacks |
| ghidra | ✅ | `--help` | binary RE (GUI) |
| radare2 (r2) | ✅ | `-v` | binary RE (CLI) |

## Web & recon (estate primary)

| Tool | Verdict | Verified flag | Estate use |
|---|---|---|---|
| ffuf | ✅ | `-V` | content fuzzing |
| gobuster | ✅ | `-h` | dir/dns enumeration |
| nikto | ✅ | `-Version` | webserver scan |
| wpscan | ✅ | `--version` | WordPress audit |
| subfinder | ✅ | `-version` | subdomain discovery |
| httpx | ✅ | `-h` | HTTP probing |

## Extras

| Tool | Verdict | Verified flag | Estate use |
|---|---|---|---|
| cheat | ✅ | `-v` | command cheatsheets |

**Result: 22/22 tools execute. All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).**