# -*- coding: utf-8 -*-
import json, io, math

pd = json.load(io.open("_live_geoL01.json", encoding="utf-8"))
pb = pd["problem_bank"]

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

def P(cx, cy, r, deg):
    return (cx + r*math.cos(math.radians(deg)), cy - r*math.sin(math.radians(deg)))

def fmt(p):
    return "%.1f,%.1f" % p

def arc(cx, cy, r, a1, a2):
    p1 = P(cx, cy, r, a1); p2 = P(cx, cy, r, a2)
    large = 1 if abs(a2-a1) > 180 else 0
    # screen y is flipped, so sweep=1 traces the math-CCW direction
    return '<path d="M%s A%g %g 0 %d 1 %s" fill="none" stroke="currentColor" stroke-width="1.4"/>' % (fmt(p1), r, r, large, fmt(p2))

def svg_open(label, w=240, h=150):
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="%s" '
            'style="max-width:280px;font-family:Inter,sans-serif" '
            'stroke-linecap="round">' % (w, h, label))

def txt(x, y, s, size=12, anchor="middle", weight="600"):
    return ('<text x="%.1f" y="%.1f" font-size="%d" text-anchor="%s" '
            'font-weight="%s" fill="currentColor">%s</text>' % (x, y, size, anchor, weight, s))

def line(p1, p2, w=1.8):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="%g"/>' % (p1[0], p1[1], p2[0], p2[1], w)

# ---------- figure builders ----------

def fig_straight_line(left_lbl, right_lbl, acute):
    # horizontal line, apex ray leaning right; acute angle on the right
    cx, cy = 120, 105
    L = (25, cy); R = (215, cy)
    ray = P(cx, cy, 78, acute)
    s = svg_open("Two angles on a straight line at a point")
    s += line(L, R) + line((cx, cy), ray)
    s += '<circle cx="%d" cy="%d" r="2.4" fill="currentColor"/>' % (cx, cy)
    s += arc(cx, cy, 30, 0, acute)                 # right (acute)
    s += arc(cx, cy, 22, acute, 180)               # left (obtuse)
    rp = P(cx, cy, 44, acute/2.0)
    lp = P(cx, cy, 40, (acute+180)/2.0)
    s += txt(rp[0]+4, rp[1], right_lbl)
    s += txt(lp[0]-4, lp[1], left_lbl)
    s += "</svg>"
    return s

def fig_point(vals, angs):
    # angles given CCW starting at 0; vals labels for each sector
    cx, cy = 120, 82
    s = svg_open("Three angles meeting around a point")
    acc = 0.0; bounds = [0.0]
    for a in angs:
        acc += a; bounds.append(acc)
    for b in bounds[:-1]:
        e = P(cx, cy, 70, b)
        s += line((cx, cy), e)
    s += '<circle cx="%d" cy="%d" r="2.6" fill="currentColor"/>' % (cx, cy)
    for i, v in enumerate(vals):
        mid = (bounds[i] + bounds[i+1]) / 2.0
        lp = P(cx, cy, 40, mid)
        s += txt(lp[0], lp[1]+4, v)
    s += "</svg>"
    return s

def fig_vertical(a_lbl, b_lbl):
    cx, cy = 120, 78
    s = svg_open("Two straight lines crossing, showing vertically opposite angles")
    s += line((35, 40), (205, 116)) + line((35, 116), (205, 40))
    s += '<circle cx="%d" cy="%d" r="2.4" fill="currentColor"/>' % (cx, cy)
    s += txt(58, 82, a_lbl, anchor="start")    # left angle
    s += txt(182, 82, b_lbl, anchor="end")     # right angle (vertically opposite)
    s += "</svg>"
    return s

def fig_triangle(lbls):
    # scalene triangle; lbls = [bottom-left, bottom-right, apex]
    A = (30, 128); B = (208, 128); C = (92, 40)
    s = svg_open("A triangle with its three angles marked")
    s += '<polygon points="%s %s %s" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.8"/>' % (fmt(A), fmt(B), fmt(C))
    s += txt(A[0]+16, A[1]-8, lbls[0], anchor="start")
    s += txt(B[0]-14, B[1]-8, lbls[1], anchor="end")
    s += txt(C[0]+2, C[1]+18, lbls[2])
    s += "</svg>"
    return s

