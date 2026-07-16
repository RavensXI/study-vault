# -*- coding: utf-8 -*-
import json, math, io, re

SRC = "_L06_diag_live.json"
OUT = "lesson_geometry-L06_diagrams.json"

def sss(a, b, c):
    x = (c*c - b*b + a*a) / (2*a)
    y2 = c*c - x*x
    y = math.sqrt(y2) if y2 > 0 else 0.0
    return [(0.0, 0.0), (a, 0.0), (x, y)]  # 0=B,1=C,2=A

def unit(dx, dy):
    m = math.hypot(dx, dy) or 1.0
    return dx/m, dy/m

def render(points, edges, angles, interior, aria, W=240, H=175, pad=34):
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    s = min((W - 2*pad)/(maxx-minx or 1), (H - 2*pad)/(maxy-miny or 1))
    offx = pad + ((W - 2*pad) - (maxx-minx)*s)/2
    offy = pad + ((H - 2*pad) - (maxy-miny)*s)/2
    def P(pt):
        return (offx + (pt[0]-minx)*s, H - (offy + (pt[1]-miny)*s))
    pix = [P(p) for p in points]
    cx = sum(p[0] for p in pix)/len(pix)
    cy = sum(p[1] for p in pix)/len(pix)
    n = len(pix)
    parts = []
    poly = " ".join("%.1f,%.1f" % (p[0], p[1]) for p in pix)
    parts.append('<polygon points="%s" fill="#60a5fa" fill-opacity="0.16" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>' % poly)
    for (i, j, text) in edges:
        if not text:
            continue
        ax, ay = pix[i]; bx, by = pix[j]
        mx, my = (ax+bx)/2, (ay+by)/2
        nx, ny = unit(-(by-ay), (bx-ax))
        if (nx*(mx-cx) + ny*(my-cy)) < 0:
            nx, ny = -nx, -ny
        parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle" dominant-baseline="middle">%s</text>' % (mx+nx*14, my+ny*14, text))
    for (i, text, right) in angles:
        vx, vy = pix[i]
        pv = pix[(i-1) % n]; nv = pix[(i+1) % n]
        d1x, d1y = unit(pv[0]-vx, pv[1]-vy)
        d2x, d2y = unit(nv[0]-vx, nv[1]-vy)
        bx, by = unit(d1x+d2x, d1y+d2y)
        if right:
            sq = 12.0
            p1 = (vx+d1x*sq, vy+d1y*sq)
            p2 = (vx+d1x*sq+d2x*sq, vy+d1y*sq+d2y*sq)
            p3 = (vx+d2x*sq, vy+d2y*sq)
            parts.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f" fill="none" stroke="currentColor" stroke-width="1.3"/>' % (p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]))
        else:
            r = 16.0
            a1 = (vx+d1x*r, vy+d1y*r); a2 = (vx+d2x*r, vy+d2y*r)
            cross = d1x*d2y - d1y*d2x
            sweep = 1 if cross > 0 else 0
            parts.append('<path d="M%.1f %.1f A%.0f %.0f 0 0 %d %.1f %.1f" fill="none" stroke="currentColor" stroke-width="1.3"/>' % (a1[0], a1[1], r, r, sweep, a2[0], a2[1]))
        if text:
            parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle" dominant-baseline="middle">%s</text>' % (vx+bx*25, vy+by*25, text))
    for k, t in enumerate(interior):
        parts.append('<text x="%.1f" y="%.1f" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle" dominant-baseline="middle">%s</text>' % (cx, cy + k*14 - (len(interior)-1)*7, t))
    return '<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:280px;width:100%%;height:auto;display:block;margin:0 auto 8px">%s</svg>' % (W, H, aria, "".join(parts))

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

def tri(a, b, c, ea, eb, ec, angA, angB, angC, interior, aria):
    pts = sss(a, b, c)
    edges = [(0, 1, ea), (1, 2, eb), (2, 0, ec)]
    angles = []
    if angB is not None: angles.append((0, angB[0], angB[1]))
    if angC is not None: angles.append((1, angC[0], angC[1]))
    if angA is not None: angles.append((2, angA[0], angA[1]))
    return render(pts, edges, angles, interior, aria)

