# -*- coding: utf-8 -*-
"""Build the full guided-learning + diagrams practice_data for maths-aqa geometry-L05."""
import json, io

LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_aqa_geoL05.json"
OUT  = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-aqa_geometry-L05.json"

pd = json.load(io.open(LIVE, encoding="utf-8"))

# ---------- SVG helpers ----------
TRI_HEAD = ('<svg viewBox="0 0 240 168" role="img" aria-label="{aria}" '
            'style="display:block;margin:0 auto 0.25rem;max-width:250px;width:100%">'
            '<polygon points="40,134 178,134 178,30" fill="#60a5fa" fill-opacity="0.15" '
            'stroke="currentColor" stroke-width="1.6"/>'
            '<path d="M167,123 h11 v11" fill="none" stroke="currentColor" stroke-width="1.2"/>')
ANGLE = ('<path d="M64.0,134.0 A24,24 0 0 0 59.2,119.6" fill="none" stroke="currentColor" '
         'stroke-width="1.2"/><text x="70" y="129" font-family="Inter,sans-serif" '
         'font-size="11" fill="currentColor">{t}</text>')
BOTTOM = ('<text x="109" y="152" font-family="Inter,sans-serif" font-size="11" '
          'fill="currentColor" text-anchor="middle">{t}</text>')
RIGHT = ('<text x="184" y="86" font-family="Inter,sans-serif" font-size="11" '
         'fill="currentColor" text-anchor="start">{t}</text>')
HYP = ('<text x="98" y="70" font-family="Inter,sans-serif" font-size="11" '
       'fill="currentColor" text-anchor="middle">{t}</text>')
CAP = '</svg><span class="figure-caption">Diagram not drawn accurately</span>'

def tri(aria, bottom=None, right=None, hyp=None, angle=None):
    s = TRI_HEAD.format(aria=aria)
    if angle: s += ANGLE.format(t=angle)
    if bottom: s += BOTTOM.format(t=bottom)
    if right: s += RIGHT.format(t=right)
    if hyp: s += HYP.format(t=hyp)
    return s + CAP

CLIFF = ('<svg viewBox="0 0 240 168" role="img" aria-label="A 25 m vertical cliff with a '
         'horizontal dashed line from the top, an angle of depression of 35 degrees down to a '
         'boat, and the horizontal distance to the boat marked with a question mark" '
         'style="display:block;margin:0 auto 0.25rem;max-width:250px;width:100%">'
         '<polygon points="46,30 46,134 206,134" fill="#f59e0b" fill-opacity="0.15" '
         'stroke="currentColor" stroke-width="1.6"/>'
         '<line x1="46" y1="30" x2="206" y2="30" stroke="currentColor" stroke-width="1" '
         'stroke-dasharray="4 3"/>'
         '<path d="M46,123 h11 v11" fill="none" stroke="currentColor" stroke-width="1.2"/>'
         '<path d="M72.0,30.0 A26,26 0 0 1 67.8,44.2" fill="none" stroke="currentColor" '
         'stroke-width="1.2"/>'
         '<text x="78" y="46" font-family="Inter,sans-serif" font-size="11" fill="currentColor">35°</text>'
         '<text x="34" y="86" font-family="Inter,sans-serif" font-size="11" fill="currentColor" '
         'text-anchor="end">25 m</text>'
         '<text x="126" y="152" font-family="Inter,sans-serif" font-size="11" fill="currentColor" '
         'text-anchor="middle">? m</text>'
         '<text x="212" y="138" font-family="Inter,sans-serif" font-size="12" fill="currentColor">⛵</text>'
         + CAP)

ISO = ('<svg viewBox="0 0 240 168" role="img" aria-label="Isosceles triangle with two equal '
       'sides of 10 cm, base 12 cm, and a dashed height line to the base marked with a question '
       'mark" style="display:block;margin:0 auto 0.25rem;max-width:250px;width:100%">'
       '<polygon points="120,28 46,134 194,134" fill="#34d399" fill-opacity="0.15" '
       'stroke="currentColor" stroke-width="1.6"/>'
       '<line x1="120" y1="28" x2="120" y2="134" stroke="currentColor" stroke-width="1.2" '
       'stroke-dasharray="4 3"/>'
       '<path d="M109,134 v-11 h11" fill="none" stroke="currentColor" stroke-width="1.2"/>'
       '<line x1="86.3" y1="83.3" x2="79.7" y2="78.7" stroke="currentColor" stroke-width="1.4"/>'
       '<line x1="160.3" y1="78.7" x2="153.7" y2="83.3" stroke="currentColor" stroke-width="1.4"/>'
       '<text x="72" y="76" font-family="Inter,sans-serif" font-size="11" fill="currentColor" '
       'text-anchor="middle">10 cm</text>'
       '<text x="168" y="76" font-family="Inter,sans-serif" font-size="11" fill="currentColor" '
       'text-anchor="middle">10 cm</text>'
       '<text x="120" y="152" font-family="Inter,sans-serif" font-size="11" fill="currentColor" '
       'text-anchor="middle">12 cm</text>'
       '<text x="126" y="92" font-family="Inter,sans-serif" font-size="11" fill="currentColor" '
       'text-anchor="start">?</text>' + CAP)