def fig_triangle_exterior(a55, xlbl, ext):
    # P (a55) bottom-left, Q third vertex bottom-mid (interior=180-ext, exterior=ext), R apex (xlbl)
    P0 = (40, 120); Q = (150, 120); R = (92, 40); extn = (222, 120)
    s = svg_open("A triangle with one side extended to show an exterior angle")
    s += '<polygon points="%s %s %s" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.8"/>' % (fmt(P0), fmt(Q), fmt(R))
    s += line(Q, extn)
    s += txt(P0[0]+16, P0[1]-8, a55, anchor="start")
    s += txt(R[0]+2, R[1]+18, xlbl)
    s += txt(Q[0]+30, Q[1]-14, ext)   # exterior angle outside, above extension
    s += "</svg>"
    return s

def fig_quad(lbls):
    A = (44, 42); B = (196, 54); Cc = (188, 138); D = (52, 128)
    s = svg_open("A quadrilateral with its four angles marked")
    s += '<polygon points="%s %s %s %s" fill="#34d399" fill-opacity="0.16" stroke="currentColor" stroke-width="1.8"/>' % (fmt(A), fmt(B), fmt(Cc), fmt(D))
    s += txt(A[0]+8, A[1]+18, lbls[0], anchor="start")
    s += txt(B[0]-8, B[1]+18, lbls[1], anchor="end")
    s += txt(Cc[0]-8, Cc[1]-8, lbls[2], anchor="end")
    s += txt(D[0]+8, D[1]-8, lbls[3], anchor="start")
    s += "</svg>"
    return s

def fig_pentagon(lbls):
    # regular-ish pentagon, label 5 vertices
    cx, cy, r = 120, 82, 60
    pts = [P(cx, cy, r, 90 + i*72) for i in range(5)]
    s = svg_open("A pentagon with its five angles marked")
    s += '<polygon points="%s" fill="#f59e0b" fill-opacity="0.16" stroke="currentColor" stroke-width="1.8"/>' % (" ".join(fmt(p) for p in pts))
    for p, l in zip(pts, lbls):
        ix = cx + (p[0]-cx)*0.72; iy = cy + (p[1]-cy)*0.72
        s += txt(ix, iy+4, l, size=11)
    s += "</svg>"
    return s

def fig_hexagon(lbls):
    cx, cy, r = 120, 80, 58
    pts = [P(cx, cy, r, 90 + i*60) for i in range(6)]
    s = svg_open("A hexagon with its six angles marked")
    s += '<polygon points="%s" fill="#60a5fa" fill-opacity="0.16" stroke="currentColor" stroke-width="1.7"/>' % (" ".join(fmt(p) for p in pts))
    for p, l in zip(pts, lbls):
        ix = cx + (p[0]-cx)*0.68; iy = cy + (p[1]-cy)*0.68
        s += txt(ix, iy+4, l, size=10)
    s += "</svg>"
    return s

def fig_isosceles(base_lbl, apex_lbl):
    A = (40, 128); B = (200, 128); C = (120, 34)
    s = svg_open("An isosceles triangle with two equal sides marked")
    s += '<polygon points="%s %s %s" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.8"/>' % (fmt(A), fmt(B), fmt(C))
    # equal-side tick marks on AC and BC
    def tick(p1, p2):
        mx = (p1[0]+p2[0])/2; my = (p1[1]+p2[1])/2
        dx = p2[0]-p1[0]; dy = p2[1]-p1[1]; L = math.hypot(dx, dy)
        nx = -dy/L*5; ny = dx/L*5
        return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="1.6"/>' % (mx-nx, my-ny, mx+nx, my+ny)
    s += tick(A, C) + tick(B, C)
    s += txt(A[0]+18, A[1]-8, base_lbl, anchor="start")
    s += txt(C[0], C[1]+18, apex_lbl)
    s += "</svg>"
    return s

def fig_parallel(top_lbl, bot_lbl, mode):
    # two parallel horizontals + transversal; mode in {alternate, cointerior, corresponding}
    s = svg_open("Two parallel lines cut by a transversal", 240, 150)
    yT, yB = 52, 108
    s += line((28, yT), (212, yT)) + line((28, yB), (212, yB))
    # parallel arrows
    s += txt(120, yT-6, "&#9654;", size=11)
    s += txt(120, yB-6, "&#9654;", size=11)
    T = (100, yT); Bm = (150, yB)
    s += line((70, 28), (180, 132))
    if mode == "corresponding":
        s += txt(T[0]+8, yT+16, top_lbl, anchor="start")
        s += txt(Bm[0]+8, yB+16, bot_lbl, anchor="start")
    elif mode == "alternate":
        s += txt(T[0]+8, yT+16, top_lbl, anchor="start")   # top, below-right
        s += txt(Bm[0]-8, yB-6, bot_lbl, anchor="end")     # bottom, above-left (Z)
    else:  # cointerior
        s += txt(T[0]+8, yT+16, top_lbl, anchor="start")   # between lines, right of T
        s += txt(Bm[0]+8, yB-6, bot_lbl, anchor="start")   # between lines, right of B
    s += "</svg>"
    return s

