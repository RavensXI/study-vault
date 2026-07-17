# -*- coding: utf-8 -*-
import json, io

LIVE = json.load(io.open("_gL03_live.json", encoding="utf-8"))

# ---------------------------------------------------------------- SVG helper
def curve_svg(f, xmin, xmax, ymin, ymax, xticks, yticks, marks, aria):
    W, H = 260, 185
    L, R, T, B = 40.0, 246.0, 14.0, 158.0
    def sx(x): return round(L + (x - xmin) / (xmax - xmin) * (R - L), 1)
    def sy(y): return round(B - (y - ymin) / (ymax - ymin) * (B - T), 1)
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:260px" font-family="Inter, sans-serif">' % (W, H, aria)]
    # axes through origin (or edges)
    ax0 = 0 if (ymin <= 0 <= ymax) else ymin
    ay0 = 0 if (xmin <= 0 <= xmax) else xmin
    out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1.2"/>' % (sx(xmin), sy(ax0), sx(xmax), sy(ax0)))
    out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1.2"/>' % (sx(ay0), sy(ymin), sx(ay0), sy(ymax)))
    # x ticks
    for t in xticks:
        out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1"/>' % (sx(t), sy(ax0), sx(t), sy(ax0) + 3))
        out.append('<text x="%s" y="%s" font-size="9" fill="currentColor" text-anchor="middle">%s</text>' % (sx(t), sy(ax0) + 13, t))
    # y ticks
    for t in yticks:
        out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="1"/>' % (sx(ay0) - 3, sy(t), sx(ay0), sy(t)))
        out.append('<text x="%s" y="%s" font-size="9" fill="currentColor" text-anchor="end">%s</text>' % (sx(ay0) - 5, sy(t) + 3, t))
    # curve
    N = 80
    pts = []
    for i in range(N + 1):
        x = xmin + (xmax - xmin) * i / N
        y = f(x)
        if ymin - 0.4 <= y <= ymax + 0.4:
            pts.append("%s,%s" % (sx(x), sy(y)))
    out.append('<polyline points="%s" fill="none" stroke="#3b82f6" stroke-width="2"/>' % " ".join(pts))
    # marks
    for m in marks:
        cx, cy = sx(m["x"]), sy(m["y"])
        if m.get("dash"):
            out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 3"/>' % (cx, sy(ax0), cx, cy))
        out.append('<circle cx="%s" cy="%s" r="3.2" fill="#f59e0b"/>' % (cx, cy))
        if m.get("label"):
            dy = m.get("ldy", -7)
            out.append('<text x="%s" y="%s" font-size="10" fill="currentColor" text-anchor="%s">%s</text>' % (cx + m.get("ldx", 5), cy + dy, m.get("anchor", "start"), m["label"]))
    out.append("</svg>")
    return "".join(out)

# ---------------------------------------------------------------- figures
# Opener: ball arch  y = -0.25 x^2 + 2x  (0..8), peak (4,4), (2,3),(6,3)
opener_svg = curve_svg(
    lambda x: -0.25 * x * x + 2 * x, 0, 8, 0, 4.6,
    [0, 2, 4, 6, 8], [],
    [{"x": 4, "y": 4, "label": "top", "anchor": "middle", "ldx": 0, "ldy": -6, "dash": True},
     {"x": 2, "y": 3, "label": "3 m", "anchor": "end", "ldx": -5, "ldy": -2}],
    "A symmetric arch showing a thrown ball, starting and landing on the ground 8 metres apart, highest at the middle")

# Teach bronze: y = x^2 - 2x - 3
tb_svg = curve_svg(lambda x: x * x - 2 * x - 3, -2.2, 4.2, -4.6, 5.4,
    [-2, -1, 0, 1, 2, 3, 4], [-4, -2, 2, 4],
    [{"x": 1, "y": -4, "label": "lowest", "anchor": "start", "ldx": 6, "ldy": 4}],
    "A U-shaped parabola y equals x squared minus 2x minus 3, lowest point near x equals 1")

# Teach silver: y = x^2 - 6x + 8 ; roots 2,4 ; TP (3,-1)
ts_svg = curve_svg(lambda x: x * x - 6 * x + 8, -0.2, 6.2, -1.6, 8.6,
    [0, 1, 2, 3, 4, 5, 6], [2, 4, 6, 8],
    [{"x": 2, "y": 0, "label": "root", "anchor": "middle", "ldx": -6, "ldy": -6},
     {"x": 4, "y": 0, "label": "root", "anchor": "start", "ldx": 4, "ldy": -6},
     {"x": 3, "y": -1, "label": "min", "anchor": "middle", "ldx": 0, "ldy": 14}],
    "A U-shaped parabola y equals x squared minus 6x plus 8 crossing the x-axis at 2 and 4, minimum at x equals 3")