FIG = {}
c = math.cos; r = math.radians; sq = math.sqrt

FIG['opener'] = render([(0.0, 0.0), (10.0, 0.0), (0.0, 4.0)],
    [(0, 1, "10 m"), (2, 0, "4 m"), (1, 2, None)], [(0, None, True)],
    ["Area = ?"], "Right-angled triangular flag with legs 10 m and 4 m; area unknown")

FIG['teach_bronze'] = tri(5, 8, sq(25+64-80*c(r(30))), "5 cm", "8 cm", None,
    None, None, ("30°", False), ["Area = ?"],
    "Triangle with sides 5 cm and 8 cm meeting at a 30 degree angle; area unknown")
FIG['teach_silver'] = tri(6, 10, sq(36+100-120*c(r(60))), "6 cm", "10 cm", "c = ?",
    None, None, ("60°", False), [],
    "Triangle with sides 6 cm and 10 cm meeting at a 60 degree angle; opposite side c unknown")
tg_c = 8*math.sin(r(180-25-140.7))/math.sin(r(25))
FIG['teach_gold'] = tri(8, 12, tg_c, "8 cm", "12 cm", None,
    ("25°", False), ("?", False), None, [],
    "Triangle with side 8 cm opposite a 25 degree angle and side 12 cm opposite the obtuse angle marked with a question mark")

FIG[('bronze', 0)] = tri(6, 10, sq(36+100-120*c(r(30))), "6 cm", "10 cm", None,
    None, None, ("30°", False), ["Area = ?"],
    "Triangle with sides 6 cm and 10 cm meeting at a 30 degree angle; area unknown")
FIG[('bronze', 1)] = tri(8, 5, sq(64+25-80*c(r(40))), "8 cm", "5 cm", None,
    None, None, ("40°", False), ["Area = ?"],
    "Triangle with sides 8 cm and 5 cm meeting at a 40 degree angle; area unknown")
FIG[('bronze', 2)] = tri(10, 20, 17.3205, "10 cm", "b = ?", None,
    ("30°", False), ("", True), None, [],
    "Triangle with a right angle, side 10 cm opposite a 30 degree angle, and unknown side b")
FIG[('bronze', 3)] = tri(7, 12, sq(49+144-168*c(r(45))), "7 cm", "12 cm", None,
    None, None, ("45°", False), ["Area = ?"],
    "Triangle with sides 7 cm and 12 cm meeting at a 45 degree angle; area unknown")
FIG[('bronze', 5)] = tri(9, 9, 9, "9 cm", "9 cm", None,
    None, None, ("60°", False), ["Area = ?"],
    "Triangle with two 9 cm sides meeting at a 60 degree angle; area unknown")
FIG[('bronze', 7)] = tri(10, 14, sq(100+196-280*c(r(55))), "10 cm", "14 cm", None,
    None, None, ("55°", False), ["Area = ?"],
    "Triangle with sides 10 cm and 14 cm meeting at a 55 degree angle; area unknown")

FIG[('silver', 0)] = tri(8, 8*math.sin(r(75))/math.sin(r(40)), 8*math.sin(r(65))/math.sin(r(40)),
    "8 cm", "b = ?", None, ("40°", False), None, ("75°", False), [],
    "Triangle with side 8 cm opposite a 40 degree angle and a 75 degree angle; side b unknown")
FIG[('silver', 1)] = tri(5, 7, sq(25+49-70*c(r(50))), "5 cm", "7 cm", "c = ?",
    None, None, ("50°", False), [],
    "Triangle with sides 5 cm and 7 cm meeting at a 50 degree angle; opposite side c unknown")
FIG[('silver', 2)] = tri(10, 8, 6, "10", "8", "6", ("?", False), None, None, [],
    "Triangle with sides 10, 8 and 6; angle A opposite side 10 unknown")