# Cuboid: front face + receding depth, space diagonal marked ?
CUBOID = ('<svg viewBox="0 0 240 168" role="img" aria-label="A cuboid with edges 4 cm, 3 cm and '
          '12 cm, and the space diagonal from one corner to the opposite corner marked with a '
          'question mark" style="display:block;margin:0 auto 0.25rem;max-width:250px;width:100%">'
          # back face (partly hidden) dashed
          '<line x1="74" y1="46" x2="174" y2="46" stroke="currentColor" stroke-width="1.2"/>'
          '<line x1="174" y1="46" x2="174" y2="106" stroke="currentColor" stroke-width="1.2"/>'
          '<line x1="74" y1="46" x2="74" y2="106" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>'
          '<line x1="74" y1="106" x2="174" y2="106" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>'
          # front face solid
          '<rect x="40" y="70" width="100" height="60" fill="#60a5fa" fill-opacity="0.12" '
          'stroke="currentColor" stroke-width="1.6"/>'
          # connectors
          '<line x1="40" y1="70" x2="74" y2="46" stroke="currentColor" stroke-width="1.4"/>'
          '<line x1="140" y1="70" x2="174" y2="46" stroke="currentColor" stroke-width="1.4"/>'
          '<line x1="140" y1="130" x2="174" y2="106" stroke="currentColor" stroke-width="1.4"/>'
          '<line x1="40" y1="130" x2="74" y2="106" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>'
          # space diagonal front-bottom-left(40,130) to back-top-right(174,46)
          '<line x1="40" y1="130" x2="174" y2="46" stroke="#f59e0b" stroke-width="1.8"/>'
          # labels
          '<text x="90" y="145" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">4 cm</text>'
          '<text x="146" y="104" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">3 cm</text>'
          '<text x="150" y="52" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">12 cm</text>'
          '<text x="86" y="80" font-family="Inter,sans-serif" font-size="12" font-weight="700" fill="currentColor" text-anchor="middle">?</text>'
          + CAP)

# ---------- guided_steps builders ----------
def pyth_hyp(a, b, c):
    aa, bb, cc = a*a, b*b, a*a+b*b
    return [
        {"pre": "%s² = " % a, "hint": "%s × %s." % (a, a), "answer": aa},
        {"pre": "%s² = " % b, "hint": "%s × %s." % (b, b), "answer": bb},
        {"pre": "Add the squares: %s + %s = " % (aa, bb), "hint": "Just add the two squares.", "answer": cc},
        {"pre": "Square root to get the hypotenuse: √%s = " % cc, "hint": "What number times itself makes %s?" % cc, "phase": "substitute", "answer": c},
        {"pre": "Check: %s² = " % c, "hint": "%s × %s." % (c, c), "done": "%s matches %s + %s, so the hypotenuse is %s cm." % (cc, aa, bb, c), "answer": c*c},
    ]

def pyth_leg(hyp, known, other):
    hh, kk, diff = hyp*hyp, known*known, hyp*hyp-known*known
    return [
        {"pre": "%s² = " % hyp, "hint": "%s × %s." % (hyp, hyp), "answer": hh},
        {"pre": "%s² = " % known, "hint": "%s × %s." % (known, known), "answer": kk},
        {"pre": "The hypotenuse is known, so subtract: %s − %s = " % (hh, kk), "hint": "Bigger square minus smaller square.", "answer": diff},
        {"pre": "√%s = " % diff, "hint": "What number times itself makes %s?" % diff, "phase": "substitute", "answer": other},
        {"pre": "Check: %s² + %s² = " % (other, known), "hint": "%s + %s." % (other*other, kk), "done": "%s = %s², so the missing side is %s cm." % (hh, hyp, other), "answer": hh},
    ]

pb = pd["problem_bank"]
B = pb["bronze"]; S = pb["silver"]; G = pb["gold"]

# ===== BRONZE =====
# B0 6,8 -> 10
B[0]["display"] = tri("Right-angled triangle with two shorter sides 6 cm and 8 cm and hypotenuse marked with a question mark", bottom="6 cm", right="8 cm", hyp="? cm") + B[0]["display"]
B[0]["hint"] = "Square both sides, add them, then square root."
B[0]["guided_steps"] = pyth_hyp(6, 8, 10)
B[0]["misconceptions"] = [{"pattern": "add_not_squared", "expect": 14, "message": "You added the sides: 6 + 8 = 14. Pythagoras squares first: c = √(6² + 8²) = √(36 + 64) = √100 = 10 cm."}]

# B1 hyp13 leg5 -> 12
B[1]["display"] = tri("Right-angled triangle with hypotenuse 13 cm, one shorter side 5 cm and the other shorter side marked with a question mark", bottom="5 cm", right="? cm", hyp="13 cm") + B[1]["display"]
B[1]["hint"] = "The hypotenuse is known, so subtract: square root of 13 squared minus 5 squared."
B[1]["guided_steps"] = pyth_leg(13, 5, 12)
B[1]["misconceptions"] = [{"pattern": "forgot_step", "expect": 13.9, "message": "You added: √(13² + 5²) = √194 ≈ 13.9. When the hypotenuse is known you SUBTRACT: a = √(13² − 5²) = √(169 − 25) = √144 = 12 cm."}]

# B2 9,12 -> 15
B[2]["display"] = tri("Right-angled triangle with two shorter sides 9 cm and 12 cm and hypotenuse marked with a question mark", bottom="9 cm", right="12 cm", hyp="? cm") + B[2]["display"]
B[2]["hint"] = "Square both sides, add them, then square root."
B[2]["guided_steps"] = pyth_hyp(9, 12, 15)
B[2]["misconceptions"] = [{"pattern": "add_not_squared", "expect": 21, "message": "You added the sides: 9 + 12 = 21. Square first: c = √(9² + 12²) = √(81 + 144) = √225 = 15 cm."}]

