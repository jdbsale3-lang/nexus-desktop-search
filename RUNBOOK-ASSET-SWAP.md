# Release Asset Swap — Runbook (v2.4.0)

Fixes a published release carrying duplicate or stale zip assets. Verified state 15 Sep 2026: release v2.4.0 published with a single correct asset (nexus-desktop-search zip, SHA 0088d68bab51135b41d582b581712b5377dc60a4839ff94835e9944af43c15c9, 144,164 B). If you ever see two assets or a wrong SHA, do this:

1. Open the release page and click Edit (pencil icon).
2. Remove every stale asset (click the x on each row) — the Assets list must be empty.
3. On your PC: download the verified zip and check the hash:
   curl -L -o nexus-desktop-search.zip <your-latest-release-url>
   Get-FileHash nexus-desktop-search.zip -Algorithm SHA256 | fl
4. Drag the cleanly named zip onto the Attach binaries box, keep "Latest" selected, click Update release.
5. Verify via API: curl -s https://api.github.com/repos/jdbsale3-lang/nexus-desktop-search/releases/latest — expect one asset, correct name, correct size.

Note: browsers auto-rename duplicate downloads (e.g. .6.zip). Rename to nexus-desktop-search.zip with F2 before dragging. All IP belongs to Darren Birch — ZEUSTRUSTAEGISSECURITY LTD.