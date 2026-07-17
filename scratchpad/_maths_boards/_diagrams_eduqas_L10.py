# -*- coding: utf-8 -*-
import json, math

pd = json.load(open("lesson_maths-eduqas_algebra-L10.json", encoding="utf-8"))
CX, CY, S = 130.0, 105.0, 13.0
def px(x, y): return (CX + x*S, CY - y*S)
M = "−"

def build_svg(cid, r2, line_fn, sols, circle_lbl, line_lbl, aria):
    r = math.sqrt(r2) * S
    x1d, x2d = -9.0, 9.0
    lx1, ly1 = px(x1d, line_fn(x1d)); lx2, ly2 = px(x2d, line_fn(x2d))
    dots = ""
    for x in sols:
        dx, dy = px(x, line_fn(x))
        # sanity: point lies on circle
        assert abs(x*x + line_fn(x)**2 - r2) < 1e-6, (x, line_fn(x), r2)
        dots += '<circle cx="%.1f" cy="%.1f" r="3.2" fill="#f59e0b"/>' % (dx, dy)
        ox = 7 if dx >= CX else -14
        oy = -5 if dy <= CY else 14
        dots += '<text x="%.1f" y="%.1f" font-size="12" font-family="Inter,sans-serif" fill="currentColor">?</text>' % (dx+ox, dy+oy)
    return (
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
      dots + '</svg>'
    )

cases = [
 (0, "clpE0", 10, lambda x: 2*x + 1, [1, -1.8], "x²+y²=10", "y=2x+1",
  "Circle x squared plus y squared equals 10 and the line y equals 2x plus 1 crossing at two points"),
 (1, "clpE1", 13, lambda x: 5 - x,   [2, 3],   "x²+y²=13", "x+y=5",
  "Circle x squared plus y squared equals 13 and the line x plus y equals 5 crossing at two points"),
 (2, "clpE2", 25, lambda x: x - 1,   [4, -3],  "x²+y²=25", "y=x" + M + "1",
  "Circle x squared plus y squared equals 25 and the line y equals x minus 1 crossing at two points"),
]

gold = pd["problem_bank"]["gold"]
added = []
for idx, cid, r2, fn, sols, clbl, llbl, aria in cases:
    p = gold[idx]
    assert "<svg" not in p["display"]
    assert sorted(p["solutions"]) == sorted(sols), (idx, p["solutions"], sols)
    svg = build_svg(cid, r2, fn, sols, clbl, llbl, aria)
    cap = '<span class="figure-caption">Diagram not drawn accurately</span>'
    p["display"] = svg + cap + p["display"]
    added.append({"tier": "gold", "index": idx, "kind": "svg",
                  "what": "Coordinate circle %s with line %s, two intersections marked ?" % (clbl, llbl)})
    print("gold[%d] svg %d chars" % (idx, len(svg)))

json.dump(pd, open("lesson_maths-eduqas_algebra-L10.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(added, open("_added_eduqas_L10.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("figures:", len(added))