# B3 hyp10 leg6 -> 8
B[3]["display"] = tri("Right-angled triangle with hypotenuse 10 cm, one shorter side 6 cm and the other shorter side marked with a question mark", bottom="6 cm", right="? cm", hyp="10 cm") + B[3]["display"]
B[3]["hint"] = "The hypotenuse is known, so subtract: square root of 10 squared minus 6 squared."
B[3]["guided_steps"] = pyth_leg(10, 6, 8)
B[3]["misconceptions"] = [{"pattern": "forgot_step", "expect": 11.7, "message": "You added: √(10² + 6²) = √136 ≈ 11.7. The hypotenuse is known, so SUBTRACT: a = √(10² − 6²) = √(100 − 36) = √64 = 8 cm."}]

# B4 8,15 -> 17
B[4]["display"] = tri("Right-angled triangle with two shorter sides 8 cm and 15 cm and hypotenuse marked with a question mark", bottom="8 cm", right="15 cm", hyp="? cm") + B[4]["display"]
B[4]["hint"] = "Square both sides, add them, then square root."
B[4]["guided_steps"] = pyth_hyp(8, 15, 17)
B[4]["misconceptions"] = [{"pattern": "add_not_squared", "expect": 23, "message": "You added the sides: 8 + 15 = 23. Pythagoras squares first: c = √(8² + 15²) = √(64 + 225) = √289 = 17 cm."}]

# B5 7,24 -> 25
B[5]["display"] = tri("Right-angled triangle with two shorter sides 7 cm and 24 cm and hypotenuse marked with a question mark", bottom="7 cm", right="24 cm", hyp="? cm") + B[5]["display"]
B[5]["hint"] = "Square both sides, add them, then square root."
B[5]["guided_steps"] = pyth_hyp(7, 24, 25)
B[5]["misconceptions"] = [{"pattern": "add_not_squared", "expect": 31, "message": "You added the sides: 7 + 24 = 31. Square first: c = √(7² + 24²) = √(49 + 576) = √625 = 25 cm."}]

# B6 sin30 H18 -> O 9  (was H20 -> 10, duplicate fix)
B[6]["display"] = tri("Right-angled triangle with a 30 degree angle, hypotenuse 18 cm and the opposite side marked with a question mark", angle="30°", right="?", hyp="18 cm") + "Using \\(\\sin 30° = 0.5\\), find the opposite side in a right triangle with hypotenuse 18 cm."
B[6]["solutions"] = [9]
B[6]["hint"] = "The opposite side is the hypotenuse times the sine: 18 × 0.5."
B[6]["guided_steps"] = [
    {"pre": "sin30° = 0.5, and the opposite is the hypotenuse times this. First write the hypotenuse: ", "hint": "The longest side, given as 18 cm.", "answer": 18},
    {"pre": "O = 18 × 0.5 = ", "hint": "Multiply, do not divide.", "phase": "substitute", "answer": 9},
    {"pre": "Check: O ÷ H = 9 ÷ 18 = ", "hint": "Nine divided by eighteen.", "done": "0.5 = sin30°, so the opposite side is 9 cm.", "answer": 0.5},
]
B[6]["misconceptions"] = [{"pattern": "wrong_formula", "expect": 36, "message": "You divided: 18 ÷ 0.5 = 36. To find the opposite you MULTIPLY: O = H × sin30° = 18 × 0.5 = 9 cm."}]

# B7 cos60 H14 -> A 7
B[7]["display"] = tri("Right-angled triangle with a 60 degree angle, hypotenuse 14 cm and the adjacent side marked with a question mark", angle="60°", bottom="?", hyp="14 cm") + B[7]["display"]
B[7]["hint"] = "The adjacent side is the hypotenuse times the cosine: 14 × 0.5."
B[7]["guided_steps"] = [
    {"pre": "cos60° = 0.5, and the adjacent is the hypotenuse times this. First write the hypotenuse: ", "hint": "The longest side, given as 14 cm.", "answer": 14},
    {"pre": "A = 14 × 0.5 = ", "hint": "Multiply, do not divide.", "phase": "substitute", "answer": 7},
    {"pre": "Check: A ÷ H = 7 ÷ 14 = ", "hint": "Seven divided by fourteen.", "done": "0.5 = cos60°, so the adjacent side is 7 cm.", "answer": 0.5},
]
B[7]["misconceptions"] = [{"pattern": "wrong_formula", "expect": 28, "message": "You divided: 14 ÷ 0.5 = 28. To find the adjacent you MULTIPLY: A = H × cos60° = 14 × 0.5 = 7 cm."}]

# ===== SILVER =====
# S0 sin40 H15 -> O 9.6
S[0]["display"] = tri("Right-angled triangle with a 40 degree angle, hypotenuse 15 cm and the opposite side marked with a question mark", angle="40°", right="?", hyp="15 cm") + S[0]["display"]
S[0]["hint"] = "Opposite with hypotenuse points to sine: O = 15 × sin40°."
S[0]["guided_steps"] = [
    {"pre": "sin40°, to 2 d.p. = ", "hint": "Type sin(40) on the calculator.", "answer": 0.64},
    {"pre": "O = 15 × sin40° = ", "hint": "Multiply the hypotenuse by sin40°, keeping full accuracy.", "phase": "substitute", "answer": 9.6},
    {"pre": "Check: O ÷ H = 9.6 ÷ 15, to 2 d.p. = ", "hint": "9.6 divided by 15.", "done": "0.64 = sin40°, so the opposite side is 9.6 cm.", "answer": 0.64},
]
S[0]["misconceptions"] = [{"pattern": "wrong_formula", "expect": 11.5, "message": "You may have used cosine: 15 × cos40° ≈ 11.5. Opposite with hypotenuse means sine: O = 15 × sin40° = 15 × 0.643 ≈ 9.6 cm."}]

