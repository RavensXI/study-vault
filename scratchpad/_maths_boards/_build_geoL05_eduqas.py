# -*- coding: utf-8 -*-
import json, io, math

# ---------- SVG helpers (theme-safe; text currentColor; soft region fills) ----------
STY = 'style="display:block;margin:0 auto 0.25rem;max-width:250px;width:100%"'
CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

def tri(aria, bottom=None, right=None, hyp=None, angle_label=None):
    """Right triangle, right angle at bottom-right (178,134). Optional angle arc at bottom-left."""
    s = '<svg viewBox="0 0 240 168" role="img" aria-label="%s" %s>' % (aria, STY)
    s += '<polygon points="40,134 178,134 178,30" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'
    s += '<path d="M167,123 h11 v11" fill="none" stroke="currentColor" stroke-width="1.2"/>'
    if angle_label is not None:
        s += '<path d="M64.0,134.0 A24,24 0 0 0 59.2,119.6" fill="none" stroke="currentColor" stroke-width="1.2"/>'
        s += '<text x="70" y="129" font-family="Inter,sans-serif" font-size="11" fill="currentColor">%s</text>' % angle_label
    if bottom is not None:
        s += '<text x="109" y="152" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % bottom
    if right is not None:
        s += '<text x="184" y="86" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">%s</text>' % right
    if hyp is not None:
        s += '<text x="98" y="70" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % hyp
    s += '</svg>' + CAP
    return s

def rect_diag(aria, width, length, diag):
    s = '<svg viewBox="0 0 240 158" role="img" aria-label="%s" %s>' % (aria, STY)
    s += '<rect x="34" y="34" width="172" height="90" fill="#60a5fa" fill-opacity="0.12" stroke="currentColor" stroke-width="1.6"/>'
    s += '<line x1="34" y1="124" x2="206" y2="34" stroke="currentColor" stroke-width="1.4"/>'
    s += '<path d="M34,124 h11 v-11" fill="none" stroke="currentColor" stroke-width="1.2"/>'
    s += '<text x="26" y="82" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="end">%s</text>' % width
    s += '<text x="120" y="140" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % length
    s += '<text x="128" y="72" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % diag
    s += '</svg>' + CAP
    return s

def isosceles(aria):
    # equal sides 10, base 12, dashed height ?
    s = '<svg viewBox="0 0 240 168" role="img" aria-label="%s" %s>' % (aria, STY)
    s += '<polygon points="120,28 46,134 194,134" fill="#34d399" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'
    s += '<line x1="120" y1="28" x2="120" y2="134" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>'
    s += '<path d="M109,134 v-11 h11" fill="none" stroke="currentColor" stroke-width="1.2"/>'
    s += '<line x1="86.3" y1="83.3" x2="79.7" y2="78.7" stroke="currentColor" stroke-width="1.4"/>'
    s += '<line x1="160.3" y1="78.7" x2="153.7" y2="83.3" stroke="currentColor" stroke-width="1.4"/>'
    s += '<text x="72" y="76" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">10 cm</text>'
    s += '<text x="168" y="76" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">10 cm</text>'
    s += '<text x="120" y="152" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">12 cm</text>'
    s += '<text x="126" y="92" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">?</text>'
    s += '</svg>' + CAP
    return s

def cliff(aria):
    # 40 m vertical cliff, dashed horizontal top, 25 deg depression, ? m base
    s = '<svg viewBox="0 0 240 168" role="img" aria-label="%s" %s>' % (aria, STY)
    s += '<polygon points="46,30 46,134 206,134" fill="#f59e0b" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'
    s += '<line x1="46" y1="30" x2="206" y2="30" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>'
    s += '<path d="M46,123 h11 v11" fill="none" stroke="currentColor" stroke-width="1.2"/>'
    s += '<path d="M72.0,30.0 A26,26 0 0 1 67.8,44.2" fill="none" stroke="currentColor" stroke-width="1.2"/>'
    s += '<text x="78" y="46" font-family="Inter,sans-serif" font-size="11" fill="currentColor">25°</text>'
    s += '<text x="34" y="86" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="end">40 m</text>'
    s += '<text x="126" y="152" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">? m</text>'
    s += '<text x="212" y="138" font-family="Inter,sans-serif" font-size="12" fill="currentColor">⛵</text>'
    s += '</svg>' + CAP
    return s

