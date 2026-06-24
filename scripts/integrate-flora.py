#!/usr/bin/env python3
"""Graft main's S3+ timeline + motion onto Maddi's S0–S2 index.html."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATE_START = 0.903
MAIN_ORIGIN = 0.448
MAIN_SPAN = 1.0 - MAIN_ORIGIN
LATE_SPAN = 1.0 - LATE_START


def remap_main(p: float) -> float:
    return round(LATE_START + (p - MAIN_ORIGIN) * (LATE_SPAN / MAIN_SPAN), 3)


def remap_copy_block(main_html: str) -> str:
    """S3–S6 copy from main with remapped data-in/out and original layout."""
    m = re.search(r"<!-- S3 -->.*<!-- S6 -->.*?</div>\s*\n", main_html, re.DOTALL)
    if not m:
        raise RuntimeError("Could not find S3–S6 copy block in main flora.html")
    block = m.group(0)
    block = block.replace("<!-- S3 -->", "    <!-- S3 — Catherine -->", 1)

    def repl_attr(match: re.Match[str]) -> str:
        attr, val = match.group(1), float(match.group(2))
        return f'data-{attr}="{remap_main(val)}"'

    block = re.sub(r'data-(in|out)="([\d.]+)"', repl_attr, block)
    # Keep Maddi's work class on narrative lines
    block = block.replace('class="t lg"', 'class="t lg work"')
    block = block.replace('class="t md"', 'class="t md work"')
    return block


def trim_maddi_sec(text: str) -> str:
    """Keep only Maddi's s0–s2 in SEC; S3+ uses MAIN_SEC."""
    pattern = re.compile(
        r"(const SEC = \{.*?s2:\[[^\]]+\],)\s*\n\s*s3a:.*?\n\};",
        re.DOTALL,
    )
    replacement = r"\1\n};"
    out, n = pattern.subn(replacement, text, count=1)
    if n != 1:
        raise RuntimeError("Failed to trim Maddi SEC block")
    return out