# S1 cos55 H12 -> A 6.9
S[1]["display"] = tri("Right-angled triangle with a 55 degree angle, hypotenuse 12 cm and the adjacent side marked with a question mark", angle="55°", bottom="?", hyp="12 cm") + S[1]["display"]
S[1]["hint"] = "Adjacent with hypotenuse points to cosine: A = 12 × cos55°."
S[1]["guided_steps"] = [
    {"pre": "cos55°, to 2 d.p. = ", "hint": "Type cos(55) on the calculator.", "answer": 0.57},
    {"pre": "A = 12 × cos55° = ", "hint": "Multiply the hypotenuse by cos55°, keeping full accuracy.", "phase": "substitute", "answer": 6.9},
    {"pre": "Check: A ÷ H = 6.9 ÷ 12, to 1 d.p. = ", "hint": "6.9 divided by 12, rounded to 1 d.p.", "done": "0.6 ≈ cos55°, so the adjacent side is 6.9 cm.", "answer": 0.6},
]
S[1]["misconceptions"] = [{"pattern": "wrong_formula", "expect": 9.8, "message": "You may have used sine: 12 × sin55° ≈ 9.8. Adjacent with hypotenuse means cosine: A = 12 × cos55° = 12 × 0.574 ≈ 6.9 cm."}]

# S2 opp7 hyp10 -> theta 44.4
S[2]["display"] = tri("Right-angled triangle with opposite side 7 cm, hypotenuse 10 cm and angle theta marked", angle="θ", right="7 cm", hyp="10 cm") + S[2]["display"]
S[2]["hint"] = "Opposite with hypotenuse points to sine: use inverse sine of 7 divided by 10."
S[2]["guided_steps"] = [
    {"pre": "Opposite over hypotenuse: 7 ÷ 10 = ", "hint": "Divide 7 by 10.", "answer": 0.7},
    {"pre": "θ = sin⁻¹(0.7) = ", "hint": "Press sin⁻¹, then 0.7.", "phase": "substitute", "answer": 44.4},
    {"pre": "Check: sin44.4°, to 2 d.p. = ", "hint": "Type sin(44.4) and round to 2 d.p.", "done": "0.70 matches 7 ÷ 10, so θ = 44.4°.", "answer": 0.7},
]
S[2]["misconceptions"] = [{"pattern": "wrong_formula", "expect": 45.6, "message": "You may have used cos⁻¹: cos⁻¹(7 ÷ 10) ≈ 45.6°. Opposite with hypotenuse means sine: θ = sin⁻¹(0.7) ≈ 44.4°."}]

# S3 opp8 adj6 -> theta 53.1
S[3]["display"] = tri("Right-angled triangle with opposite side 8 cm, adjacent side 6 cm and angle theta marked", angle="θ", bottom="6 cm", right="8 cm") + S[3]["display"]
S[3]["hint"] = "Opposite with adjacent points to tan: use inverse tan of 8 divided by 6."
S[3]["guided_steps"] = [
    {"pre": "Opposite over adjacent: 8 ÷ 6, to 2 d.p. = ", "hint": "Divide 8 by 6.", "answer": 1.33},
    {"pre": "θ = tan⁻¹(8 ÷ 6) = ", "hint": "Press tan⁻¹, then 8 ÷ 6; keep full accuracy.", "phase": "substitute", "answer": 53.1},
    {"pre": "Check: tan53.1°, to 2 d.p. = ", "hint": "Type tan(53.1) and round to 2 d.p.", "done": "1.33 matches 8 ÷ 6, so θ = 53.1°.", "answer": 1.33},
]
S[3]["misconceptions"] = [{"pattern": "wrong_formula", "expect": 36.9, "message": "You may have divided 6 by 8: tan⁻¹(6 ÷ 8) ≈ 36.9°. Opposite over adjacent is 8 over 6, so θ = tan⁻¹(8 ÷ 6) ≈ 53.1°."}]

# S4 ladder5 70 -> height 4.7
S[4]["display"] = tri("A ladder 5 m long as the hypotenuse of a right-angled triangle, making a 70 degree angle with the ground, and the height up the wall marked with a question mark", angle="70°", right="? m", hyp="5 m") + S[4]["display"]
S[4]["hint"] = "The height is opposite the 70° angle, so height = 5 × sin70°."
S[4]["guided_steps"] = [
    {"pre": "sin70°, to 2 d.p. = ", "hint": "Type sin(70) on the calculator.", "answer": 0.94},
    {"pre": "Height is opposite the angle: h = 5 × sin70° = ", "hint": "Multiply 5 by sin70°, keeping full accuracy.", "phase": "substitute", "answer": 4.7},
    {"pre": "Check: h ÷ 5 = 4.7 ÷ 5, to 2 d.p. = ", "hint": "4.7 divided by 5.", "done": "0.94 = sin70°, so the ladder reaches 4.7 m.", "answer": 0.94},
]
S[4]["misconceptions"] = [{"pattern": "wrong_formula", "expect": 1.7, "message": "You may have used cosine: 5 × cos70° ≈ 1.7 m, which is the distance along the ground. The height is opposite the 70° angle, so use sine: h = 5 × sin70° ≈ 4.7 m."}]

