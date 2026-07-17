# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams build for maths-ocr graphs-L03 (Quadratic Graphs).
Every box answer is COMPUTED, not transcribed, so the walk is guaranteed continuous."""
import json, io

MINUS = "−"   # unicode minus (not em dash)
ARROW = "→"

live = json.load(io.open("_glive_graphsL03.json", encoding="utf-8"))
pb = live["problem_bank"]

# ---------- helpers to build guided_steps ----------
def box(pre, ans, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(s):
    return {"say": s}

# ---------- OPENER (fountain water arc) ----------
# f(x) = -3/16 * x*(x-8): roots x=0,8 ; peak (4,3)
def fountain_svg():
    XLO, XHI = 0, 8
    px0, px1 = 40.0, 235.0
    def mx(x): return px0 + (x - XLO) / (XHI - XLO) * (px1 - px0)
    YLO, YHI = 0, 4
    py0, py1 = 165.0, 25.0
    def my(y): return py0 + (y - YLO) / (YHI - YLO) * (py1 - py0)
    parts = ['<svg viewBox="0 0 260 200" role="img" aria-label="Curve of water height in metres against sideways distance in metres: it rises from 0 at distance 0 to a peak of 3 metres at distance 4 metres, then falls back to 0 at distance 8 metres" style="max-width:260px" font-family="Inter, sans-serif">']
    parts.append('<line x1="40" y1="20" x2="40" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    parts.append('<line x1="40" y1="165" x2="238" y2="165" stroke="currentColor" stroke-width="1.2"/>')
    for yv in range(0, 5):
        yy = my(yv)
        parts.append('<line x1="37" y1="%.1f" x2="40" y2="%.1f" stroke="currentColor" stroke-width="1"/>' % (yy, yy))
        parts.append('<text x="33" y="%.1f" font-size="9" fill="currentColor" text-anchor="end">%d</text>' % (yy + 3, yv))
    for xv in range(0, 9, 2):
        xx = mx(xv)
        parts.append('<line x1="%.1f" y1="165" x2="%.1f" y2="168" stroke="currentColor" stroke-width="1"/>' % (xx, xx))
        parts.append('<text x="%.1f" y="179" font-size="9" fill="currentColor" text-anchor="middle">%d</text>' % (xx, xv))
    pts = []
    x = 0.0
    while x <= 8.0001:
        y = -3.0/16.0 * x * (x - 8)
        pts.append("%.1f,%.1f" % (mx(x), my(y)))
        x += 0.5
    parts.append('<polyline points="%s" fill="none" stroke="#3b82f6" stroke-width="2"/>' % " ".join(pts))
    parts.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#3b82f6"/>' % (mx(4), my(3)))
    parts.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#3b82f6"/>' % (mx(0), my(0)))
    parts.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#3b82f6"/>' % (mx(8), my(0)))
    parts.append('<text x="%.1f" y="%.1f" font-size="9" fill="currentColor" text-anchor="middle">peak</text>' % (mx(4), my(3) - 5))
    parts.append('<text x="139" y="193" font-size="10" fill="currentColor" text-anchor="middle">distance (m)</text>')
    parts.append('<text x="12" y="92" font-size="10" fill="currentColor" text-anchor="middle" transform="rotate(-90 12 92)">height (m)</text>')
    parts.append('</svg>')
    return "".join(parts)

opener = {
    "label": "Before any algebra",
    "display": fountain_svg() + "<p>A garden sprinkler shoots water in an arch. The graph shows the water's height (in metres) against how far it has travelled sideways (in metres), until it lands.</p>",
    "steps": [
        box("What is the greatest height the water reaches? ", 3,
            "Read the height at the very top of the arch.", post=" m"),
        box("How far from the sprinkler does the water land (back to height 0)? ", 8,
            "Read the distance where the curve returns to height 0.", post=" m"),
        sayonly("The top you read, (4, 3), is the <strong>turning point</strong>, the highest point of the arch. The two ground points, distance 0 and distance 8, are the <strong>roots</strong> where height is 0, and the arch is symmetric about the peak. Every quadratic graph \\(y = ax^2 + bx + c\\) has this same arch (or valley) shape: a turning point, and up to two roots.")
    ]
}

# ---------- TEACH walks ----------
teach = {}
# bronze: read basic features of y = x^2 - 4
teach["bronze"] = {
    "display": "Look at \\(y = x^2 - 4\\).",
    "label": "Together: reading a simple parabola",
    "steps": [
        box("Find y when x = 3. First square x: 3² = ", 3*3,
            "Multiply 3 by itself."),
        box("Now subtract 4: 9 " + MINUS + " 4 = ", 3*3-4,
            "Take 4 away from your squared value."),
        box("The y-intercept is where x = 0: 0² " + MINUS + " 4 = ", 0-4,
            "Put x = 0 in; only the constant is left.", phase="substitute"),
        box("A root is where y = 0, so x² = 4. The positive root is x = ", 2,
            "What positive number squares to 4?"),
        box("Check that root: 2² " + MINUS + " 4 = ", 0,
            "Square 2, then subtract 4.",
            done="It gives 0, so x = 2 is genuinely a root of the curve.")
    ]
}
# silver: full features of y = x^2 - 6x + 8 (a=1)
teach["silver"] = {
    "display": "Look at \\(y = x^2 - 6x + 8\\).",
    "label": "Together: roots and turning point",
    "steps": [
        box("Factorise to (x " + MINUS + " 2)(x " + MINUS + " 4). The smaller root is x = ", 2,
            "Set each bracket to 0: x = 2 or x = 4."),
        box("The larger root is x = ", 4,
            "The other bracket, x " + MINUS + " 4 = 0."),
        box("The turning point x is the midpoint of the roots: (2 + 4) ÷ 2 = ", (2+4)//2,
            "Average the two roots.", phase="substitute"),
        box("Substitute x = 3 for the y-coordinate: 3² " + MINUS + " 6×3 + 8 = ", 3*3-6*3+8,
            "Work out 9, then " + MINUS + "18, then +8."),
        box("Check the y-intercept: set x = 0 to get ", 8,
            "The constant term is the y-intercept.",
            done="Opens upward, vertex (3, " + MINUS + "1), crosses the y-axis at 8: all consistent.")
    ]
}
# gold: a != 1, y = 2x^2 - 12x + 10
teach["gold"] = {
    "display": "Look at \\(y = 2x^2 - 12x + 10\\).",
    "label": "Together: when the x² coefficient is not 1",
    "steps": [
        box("Here a = 2, b = " + MINUS + "12. Work out 2a = 2×2 = ", 4,
            "Double the value of a."),
        box("Turning point x = " + MINUS + "b ÷ (2a) = 12 ÷ 4 = ", 12//4,
            "Divide " + MINUS + "b by 2a.", phase="substitute"),
        box("Substitute x = 3 for y: 2×3² " + MINUS + " 12×3 + 10 = 18 " + MINUS + " 36 + 10 = ", 2*9-12*3+10,
            "Work each term, then add."),
        box("Divide the equation by 2 to factorise: x² " + MINUS + " 6x + 5 = (x " + MINUS + " 1)(x " + MINUS + " 5). Smaller root x = ", 1,
            "Set the first bracket to 0."),
        box("Check: put x = 1 in the original: 2×1 " + MINUS + " 12 + 10 = ", 2*1-12+10,
            "Work out 2, then " + MINUS + "12, then +10.",
            done="It gives 0, so x = 1 is a root; the vertex (3, " + MINUS + "8) sits below the axis.")
    ]
}

# ---------- CHART builder ----------
def make_chart(f, xlo, xhi, ymin, ymax, ystep=2):
    data = []
    x = xlo
    while x <= xhi + 1e-9:
        data.append({"x": round(x, 2), "y": round(f(x), 2)})
        x += 0.5
    return {
        "type": "scatter",
        "data": {"datasets": [{
            "type": "line", "data": data, "tension": 0.35, "fill": False,
            "borderColor": "#3b82f6", "pointRadius": 0, "pointBackgroundColor": "#3b82f6"}]},
        "options": {"scales": {
            "x": {"min": xlo - 0.5, "max": xhi + 0.5, "ticks": {"stepSize": 1},
                  "grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": "x", "display": True}},
            "y": {"min": ymin, "max": ymax, "ticks": {"stepSize": ystep},
                  "grid": {"color": "rgba(0,0,0,0.08)"}, "title": {"text": "y", "display": True}}}}}

# ---------- per-problem guided_steps + hints + misconceptions ----------
def mc(pattern, message, expect):
    return {"pattern": pattern, "message": message, "expect": expect}

# BRONZE
b = pb["bronze"]

# b0 eval x^2+3 at x=2 -> 7
b[0]["hint"] = "Square x first, then add the constant."
b[0]["misconceptions"] = [mc("forgot_constant",
    "You found x² = 4 but stopped there. Add the constant: 4 + 3 = 7.", 4)]
b[0]["guided_steps"] = [
    box("Substitute x = 2. First the x² part: 2² = ", 2*2, "Multiply 2 by itself."),
    box("Now add the constant: 4 + 3 = ", 2*2+3, "Add 3 to your squared value.", phase="substitute"),
    box("Check the point (2, 7): 2² + 3 = ", 2*2+3, "Redo the substitution to be sure.",
        done="It gives 7 again, so y = 7.")]

# b1 eval x^2-1 at x=-3 -> 8
b[1]["hint"] = "A negative squared is positive, then subtract 1."
b[1]["misconceptions"] = [mc("neg_square_sign",
    "A negative number squared is positive: (−3)² = 9, not −9. So y = 9 " + MINUS + " 1 = 8.", -10)]
b[1]["guided_steps"] = [
    box("Substitute x = −3. First (−3)² = ", (-3)*(-3), "A negative times a negative is positive."),
    box("Now subtract 1: 9 " + MINUS + " 1 = ", (-3)*(-3)-1, "Take 1 away.", phase="substitute"),
    box("Check: (−3)² " + MINUS + " 1 = ", (-3)*(-3)-1, "Redo it to confirm.",
        done="It gives 8, so y = 8.")]

# b2 min of y=x^2, give y -> 0  (chart of y=x^2)
b[2]["hint"] = "The lowest point of y = x² sits at the origin."
b[2]["misconceptions"] = []
b[2]["guided_steps"] = [
    box("Test x = 2: 2² = ", 2*2, "Square 2."),
    box("Test x = −2: (−2)² = ", (-2)*(-2), "Square −2; a negative squared is positive."),
    box("Equal heights either side, so the lowest point is halfway, at x = 0. Its height: 0² = ", 0,
        "Square 0.", say="Both sides give 4, so the bottom of the valley is between them, at x = 0.",
        phase="substitute"),
    box("Anything squared is 0 or more, so nothing is lower. The minimum y-value is ", 0,
        "Read the height at the bottom point.",
        done="The vertex is (0, 0), so the y-value is 0.")]
b[2]["chart"] = make_chart(lambda x: x*x, -3, 3, -1, 10, 2)

# b3 roots x^2-4 positive root -> 2
b[3]["hint"] = "Set y = 0, so x² = 4, then square root."
b[3]["misconceptions"] = [mc("forgot_sqrt",
    "x² = 4 means x = √4 = 2, not 4. The 4 is x², not x.", 4)]
b[3]["guided_steps"] = [
    box("Roots are where y = 0. Set x² " + MINUS + " 4 = 0, so x² = ", 4, "Move the 4 across."),
    box("Take the square root: √4 = ", 2, "What positive number squares to 4?", phase="substitute"),
    box("Check: 2² " + MINUS + " 4 = ", 2*2-4, "Square 2, then subtract 4.",
        done="It gives 0, so x = 2 is a root.")]

# b4 eval x^2+2x at x=3 -> 15
b[4]["hint"] = "Square x for the x² term, work out 2x, then add."
b[4]["misconceptions"] = [mc("forgot_square",
    "x² means 3² = 9, not 3. So y = 9 + 6 = 15.", 9)]
b[4]["guided_steps"] = [
    box("Substitute x = 3. The x² term: 3² = ", 3*3, "Square 3."),
    box("The 2x term: 2 × 3 = ", 2*3, "Multiply 2 by x."),
    box("Add them: 9 + 6 = ", 3*3+2*3, "Add the two parts.", phase="substitute"),
    box("Check: 3² + 2×3 = ", 3*3+2*3, "Redo the substitution.",
        done="It gives 15, so y = 15.")]

# b5 y-intercept of x^2-3x+6 -> 6  (CHANGED from +7 to de-dup with b0)
b[5]["display"] = "What is the y-intercept of \\(y = x^2 - 3x + 6\\)?"
b[5]["solutions"] = [6]
b[5]["hint"] = "The y-intercept is the constant term, found by setting x = 0."
b[5]["misconceptions"] = [mc("read_x_coeff",
    "The y-intercept is the constant term (where x = 0), which is 6, not the −3x coefficient.", -3)]
b[5]["guided_steps"] = [
    box("The y-intercept is where x = 0. The x² term: 0² = ", 0, "Square 0."),
    box("The x term: −3 × 0 = ", 0, "Multiply −3 by 0."),
    box("So only the constant is left: y = ", 6, "Everything with an x vanished.", phase="substitute"),
    box("Read it off the equation: the number with no x is ", 6, "Spot the constant term.",
        done="The curve crosses the y-axis at (0, 6).")]

# b6 direction of -x^2+4, enter 1 max 0 min -> 1  (chart)
b[6]["hint"] = "Look only at the sign of the x² term to decide up or down."
b[6]["misconceptions"] = [mc("read_constant",
    "The direction depends on the x² coefficient (−1, negative), not the +4. Negative opens downward: a maximum.", 0)]
b[6]["guided_steps"] = [
    box("Test the shape. At x = 0: −(0²) + 4 = ", -(0)+4, "Square 0, negate, add 4."),
    box("At x = 2: −(2²) + 4 = ", -(2*2)+4, "Square 2, make it negative, add 4."),
    box("Lower on both sides of the top, so it opens downward: a maximum. Enter 1 for maximum: ", 1,
        "Downward parabolas have a highest point.",
        say="At x = 0 it is 4, but at x = 2 it has dropped to 0, so the top is the peak.",
        phase="substitute"),
    box("Confirm from the x² sign: the coefficient is −1, negative, which always opens down. Enter 1: ", 1,
        "Negative x² coefficient means maximum.",
        done="Both checks agree: it is a maximum, answer 1.")]
b[6]["chart"] = make_chart(lambda x: -(x*x)+4, -3, 3, -6, 5, 2)

# b7 roots x^2-9 positive root -> 3
b[7]["hint"] = "Set y = 0, so x² = 9, then square root."
b[7]["misconceptions"] = [mc("forgot_sqrt",
    "x² = 9 gives x = √9 = 3, not 9. The 9 is x², not x.", 9)]
b[7]["guided_steps"] = [
    box("Set y = 0: x² " + MINUS + " 9 = 0, so x² = ", 9, "Move the 9 across."),
    box("Take the square root: √9 = ", 3, "What positive number squares to 9?", phase="substitute"),
    box("Check: 3² " + MINUS + " 9 = ", 3*3-9, "Square 3, then subtract 9.",
        done="It gives 0, so x = 3 is a root.")]

# SILVER
s = pb["silver"]

# s0 roots x^2-7x+12 smaller -> 3
s[0]["hint"] = "Find two numbers multiplying to 12 and adding to −7, then take the smaller root."
s[0]["misconceptions"] = [mc("sign_slip",
    "Signs: (x " + MINUS + " 3)(x " + MINUS + " 4) gives roots +3 and +4, since (−3)×(−4) = 12 and −3 " + MINUS + " 4 = −7. The smaller is 3.", -4)]
s[0]["guided_steps"] = [
    box("Two numbers multiply to 12 and add to −7. Their product is ", 12, "Read the constant term."),
    box("Those numbers are −3 and −4, so (x " + MINUS + " 3)(x " + MINUS + " 4) = 0. One root: x = ", 3,
        "Set the first bracket to 0.", say="Check: (−3)×(−4) = 12 and −3 + (−4) = −7. Correct.",
        phase="substitute"),
    box("The other root: x = ", 4, "Set the second bracket to 0."),
    box("The smaller of 3 and 4 is ", 3, "Pick the lower value.",
        done="Check: 3² " + MINUS + " 7×3 + 12 = 9 " + MINUS + " 21 + 12 = 0, so 3 is a root.")]

# s1 tp_x x^2-4x+1 -> 2
s[1]["hint"] = "Use x = −b/(2a) with a = 1 and b = −4."
s[1]["misconceptions"] = [mc("sign_slip_b",
    "Use x = −b/(2a). Here b = −4, so −b = +4 and x = 4/2 = 2. Dropping the double negative gives −2.", -2)]
s[1]["guided_steps"] = [
    box("Read a and b: a = 1, b = −4. Work out 2a = 2 × 1 = ", 2, "Double a."),
    box("Now −b = −(−4) = ", 4, "The opposite of −4 is +4.", phase="substitute"),
    box("Divide: 4 ÷ 2 = ", 2, "Divide −b by 2a."),
    box("Check by symmetry: y at x = 1 is 1 " + MINUS + " 4 + 1 = −2; y at x = 3 is 9 " + MINUS + " 12 + 1 = −2. Equal, so the middle x is ", 2,
        "The turning point is halfway between equal heights.",
        done="Both sides match at x = 2, confirming the turning point x-coordinate.")]

# s2 tp_y x^2-4x+1 -> -3
s[2]["hint"] = "Find the turning point x first, then substitute to get y."
s[2]["misconceptions"] = [mc("used_constant",
    "The y-intercept is 1, but the turning point y is found by substituting x = 2: 4 " + MINUS + " 8 + 1 = −3.", 1)]
s[2]["guided_steps"] = [
    box("Turning point x = −b/(2a) = 4/2 = ", 2, "Work out −b over 2a first."),
    box("Substitute x = 2. The x² term: 2² = ", 2*2, "Square 2.", phase="substitute"),
    box("The −4x term: −4 × 2 = ", -4*2, "Multiply −4 by 2."),
    box("Add with the +1: 4 + (−8) + 1 = ", 2*2-4*2+1, "Combine the three parts."),
    box("Shape check: a = 1 > 0, so this is the lowest point, y = ", 2*2-4*2+1,
        "The minimum value is the turning point y.",
        done="The vertex is (2, −3), so the y-coordinate is −3.")]

# s3 y-intercept 3x^2-2x+5 -> 5
s[3]["hint"] = "The y-intercept is the constant term (set x = 0)."
s[3]["misconceptions"] = [mc("read_x_coeff",
    "The y-intercept is the constant 5 (at x = 0), not the −2x coefficient.", -2)]
s[3]["guided_steps"] = [
    box("Set x = 0. The 3x² term: 3 × 0² = ", 0, "Square 0, then times 3."),
    box("The −2x term: −2 × 0 = ", 0, "Multiply −2 by 0."),
    box("Only the constant remains: y = ", 5, "Everything with an x vanished.", phase="substitute"),
    box("Read it off: the number with no x is ", 5, "Spot the constant term.",
        done="The curve crosses the y-axis at (0, 5).")]

# s4 sum roots x^2+6x+8 -> -6
s[4]["hint"] = "The sum of the roots is −b/a."
s[4]["misconceptions"] = [mc("sign_slip",
    "Sum of roots = −b/a = −6/1 = −6. Using +b gives +6, the wrong sign. The roots −2 and −4 sum to −6.", 6)]
s[4]["guided_steps"] = [
    box("Factorise: x² + 6x + 8 = (x + 2)(x + 4). One root: x = ", -2, "Set x + 2 = 0."),
    box("The other root: x = ", -4, "Set x + 4 = 0.", phase="substitute"),
    box("Add them: −2 + (−4) = ", -2+-4, "Add the two roots."),
    box("Check with the formula −b/a = −6/1 = ", -6, "Compare with −b over a.",
        done="Both methods give −6, so the sum of the roots is −6.")]

# s5 max value -x^2+2x+3 -> 4 (chart)
s[5]["hint"] = "Find the turning point x, then work out the y-value there."
s[5]["misconceptions"] = [mc("gave_x",
    "x = 1 is where the maximum occurs, but the maximum VALUE is the y there: −1 + 2 + 3 = 4.", 1)]
s[5]["guided_steps"] = [
    box("Turning point x = −b/(2a) = −2/(−2) = ", 1, "Divide −b by 2a; a = −1, b = 2."),
    box("Substitute x = 1. The −x² term: −(1²) = ", -(1), "Square 1, then make it negative.", phase="substitute"),
    box("The +2x term: 2 × 1 = ", 2*1, "Multiply 2 by 1."),
    box("Add with +3: −1 + 2 + 3 = ", -(1)+2*1+3, "Combine the three parts."),
    box("Shape check: a = −1 < 0, so it opens down and this is the highest point. Max y = ", -(1)+2*1+3,
        "The maximum value is the turning point y.",
        done="The vertex is (1, 4), so the maximum value of y is 4.")]
s[5]["chart"] = make_chart(lambda x: -(x*x)+2*x+3, -3, 5, -6, 5, 2)

# s6 how many roots x^2+4 -> 0 (chart)
s[6]["hint"] = "Find the lowest point; if it is above the x-axis there are no roots."
s[6]["misconceptions"] = [mc("assume_two",
    "Not every parabola crosses the x-axis. x² + 4 has its lowest point at y = 4, above the axis, so it has 0 roots.", 2)]
s[6]["guided_steps"] = [
    box("Roots are where y = 0. The smallest x² can be is at x = 0: 0² = ", 0, "Square 0."),
    box("Then the lowest y is 0 + 4 = ", 4, "Add 4 to the smallest x².", phase="substitute"),
    box("The bottom of the curve is y = 4, above the x-axis, so it never reaches 0. Number of crossings: ", 0,
        "How many times does it touch or cross the x-axis?",
        say="Since the whole curve sits at height 4 or more, it cannot cross the x-axis."),
    box("Check: x² is never negative, so x² + 4 is always at least 4, never 0. Number of roots = ", 0,
        "Can x² + 4 ever equal 0?",
        done="It stays above the axis, so there are 0 roots.")]
s[6]["chart"] = make_chart(lambda x: x*x+4, -3, 3, -1, 14, 2)

# GOLD
g = pb["gold"]

# g0 tp_x 2x^2-8x+6 -> 2
g[0]["hint"] = "Use x = −b/(2a), and remember 2a = 4 here."
g[0]["misconceptions"] = [mc("forgot_a_in_2a",
    "Use 2a in the bottom: 2a = 4, so x = 8/4 = 2. Dividing by 2 (forgetting a = 2) gives 4.", 4)]
g[0]["guided_steps"] = [
    box("Read a and b: a = 2, b = −8. Work out 2a = 2 × 2 = ", 4, "Double a; do not forget a = 2."),
    box("Now −b = −(−8) = ", 8, "The opposite of −8 is +8.", phase="substitute"),
    box("Divide: 8 ÷ 4 = ", 2, "Divide −b by 2a."),
    box("Check: 2x² " + MINUS + " 8x + 6 factors to 2(x " + MINUS + " 1)(x " + MINUS + " 3), roots 1 and 3; their midpoint is (1 + 3)/2 = ", 2,
        "The turning point is halfway between the roots.",
        done="Both methods give x = 2 for the turning point.")]

# g1 tp_y 2x^2-8x+6 -> -2
g[1]["hint"] = "Find the turning point x = 2 first, then substitute into the equation."
g[1]["misconceptions"] = [mc("wrong_tp_x",
    "The turning point is at x = 2, not x = 4. Substituting x = 2: 2(4) " + MINUS + " 16 + 6 = −2.", 6)]
g[1]["guided_steps"] = [
    box("Turning point x = −b/(2a) = 8/4 = ", 2, "Work out −b over 2a first."),
    box("Substitute x = 2. The 2x² term: 2 × 2² = 2 × 4 = ", 2*4, "Square 2, then times 2.", phase="substitute"),
    box("The −8x term: −8 × 2 = ", -8*2, "Multiply −8 by 2."),
    box("Add with +6: 8 + (−16) + 6 = ", 2*4-8*2+6, "Combine the three parts."),
    box("Shape check: a = 2 > 0, so it opens up and this is the minimum, y = ", 2*4-8*2+6,
        "The minimum value is the turning point y.",
        done="The vertex is (2, −2), so the y-coordinate is −2.")]

# g2 tp_x given roots -1 and 9 -> 4  (CHANGED from 5 to de-dup with g0)
g[2]["display"] = "The roots of a quadratic are \\(x = -1\\) and \\(x = 9\\). Find the x-coordinate of the turning point."
g[2]["solutions"] = [4]
g[2]["hint"] = "The turning point x is the average of the two roots."
g[2]["misconceptions"] = [mc("used_difference",
    "The turning point is the average (sum ÷ 2): (−1 + 9)/2 = 4. Using the difference instead gives 5.", 5)]
g[2]["guided_steps"] = [
    box("The turning point is halfway between the roots. Add them: −1 + 9 = ", -1+9, "Add the two roots."),
    box("Halve it: 8 ÷ 2 = ", (-1+9)//2, "Divide the sum by 2.", phase="substitute"),
    box("So the turning point x-coordinate is ", 4, "State the midpoint."),
    box("Check the distances: 4 is 5 away from −1 and 5 away from 9. Equal, so the midpoint x is ", 4,
        "Confirm it is the same distance from each root.",
        done="4 is exactly between −1 and 9, so it is the turning point x-coordinate.")]

# g3 product roots x^2-2x-15 -> -15
g[3]["hint"] = "The product of the roots is c/a."
g[3]["misconceptions"] = [mc("sign_slip",
    "Product = c/a = −15/1 = −15. The roots are 5 and −3, and 5 × (−3) = −15. Dropping the sign gives +15.", 15)]
g[3]["guided_steps"] = [
    box("Factorise: x² " + MINUS + " 2x " + MINUS + " 15 = (x " + MINUS + " 5)(x + 3). One root: x = ", 5, "Set x " + MINUS + " 5 = 0."),
    box("The other root: x = ", -3, "Set x + 3 = 0.", phase="substitute"),
    box("Multiply them: 5 × (−3) = ", 5*-3, "Multiply the two roots."),
    box("Check with the constant term: c/a = −15/1 = ", -15, "Compare with c over a.",
        done="Both methods give −15, so the product of the roots is −15.")]

# g4 max value -3x^2+12x-9 -> 3 (chart)
g[4]["hint"] = "Find the turning point x, then substitute to get the maximum y-value."
g[4]["misconceptions"] = [mc("gave_x",
    "x = 2 is where the max occurs; the maximum VALUE is y there: −12 + 24 " + MINUS + " 9 = 3.", 2)]
g[4]["guided_steps"] = [
    box("Read a = −3, b = 12. Work out 2a = 2 × (−3) = ", -6, "Double a; keep the minus."),
    box("Turning point x = −b/(2a) = −12/(−6) = ", 2, "Divide −b by 2a.", phase="substitute"),
    box("Substitute x = 2. The −3x² term: −3 × 2² = −3 × 4 = ", -3*4, "Square 2, then times −3."),
    box("The +12x term: 12 × 2 = ", 12*2, "Multiply 12 by 2."),
    box("Add with −9: −12 + 24 + (−9) = ", -3*4+12*2-9, "Combine the three parts."),
    box("Shape check: a = −3 < 0, opens down, so this is the maximum. Max y = ", -3*4+12*2-9,
        "The maximum value is the turning point y.",
        done="The vertex is (2, 3), so the maximum value of y is 3.")]
g[4]["chart"] = make_chart(lambda x: -3*x*x+12*x-9, 0, 4, -12, 5, 2)

# ---------- descriptions ----------
pb["bronze_description"] = "Read one feature straight off a simple quadratic: a value, an intercept, a root, or the direction."
pb["silver_description"] = "Find roots, turning points and max or min values of quadratics where the x² coefficient is 1."
pb["gold_description"] = "Work with quadratics where the x² coefficient is not 1, and use facts about the roots."

# ---------- tier_guides ----------
tier_guides = {
 "bronze": {
  "title": "Bronze: read one feature off the curve",
  "steps": [
   "A quadratic \\(y = ax^2 + bx + c\\) draws a <strong>parabola</strong>: a U-shape if a is positive, an arch if a is negative.",
   "To find y at a value of x, substitute: square the x, then work out the other terms and add. Watch the sign when x is negative.",
   "The <strong>y-intercept</strong> is the constant c (set x = 0). A <strong>root</strong> is where y = 0."
  ],
  "example": {
   "question": "For y = x² " + MINUS + " 4, find y when x = 3 and give the positive root.",
   "steps": [
    {"label": "Substitute", "content": "<p>\\(y = 3^2 - 4 = 9 - 4 = 5\\)</p>"},
    {"label": "Roots", "content": "<p>Set \\(y = 0\\): \\(x^2 = 4\\), so \\(x = 2\\) or \\(x = -2\\).</p>"},
    {"label": "Check", "content": "<p>\\(2^2 - 4 = 0\\) ✓</p>"},
    {"label": "Answer", "content": "<p>\\(y = 5\\); positive root \\(x = 2\\)</p>", "isAnswer": True, "is_answer": True}
   ]
  }
 },
 "silver": {
  "title": "Silver: roots and turning points (a = 1)",
  "steps": [
   "<strong>Roots</strong>: factorise \\(x^2 + bx + c\\) into two brackets, then set each to 0. Two numbers that multiply to c and add to b.",
   "<strong>Turning point</strong>: the x-coordinate is \\(x = \\frac{-b}{2a}\\) (or the midpoint of the roots). Substitute it back for the y-coordinate.",
   "If a is positive the turning point is a minimum; if a is negative it is a maximum. Its y-value is the min or max value."
  ],
  "example": {
   "question": "Find the turning point of y = x² " + MINUS + " 6x + 8.",
   "steps": [
    {"label": "x-coordinate", "content": "<p>\\(x = \\frac{-(-6)}{2} = 3\\)</p>"},
    {"label": "y-coordinate", "content": "<p>\\(y = 9 - 18 + 8 = -1\\)</p>"},
    {"label": "Check", "content": "<p>\\(a = 1 > 0\\), so this is a minimum.</p>"},
    {"label": "Answer", "content": "<p>Turning point \\((3, -1)\\)</p>", "isAnswer": True, "is_answer": True}
   ]
  }
 },
 "gold": {
  "title": "Gold: when the x² coefficient is not 1",
  "steps": [
   "The turning point x is still \\(x = \\frac{-b}{2a}\\), but now use the real value of a (for example 2a = 4 when a = 2).",
   "For the max or min <strong>value</strong>, substitute that x back into the full equation. That y is the answer, not the x.",
   "Root facts: the roots sum to \\(\\frac{-b}{a}\\) and multiply to \\(\\frac{c}{a}\\); the turning point x is the average of the roots."
  ],
  "example": {
   "question": "Find the turning point of y = 2x² " + MINUS + " 12x + 10.",
   "steps": [
    {"label": "x-coordinate", "content": "<p>\\(2a = 4\\), so \\(x = \\frac{12}{4} = 3\\)</p>"},
    {"label": "y-coordinate", "content": "<p>\\(y = 18 - 36 + 10 = -8\\)</p>"},
    {"label": "Check", "content": "<p>\\(a = 2 > 0\\), a minimum.</p>"},
    {"label": "Answer", "content": "<p>Turning point \\((3, -8)\\)</p>", "isAnswer": True, "is_answer": True}
   ]
  }
 }
}

# ---------- slim method_card (trim steps 5 -> 4) ----------
live["method_card"] = {
 "title": "How to Work with Quadratic Graphs",
 "steps": [
  "Sign of x²: positive opens upward (minimum), negative opens downward (maximum).",
  "Roots: where the curve crosses the x-axis (y = 0). Factorise or read them off.",
  "Turning point: x is the midpoint of the roots, or \\(x = \\frac{-b}{2a}\\); substitute back for y.",
  "y-intercept: the constant c, where x = 0."
 ],
 "content": "<p>A <strong>quadratic graph</strong> is a U-shaped (or arch-shaped) curve called a <strong>parabola</strong>, given by \\(y = ax^2 + bx + c\\).</p><p>If \\(a > 0\\) it opens upward (minimum); if \\(a < 0\\) it opens downward (maximum).</p><p>The <strong>roots</strong> are where the curve crosses the x-axis (\\(y = 0\\)); the <strong>turning point</strong> is the vertex.</p>",
 "example": "<p><strong>Sketch \\(y = x^2 - 4x + 3\\).</strong></p><p>Roots: \\((x-1)(x-3) = 0\\), so \\(x = 1\\) and \\(x = 3\\).</p><p>Turning point: \\(x = \\frac{1+3}{2} = 2\\), \\(y = 4 - 8 + 3 = -1\\). Vertex \\((2, -1)\\).</p>"
}

# ---------- fix em dashes in preserved worked_examples labels ----------
for we in live.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ")

# ---------- attach guided + tier_guides ----------
live["guided"] = {"opener": opener, "teach": teach}
live["tier_guides"] = tier_guides

json.dump(live, io.open("lesson_maths-ocr_graphs-L03.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written lesson_maths-ocr_graphs-L03.json")
