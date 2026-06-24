#!/usr/bin/env python3
"""Safely build flora.html from index.html + main late sections."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATE_START = 0.903
MAIN_ORIGIN = 0.448
MAIN_SPAN = 1.0 - MAIN_ORIGIN
LATE_SPAN = 1.0 - LATE_START


def to_main_p(p: float) -> float:
    if p < LATE_START:
        return MAIN_ORIGIN
    return MAIN_ORIGIN + (p - LATE_START) / LATE_SPAN * MAIN_SPAN


def remap_main(p: float) -> float:
    return round(LATE_START + (p - MAIN_ORIGIN) * (LATE_SPAN / MAIN_SPAN), 3)


def main() -> None:
    index_lines = (ROOT / "index.html").read_text().splitlines(keepends=True)
    main_flora = (ROOT / "flora-main-ref.html").read_text()
    main_script = main_flora.split("<script>", 1)[1].rsplit("</script>", 1)[0]

  # S3+ copy with remapped timings (Catherine + Katarina from main)
    s3_block = """    <!-- S3 — Catherine -->
    <div class="t lg work" data-in="0.904" data-out="0.919" style="top:26%; left:6%;">during menopause ,
they become hard to read .</div>
    <div class="t md work" data-in="0.920" data-out="0.926" style="top:40%; left:50%; max-width:38%; white-space:normal;">more than a billion women will be in menopause globally by 2030 .</div>

    <!-- S4 — Katarina -->
    <div class="t lg tc work" data-in="0.929" data-out="0.935">“you’re too emotional”</div>
    <div class="t tc work" data-in="0.936" data-out="0.946">
      <div class="lg" style="font-size:clamp(22px,2.6vw,34px); line-height:1.16;">over time ,
many women stop
trusting themselves .</div>
      <div class="sm" style="margin-top:14px;">what the science says : 20% of working women experience a loss of confidence during menopause .</div>
    </div>

    <!-- S5 -->
    <div class="t lg work" data-in="0.962" data-out="0.970" data-zoom-fade style="top:10%; right:7%; text-align:right;">your body has always
been speaking ;</div>
    <div class="t lg work" data-in="0.976" data-out="0.982" style="top:12%; left:7%; text-align:left;">take care of
your gut ;</div>
    <div class="t lg work" data-in="0.978" data-out="0.984" data-zoom-fade style="bottom:24%; right:7%; text-align:right;">so you can
listen to it ;</div>
    <div class="t lg work end-hero" data-in="0.989" data-out="1.01" data-zoom-reveal="0.78">and learn to trust
your gut feeling .</div>

    <!-- S6 -->
    <div class="t sm work" data-in="0.989" data-out="1.01" style="bottom:7%; left:50%; transform:translate(-50%,0); white-space:normal; text-align:center; max-width:min(88vw,420px);">we are not doctors ;
please talk to your doctors
to learn more</div>
"""

    # Find S3 block in index
    out = []
    i = 0
    while i < len(index_lines):
        line = index_lines[i]
        if line.strip() == "<!-- S3 -->":
            out.append(s3_block)
            i += 1
            while i < len(index_lines) and "<!-- S6 -->" not in index_lines[i]:
                i += 1
            while i < len(index_lines) and "</div>" not in index_lines[i]:
                i += 1
            if i < len(index_lines):
                i += 1  # skip closing S6 div
            continue
        out.append(line)
        i += 1

    text = "".join(out)

    storm_css = """
  #copy.storm-dark .work,
  #copy.storm-dark .work .lg,
  #copy.storm-dark .work .sm{ color:#F5F2EB; }
  .t.end-hero{
    left:0; right:0; width:100%; top:calc(17% + 40px);
    transform:translateY(8px); text-align:center; white-space:normal;
    max-width:none; padding:0 6vw;
    background:linear-gradient(155deg, #2a5224 0%, #3d7a35 42%, #5c9a48 72%, #76b947 100%);
    -webkit-background-clip:text; background-clip:text; color:transparent;
  }
  .t.end-hero.show{ transform:translateY(0); }
"""
    text = text.replace("  .faint{ color:#9a9a9a; }", "  .faint{ color:#9a9a9a; }" + storm_css)

    # Extract main late engine
    start = main_script.index("const SEC = {")
    end = main_script.index("function updateCopy(){")
    late_js = main_script[start:end]
    late_js = late_js.replace("const SEC = {", "const MAIN_SEC = {")
    late_js = late_js.replace("function updateParticles(t)", "function updateParticlesMain(t, p0)")
    late_js = late_js.replace("const p0=scrollProgress;", "")
    late_js = late_js.replace("SEC.", "MAIN_SEC.")

    helpers = f"""
/* ---------- main late timeline (Catherine S3 + Katarina S4–S6) ---------- */
const LATE_START = {LATE_START};
const MAIN_ORIGIN = {MAIN_ORIGIN};
function toMainP(p) {{
  if (p < LATE_START) return MAIN_ORIGIN;
  return MAIN_ORIGIN + (p - LATE_START) / (1 - LATE_START) * (1 - MAIN_ORIGIN);
}}
let gardenView = {{ zoomT: 0 }};
const copyRoot = document.getElementById('copy');

"""

    marker = "/* ---------- copy fade ---------- */"
    text = text.replace(marker, helpers + late_js + "\n" + marker)

    text = text.replace(
        "function updateParticles(t, dt){\n  const p0=scrollProgress;\n  const onLanding = p0 < SEC.s1[0];",
        "function updateParticles(t, dt){\n  const p0=scrollProgress;\n  if(p0 >= LATE_START){ updateParticlesMain(t, toMainP(p0)); return 'late'; }\n  const onLanding = p0 < SEC.s1[0];",
    )

    late_frame = """
  if(p0 >= LATE_START){
    const pM = toMainP(p0);
    updateGardenView(pM);
    const rp = rainProgress(t, pM);
    const dark = stormBgDark(pM, rp);
    if(dark > 0.02) drawStormBg(dark, pM);
    if(copyRoot) copyRoot.classList.toggle('storm-dark', dark > 0.38);
    const condense = Math.min(1, Math.max(0, (pM - 0.435) / 0.08));
    const diamond = Math.min(1, Math.max(0, (pM - 0.532) / 0.024));
    const blocks = Math.min(1, Math.max(0, (pM - 0.552) / 0.048));
    if(condense > 0.01) drawGutCondense(condense, t, 1);
    if(diamond > 0.01) drawDiamondGrid(diamond, t);
    if(blocks > 0.01) drawBlockField(blocks, t, 1 - rp * 0.5);
    if(stormBgDark(pM, rp) > 0.05) drawS4GridDots(t, pM, rp);
    if(rp > 0.01){ drawGroundEmergence(rp, rp); drawIsoFloor(rp); }
    drawGarden(t);
    updateCopyLate(pM);
    requestAnimationFrame(frame);
    return;
  }
"""
    text = text.replace(
        "  if(p0 < SEC.s5a[0]+0.02){",
        late_frame + "  if(p0 < LATE_START && p0 < SEC.s5a[0]+0.02){",
    )

    main_copy = main_script.split("function updateCopy(){", 1)[1].split("\n}", 1)[0]
    text = text.replace(
        "function updateCopy(){",
        "function updateCopyLate(p0){\n  const zoomT = gardenView.zoomT || 0;" + main_copy + "\n}\nfunction updateCopy(){",
    )

    text = text.replace("const TOTAL_VH = 9.8;", "const TOTAL_VH = 16;")

    (ROOT / "flora.html").write_text(text)
    print(f"flora.html: {len(text.splitlines())} lines")


if __name__ == "__main__":
    main()