# S5 adj9 38 tan -> x 7.0
S[5]["display"] = tri("Right-angled triangle with a 38 degree angle, adjacent side 9 cm and the opposite side x marked with a question mark", angle="38°", bottom="9 cm", right="x") + S[5]["display"]
S[5]["hint"] = "Opposite with adjacent points to tan: x = 9 × tan38°."
S[5]["guided_steps"] = [
    {"pre": "tan38°, to 2 d.p. = ", "hint": "Type tan(38) on the calculator.", "answer": 0.78},
    {"pre": "x = 9 × tan38° = ", "hint": "Multiply the adjacent by tan38°, keeping full accuracy.", "phase": "substitute", "answer": 7.0},
    {"pre": "Check: x ÷ 9 = 7 ÷ 9, to 2 d.p. = ", "hint": "7 divided by 9.", "done": "0.78 = tan38°, so x = 7.0 cm.", "answer": 0.78},
]
S[5]["misconceptions"] = [{"pattern": "wrong_formula", "expect": 5.5, "message": "You may have used sine: 9 × sin38° ≈ 5.5. Opposite with adjacent means tangent: x = 9 × tan38° = 9 × 0.781 ≈ 7.0 cm."}]

# S6 legs 3.5,4.8 -> hyp 5.9
S[6]["display"] = tri("Right-angled triangle with two shorter sides 3.5 cm and 4.8 cm and hypotenuse marked with a question mark", bottom="3.5 cm", right="4.8 cm", hyp="? cm") + S[6]["display"]
S[6]["hint"] = "Both are shorter sides, so add: square root of 3.5 squared plus 4.8 squared."
S[6]["guided_steps"] = [
    {"pre": "3.5² = ", "hint": "3.5 × 3.5.", "answer": 12.25},
    {"pre": "4.8² = ", "hint": "4.8 × 4.8.", "answer": 23.04},
    {"pre": "Add the squares: 12.25 + 23.04 = ", "hint": "Just add the two squares.", "answer": 35.29},
    {"pre": "√35.29, to 1 d.p. = ", "hint": "Square root of 35.29 on the calculator.", "phase": "substitute", "answer": 5.9},
    {"pre": "Check: 5.9², to 2 d.p. = ", "hint": "5.9 × 5.9.", "done": "34.81 ≈ 35.29 (5.9 is rounded), so the hypotenuse is 5.9 cm.", "answer": 34.81},
]
S[6]["misconceptions"] = [{"pattern": "wrong_formula", "expect": 3.3, "message": "You may have subtracted: √(4.8² − 3.5²) ≈ 3.3. Both are shorter sides, so ADD: c = √(3.5² + 4.8²) = √35.29 ≈ 5.9 cm."}]

# ===== GOLD =====
# G0 cliff25 dep35 -> 35.7  (was 32 -> 40, duplicate fix)
G[0]["display"] = CLIFF + "From the top of a 25 m cliff, the angle of depression to a boat is 35°. How far is the boat from the base of the cliff? Give to 1 d.p."
G[0]["solutions"] = [35.7]
G[0]["hint"] = "The height is opposite and the distance is adjacent, so distance = 25 ÷ tan35°."
G[0]["guided_steps"] = [
    {"say": "The angle of depression from the top equals the angle of elevation at the boat, 35°. The height (25 m) is opposite that angle and the distance is adjacent, so tan35° = 25 ÷ distance, which rearranges to distance = 25 ÷ tan35°."},
    {"pre": "tan35°, to 3 d.p. = ", "hint": "Type tan(35) on the calculator.", "answer": 0.7},
    {"pre": "d = 25 ÷ tan35° = ", "hint": "Divide 25 by tan35°, keeping full accuracy.", "phase": "substitute", "answer": 35.7},
    {"pre": "Check: 35.7 × tan35°, to the nearest whole number = ", "hint": "35.7 × 0.700, rounded.", "done": "That returns the 25 m height, so the boat is 35.7 m away.", "answer": 25},
]
G[0]["misconceptions"] = [{"pattern": "wrong_formula", "expect": 17.5, "message": "You multiplied: 25 × tan35° ≈ 17.5. The height is opposite and the distance is adjacent, and the height is known, so DIVIDE: d = 25 ÷ tan35° ≈ 35.7 m."}]

# G1 isosceles 10,10,12 -> h 8
G[1]["display"] = ISO + G[1]["display"]
G[1]["hint"] = "Halve the base first, then the height, half-base and equal side form a right triangle."
G[1]["guided_steps"] = [
    {"pre": "Half the base: 12 ÷ 2 = ", "hint": "The height splits the base into two equal halves.", "answer": 6},
    {"pre": "The equal side is the hypotenuse: 10² = ", "hint": "Ten squared is 10 × 10.", "answer": 100},
    {"pre": "6² = ", "hint": "Six squared is 6 × 6.", "answer": 36},
    {"pre": "Subtract: 100 − 36 = ", "hint": "Bigger square minus smaller square.", "answer": 64},
    {"pre": "√64 = ", "hint": "What number times itself makes 64?", "phase": "substitute", "answer": 8},
    {"pre": "Check: 8² + 6² = ", "hint": "64 + 36.", "done": "100 = 10², so the height is 8 cm.", "answer": 100},
]
G[1]["misconceptions"] = [{"pattern": "forgot_step", "expect": None, "note": "Forgetting to halve gives sqrt(100-144) which is not real, so no single determinate wrong value.", "message": "Drop the height to the middle of the base. That makes a right triangle with hypotenuse 10 and base 6 (half of 12): h = √(10² − 6²) = √64 = 8 cm. Using the full base of 12 has no real answer, so always halve it first."}]

