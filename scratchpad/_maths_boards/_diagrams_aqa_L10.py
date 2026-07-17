# -*- coding: utf-8 -*-
import json, math

pd = json.load(open("lesson_maths-aqa_algebra-L10.json", encoding="utf-8"))
CX, CY, S = 130.0, 105.0, 13.0
M = "−"
def px(x, y): return (CX + x*S, CY - y*S)

def build_svg(cid, r2, line_fn, sols, circle_lbl, line_lbl, aria):
    r = math.sqrt(r2) * S
    lx1, ly1 = px(-9.0, line_fn(-9.0))
    lx2, ly2 = px(9.0, line_fn(9.0))
    dots = ""
    for x in sols:
        dx, dy = px(x, line_fn(x))
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
      dots + '</svg>')

cap = '<span class="figure-caption">Diagram not drawn accurately</span>'
# (tier, index, cid, r2, line_fn, sols, circle_lbl, line_lbl, aria)
cases = [
 ("silver", 1, "clpS1", 13, lambda x: x + 1, [-3, 2], "x²+y²=13", "y=x+1",
  "Circle x squared plus y squared equals 13 and the line y equals x plus 1 crossing at two points"),
 ("silver", 2, "clpS2", 10, lambda x: x - 2, [-1, 3], "x²+y²=10", "y=x" + M + "2",
  "Circle x squared plus y squared equals 10 and the line y equals x minus 2 crossing at two points"),
 ("gold", 1, "clpG1", 25, lambda x: x - 1, [-3, 4], "x²+y²=25", "y=x" + M + "1",
  "Circle x squared plus y squared equals 25 and the line y equals x minus 1 crossing at two points"),
]
added = []
for tier, idx, cid, r2, fn, sols, clbl, llbl, aria in cases:
    p = pd["problem_bank"][tier][idx]
    assert "<svg" not in p["display"], (tier, idx)
    # sanity: intersection points must be on the circle
    for x in sols:
        assert abs(x*x + fn(x)**2 - r2) < 1e-9, ("point off circle", tier, idx, x)
    svg = build_svg(cid, r2, fn, sols, clbl, llbl, aria)
    p["display"] = svg + cap + p["display"]
    added.append({"tier": tier, "index": idx, "kind": "svg",
                  "what": "Coordinate circle %s with line %s, two intersections marked ?" % (clbl, llbl)})
    print("%s[%d] svg %d chars" % (tier, idx, len(svg)))

json.dump(pd, open("lesson_maths-aqa_algebra-L10.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(added, open("_added_aqa_L10.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("figures added:", len(added))
