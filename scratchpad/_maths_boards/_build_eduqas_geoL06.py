# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams conversion of eduqas geometry-L06
(Sine Rule, Cosine Rule & Area Formula). Bank rebuilt as single_value
numeric problems with figures; preserves related_videos/topic_links/
worked_examples from the live row byte-for-byte."""
import json, io, math, re
r = math.radians
MINUS = "−"  # unicode minus for student text

# ---------------------------------------------------------------------------
# SVG generator (reused from _gen_figs_L06.py, unchanged geometry engine)
# ---------------------------------------------------------------------------
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
            rr = 16.0
            a1 = (vx+d1x*rr, vy+d1y*rr); a2 = (vx+d2x*rr, vy+d2y*rr)
            cross = d1x*d2y - d1y*d2x
            sweep = 1 if cross > 0 else 0
            parts.append('<path d="M%.1f %.1f A%.0f %.0f 0 0 %d %.1f %.1f" fill="none" stroke="currentColor" stroke-width="1.3"/>' % (a1[0], a1[1], rr, rr, sweep, a2[0], a2[1]))
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

c = math.cos; sq = math.sqrt

# ---------------------------------------------------------------------------
# guided step builders
# ---------------------------------------------------------------------------
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint, "post": post}
    if say: d["say"] = say
    if done: d["done"] = done
    if phase: d["phase"] = phase
    return d

def say(s):
    return {"say": s}

def mis(expect, message, pattern="wrong_formula", note=None):
    d = {"check": "common", "expect": expect, "message": message, "pattern": pattern}
    if note: d["note"] = note
    return d

# ---------------------------------------------------------------------------
# BANK  (all single_value; every number fresh-solved in _solve_eduqas_geoL06.py)
# ---------------------------------------------------------------------------
bronze = []
silver = []
gold = []

# ---- BRONZE 0: sine rule, find side ----
bronze.append({
 "display": "Sine rule: \\(A = 30°\\), \\(a = 6\\), \\(B = 50°\\). Find \\(b\\) to 1 d.p.",
 "solutions": [9.2], "calculator": True, "input_type": "single_value",
 "hint": "Rearrange the sine rule to b = a times sinB divided by sinA.",
 "guided_steps": [
   say("Sine rule: \\(\\frac{b}{\\sin B} = \\frac{a}{\\sin A}\\), so b = a × sinB ÷ sinA. a = 6, A = 30°, B = 50°. sin50° = 0.7660, sin30° = 0.5."),
   box("a × sinB = 6 × 0.7660 = ?  (to 2 d.p.) ", 4.60, "Six times 0.7660."),
   box("Divide by sinA: 4.60 ÷ 0.5 = ?  (to 1 d.p.) ", 9.2, "Dividing by 0.5 doubles it.", phase="substitute", done="b ≈ 9.2."),
   box("Check the ratios balance: b ÷ sinB = 9.2 ÷ 0.7660 = ?  (to 1 d.p.) ", 12.0, "Nine point two over 0.766.", done="and a ÷ sinA = 6 ÷ 0.5 = 12 too, so it holds."),
 ],
 "misconceptions": [mis(3.9, "The ratio is upside down. b = a × sinB ÷ sinA = 6 × 0.766 ÷ 0.5 ≈ 9.2. Multiplying by sinA and dividing by sinB instead gives about 3.9.", note="6 sin30/sin50")],
})
# ---- BRONZE 1: sine rule, find side ----
bronze.append({
 "display": "Sine rule: \\(a = 10\\), \\(A = 45°\\), \\(B = 65°\\). Find \\(b\\) to 1 d.p.",
 "solutions": [12.8], "calculator": True, "input_type": "single_value",
 "hint": "b = a times sinB divided by sinA.",
 "guided_steps": [
   say("b = a × sinB ÷ sinA. a = 10, A = 45°, B = 65°. sin65° = 0.9063, sin45° = 0.7071 (4 d.p.)."),
   box("a × sinB = 10 × 0.9063 = ?  (to 2 d.p.) ", 9.06, "Ten times 0.9063."),
   box("Divide by sinA: 9.06 ÷ 0.7071 = ?  (to 1 d.p.) ", 12.8, "About 9.06 ÷ 0.71.", phase="substitute", done="b ≈ 12.8."),
   box("Sense check: B (65°) is bigger than A (45°), so b should be bigger than a = 10. Enter b again: ", 12.8, "You found b = 12.8.", done="12.8 is more than 10, so it fits."),
 ],
 "misconceptions": [mis(7.8, "The ratio is inverted. b = a × sinB ÷ sinA = 10 × 0.9063 ÷ 0.7071 ≈ 12.8. Dividing the other way gives about 7.8.", note="10 sin45/sin65")],
})
# ---- BRONZE 2: sine rule, find angle ----
bronze.append({
 "display": "Sine rule: \\(a = 8\\), \\(A = 40°\\), \\(b = 10\\). Find angle \\(B\\) to 1 d.p.",
 "solutions": [53.5], "calculator": True, "input_type": "single_value",
 "hint": "sinB = b times sinA divided by a, then inverse sine.",
 "guided_steps": [
   say("Sine rule for an angle: sinB = b × sinA ÷ a. a = 8, A = 40°, b = 10. sin40° = 0.6428 (4 d.p.)."),
   box("b × sinA = 10 × 0.6428 = ?  (to 3 d.p.) ", 6.428, "Ten times 0.6428."),
   box("sinB = 6.428 ÷ 8 = ?  (to 4 d.p.) ", 0.8035, "Divide by 8.", phase="substitute"),
   box("B = sin⁻¹(0.8035) = ?  (to 1 d.p.) ", 53.5, "Inverse sine of about 0.80.", done="B ≈ 53.5°."),
 ],
 "misconceptions": [mis(30.9, "sinB and a are the wrong way round. sinB = b × sinA ÷ a = 10 × 0.6428 ÷ 8 = 0.804, giving B ≈ 53.5°. Using 8 × sin40° ÷ 10 = 0.514 gives the wrong 30.9°.", note="8 sin40/10")],
})
# ---- BRONZE 3: sine rule, find side (replaces concept MC) ----
bronze.append({
 "display": "Sine rule: \\(A = 50°\\), \\(a = 9\\), \\(B = 40°\\). Find \\(b\\) to 1 d.p.",
 "solutions": [7.6], "calculator": True, "input_type": "single_value",
 "hint": "b = a times sinB divided by sinA.",
 "guided_steps": [
   say("b = a × sinB ÷ sinA. a = 9, A = 50°, B = 40°. sin40° = 0.6428, sin50° = 0.7660 (4 d.p.)."),
   box("a × sinB = 9 × 0.6428 = ?  (to 3 d.p.) ", 5.785, "Nine times 0.6428."),
   box("Divide by sinA: 5.785 ÷ 0.7660 = ?  (to 1 d.p.) ", 7.6, "About 5.79 ÷ 0.77.", phase="substitute", done="b ≈ 7.6."),
   box("Sense check: B (40°) is smaller than A (50°), so b should be shorter than a = 9. Enter b again: ", 7.6, "You found b = 7.6.", done="7.6 is less than 9, so it fits."),
 ],
 "misconceptions": [mis(10.7, "The ratio is inverted. b = a × sinB ÷ sinA = 9 × 0.6428 ÷ 0.7660 ≈ 7.6. Dividing the other way gives about 10.7.", note="9 sin50/sin40")],
})
# ---- BRONZE 4: area formula ----
bronze.append({
 "display": "Find the area of a triangle with sides 5 cm and 8 cm and included angle \\(30°\\).",
 "solutions": [10], "calculator": True, "input_type": "single_value",
 "hint": "Area is half of the two sides multiplied, times the sine of the angle between them.",
 "guided_steps": [
   say("Area of any triangle = \\(\\tfrac{1}{2}ab\\sin C\\). a = 5, b = 8, and the angle between them is C = 30°."),
   box("Multiply the two sides: 5 × 8 = ", 40, "Five eights."),
   box("Halve it (the ½ in the formula): 40 ÷ 2 = ", 20, "Half of 40.", phase="substitute"),
   box("Now multiply by sin30°, which is exactly 0.5: 20 × 0.5 = ", 10, "Half of 20.", done="Area = 10 cm²."),
 ],
 "misconceptions": [mis(20, "You may have left out the ½. Area is HALF of a × b × sinC: ½ × 5 × 8 × 0.5 = 10, not 20. Dropping the ½ doubles your answer.", note="5*8*sin30")],
})
# ---- BRONZE 5: sine rule, find side ----
bronze.append({
 "display": "Sine rule: \\(C = 80°\\), \\(c = 15\\), \\(A = 35°\\). Find \\(a\\) to 1 d.p.",
 "solutions": [8.7], "calculator": True, "input_type": "single_value",
 "hint": "a = c times sinA divided by sinC.",
 "guided_steps": [
   say("Match each side to its opposite angle: a = c × sinA ÷ sinC. c = 15, A = 35°, C = 80°. sin35° = 0.5736, sin80° = 0.9848 (4 d.p.)."),
   box("c × sinA = 15 × 0.5736 = ?  (to 2 d.p.) ", 8.60, "Fifteen times 0.5736."),
   box("Divide by sinC: 8.60 ÷ 0.9848 = ?  (to 1 d.p.) ", 8.7, "About 8.60 ÷ 0.98.", phase="substitute", done="a ≈ 8.7."),
   box("Sense check: A (35°) is the smallest angle, so a should be the shortest side (shorter than c = 15). Enter a again: ", 8.7, "You found a = 8.7.", done="8.7 is less than 15, so it fits."),
 ],
 "misconceptions": [mis(25.8, "The ratio is inverted. a = c × sinA ÷ sinC = 15 × 0.5736 ÷ 0.9848 ≈ 8.7. Dividing the other way gives about 25.8.", note="15 sin80/sin35")],
})
# ---- BRONZE 6: sine rule, find angle (replaces concept MC) ----
bronze.append({
 "display": "Sine rule: \\(a = 7\\), \\(A = 35°\\), \\(b = 9\\). Find angle \\(B\\) to 1 d.p.",
 "solutions": [47.5], "calculator": True, "input_type": "single_value",
 "hint": "sinB = b times sinA divided by a, then inverse sine.",
 "guided_steps": [
   say("sinB = b × sinA ÷ a. a = 7, A = 35°, b = 9. sin35° = 0.5736 (4 d.p.)."),
   box("b × sinA = 9 × 0.5736 = ?  (to 3 d.p.) ", 5.162, "Nine times 0.5736."),
   box("sinB = 5.162 ÷ 7 = ?  (to 4 d.p.) ", 0.7375, "Divide by 7.", phase="substitute"),
   box("B = sin⁻¹(0.7375) = ?  (to 1 d.p.) ", 47.5, "Inverse sine of about 0.74.", done="B ≈ 47.5°."),
 ],
 "misconceptions": [mis(26.5, "sinB and a are swapped. sinB = b × sinA ÷ a = 9 × 0.5736 ÷ 7 = 0.738, so B ≈ 47.5°. Using 7 × sin35° ÷ 9 = 0.446 gives the wrong 26.5°.", note="7 sin35/9")],
})
# ---- BRONZE 7: area formula, right angle (non-calc) ----
bronze.append({
 "display": "Find the area of a triangle with sides 12 cm and 7 cm and included angle \\(90°\\).",
 "solutions": [42], "calculator": False, "input_type": "single_value",
 "hint": "Use Area = half times a times b times sinC, with sin90 equal to 1.",
 "guided_steps": [
   say("Area = \\(\\tfrac{1}{2}ab\\sin C\\). a = 12, b = 7, C = 90°, and sin90° = 1."),
   box("Multiply the two sides: 12 × 7 = ", 84, "Twelve sevens."),
   box("Halve it: 84 ÷ 2 = ", 42, "Half of 84.", phase="substitute"),
   box("Multiply by sin90° = 1: 42 × 1 = ", 42, "Anything times 1 is itself.", done="Area = 42 cm². A right angle makes sinC = 1, so it is just ½ base × height."),
 ],
 "misconceptions": [mis(84, "You may have left out the ½. Area = ½ × 12 × 7 × sin90° = ½ × 84 × 1 = 42, not 84. Dropping the ½ doubles it.", note="12*7*sin90")],
})

# ---- SILVER 0: cosine rule, find side ----
silver.append({
 "display": "Cosine rule: \\(b = 7\\), \\(c = 10\\), \\(A = 60°\\). Find \\(a\\) to 1 d.p.",
 "solutions": [8.9], "calculator": True, "input_type": "single_value",
 "hint": "a squared = b squared plus c squared minus 2bc times cosA, then square root.",
 "guided_steps": [
   say("Cosine rule for a side: \\(a^2 = b^2 + c^2 - 2bc\\cos A\\). b = 7, c = 10, A = 60°. cos60° = 0.5, and 2bc = 140."),
   box("b² + c² = 49 + 100 = ", 149, "Add the two squares."),
   box("The last term, 2bc × cosA = 140 × 0.5 = ", 70, "Half of 140."),
   box("a² = 149 " + MINUS + " 70 = ", 79, "149 take away 70.", phase="substitute"),
   box("a = √79 = ?  (to 1 d.p.) ", 8.9, "Square root of 79 is about 8.9.", done="a ≈ 8.9 cm."),
 ],
 "misconceptions": [mis(12.2, "You dropped the " + MINUS + "2bc·cosA term. a² = 49 + 100 " + MINUS + " 140cos60° = 149 " + MINUS + " 70 = 79, so a ≈ 8.9, not √149 ≈ 12.2.", note="sqrt149")],
})
# ---- SILVER 1: cosine rule, find angle ----
silver.append({
 "display": "Cosine rule: \\(a = 5\\), \\(b = 8\\), \\(c = 9\\). Find angle \\(A\\) to 1 d.p.",
 "solutions": [33.6], "calculator": True, "input_type": "single_value",
 "hint": "cosA = (b squared plus c squared minus a squared) divided by 2bc, then inverse cosine.",
 "guided_steps": [
   say("Cosine rule for an angle: \\(\\cos A = \\frac{b^2 + c^2 - a^2}{2bc}\\). Side a is opposite A. a = 5, b = 8, c = 9, so 2bc = 144."),
   box("Top line, b² + c² " + MINUS + " a² = 64 + 81 " + MINUS + " 25 = ", 120, "64 + 81 is 145, then minus 25."),
   box("cosA = 120 ÷ 144 = ?  (to 4 d.p.) ", 0.8333, "120 over 144.", phase="substitute"),
   box("A = cos⁻¹(0.8333) = ?  (to 1 d.p.) ", 33.6, "Inverse cosine of about 0.83.", done="A ≈ 33.6°."),
 ],
 "misconceptions": [mis(84.3, "Keep the side opposite your angle as the " + MINUS + "a² term. Here a = 5 is opposite A, so top line = 64 + 81 " + MINUS + " 25 = 120 and A ≈ 33.6°. Putting c = 9 as the subtracted square finds the angle opposite 9 instead: 84.3°.", note="angle opp 9")],
})
# ---- SILVER 2: area formula ----
silver.append({
 "display": "Find the area of a triangle with sides 11 cm and 14 cm and included angle \\(42°\\). Give it to 1 d.p.",
 "solutions": [51.5], "calculator": True, "input_type": "single_value",
 "hint": "Half of 11 times 14, then multiply by sin42.",
 "guided_steps": [
   say("Area = \\(\\tfrac{1}{2}ab\\sin C\\). a = 11, b = 14, C = 42°, and sin42° = 0.6691 (4 d.p.)."),
   box("The two sides: 11 × 14 = ", 154, "Eleven fourteens."),
   box("Halve it: 154 ÷ 2 = ", 77, "Half of 154.", phase="substitute"),
   box("Multiply by sin42°: 77 × 0.6691 = ?  (to 1 d.p.) ", 51.5, "About 77 × 0.67.", done="Area ≈ 51.5 cm²."),
 ],
 "misconceptions": [mis(103.0, "That is a × b × sinC without the ½. Halve it: ½ × 11 × 14 × sin42° ≈ 51.5 cm².", note="11*14*sin42")],
})
# ---- SILVER 3: cosine rule, find angle (replaces yes/no concept) ----
silver.append({
 "display": "A triangle has sides 6, 8 and 10. Use the cosine rule to find its largest angle (opposite side 10) to 1 d.p.",
 "solutions": [90], "calculator": True, "input_type": "single_value",
 "hint": "The largest angle is opposite the longest side; cosC = (a squared plus b squared minus c squared) over 2ab.",
 "guided_steps": [
   say("The largest angle sits opposite the longest side, 10. Call it C. \\(\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}\\) with a = 6, b = 8, c = 10, so 2ab = 96."),
   box("Top line, a² + b² " + MINUS + " c² = 36 + 64 " + MINUS + " 100 = ", 0, "36 + 64 is 100, then minus 100."),
   box("cosC = 0 ÷ 96 = ", 0, "Zero divided by anything is 0.", phase="substitute"),
   box("C = cos⁻¹(0) = ?  degrees ", 90, "The angle whose cosine is 0 is a right angle.", done="C = 90°. The 6, 8, 10 triangle is right-angled (6² + 8² = 10²)."),
 ],
 "misconceptions": [mis(36.9, "That is an angle opposite one of the shorter sides. The largest angle is opposite the longest side (10): cosC = 0, so C = 90°. The angle opposite 6 works out as 36.9°.", note="angle opp 6")],
})
# ---- SILVER 4: cosine rule, obtuse SAS side (replaces trick MC) ----
silver.append({
 "display": "Two sides of a triangle are 9 cm and 13 cm with an included angle of \\(110°\\). Find the third side to 1 d.p.",
 "solutions": [18.2], "calculator": True, "input_type": "single_value",
 "hint": "Third side squared = 9 squared + 13 squared minus 2 times 9 times 13 times cos110, and cos110 is negative.",
 "guided_steps": [
   say("Cosine rule for a side: \\(x^2 = 9^2 + 13^2 - 2(9)(13)\\cos 110°\\). cos110° = " + MINUS + "0.3420, and 2 × 9 × 13 = 234."),
   box("9² + 13² = 81 + 169 = ", 250, "Add the two squares."),
   box("The last term, 234 × cos110° = 234 × (" + MINUS + "0.3420) = ?  (to 1 d.p.) ", -80.0, "234 times minus 0.342."),
   box("x² = 250 " + MINUS + " (" + MINUS + "80.0) = 250 + 80.0 = ", 330, "Subtracting a negative adds it on.", phase="substitute"),
   box("x = √330 = ?  (to 1 d.p.) ", 18.2, "Square root of 330 is about 18.2.", done="x ≈ 18.2 cm. The obtuse angle makes the third side longer than either given side, which fits."),
 ],
 "misconceptions": [mis(13.0, "Check the sign of cos110°. It is " + MINUS + "0.342, so the last term is " + MINUS + "80.0 and x² = 250 + 80.0 = 330, giving x ≈ 18.2. Treating cos110° as +0.342 gives x² = 170 and the wrong 13.0 cm.", note="sign error")],
})
# ---- SILVER 5: area formula ----
silver.append({
 "display": "Find the area of a triangle with \\(a = 15\\), \\(b = 20\\) and included angle \\(C = 75°\\). Give it to 1 d.p.",
 "solutions": [144.9], "calculator": True, "input_type": "single_value",
 "hint": "Half of 15 times 20, then multiply by sin75.",
 "guided_steps": [
   say("Area = \\(\\tfrac{1}{2}ab\\sin C\\). a = 15, b = 20, C = 75°, and sin75° = 0.9659 (4 d.p.)."),
   box("The two sides: 15 × 20 = ", 300, "Fifteen twenties."),
   box("Halve it: 300 ÷ 2 = ", 150, "Half of 300.", phase="substitute"),
   box("Multiply by sin75°: 150 × 0.9659 = ?  (to 1 d.p.) ", 144.9, "About 150 × 0.97.", done="Area ≈ 144.9 cm²."),
 ],
 "misconceptions": [mis(289.8, "That is a × b × sinC without the ½. Halve it: ½ × 15 × 20 × sin75° ≈ 144.9 cm².", note="15*20*sin75")],
})
# ---- SILVER 6: cosine rule, obtuse angle (FIX stored 111.8 -> 106.6) ----
silver.append({
 "display": "Cosine rule: \\(a = 4\\), \\(b = 7\\), \\(c = 9\\). Find angle \\(C\\) to 1 d.p.",
 "solutions": [106.6], "calculator": True, "input_type": "single_value",
 "hint": "cosC = (a squared plus b squared minus c squared) divided by 2ab, then inverse cosine.",
 "guided_steps": [
   say("Cosine rule for an angle: \\(\\cos C = \\frac{a^2 + b^2 - c^2}{2ab}\\). Side c is opposite C. a = 4, b = 7, c = 9, so 2ab = 56."),
   box("Top line, a² + b² " + MINUS + " c² = 16 + 49 " + MINUS + " 81 = ", -16, "16 + 49 is 65, then minus 81.", say=None),
   box("cosC = (" + MINUS + "16) ÷ 56 = ?  (to 4 d.p.) ", -0.2857, "Minus 16 over 56.", phase="substitute"),
   box("C = cos⁻¹(" + MINUS + "0.2857) = ?  (to 1 d.p.) ", 106.6, "A negative cosine gives an obtuse angle.", done="C ≈ 106.6°, just over a right angle."),
 ],
 "misconceptions": [mis(73.4, "Watch the sign of the top line. a² + b² " + MINUS + " c² = 16 + 49 " + MINUS + " 81 = " + MINUS + "16, not +16. A negative cosine means C is obtuse: C ≈ 106.6°. Dropping the minus sign gives the wrong 73.4°.", note="sign +16 -> 73.4")],
})

# ---- GOLD 0: bearings, cosine rule (FIX stored 16.6 -> 16.5) ----
gold.append({
 "display": "Two ships leave a port. Ship A sails 10 km on a bearing of \\(040°\\); ship B sails 15 km on a bearing of \\(120°\\). Find the distance between the two ships to 1 d.p.",
 "solutions": [16.5], "calculator": True, "input_type": "single_value",
 "hint": "The angle between the paths is 120 minus 40; then use the cosine rule.",
 "guided_steps": [
   say("The two paths leave the same port, so the angle between them is the difference in bearings: 120° " + MINUS + " 40°. Then use the cosine rule with the two distances."),
   box("Angle at the port = 120 " + MINUS + " 40 = ?  degrees ", 80, "Subtract the bearings."),
   box("d² = 10² + 15² " + MINUS + " 2(10)(15)cos80°. First 10² + 15² = 100 + 225 = ", 325, "Add the two squares."),
   box("The last term, 300 × cos80° = 300 × 0.1736 = ?  (to 1 d.p.) ", 52.1, "300 times 0.1736."),
   box("d² = 325 " + MINUS + " 52.1 = ?  (to 1 d.p.) ", 272.9, "325 take away 52.1.", phase="substitute"),
   box("d = √272.9 = ?  (to 1 d.p.) ", 16.5, "Square root of about 273 is 16.5.", done="The ships are about 16.5 km apart."),
 ],
 "misconceptions": [mis(18.0, "You need the cosine rule, not Pythagoras. The angle between the paths is 80°, not 90°, so d² = 325 " + MINUS + " 52.1 = 272.9 and d ≈ 16.5 km. Treating it as right-angled gives √325 ≈ 18.0 km.", note="pythag sqrt325")],
})
# ---- GOLD 1: SSS -> angle -> area ----
gold.append({
 "display": "A triangle has sides 13 cm, 14 cm and 15 cm. Find its area to the nearest whole number.",
 "solutions": [84], "calculator": True, "input_type": "single_value",
 "hint": "Find the angle between two sides with the cosine rule, then use area = half ab sinC.",
 "guided_steps": [
   say("With three sides and no angle, first find the angle between 13 and 14 (opposite 15) using the cosine rule, then use the area formula. \\(\\cos C = \\frac{13^2 + 14^2 - 15^2}{2(13)(14)}\\), and 2 × 13 × 14 = 364."),
   box("Top line, 13² + 14² " + MINUS + " 15² = 169 + 196 " + MINUS + " 225 = ", 140, "169 + 196 is 365, then minus 225."),
   box("cosC = 140 ÷ 364 = ?  (to 4 d.p.) ", 0.3846, "140 over 364."),
   box("C = cos⁻¹(0.3846) = ?  (to 1 d.p.) ", 67.4, "Inverse cosine of about 0.38.", phase="substitute"),
   box("Now area = ½ × 13 × 14 × sin67.4° = 91 × 0.9231 = ?  (nearest whole number) ", 84, "Ninety-one times about 0.92.", done="Area ≈ 84 cm²."),
 ],
 "misconceptions": [mis(91, "There is no right angle, so ½ × base × height using two sides is wrong. Find an angle first: area = ½ × 13 × 14 × sin67.4° ≈ 84 cm². The value 91 is just ½ × 13 × 14, assuming a right angle.", note="halfbh 13*14/2")],
})
# ---- GOLD 2: cosine rule, obtuse angle side (FIX stored 14.8 -> 14.7) ----
gold.append({
 "display": "In triangle PQR, \\(PQ = 8\\) cm, \\(QR = 11\\) cm and angle \\(PQR = 100°\\). Find \\(PR\\) to 1 d.p.",
 "solutions": [14.7], "calculator": True, "input_type": "single_value",
 "hint": "PR squared = 8 squared + 11 squared minus 2 times 8 times 11 times cos100, and cos100 is negative.",
 "guided_steps": [
   say("Angle Q is between PQ and QR, so PR is opposite it: \\(PR^2 = 8^2 + 11^2 - 2(8)(11)\\cos 100°\\). cos100° = " + MINUS + "0.1736, and 2 × 8 × 11 = 176."),
   box("8² + 11² = 64 + 121 = ", 185, "Add the two squares."),
   box("The last term, 176 × cos100° = 176 × (" + MINUS + "0.1736) = ?  (to 1 d.p.) ", -30.6, "176 times minus 0.1736."),
   box("PR² = 185 " + MINUS + " (" + MINUS + "30.6) = 185 + 30.6 = ?  (to 1 d.p.) ", 215.6, "Subtracting a negative adds it on.", phase="substitute"),
   box("PR = √215.6 = ?  (to 1 d.p.) ", 14.7, "Square root of about 216 is 14.7.", done="PR ≈ 14.7 cm."),
 ],
 "misconceptions": [mis(12.4, "cos100° is negative (" + MINUS + "0.1736), so the last term adds on: PR² = 185 + 30.6 = 215.6 and PR ≈ 14.7. Treating cos100° as positive gives PR² = 154.4 and the wrong 12.4 cm.", note="sign error")],
})
# ---- GOLD 3: area backwards -> angle ----
gold.append({
 "display": "A triangle has area 30 cm² and two sides of 10 cm and 8 cm. Find the angle between those two sides to 1 d.p.",
 "solutions": [48.6], "calculator": True, "input_type": "single_value",
 "hint": "Rearrange the area formula: sinC = 2 times area divided by ab, then inverse sine.",
 "guided_steps": [
   say("Work backwards from the area. Area = \\(\\tfrac{1}{2}ab\\sin C\\), so sinC = 2 × Area ÷ (a × b). Area = 30, a = 10, b = 8."),
   box("a × b = 10 × 8 = ", 80, "Ten eights."),
   box("sinC = (2 × 30) ÷ 80 = 60 ÷ 80 = ", 0.75, "Sixty over 80.", phase="substitute"),
   box("C = sin⁻¹(0.75) = ?  (to 1 d.p.) ", 48.6, "Inverse sine of 0.75.", done="The included angle is about 48.6°."),
 ],
 "misconceptions": [mis(22.0, "You may have left out the ½. Area = ½ × a × b × sinC, so sinC = 2 × 30 ÷ 80 = 0.75 and C ≈ 48.6°. Using 30 ÷ 80 = 0.375 (no ½) gives the wrong 22.0°.", note="30/80")],
})
# ---- GOLD 4: parallelogram area ----
gold.append({
 "display": "A parallelogram has sides 6 cm and 10 cm with an angle of \\(70°\\) between them. Find its area to 1 d.p.",
 "solutions": [56.4], "calculator": True, "input_type": "single_value",
 "hint": "A parallelogram is two triangles: work out ab times sinC (no half).",
 "guided_steps": [
   say("A parallelogram is two identical triangles. Each triangle is \\(\\tfrac{1}{2}\\times 6\\times 10\\times\\sin 70°\\). sin70° = 0.9397 (4 d.p.)."),
   box("One triangle first: ½ × 6 × 10 = ", 30, "Half of 6 × 10."),
   box("That triangle's area: 30 × 0.9397 = ?  (to 1 d.p.) ", 28.2, "About 30 × 0.94.", phase="substitute"),
   box("Two triangles make the parallelogram: 28.2 × 2 = ?  (to 1 d.p.) ", 56.4, "Double one triangle.", done="Area ≈ 56.4 cm², the same as a × b × sin70°."),
 ],
 "misconceptions": [mis(28.2, "That is the area of ONE triangle (½ × 6 × 10 × sin70°). A parallelogram is two of them, so double it: 6 × 10 × sin70° ≈ 56.4 cm².", note="one triangle")],
})

pb = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description": "Use the sine rule for a missing side or angle, or the area formula ½ab sinC with a nice angle.",
 "silver_description": "Pick the cosine rule (a side or an angle) or the area formula, then rearrange to the unknown.",
 "gold_description": "Multi-step problems: derive an angle from bearings or three sides, work backwards from an area, or adapt the formula to a new shape.",
}

# ---------------------------------------------------------------------------
# guided (opener + teach)
# ---------------------------------------------------------------------------
opener = {
 "label": "Before any formula",
 "display": ("A right-angled triangular flag.<br>The two straight edges meeting at the corner are 6 m and 8 m."),
 "steps": [
   box("A triangular flag. Forget formulas: a right-angled triangle is exactly half of a rectangle. The 6 m by 8 m rectangle has area 48 m², so the triangle's area = ",
       24, "Half of 48.", post=" m²", say="A triangular flag. No formulas yet, just common sense."),
   say("You just used ½ × base × height. That works because the corner is 90°. Tilt the corner and the triangle squashes: its true height shrinks to (side × sinC). So for ANY angle, <strong>Area = ½ × a × b × sinC</strong>. At 90°, sin90° = 1, and you get ½ base × height back."),
   box("Same edges 6 m and 8 m, but now they meet at 30°. Area = ½ × 6 × 8 × sin30°. Since sin30° = 0.5: 24 × 0.5 = ",
       12, "Half of 24.", post=" m²"),
   say("That sinC factor is the whole idea. It powers the area formula, the sine rule and the cosine rule, stretching right-angle trig to every triangle. Algebra just labels the sides a, b, c opposite angles A, B, C."),
 ],
}

teach = {
 "bronze": {
  "label": "Together: the sine rule for a side",
  "display": "Find side \\(b\\) when \\(a = 8\\), \\(A = 30°\\), \\(B = 90°\\). Use the sine rule.",
  "steps": [
    say("Sine rule: \\(\\frac{b}{\\sin B} = \\frac{a}{\\sin A}\\), so b = a × sinB ÷ sinA. a = 8, A = 30°, B = 90°, with sin90° = 1 and sin30° = 0.5."),
    box("First a × sinB = 8 × 1 = ", 8, "Eight times one."),
    box("Now divide by sinA: 8 ÷ 0.5 = ", 16, "Dividing by 0.5 doubles it.", done="b = 16."),
    box("Check the ratios balance: b ÷ sinB = 16 ÷ 1 = ", 16, "Sixteen over one."),
    box("and a ÷ sinA = 8 ÷ 0.5 = ", 16, "Eight over 0.5.", done="Both ratios equal 16, so the sine rule holds. That is the whole move: match each side to its opposite angle, then rearrange."),
  ],
 },
 "silver": {
  "label": "Together: the cosine rule for a side",
  "display": "Find side \\(c\\) when \\(a = 5\\), \\(b = 8\\), \\(C = 60°\\). Use the cosine rule.",
  "steps": [
    say("Cosine rule for a side: \\(c^2 = a^2 + b^2 - 2ab\\cos C\\). a = 5, b = 8, C = 60°, and cos60° = 0.5."),
    box("a² + b² = 25 + 64 = ", 89, "Add the two squares."),
    box("2ab = 2 × 5 × 8 = ", 80, "Two times 5 times 8."),
    box("c² = 89 " + MINUS + " 80 × 0.5 = 89 " + MINUS + " 40 = ", 49, "80 × 0.5 = 40, then subtract."),
    box("c = √49 = ", 7, "Square root of 49.", done="c = 7 cm. New move: the cosine rule finds the third side from two sides and the angle between them."),
  ],
 },
 "gold": {
  "label": "Together: the ambiguous case",
  "display": "Find the obtuse angle \\(B\\) when \\(a = 9\\), \\(b = 12\\), \\(A = 35°\\).",
  "steps": [
    say("The ambiguous case. sinB = b × sinA ÷ a = 12 × sin35° ÷ 9. sin35° = 0.5736 (4 d.p.)."),
    box("b × sinA = 12 × 0.5736 = ?  (to 4 d.p.) ", 6.8832, "Twelve times 0.5736."),
    box("sinB = 6.8832 ÷ 9 = ?  (to 4 d.p.) ", 0.7648, "Divide by 9."),
    box("The acute answer: sin⁻¹(0.7648) = ?  (to 1 d.p.) ", 49.9, "Inverse sine of about 0.76."),
    box("The obtuse partner: 180 " + MINUS + " 49.9 = ", 130.1, "180 take away 49.9.", done="B = 130.1°. Any sine has TWO angles between 0° and 180°; always ask which one the triangle needs."),
  ],
 },
}

# ---------------------------------------------------------------------------
# tier_guides
# ---------------------------------------------------------------------------
def exstep(label, content, ans=False):
    d = {"label": label, "content": content}
    if ans: d["isAnswer"] = True; d["is_answer"] = True
    return d

tier_guides = {
 "bronze": {
  "title": "Bronze: one formula, straight in",
  "steps": [
    "Match each side to the angle opposite it. The sine rule pairs them: <strong>b = a sinB ÷ sinA</strong>. To find an angle instead, use sinB = b sinA ÷ a and finish with inverse sine.",
    "For an area from two sides and the angle between them: <strong>Area = ½ab sinC</strong>. Multiply the sides, halve, then times the sine.",
    "Keep sin90° = 1 and sin30° = 0.5 in mind; they turn up a lot.",
  ],
  "example": {
   "question": "Find side b when a = 6, A = 30°, B = 50°.",
   "steps": [
     exstep("Sine rule", "<p>b = \\(\\frac{6\\sin 50°}{\\sin 30°}\\) = \\(\\frac{6\\times 0.766}{0.5}\\)</p>"),
     exstep("Work", "<p>= 4.60 ÷ 0.5</p>"),
     exstep("Check", "<p>B (50°) is bigger than A (30°), so b should be longer than 6</p>"),
     exstep("Answer", "<p>b ≈ 9.2 cm</p>", ans=True),
   ],
  },
 },
 "silver": {
  "title": "Silver: pick the rule and rearrange",
  "steps": [
    "Two sides and the angle between them, or all three sides: <strong>cosine rule</strong>. For a side, \\(a^2 = b^2 + c^2 - 2bc\\cos A\\), then square root.",
    "For an angle from three sides, \\(\\cos A = \\frac{b^2 + c^2 - a^2}{2bc}\\), then inverse cosine. Keep the side opposite your angle as the " + MINUS + "a² term.",
    "A negative cosine means the angle is obtuse (over 90°), so watch the sign of the top line.",
  ],
  "example": {
   "question": "Find side a when b = 7, c = 10, A = 60°.",
   "steps": [
     exstep("Cosine rule", "<p>\\(a^2 = 49 + 100 - 2(7)(10)\\cos 60°\\)</p>"),
     exstep("Work", "<p>= 149 " + MINUS + " 70 = 79</p>"),
     exstep("Check", "<p>\\(a = \\sqrt{79}\\), which sits between 7 and 10 plus a bit</p>"),
     exstep("Answer", "<p>a ≈ 8.9 cm</p>", ans=True),
   ],
  },
 },
 "gold": {
  "title": "Gold: derive, reverse and adapt",
  "steps": [
    "Bearings: the angle between two paths from one point is the difference in bearings. Then reach for the cosine rule.",
    "Backwards from an area: rearrange to sinC = 2 × Area ÷ ab. Three sides but no angle: cosine rule for an angle first, then area = ½ab sinC.",
    "New shapes reuse the same idea: a parallelogram is just two triangles, so its area is ab sinC (no half).",
  ],
  "example": {
   "question": "A parallelogram has sides 6 cm and 10 cm with a 70° angle. Find its area.",
   "steps": [
     exstep("One triangle", "<p>½ × 6 × 10 × sin70° = 30 × 0.9397</p>"),
     exstep("Work", "<p>= 28.2 cm² for one triangle</p>"),
     exstep("Check", "<p>A parallelogram is two triangles, so double it</p>"),
     exstep("Answer", "<p>Area ≈ 56.4 cm²</p>", ans=True),
   ],
  },
 },
}

# ---------------------------------------------------------------------------
# method_card (slim reference)
# ---------------------------------------------------------------------------
method_card = {
 "title": "Sine Rule, Cosine Rule & Area Formula",
 "steps": [
   "Label sides a, b, c opposite angles A, B, C.",
   "A side with its opposite angle known: sine rule, a ÷ sinA = b ÷ sinB.",
   "Two sides and the angle between them: Area = ½ab sinC, or cosine rule for the third side.",
   "All three sides: cosine rule rearranged gives an angle.",
 ],
 "content": "<p>These tools work in <strong>any</strong> triangle, not just right-angled ones.</p><p><strong>Area</strong> = \\(\\tfrac{1}{2}ab\\sin C\\) uses two sides and the angle between them.</p><p><strong>Sine rule</strong> pairs each side with its opposite angle: use it when you know one such pair plus one more side or angle.</p><p><strong>Cosine rule</strong> covers the rest: two sides and the included angle to find the third side, or all three sides to find an angle. A negative cosine gives an obtuse angle, so check the sign.</p>",
 "example": "<p><strong>Find a when b = 7, c = 10, A = 60°.</strong></p><p>\\(a^2 = 49 + 100 - 2(7)(10)\\cos 60° = 149 - 70 = 79\\), so \\(a = \\sqrt{79} \\approx 8.9\\) cm.</p>",
}

# ---------------------------------------------------------------------------
# FIGURES
# ---------------------------------------------------------------------------
def prepend(display, svg): return svg + CAP + display

# helper: full triangle from one side + two angles (sine rule) -> all 3 sides
def tri_from_2ang(sideval, sideAngle, otherAngle):
    # returns (a,b,c) with a opp A etc; caller maps
    pass

added = []
FIG = {}
sin = math.sin

# opener: right-angle flag legs 6 and 8
FIG['opener'] = render([(0.0, 0.0), (8.0, 0.0), (0.0, 6.0)],
    [(0, 1, "8 m"), (2, 0, "6 m"), (1, 2, None)], [(0, None, True)],
    ["Area = ?"], "Right-angled triangular flag with legs 8 m and 6 m; area unknown")

# teach_bronze: a=8 opp A=30, right angle B=90, find b (opp B). C=60. c=8 sin60/sin30
tb_c = 8*sin(r(60))/sin(r(30))
FIG['teach_bronze'] = tri(8, 16, tb_c, "8 cm", "b = ?", None,
    ("30°", False), ("", True), None, [],
    "Triangle with a right angle, side 8 cm opposite a 30 degree angle, and unknown side b")
# teach_silver: sides a=5,b=8 meet at C=60, opp side c=7
FIG['teach_silver'] = tri(5, 8, 7, "5 cm", "8 cm", "c = ?",
    None, None, ("60°", False), [],
    "Triangle with sides 5 cm and 8 cm meeting at a 60 degree angle; opposite side c unknown")
# teach_gold: a=9 opp A=35, b=12 opp obtuse B=130.1, find B (?). C=14.9
tg_c = 9*sin(r(180-35-130.1))/sin(r(35))
FIG['teach_gold'] = tri(9, 12, tg_c, "9 cm", "12 cm", None,
    ("35°", False), ("?", False), None, [],
    "Triangle with side 9 cm opposite a 35 degree angle and side 12 cm opposite the obtuse angle marked with a question mark")

# --- bronze problem figures ---
# b0 A=30,a=6,B=50 -> b (opp B). C=100. a=6, b, c
b0b = 6*sin(r(50))/sin(r(30)); b0c = 6*sin(r(100))/sin(r(30))
FIG[('bronze',0)] = tri(6, b0b, b0c, "6 cm", "b = ?", None,
    ("30°", False), ("50°", False), None, [],
    "Triangle with side 6 cm opposite a 30 degree angle, a 50 degree angle, and unknown side b")
# b1 a=10,A=45,B=65 -> b. C=70
b1b = 10*sin(r(65))/sin(r(45)); b1c = 10*sin(r(70))/sin(r(45))
FIG[('bronze',1)] = tri(10, b1b, b1c, "10 cm", "b = ?", None,
    ("45°", False), ("65°", False), None, [],
    "Triangle with side 10 cm opposite a 45 degree angle, a 65 degree angle, and unknown side b")
# b2 a=8,A=40,b=10 -> B(opp b, marked ?). C=180-40-53.47=86.53
b2C = 180-40-53.47; b2c = 8*sin(r(b2C))/sin(r(40))
FIG[('bronze',2)] = tri(8, 10, b2c, "8 cm", "10 cm", None,
    ("40°", False), ("?", False), None, [],
    "Triangle with side 8 cm opposite a 40 degree angle and side 10 cm opposite the unknown angle B")
# b3 A=50,a=9,B=40 -> b. C=90
b3b = 9*sin(r(40))/sin(r(50)); b3c = 9*sin(r(90))/sin(r(50))
FIG[('bronze',3)] = tri(9, b3b, b3c, "9 cm", "b = ?", None,
    ("50°", False), ("40°", False), None, [],
    "Triangle with side 9 cm opposite a 50 degree angle, a 40 degree angle, and unknown side b")
# b4 area 5,8,30
FIG[('bronze',4)] = tri(5, 8, sq(25+64-80*c(r(30))), "5 cm", "8 cm", None,
    None, None, ("30°", False), ["Area = ?"],
    "Triangle with sides 5 cm and 8 cm meeting at a 30 degree angle; area unknown")
# b5 C=80,c=15,A=35 -> a(opp A). B=65. a=15 sin35/sin80, b=15 sin65/sin80
b5a = 15*sin(r(35))/sin(r(80)); b5b = 15*sin(r(65))/sin(r(80))
FIG[('bronze',5)] = tri(b5a, b5b, 15, "a = ?", None, "15 cm",
    ("35°", False), None, ("80°", False), [],
    "Triangle with side 15 cm opposite an 80 degree angle, a 35 degree angle, and unknown side a")
# b6 a=7,A=35,b=9 -> B (opp b, ?). C=180-35-47.5=97.5
b6C = 180-35-47.5; b6c = 7*sin(r(b6C))/sin(r(35))
FIG[('bronze',6)] = tri(7, 9, b6c, "7 cm", "9 cm", None,
    ("35°", False), ("?", False), None, [],
    "Triangle with side 7 cm opposite a 35 degree angle and side 9 cm opposite the unknown angle B")
# b7 area 12,7,90
FIG[('bronze',7)] = tri(12, 7, sq(144+49), "12 cm", "7 cm", None,
    None, None, ("", True), ["Area = ?"],
    "Right-angled triangle with sides 12 cm and 7 cm meeting at the right angle; area unknown")

# --- silver problem figures ---
# s0 cosine side b=7,c=10,A=60 -> a. sides a(opp A, ?),b=7,c=10
s0a = sq(49+100-140*c(r(60)))
FIG[('silver',0)] = tri(s0a, 7, 10, "a = ?", "7 cm", "10 cm",
    ("60°", False), None, None, [],
    "Triangle with sides 7 cm and 10 cm meeting at a 60 degree angle; opposite side a unknown")
# s1 a=5,b=8,c=9 find A(opp a, ?)
FIG[('silver',1)] = tri(5, 8, 9, "5", "8", "9", ("?", False), None, None, [],
    "Triangle with sides 5, 8 and 9; angle A opposite side 5 unknown")
# s2 area 11,14,42
FIG[('silver',2)] = tri(11, 14, sq(121+196-2*11*14*c(r(42))), "11 cm", "14 cm", None,
    None, None, ("42°", False), ["Area = ?"],
    "Triangle with sides 11 cm and 14 cm meeting at a 42 degree angle; area unknown")
# s3 sides 6,8,10 largest angle opp 10 (?). a=6,b=8,c=10 -> angle C at vertex opp c
FIG[('silver',3)] = tri(6, 8, 10, "6", "8", "10", None, None, ("?", False), [],
    "Triangle with sides 6, 8 and 10; largest angle opposite side 10 unknown")
# s4 sides 9,13 angle 110 between, third x opp 110. Put A=110 between b=9,c=13; a=x
s4a = sq(81+169-2*9*13*c(r(110)))
FIG[('silver',4)] = tri(s4a, 9, 13, "x = ?", "9 cm", "13 cm",
    ("110°", False), None, None, [],
    "Triangle with sides 9 cm and 13 cm meeting at a 110 degree angle; opposite side x unknown")
# s5 area a=15,b=20,C=75
FIG[('silver',5)] = tri(15, 20, sq(225+400-2*15*20*c(r(75))), "15 cm", "20 cm", None,
    None, None, ("75°", False), ["Area = ?"],
    "Triangle with sides 15 cm and 20 cm meeting at a 75 degree angle; area unknown")
# s6 a=4,b=7,c=9 find C(opp c=9, ?)
FIG[('silver',6)] = tri(4, 7, 9, "4", "7", "9", None, None, ("?", False), [],
    "Triangle with sides 4, 7 and 9; angle C opposite side 9 unknown")

# --- gold problem figures (g0 bearings skipped: needs bespoke north-line figure) ---
# g1 sides 13,14,15 area
FIG[('gold',1)] = tri(13, 14, 15, "13", "14", "15", None, None, None, ["Area = ?"],
    "Triangle with sides 13, 14 and 15; area unknown")
# g2 PQR PQ=8,QR=11,angle Q=100, find PR(opp Q). At vertex Q the two sides 8 and 11 meet.
# Map: angle at B(vertex0)=Q=100 between sides a(BC) and c(AB). Let a=BC=11(QR), c=AB=8(PQ), b=CA=PR opp Q
g2b = sq(64+121-176*c(r(100)))
FIG[('gold',2)] = tri(11, g2b, 8, "11 cm", "PR = ?", "8 cm",
    None, ("100°", False), None, [],
    "Triangle PQR with PQ 8 cm and QR 11 cm meeting at a 100 degree angle at Q; PR unknown")
# g3 area=30 sides 10,8 find angle between (?)
g3ang = math.degrees(math.asin(2*30/(10*8)))
FIG[('gold',3)] = tri(10, 8, sq(100+64-160*c(r(g3ang))), "10 cm", "8 cm", None,
    None, None, ("?", False), ["Area = 30 cm²"],
    "Triangle with sides 10 cm and 8 cm, area 30 square cm; included angle unknown")
# g4 parallelogram 6,10,70
th = r(70)
FIG[('gold',4)] = render(
    [(0.0, 0.0), (10.0, 0.0), (10+6*c(th), 6*sin(th)), (6*c(th), 6*sin(th))],
    [(0, 1, "10 cm"), (1, 2, "6 cm"), (2, 3, None), (3, 0, None)],
    [(0, "70°", False)], ["Area = ?"],
    "Parallelogram with sides 10 cm and 6 cm and a 70 degree angle; area unknown")

# ---------------------------------------------------------------------------
# assemble + apply figures
# ---------------------------------------------------------------------------
live = json.load(io.open("_live_eduqas_geoL06.json", encoding="utf-8"))

# preserved worked_examples carry em dashes in step labels ("Step 1 — ...");
# the no-em-dash style rule (validator-enforced) wins: swap — for a colon only.
def desash(o):
    if isinstance(o, dict): return {k: desash(v) for k, v in o.items()}
    if isinstance(o, list): return [desash(v) for v in o]
    if isinstance(o, str): return o.replace(" — ", ": ").replace("—", ":")
    return o
live_we = desash(live["worked_examples"])

pd = {
 "guided": {"opener": opener, "teach": teach},
 "tier_guides": tier_guides,
 "problem_bank": pb,
 "method_card": method_card,
 # preserved byte-for-byte from live:
 "topic_links": live["topic_links"],
 "related_videos": live["related_videos"],
 "worked_examples": live_we,
}

# apply figures
pd["guided"]["opener"]["display"] = prepend(pd["guided"]["opener"]["display"], FIG['opener']); added.append("opener")
for tier in ("bronze","silver","gold"):
    pd["guided"]["teach"][tier]["display"] = prepend(pd["guided"]["teach"][tier]["display"], FIG['teach_'+tier]); added.append("teach."+tier)
for tier in ("bronze","silver","gold"):
    for i, prob in enumerate(pd["problem_bank"][tier]):
        if (tier, i) in FIG:
            prob["display"] = prepend(prob["display"], FIG[(tier, i)]); added.append("%s[%d]" % (tier, i))

json.dump(pd, io.open("lesson_maths-eduqas_geometry-L06.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("FIGURES ADDED:", len(added)); print(added)
# figure label sanity
for name, fig in FIG.items():
    labels = re.findall(r">([^<]+)</text>", fig)
    if len(fig) > 3000: print("WARN big svg", name, len(fig))
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
print("wrote lesson_maths-eduqas_geometry-L06.json")