def prepend(prob, svg):
    prob["display"] = svg + CAP + " " + prob["display"]

# ---------- BANK: hints, misconceptions(expect), guided_steps, figures ----------

def mc(pattern, expect, message):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

# ===== BRONZE =====
b = pb["bronze"]

# B0: straight line x and 110 (was 115 -> fix duplicate; x=70)
b[0]["display"] = "Two angles on a straight line are \\(x\\) and \\(110°\\). Find \\(x\\)."
b[0]["solutions"] = [70]
b[0]["hint"] = "A straight line is 180°, so subtract the known angle from 180."
b[0]["misconceptions"] = [mc("add_not_subtract", 290,
    "Angles on a straight line add to 180°, so x = 180 − 110 = 70°. Adding them gives 290, far too big for one angle.")]
b[0]["guided_steps"] = [
    sayonly("The two angles sit on a straight line, so together they make 180°."),
    box("Write the total for a straight line: ", 180, "Half a full turn is 180°."),
    box("Subtract the known angle: 180 − 110 = ", 70, "180 take away 110.", done="That is x.", phase="substitute"),
    box("Check: 110 + 70 = ", 180, "Add your answer back to the known angle.", done="Back to 180°, so x = 70° is right.", phase="substitute"),
]
prepend(b[0], fig_straight_line("110°", "?", 70))

# B1: around a point 120, 85, x=155
b[1]["hint"] = "Angles around a point add to 360°, so subtract both known angles from 360."
b[1]["misconceptions"] = [mc("forgot_one", 240,
    "Subtract BOTH known angles from a full turn: 360 − 120 − 85 = 155°. Taking away only one leaves 240.")]
b[1]["guided_steps"] = [
    sayonly("Angles that meet around a point make one full turn, 360°."),
    box("Add the two known angles: 120 + 85 = ", 205, "120 plus 85."),
    box("Subtract from a full turn: 360 − 205 = ", 155, "360 take away 205.", done="So x = 155°.", phase="substitute"),
    box("Check: 120 + 85 + 155 = ", 360, "All three should make a full turn.", done="A full 360°, so x = 155° is right.", phase="substitute"),
]
prepend(b[1], fig_point(["120°", "85°", "?"], [120, 85, 155]))

# B2: vertically opposite 3x+10 and 70, x=20
b[2]["hint"] = "Vertically opposite angles are equal, so set 3x + 10 equal to 70."
b[2]["misconceptions"] = [mc("forgot_divide", 60,
    "Setting 3x + 10 = 70 gives 3x = 60, then divide by 3: x = 20. 60 is the value of 3x, not x.")]
b[2]["guided_steps"] = [
    sayonly("Vertically opposite angles (across the X) are equal, so \\(3x + 10 = 70\\)."),
    box("Take 10 from both sides: 70 − 10 = ", 60, "That leaves 3x on its own."),
    box("Now 3x = 60, so divide by 3: 60 ÷ 3 = ", 20, "60 shared into 3.", done="So x = 20.", phase="substitute"),
    box("Check: 3 × 20 + 10 = ", 70, "Put x back in.", done="That gives 70°, matching the opposite angle.", phase="substitute"),
]
prepend(b[2], fig_vertical("70°", "3x + 10"))

# B3: triangle 40,75,x=65
b[3]["hint"] = "The three angles of a triangle add to 180°."
b[3]["misconceptions"] = [mc("used_360", 245,
    "Angles in a triangle add to 180°, not 360°. x = 180 − 40 − 75 = 65°.")]
b[3]["guided_steps"] = [
    sayonly("The three angles inside any triangle add up to 180°."),
    box("Add the two known angles: 40 + 75 = ", 115, "40 plus 75."),
    box("Subtract from 180: 180 − 115 = ", 65, "180 take away 115.", done="So x = 65°.", phase="substitute"),
    box("Check: 40 + 75 + 65 = ", 180, "The three angles should total 180°.", done="Exactly 180°, so x = 65° is right.", phase="substitute"),
]
prepend(b[3], fig_triangle(["40°", "75°", "?"]))