def coordgrid(aria):
    # grid 0..5 x, 0..7 y; A(1,2) B(4,6); legs 3 and 4; hyp ?
    ox, oy, ux, uy = 28, 182, 30, 22
    def px(x): return ox + x * ux
    def py(y): return oy - y * uy
    s = '<svg viewBox="0 0 200 210" role="img" aria-label="%s" %s>' % (aria, STY)
    # grid
    for x in range(0, 6):
        s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-opacity="0.15" stroke-width="1"/>' % (px(x), py(0), px(x), py(7))
    for y in range(0, 8):
        s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-opacity="0.15" stroke-width="1"/>' % (px(0), py(y), px(5), py(y))
    # axes
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.4"/>' % (px(0), py(0), px(5), py(0))
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.4"/>' % (px(0), py(0), px(0), py(7))
    ax, ay, bx, by = px(1), py(2), px(4), py(6)
    # legs (dashed) and hypotenuse
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>' % (ax, ay, bx, ay)
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>' % (bx, ay, bx, by)
    s += '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#60a5fa" stroke-width="1.8"/>' % (ax, ay, bx, by)
    # points
    s += '<circle cx="%d" cy="%d" r="3.2" fill="#60a5fa"/>' % (ax, ay)
    s += '<circle cx="%d" cy="%d" r="3.2" fill="#60a5fa"/>' % (bx, by)
    # labels
    s += '<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="end">(1, 2)</text>' % (ax - 5, ay + 4)
    s += '<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="10" fill="currentColor">(4, 6)</text>' % (bx + 6, by + 3)
    s += '<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">3</text>' % ((ax + bx) // 2, ay + 13)
    s += '<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="10" fill="currentColor">4</text>' % (bx + 5, (ay + by) // 2)
    s += '<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" font-weight="700" fill="currentColor" text-anchor="middle">?</text>' % ((ax + bx) // 2 - 8, (ay + by) // 2 - 3)
    s += '</svg>' + CAP
    return s

def ship_bearing(aria):
    # triangle: east 12 (bottom), north 9 (right vertical), return = hyp; North arrow at start (40,134)
    s = '<svg viewBox="0 0 240 168" role="img" aria-label="%s" %s>' % (aria, STY)
    s += '<polygon points="40,134 178,134 178,30" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1.6"/>'
    s += '<path d="M167,123 h11 v11" fill="none" stroke="currentColor" stroke-width="1.2"/>'
    # North arrow at start vertex
    s += '<line x1="40" y1="134" x2="40" y2="104" stroke="currentColor" stroke-width="1.2"/>'
    s += '<path d="M40,102 l-4,7 h8 z" fill="currentColor"/>'
    s += '<text x="40" y="98" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">N</text>'
    s += '<text x="109" y="152" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">12 km east</text>'
    s += '<text x="184" y="86" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="start">9 km north</text>'
    s += '<text x="96" y="70" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">return</text>'
    s += '</svg>' + CAP
    return s

# tiled-squares Pythagoras opener SVG (3,4,5). Text uses currentColor; tile fills are soft.
def opener_svg():
    s = '<svg viewBox="14 0 232 248" style="display:block;margin:0 auto 0.25rem;max-width:250px;width:100%" role="img" aria-label="Right-angled triangle with short sides 3 and 4 and a tiled square drawn on each of the three sides">'
    # 3x3 blue square on vertical leg (9 tiles), x 41..95, y 96..150
    for cx in (41, 59, 77):
        for cy in (96, 114, 132):
            s += '<rect x="%d" y="%d" width="18" height="18" fill="#dbeafe" stroke="#fff" stroke-width="1.2"/>' % (cx, cy)
    # 4x4 yellow square on horizontal leg (16 tiles), x 95..167, y 150..222
    for cx in (95, 113, 131, 149):
        for cy in (150, 168, 186, 204):
            s += '<rect x="%d" y="%d" width="18" height="18" fill="#fef3c7" stroke="#fff" stroke-width="1.2"/>' % (cx, cy)
    # 5x5 green square on hypotenuse (25 tiles), rotated about (167,150)
    s += '<g transform="translate(167,150) rotate(216.87)">'
    for gx in (0, 18, 36, 54, 72):
        for gy in (0, 18, 36, 54, 72):
            s += '<rect x="%d" y="%d" width="18" height="18" fill="#dcfce7" stroke="#fff" stroke-width="1.2"/>' % (gx, gy)
    s += '</g>'
    # triangle
    s += '<polygon points="95,150 167,150 95,96" fill="#f3ece2" stroke="currentColor" stroke-width="1.6"/>'
    s += '<rect x="95" y="142" width="8" height="8" fill="none" stroke="currentColor" stroke-width="1.2"/>'
    s += '<text x="68" y="127" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">9 tiles</text>'
    s += '<text x="131" y="190" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">16 tiles</text>'
    s += '<text x="158" y="90" font-family="Inter,sans-serif" font-size="13" font-weight="700" fill="currentColor" text-anchor="middle">? tiles</text>'
    s += '<text x="102" y="127" font-family="Inter,sans-serif" font-size="11" font-weight="700" fill="currentColor">3</text>'
    s += '<text x="128" y="146" font-family="Inter,sans-serif" font-size="11" font-weight="700" fill="currentColor" text-anchor="middle">4</text>'
    s += '</svg><span style="font-size:0.8rem;font-weight:400">Short sides 3 and 4, a tiled square on every side.</span>'
    return s

def box(pre, answer, hint, post=None, done=None, say=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post is not None: d["post"] = post
    if done is not None: d["done"] = done
    if say is not None: d["say"] = say
    if phase is not None: d["phase"] = phase
    return d

def say(text):
    return {"say": text}

# ---------------- PROBLEM BANK ----------------
bronze = [
 {  # B1
  "display": tri("Right-angled triangle with two shorter sides 3 cm and 4 cm and the hypotenuse marked with a question mark", bottom="3 cm", right="4 cm", hyp="? cm") + "Find the hypotenuse: sides 3 cm and 4 cm.",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Square both sides, add them, then square root.",
  "guided_steps": [
    box("3² = ", 9, "Three squared is 3 × 3."),
    box("4² = ", 16, "Four squared is 4 × 4."),
    box("Add the squares: 9 + 16 = ", 25, "Just add the two squares."),
    box("Square root to get the hypotenuse: √25 = ", 5, "What number times itself makes 25?", phase="substitute"),
    box("Check: 5² = ", 25, "Five squared is 5 × 5.", done="25 matches 9 + 16, so the hypotenuse is 5 cm."),
  ],
  "misconceptions": [{"check": "common", "expect": 7, "pattern": "wrong_formula",
    "message": "You added the sides: 3 + 4 = 7. Pythagoras squares first: c = √(3² + 4²) = √(9 + 16) = √25 = 5."}],
 },
 {  # B2
  "display": tri("Right-angled triangle with two shorter sides 8 cm and 15 cm and the hypotenuse marked with a question mark", bottom="8 cm", right="15 cm", hyp="? cm") + "Find the hypotenuse: sides 8 cm and 15 cm.",
  "solutions": [17], "calculator": False, "input_type": "single_value",
  "hint": "Square both sides, add them, then square root.",
  "guided_steps": [
    box("8² = ", 64, "Eight squared is 8 × 8."),
    box("15² = ", 225, "Fifteen squared is 15 × 15."),
    box("Add the squares: 64 + 225 = ", 289, "Just add the two squares."),
    box("√289 = ", 17, "What number times itself makes 289? Try 17.", phase="substitute"),
    box("Check: 17² = ", 289, "17 × 17.", done="289 matches 64 + 225, so the hypotenuse is 17 cm."),
  ],
  "misconceptions": [{"check": "common", "expect": 23, "pattern": "wrong_formula",
    "message": "You added the sides: 8 + 15 = 23. Square first: c = √(8² + 15²) = √(64 + 225) = √289 = 17."}],
 },
 {  # B3
  "display": tri("Right-angled triangle with hypotenuse 13 cm, one shorter side 5 cm and the other shorter side marked with a question mark", bottom="5 cm", right="? cm", hyp="13 cm") + "Find the shorter side: hypotenuse 13 cm, other side 5 cm.",
  "solutions": [12], "calculator": False, "input_type": "single_value",
  "hint": "The hypotenuse is known, so subtract the squares before rooting.",
  "guided_steps": [
    box("13² = ", 169, "Thirteen squared is 13 × 13."),
    box("5² = ", 25, "Five squared is 5 × 5."),
    box("The hypotenuse is known, so subtract: 169 − 25 = ", 144, "Bigger square minus smaller square."),
    box("√144 = ", 12, "What number times itself makes 144?", phase="substitute"),
    box("Check: 12² + 5² = ", 169, "144 + 25.", done="169 = 13², so the missing side is 12 cm."),
  ],
  "misconceptions": [{"check": "common", "expect": 13.9, "pattern": "forgot_step",
    "message": "You added: √(13² + 5²) = √194 ≈ 13.9. When the hypotenuse is known you SUBTRACT: a = √(13² − 5²) = √(169 − 25) = √144 = 12."}],
 },
 {  # B4
  "display": tri("Right-angled triangle with hypotenuse 10 cm, one shorter side 6 cm and the other shorter side marked with a question mark", bottom="6 cm", right="? cm", hyp="10 cm") + "Find the shorter side: hypotenuse 10 cm, other side 6 cm.",
  "solutions": [8], "calculator": False, "input_type": "single_value",
  "hint": "The hypotenuse is known, so subtract the squares before rooting.",
  "guided_steps": [
    box("10² = ", 100, "Ten squared is 10 × 10."),
    box("6² = ", 36, "Six squared is 6 × 6."),
    box("The hypotenuse is known, so subtract: 100 − 36 = ", 64, "Bigger square minus smaller square."),
    box("√64 = ", 8, "What number times itself makes 64?", phase="substitute"),
    box("Check: 8² + 6² = ", 100, "64 + 36.", done="100 = 10², so the missing side is 8 cm."),
  ],
  "misconceptions": [{"check": "common", "expect": 11.7, "pattern": "forgot_step",
    "message": "You added: √(10² + 6²) = √136 ≈ 11.7. When the hypotenuse is known you SUBTRACT: a = √(10² − 6²) = √(100 − 36) = √64 = 8."}],
 },
 {  # B5
  "display": tri("Right-angled triangle with two shorter sides 7 cm and 24 cm and the hypotenuse marked with a question mark", bottom="7 cm", right="24 cm", hyp="? cm") + "A right triangle has sides 7 cm and 24 cm. Find the hypotenuse.",
  "solutions": [25], "calculator": False, "input_type": "single_value",
  "hint": "Square both sides, add them, then square root.",
  "guided_steps": [
    box("7² = ", 49, "Seven squared is 7 × 7."),
    box("24² = ", 576, "Twenty-four squared is 24 × 24."),
    box("Add the squares: 49 + 576 = ", 625, "Just add the two squares."),
    box("√625 = ", 25, "What number times itself makes 625? Try 25.", phase="substitute"),
    box("Check: 25² = ", 625, "25 × 25.", done="625 matches 49 + 576, so the hypotenuse is 25 cm."),
  ],
  "misconceptions": [{"check": "common", "expect": 31, "pattern": "wrong_formula",
    "message": "You added the sides: 7 + 24 = 31. Square first: c = √(7² + 24²) = √(49 + 576) = √625 = 25."}],
 },
 {  # B6 conceptual MCQ preserved
  "display": tri("Triangle with sides 9, 12 and 15 labelled, to be tested for a right angle", bottom="9", right="12", hyp="15") + "Is a triangle with sides 9, 12, 15 right-angled?",
  "options": ["Yes, because \\(9^2 + 12^2 = 15^2\\)", "No, the sides do not satisfy Pythagoras", "Yes, because it is isosceles", "No, 15 is too long"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Work out 9² + 12² and compare it with 15².",
  "misconceptions": [
    {"check": "wrong_calc", "expect": None, "pattern": "wrong_calc",
     "message": "9² + 12² = 81 + 144 = 225, and 15² = 225. They match, so it IS right-angled."},
    {"check": "confused", "expect": None, "pattern": "confused",
     "message": "The test is: does a² + b² = c²? Here 81 + 144 = 225 = 15², so yes."},
  ],
 },
 {  # B7
  "display": tri("Right-angled triangle with two shorter sides 9 and 40 and the hypotenuse labelled x", bottom="9", right="40", hyp="x") + "Find \\(x\\): hypotenuse \\(x\\), shorter sides 9 and 40.",
  "solutions": [41], "calculator": False, "input_type": "single_value",
  "hint": "Square both shorter sides, add, then square root.",
  "guided_steps": [
    box("9² = ", 81, "Nine squared is 9 × 9."),
    box("40² = ", 1600, "Forty squared is 40 × 40."),
    box("Add the squares: 81 + 1600 = ", 1681, "Just add the two squares."),
    box("√1681 = ", 41, "What number times itself makes 1681? Try 41.", phase="substitute"),
    box("Check: 41² = ", 1681, "41 × 41.", done="1681 matches 81 + 1600, so x = 41."),
  ],
  "misconceptions": [{"check": "common", "expect": 49, "pattern": "wrong_formula",
    "message": "You added the sides: 9 + 40 = 49. Square first: x = √(9² + 40²) = √(81 + 1600) = √1681 = 41."}],
 },
 {  # B8 REPAIRED (was diagonal 10, side 6 -> 8, duplicate of B4)
  "display": rect_diag("A rectangle with width 12 cm, a diagonal of 20 cm drawn corner to corner, and the length marked with a question mark", width="12 cm", length="? cm", diag="20 cm") + "A rectangle has diagonal 20 cm and width 12 cm. Find the length.",
  "solutions": [16], "calculator": False, "input_type": "single_value",
  "hint": "The diagonal is the hypotenuse, so subtract: square root of 20 squared minus 12 squared.",
  "guided_steps": [
    box("The diagonal is the hypotenuse: 20² = ", 400, "Twenty squared is 20 × 20."),
    box("12² = ", 144, "Twelve squared is 12 × 12."),
    box("Subtract: 400 − 144 = ", 256, "Bigger square minus smaller square."),
    box("√256 = ", 16, "What number times itself makes 256? Try 16.", phase="substitute"),
    box("Check: 16² + 12² = ", 400, "256 + 144.", done="400 = 20², so the length is 16 cm."),
  ],
  "misconceptions": [{"check": "common", "expect": 23.3, "pattern": "forgot_step",
    "message": "You added: √(20² + 12²) = √544 ≈ 23.3. The diagonal is the hypotenuse, so SUBTRACT: length = √(20² − 12²) = √(400 − 144) = √256 = 16 cm."}],
 },
]

silver = [
 {  # S1 inverse sin (abstract, no figure)
  "display": "\\(\\sin\\theta = 0.6\\). Find \\(\\theta\\) to 1 d.p.",
  "solutions": [36.9], "calculator": True, "input_type": "single_value",
  "hint": "Use the inverse sine button on 0.6.",
  "guided_steps": [
    say("sin θ = 0.6 is the ratio opposite ÷ hypotenuse. To get the angle back, use inverse sin."),
    box("sin⁻¹(0.6), to 2 d.p. = ", 36.87, "Press sin⁻¹, then 0.6."),
    box("Round to 1 d.p.: θ = ", 36.9, "One decimal place.", phase="substitute"),
    box("Check by going forward: sin36.9°, to 1 d.p. = ", 0.6, "Type sin(36.9) and round to 1 d.p.", done="0.6 matches, so θ = 36.9°."),
  ],
  "misconceptions": [{"check": "common", "expect": 53.1, "pattern": "wrong_formula",
    "message": "You used cos⁻¹: cos⁻¹(0.6) ≈ 53.1°. The ratio here is a sine, so use inverse sin: θ = sin⁻¹(0.6) ≈ 36.9°."}],
 },
 {  # S2 opp, angle 40, hyp 15
  "display": tri("Right-angled triangle with a 40 degree angle, hypotenuse 15 cm and the opposite side marked with a question mark", angle_label="40°", right="?", hyp="15 cm") + "Find the opposite side: angle \\(40^\\circ\\), hypotenuse 15 cm. Give to 1 d.p.",
  "solutions": [9.6], "calculator": True, "input_type": "single_value",
  "hint": "Opposite with hypotenuse points to sine: multiply 15 by sin40°.",
  "guided_steps": [
    box("sin40°, to 2 d.p. = ", 0.64, "Type sin(40) on the calculator."),
    box("O = 15 × sin40° = ", 9.6, "Multiply the hypotenuse by sin40°, keeping full accuracy.", phase="substitute"),
    box("Check: sin⁻¹(9.6 ÷ 15), to the nearest degree = ", 40, "Divide 9.6 by 15, then press sin⁻¹.", done="That returns the 40° angle, so the opposite is 9.6 cm."),
  ],
  "misconceptions": [{"check": "common", "expect": 11.5, "pattern": "wrong_ratio",
    "message": "You used cosine: 15 × cos40° ≈ 11.5. Opposite with hypotenuse means sine: O = 15 × sin40° ≈ 9.6 cm."}],
 },
 {  # S3 adj, angle 55, hyp 20
  "display": tri("Right-angled triangle with a 55 degree angle, hypotenuse 20 cm and the adjacent side marked with a question mark", angle_label="55°", bottom="?", hyp="20 cm") + "Find the adjacent side: angle \\(55^\\circ\\), hypotenuse 20 cm. Give to 1 d.p.",
  "solutions": [11.5], "calculator": True, "input_type": "single_value",
  "hint": "Adjacent with hypotenuse points to cosine: multiply 20 by cos55°.",
  "guided_steps": [
    box("cos55°, to 2 d.p. = ", 0.57, "Type cos(55) on the calculator."),
    box("A = 20 × cos55° = ", 11.5, "Multiply the hypotenuse by cos55°, keeping full accuracy.", phase="substitute"),
    box("Check: cos⁻¹(11.5 ÷ 20), to the nearest degree = ", 55, "Divide 11.5 by 20, then press cos⁻¹.", done="That returns the 55° angle, so the adjacent is 11.5 cm."),
  ],
  "misconceptions": [{"check": "common", "expect": 16.4, "pattern": "wrong_ratio",
    "message": "You used sine: 20 × sin55° ≈ 16.4. Adjacent with hypotenuse means cosine: A = 20 × cos55° ≈ 11.5 cm."}],
 },
 {  # S4 angle from opp 8 adj 15
  "display": tri("Right-angled triangle with opposite side 8 and adjacent side 15, angle theta marked at the corner", angle_label="θ", bottom="15", right="8") + "Find angle \\(\\theta\\): opposite 8, adjacent 15. Give to 1 d.p.",
  "solutions": [28.1], "calculator": True, "input_type": "single_value",
  "hint": "Opposite with adjacent points to tan: take inverse tan of 8 divided by 15.",
  "guided_steps": [
    box("Opposite ÷ adjacent: 8 ÷ 15, to 2 d.p. = ", 0.53, "Divide 8 by 15."),
    box("θ = tan⁻¹(8 ÷ 15) = ", 28.1, "Press tan⁻¹, then 8 ÷ 15; keep full accuracy.", phase="substitute"),
    box("Check: tan28.1°, to 2 d.p. = ", 0.53, "Type tan(28.1) and round to 2 d.p.", done="0.53 matches 8 ÷ 15, so θ = 28.1°."),
  ],
  "misconceptions": [{"check": "common", "expect": 61.9, "pattern": "inverted",
    "message": "You inverted the ratio: tan⁻¹(15 ÷ 8) ≈ 61.9°. Opposite over adjacent is 8 over 15, so θ = tan⁻¹(8 ÷ 15) ≈ 28.1°."}],
 },
 {  # S5 hyp, angle 30, opp 6
  "display": tri("Right-angled triangle with a 30 degree angle, opposite side 6 cm and the hypotenuse marked with a question mark", angle_label="30°", right="6 cm", hyp="?") + "Find the hypotenuse: angle \\(30^\\circ\\), opposite 6 cm.",
  "solutions": [12], "calculator": True, "input_type": "single_value",
  "hint": "Opposite and hypotenuse point to sine: divide 6 by sin30°.",
  "guided_steps": [
    say("You know the opposite and want the hypotenuse, so use sin: sin30° = opposite ÷ hypotenuse, which rearranges to H = opposite ÷ sin30°."),
    box("sin30° = ", 0.5, "Sine of 30 degrees is a half."),
    box("H = 6 ÷ 0.5 = ", 12, "Divide, do not multiply.", phase="substitute"),
    box("Check: H × sin30° = 12 × 0.5 = ", 6, "Twelve times a half.", done="That returns the opposite, 6, so the hypotenuse is 12 cm."),
  ],
  "misconceptions": [{"check": "common", "expect": 3, "pattern": "wrong_formula",
    "message": "You multiplied: 6 × sin30° = 3. To find the hypotenuse you DIVIDE: H = 6 ÷ sin30° = 6 ÷ 0.5 = 12 cm."}],
 },
 {  # S6 conceptual MCQ preserved
  "display": "Which ratio uses the Opposite and the Adjacent?",
  "options": ["\\(\\tan\\)", "\\(\\sin\\)", "\\(\\cos\\)", "Pythagoras"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Opposite over adjacent is the tangent ratio.",
  "misconceptions": [
    {"check": "sin", "expect": None, "pattern": "sin", "message": "sin uses Opposite ÷ Hypotenuse. tan uses Opposite ÷ Adjacent."},
    {"check": "cos", "expect": None, "pattern": "cos", "message": "cos uses Adjacent ÷ Hypotenuse. tan uses Opposite ÷ Adjacent."},
  ],
 },
 {  # S7 opp, angle 50, adj 10
  "display": tri("Right-angled triangle with a 50 degree angle, adjacent side 10 cm and the opposite side marked with a question mark", angle_label="50°", bottom="10 cm", right="?") + "Find the opposite side: angle \\(50^\\circ\\), adjacent 10 cm. Give to 1 d.p.",
  "solutions": [11.9], "calculator": True, "input_type": "single_value",
  "hint": "Opposite with adjacent points to tan: multiply 10 by tan50°.",
  "guided_steps": [
    box("tan50°, to 2 d.p. = ", 1.19, "Type tan(50) on the calculator."),
    box("O = 10 × tan50° = ", 11.9, "Multiply the adjacent by tan50°, keeping full accuracy.", phase="substitute"),
    box("Check: tan⁻¹(11.9 ÷ 10), to the nearest degree = ", 50, "Divide 11.9 by 10, then press tan⁻¹.", done="That returns the 50° angle, so the opposite is 11.9 cm."),
  ],
  "misconceptions": [{"check": "common", "expect": 7.7, "pattern": "wrong_ratio",
    "message": "You used sine: 10 × sin50° ≈ 7.7. Opposite with adjacent means tangent: O = 10 × tan50° ≈ 11.9 cm."}],
 },
]

gold = [
 {  # G1 ladder
  "display": tri("A ladder 5 m long as the hypotenuse of a right-angled triangle, its foot 1.5 m from the wall and the height up the wall marked with a question mark", bottom="1.5 m", right="? m", hyp="5 m") + "A ladder 5 m long leans against a wall. Its foot is 1.5 m from the wall. How high up the wall does it reach? (to 1 d.p.)",
  "solutions": [4.8], "calculator": True, "input_type": "single_value",
  "hint": "The ladder is the hypotenuse, so subtract: square root of 5 squared minus 1.5 squared.",
  "guided_steps": [
    box("5² = ", 25, "Five squared is 5 × 5."),
    box("1.5² = ", 2.25, "1.5 × 1.5."),
    box("The ladder is the hypotenuse, so subtract: 25 − 2.25 = ", 22.75, "Bigger square minus smaller square."),
    box("√22.75, to 1 d.p. = ", 4.8, "Square root of 22.75 on the calculator.", phase="substitute"),
    box("Check: 5² − 1.5² = ", 22.75, "Twenty-five minus 2.25.", done="√22.75 ≈ 4.8, so the ladder reaches 4.8 m up the wall."),
  ],
  "misconceptions": [{"check": "common", "expect": 5.2, "pattern": "forgot_step",
    "message": "You added: √(5² + 1.5²) = √27.25 ≈ 5.2. The ladder is the hypotenuse, so SUBTRACT: h = √(5² − 1.5²) = √22.75 ≈ 4.8 m."}],
 },
 {  # G2 isosceles
  "display": isosceles("Isosceles triangle with two equal sides of 10 cm, base 12 cm and a dashed height line marked with a question mark") + "An isosceles triangle has equal sides 10 cm and base 12 cm. Find its height. (to 1 d.p.)",
  "solutions": [8], "calculator": True, "input_type": "single_value",
  "hint": "Split it down the middle: the height, half the base (6) and a slant side (10) form a right triangle.",
  "guided_steps": [
    box("Half the base: 12 ÷ 2 = ", 6, "The height splits the base into two equal halves."),
    box("The slant side is the hypotenuse: 10² = ", 100, "Ten squared is 10 × 10."),
    box("6² = ", 36, "Six squared is 6 × 6."),
    box("Subtract: 100 − 36 = ", 64, "Bigger square minus smaller square."),
    box("√64 = ", 8, "What number times itself makes 64?", phase="substitute"),
    box("Check: 8² + 6² = ", 100, "64 + 36.", done="100 = 10², so the height is 8 cm."),
  ],
  "misconceptions": [{"check": "common", "expect": None, "pattern": "forgot_step", "note": "Using full base 12 gives sqrt(100-144), no real value: expect null.",
    "message": "Drop the height to the middle of the base first. That makes a right triangle with hypotenuse 10 and base 6 (half of 12): h = √(10² − 6²) = √64 = 8 cm. Using the full base of 12 has no real answer."}],
 },
 {  # G3 cliff depression
  "display": cliff("A 40 m vertical cliff with a dashed horizontal line from the top, an angle of depression of 25 degrees down to a boat, and the horizontal distance to the boat marked with a question mark") + "From the top of a 40 m cliff, the angle of depression to a boat is \\(25^\\circ\\). How far is the boat from the base of the cliff? (nearest m)",
  "solutions": [86], "calculator": True, "input_type": "single_value",
  "hint": "The height is opposite and the distance is adjacent, so distance = 40 ÷ tan25°.",
  "guided_steps": [
    say("The angle of depression from the top equals the angle of elevation at the boat, 25°. The height (40 m) is opposite that angle and the distance is adjacent, so tan25° = 40 ÷ distance, giving distance = 40 ÷ tan25°."),
    box("tan25°, to 3 d.p. = ", 0.466, "Type tan(25) on the calculator."),
    box("d = 40 ÷ tan25°, to the nearest metre = ", 86, "Divide 40 by tan25°, keeping full accuracy.", phase="substitute"),
    box("Check: 86 × tan25°, to the nearest metre = ", 40, "86 times tan25°, rounded.", done="That returns the 40 m height, so the boat is 86 m away."),
  ],
  "misconceptions": [{"check": "common", "expect": 19, "pattern": "wrong_formula",
    "message": "You multiplied: 40 × tan25° ≈ 19. The height is opposite and the distance is adjacent, and the height is known, so DIVIDE: d = 40 ÷ tan25° ≈ 86 m."}],
 },
 {  # G4 distance between coordinates
  "display": coordgrid("A coordinate grid with the points 1 comma 2 and 4 comma 6 joined by a line, the horizontal gap 3 and vertical gap 4 shown as dashed legs and the distance marked with a question mark") + "Find the distance between \\((1, 2)\\) and \\((4, 6)\\).",
  "solutions": [5], "calculator": True, "input_type": "single_value",
  "hint": "The horizontal and vertical gaps are the legs; the distance is their hypotenuse.",
  "guided_steps": [
    box("Horizontal gap: 4 − 1 = ", 3, "Subtract the x-coordinates."),
    box("Vertical gap: 6 − 2 = ", 4, "Subtract the y-coordinates."),
    box("Square and add: 3² + 4² = ", 25, "9 + 16."),
    box("√25 = ", 5, "What number times itself makes 25?", phase="substitute"),
    box("Check: 5² = ", 25, "Five squared.", done="25 = 3² + 4², so the distance is 5."),
  ],
  "misconceptions": [{"check": "common", "expect": 25, "pattern": "forgot_root",
    "message": "You stopped at d² = 25. Take the square root: d = √25 = 5."}],
 },
 {  # G5 ship bearing
  "display": ship_bearing("Right-angled triangle for a ship sailing 12 km east then 9 km north, with a North arrow at the start and the return path as the hypotenuse") + "A ship sails 12 km east then 9 km north. What bearing must it take to return directly to the start? (nearest degree)",
  "solutions": [233], "calculator": True, "input_type": "single_value",
  "hint": "Find the acute angle from tan⁻¹(12 ÷ 9), then add 180° for the south-west return bearing.",
  "guided_steps": [
    say("The trip out went 12 km east then 9 km north. To return, the ship heads back into the south-west. At the finish, the angle between due south and the path back has tan = 12 (west) ÷ 9 (south)."),
    box("12 ÷ 9, to 2 d.p. = ", 1.33, "Divide 12 by 9."),
    box("That angle, tan⁻¹(12 ÷ 9), to the nearest degree = ", 53, "Press tan⁻¹, then 12 ÷ 9."),
    box("Bearings run clockwise from north; the south-west return is 180 + 53 = ", 233, "Add 180 to the angle past south.", phase="substitute"),
    box("Check: a return bearing is 180° from the outward one, so 233 − 180 = ", 53, "233 minus 180.", done="53 is the outward bearing (N53°E), confirming the return is 233°."),
  ],
  "misconceptions": [{"check": "common", "expect": 53, "pattern": "wrong_bearing",
    "message": "053° is the outward bearing, the way the ship first travelled. The return is the opposite direction: add 180° to get 053 + 180 = 233°."}],
 },
]

problem_bank = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": "Find the hypotenuse or a shorter side using Pythagoras.",
  "silver_description": "Use SOHCAHTOA to find sides and angles.",
  "gold_description": "Turn a worded or real situation into a right-angled triangle, then finish with Pythagoras or trigonometry.",
}

# ---------------- GUIDED (opener + teach) ----------------
guided = {
 "opener": {
   "label": "Before any formula",
   "display": opener_svg(),
   "steps": [
     box("The two smaller squares hold 9 tiles and 16 tiles. Together that is 9 + 16 = ", 25,
         "Add the two tile counts.",
         say="Here is a right-angled triangle with a square of tiles built on each side. No formula yet, just count and add."),
     box("A square built from 25 tiles has how many tiles along each edge? ", 5,
         "What number times itself makes 25?",
         say="The neat part: the square on the longest side holds exactly that many tiles, 25. That is Pythagoras, the two smaller squares add up to the biggest."),
     say("So the longest side is 5. Writing the short sides as \\(a\\) and \\(b\\) and the longest as \\(c\\), every right triangle obeys \\(a^2 + b^2 = c^2\\). Squaring a side counts the tiles in its square; square rooting turns the tile count back into a length."),
   ],
 },
 "teach": {
   "bronze": {
     "label": "Together: your first one",
     "display": "Find the hypotenuse of a right triangle with shorter sides 9 cm and 12 cm.",
     "steps": [
       say("The two shorter sides are 9 and 12. Pythagoras says: square each, add, then square root."),
       box("9² = ", 81, "9 × 9."),
       box("12² = ", 144, "12 × 12."),
       box("Add the squares: 81 + 144 = ", 225, "Just add them."),
       box("Square root to get the hypotenuse: √225 = ", 15, "What number times itself makes 225? Try 15.", done="Square, add, root. That is the whole method."),
       box("Check: 15² = ", 225, "15 × 15.", done="225 = 81 + 144, so the hypotenuse is 15 cm."),
     ],
   },
   "silver": {
     "label": "Together: the silver move",
     "display": "In a right triangle the opposite side is 5 cm and the adjacent side is 12 cm. Find the angle \\(\\theta\\) to 1 d.p.",
     "steps": [
       say("You know the opposite and the adjacent, so the ratio is tan. To get the angle back, use inverse tan, the new move at this level."),
       box("The ratio, opposite ÷ adjacent: 5 ÷ 12, to 2 d.p. = ", 0.42, "Divide 5 by 12."),
       box("Inverse tan turns that ratio into the angle: θ = tan⁻¹(5 ÷ 12) = ", 22.6, "Press tan⁻¹, then 5 ÷ 12; keep full accuracy.", done="Inverse tan undoes tan to reveal the angle. That was the point."),
       box("The two acute angles add to 90°, so the other one is 90 − 22.6 = ", 67.4, "Ninety minus 22.6."),
       box("Check: tan22.6°, to 2 d.p. = ", 0.42, "Type tan(22.6) and round to 2 d.p.", done="0.42 matches 5 ÷ 12, so θ = 22.6°."),
     ],
   },
   "gold": {
     "label": "Together: the gold move",
     "display": "A slide drops 2 m over a horizontal run of 5 m. Find the angle it makes with the ground, to 1 d.p.",
     "steps": [
       say("Draw the triangle from the words: the drop, 2 m, is opposite the angle; the run, 5 m, is adjacent. Opposite and adjacent means tan."),
       box("The ratio, drop ÷ run: 2 ÷ 5 = ", 0.4, "Divide 2 by 5."),
       box("Inverse tan gives the angle: θ = tan⁻¹(2 ÷ 5) = ", 21.8, "Press tan⁻¹, then 2 ÷ 5.", done="Reading the triangle out of the words is the gold move."),
       box("The slide itself is the hypotenuse: √(2² + 5²) = √29, to 1 d.p. = ", 5.4, "Square root of 29 on the calculator."),
       box("Check: tan21.8°, to 2 d.p. = ", 0.4, "Type tan(21.8) and round to 2 d.p.", done="0.4 matches the ratio, so the slide sits at 21.8°."),
     ],
   },
 },
}

# ---------------- tier_guides ----------------
tier_guides = {
 "bronze": {
   "title": "Bronze: one formula, straight in",
   "steps": [
     "Read the two known values straight off the triangle. No rearranging needed yet.",
     "For Pythagoras: square both sides, then add for the hypotenuse, or subtract then square root for a shorter side.",
     "For a trig side with a given ratio like \\(\\sin 30° = 0.5\\), multiply the hypotenuse by it; for an angle, use \\(\\tan^{-1}\\) on the ratio.",
   ],
   "example": {
     "question": "Find the hypotenuse: sides 6 cm and 8 cm.",
     "steps": [
       {"label": "Square and add", "content": "<p>\\(6^2 + 8^2 = 36 + 64 = 100\\)</p>"},
       {"label": "Square root", "content": "<p>\\(c = \\sqrt{100} = 10\\)</p>"},
       {"label": "Check", "content": "<p>\\(6^2 + 8^2 = 100 = 10^2\\) ✓</p>"},
       {"label": "Answer", "content": "<p>\\(c = 10\\) cm</p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "silver": {
   "title": "Silver: choose and rearrange",
   "steps": [
     "Nothing is ready to use. First decide: Pythagoras (three sides, no angle) or a trig ratio (an angle is involved).",
     "Pick the ratio that pairs your two sides: \\(\\sin\\) for O and H, \\(\\cos\\) for A and H, \\(\\tan\\) for O and A, then rearrange for the unknown.",
     "Real shapes count: split an isosceles triangle down the middle, or read a rectangle's diagonal as a hypotenuse.",
   ],
   "example": {
     "question": "Find the opposite side when \\(\\theta = 30°\\) and the hypotenuse is 14 cm.",
     "steps": [
       {"label": "Choose ratio", "content": "<p>Opposite and hypotenuse, so \\(\\sin\\theta = \\frac{O}{H}\\), giving \\(O = H\\sin\\theta\\).</p>"},
       {"label": "Substitute", "content": "<p>\\(O = 14 \\times \\sin 30° = 14 \\times 0.5 = 7\\)</p>"},
       {"label": "Check", "content": "<p>\\(7 \\div 14 = 0.5 = \\sin 30°\\) ✓</p>"},
       {"label": "Answer", "content": "<p>\\(O = 7\\) cm</p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "gold": {
   "title": "Gold: build the triangle from the words",
   "steps": [
     "The right triangle is hidden in a story or a shape. Sketch it and label the sides you are given.",
     "Journeys and bearings give two legs, so find the hypotenuse. Elevation and depression give an angle with a height and a distance, so use \\(\\tan\\).",
     "For coordinates, the horizontal and vertical gaps are the two legs and the distance between the points is the hypotenuse.",
   ],
   "example": {
     "question": "A ship sails 9 km east then 12 km north. How far is it from the start?",
     "steps": [
       {"label": "Set up", "content": "<p>The two legs are 9 and 12; the direct distance is the hypotenuse.</p>"},
       {"label": "Pythagoras", "content": "<p>\\(9^2 + 12^2 = 81 + 144 = 225\\)</p>"},
       {"label": "Check", "content": "<p>\\(\\sqrt{225} = 15\\), and \\(15^2 = 225\\) ✓</p>"},
       {"label": "Answer", "content": "<p>\\(15\\) km</p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
}

# ---------------- method_card (slim) ----------------
method_card = {
  "title": "How to Use Pythagoras & SOHCAHTOA",
  "steps": [
    "Label the sides: hypotenuse (longest, opposite the right angle), then opposite and adjacent relative to the angle.",
    "Two sides and no angle: use Pythagoras. An angle is involved: use SOHCAHTOA.",
    "Substitute into the formula and solve: square root for Pythagoras, or an inverse trig button for an angle.",
  ],
  "content": "<p><strong>Pythagoras:</strong> in a right-angled triangle \\(a^2 + b^2 = c^2\\), where \\(c\\) is the hypotenuse. To find the hypotenuse, \\(c = \\sqrt{a^2 + b^2}\\); to find a shorter side, subtract: \\(a = \\sqrt{c^2 - b^2}\\).</p><p><strong>SOHCAHTOA:</strong> \\(\\sin\\theta = \\frac{O}{H}\\), \\(\\cos\\theta = \\frac{A}{H}\\), \\(\\tan\\theta = \\frac{O}{A}\\). To find a side, rearrange; to find an angle, use \\(\\sin^{-1}\\), \\(\\cos^{-1}\\) or \\(\\tan^{-1}\\). Keep the calculator in degrees.</p>",
  "example": "<p><strong>Find the hypotenuse of a right triangle with sides 5 cm and 12 cm.</strong></p><p>\\(c = \\sqrt{5^2 + 12^2} = \\sqrt{25 + 144} = \\sqrt{169} = 13\\) cm</p>",
}

# ---------------- preserved fields (from live/pre-dump) ----------------
live = json.load(io.open("_geoL05_live.json", encoding="utf-8"))["practice_data"]
topic_links = live["topic_links"]
related_videos = live["related_videos"]
worked_examples = live["worked_examples"]
# Style repair: preserved worked_examples labels use em dashes (banned, student-facing).
# Replace " — " with ": " minimally; content unchanged otherwise.
for we in worked_examples:
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

pd = {
  "guided": guided,
  "method_card": method_card,
  "tier_guides": tier_guides,
  "topic_links": topic_links,
  "problem_bank": problem_bank,
  "related_videos": related_videos,
  "worked_examples": worked_examples,
}

out = "lesson_maths-eduqas_geometry-L05.json"
json.dump(pd, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out)

# ---------------- self-verify every box & solution ----------------
def rd(x, n): return round(x, n)
errs = []
def ck(name, got, want):
    if abs(got - want) > 0.05:
        errs.append("%s: computed %s but wrote %s" % (name, got, want))

deg = math.radians
# bronze
ck("B1 hyp", math.hypot(3,4), 5); ck("B2 hyp", math.hypot(8,15), 17)
ck("B3", math.sqrt(13**2-5**2), 12); ck("B4", math.sqrt(10**2-6**2), 8)
ck("B5 hyp", math.hypot(7,24), 25); ck("B7 hyp", math.hypot(9,40), 41)
ck("B8", math.sqrt(20**2-12**2), 16)
ck("B3 expect", math.hypot(13,5), 13.9); ck("B4 expect", math.hypot(10,6), 11.7)
ck("B8 expect", math.hypot(20,12), 23.3)
# silver
ck("S1", math.degrees(math.asin(0.6)), 36.9); ck("S1 2dp", math.degrees(math.asin(0.6)), 36.87)
ck("S1 expect", math.degrees(math.acos(0.6)), 53.1)
ck("S2 sin40", math.sin(deg(40)), 0.64); ck("S2", 15*math.sin(deg(40)), 9.6); ck("S2 exp", 15*math.cos(deg(40)), 11.5)
ck("S3 cos55", math.cos(deg(55)), 0.57); ck("S3", 20*math.cos(deg(55)), 11.5); ck("S3 exp", 20*math.sin(deg(55)), 16.4)
ck("S4 ratio", 8/15, 0.53); ck("S4", math.degrees(math.atan(8/15)), 28.1); ck("S4 tan28.1", math.tan(deg(28.1)), 0.53); ck("S4 exp", math.degrees(math.atan(15/8)), 61.9)
ck("S5", 6/math.sin(deg(30)), 12); ck("S5 exp", 6*math.sin(deg(30)), 3)
ck("S7 tan50", math.tan(deg(50)), 1.19); ck("S7", 10*math.tan(deg(50)), 11.9); ck("S7 exp", 10*math.sin(deg(50)), 7.7)
# gold
ck("G1", math.sqrt(25-2.25), 4.8); ck("G1 sub", 25-2.25, 22.75); ck("G1 exp", math.sqrt(25+2.25), 5.2)
ck("G2", math.sqrt(100-36), 8)
ck("G3 tan25", math.tan(deg(25)), 0.466); ck("G3", 40/math.tan(deg(25)), 86); ck("G3 chk", 86*math.tan(deg(25)), 40); ck("G3 exp", 40*math.tan(deg(25)), 19)
ck("G4", math.hypot(3,4), 5)
ck("G5 ratio", 12/9, 1.33); ck("G5 ang", math.degrees(math.atan(12/9)), 53); ck("G5", 180+53, 233)
# teach
ck("T-bronze", math.hypot(9,12), 15)
ck("T-silver ratio", 5/12, 0.42); ck("T-silver", math.degrees(math.atan(5/12)), 22.6); ck("T-silver other", 90-22.6, 67.4)
ck("T-gold ratio", 2/5, 0.4); ck("T-gold", math.degrees(math.atan(2/5)), 21.8); ck("T-gold hyp", math.sqrt(4+25), 5.4)
# opener
ck("opener add", 9+16, 25); ck("opener edge", math.sqrt(25), 5)

if errs:
    print("VERIFY ERRORS:")
    for e in errs: print("  -", e)
else:
    print("VERIFY: all", "boxes/solutions/expects recompute correctly")
