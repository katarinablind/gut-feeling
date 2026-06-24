#!/usr/bin/env python3
"""Insert palette + grid core back after SEC (rebalance had deleted it)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
restore = (ROOT / "flora-restore.html").read_text().splitlines(keepends=True)
broken = (ROOT / "flora-broken.html").read_text()

start = restore.index("/* ---------- palette ---------- */\n")
end = restore.index("/* S2→S3 hold — stream stays on screen with copy cleared before the gut blooms. */\n")
chunk = "".join(restore[start:end])
chunk = chunk.replace("    resetDotStorm();\n", "")

marker = "};\n\n/* ---------- palette ---------- */"
if marker not in broken:
    raise SystemExit("marker not found in flora-broken.html")
fixed = broken.replace(marker, "};\n\n" + chunk + marker, 1)

for name in ("flora.html", "index.html"):
    (ROOT / name).write_text(fixed)
    print(f"Fixed {name} ({len(fixed.splitlines())} lines)")