# G2 cuboid 3,4,12 -> 13
G[2]["display"] = CUBOID + G[2]["display"]
G[2]["hint"] = "Use all three dimensions: square root of 3 squared plus 4 squared plus 12 squared."
G[2]["guided_steps"] = [
    {"pre": "3² = ", "hint": "Three squared is 3 × 3.", "answer": 9},
    {"pre": "4² = ", "hint": "Four squared is 4 × 4.", "answer": 16},
    {"pre": "12² = ", "hint": "Twelve squared is 12 × 12.", "answer": 144},
    {"pre": "Add all three: 9 + 16 + 144 = ", "hint": "Add the three squares.", "answer": 169},
    {"pre": "√169 = ", "hint": "What number times itself makes 169? Try 13.", "phase": "substitute", "answer": 13},
    {"pre": "Check: 13² = ", "hint": "13 × 13.", "done": "169 matches 9 + 16 + 144, so the diagonal is 13 cm.", "answer": 169},
]
G[2]["misconceptions"] = [{"pattern": "2d_only", "expect": 5, "message": "You found only the base diagonal: √(3² + 4²) = 5. The space diagonal uses all three edges: √(3² + 4² + 12²) = √169 = 13 cm."}]

# G3 adj11 25 cos -> hyp 12.1
G[3]["display"] = tri("Right-angled triangle with a 25 degree angle, adjacent side 11 cm and the hypotenuse marked with a question mark", angle="25°", bottom="11 cm", hyp="? cm") + G[3]["display"]
G[3]["hint"] = "Adjacent with hypotenuse points to cosine, and the adjacent is known, so hypotenuse = 11 ÷ cos25°."
G[3]["guided_steps"] = [
    {"pre": "cos25°, to 2 d.p. = ", "hint": "Type cos(25) on the calculator.", "answer": 0.91},
    {"pre": "The adjacent is known, so divide: H = 11 ÷ cos25° = ", "hint": "Divide 11 by cos25°, keeping full accuracy.", "phase": "substitute", "answer": 12.1},
    {"pre": "Check: A ÷ H = 11 ÷ 12.1, to 2 d.p. = ", "hint": "11 divided by 12.1.", "done": "0.91 = cos25°, so the hypotenuse is 12.1 cm.", "answer": 0.91},
]
G[3]["misconceptions"] = [{"pattern": "wrong_formula", "expect": 10.0, "message": "You multiplied: 11 × cos25° ≈ 10.0. Here the adjacent is known and you want the hypotenuse, so DIVIDE: H = 11 ÷ cos25° ≈ 12.1 cm."}]

# G4 field 50,120 -> saving 40
G[4]["display"] = tri("Right-angled triangular field with shorter sides 120 m and 50 m and the diagonal path drawn as the hypotenuse", bottom="120 m", right="50 m", hyp="path") + G[4]["display"]
G[4]["hint"] = "Find the diagonal with Pythagoras, then subtract it from 50 + 120."
G[4]["guided_steps"] = [
    {"pre": "50² = ", "hint": "Fifty squared is 50 × 50.", "answer": 2500},
    {"pre": "120² = ", "hint": "One hundred and twenty squared.", "answer": 14400},
    {"pre": "Add the squares: 2500 + 14400 = ", "hint": "Just add the two squares.", "answer": 16900},
    {"pre": "√16900 = ", "hint": "What number times itself makes 16900? Try 130.", "answer": 130},
    {"pre": "Both sides together: 50 + 120 = ", "hint": "Add the two shorter sides.", "phase": "substitute", "answer": 170},
    {"pre": "How much shorter the diagonal is: 170 − 130 = ", "hint": "Both sides minus the diagonal.", "answer": 40},
    {"pre": "Check: 130 + 40 = ", "hint": "Diagonal plus the saving.", "done": "170 = 50 + 120, so the diagonal saves 40 m.", "answer": 170},
]
G[4]["misconceptions"] = [{"pattern": "forgot_step", "expect": 130, "message": "You may have stopped at the diagonal: √(50² + 120²) = √16900 = 130 m. The question asks how much SHORTER the diagonal is: 170 − 130 = 40 m."}]

# ---------- tier descriptions ----------
pb["bronze_description"] = "Put the given numbers straight into one formula: square, add or subtract and root for Pythagoras, or multiply by a given sine or cosine for a side."
pb["silver_description"] = "Decide the method first, then rearrange it: choose Pythagoras or the right trig ratio, substitute and solve, often with a calculator or inside a real shape."
pb["gold_description"] = "Turn a worded or real situation into a right-angled triangle, then finish with Pythagoras or trigonometry, sometimes reaching into three dimensions."