# B4: exterior angle regular hexagon = 60
b[4]["hint"] = "The exterior angles of a regular polygon share 360° equally."
b[4]["misconceptions"] = [mc("gave_interior", 120,
    "That is the interior angle. The exterior angle = 360 ÷ 6 = 60°.")]
b[4]["guided_steps"] = [
    sayonly("The exterior angles of any polygon add up to 360°, shared equally when it is regular."),
    box("Write the total of the exterior angles: ", 360, "One full turn."),
    box("Share between the 6 sides: 360 ÷ 6 = ", 60, "360 divided by 6.", done="So each exterior angle is 60°.", phase="substitute"),
    box("Check the matching interior angle: 180 − 60 = ", 120, "Interior and exterior make a straight line.", done="120° is the interior angle, as expected for a regular hexagon.", phase="substitute"),
]

# B5: quadrilateral 90,80,110,x=80
b[5]["hint"] = "A quadrilateral's angles add to 360°."
b[5]["misconceptions"] = [mc("forgot_subtract", 280,
    "Subtract the total of the known angles from 360°: 360 − 280 = 80°. 280 is just the three added together.")]
b[5]["guided_steps"] = [
    sayonly("The four angles inside a quadrilateral add up to 360°."),
    box("Add the three known angles: 90 + 80 + 110 = ", 280, "90 plus 80 plus 110."),
    box("Subtract from 360: 360 − 280 = ", 80, "360 take away 280.", done="So x = 80°.", phase="substitute"),
    box("Check: 90 + 80 + 110 + 80 = ", 360, "All four should total 360°.", done="A full 360°, so x = 80° is right.", phase="substitute"),
]
prepend(b[5], fig_quad(["90°", "80°", "110°", "?"]))

# B6: straight line 2x and 3x+30, x=30
b[6]["hint"] = "Add both angle expressions, set the total to 180, then solve."
b[6]["misconceptions"] = [mc("used_360", 66,
    "A straight line is 180°, not 360°: 5x + 30 = 180, so 5x = 150 and x = 30.")]
b[6]["guided_steps"] = [
    sayonly("The two angles sit on a straight line, so \\(2x + 3x + 30 = 180\\)."),
    box("Add the x terms: 2x + 3x = ", 5, "2 lots plus 3 lots.", post="x"),
    box("Take the 30 across: 180 − 30 = ", 150, "180 take away 30."),
    box("Now 5x = 150, so x = 150 ÷ 5 = ", 30, "150 shared into 5.", done="So x = 30°.", phase="substitute"),
    box("Check: 2 × 30 + 3 × 30 + 30 = ", 180, "Work out both angles and add.", done="60 + 120 = 180°, so x = 30° is right.", phase="substitute"),
]
prepend(b[6], fig_straight_line("3x + 30", "2x", 60))

# B7: interior angle regular pentagon = 108
b[7]["hint"] = "Interior angle sum is (5 − 2) × 180, then divide by 5."
b[7]["misconceptions"] = [mc("gave_exterior", 72,
    "That is the exterior angle (360 ÷ 5). The interior angle = 540 ÷ 5 = 108°.")]
b[7]["guided_steps"] = [
    sayonly("Interior angle sum of a pentagon = (5 − 2) × 180."),
    box("Work out the sum: (5 − 2) × 180 = 3 × 180 = ", 540, "3 lots of 180."),
    box("Share between the 5 angles: 540 ÷ 5 = ", 108, "540 divided by 5.", done="So each interior angle is 108°.", phase="substitute"),
    box("Check: 5 × 108 = ", 540, "Five equal angles should rebuild the sum.", done="Back to 540°, so 108° is right.", phase="substitute"),
]

# ===== SILVER =====
s = pb["silver"]

# S0: triangle 55, x, exterior 130 -> x=75
s[0]["hint"] = "The exterior angle equals the two opposite interior angles added together."
s[0]["misconceptions"] = [mc("gave_third_interior", 50,
    "50° is the third interior angle (180 − 130). The question wants x: 130 = 55 + x, so x = 75°.")]