# Teach gold: y = -x^2 + 4x - 1 ; TP (2,3) max
tg_svg = curve_svg(lambda x: -x * x + 4 * x - 1, -0.8, 4.8, -3.4, 4.0,
    [0, 1, 2, 3, 4], [-2, 2],
    [{"x": 2, "y": 3, "label": "max", "anchor": "middle", "ldx": 0, "ldy": -6, "dash": True}],
    "An n-shaped downward parabola y equals minus x squared plus 4x minus 1, maximum at x equals 2")

# ---------------------------------------------------------------- step helpers
def S(say):
    return {"say": say}

def Bx(pre, ans, hint, post="", done=None, phase=False, say=None):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if done: d["done"] = done
    if phase: d["phase"] = "substitute"
    if say is not None: d["say"] = say
    return d

# ---------------------------------------------------------------- method_card
method_card = {
    "title": "How to Plot and Read Quadratic Graphs",
    "steps": [
        "Substitute x-values into y = ax² + bx + c to build a table of points.",
        "Plot the points and join them with a smooth U or ∩ curve, never straight lines.",
        "Roots are where y = 0; the y-intercept is c; the turning point is the lowest or highest point.",
        "The curve is symmetric: the turning point x is halfway between the roots, or x = −b ÷ (2a)."
    ],
    "content": "<p>A <strong>quadratic graph</strong> \\(y = ax^2 + bx + c\\) is a symmetric curve called a <strong>parabola</strong>. If \\(a\\) is positive it opens upward (U shape); if \\(a\\) is negative it opens downward (∩ shape).</p><p>The <strong>roots</strong> are where it crosses the x-axis (\\(y = 0\\)). The <strong>y-intercept</strong> is \\(c\\), where \\(x = 0\\). The <strong>turning point</strong> is the lowest or highest point; it sits on the line of symmetry at \\(x = -\\frac{b}{2a}\\), halfway between the roots.</p>",
    "example": "<p><strong>Plot \\(y = x^2 - 4x + 3\\).</strong></p><p>Table: \\(x = 0\\) gives 3, \\(x = 1\\) gives 0, \\(x = 2\\) gives −1, \\(x = 3\\) gives 0, \\(x = 4\\) gives 3.</p><p>Roots \\(x = 1\\) and \\(x = 3\\); turning point \\((2, -1)\\); y-intercept 3.</p>"
}