def main() -> None:
    index_path = ROOT / "index.html"
    main_flora = (ROOT / "flora-main-ref.html").read_text()
    text = index_path.read_text()
    main_script = main_flora.split("<script>", 1)[1].rsplit("</script>", 1)[0]

    s3_block = remap_copy_block(main_flora)

    # Replace S3–S6 copy
    text = re.sub(
        r"    <!-- S3 — Catherine -->.*?    <!-- S6 -->.*?</div>\s*\n",
        s3_block,
        text,
        count=1,
        flags=re.DOTALL,
    )

    text = trim_maddi_sec(text)
    text = text.replace("SEC.s3a[0]", "S3_START")

    # Late engine from main (Catherine S3 + Katarina S4–S6)
    start = main_script.index("const SEC = {")
    end = main_script.index("function updateCopy(){")
    late_js = main_script[start:end]
    late_js = late_js.replace("const SEC = {", "const MAIN_SEC = {", 1)
    late_js = late_js.replace("function updateParticles(t)", "function updateParticlesMain(t, p0)", 1)
    late_js = late_js.replace("const p0=scrollProgress;", "", 1)
    late_js = late_js.replace("SEC.", "MAIN_SEC.")
    late_js = late_js.replace(
        "function drawGarden(t){\n  const p0=scrollProgress;",
        "function drawGarden(t, p0Arg){\n  const p0=p0Arg!==undefined?p0Arg:scrollProgress;",
    )

    helpers = f"""
/* ---------- main late timeline (Catherine S3 + Katarina S4–S6) ---------- */
const LATE_START = {LATE_START};
const MAIN_ORIGIN = {MAIN_ORIGIN};
function toMainP(p) {{
  if (p < LATE_START) return MAIN_ORIGIN;
  return MAIN_ORIGIN + (p - LATE_START) / {LATE_SPAN} * {MAIN_SPAN};
}}
const copyRoot = document.getElementById('copy');

"""

    marker = "/* ---------- copy fade ---------- */"
    if marker not in text:
        raise RuntimeError("copy fade marker not found")
    text = text.replace(marker, helpers + late_js + "\n" + marker, 1)

    # Delegate particle sim to main engine after S2
    old = (
        "function updateParticles(t, dt){\n"
        "  const p0=scrollProgress;\n"
        "  const onLanding = p0 < SEC.s1[0];"
    )
    new = (
        "function updateParticles(t, dt){\n"
        "  const p0=scrollProgress;\n"
        "  if(p0 >= LATE_START){ updateParticlesMain(t, toMainP(p0)); return 'late'; }\n"
        "  const onLanding = p0 < SEC.s1[0];"
    )
    if old not in text:
        raise RuntimeError("updateParticles header not found")
    text = text.replace(old, new, 1)

    # Late render path — main's storm / blocks / garden choreography (early exit)
    late_frame = """
  if(p0 >= LATE_START){
    ctx.clearRect(0,0,W,H);
    const pM = toMainP(p0);
    updateParticlesMain(t, pM);
    updateGardenView(pM);
    const rp = rainProgress(t, pM);
    const dark = stormBgDark(pM, rp);
    if(dark > 0.02) drawStormBg(dark, pM);
    if(copyRoot) copyRoot.classList.toggle('storm-dark', dark > 0.38);

    const condense = Math.min(1, Math.max(0, (pM - 0.435) / 0.08));
    const diamond = Math.min(1, Math.max(0, (pM - 0.532) / 0.024));
    const blocks = Math.min(1, Math.max(0, (pM - 0.552) / 0.048));
    const condenseFade = 1 - seg(pM, 0.512, 0.538);
    const diamondForm = seg(pM, 0.532, 0.556);
    const diamondFade = 1 - seg(pM, 0.560, 0.590);
    const blockGrow = seg(pM, 0.552, 0.600);

    if(condense > 0.01 && condenseFade > 0.01) drawGutCondense(condense, t, condenseFade);
    if(diamondForm > 0.01 && diamondFade > 0.01) drawDiamondGrid(diamondForm, diamondFade, t);
    if(pM >= MAIN_SEC.s3b[0] && pM < MAIN_SEC.s4a[0]){
      const blockA = 1 - seg(pM, MAIN_SEC.s4a[0]-0.012, MAIN_SEC.s4a[0]);
      if(blockGrow > 0 && blockA > 0.01) drawBlockField(blockGrow, blockA, t);
    }
    if(stormBgDark(pM, rp) > 0.05) drawS4GridDots(t, pM, rp);
    const isoBase = pM >= MAIN_SEC.s4r[0] ? ease(Math.min(1, rp*1.2)) : 0;
    const isoA = isoBase * (1 - (gardenView.zoomT || 0) * 0.88);
    if(isoA > 0.01){ drawGroundEmergence(isoA, rp); drawIsoFloor(isoA); }
    if((gardenView.zoomT || 0) > 0.06){
      const w = ease(gardenView.zoomT);
      const top = H * (0.48 - w * 0.14);
      const grd = ctx.createLinearGradient(0, top, 0, H);
      grd.addColorStop(0, 'rgba(249,249,245,0)');
      grd.addColorStop(0.4, `rgba(210,228,186,${w*0.32})`);
      grd.addColorStop(1, `rgba(168,198,142,${w*0.58})`);
      ctx.fillStyle = grd;
      ctx.fillRect(0, top, W, H - top);
    }
    drawGarden(t, pM);

    if(pM < MAIN_SEC.s5a[0] + 0.02){
      for(let idx = 0; idx < N; idx++){
        const p = P[idx];
        if(p.alpha < 0.02) continue;
        drawParticle(p, p.x, p.y, 6.0 * p.size, p.alpha);
      }
    }

    updateCopyLate(p0);
    updateJourney();
    updateBackground();
    requestAnimationFrame(frame);
    return;
  }
"""
    frame_anchor = "  const p0=scrollProgress;\n  ctx.clearRect(0,0,W,H);"
    if frame_anchor not in text:
        raise RuntimeError("frame anchor not found")
    text = text.replace(frame_anchor, "  const p0=scrollProgress;\n" + late_frame + "\n  ctx.clearRect(0,0,W,H);", 1)

    # Guard early-phase particle draw so it never runs during S3+
    text = text.replace(
        "  if(p0 < SEC.s5a[0]+0.02){",
        "  if(p0 < LATE_START){",
        1,
    )

    # Skip Maddi's crushed late overlays once main engine owns the timeline
    text = text.replace(
        "  if(p0>=SEC.s3b[0] && p0<SEC.s4a[0]) drawGutBlocks();\n  drawGarden(t);",
        "",
        1,
    )
    text = text.replace(
        "  if(stormDotA>0.01) drawStormGridDots(t, p0, stormDotA);\n"
        "  if(isoA>0.01){ drawGroundEmergence(isoA); drawIsoFloor(isoA); }\n\n",
        "",
        1,
    )

    main_copy_body = main_script.split("function updateCopy(){", 1)[1].split("\n}", 1)[0]
    text = text.replace(
        "function updateCopy(){",
        "function updateCopyLate(p0){\n  const zf=gardenView.zoomT || 0;" + main_copy_body + "\n}\nfunction updateCopy(){",
        1,
    )

    # Journey rail: remap s3+ keys to integrated scroll positions
    journey_old = """    { p: SEC.s2[1],    j: 0.44 },
    { p: SEC.s3b[1],   j: 0.58 },
    { p: SEC.s4c[1],   j: 0.74 },
    { p: SEC.s5a[0],   j: 0.88 },"""
    journey_new = f"""    {{ p: SEC.s2[1],    j: 0.44 }},
    {{ p: {remap_main(0.60)}, j: 0.58 }},
    {{ p: {remap_main(0.82)}, j: 0.74 }},
    {{ p: {remap_main(0.82)}, j: 0.88 }},"""
    text = text.replace(journey_old, journey_new, 1)

    # Fix Maddi early-path references after SEC trim
    text = text.replace(
        "  const inStorm = (p0>=SEC.s4a[0] && p0<SEC.s4c[1]);\n"
        "  const inRain = (p0>=SEC.s4c[0] && p0<SEC.s4c[1]);",
        "  const inStorm = false; /* S3+ storm handled by updateParticlesMain */\n"
        "  const inRain = false;",
        1,
    )
    text = text.replace(
        "  if(p0>=SEC.s6[0]) phase='s6';",
        "",
        1,
    )
    frame_storm = (
        "  const dotA  = seg(p0, SEC.s2[1], SEC.s2[1]+0.03) * (1-seg(p0, SEC.s4a[0]-0.02, SEC.s4a[0]+0.02));\n"
        "  const inStormPhase = p0>=SEC.s4a[0] && p0<SEC.s4c[1];\n"
        "  const stormDotA = inStormPhase ? 1-seg(p0, SEC.s4c[0]+0.55, SEC.s4c[1])*0.9 : 0;\n"
        "  const rainProg = seg(p0, SEC.s4c[0], SEC.s4c[1]);\n"
        "  const isoA  = (p0>=SEC.s4c[0] ? ease(Math.min(1, rainProg*1.2)) : 0) * (p0>SEC.s6[0]? 1-seg(p0,SEC.s6[0]+0.03,1)*0.55 : 1);\n"
    )
    text = text.replace(frame_storm, "  const dotA  = seg(p0, SEC.s2[1], SEC.s2[1]+0.03);\n", 1)

    for out_name in ("flora.html", "index.html"):
        (ROOT / out_name).write_text(text)
        print(f"Wrote {out_name} ({len(text.splitlines())} lines)")


if __name__ == "__main__":
    main()
