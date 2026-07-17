# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams build for maths-aqa geometry-L06
Sine Rule, Cosine Rule & Area Formula. Repairs bank, adds guided stack + SVG triangles."""
import json, math

R = lambda x: round(x, 1)
r4 = lambda x: round(x, 4)
sind = lambda d: math.sin(math.radians(d))
cosd = lambda d: math.cos(math.radians(d))
DEG = "°"

# ---------- triangle SVG drawer ----------
def _norm(v):
    L = math.hypot(v[0], v[1]) or 1.0
    return (v[0]/L, v[1]/L)

def layout(a, b, c):
    """A(idx0) at origin, B(idx1) at (c,0), C(idx2) from angle A. a opp A, b opp B, c opp C."""
    cosA = (b*b + c*c - a*a) / (2*b*c)
    A = math.acos(max(-1.0, min(1.0, cosA)))
    return [(0.0, 0.0), (c, 0.0), (b*math.cos(A), b*math.sin(A))]

def scale_pts(pts, W=210, H=162, pad=36):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    minx, maxx = min(xs), max(xs); miny, maxy = min(ys), max(ys)
    w = (maxx-minx) or 1; h = (maxy-miny) or 1
    s = min((W-2*pad)/w, (H-2*pad)/h)
    dw = (W - w*s)/2; dh = (H - h*s)/2
    return [(dw + (x-minx)*s, H - dh - (y-miny)*s) for (x, y) in pts]

def tri_svg(a, b, c, names, sides=None, angles=None, right=None, area=None, aria=""):
    sides = sides or {}; angles = angles or {}
    P = scale_pts(layout(a, b, c))
    A, B, C = P
    G = ((A[0]+B[0]+C[0])/3, (A[1]+B[1]+C[1])/3)
    def outw(pt, d):
        v = _norm((pt[0]-G[0], pt[1]-G[1]))
        return (pt[0]+d*v[0], pt[1]+d*v[1])
    parts = [f'<svg viewBox="0 0 210 162" role="img" aria-label="{aria}" '
             f'style="max-width:270px;font-family:Inter,sans-serif" stroke-linejoin="round">']
    parts.append(f'<polygon points="{A[0]:.1f},{A[1]:.1f} {B[0]:.1f},{B[1]:.1f} {C[0]:.1f},{C[1]:.1f}" '
                 f'fill="#60a5fa" fill-opacity="0.14" stroke="currentColor" stroke-width="1.7"/>')
    # side labels: a=BC(1,2), b=CA(2,0), c=AB(0,1)
    edge = {'a': (B, C), 'b': (C, A), 'c': (A, B)}
    for k, txt in sides.items():
        m1, m2 = edge[k]
        mid = ((m1[0]+m2[0])/2, (m1[1]+m2[1])/2)
        lx, ly = outw(mid, 14)
        parts.append(f'<text x="{lx:.1f}" y="{ly+3:.1f}" font-size="11" text-anchor="middle" '
                     f'font-weight="600" fill="currentColor">{txt}</text>')
    # angle marks
    adj = {0: (B, C), 1: (A, C), 2: (A, B)}
    for idx, txt in angles.items():
        V = P[idx]; U, Wv = adj[idx]
        d1 = _norm((U[0]-V[0], U[1]-V[1])); d2 = _norm((Wv[0]-V[0], Wv[1]-V[1]))
        if right == idx:
            s = 12
            p1 = (V[0]+s*d1[0], V[1]+s*d1[1])
            p2 = (V[0]+s*d1[0]+s*d2[0], V[1]+s*d1[1]+s*d2[1])
            p3 = (V[0]+s*d2[0], V[1]+s*d2[1])
            parts.append(f'<polyline points="{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} '
                         f'{p3[0]:.1f},{p3[1]:.1f}" fill="none" stroke="currentColor" stroke-width="1.3"/>')
        else:
            rr = 16
            st = (V[0]+rr*d1[0], V[1]+rr*d1[1]); en = (V[0]+rr*d2[0], V[1]+rr*d2[1])
            cross = d1[0]*d2[1] - d1[1]*d2[0]
            sweep = 1 if cross > 0 else 0
            parts.append(f'<path d="M{st[0]:.1f},{st[1]:.1f} A{rr},{rr} 0 0 {sweep} {en[0]:.1f},{en[1]:.1f}" '
                         f'fill="none" stroke="currentColor" stroke-width="1.3"/>')
        bis = _norm((d1[0]+d2[0], d1[1]+d2[1]))
        lx, ly = V[0]+24*bis[0], V[1]+24*bis[1]
        parts.append(f'<text x="{lx:.1f}" y="{ly+3:.1f}" font-size="10.5" text-anchor="middle" '
                     f'fill="currentColor">{txt}</text>')
    # vertex names
    for idx, nm in names.items():
        vx, vy = outw(P[idx], 13)
        parts.append(f'<text x="{vx:.1f}" y="{vy+3:.1f}" font-size="11" text-anchor="middle" '
                     f'font-weight="700" fill="currentColor">{nm}</text>')
    if area:
        parts.append(f'<text x="{G[0]:.1f}" y="{G[1]+3:.1f}" font-size="10" text-anchor="middle" '
                     f'fill="currentColor">{area}</text>')
    parts.append('</svg><span class="figure-caption">Diagram not drawn accurately</span> ')
    return "".join(parts)

# ---------- guided_steps generators (all box values computed) ----------
def gs_sine_side(Aa, Ba, bside, ans, subj_letter="a", oppA=True):
    """find side opposite Aa using ratio with (bside, Ba). a = bside*sinA/sinB."""
    num = r4(bside*sind(Aa)); den = r4(sind(Ba))
    assert R(num/den) == ans, (num, den, num/den, ans)
    return [
        {"say": f"Sine rule: \\(\\frac{{{subj_letter}}}{{\\sin A}} = \\frac{{b}}{{\\sin B}}\\). "
                f"You know the pair (\\(b={bside}\\), \\(B={Ba}{DEG}\\)) and angle \\(A={Aa}{DEG}\\), "
                f"so \\({subj_letter} = \\frac{{b\\sin A}}{{\\sin B}}\\)."},
        {"pre": f"Top line: {bside} × sin {Aa}{DEG} = ", "post": "", "answer": num,
         "hint": f"Type {bside} × sin {Aa} into the calculator, 4 d.p."},
        {"pre": f"Bottom line: sin {Ba}{DEG} = ", "post": "", "answer": den,
         "hint": f"sin {Ba} on the calculator, 4 d.p.", "phase": "substitute"},
        {"pre": f"Divide: {num} ÷ {den} = ", "post": "", "answer": ans,
         "hint": "Top divided by bottom, 1 d.p.", "done": f"So {subj_letter} = {ans}."},
        {"pre": f"Check: {ans} × sin {Ba}{DEG} ÷ sin {Aa}{DEG} rounds to ", "post": "", "answer": bside,
         "hint": "Should return the known side b.", "done": f"Back to b = {bside}, so {subj_letter} = {ans} is right."},
    ]

def gs_sine_angle(aside, bside, Aa, ans, want="B"):
    """find angle B: sinB = bside*sinA/aside."""
    num = r4(bside*sind(Aa)); sinv = r4(num/aside)
    assert R(math.degrees(math.asin(min(1.0, num/aside)))) == ans
    return [
        {"say": f"Sine rule for an angle: \\(\\frac{{\\sin {want}}}{{b}} = \\frac{{\\sin A}}{{a}}\\), "
                f"so \\(\\sin {want} = \\frac{{b\\sin A}}{{a}}\\). Here \\(a={aside}\\), \\(b={bside}\\), \\(A={Aa}{DEG}\\)."},
        {"pre": f"Top line: {bside} × sin {Aa}{DEG} = ", "post": "", "answer": num,
         "hint": f"{bside} × sin {Aa}, 4 d.p."},
        {"pre": f"Divide by {aside}: {num} ÷ {aside} = ", "post": "", "answer": sinv,
         "hint": f"That is sin {want}, 4 d.p.", "phase": "substitute"},
        {"pre": f"Inverse sine: sin⁻¹({sinv}) = ", "post": "", "answer": ans,
         "hint": "Use sin⁻¹ (shift sin), 1 d.p.", "done": f"So {want} = {ans}{DEG}."},
        {"pre": f"Check it is acute and under 180: sin {ans}{DEG} rounds to ", "post": "", "answer": sinv,
         "hint": "Should return the sine value.", "done": f"Returns {sinv}, so {want} = {ans}{DEG} is right."},
    ]

def gs_cos_side(s1, s2, inc, ans, letter="c"):
    """third side: c^2 = s1^2 + s2^2 - 2 s1 s2 cos(inc)."""
    sq1 = s1*s1; sq2 = s2*s2; ssum = sq1+sq2
    prod = r4(2*s1*s2*cosd(inc)); c2 = r4(ssum - prod)
    assert R(math.sqrt(c2)) == ans
    return [
        {"say": f"Cosine rule for a side: \\({letter}^2 = a^2 + b^2 - 2ab\\cos C\\). "
                f"Two sides {s1} and {s2} with the angle {inc}{DEG} between them."},
        {"pre": f"Square and add the two sides: {s1}² + {s2}² = {sq1} + {sq2} = ", "post": "", "answer": ssum,
         "hint": "Square each, then add."},
        {"pre": f"The subtracted part: 2 × {s1} × {s2} × cos {inc}{DEG} = ", "post": "", "answer": prod,
         "hint": f"2 × {s1} × {s2} × cos {inc}, 4 d.p.", "phase": "substitute"},
        {"pre": f"So {letter}² = {ssum} − ({prod}) = ", "post": "", "answer": c2,
         "hint": "Subtract the part from the sum.", "done": f"{letter}² = {c2}."},
        {"pre": f"Square root: √{c2} = ", "post": "", "answer": ans,
         "hint": "Square root, 1 d.p.", "done": f"So {letter} = {ans}."},
    ]

def gs_cos_angle(a, b, c, ans, want="A"):
    """angle opposite a: cosA = (b^2+c^2-a^2)/(2bc)."""
    top = b*b + c*c - a*a; bot = 2*b*c; cv = r4(top/bot)
    assert R(math.degrees(math.acos(top/bot))) == ans
    return [
        {"say": f"Cosine rule for an angle: \\(\\cos {want} = \\frac{{b^2 + c^2 - a^2}}{{2bc}}\\), "
                f"where \\(a={a}\\) is opposite the angle you want."},
        {"pre": f"Top line: {b}² + {c}² − {a}² = {b*b} + {c*c} − {a*a} = ", "post": "", "answer": top,
         "hint": "Square all three, then combine."},
        {"pre": f"Bottom line: 2 × {b} × {c} = ", "post": "", "answer": bot,
         "hint": f"2 × {b} × {c}.", "phase": "substitute"},
        {"pre": f"Divide: {top} ÷ {bot} = ", "post": "", "answer": cv,
         "hint": f"That is cos {want}, 4 d.p.", "done": f"cos {want} = {cv}."},
        {"pre": f"Inverse cosine: cos⁻¹({cv}) = ", "post": "", "answer": ans,
         "hint": "Use cos⁻¹ (shift cos), 1 d.p.", "done": f"So {want} = {ans}{DEG}."},
    ]

def gs_area(s1, s2, inc, ans):
    """area = 1/2 s1 s2 sin inc."""
    half = r4(0.5*s1*s2); si = r4(sind(inc))
    assert R(half*si) == ans
    return [
        {"say": f"Area of a triangle: \\(\\frac12 ab\\sin C\\). Two sides {s1} and {s2} with the "
                f"included angle {inc}{DEG}."},
        {"pre": f"Half the product of the sides: ½ × {s1} × {s2} = ", "post": "", "answer": half,
         "hint": f"Multiply {s1} and {s2}, then halve."},
        {"pre": f"Sine of the angle: sin {inc}{DEG} = ", "post": "", "answer": si,
         "hint": f"sin {inc}, 4 d.p.", "phase": "substitute"},
        {"pre": f"Multiply: {half} × {si} = ", "post": "", "answer": ans,
         "hint": "Product of the two, 1 d.p.", "done": f"So the area = {ans} cm²."},
        {"pre": f"Check the units: area is in cm², so to 1 d.p. it is ", "post": "", "answer": ans,
         "hint": "Same value, confirmed.", "done": f"Area = {ans} cm² confirmed."},
    ]

# ---------- assemble problems ----------
pb = {}

# ===== BRONZE =====
bronze = []
# B1 sine side: A40 B60 b12 -> a 8.9
bronze.append({
    "display": tri_svg(8.9067, 12, 13.65, {0:"A",1:"B",2:"C"},
                       sides={'b':"12", 'a':"?"}, angles={0:f"40{DEG}",1:f"60{DEG}"},
                       aria="Triangle ABC with angle A 40 degrees, angle B 60 degrees and side b 12")
               + "Find side \\(a\\) using the sine rule: \\(A = 40°\\), \\(B = 60°\\), \\(b = 12\\). Give to 1 d.p.",
    "solutions": [8.9], "calculator": True, "input_type": "single_value",
    "hint": "Make a the subject: a = b sin A ÷ sin B.",
    "guided_steps": gs_sine_side(40, 60, 12, 8.9),
    "misconceptions": [
        {"pattern": "inverted_ratio", "expect": 16.2,
         "message": "You inverted the fraction. The unknown side sits over its own angle: a = 12 sin 40 ÷ sin 60 = 8.9, not 12 sin 60 ÷ sin 40 = 16.2.",
         "note": "12*sin60/sin40"}],
})
# B2 sine angle: a9 b12 A35 -> B 49.9 (FIX from 49.5)
bronze.append({
    "display": tri_svg(9, 12, 15.63, {0:"A",1:"B",2:"C"},
                       sides={'a':"9", 'b':"12"}, angles={0:f"35{DEG}",1:"?"},
                       aria="Triangle ABC with side a 9, side b 12 and angle A 35 degrees, angle B unknown")
               + "Find angle \\(B\\): \\(a = 9\\), \\(b = 12\\), \\(A = 35°\\). Give to 1 d.p.",
    "solutions": [49.9], "calculator": True, "input_type": "single_value",
    "hint": "sin B = b sin A ÷ a, then use inverse sine.",
    "guided_steps": gs_sine_angle(9, 12, 35, 49.9, "B"),
    "misconceptions": [
        {"pattern": "swapped_sides", "expect": 25.5,
         "message": "You put the sides the wrong way up. sin B = b sin A ÷ a = 12 sin 35 ÷ 9. Using 9 sin 35 ÷ 12 gives sin B = 0.4302 and B = 25.5°.",
         "note": "asin(9*sin35/12)"}],
})
# B3 area 6,10 inc45 -> 21.2
bronze.append({
    "display": tri_svg(7.15, 6, 10, {0:"A",1:"B",2:"C"},
                       sides={'b':"6", 'c':"10"}, angles={0:f"45{DEG}"}, area="Area = ?",
                       aria="Triangle with two sides 6 and 10 and the included angle 45 degrees")
               + "Find the area of a triangle with sides 6 cm and 10 cm and included angle 45°. Give to 1 d.p.",
    "solutions": [21.2], "calculator": True, "input_type": "single_value",
    "hint": "Area = half times the two sides times the sine of the angle between them.",
    "guided_steps": gs_area(6, 10, 45, 21.2),
    "misconceptions": [
        {"pattern": "no_half", "expect": 42.4,
         "message": "You left out the half. Area = ½ × 6 × 10 × sin 45 = 21.2 cm². Without the ½ you get 42.4 cm², which is twice too big.",
         "note": "6*10*sin45"}],
})
# B4 area 8,6 inc30 -> 12 (CHANGED from 8,5 which gave duplicate 10)
bronze.append({
    "display": tri_svg(4.36, 8, 6, {0:"A",1:"B",2:"C"},
                       sides={'b':"8", 'c':"6"}, angles={0:f"30{DEG}"}, area="Area = ?",
                       aria="Triangle with two sides 8 and 6 and the included angle 30 degrees")
               + "Find the area of a triangle with sides 8 cm and 6 cm and included angle 30°. Give to 1 d.p.",
    "solutions": [12], "calculator": True, "input_type": "single_value",
    "hint": "Area = half times the two sides times the sine of the angle between them.",
    "guided_steps": gs_area(8, 6, 30, 12),
    "misconceptions": [
        {"pattern": "no_half", "expect": 24,
         "message": "You left out the half. Area = ½ × 8 × 6 × sin 30 = 12 cm². Without the ½ you get 24 cm².",
         "note": "8*6*sin30"}],
})
# B5 sine side: A50 B80 a7 -> b 9
bronze.append({
    "display": tri_svg(7, 8.999, 7, {0:"A",1:"B",2:"C"},
                       sides={'a':"7", 'b':"?"}, angles={0:f"50{DEG}",1:f"80{DEG}"},
                       aria="Triangle ABC with angle A 50 degrees, angle B 80 degrees and side a 7")
               + "Find side \\(b\\) using the sine rule: \\(A = 50°\\), \\(B = 80°\\), \\(a = 7\\). Give to 1 d.p.",
    "solutions": [9], "calculator": True, "input_type": "single_value",
    "hint": "Make b the subject: b = a sin B ÷ sin A.",
    "guided_steps": gs_sine_side(80, 50, 7, 9, subj_letter="b"),
    "misconceptions": [
        {"pattern": "inverted_ratio", "expect": 5.4,
         "message": "You inverted the fraction. b = 7 sin 80 ÷ sin 50 = 9.0. Using 7 sin 50 ÷ sin 80 gives 5.4.",
         "note": "7*sin50/sin80"}],
})
# B6 cosine side C90 -> c 10
bronze.append({
    "display": tri_svg(6, 8, 10, {0:"A",1:"B",2:"C"},
                       sides={'a':"6", 'b':"8", 'c':"?"}, angles={2:f"90{DEG}"}, right=2,
                       aria="Right angled triangle with legs 6 and 8 and the right angle at C")
               + "Find side \\(c\\) using the cosine rule: \\(a = 6\\), \\(b = 8\\), \\(C = 90°\\). Give to 1 d.p.",
    "solutions": [10], "calculator": True, "input_type": "single_value",
    "hint": "c squared = a squared plus b squared minus 2ab cos C; cos 90 is zero.",
    "guided_steps": gs_cos_side(6, 8, 90, 10),
    "misconceptions": [
        {"pattern": "no_sqrt", "expect": 100,
         "message": "You stopped at c². Here c² = 36 + 64 − 0 = 100, so you still need the square root: c = √100 = 10.",
         "note": "forgot sqrt"}],
})
# B7 area 12,9 inc60 -> 46.8
bronze.append({
    "display": tri_svg(10.82, 12, 9, {0:"A",1:"B",2:"C"},
                       sides={'b':"12", 'c':"9"}, angles={0:f"60{DEG}"}, area="Area = ?",
                       aria="Triangle with two sides 12 and 9 and the included angle 60 degrees")
               + "Find the area of a triangle with sides 12 cm and 9 cm and included angle 60°. Give to 1 d.p.",
    "solutions": [46.8], "calculator": True, "input_type": "single_value",
    "hint": "Area = half times the two sides times the sine of the angle between them.",
    "guided_steps": gs_area(12, 9, 60, 46.8),
    "misconceptions": [
        {"pattern": "no_half", "expect": 93.5,
         "message": "You left out the half. Area = ½ × 12 × 9 × sin 60 = 46.8 cm². Without the ½ you get 93.5 cm².",
         "note": "12*9*sin60"}],
})
# B8 cosine side b10 c7 A50 -> a 7.7
bronze.append({
    "display": tri_svg(7.68, 10, 7, {0:"A",1:"B",2:"C"},
                       sides={'b':"10", 'c':"7", 'a':"?"}, angles={0:f"50{DEG}"},
                       aria="Triangle with sides b 10 and c 7 and the included angle A 50 degrees")
               + "Find side \\(a\\) using the cosine rule: \\(b = 10\\), \\(c = 7\\), \\(A = 50°\\). Give to 1 d.p.",
    "solutions": [7.7], "calculator": True, "input_type": "single_value",
    "hint": "a squared = b squared plus c squared minus 2bc cos A.",
    "guided_steps": gs_cos_side(10, 7, 50, 7.7, letter="a"),
    "misconceptions": [
        {"pattern": "sign_add", "expect": 15.5,
         "message": "You added the last term instead of subtracting it. a² = 100 + 49 − 2(10)(7)cos 50 = 59.0, so a = 7.7. Adding gives a² = 239.0 and a = 15.5.",
         "note": "sqrt(149+2*70*cos50)"}],
})
pb["bronze"] = bronze
pb["bronze_description"] = ("Use a single rule once: the sine rule for a missing side or angle, "
                            "the area formula ½ab sin C, or the cosine rule for a side.")

# ===== SILVER =====
silver = []
# S1 SSS a8 b6 c10 find A -> 53.1
silver.append({
    "display": tri_svg(8, 6, 10, {0:"A",1:"B",2:"C"},
                       sides={'a':"8", 'b':"6", 'c':"10"}, angles={0:"?"},
                       aria="Triangle ABC with sides a 8, b 6 and c 10, angle A unknown")
               + "Find angle \\(A\\) using the cosine rule: \\(a = 8\\), \\(b = 6\\), \\(c = 10\\). Give to 1 d.p.",
    "solutions": [53.1], "calculator": True, "input_type": "single_value",
    "hint": "cos A = (b squared + c squared minus a squared) over 2bc.",
    "guided_steps": gs_cos_angle(8, 6, 10, 53.1, "A"),
    "misconceptions": [
        {"pattern": "sign_flip", "expect": 126.9,
         "message": "You kept a² positive on top. The side opposite the angle is subtracted: cos A = (36 + 100 − 64) ÷ 120 = 0.6, giving A = 53.1°. Flipping the signs gives cos A = −0.6 and A = 126.9°.",
         "note": "acos(-0.6)"}],
})
# S2 SSS a12 b9 c7 find C -> 35.4 (FIX from 35.2)
silver.append({
    "display": tri_svg(12, 9, 7, {0:"A",1:"B",2:"C"},
                       sides={'a':"12", 'b':"9", 'c':"7"}, angles={2:"?"},
                       aria="Triangle ABC with sides a 12, b 9 and c 7, angle C unknown")
               + "Find angle \\(C\\): \\(a = 12\\), \\(b = 9\\), \\(c = 7\\). Give to 1 d.p.",
    "solutions": [35.4], "calculator": True, "input_type": "single_value",
    "hint": "cos C = (a squared + b squared minus c squared) over 2ab.",
    "guided_steps": gs_cos_angle(7, 12, 9, 35.4, "C"),
    "misconceptions": [
        {"pattern": "sign_flip", "expect": 144.6,
         "message": "The side opposite the wanted angle is the one subtracted: cos C = (144 + 81 − 49) ÷ 216 = 0.8148, giving C = 35.4°. Flipping the signs gives cos C = −0.8148 and C = 144.6°.",
         "note": "acos(-0.8148)"}],
})
# S3 SAS 11,14 inc75 third -> 15.4
silver.append({
    "display": tri_svg(15.4, 11, 14, {0:"A",1:"B",2:"C"},
                       sides={'b':"11", 'c':"14", 'a':"?"}, angles={0:f"75{DEG}"},
                       aria="Triangle with two sides 11 and 14 and the included angle 75 degrees")
               + "A triangle has sides 11 cm and 14 cm and an included angle of 75°. Find the third side to 1 d.p.",
    "solutions": [15.4], "calculator": True, "input_type": "single_value",
    "hint": "Third side squared = 11 squared + 14 squared minus 2 times 11 times 14 times cos 75.",
    "guided_steps": gs_cos_side(11, 14, 75, 15.4),
    "misconceptions": [
        {"pattern": "sign_add", "expect": 19.9,
         "message": "You added the cosine term instead of subtracting it. c² = 121 + 196 − 308 cos 75 = 237.3, so c = 15.4. Adding gives c² = 396.7 and c = 19.9.",
         "note": "sqrt(317+308*cos75)"}],
})
# S4 area PQ15 PR11 P42 -> 55.2
silver.append({
    "display": tri_svg(10.19, 11, 15, {0:"P",1:"Q",2:"R"},
                       sides={'c':"15", 'b':"11"}, angles={0:f"42{DEG}"}, area="Area = ?",
                       aria="Triangle PQR with PQ 15, PR 11 and angle P 42 degrees")
               + "Find the area of triangle PQR where PQ = 15, PR = 11 and angle P = 42°. Give to 1 d.p.",
    "solutions": [55.2], "calculator": True, "input_type": "single_value",
    "hint": "Area = half times PQ times PR times sin P.",
    "guided_steps": gs_area(15, 11, 42, 55.2),
    "misconceptions": [
        {"pattern": "no_half", "expect": 110.4,
         "message": "You left out the half. Area = ½ × 15 × 11 × sin 42 = 55.2 cm². Without the ½ you get 110.4 cm².",
         "note": "15*11*sin42"}],
})
# S5 sine side a5 A30 B105 find b -> 9.7
silver.append({
    "display": tri_svg(5, 9.66, 7.07, {0:"A",1:"B",2:"C"},
                       sides={'a':"5", 'b':"?"}, angles={0:f"30{DEG}",1:f"105{DEG}"},
                       aria="Triangle ABC with side a 5, angle A 30 degrees and angle B 105 degrees")
               + "In triangle ABC, a = 5, A = 30°, B = 105°. Find side b to 1 d.p.",
    "solutions": [9.7], "calculator": True, "input_type": "single_value",
    "hint": "b = a sin B ÷ sin A.",
    "guided_steps": gs_sine_side(105, 30, 5, 9.7, subj_letter="b"),
    "misconceptions": [
        {"pattern": "inverted_ratio", "expect": 2.6,
         "message": "You inverted the fraction. b = 5 sin 105 ÷ sin 30 = 9.7. Using 5 sin 30 ÷ sin 105 gives 2.6.",
         "note": "5*sin30/sin105"}],
})
# S6 cosine side b15 c20 A110 find a -> 28.8
silver.append({
    "display": tri_svg(28.8, 15, 20, {0:"A",1:"B",2:"C"},
                       sides={'b':"15", 'c':"20", 'a':"?"}, angles={0:f"110{DEG}"},
                       aria="Triangle with sides b 15 and c 20 and the obtuse included angle A 110 degrees")
               + "Find side \\(a\\) using cosine rule: \\(b = 15\\), \\(c = 20\\), \\(A = 110°\\). Give to 1 d.p.",
    "solutions": [28.8], "calculator": True, "input_type": "single_value",
    "hint": "a squared = 15 squared + 20 squared minus 2 times 15 times 20 times cos 110; cos 110 is negative.",
    "guided_steps": gs_cos_side(15, 20, 110, 28.8, letter="a"),
    "misconceptions": [
        {"pattern": "sign_cos", "expect": 20.5,
         "message": "cos 110 is negative, so the last term adds on: a² = 225 + 400 + 205.2 = 830.2 and a = 28.8. Treating cos 110 as positive gives a² = 419.8 and a = 20.5.",
         "note": "sqrt(625-600*cos110pos)"}],
})
# S7 hikers 3,5 angle60 -> 4.4 (no figure: bearings)
silver.append({
    "display": "Two hikers start at the same point. One walks 3 km on bearing 060° and the other 5 km on bearing 120°. How far apart are they? Give to 1 d.p.",
    "solutions": [4.4], "calculator": True, "input_type": "single_value",
    "hint": "The angle between the two paths is 120 minus 60; then use the cosine rule.",
    "guided_steps": [
        {"say": "First the angle between the paths. Both bearings share the same start, so the angle is the difference of the bearings."},
        {"pre": "Angle between paths: 120° − 60° = ", "post": "", "answer": 60,
         "hint": "Subtract the smaller bearing from the larger."},
        {"say": "Now the cosine rule with sides 3 and 5 and that included angle: \\(d^2 = 3^2 + 5^2 - 2(3)(5)\\cos 60°\\)."},
        {"pre": "Square and add the distances: 3² + 5² = 9 + 25 = ", "post": "", "answer": 34,
         "hint": "Square each, then add.", "phase": "substitute"},
        {"pre": "The subtracted part: 2 × 3 × 5 × cos 60° = ", "post": "", "answer": 15,
         "hint": "2 × 3 × 5 × cos 60; cos 60 = 0.5."},
        {"pre": "So d² = 34 − 15 = ", "post": "", "answer": 19,
         "hint": "Subtract.", "done": "d² = 19."},
        {"pre": "Square root: √19 = ", "post": "", "answer": 4.4,
         "hint": "Square root, 1 d.p.", "done": "So they are 4.4 km apart."},
    ],
    "misconceptions": [
        {"pattern": "sign_add", "expect": 7,
         "message": "You added the cosine term instead of subtracting it. d² = 34 − 15 = 19, so d = 4.4 km. Adding gives d² = 49 and d = 7 km.",
         "note": "sqrt(34+15)"}],
})
pb["silver"] = silver
pb["silver_description"] = ("Use the cosine rule for three sides (an angle) or two sides and the included "
                            "angle (a side), and set up bearings problems.")

# ===== GOLD =====
gold = []
# G1 ambiguous a10 b7 B40 -> 66.7, 113.3
sinA_g1 = r4(10*sind(40)/7)  # 0.9183
A1 = R(math.degrees(math.asin(10*sind(40)/7)))
gold.append({
    "display": tri_svg(10, 7, 10.43, {0:"A",1:"B",2:"C"},
                       sides={'a':"10", 'b':"7"}, angles={1:f"40{DEG}",0:"?"},
                       aria="Triangle ABC with side a 10, side b 7 and angle B 40 degrees, angle A unknown")
               + "In triangle ABC, a = 10, b = 7, B = 40°. Find the two possible values of angle A. Give both to 1 d.p.",
    "solutions": [66.7, 113.3], "calculator": True, "input_type": "two_solutions",
    "hint": "Find sin A, take the inverse sine, then also use 180 minus that angle.",
    "guided_steps": [
        {"say": "Sine rule for the angle: \\(\\sin A = \\frac{a\\sin B}{b} = \\frac{10\\sin 40°}{7}\\)."},
        {"pre": "Top line: 10 × sin 40° = ", "post": "", "answer": r4(10*sind(40)),
         "hint": "10 × sin 40, 4 d.p."},
        {"pre": f"Divide by 7: {r4(10*sind(40))} ÷ 7 = ", "post": "", "answer": sinA_g1,
         "hint": "That is sin A, 4 d.p.", "phase": "substitute"},
        {"pre": f"First angle: sin⁻¹({sinA_g1}) = ", "post": "", "answer": A1,
         "hint": "Inverse sine, 1 d.p.", "done": f"The acute answer is {A1}{DEG}."},
        {"pre": f"Second angle (ambiguous case): 180° − {A1}° = ", "post": "", "answer": R(180-A1),
         "hint": "Sine gives two angles under 180.",
         "done": f"Check: {R(180-A1)}{DEG} + 40{DEG} = {R(180-A1)+40}{DEG} < 180{DEG}, so both fit. A = {A1}{DEG} or {R(180-A1)}{DEG}."},
    ],
    "misconceptions": [
        {"pattern": "one_solution", "expect": [66.7, 66.7],
         "message": "You found only the acute angle. Because a is longer than b, the ambiguous case applies: A = 66.7° or 180 − 66.7 = 113.3°. Both give a valid triangle.",
         "note": "student gives acute only"}],
})
# G2 ship bearings AC 8.2 (no figure)
gold.append({
    "display": "A ship sails 8 km from A to B on bearing 040°, then 6 km from B to C on bearing 150°. Find AC to 1 d.p.",
    "solutions": [8.2], "calculator": True, "input_type": "single_value",
    "hint": "Find the interior angle at B first, then use the cosine rule on the sides 8 and 6.",
    "guided_steps": [
        {"say": "First the interior angle at B. The back bearing from B to A is 040 + 180 = 220°, and the bearing on to C is 150°."},
        {"pre": "Interior angle at B: 220° − 150° = ", "post": "", "answer": 70,
         "hint": "Back bearing to A minus bearing to C."},
        {"say": "Now the cosine rule with AB = 8, BC = 6 and that 70° between them: \\(AC^2 = 8^2 + 6^2 - 2(8)(6)\\cos 70°\\)."},
        {"pre": "Square and add: 8² + 6² = 64 + 36 = ", "post": "", "answer": 100,
         "hint": "Square each, then add.", "phase": "substitute"},
        {"pre": "The subtracted part: 2 × 8 × 6 × cos 70° = ", "post": "", "answer": r4(96*cosd(70)),
         "hint": "2 × 8 × 6 × cos 70, 4 d.p."},
        {"pre": f"So AC² = 100 − {r4(96*cosd(70))} = ", "post": "", "answer": r4(100-96*cosd(70)),
         "hint": "Subtract.", "done": f"AC² = {r4(100-96*cosd(70))}."},
        {"pre": f"Square root: √{r4(100-96*cosd(70))} = ", "post": "", "answer": 8.2,
         "hint": "Square root, 1 d.p.", "done": "So AC = 8.2 km."},
    ],
    "misconceptions": [
        {"pattern": "wrong_angle", "expect": 11.5,
         "message": "You used 150 − 40 = 110° for the angle. The interior angle at B needs the back bearing to A (220°), giving 220 − 150 = 70°. With 110° you get AC = 11.5 km.",
         "note": "sqrt(100-96cos110)"}],
})
# G3 area 40 PQ10 PR12 find acute P -> 41.8
gold.append({
    "display": tri_svg(8.07, 12, 10, {0:"P",1:"Q",2:"R"},
                       sides={'c':"10", 'b':"12"}, angles={0:"?"}, area="Area = 40",
                       aria="Triangle PQR with PQ 10, PR 12 and area 40, angle P unknown")
               + "Triangle PQR has area 40 cm², PQ = 10 cm, PR = 12 cm. Find the acute angle P to 1 d.p.",
    "solutions": [41.8], "calculator": True, "input_type": "single_value",
    "hint": "Put the numbers into area = half times PQ times PR times sin P, then rearrange for sin P.",
    "guided_steps": [
        {"say": "Area = ½ × PQ × PR × sin P, so 40 = ½ × 10 × 12 × sin P."},
        {"pre": "Half the product of the sides: ½ × 10 × 12 = ", "post": "", "answer": 60,
         "hint": "Multiply 10 and 12, then halve."},
        {"pre": "Rearrange for sin P: 40 ÷ 60 = ", "post": "", "answer": r4(40/60),
         "hint": "Area divided by that number, 4 d.p.", "phase": "substitute"},
        {"pre": f"Inverse sine: sin⁻¹({r4(40/60)}) = ", "post": "", "answer": 41.8,
         "hint": "Use sin⁻¹, 1 d.p.", "done": "So the acute angle P = 41.8°."},
        {"pre": "Check: ½ × 10 × 12 × sin 41.8° rounds to ", "post": "", "answer": 40,
         "hint": "Should return the area.", "done": "Back to area 40 cm², so P = 41.8° is right."},
    ],
    "misconceptions": [
        {"pattern": "no_half", "expect": 19.5,
         "message": "You left out the half, dividing by 10 × 12 = 120. That gives sin P = 40 ÷ 120 = 0.3333 and P = 19.5°. With the ½ the divisor is 60, giving P = 41.8°.",
         "note": "asin(40/120)"}],
})
# G4 sides 13,14,15 area -> 84
gold.append({
    "display": tri_svg(13, 14, 15, {0:"A",1:"B",2:"C"},
                       sides={'a':"13", 'b':"14", 'c':"15"}, angles={}, area="Area = ?",
                       aria="Triangle with sides 13, 14 and 15")
               + "A triangle has sides 13 cm, 14 cm and 15 cm. Find its area to 1 d.p.",
    "solutions": [84], "calculator": True, "input_type": "single_value",
    "hint": "Find one angle with the cosine rule, then use area = half times two sides times sin of that angle.",
    "guided_steps": [
        {"say": "No angle is given, so find one first. Use the cosine rule for the angle A between the sides 14 and 15 (opposite the side 13): \\(\\cos A = \\frac{14^2 + 15^2 - 13^2}{2(14)(15)}\\)."},
        {"pre": "Top line: 14² + 15² − 13² = 196 + 225 − 169 = ", "post": "", "answer": 252,
         "hint": "Square all three, then combine."},
        {"pre": "Bottom line: 2 × 14 × 15 = ", "post": "", "answer": 420,
         "hint": "2 × 14 × 15."},
        {"pre": "So cos A = 252 ÷ 420 = ", "post": "", "answer": 0.6,
         "hint": "Divide.", "phase": "substitute"},
        {"pre": "Angle A: cos⁻¹(0.6) = ", "post": "", "answer": R(math.degrees(math.acos(0.6))),
         "hint": "Inverse cosine, 1 d.p.", "done": f"A = {R(math.degrees(math.acos(0.6)))}{DEG}."},
        {"pre": "Now the area: ½ × 14 × 15 × sin 53.1° = ", "post": "", "answer": 84,
         "hint": "½ × 14 × 15 × sin A, 1 d.p.", "done": "So the area = 84.0 cm²."},
    ],
    "misconceptions": [
        {"pattern": "assume_right", "expect": 91,
         "message": "You assumed a right angle and did ½ × 13 × 14 = 91. The triangle is not right angled: find an angle with the cosine rule first, which gives an area of 84.0 cm².",
         "note": "0.5*13*14"}],
})
# G5 cosine side x9 y11 Z120 find z -> 17.3
gold.append({
    "display": tri_svg(9, 11, 17.35, {0:"X",1:"Y",2:"Z"},
                       sides={'a':"9", 'b':"11", 'c':"?"}, angles={2:f"120{DEG}"},
                       aria="Triangle XYZ with x 9, y 11 and the obtuse angle Z 120 degrees, side z unknown")
               + "In triangle XYZ, x = 9, y = 11, Z = 120°. Find side z to 1 d.p.",
    "solutions": [17.3], "calculator": True, "input_type": "single_value",
    "hint": "z squared = 9 squared + 11 squared minus 2 times 9 times 11 times cos 120; cos 120 is negative.",
    "guided_steps": [
        {"say": "Cosine rule for the side opposite Z: \\(z^2 = x^2 + y^2 - 2xy\\cos Z = 9^2 + 11^2 - 2(9)(11)\\cos 120°\\)."},
        {"pre": "Square and add: 9² + 11² = 81 + 121 = ", "post": "", "answer": 202,
         "hint": "Square each, then add."},
        {"pre": "The last term: 2 × 9 × 11 × cos 120° = ", "post": "", "answer": -99,
         "hint": "cos 120 = −0.5, so 198 × (−0.5).", "phase": "substitute"},
        {"pre": "So z² = 202 − (−99) = 202 + 99 = ", "post": "", "answer": 301,
         "hint": "Subtracting a negative adds.", "done": "z² = 301."},
        {"pre": "Square root: √301 = ", "post": "", "answer": 17.3,
         "hint": "Square root, 1 d.p.", "done": "So z = 17.3."},
    ],
    "misconceptions": [
        {"pattern": "sign_cos", "expect": 10.1,
         "message": "You treated cos 120 as positive. It is −0.5, so the term adds: z² = 202 + 99 = 301 and z = 17.3. Using +0.5 gives z² = 103 and z = 10.1.",
         "note": "sqrt(202-99)"}],
})
pb["gold"] = gold
pb["gold_description"] = ("Combine the rules: the ambiguous sine rule case, bearings, area to find an angle, "
                          "and three sides to an area.")

# ---------- tier_guides ----------
tier_guides = {
    "bronze": {
        "title": "Bronze: one rule, used once",
        "steps": [
            "Sine rule when you have a matching side and angle pair: \\(\\frac{a}{\\sin A} = \\frac{b}{\\sin B}\\).",
            "Area of a triangle from two sides and the angle between them: Area = \\(\\frac12 ab\\sin C\\).",
            "Cosine rule for a side from two sides and the included angle: \\(c^2 = a^2 + b^2 - 2ab\\cos C\\).",
        ],
        "example": {
            "question": "Find side a: A = 30°, B = 90°, b = 8.",
            "steps": [
                {"label": "Set up", "content": "a = b sin A ÷ sin B"},
                {"label": "Substitute", "content": "a = 8 × sin 30 ÷ sin 90"},
                {"label": "Check", "content": "sin 90 = 1, so a = 8 × 0.5"},
                {"label": "Answer", "content": "a = 4.0", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: cosine rule and bearings",
        "steps": [
            "Three sides and you want an angle: \\(\\cos A = \\frac{b^2 + c^2 - a^2}{2bc}\\), then inverse cosine.",
            "Two sides and the included angle for the third side: \\(a^2 = b^2 + c^2 - 2bc\\cos A\\).",
            "Bearings: find the interior angle from the two bearings first, then apply the cosine rule.",
        ],
        "example": {
            "question": "Find angle A: a = 7, b = 5, c = 6.",
            "steps": [
                {"label": "Set up", "content": "cos A = (5² + 6² − 7²) ÷ (2 × 5 × 6)"},
                {"label": "Work out", "content": "cos A = 12 ÷ 60 = 0.2"},
                {"label": "Check", "content": "cos⁻¹ gives an acute angle"},
                {"label": "Answer", "content": "A = 78.5°", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: pick and combine the rules",
        "steps": [
            "Ambiguous case: after finding an acute angle from the sine rule, also test 180 minus it.",
            "Area with no given angle: find an angle by the cosine rule first, then \\(\\frac12 ab\\sin C\\).",
            "Rearrange the area formula to find an angle: sin C = 2 × Area ÷ (ab).",
        ],
        "example": {
            "question": "Area 24, sides 8 and 12. Find the acute included angle.",
            "steps": [
                {"label": "Rearrange", "content": "sin C = 2 × 24 ÷ (8 × 12)"},
                {"label": "Work out", "content": "sin C = 48 ÷ 96 = 0.5"},
                {"label": "Check", "content": "acute, so use sin⁻¹"},
                {"label": "Answer", "content": "C = 30.0°", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------- guided (opener + teach) ----------
# opener SVG: 30-60-90 triangle, right angle marked, side opposite 30 = 5, hypotenuse ?
opener_svg = tri_svg(5, 8.66, 10, {0:"A",1:"B",2:"C"},
                     sides={'a':"5 cm", 'c':"?"}, angles={0:f"30{DEG}",1:f"60{DEG}",2:f"90{DEG}"}, right=2,
                     aria="A 30, 60, 90 triangle with the side opposite 30 degrees equal to 5 cm")

guided = {
    "opener": {
        "display": opener_svg + "In any triangle, the longer side always faces the bigger angle. This triangle has angles 30°, 60° and 90°, and the side facing the 30° angle is 5 cm.",
        "steps": [
            {"pre": "Which angle does the longest side face, the 30° angle or the 60° angle? Type the bigger angle: ",
             "post": "", "answer": 60, "hint": "The longer side faces the bigger angle."},
            {"pre": "In a 30-60-90 triangle the side facing 90° is exactly double the side facing 30°. If that short side is 5 cm, the longest side is 5 × 2 = ",
             "post": "", "answer": 10, "hint": "Double 5 cm."},
            {"say": "You used the rule that a bigger angle faces a longer side. The <strong>sine rule</strong> makes this exact: \\(\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C}\\), so every side is proportional to the sine of the angle facing it. When you cannot pair a side with its opposite angle, the <strong>cosine rule</strong> \\(a^2 = b^2 + c^2 - 2bc\\cos A\\) takes over."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "In triangle ABC, A = 40°, B = 75°, b = 13. Find side a to 1 d.p.",
            "steps": [
                {"say": "You have the pair (b, B) and the angle A, so use the sine rule and make a the subject: a = b sin A ÷ sin B."},
                {"pre": "Top line: 13 × sin 40° = ", "post": "", "answer": r4(13*sind(40)),
                 "hint": "13 × sin 40, 4 d.p."},
                {"pre": "Bottom line: sin 75° = ", "post": "", "answer": r4(sind(75)),
                 "hint": "sin 75, 4 d.p."},
                {"pre": f"Divide: {r4(13*sind(40))} ÷ {r4(sind(75))} = ", "post": "", "answer": R(13*sind(40)/sind(75)),
                 "hint": "Top divided by bottom, 1 d.p.", "done": f"So a = {R(13*sind(40)/sind(75))}."},
                {"pre": f"Check: {R(13*sind(40)/sind(75))} × sin 75° ÷ sin 40° rounds to ", "post": "", "answer": 13,
                 "hint": "Should return b.", "done": "Back to b = 13. Gone: that is the whole sine rule move."},
            ],
        },
        "silver": {
            "display": "A triangle has sides 7 cm and 9 cm with an included angle of 50°. Find the third side to 1 d.p.",
            "steps": [
                {"say": "No matching side-angle pair, so use the cosine rule: c² = a² + b² − 2ab cos C, with a = 7, b = 9, C = 50°."},
                {"pre": "Square and add: 7² + 9² = 49 + 81 = ", "post": "", "answer": 130,
                 "hint": "Square each, then add."},
                {"pre": "The subtracted part: 2 × 7 × 9 × cos 50° = ", "post": "", "answer": r4(126*cosd(50)),
                 "hint": "2 × 7 × 9 × cos 50, 4 d.p."},
                {"pre": f"So c² = 130 − {r4(126*cosd(50))} = ", "post": "", "answer": r4(130-126*cosd(50)),
                 "hint": "Subtract."},
                {"pre": f"Square root: √{r4(130-126*cosd(50))} = ", "post": "", "answer": R(math.sqrt(130-126*cosd(50))),
                 "hint": "Square root, 1 d.p.", "done": f"So the third side = {R(math.sqrt(130-126*cosd(50)))}. Gone: the cosine rule handles two sides and the angle between."},
            ],
        },
        "gold": {
            "display": "In triangle ABC, a = 9, b = 6, B = 35°. Find both possible values of angle A to 1 d.p.",
            "steps": [
                {"say": "Because a is longer than b, the sine rule can give two angles. Start with sin A = a sin B ÷ b."},
                {"pre": "Top line: 9 × sin 35° = ", "post": "", "answer": r4(9*sind(35)),
                 "hint": "9 × sin 35, 4 d.p."},
                {"pre": f"Divide by 6: {r4(9*sind(35))} ÷ 6 = ", "post": "", "answer": r4(9*sind(35)/6),
                 "hint": "That is sin A, 4 d.p."},
                {"pre": f"First value: sin⁻¹({r4(9*sind(35)/6)}) = ", "post": "", "answer": R(math.degrees(math.asin(9*sind(35)/6))),
                 "hint": "Inverse sine, 1 d.p."},
                {"pre": f"Second value: 180° − {R(math.degrees(math.asin(9*sind(35)/6)))}° = ", "post": "", "answer": R(180-math.degrees(math.asin(9*sind(35)/6))),
                 "hint": "Sine gives two angles under 180.",
                 "done": f"So A = {R(math.degrees(math.asin(9*sind(35)/6)))}{DEG} or {R(180-math.degrees(math.asin(9*sind(35)/6)))}{DEG}. Gone: that is the ambiguous case."},
            ],
        },
    },
}

# ---------- method_card (slim) ----------
method_card = {
    "title": "Sine Rule, Cosine Rule & Area Formula",
    "steps": [
        "Label sides a, b, c opposite angles A, B, C.",
        "A side and its opposite angle known: use the sine rule.",
        "Two sides and the included angle, or three sides: use the cosine rule.",
        "Area from two sides and the angle between them: ½ab sin C.",
    ],
    "content": ("<p><strong>Sine rule:</strong> \\(\\frac{a}{\\sin A} = \\frac{b}{\\sin B}\\), for a side or angle "
                "with a matching pair.</p><p><strong>Cosine rule (side):</strong> \\(a^2 = b^2 + c^2 - 2bc\\cos A\\) "
                "for two sides and the included angle.</p><p><strong>Cosine rule (angle):</strong> "
                "\\(\\cos A = \\frac{b^2 + c^2 - a^2}{2bc}\\) for three sides.</p>"
                "<p><strong>Area:</strong> \\(\\frac12 ab\\sin C\\).</p>"),
    "example": ("<p><strong>Find a when b = 8, A = 50°, B = 70°.</strong></p>"
                "<p>\\(a = \\frac{8\\sin 50°}{\\sin 70°} = 6.5\\)</p>"),
}

# ---------- keep preserved fields, assemble ----------
live = json.load(open("_live_geometry-L06.json", encoding="utf-8"))
out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "problem_bank": pb,
    "related_videos": live["related_videos"],
    "worked_examples": live["worked_examples"],
    "tier_guides": tier_guides,
    "guided": guided,
}

with open("lesson_maths-aqa_geometry-L06.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)

# sanity: word counts
def wc(s):
    return len([w for w in s.replace("\\(", " ").replace("\\)", " ").split() if w])
print("method_card.content words:", wc(method_card["content"]))
for t in ("bronze", "silver", "gold"):
    print(t, "tier_guide steps words:", sum(wc(s) for s in tier_guides[t]["steps"]))
print("wrote lesson_maths-aqa_geometry-L06.json")