s[0]["guided_steps"] = [
    sayonly("An exterior angle equals the sum of the two interior angles not next to it: \\(55 + x = 130\\)."),
    box("The two far interior angles add to the exterior angle. Type that exterior angle: ", 130, "It is given as 130°."),
    box("So x = 130 − 55 = ", 75, "130 take away 55.", done="So x = 75°.", phase="substitute"),
    box("Check the third interior angle: 180 − 130 = ", 50, "Interior and exterior sit on a straight line.", done="55 + 75 + 50 = 180°, so x = 75° is right.", phase="substitute"),
]
prepend(s[0], fig_triangle_exterior("55°", "x", "130°"))

# S1: regular polygon interior 156 -> 15 sides
s[1]["hint"] = "Find the exterior angle first (180 − 156), then divide 360 by it."
s[1]["misconceptions"] = [mc("gave_exterior", 24,
    "24° is the exterior angle. The number of sides = 360 ÷ 24 = 15.")]
s[1]["guided_steps"] = [
    sayonly("Work through the exterior angle: interior + exterior = 180°."),
    box("Exterior angle = 180 − 156 = ", 24, "180 take away 156."),
    box("Number of sides = 360 ÷ 24 = ", 15, "360 divided by 24.", done="So it has 15 sides.", phase="substitute"),
    box("Check: 24 × 15 = ", 360, "The exterior angles should make a full turn.", done="A full 360°, so 15 sides is right.", phase="substitute"),
]

# S2: alternate angles ABE 65, x=65
s[2]["hint"] = "Alternate angles are equal."
s[2]["misconceptions"] = [mc("used_cointerior", 115,
    "Alternate angles are equal, so x = 65°. 115° would be a co-interior angle (180 − 65).")]
s[2]["guided_steps"] = [
    sayonly("Alternate angles (the Z shape) between parallel lines are equal."),
    box("Angle ABE is given. Type it: ", 65, "It is stated as 65°."),
    box("BEF is alternate to ABE, so x = ", 65, "Equal to the alternate angle.", done="So x = 65°.", phase="substitute"),
    box("A co-interior partner would be 180 − 65 = ", 115, "That is the C-angle, which we did NOT use.", done="115° is the supplementary angle, not x, confirming alternate angles stay equal.", phase="substitute"),
]
prepend(s[2], fig_parallel("65°", "x", "alternate"))

# S3: co-interior 72 -> 108
s[3]["hint"] = "Co-interior angles add to 180°."
s[3]["misconceptions"] = [mc("thought_equal", 72,
    "Co-interior (C) angles add to 180°, they are not equal: 180 − 72 = 108°.")]
s[3]["guided_steps"] = [
    sayonly("Co-interior angles (the C shape) between parallel lines add up to 180°."),
    box("Write the total for co-interior angles: ", 180, "They are supplementary."),
    box("Subtract the known angle: 180 − 72 = ", 108, "180 take away 72.", done="So the other angle is 108°.", phase="substitute"),
    box("Check: 72 + 108 = ", 180, "The pair should total 180°.", done="Exactly 180°, so 108° is right.", phase="substitute"),
]
prepend(s[3], fig_parallel("72°", "?", "cointerior"))

# S4: pentagon x,2x,3x,90,120 -> x=55
s[4]["hint"] = "Add the angles, set the total to 540, then solve for x."
s[4]["misconceptions"] = [mc("used_360", 25,
    "A pentagon's angles add to 540°, not 360°: 6x + 210 = 540, so 6x = 330 and x = 55.")]
s[4]["guided_steps"] = [
    sayonly("A pentagon's angles add to (5 − 2) × 180 = 540°."),
    box("Add the x terms: x + 2x + 3x = ", 6, "1 plus 2 plus 3 lots of x.", post="x"),
    box("Add the numbers: 90 + 120 = ", 210, "90 plus 120."),
    box("So 6x + 210 = 540. Take 210 across: 540 − 210 = ", 330, "540 take away 210.", phase="substitute"),
    box("6x = 330, so x = 330 ÷ 6 = ", 55, "330 shared into 6.", done="So x = 55°.", phase="substitute"),
    box("Check the biggest angle 3x: 3 × 55 = ", 165, "Work out the largest, then the total.", done="55 + 110 + 165 + 90 + 120 = 540°, so x = 55° is right.", phase="substitute"),
]
prepend(s[4], fig_pentagon(["x", "2x", "3x", "90°", "120°"]))

# S5: isosceles, 50 is a base angle -> other (apex) = 80
s[5]["hint"] = "Both equal angles are 50°, so subtract 100 from 180."
s[5]["misconceptions"] = [mc("fifty_as_apex", 65,
    "Here 50° is one of the two equal base angles, so both are 50°. The third angle = 180 − 100 = 80°. Treating 50° as the odd one gives 65°.")]
