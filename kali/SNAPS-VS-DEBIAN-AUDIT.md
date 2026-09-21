# SNAPS vs DEBIAN PACKAGES — Full Audit for the ZEUS Kali-AEGIS Programme
**Date:** 2026-09-21 · **Context:** the estate Linux workstation (Kali-AEGIS container) runs Debian-native packages today. Decision question: adopt snaps, stay .deb, or mix?

---

## 1. What each actually is

| | **Snap** | **Debian package (.deb)** |
|---|---|---|
| Packager | Canonical (Ubuntu) | Debian project / Kali team |
| Distribution | Snap Store (Canonical-run) | apt repositories (deb.debian.org, kali.download) |
| Install | `snap install <name>` | `apt install <name>` |
| Runtime | SquashFS loop-mounted + confinement daemon (snapd) | Native binaries, standard filesystem |
| Updating | Auto-updates by default (unattended) | Explicit `apt upgrade` (controlled) |
| Sandbox | Yes — AppArmor confinement per snap | No sandbox (standard Linux privileges) |

## 2. Audit scores for the ZEUS programme (security workstation)

| Criterion | Snap | .deb | Verdict for Kali-AEGIS |
|---|---|---|---|
| **Safety / supply chain** | Store is single-vendor (Canonical); audit trail decent but centralised | apam signed with Debian/Kali keys, mirrors auditable | **.deb wins** — Debian/Kali security teams are the model for trackable trust |
| **Control over updates** | Auto-update on by default — a security tool can change mid-engagement | Explicit apt upgrade — you decide when | **.deb wins decisively** for a security lab: no silent tool drift |
| **Raw capability** | Confinement blocks raw sockets/caps unless "classic" confinement (often not available) | Native privileges — nmap, wireshark, metasploit, responder work as-is | **.deb wins** — our 22 verified tools need exactly this |
| **Speed** | Loop-mounted squashfs + daemon — slower cold start | Native, instant | **.deb wins** |
| **Disk footprint** | Each snap carries full deps — duplicates | Shared library deps via apt | **.deb wins** (the droplet's 47 GB matters) |
| **Kali compatibility** | Kali does NOT ship snaps; most Kali tools have no snap at all | Kali IS Debian — every tool ships as .deb | **.deb wins absolutely** — snaps barely exist in Kali |
| **Offline/air-gap** | Snap store required at runtime for updates | apt works offline once mirrored | **.deb wins** for estate isolation |

## 3. The one honest use-case where snaps are better

Snaps shine for **desktop GUI apps needing auto-update** (browsers, editors, media apps) and for Canonical-maintained app distribution on stock Ubuntu. On a Kali security workstation serving the estate, none of that applies.

## 3b. Bonus comparator: Flatpak

| Criterion | Flatpak | .deb | Verdict for ZEUS |
|---|---|---|---|
| Vendor | Freedesktop/Flathub (community) | Debian/Kali | .deb — Flatpak is community-curated, no formal security SLA |
| Sandbox | Bubblewrap confinement, portal-based | native | .deb — sandbox blocks raw-socket tooling |
| Runtime model | Bundled runtimes per app (big) | shared libs | .deb — droplet disk matters |
| Update control | Explicit (flatpak update) | explicit (apt) | tie |
| Kali compatibility | Some apps on Flathub; no Kali-native security tools | everything | .deb absolutely |
| Speed | LAN/runtime indirection | native | .deb |
| GUI desktop apps | strong (GNOME/KDE ecosystem) | also strong | tie — but irrelevant for headless estate |

**Flatpak verdict:** same conclusion as snaps — a fine desktop-app format (Firefox, editors) for a workstation with spare disk, **wrong choice for Kali-AEGIS** where raw sockets, native speed, and Debian/Kali signature trust rule. No flatpak in the estate; single-source apt stands.

## 4. Recommendation — ZEUS Kali-AEGIS

**Stay 100% Debian-native (.deb / apt). Do not install snapd or flatpak on the droplet or in the image.**

Rationale, in one line: every estate requirement — controlled upgrades, raw-socket tools, small disk, offline-safety, Kali ecosystem identity — is satisfied by .deb and contradicted by snaps. The build, CI, and toolset are all scenario-tested on .deb already (22/22 tools verified). Introducing snaps would add a second package manager, auto-update risk, and confinement friction for zero estate gain.

**Guardrail:** pin this in the KALI-RUNBOOK — `apt` is the single package source; snapd remains uninstalled.

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).