# ---------- tier_guides ----------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one formula, straight in",
        "steps": [
            "Read the two known values straight off the triangle. No rearranging needed yet.",
            "For Pythagoras, square both sides then add for the hypotenuse, or subtract then square root for a shorter side.",
            "For a trig side you are given the ratio (like \\(\\sin 30° = 0.5\\)): multiply the hypotenuse by it."
        ],
        "example": {
            "question": "Find the hypotenuse: sides 6 cm and 8 cm.",
            "steps": [
                {"label": "Square and add", "content": "<p>\\(6^2 + 8^2 = 36 + 64 = 100\\)</p>"},
                {"label": "Square root", "content": "<p>\\(c = \\sqrt{100} = 10\\)</p>"},
                {"label": "Check", "content": "<p>\\(6^2 + 8^2 = 100 = 10^2\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(c = 10\\) cm</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: choose and rearrange",
        "steps": [
            "Nothing is handed to you ready to use. First decide: Pythagoras (three sides, no angle) or a trig ratio (an angle is involved).",
            "Pick the ratio that pairs your two sides: \\(\\sin\\) for O and H, \\(\\cos\\) for A and H, \\(\\tan\\) for O and A. Rearrange to make the unknown the subject.",
            "Real shapes count too: split an isosceles triangle down the middle, or read the diagonal of a rectangle as a hypotenuse."
        ],
        "example": {
            "question": "Find the opposite side when \\(\\theta = 30°\\) and the hypotenuse is 14 cm.",
            "steps": [
                {"label": "Choose ratio", "content": "<p>Opposite and hypotenuse, so \\(\\sin\\theta = \\frac{O}{H}\\), giving \\(O = H\\sin\\theta\\).</p>"},
                {"label": "Substitute", "content": "<p>\\(O = 14 \\times \\sin 30° = 14 \\times 0.5 = 7\\)</p>"},
                {"label": "Check", "content": "<p>\\(7 \\div 14 = 0.5 = \\sin 30°\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(O = 7\\) cm</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: build the triangle from the words",
        "steps": [
            "The right triangle is hidden in a story, a real shape, or a solid. Sketch it and label the sides you are told.",
            "Journeys give two legs (find the hypotenuse). Elevation and depression give an angle with a height and a distance (use \\(\\tan\\)).",
            "For a cuboid, the space diagonal uses all three edges: \\(\\sqrt{a^2 + b^2 + c^2}\\)."
        ],
        "example": {
            "question": "A ship sails 9 km east then 12 km north. How far is it from the start?",
            "steps": [
                {"label": "Set up", "content": "<p>The two legs are 9 and 12; the direct distance is the hypotenuse.</p>"},
                {"label": "Pythagoras", "content": "<p>\\(9^2 + 12^2 = 81 + 144 = 225\\)</p>"},
                {"label": "Check", "content": "<p>\\(\\sqrt{225} = 15\\), and \\(15^2 = 225\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(15\\) km</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------- guided (opener + teach) ----------
OPENER_SVG = ('<svg viewBox="14 0 232 248" style="display:block;margin:0 auto 0.25rem;'
              'max-width:250px;width:100%" role="img" aria-label="Right-angled triangle, short '
              'sides 3 and 4, with a tiled square drawn on each of the three sides">')
# tiles for the 3x3 square (blue) on the vertical short side
for c in range(3):
    for r in range(3):
        OPENER_SVG += '<rect x="%d" y="%d" width="18" height="18" fill="#dbeafe" stroke="#fff" stroke-width="1.2"/>' % (41+18*c, 96+18*r)
# tiles for the 4x4 square (amber) on the horizontal short side
for c in range(4):
    for r in range(4):
        OPENER_SVG += '<rect x="%d" y="%d" width="18" height="18" fill="#fef3c7" stroke="#fff" stroke-width="1.2"/>' % (95+18*c, 150+18*r)
# tiles for the 5x5 square (green) on the hypotenuse, rotated
OPENER_SVG += '<g transform="translate(167,150) rotate(216.87)">'
for c in range(5):
    for r in range(5):
        OPENER_SVG += '<rect x="%d" y="%d" width="18" height="18" fill="#dcfce7" stroke="#fff" stroke-width="1.2"/>' % (18*c, 18*r)
OPENER_SVG += '</g>'
OPENER_SVG += ('<polygon points="95,150 167,150 95,96" fill="#f3ece2" stroke="currentColor" stroke-width="1.6"/>'
               '<rect x="95" y="142" width="8" height="8" fill="none" stroke="currentColor" stroke-width="1.2"/>'
               '<text x="68" y="127" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">9 tiles</text>'
               '<text x="131" y="190" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">16 tiles</text>'
               '<text x="158" y="90" font-family="Inter,sans-serif" font-size="13" font-weight="700" fill="currentColor" text-anchor="middle">? tiles</text>'
               '<text x="102" y="127" font-family="Inter,sans-serif" font-size="11" font-weight="700" fill="currentColor">3</text>'
               '<text x="128" y="146" font-family="Inter,sans-serif" font-size="11" font-weight="700" fill="currentColor" text-anchor="middle">4</text>'
               '</svg><span style="font-size:0.8rem;font-weight:400">Short sides 3 and 4, a tiled square on every side.</span>')

pd["guided"] = {
    "opener": {
        "label": "Before any formula",
        "display": OPENER_SVG,
        "steps": [
            {"say": "Here is a right-angled triangle with a square tiled onto each side. No formula needed, just count and add.",
             "pre": "The two smaller squares hold 9 tiles and 16 tiles. Altogether that is 9 + 16 = ",
             "hint": "Just add the two tile counts.", "answer": 25},
            {"say": "The clever bit: the square on the longest side holds exactly that many tiles too, 25. That is Pythagoras, the two smaller squares add up to the biggest one.",
             "pre": "A square made of 25 tiles is how many tiles along each edge? ",
             "hint": "What number times itself makes 25?", "answer": 5},
            {"say": "So the longest side is 5. In symbols, the short sides \\(a\\) and \\(b\\) and the longest side \\(c\\) obey \\(a^2 + b^2 = c^2\\). Squaring a side counts the tiles in its square; square rooting turns the tile count back into a length."}
        ]
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "Find the hypotenuse of a right triangle with shorter sides 12 cm and 16 cm.",
            "steps": [
                {"say": "The two shorter sides are 12 and 16. Pythagoras says: square each, add, then square root."},
                {"pre": "12² = ", "hint": "12 × 12.", "answer": 144},
                {"pre": "16² = ", "hint": "16 × 16.", "answer": 256},
                {"pre": "Add the squares: 144 + 256 = ", "hint": "Just add them.", "answer": 400},
                {"pre": "Square root to get the hypotenuse: √400 = ", "hint": "What number times itself makes 400? Try 20.", "done": "Square, add, root. That is the whole method.", "answer": 20},
                {"pre": "Check: 20² = ", "hint": "20 × 20.", "done": "400 = 144 + 256, so the hypotenuse is 20 cm.", "answer": 400}
            ]
        },
        "silver": {
            "label": "Together: the silver move",
            "display": "In a right triangle the opposite side is 9 cm and the adjacent side is 12 cm. Find the angle \\(\\theta\\) to 1 d.p.",
            "steps": [
                {"say": "You know the opposite and the adjacent, so the ratio is tan. To get the angle back, use inverse tan, the new move at this level."},
                {"pre": "The ratio, opposite ÷ adjacent: 9 ÷ 12 = ", "hint": "Divide 9 by 12.", "answer": 0.75},
                {"pre": "Inverse tan turns that ratio into the angle: θ = tan⁻¹(0.75) = ", "hint": "Press tan⁻¹, then 0.75.", "done": "Inverse tan undoes tan to reveal the angle. That was the point.", "answer": 36.9},
                {"pre": "The two acute angles add to 90°, so the other one is 90 − 36.9 = ", "hint": "Ninety minus 36.9.", "answer": 53.1},
                {"pre": "Check: tan36.9°, to 2 d.p. = ", "hint": "Type tan(36.9) and round to 2 d.p.", "done": "0.75 matches 9 ÷ 12, so θ = 36.9°.", "answer": 0.75}
            ]
        },
        "gold": {
            "label": "Together: the gold move",
            "display": "A ramp rises 1.5 m over a horizontal run of 8 m. Find the angle the ramp makes with the ground, to 1 d.p.",
            "steps": [
                {"say": "Draw the right triangle out of the words: the rise, 1.5 m, is opposite the angle; the run, 8 m, is adjacent. Opposite and adjacent means tan."},
                {"pre": "The ratio, rise ÷ run: 1.5 ÷ 8, to 2 d.p. = ", "hint": "Divide 1.5 by 8.", "answer": 0.19},
                {"pre": "Inverse tan gives the angle: θ = tan⁻¹(1.5 ÷ 8) = ", "hint": "Press tan⁻¹, then 1.5 ÷ 8; keep full accuracy.", "done": "Reading the triangle out of the words is the gold move.", "answer": 10.6},
                {"pre": "Check: tan10.6°, to 2 d.p. = ", "hint": "Type tan(10.6) and round to 2 d.p.", "done": "0.19 matches the ratio, so the ramp sits at 10.6°.", "answer": 0.19},
                {"pre": "The ramp itself is the hypotenuse: √(1.5² + 8²) = √66.25, to 1 d.p. = ", "hint": "Square root of 66.25 on the calculator.", "done": "Same triangle, Pythagoras gives the ramp's length: 8.1 m.", "answer": 8.1}
            ]
        }
    }
}

# ---------- method_card (slim) ----------
pd["method_card"] = {
    "title": "How to Use Pythagoras & SOHCAHTOA",
    "steps": [
        "Label the sides: hypotenuse (longest, opposite the right angle), then opposite and adjacent relative to the angle.",
        "Two sides and no angle: use Pythagoras. An angle is involved: use SOHCAHTOA.",
        "Substitute into the formula and solve: square root for Pythagoras, or inverse trig for an angle."
    ],
    "content": "<p><strong>Pythagoras:</strong> in a right-angled triangle \\(a^2 + b^2 = c^2\\), where \\(c\\) is the hypotenuse (longest side, opposite the right angle). To find the hypotenuse, \\(c = \\sqrt{a^2 + b^2}\\); to find a shorter side, subtract: \\(a = \\sqrt{c^2 - b^2}\\).</p><p><strong>SOHCAHTOA</strong> links an angle to two sides: \\(\\sin\\theta = \\frac{O}{H}\\), \\(\\cos\\theta = \\frac{A}{H}\\), \\(\\tan\\theta = \\frac{O}{A}\\). To find a side, rearrange; to find an angle, use \\(\\sin^{-1}\\), \\(\\cos^{-1}\\) or \\(\\tan^{-1}\\). Keep the calculator in degrees.</p>",
    "example": "<p><strong>Find the hypotenuse of a right triangle with sides 5 cm and 12 cm.</strong></p><p>\\(c = \\sqrt{5^2 + 12^2} = \\sqrt{25 + 144} = \\sqrt{169} = 13\\) cm</p>"
}

# related_videos, worked_examples, topic_links preserved untouched.
json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written", OUT)
print("method_card content words:", len(pd["method_card"]["content"].replace("\\("," ").replace("\\)"," ").split()))