s[5]["guided_steps"] = [
    sayonly("An isosceles triangle has two equal angles. Here 50° is one of the equal pair, so both are 50°."),
    box("Add the two equal angles: 50 + 50 = ", 100, "The two base angles."),
    box("Third angle = 180 − 100 = ", 80, "180 take away 100.", done="So the other angle is 80°.", phase="substitute"),
    box("Check: 50 + 50 + 80 = ", 180, "All three should total 180°.", done="Exactly 180°, so 80° is right.", phase="substitute"),
]
prepend(s[5], fig_isosceles("50°", "?"))

# S6: nonagon interior sum = 1260
s[6]["hint"] = "Use (n − 2) × 180 with n = 9."
s[6]["misconceptions"] = [mc("forgot_minus2", 1620,
    "Use (n − 2) × 180: (9 − 2) × 180 = 1260°. Multiplying by 9 forgets to subtract 2.")]
s[6]["guided_steps"] = [
    sayonly("Interior angle sum = (n − 2) × 180, with n = 9 sides."),
    box("Work out n − 2: 9 − 2 = ", 7, "Nine sides, take away 2."),
    box("Multiply by 180: 7 × 180 = ", 1260, "7 lots of 180.", done="So the sum is 1260°.", phase="substitute"),
    box("Check by splitting: 7 × 18 = 126, then × 10 = ", 1260, "Same product, different order.", done="Still 1260°, so the answer is right.", phase="substitute"),
]

# ===== GOLD =====
g = pb["gold"]

# G0: corresponding 3x+15 and 5x-25 -> x=20
g[0]["hint"] = "Corresponding angles are equal, so set the two expressions equal."
g[0]["misconceptions"] = [mc("sign_slip", -5,
    "Keep signs straight: 3x + 15 = 5x − 25 gives 2x = 40, so x = 20. Adding the x terms by mistake gives 8x = −40 and x = −5, which cannot be right.")]
g[0]["guided_steps"] = [
    sayonly("Corresponding angles (the F shape) are equal, so \\(3x + 15 = 5x - 25\\)."),
    box("Move the x terms to one side: 5x − 3x = ", 2, "5 lots take away 3 lots.", post="x"),
    box("Move the numbers to the other side: 15 + 25 = ", 40, "Both numbers cross over and add."),
    box("So 2x = 40, x = 40 ÷ 2 = ", 20, "40 shared into 2.", done="So x = 20.", phase="substitute"),
    box("Check: 3 × 20 + 15 = ", 75, "Work out both expressions.", done="5 × 20 − 25 = 75 too, so x = 20 is right.", phase="substitute"),
]
prepend(g[0], fig_parallel("3x + 15", "5x − 25", "corresponding"))

# G1: interior = 5 x exterior -> 12 sides
g[1]["hint"] = "Interior + exterior = 180, and interior is 5 lots of the exterior."
g[1]["misconceptions"] = [mc("forgot_add_exterior", 10,
    "Interior + exterior = 180, so 5e + e = 180 (six lots of e): e = 30° and 360 ÷ 30 = 12 sides. Using 5e = 180 forgets the exterior angle itself.")]
g[1]["guided_steps"] = [
    sayonly("Interior + exterior = 180°, and here interior = 5 × exterior, so \\(5e + e = 180\\)."),
    box("Add the lots of e: 5e + e = ", 6, "Five lots plus one lot.", post="e"),
    box("So 6e = 180, e = 180 ÷ 6 = ", 30, "180 shared into 6.", phase="substitute"),
    box("Number of sides = 360 ÷ 30 = ", 12, "360 divided by the exterior angle.", done="So it has 12 sides.", phase="substitute"),
    box("Check: interior = 180 − 30 = 150, and 150 ÷ 30 = ", 5, "Interior should be 5 times the exterior.", done="Exactly 5 times, so 12 sides is right.", phase="substitute"),
]