# ---------------------------------------------------------------- tier_guides
tier_guides = {
    "bronze": {
        "title": "Bronze: Substituting into a quadratic",
        "steps": [
            "Replace every \\(x\\) in \\(y = ax^2 + bx + c\\) with the value you are given.",
            "Work out the square first, then the multiply, keeping the signs. Remember \\((-3)^2 = +9\\).",
            "Add the three parts. At \\(x = 0\\) everything but \\(c\\) vanishes, so the y-intercept is \\(c\\)."
        ],
        "example": {
            "question": "Find \\(y\\) when \\(x = 3\\) for \\(y = x^2 - 2x - 3\\).",
            "steps": [
                {"label": "Square", "content": "\\(3^2 = 9\\)"},
                {"label": "Middle term", "content": "\\(-2 \\times 3 = -6\\)"},
                {"label": "Add", "content": "\\(9 - 6 - 3\\)"},
                {"label": "Answer", "content": "\\(y = 0\\)", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: Roots, symmetry and turning points",
        "steps": [
            "Roots are where \\(y = 0\\). Factorise, or use that the roots add to \\(-b\\) and multiply to \\(c\\).",
            "The turning point sits halfway between the roots, so average them to get its \\(x\\).",
            "Substitute that \\(x\\) back to get the turning point \\(y\\). The curve is symmetric about that line."
        ],
        "example": {
            "question": "Turning point of \\(y = x^2 - 6x + 8\\).",
            "steps": [
                {"label": "Roots", "content": "\\((x-2)(x-4)=0\\), so \\(x = 2\\) or \\(x = 4\\)"},
                {"label": "Symmetry", "content": "\\(x = (2 + 4) \\div 2 = 3\\)"},
                {"label": "y-value", "content": "\\(9 - 18 + 8 = -1\\)"},
                {"label": "Answer", "content": "\\((3, -1)\\)", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: Turning points from the formula",
        "steps": [
            "For \\(y = ax^2 + bx + c\\) the turning point \\(x\\) is \\(x = -b \\div (2a)\\). Mind the signs.",
            "If \\(a\\) is positive the curve is a U (minimum); if \\(a\\) is negative it is a ∩ (maximum).",
            "Completed square \\(y = (x - a)^2 + b\\) shows the turning point straight off, at \\((a, b)\\)."
        ],
        "example": {
            "question": "Turning point of \\(y = -x^2 + 4x - 1\\).",
            "steps": [
                {"label": "x-value", "content": "\\(x = -4 \\div (2 \\times -1) = 2\\)"},
                {"label": "y-value", "content": "\\(-4 + 8 - 1 = 3\\)"},
                {"label": "Shape", "content": "\\(a < 0\\), so it is a maximum"},
                {"label": "Answer", "content": "\\((2, 3)\\) maximum", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------------------------------------------------------- opener
opener = {
    "display": opener_svg,
    "steps": [
        S("A ball is kicked across a field. Its flight makes a smooth arch, shown above. No algebra, just look at the picture."),
        Bx("The ball leaves the ground at x = 0 and lands at x = 8. It is highest exactly halfway along, at x = ", 4,
           "Halfway between 0 and 8.", post=" m"),
        S("That midpoint is the <strong>turning point</strong>: the very top (or bottom) of the arch. It always sits halfway between the two places the curve meets the ground, its <strong>roots</strong>."),
        Bx("The arch is a mirror image about that middle. It is 3 m high at x = 2, so it is also 3 m high at x = ", 6,
           "The middle is x = 4, and 2 is two steps to the left, so count two steps to the right.", post=" m"),
        S("Equal heights come in mirror pairs. Those two facts, a turning point halfway between the roots and matching heights either side, are the whole of quadratic graphs. Every parabola \\(y = ax^2 + bx + c\\) is this same symmetric arch: opening up if \\(a\\) is positive, down if \\(a\\) is negative.")
    ]
}

# ---------------------------------------------------------------- teach walks
teach = {
    "bronze": {
        "display": tb_svg + "<p>Build the graph of \\(y = x^2 - 2x - 3\\) by substituting x-values into a table.</p>",
        "steps": [
            S("Take each x in turn and work out y. Square first, then the middle term, then add."),
            Bx("x = 0:  y = 0 − 0 − 3 = ", -3, "Only the constant is left."),
            Bx("x = 1:  y = 1 − 2 − 3 = ", -4, "1 minus 2 minus 3."),
            Bx("x = 2:  y = 4 − 4 − 3 = ", -3, "4 minus 4 minus 3.", done="Same as x = 0. The curve is symmetric."),
            Bx("x = 3:  y = 9 − 6 − 3 = ", 0, "9 minus 6 minus 3."),
            S("Plot (0, −3), (1, −4), (2, −3), (3, 0) and join with a smooth U. The lowest point is at x = 1."),
            Bx("Check it rises again: at x = 4, y = 16 − 8 − 3 = ", 5, "16 minus 8 minus 3.", done="It climbs back up, confirming the U shape.")
        ]
    },
    "silver": {
        "display": ts_svg + "<p>Find the roots and turning point of \\(y = x^2 - 6x + 8\\).</p>",
        "steps": [
            S("Roots are where y = 0. Factorise \\(x^2 - 6x + 8\\): two numbers that multiply to 8 and add to −6."),
            Bx("Those numbers are −2 and −4, giving (x − 2)(x − 4). The smaller root is x = ", 2, "x − 2 = 0."),
            Bx("The larger root is x = ", 4, "x − 4 = 0."),
            S("The turning point sits halfway between the roots."),
            Bx("Turning point x = (2 + 4) ÷ 2 = ", 3, "Average the two roots."),
            Bx("Turning point y = 3² − 6×3 + 8 = 9 − 18 + 8 = ", -1, "9 minus 18 plus 8."),
            Bx("Check the symmetry: at x = 5, y = 25 − 30 + 8 = ", 3, "25 minus 30 plus 8.", done="Same height as x = 1, so x = 3 really is the middle.")
        ]
    },
    "gold": {
        "display": tg_svg + "<p>Find the turning point of \\(y = -x^2 + 4x - 1\\) and say if it is a maximum or minimum.</p>",
        "steps": [
            S("Here \\(a = -1\\), which is negative, so the curve is ∩-shaped and the turning point is a <strong>maximum</strong>. Use \\(x = -b \\div (2a)\\) with a = −1, b = 4."),
            Bx("Bottom of the formula: 2a = 2 × (−1) = ", -2, "2 times minus 1."),
            Bx("Turning point x = −4 ÷ (−2) = ", 2, "A minus divided by a minus is positive."),
            S("Now substitute x = 2 to get the height of the maximum."),
            Bx("The square term: −(2²) = ", -4, "Square 2 first, then apply the minus."),
            Bx("y = −4 + 4×2 − 1 = −4 + 8 − 1 = ", 3, "Minus 4 plus 8 minus 1.", done="The maximum is at (2, 3)."),
            Bx("Check the mirror: at x = 3, y = −9 + 12 − 1 = ", 2, "Minus 9 plus 12 minus 1.", done="Same as x = 1, confirming x = 2 is the peak.")
        ]
    }
}

# ---------------------------------------------------------------- problem bank
def prob(display, sol, it, hint, gs=None, misc=None, options=None, chart=None, calc=False):
    p = {"display": display, "solutions": sol if isinstance(sol, list) else [sol],
         "calculator": calc, "input_type": it, "hint": hint,
         "misconceptions": misc or []}
    if options is not None: p["options"] = options
    if gs is not None: p["guided_steps"] = gs
    if chart is not None: p["chart"] = chart
    return p

def mc(expect, message, pattern):
    return {"pattern": pattern, "expect": expect, "message": message}

# ----- BRONZE -----
bronze = []

# B0  y=x^2+3x+2, x=2 -> 12
bronze.append(prob(
    "For \\(y = x^2 + 3x + 2\\), find \\(y\\) when \\(x = 2\\).", 12, "single_value",
    "Work out 2 squared first, then 3 times 2, then add on the 2.",
    gs=[
        S("Substitute x = 2 into each term."),
        Bx("The square: 2² = ", 4, "2 times 2."),
        Bx("The middle term: 3 × 2 = ", 6, "Three lots of 2."),
        Bx("Add the three parts: y = 4 + 6 + 2 = ", 12, "4 plus 6 plus 2.", phase=True),
        Bx("Check by re-adding: 4 + 6 = 10, then 10 + 2 = ", 12, "Add the constant last.", done="y = 12 at x = 2.")
    ],
    misc=[mc(10, "Do not drop the constant. y = 4 + 6 + 2 = 12, not 10.", "dropped_constant")]))

# B1  y=x^2-5x+6, x=0 -> 6
bronze.append(prob(
    "For \\(y = x^2 - 5x + 6\\), find \\(y\\) when \\(x = 0\\).", 6, "single_value",
    "Put x = 0 in; only the constant is left.",
    gs=[
        S("Substitute x = 0. Every term with an x becomes 0."),
        Bx("The square: 0² = ", 0, "Zero times zero."),
        Bx("The middle term: −5 × 0 = ", 0, "Anything times 0 is 0."),
        Bx("So y = 0 − 0 + 6 = ", 6, "Only the constant is left.", phase=True),
        Bx("This is the y-intercept. The constant term is ", 6, "Read the number on its own.", done="At x = 0, y = c = 6.")
    ],
    misc=[mc(0, "At x = 0 the x-terms vanish, but the constant 6 stays, so y = 6, not 0.", "root_intercept_mix")]))

# B2  y-intercept of y=x^2+4x-7 -> -7
bronze.append(prob(
    "What is the y-intercept of \\(y = x^2 + 4x - 7\\)?", -7, "single_value",
    "The y-intercept is the constant term, keeping its sign.",
    gs=[
        S("The y-intercept is the value of y when x = 0."),
        Bx("Put x = 0: the square 0² = ", 0, "Zero squared."),
        Bx("The x term: 4 × 0 = ", 0, "Anything times 0."),
        Bx("So y = 0 + 0 + (−7) = ", -7, "Only the constant survives.", phase=True),
        Bx("The constant c in y = x² + 4x − 7 is ", -7, "Keep the minus sign.", done="y-intercept always equals c.")
    ],
    misc=[
        mc(7, "The y-intercept keeps its sign: c = −7, not 7.", "sign_dropped"),
        mc(4, "The y-intercept is the constant term, not the number in front of x. It is −7.", "used_b")
    ]))

# B3  y=x^2-4, x=3 -> 5
bronze.append(prob(
    "For \\(y = x^2 - 4\\), find \\(y\\) when \\(x = 3\\).", 5, "single_value",
    "Square the 3 to get 9, then subtract 4.",
    gs=[
        S("Substitute x = 3."),
        Bx("The square: 3² = ", 9, "3 times 3, not 3 times 2."),
        S("There is no middle term here, just subtract 4."),
        Bx("y = 9 − 4 = ", 5, "Nine take away four.", phase=True),
        Bx("Check: 9 − 4 lands on ", 5, "Recount.", done="y = 5 at x = 3.")
    ],
    misc=[mc(2, "3² means 3 × 3 = 9, not 3 × 2 = 6. Then 9 − 4 = 5.", "square_as_double")]))

# B4  y=x^2+2x, x=-1 -> -1
bronze.append(prob(
    "For \\(y = x^2 + 2x\\), find \\(y\\) when \\(x = -1\\).", -1, "single_value",
    "Square the −1 to get +1, then add 2 times −1.",
    gs=[
        S("Substitute x = −1. Take care with the signs."),
        Bx("The square: (−1)² = ", 1, "A minus times a minus is a plus."),
        Bx("The x term: 2 × (−1) = ", -2, "Two lots of minus one."),
        Bx("So y = 1 + (−2) = ", -1, "One take away two.", phase=True),
        Bx("Check: 1 − 2 = ", -1, "Recount on a line.", done="y = −1 at x = −1.")
    ],
    misc=[mc(-3, "(−1)² = +1, not −1. Then 1 + (−2) = −1.", "neg_square")]))

# B5  CHANGED: y-intercept 8 -> c=8  (was y-intercept 5 -> 5, duplicate of B3)
bronze.append(prob(
    "The curve \\(y = x^2 + bx + c\\) has y-intercept 8. What is \\(c\\)?", 8, "single_value",
    "The y-intercept always equals c.",
    gs=[
        S("The y-intercept is the height of the curve where it crosses the y-axis."),
        Bx("The y-axis is where x = ", 0, "The y-axis is the vertical line x = 0."),
        Bx("At x = 0 the x² and bx terms are 0, so y = c. The y-intercept is 8, therefore c = ", 8, "y-intercept equals c.", phase=True),
        Bx("Check: with c = 8, at x = 0, y = 0 + 0 + 8 = ", 8, "Substitute back.", done="The y-intercept is 8, so c = 8.")
    ],
    misc=[]))

# B6  MC shape of y=2x^2+3 -> U (index 0)
bronze.append(prob(
    "Which shape does the graph \\(y = 2x^2 + 3\\) have?", 0, "multiple_choice",
    "Look at the sign of the number in front of x squared.",
    options=["U shape (opens up)", "∩ shape (opens down)", "Straight line", "S shape"],
    misc=[mc(1, "Since a = 2 (positive), the parabola opens upward into a U shape.", "shape_confusion")]))

# B7  CHANGED: y=x^2-6x+9, x=1 -> 4  (was x=3 -> 0, duplicate of B6 index)
bronze.append(prob(
    "For \\(y = x^2 - 6x + 9\\), find \\(y\\) when \\(x = 1\\).", 4, "single_value",
    "Square the 1, then subtract 6 times 1, then add 9.",
    gs=[
        S("Substitute x = 1."),
        Bx("The square: 1² = ", 1, "One times one."),
        Bx("The middle term: −6 × 1 = ", -6, "Minus six times one."),
        Bx("So y = 1 − 6 + 9 = ", 4, "One minus six plus nine.", phase=True),
        Bx("Check: 1 − 6 = −5, then −5 + 9 = ", 4, "Add nine last.", done="y = 4 at x = 1. (This curve has a repeated root at x = 3, where it touches the x-axis.)")
    ],
    misc=[mc(16, "The middle term is −6 × 1 = −6, so y = 1 − 6 + 9 = 4, not 16.", "sign_error")]))

# ----- SILVER -----
silver = []

# S0  roots -1,5 of y=x^2-4x-5, TP x -> 2   (add chart)
s0_chart = {
    "type": "scatter",
    "data": {"datasets": [
        {"type": "line", "data": [{"x": x, "y": x * x - 4 * x - 5} for x in range(-2, 7)],
         "tension": 0.35, "fill": False, "borderColor": "#3b82f6", "pointRadius": 0},
        {"type": "scatter", "data": [{"x": -1, "y": 0}, {"x": 5, "y": 0}],
         "pointRadius": 5, "pointBackgroundColor": "#f59e0b", "borderColor": "#f59e0b"}
    ]},
    "options": {"plugins": {"legend": {"display": False}}, "scales": {
        "x": {"min": -2, "max": 6, "ticks": {"stepSize": 1}, "grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": "x", "display": True}},
        "y": {"min": -10, "max": 8, "ticks": {"stepSize": 2}, "grid": {"color": "rgba(0,0,0,0.08)"}, "title": {"text": "y", "display": True}}
    }}
}
silver.append(prob(
    "The roots of \\(y = x^2 - 4x - 5\\) are \\(x = -1\\) and \\(x = 5\\) (marked on the graph). What is the \\(x\\)-coordinate of the turning point?", 2, "single_value",
    "Average the two roots.",
    gs=[
        S("A parabola is symmetric, so the turning point sits exactly halfway between the roots."),
        Bx("Add the roots: −1 + 5 = ", 4, "Minus one plus five."),
        Bx("Halfway means divide by 2: 4 ÷ 2 = ", 2, "Half of four.", phase=True),
        Bx("Check the gaps match: from −1 to 2 is 3, and from 2 to 5 is ", 3, "Count the steps.", done="Equal gaps, so x = 2 is the midpoint.")
    ],
    misc=[mc(4, "Halfway means the average: (−1 + 5) ÷ 2 = 2. Stopping at the sum 4 forgets to halve.", "forgot_halve")],
    chart=s0_chart))

# S1  y=x^2-4x-5, TP y -> -9
silver.append(prob(
    "For \\(y = x^2 - 4x - 5\\), find the \\(y\\)-coordinate of the turning point.", -9, "single_value",
    "Find the turning point x first (average the roots), then substitute.",
    gs=[
        S("The roots are −1 and 5, so the turning point x = (−1 + 5) ÷ 2 = 2. Now substitute x = 2."),
        Bx("The square: 2² = ", 4, "Two times two."),
        Bx("The middle term: −4 × 2 = ", -8, "Minus four times two."),
        Bx("So y = 4 + (−8) + (−5) = ", -9, "Four minus eight minus five.", phase=True),
        Bx("Check: 4 − 8 = −4, then −4 − 5 = ", -9, "Keep going down.", done="Turning point is (2, −9).")
    ],
    misc=[mc(7, "The middle term is −4 × 2 = −8, so y = 4 − 8 − 5 = −9. Using +8 gives the wrong sign.", "sign_error")]))

# S2  MC shape y=-3x^2+2x+1 -> ∩ (index 1)
silver.append(prob(
    "Which shape does the graph \\(y = -3x^2 + 2x + 1\\) have?", 1, "multiple_choice",
    "A negative number in front of x squared flips the curve over.",
    options=["U shape (opens up)", "∩ shape (opens down)", "Straight line", "S shape"],
    misc=[mc(0, "Since a = −3 (negative), the parabola opens downward into a ∩ shape.", "shape_confusion")]))

# S3  y=x^2-2x-8, one root x=4, other -> -2
silver.append(prob(
    "For \\(y = x^2 - 2x - 8\\), one root is at \\(x = 4\\). Find the other root.", -2, "single_value",
    "The two roots add up to −b; subtract the known root.",
    gs=[
        S("For \\(x^2 + bx + c\\) the two roots add up to −b. Here b = −2, so the roots add to 2."),
        Bx("The roots add to 2. One root is 4, so the other is 2 − 4 = ", -2, "Two minus four.", phase=True),
        Bx("Check the product: the roots multiply to c = −8. Is 4 × (−2) = ", -8, "Four times minus two."),
        Bx("Substitute x = −2 into y: 4 + 4 − 8 = ", 0, "(−2)² is 4; −2×(−2) is 4.", done="y = 0 confirms −2 is a root.")
    ],
    misc=[mc(2, "The roots add to 2 (that is −b). With one root 4, the other is 2 − 4 = −2, a negative.", "dropped_sign")]))

# S4  y=x^2+3x-1, x=-2 -> -3
silver.append(prob(
    "Find the value of \\(y\\) when \\(x = -2\\) for the equation \\(y = x^2 + 3x - 1\\).", -3, "single_value",
    "Square the −2 to get +4, then add 3 times −2.",
    gs=[
        S("Substitute x = −2. Mind the signs."),
        Bx("The square: (−2)² = ", 4, "A minus times a minus is a plus."),
        Bx("The middle term: 3 × (−2) = ", -6, "Three times minus two."),
        Bx("So y = 4 + (−6) − 1 = ", -3, "Four minus six minus one.", phase=True),
        Bx("Check: 4 − 6 = −2, then −2 − 1 = ", -3, "Take one more away.", done="y = −3 at x = −2.")
    ],
    misc=[mc(-11, "(−2)² = +4, not −4. Then 4 + (−6) − 1 = −3.", "neg_square")]))

# S5  roots 2,6 -> line of symmetry x=4
silver.append(prob(
    "A quadratic has roots at \\(x = 2\\) and \\(x = 6\\). What is the \\(x\\)-coordinate of the line of symmetry?", 4, "single_value",
    "The line of symmetry is the average of the roots.",
    gs=[
        S("The line of symmetry runs through the turning point, halfway between the roots."),
        Bx("Add the roots: 2 + 6 = ", 8, "Two plus six."),
        Bx("Halfway means divide by 2: 8 ÷ 2 = ", 4, "Half of eight.", phase=True),
        Bx("Check the gaps: from 2 to 4 is 2, and from 4 to 6 is ", 2, "Count the steps.", done="Equal gaps, so the line of symmetry is x = 4.")
    ],
    misc=[mc(8, "The line of symmetry is the average of the roots: (2 + 6) ÷ 2 = 4. The sum 8 has not been halved.", "forgot_halve")]))

# S6  y=2x^2-8x+6, x=1 -> 0
silver.append(prob(
    "For \\(y = 2x^2 - 8x + 6\\), find \\(y\\) when \\(x = 1\\).", 0, "single_value",
    "Remember the 2 in front: 2 times x squared.",
    gs=[
        S("Substitute x = 1. The first term has a 2 in front."),
        Bx("The squared term: 2 × 1² = 2 × 1 = ", 2, "Square the 1, then times 2."),
        Bx("The middle term: −8 × 1 = ", -8, "Minus eight times one."),
        Bx("So y = 2 − 8 + 6 = ", 0, "Two minus eight plus six.", phase=True),
        Bx("Check: 2 − 8 = −6, then −6 + 6 = ", 0, "Add six back.", done="y = 0, so x = 1 is a root.")
    ],
    misc=[mc(-1, "The first term is 2x² = 2 × 1² = 2, not 1. Then 2 − 8 + 6 = 0.", "forgot_coefficient")]))

# ----- GOLD -----
gold = []

# G0  y=-x^2+6x-5, TP y -> 4
gold.append(prob(
    "For \\(y = -x^2 + 6x - 5\\), find the \\(y\\)-coordinate of the turning point.", 4, "single_value",
    "Find x with −b over 2a, then substitute to get y.",
    gs=[
        S("Turning point x = −b ÷ (2a), with a = −1 and b = 6."),
        Bx("Bottom of the formula: 2a = 2 × (−1) = ", -2, "Two times minus one."),
        Bx("x = −6 ÷ (−2) = ", 3, "A minus over a minus is positive."),
        S("Now substitute x = 3 to find the y of the turning point."),
        Bx("The square term: −(3²) = ", -9, "Square 3 first, then apply the minus.", phase=True),
        Bx("The middle term: 6 × 3 = ", 18, "Six times three.", phase=True),
        Bx("So y = −9 + 18 − 5 = ", 4, "Minus nine plus eighteen minus five.", phase=True),
        Bx("Check: −9 + 18 = 9, then 9 − 5 = ", 4, "Take five away.", done="Maximum turning point at (3, 4).")
    ],
    misc=[mc(22, "The x² term is −(3²) = −9, not +9. Then −9 + 18 − 5 = 4.", "neg_square")]))

# G1  y=x^2-8x+k touches once -> k=16
gold.append(prob(
    "A quadratic \\(y = x^2 - 8x + k\\) touches the x-axis at exactly one point. Find \\(k\\).", 16, "single_value",
    "One root means the discriminant b² − 4ac is 0.",
    gs=[
        S("Touching at one point means the two roots are equal, so the discriminant b² − 4ac = 0. Here a = 1, b = −8, c = k."),
        Bx("b² = (−8)² = ", 64, "A minus times a minus is a plus."),
        Bx("The 4ac part is 4 × 1 × k = 4k. The number in front of k is ", 4, "Four times one."),
        Bx("Set it to zero: 64 − 4k = 0, so 4k = 64 and k = 64 ÷ 4 = ", 16, "Sixty-four over four.", phase=True),
        Bx("Check: with k = 16, x² − 8x + 16 = (x − 4)². Its repeated root is x = ", 4, "What makes the bracket zero.", done="One repeated root, so the curve touches once.")
    ],
    misc=[mc(-16, "(−8)² = +64, not −64. Then 64 − 4k = 0 gives k = 16.", "neg_square")]))

# G2  y=(x-3)^2-4, TP y -> -4
gold.append(prob(
    "The curve \\(y = (x - 3)^2 - 4\\) is in completed square form. What are the coordinates of the turning point?<br>Give the <strong>y-coordinate</strong>.", -4, "single_value",
    "In (x − a)² + b the turning point is (a, b).",
    gs=[
        S("Completed square form \\(y = (x - a)^2 + b\\) has its turning point at (a, b). Compare (x − 3)² − 4."),
        Bx("The number inside the bracket gives a: x − 3 means a = ", 3, "What makes the bracket zero."),
        Bx("The number outside gives b, the y of the turning point: (x − 3)² − 4 means b = ", -4, "Keep the minus sign.", phase=True),
        Bx("Check by substituting x = 3: (3 − 3)² − 4 = 0 − 4 = ", -4, "The bracket is 0.", done="At x = 3 the bracket is 0, leaving −4, the minimum.")
    ],
    misc=[
        mc(3, "The turning point is (3, −4). The y-coordinate is the −4 outside the bracket, not the 3 inside.", "used_a"),
        mc(4, "Keep the sign: (x − 3)² − 4 has b = −4, so the y-coordinate is −4.", "sign_dropped")
    ]))

# G3  y=3x^2-12x+7, TP x -> 2
gold.append(prob(
    "For \\(y = 3x^2 - 12x + 7\\), find the \\(x\\)-coordinate of the turning point.", 2, "single_value",
    "Use x = −b ÷ (2a); divide by 2 times 3.",
    gs=[
        S("Turning point x = −b ÷ (2a), with a = 3 and b = −12."),
        Bx("Bottom: 2a = 2 × 3 = ", 6, "Two times three."),
        Bx("Top: −b = −(−12) = ", 12, "The opposite of minus twelve."),
        Bx("x = 12 ÷ 6 = ", 2, "Twelve over six.", phase=True),
        Bx("Check with the y: 3×4 − 12×2 + 7 = 12 − 24 + 7 = ", -5, "That is the minimum y.", done="The turning point x we wanted is 2.")
    ],
    misc=[
        mc(4, "Divide by 2a = 2 × 3 = 6, not by 3. That gives 12 ÷ 6 = 2.", "forgot_2a"),
        mc(-2, "−b = −(−12) = +12, a positive. Then 12 ÷ 6 = 2.", "sign_error")
    ]))

# G4  MC y=-2x^2+8x-3 max or min -> Maximum (index 0)
gold.append(prob(
    "The curve \\(y = -2x^2 + 8x - 3\\) has a turning point. Is it a maximum or minimum?", 0, "multiple_choice",
    "A negative number in front of x squared gives a maximum.",
    options=["Maximum", "Minimum"],
    misc=[mc(1, "Since a = −2 (negative), the curve is ∩-shaped, so the turning point is a maximum.", "shape_confusion")]))

problem_bank = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": LIVE["problem_bank"]["bronze_description"],
    "silver_description": LIVE["problem_bank"]["silver_description"],
    "gold_description": LIVE["problem_bank"]["gold_description"]
}

# ---------------------------------------------------------------- worked_examples (fix em dashes)
worked_examples = json.loads(json.dumps(LIVE["worked_examples"]))
def dedash(obj):
    if isinstance(obj, dict):
        return {k: dedash(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [dedash(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace(" — ", ": ").replace("—", "-")
    return obj
worked_examples = dedash(worked_examples)

# ---------------------------------------------------------------- assemble
pd = {
    "method_card": method_card,
    "tier_guides": tier_guides,
    "guided": {"opener": opener, "teach": teach},
    "topic_links": LIVE["topic_links"],
    "problem_bank": problem_bank,
    "related_videos": LIVE.get("related_videos", []),
    "worked_examples": worked_examples
}

json.dump(pd, io.open("lesson_maths-eduqas_graphs-L03.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_maths-eduqas_graphs-L03.json")
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
