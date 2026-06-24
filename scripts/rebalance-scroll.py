#!/usr/bin/env python3
"""Rebalance scroll: Maddi ~42% progress / team ~58%, with full main S3+ copy + timings."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOTAL_VH = 22
LATE_START = 0.42
MAIN_ORIGIN = 0.448
MAIN_SPAN = 1.0 - MAIN_ORIGIN
LATE_SPAN = 1.0 - LATE_START
OLD_MADDI_END = 0.903
MADDI_SCALE = LATE_START / OLD_MADDI_END

S2_S3_GAP = 0.075 * MADDI_SCALE
S1_DUR = (0.395 - 0.075) * MADDI_SCALE
S2_DUR = 0.203 * MADDI_SCALE
S0_END = 0.305 * MADDI_SCALE
S1_START = S0_END
S1_END = S1_START + S1_DUR
S2_START = S1_END
S2_END = LATE_START - S2_S3_GAP


def remap_main(p: float) -> float:
    return round(LATE_START + (p - MAIN_ORIGIN) * (LATE_SPAN / MAIN_SPAN), 3)


def scale_maddi(p: float) -> float:
    return round(p * MADDI_SCALE, 3)


def remap_copy_block(main_html: str) -> str:
    m = re.search(r"<!-- S3 -->.*<!-- S6 -->.*?</div>\s*\n", main_html, re.DOTALL)
    if not m:
        raise RuntimeError("S3–S6 block missing in flora-main-ref.html")
    block = m.group(0).replace("<!-- S3 -->", "    <!-- S3 — Catherine -->", 1)

    def repl_attr(match: re.Match[str]) -> str:
        attr, val = match.group(1), float(match.group(2))
        return f'data-{attr}="{remap_main(val)}"'

    block = re.sub(r'data-(in|out)="([\d.]+)"', repl_attr, block)
    block = block.replace('class="t lg"', 'class="t lg work"')
    block = block.replace('class="t md"', 'class="t md work"')
    return block


def scale_maddi_copy(html: str) -> str:
    start = html.index("    <!-- S0 — landing -->")
    end = html.index("    <!-- S3 — Catherine -->")
    head, maddi, tail = html[:start], html[start:end], html[end:]

    def repl_attr(match: re.Match[str]) -> str:
        attr, val = match.group(1), float(match.group(2))
        return f'data-{attr}="{scale_maddi(val)}"'

    maddi = re.sub(r'data-(in|out)="([\d.]+)"', repl_attr, maddi)
    return head + maddi + tail


def main() -> None:
    main_flora = (ROOT / "flora-main-ref.html").read_text()
    text = (ROOT / "flora.html").read_text()

    text = scale_maddi_copy(text)

    s3_block = remap_copy_block(main_flora)
    text = re.sub(
        r"    <!-- S3 — Catherine -->.*?    <!-- S6 -->.*?</div>\s*\n",
        s3_block,
        text,
        count=1,
        flags=re.DOTALL,
    )

    sec_block = f"""/* S2→S3 hold — stream stays on screen with copy cleared before the gut blooms. */
const S2_S3_GAP = {round(S2_S3_GAP, 4)};
const S1_DUR = {round(S1_DUR, 4)};
const S2_DUR = {round(S2_DUR, 4)};
const SEC = {{
  /* Maddi S0–S2 — compressed to [0, LATE_START) so Catherine/Katarina own the rest. */
  s0:[0, {round(S0_END, 4)}],
  s1:[{round(S1_START, 4)}, {round(S1_END, 4)}],
  s2:[{round(S2_START, 4)}, {round(S2_END, 4)}],
}};"""

    text = re.sub(r"const TOTAL_VH = \d+;", f"const TOTAL_VH = {TOTAL_VH};", text, count=1)
    text = re.sub(
        r"/\* S2→S3 hold[\s\S]*?const SEC = \{[\s\S]*?\};",
        sec_block,
        text,
        count=1,
    )
    # Ensure LATE_START / S3_START live next to TOTAL_VH
    if "const LATE_START" not in text.split("const SEC")[0]:
        text = text.replace(
            f"const TOTAL_VH = {TOTAL_VH};",
            f"const TOTAL_VH = {TOTAL_VH};\nconst LATE_START = {LATE_START};\nconst S3_START = LATE_START;",
            1,
        )

    text = re.sub(
        r"const LATE_START = [\d.]+;\nconst MAIN_ORIGIN = [\d.]+;\nfunction toMainP\(p\) \{[\s\S]*?\}",
        f"""const MAIN_ORIGIN = {MAIN_ORIGIN};
const LATE_SPAN = {LATE_SPAN};
const MAIN_SPAN = {MAIN_SPAN};
function toMainP(p) {{
  if (p < LATE_START) return MAIN_ORIGIN;
  return MAIN_ORIGIN + (p - LATE_START) / LATE_SPAN * MAIN_SPAN;
}}""",
        text,
        count=1,
    )

    # Journey rail — team sections spread across second half of scroll
    journey = f"""  const JOURNEY_KEYS = [
    {{ p: 0,            j: 0    }},
    {{ p: SEC.s0[1],    j: 0.14 }},
    {{ p: SEC.s1[1],    j: 0.30 }},
    {{ p: SEC.s2[1],    j: 0.44 }},
    {{ p: {remap_main(0.60)}, j: 0.58 }},
    {{ p: {remap_main(0.82)}, j: 0.74 }},
    {{ p: {remap_main(0.92)}, j: 0.88 }},
    {{ p: 1,            j: 1    }},
  ];"""
    text = re.sub(
        r"  const JOURNEY_KEYS = \[[\s\S]*?\];",
        journey,
        text,
        count=1,
    )

    bg = f"""const BG_KEYS = [
  {{ p: 0.00, c: [252, 253, 254] }},
  {{ p: {round(LATE_START - 0.02, 3)}, c: [252, 253, 254] }},
  {{ p: {remap_main(0.60)}, c: [252, 253, 254] }},
  {{ p: {remap_main(0.70)}, c: [158, 165, 158] }},
  {{ p: {remap_main(0.82)}, c: [188, 200, 178] }},
  {{ p: {remap_main(0.93)}, c: [218, 232, 208] }},
  {{ p: 1.00, c: [252, 253, 254] }},
];"""
    text = re.sub(
        r"const BG_KEYS = \[[\s\S]*?\];",
        bg,
        text,
        count=1,
    )

    for name in ("flora.html", "index.html"):
        (ROOT / name).write_text(text)
        print(f"Wrote {name} — TOTAL_VH={TOTAL_VH}, LATE_START={LATE_START}")
        print(f"  Maddi scroll ≈ {LATE_START * TOTAL_VH:.1f}vh, team ≈ {LATE_SPAN * TOTAL_VH:.1f}vh")


if __name__ == "__main__":
    main()
