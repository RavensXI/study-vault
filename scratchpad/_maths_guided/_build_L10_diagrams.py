# -*- coding: utf-8 -*-
import json, math

pd = json.load(open("_L10_live_fresh.json", encoding="utf-8"))

CX, CY, S = 130.0, 105.0, 13.0   # centre px, scale px per unit
def px(x, y):
    return (CX + x*S, CY - y*S)

def build_svg(cid, r2, line_fn, sols, circle_lbl, line_lbl, aria):
    r = math.sqrt(r2) * S
    # line endpoints in data x=-9..9, clipped by clipPath
    x1d, x2d = -9.0, 9.0
    lx1, ly1 = px(x1d, line_fn(x1d))
    lx2, ly2 = px(x2d, line_fn(x2d))
    pts = []
    for x in sols:
        y = line_fn(x)
        pts.append(px(x, y))
    dots = ""
    for i, (dx, dy) in enumerate(pts):
        dots += '<circle cx="%.1f" cy="%.1f" r="3.2" fill="#f59e0b"/>' % (dx, dy)
        # place ? label away from origin
        ox = 7 if dx >= CX else -14
        oy = -5 if dy <= CY else 14
        dots += '<text x="%.1f" y="%.1f" font-size="12" font-family="Inter,sans-serif" fill="currentColor">?</text>' % (dx+ox, dy+oy)
    svg = (
      '<svg viewBox="0 0 260 224" role="img" aria-label="%s" style="max-width:280px">' % aria +
      '<defs><clipPath id="%s"><rect x="6" y="6" width="248" height="196"/></clipPath></defs>' % cid +
      '<g clip-path="url(#%s)">' % cid +
      '<line x1="8" y1="105" x2="252" y2="105" stroke="currentColor" stroke-width="1" opacity="0.35"/>' +
      '<line x1="130" y1="10" x2="130" y2="198" stroke="currentColor" stroke-width="1" opacity="0.35"/>' +
      '<circle cx="130" cy="105" r="%.1f" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>' % r +
      '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#f59e0b" stroke-width="1.8"/>' % (lx1, ly1, lx2, ly2) +
      '</g>' +
      '<text x="250" y="101" font-size="10" font-family="Inter,sans-serif" fill="currentColor" text-anchor="end">x</text>' +
      '<text x="134" y="18" font-size="10" font-family="Inter,sans-serif" fill="currentColor">y</text>' +
      '<text x="122" y="118" font-size="10" font-family="Inter,sans-serif" fill="currentColor">O</text>' +
      '<text x="8" y="20" font-size="10.5" font-family="Inter,sans-serif" fill="currentColor">%s</text>' % circle_lbl +
      '<text x="8" y="219" font-size="10.5" font-family="Inter,sans-serif" fill="currentColor">%s</text>' % line_lbl +
      dots +
      '</svg>'
    )
    return svg

# unicode minus (−) and superscript two for labels
M = "−"
cases = [
 (0, "clpG0", 25, lambda x: 7 - x,   [4, 3],   "x²+y²=25", "x+y=7",
  "Circle x squared plus y squared equals 25 and the line x plus y equals 7 crossing at two points"),
 (1, "clpG1", 10, lambda x: 2*x + 1, [1, -1.8], "x²+y²=10", "y=2x+1",
  "Circle x squared plus y squared equals 10 and the line y equals 2x plus 1 crossing at two points"),
 (2, "clpG2", 13, lambda x: x - 1,   [3, -2],  "x²+y²=13", "x"+M+"y=1",
  "Circle x squared plus y squared equals 13 and the line x minus y equals 1 crossing at two points"),
 (3, "clpG3", 20, lambda x: x + 2,   [2, -4],  "x²+y²=20", "y=x+2",
  "Circle x squared plus y squared equals 20 and the line y equals x plus 2 crossing at two points"),
]

gold = pd["problem_bank"]["gold"]
added = []
for idx, cid, r2, fn, sols, clbl, llbl, aria in cases:
    p = gold[idx]
    disp = p["display"]
    if "<svg" in disp:
        raise SystemExit("problem already has svg: gold[%d]" % idx)
    svg = build_svg(cid, r2, fn, sols, clbl, llbl, aria)
    cap = '<span class="figure-caption">Diagram not drawn accurately</span>'
    p["display"] = svg + cap + disp
    added.append({"tier": "gold", "index": idx, "kind": "svg",
                  "what": "Coordinate circle %s with line %s, two intersections marked ?" % (clbl, llbl),
                  "svg_len": len(svg)})
    print("gold[%d] svg %d chars" % (idx, len(svg)))

json.dump(pd, open("lesson_algebra-L10_diagrams.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(added, open("_added_L10.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("written. figures:", len(added))