# G2: hexagon 2x,3x+10,x+50,130,150,x+30 -> x=50
g[2]["hint"] = "Collect the x terms and the numbers, then set the total to 720."
g[2]["misconceptions"] = []
g[2]["guided_steps"] = [
    sayonly("A hexagon's angles add to (6 − 2) × 180 = 720°."),
    box("Add the x terms: 2x + 3x + x + x = ", 7, "Count every lot of x.", post="x"),
    box("Add all the numbers: 10 + 50 + 130 + 150 + 30 = ", 370, "Add the five constants."),
    box("So 7x + 370 = 720. Take 370 across: 720 − 370 = ", 350, "720 take away 370.", phase="substitute"),
    box("7x = 350, so x = 350 ÷ 7 = ", 50, "350 shared into 7.", done="So x = 50.", phase="substitute"),
    box("Check one angle: 3x + 10 = 3 × 50 + 10 = ", 160, "Rebuild an angle to test x.", done="All six angles then total 720°, so x = 50 is right.", phase="substitute"),
]
prepend(g[2], fig_hexagon(["2x", "3x+10", "x+50", "130°", "150°", "x+30"]))

# G3: a:b:c = 2:3:4 at a point, find b -> 120
g[3]["hint"] = "Split 360° into 2 + 3 + 4 = 9 parts; b takes 3 of them."
g[3]["misconceptions"] = [
    mc("used_180", 60, "Angles at a point add to 360°, not 180°. One part = 360 ÷ 9 = 40°, so b = 3 × 40 = 120°."),
    mc("gave_c", 160, "b is the 3-part share: 3 × 40 = 120°. 160° is c, the 4-part share."),
]
g[3]["guided_steps"] = [
    sayonly("Angles at a point add to 360°. Split it in the ratio 2 : 3 : 4."),
    box("Add the ratio parts: 2 + 3 + 4 = ", 9, "Total number of shares."),
    box("One part = 360 ÷ 9 = ", 40, "360 shared into 9.", phase="substitute"),
    box("b is 3 parts: 3 × 40 = ", 120, "b takes the middle share.", done="So b = 120°.", phase="substitute"),
    box("Check: 9 × 40 = ", 360, "All the parts should rebuild the full turn.", done="A full 360°, so b = 120° is right.", phase="substitute"),
]

# G4: triangle ratio 3:4:5, largest = 75
g[4]["hint"] = "Split 180° into 3 + 4 + 5 = 12 parts; the largest takes 5."
g[4]["misconceptions"] = [
    mc("used_360", 150, "A triangle's angles add to 180°, not 360°. One part = 180 ÷ 12 = 15°, largest = 5 × 15 = 75°."),
    mc("gave_smallest", 45, "The largest is the 5-part share: 5 × 15 = 75°. 45° is the smallest (3 parts)."),
]
g[4]["guided_steps"] = [
    sayonly("A triangle's angles add to 180°. Split it in the ratio 3 : 4 : 5."),
    box("Add the ratio parts: 3 + 4 + 5 = ", 12, "Total number of shares."),
    box("One part = 180 ÷ 12 = ", 15, "180 shared into 12.", phase="substitute"),
    box("The largest is 5 parts: 5 × 15 = ", 75, "Biggest ratio number is 5.", done="So the largest angle is 75°.", phase="substitute"),
    box("Check: 12 × 15 = ", 180, "All the parts should rebuild 180°.", done="Exactly 180°, so 75° is right.", phase="substitute"),
]

# ---------- tier descriptions ----------
pb["bronze_description"] = "One unknown angle found by subtracting from a known total."
pb["silver_description"] = "Polygon angle rules, parallel-line rules, and the exterior-angle fact."
pb["gold_description"] = "Form an equation from the angle facts, then solve for the unknown."