s3_c = 12*math.sin(r(180-40-53.5))/math.sin(r(40))
FIG[('silver', 3)] = tri(12, 15, s3_c, "12 cm", "15 cm", None,
    ("40°", False), ("?", False), None, [],
    "Triangle with side 12 cm opposite a 40 degree angle and side 15 cm opposite the unknown angle B")
FIG[('silver', 4)] = tri(11, 13, sq(121+169-286*c(r(52))), "11 cm", "13 cm", None,
    None, None, ("52°", False), ["Area = ?"],
    "Triangle with sides 11 cm and 13 cm meeting at a 52 degree angle; area unknown")
FIG[('silver', 5)] = tri(9, 11, 14, "9", "11", "14", None, None, ("?", False), [],
    "Triangle with sides 9, 11 and 14; angle C opposite side 14 unknown")
FIG[('silver', 6)] = tri(10*math.sin(r(35))/math.sin(r(80)), 10*math.sin(r(65))/math.sin(r(80)), 10,
    "a = ?", None, "10 cm", ("35°", False), None, ("80°", False), [],
    "Triangle with side 10 cm opposite an 80 degree angle and a 35 degree angle; side a unknown")

g0_ang = math.degrees(math.asin(2*30/(8*11)))
FIG[('gold', 0)] = tri(8, 11, sq(64+121-2*8*11*c(r(g0_ang))), "8 cm", "11 cm", None,
    None, None, ("?", False), ["Area = 30 cm²"],
    "Triangle with sides 8 cm and 11 cm, area 30 square cm; included angle unknown")
FIG[('gold', 1)] = tri(7, 9, sq(49+81-126*c(r(120))), "7 cm", "9 cm", "c = ?",
    None, None, ("120°", False), [],
    "Triangle with sides 7 cm and 9 cm meeting at a 120 degree angle; opposite side c unknown")
FIG[('gold', 2)] = tri(5, 6, 7, "5", "6", "7", None, None, ("?", False), [],
    "Triangle with sides 5, 6 and 7; largest angle opposite side 7 unknown")
g3_c = 10*math.sin(r(180-30-135.6))/math.sin(r(30))
FIG[('gold', 3)] = tri(10, 14, g3_c, "10 cm", "14 cm", None,
    ("30°", False), ("?", False), None, [],
    "Triangle with side 10 cm opposite a 30 degree angle and side 14 cm opposite the obtuse angle B")
th = r(65)
FIG[('gold', 4)] = render(
    [(0.0, 0.0), (12.0, 0.0), (12+8*c(th), 8*math.sin(th)), (8*c(th), 8*math.sin(th))],
    [(0, 1, "12 cm"), (1, 2, "8 cm"), (2, 3, None), (3, 0, None)],
    [(0, "65°", False)], ["Area = ?"],
    "Parallelogram with sides 12 cm and 8 cm and a 65 degree angle; area unknown")

pd = json.load(io.open(SRC, encoding="utf-8"))
def prepend(display, svg): return svg + CAP + display

added = []
g = pd["guided"]
g["opener"]["display"] = prepend(g["opener"]["display"], FIG['opener'])
added.append("opener")
for tier in ("bronze", "silver", "gold"):
    g["teach"][tier]["display"] = prepend(g["teach"][tier]["display"], FIG['teach_' + tier])
    added.append("teach." + tier)
pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    for i, prob in enumerate(pb[tier]):
        if (tier, i) in FIG:
            prob["display"] = prepend(prob["display"], FIG[(tier, i)])
            added.append("%s[%d]" % (tier, i))

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("FIGURES ADDED:", len(added))
print(added)
for name, fig in FIG.items():
    labels = re.findall(r">([^<]+)</text>", fig)
    aria = re.search(r'aria-label="([^"]+)"', fig).group(1)
    print("\n%s | %s | labels=%s" % (str(name), aria, labels))
    if len(fig) > 3000:
        print("  WARN big svg", len(fig))
