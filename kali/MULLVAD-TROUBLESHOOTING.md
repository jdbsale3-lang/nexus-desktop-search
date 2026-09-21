# Mullvad VPN — Troubleshooting & Checklist (24/7 protection)
Companion to the PC setup checklist. If VPN or the browser misbehaves, run these in order.

## Symptom → Fix table

| Symptom | Likely cause | Fix |
|---|---|---|
| **"You are not protected" at mullvad.net/en/check** | VPN not connected / wrong link | Open Mullvad → Select location → Connect → re-check |
| **VPN says connected but check shows home IP** | Kill switch off / other VPN leak | Settings → **Kill switch: ON** → reconnect → re-check |
| **Site blocked or slow** | that location is congested/blocked | **Switch Location** (e.g. UK → Germany), keep VPN on |
| **Auto-connect not firing at boot** | toggle off / admin permissions | Settings → **Auto-connect on startup: ON** → run app as admin once |
| **Can't log into x.com in Mullvad Browser** | Mullvad exit conflicts with site | switch location; log in; keep VPN on; or add site to Mullvad Browser's per-site settings |
| **Twitter cookies fail right after export** | cookies expired / session rotated | re-login x.com, re-export fresh `auth_token`+`ct0` within the same session |
| **Mullvad Browser won't start** | install interrupted / permissions | re-run installer; run as admin; check Windows SmartScreen override |
| **No Mullvad icon in tray** | app exited | relaunch from Start menu; verify tray icon (right-click → Connect) |
| **"Account number not recognised"** | wrong digits / typo | recheck the 16 digits from your welcome email; mullvad.net → Account
| **PC wakes from sleep, VPN off** | auto-reconnect gap | Settings → **Connect on startup** + **Reconnect on network change: ON** |

## Daily checklist (30 seconds)
- [ ] Tray icon shows Mullvad running
- [ ] mullvad.net/en/check → green "You are protected"
- [ ] IP ≠ your home IP
- [ ] Mullvad Browser opened with VPN on (when browsing estate/X work)

## When All Else Fails
1. `Settings → Disconnected` → reconnect fresh.
2. Restart Mullvad app (right-click tray → Quit → relaunch).
3. Restart the PC — auto-connect re-engages.
4. Fresh re-export of Twitter cookies in a NEW session (old ones die).

---
All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD (administered by the Darren & Jill Birch Trust).