# ---------- tier_guides ----------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one missing angle from a total",
        "steps": [
            "Name the total: a straight line is <strong>180°</strong>, a point <strong>360°</strong>, a triangle <strong>180°</strong>, a quadrilateral <strong>360°</strong>.",
            "Add up the angles you already know.",
            "Subtract that from the total to get the missing angle.",
        ],
        "example": {
            "question": "A triangle has angles 30°, 90° and t. Find t.",
            "steps": [
                {"label": "Total", "content": "A triangle adds to 180°."},
                {"label": "Known", "content": "30 + 90 = 120"},
                {"label": "Subtract", "content": "180 − 120 = 60"},
                {"label": "Check", "content": "30 + 90 + 60 = 180 ✓"},
                {"label": "Answer", "content": "t = 60°", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: polygons, parallel lines and exterior angles",
        "steps": [
            "Regular polygon: exterior = <strong>360 ÷ n</strong>, and interior + exterior = <strong>180°</strong>.",
            "Interior angle sum = <strong>(n − 2) × 180</strong>.",
            "Parallel lines: alternate angles equal, co-interior add to 180°, corresponding equal.",
            "Exterior angle of a triangle = the two opposite interior angles added.",
        ],
        "example": {
            "question": "A regular polygon has an exterior angle of 40°. How many sides?",
            "steps": [
                {"label": "Rule", "content": "Exterior angles share 360°."},
                {"label": "Divide", "content": "360 ÷ 40 = 9"},
                {"label": "Check", "content": "40 × 9 = 360 ✓"},
                {"label": "Answer", "content": "9 sides", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: build an equation and solve",
        "steps": [
            "Write each angle in terms of x, using the right total or equal-angle rule.",
            "Add them to the correct total, or set equal expressions equal.",
            "Solve for x, then substitute back and check.",
        ],
        "example": {
            "question": "Angles 2x, 3x and 4x meet on a straight line. Find x.",
            "steps": [
                {"label": "Set up", "content": "2x + 3x + 4x = 180"},
                {"label": "Collect", "content": "9x = 180"},
                {"label": "Solve", "content": "x = 20"},
                {"label": "Check", "content": "40 + 60 + 80 = 180 ✓"},
                {"label": "Answer", "content": "x = 20°", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------- guided: opener + teach ----------
opener_svg = fig_straight_line("130°", "?", 50)
pd["guided"] = {
    "opener": {
        "display": opener_svg + '<br>A pencil rests on a perfectly flat table. The table top is a straight line, and one side of the pencil makes an angle of 130° with it.',
        "steps": [
            box("A straight line measures 180° in total. One angle is 130°, so the other is 180 − 130 = ", 50,
                "Take 130 away from 180."),
            sayonly("Now picture that pencil standing upright at the very centre of a clock face. Going all the way round the point is a full turn, 360°."),
            box("Three angles meet at that centre: 120°, 130° and one more. The missing one is 360 − 120 − 130 = ", 110,
                "Take both known angles from 360."),
            sayonly("<strong>That is the whole topic in two facts.</strong> Angles on a straight line add to <strong>180°</strong>; angles around a point add to <strong>360°</strong>. Every other rule today grows from these."),
        ],
    },
    "teach": {
        "bronze": {
            "display": fig_triangle(["50°", "60°", "t"]) + CAP + " A triangle has angles 50°, 60° and t. Find t.",
            "steps": [
                sayonly("Every triangle's three angles add up to the same total. Let us find t."),
                box("How many degrees inside a triangle? Type the total: ", 180, "Half a full turn."),
                box("Add the two known angles: 50 + 60 = ", 110, "50 plus 60."),
                box("Subtract from the total: 180 − 110 = ", 70, "180 take away 110.", done="That is t."),
                box("Check: 50 + 60 + 70 = ", 180, "Add all three back.", done="Back to 180°. That was the whole point: known angles away from the total."),
            ],
        },
        "silver": {
            "display": "A regular polygon has an interior angle of 150°. How many sides does it have?",
            "steps": [
                sayonly("For a regular polygon, the quickest route is through the exterior angle."),
                box("Interior + exterior = 180°, so exterior = 180 − 150 = ", 30, "180 take away 150."),
                box("The exterior angles share 360°, so sides = 360 ÷ 30 = ", 12, "360 divided by 30."),
                box("Check the exterior total: 30 × 12 = ", 360, "Should be one full turn.", done="A full 360°."),
                box("And back to the interior: 180 − 30 = ", 150, "Straight-line pair.", done="Matches the 150° we started with. The new move: go via the exterior angle."),
            ],
        },
        "gold": {
            "display": fig_parallel("4x + 5", "6x − 15", "corresponding") + CAP + " Two corresponding angles are 4x + 5 and 6x − 15. Find x.",
            "steps": [
                sayonly("Corresponding angles are equal, so \\(4x + 5 = 6x - 15\\). The new move: turn the words into one equation and solve."),
                box("Move the x terms: 6x − 4x = ", 2, "6 lots take away 4 lots.", post="x"),
                box("Move the numbers across: 5 + 15 = ", 20, "Both numbers cross and add."),
                box("So 2x = 20, x = 20 ÷ 2 = ", 10, "20 shared into 2.", done="That is x."),
                box("Check: 4 × 10 + 5 = ", 45, "Work out both expressions.", done="6 × 10 − 15 = 45 too, so x = 10 is right."),
            ],
        },
    },
}

json.dump(pd, io.open("lesson_geometry-L01.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written lesson_geometry-L01.json")
