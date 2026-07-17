# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams conversion for maths-aqa algebra-L12
Quadratic Inequalities & Regions. Fresh-solve verified; builds guided shape.
Writes lesson_maths-aqa_algebra-L12.json for the validator + PATCH."""
import json, io, math

SRC = "_aqa_L12_live.json"
OUT = "lesson_maths-aqa_algebra-L12.json"

pd = json.load(io.open(SRC, encoding="utf-8"))

# ---------------------------------------------------------------------------
# FIGURE GENERATORS (theme-safe SVG)
# ---------------------------------------------------------------------------
def parabola_svg(r, s, xmin, xmax, region, inclusive, aria):
    """U-parabola y=(x-r)(x-s), roots r<s, axis marked, solution region shaded.
    region: 'between' or 'outside'. inclusive: closed vs open root circles."""
    W = 260.0
    x0, x1 = 22.0, 240.0
    def px(x):
        return x0 + (x - xmin) / (xmax - xmin) * (x1 - x0)
    # graph-y extremes
    yvertex = -((s - r) / 2.0) ** 2
    yedge = max((xmin - r) * (xmin - s), (xmax - r) * (xmax - s))
    axis_py = 88.0
    above = axis_py - 20.0   # room for positive arms
    below = 128.0 - axis_py  # room for the dip
    scale = min(above / yedge, below / (-yvertex))
    def py(yg):
        return axis_py - yg * scale
    pts = []
    n = 48
    for i in range(n + 1):
        x = xmin + (xmax - xmin) * i / n
        yg = (x - r) * (x - s)
        pts.append("%.1f,%.1f" % (px(x), py(yg)))
    poly = " ".join(pts)
    rp, sp = px(r), px(s)
    circ = 'fill="var(--sv-bg, #faf8f5)"' if not inclusive else 'fill="currentColor"'
    # shaded region on the axis
    if region == "between":
        shade = ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="#f59e0b" stroke-width="4" stroke-opacity="0.6"/>'
                 % (rp, axis_py, sp, axis_py))
    else:
        shade = ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="#f59e0b" stroke-width="4" stroke-opacity="0.6"/>'
                 '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'stroke="#f59e0b" stroke-width="4" stroke-opacity="0.6"/>'
                 % (x0, axis_py, rp, axis_py, sp, axis_py, x1, axis_py))
    def rootlbl(v):
        return ("%g" % v)
    svg = (
        '<svg viewBox="0 0 260 140" role="img" aria-label="%s" '
        'style="max-width:280px;width:100%%;height:auto;font-family:Inter,sans-serif">'
        '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" '
        'stroke-width="1" stroke-opacity="0.4"/>'
        '%s'
        '<polyline points="%s" fill="none" stroke="#3b82f6" stroke-width="2"/>'
        '<circle cx="%.1f" cy="%.1f" r="3.5" stroke="#3b82f6" stroke-width="1.5" %s/>'
        '<circle cx="%.1f" cy="%.1f" r="3.5" stroke="#3b82f6" stroke-width="1.5" %s/>'
        '<text x="%.1f" y="%.1f" font-size="11" fill="currentColor" text-anchor="middle">%s</text>'
        '<text x="%.1f" y="%.1f" font-size="11" fill="currentColor" text-anchor="middle">%s</text>'
        '</svg>'
    ) % (
        aria,
        x0, axis_py, x1, axis_py,
        shade,
        poly,
        rp, axis_py, circ,
        sp, axis_py, circ,
        rp, axis_py + 15, rootlbl(r),
        sp, axis_py + 15, rootlbl(s),
    )
    return svg

def numberline_svg(lo, hi, r, s, ints, aria):
    """Number line lo..hi, open circles at roots r,s, filled dots at solution ints."""
    x0, x1 = 20.0, 240.0
    ay = 34.0
    def px(x):
        return x0 + (x - lo) / (hi - lo) * (x1 - x0)
    ticks = ""
    for t in range(lo, hi + 1):
        tx = px(t)
        ticks += ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" '
                  'stroke-width="1" stroke-opacity="0.4"/>'
                  '<text x="%.1f" y="%.1f" font-size="10" fill="currentColor" '
                  'text-anchor="middle">%d</text>' % (tx, ay - 4, tx, ay + 4, tx, ay + 16, t))
    shade = ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#f59e0b" '
             'stroke-width="4" stroke-opacity="0.55"/>' % (px(r), ay, px(s), ay))
    roots = ""
    for v in (r, s):
        roots += ('<circle cx="%.1f" cy="%.1f" r="4" fill="var(--sv-bg, #faf8f5)" '
                  'stroke="#3b82f6" stroke-width="1.5"/>' % (px(v), ay))
    dots = ""
    for v in ints:
        dots += '<circle cx="%.1f" cy="%.1f" r="3.5" fill="#3b82f6"/>' % (px(v), ay)
    svg = (
        '<svg viewBox="0 0 260 56" role="img" aria-label="%s" '
        'style="max-width:280px;width:100%%;height:auto;font-family:Inter,sans-serif">'
        '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" '
        'stroke-width="1" stroke-opacity="0.5"/>%s%s%s%s</svg>'
    ) % (aria, x0, ay, x1, ay, ticks, shade, roots, dots)
    return svg

CAP = '<span class="figure-caption">Sketch, not to scale</span>'

# ---------------------------------------------------------------------------
# METHOD CARD (slim)
# ---------------------------------------------------------------------------
pd["method_card"] = {
    "title": "Quadratic Inequalities and Regions",
    "steps": [
        "Rearrange so one side is 0.",
        "Factorise (or use the formula) to find the roots.",
        "Sketch the U-shaped parabola.",
        "For \\(< 0\\) take between the roots; for \\(> 0\\) take outside them.",
    ],
    "content": (
        "<p><strong>Quadratic inequalities</strong> compare an \\(x^2\\) expression "
        "to zero. Find where it equals zero (the roots), then read the U-shaped graph "
        "to see which region has the sign you want.</p>"
        "<p>Below zero (\\(< 0\\)) is BETWEEN the roots; above zero (\\(> 0\\)) is "
        "OUTSIDE them. Use \\(\\le\\) or \\(\\ge\\) when equality is allowed, and "
        "remember every square has a positive and a negative root.</p>"
    ),
    "example": (
        "<p><strong>Solve</strong> \\(x^2 - 5x + 6 < 0\\)</p>"
        "<p><strong>Step 1:</strong> Factorise: \\((x-2)(x-3) < 0\\)</p>"
        "<p><strong>Step 2:</strong> Roots at \\(x = 2\\) and \\(x = 3\\)</p>"
        "<p><strong>Step 3:</strong> U-shape is below zero <em>between</em> the roots</p>"
        "<p><strong>Answer:</strong> \\(2 < x < 3\\)</p>"
    ),
}

# ---------------------------------------------------------------------------
# TIER DESCRIPTIONS
# ---------------------------------------------------------------------------
pb = pd["problem_bank"]
pb["bronze_description"] = "A square compared to a number, or an already-factorised product. Read the region straight off."
pb["silver_description"] = "Factorise a three-term quadratic first, then choose between or outside the roots."
pb["gold_description"] = "Rearrange, watch a sign flip, then answer the follow-up: count integers, combine conditions, or use the discriminant."

# ---------------------------------------------------------------------------
# HINTS + HONEST MISCONCEPTIONS (keyed by tier+index) for the MULTIPLE-CHOICE
# problems. expect = index of the distractor the error lands on.
# Correct answer is always option index 0 (fresh-solve verified).
# ---------------------------------------------------------------------------
def mc(pattern, expect, message, note):
    return {"pattern": pattern, "check": pattern, "expect": expect,
            "message": message, "note": note}

# bronze
pb["bronze"][0]["hint"] = "Roots are 3 and −3. Less than zero means between them."
pb["bronze"][0]["misconceptions"] = [
    mc("positive_root_only", 1,
       "You kept only the positive root. \\((-3)^2 = 9\\) as well, so \\(x^2 < 9\\) "
       "holds for every value from \\(-3\\) up to 3: \\(-3 < x < 3\\).",
       "picks x<3 (option idx1)"),
    mc("region_flipped", 3,
       "That is the OUTSIDE region. A U-shape is below zero BETWEEN its roots, so "
       "\\(x^2 - 9 < 0\\) gives \\(-3 < x < 3\\).",
       "picks x<-3 or x>3 (idx3)"),
]
pb["bronze"][1]["hint"] = "Roots are 2 and −2. Greater than zero means outside them."
pb["bronze"][1]["misconceptions"] = [
    mc("region_flipped", 1,
       "That is the BETWEEN region. For \\(> 0\\) the U-shape is above zero OUTSIDE "
       "the roots, so the answer is \\(x < -2\\) or \\(x > 2\\).",
       "picks -2<x<2 (idx1)"),
    mc("positive_root_only", 2,
       "You kept only the positive side. The curve is also above zero for very "
       "negative \\(x\\), so include \\(x < -2\\): \\(x < -2\\) or \\(x > 2\\).",
       "picks x>2 (idx2)"),
]
pb["bronze"][2]["hint"] = "Roots are 1 and −1. Less than or equal means between, ends included."
pb["bronze"][2]["misconceptions"] = [
    mc("positive_root_only", 1,
       "The negative root counts too: \\((-1)^2 = 1\\). So \\(x^2 \\le 1\\) gives "
       "\\(-1 \\le x \\le 1\\).",
       "picks x<=1 (idx1)"),
    mc("region_flipped", 3,
       "That is the outside region. For \\(\\le 0\\) take BETWEEN the roots "
       "(inclusive): \\(-1 \\le x \\le 1\\).",
       "picks outside (idx3)"),
]
pb["bronze"][3]["hint"] = "Roots are 1 and 5. Less than zero means between them."
pb["bronze"][3]["misconceptions"] = [
    mc("region_flipped", 1,
       "That is the OUTSIDE region. A U-shape dips below zero BETWEEN its roots, so "
       "\\((x-1)(x-5) < 0\\) gives \\(1 < x < 5\\).",
       "picks x<1 or x>5 (idx1)"),
]
pb["bronze"][4]["hint"] = "Roots are −3 and 2. Greater than zero means outside them."
pb["bronze"][4]["misconceptions"] = [
    mc("region_flipped", 1,
       "That is the BETWEEN region. For \\(> 0\\) take OUTSIDE the roots: "
       "\\(x < -3\\) or \\(x > 2\\).",
       "picks -3<x<2 (idx1)"),
    mc("one_bracket_only", 3,
       "You solved only one bracket. Both roots matter: the answer is \\(x < -3\\) "
       "or \\(x > 2\\), not just \\(x > -3\\).",
       "picks x>-3 (idx3)"),
]
pb["bronze"][5]["hint"] = "Square-root both sides: roots 5 and −5. Less than zero means between."
pb["bronze"][5]["misconceptions"] = [
    mc("positive_root_only", 1,
       "The negative root counts: \\((-5)^2 = 25\\). So \\(x^2 < 25\\) gives "
       "\\(-5 < x < 5\\).",
       "picks x<5 (idx1)"),
    mc("no_square_root", 2,
       "You forgot to square-root. \\(x^2 < 25\\) means \\(x\\) lies between "
       "\\(-5\\) and 5, not between \\(-25\\) and 25.",
       "picks x<25 (idx2)"),
]
pb["bronze"][6]["hint"] = "Roots are 4 and −2. Greater than or equal means outside, ends included."
pb["bronze"][6]["misconceptions"] = [
    mc("region_flipped", 1,
       "That is the BETWEEN region. For \\(\\ge 0\\) take OUTSIDE the roots "
       "(inclusive): \\(x \\le -2\\) or \\(x \\ge 4\\).",
       "picks between (idx1)"),
]
pb["bronze"][7]["hint"] = "Roots are 6 and −6. Greater than or equal means outside them."
pb["bronze"][7]["misconceptions"] = [
    mc("region_flipped", 1,
       "That is the BETWEEN region. For \\(\\ge 0\\) the U-shape is above zero "
       "OUTSIDE the roots: \\(x \\le -6\\) or \\(x \\ge 6\\).",
       "picks between (idx1)"),
    mc("positive_root_only", 2,
       "The negative side counts too: very negative \\(x\\) also gives a big square. "
       "Include \\(x \\le -6\\): \\(x \\le -6\\) or \\(x \\ge 6\\).",
       "picks x>=6 (idx2)"),
]

# silver
pb["silver"][0]["hint"] = "Factorise to (x−2)(x−3). Less than zero means between the roots."
pb["silver"][0]["misconceptions"] = [
    mc("region_flipped", 1,
       "That is the OUTSIDE region. For \\(< 0\\) take BETWEEN the roots: "
       "\\(2 < x < 3\\).",
       "picks x<2 or x>3 (idx1)"),
]
pb["silver"][1]["hint"] = "Factorise to (x+3)(x−2). Greater than zero means outside the roots."
pb["silver"][1]["misconceptions"] = [
    mc("region_flipped", 1,
       "That is the BETWEEN region. For \\(> 0\\) take OUTSIDE the roots: "
       "\\(x < -3\\) or \\(x > 2\\).",
       "picks -3<x<2 (idx1)"),
]
pb["silver"][2]["hint"] = "Factorise to (x−2)(x−5). Less than or equal means between, ends included."
pb["silver"][2]["misconceptions"] = [
    mc("region_flipped", 1,
       "That is the outside region. For \\(\\le 0\\) take BETWEEN the roots: "
       "\\(2 \\le x \\le 5\\).",
       "picks outside (idx1)"),
    mc("lost_equality", 3,
       "The sign is \\(\\le\\), so the roots are included. Use \\(\\le\\), giving "
       "\\(2 \\le x \\le 5\\), not the strict \\(2 < x < 5\\).",
       "picks strict (idx3)"),
]
pb["silver"][3]["hint"] = "Factorise to (x−6)(x+2). Greater than or equal means outside, ends included."
pb["silver"][3]["misconceptions"] = [
    mc("region_flipped", 1,
       "That is the BETWEEN region. For \\(\\ge 0\\) take OUTSIDE the roots "
       "(inclusive): \\(x \\le -2\\) or \\(x \\ge 6\\).",
       "picks between (idx1)"),
]
pb["silver"][5]["hint"] = "Factorise to (2x+1)(x−3). Roots are −½ and 3; between for less-than-or-equal."
pb["silver"][5]["misconceptions"] = [
    mc("region_flipped", 1,
       "That is the outside region. For \\(\\le 0\\) take BETWEEN the roots: "
       "\\(-\\tfrac{1}{2} \\le x \\le 3\\).",
       "picks outside (idx1)"),
    mc("wrong_roots", 3,
       "Check the roots. \\((2x+1)(x-3)=0\\) gives \\(x = -\\tfrac{1}{2}\\) and "
       "\\(x = 3\\), not \\(-3\\) and \\(\\tfrac{1}{2}\\).",
       "picks -3<=x<=1/2 (idx3)"),
]
pb["silver"][6]["hint"] = "Factorise to (x+4)(x−1). Greater than zero means outside the roots."
pb["silver"][6]["misconceptions"] = [
    mc("region_flipped", 1,
       "That is the BETWEEN region. For \\(> 0\\) take OUTSIDE the roots: "
       "\\(x < -4\\) or \\(x > 1\\).",
       "picks -4<x<1 (idx1)"),
]

# gold MC (0..3)
pb["gold"][0]["hint"] = "Multiply by −1 and flip the sign: x²+x−6<0, roots −3 and 2, between them."
pb["gold"][0]["misconceptions"] = [
    mc("sign_not_flipped", 1,
       "When you multiply by \\(-1\\) the inequality flips. \\(6 - x - x^2 > 0\\) "
       "becomes \\(x^2 + x - 6 < 0\\), which is BETWEEN the roots: \\(-3 < x < 2\\).",
       "keeps >0, gives outside (idx1)"),
    mc("root_signs", 3,
       "Check the root signs. \\(x^2 + x - 6 = (x+3)(x-2)\\), so the roots are "
       "\\(-3\\) and 2, giving \\(-3 < x < 2\\).",
       "picks -2<x<3 (idx3)"),
]
pb["gold"][1]["hint"] = "Rearrange to x²−2x−3>0, factorise (x−3)(x+1), outside the roots."
pb["gold"][1]["misconceptions"] = [
    mc("region_flipped", 1,
       "That is the BETWEEN region. \\(x^2 - 2x - 3 > 0\\) is above zero OUTSIDE "
       "the roots: \\(x < -1\\) or \\(x > 3\\).",
       "picks -1<x<3 (idx1)"),
    mc("positive_root_only", 2,
       "The negative side counts too. Include \\(x < -1\\): the full answer is "
       "\\(x < -1\\) or \\(x > 3\\).",
       "picks x>3 (idx2)"),
]
pb["gold"][2]["hint"] = "No real roots means discriminant below zero: k²−36<0, so between −6 and 6."
pb["gold"][2]["misconceptions"] = [
    mc("discriminant_wrong_way", 1,
       "No real roots needs \\(b^2 - 4ac < 0\\), so \\(k^2 - 36 < 0\\), which is "
       "\\(-6 < k < 6\\). The outside region \\(k < -6\\) or \\(k > 6\\) gives two "
       "real roots instead.",
       "uses >0 (idx1)"),
]
pb["gold"][3]["hint"] = "Solve the quadratic to −4≤x≤2, then keep only the part with x>0."
pb["gold"][3]["misconceptions"] = [
    mc("ignored_second_condition", 1,
       "You solved only the quadratic. \\((x+4)(x-2) \\le 0\\) gives "
       "\\(-4 \\le x \\le 2\\), but \\(x > 0\\) then trims it to \\(0 < x \\le 2\\).",
       "picks -4<=x<=2 (idx1)"),
    mc("boundary_strictness", 2,
       "The quadratic uses \\(\\le\\), so \\(x = 2\\) is included. Combined with "
       "\\(x > 0\\) the answer is \\(0 < x \\le 2\\), keeping the 2.",
       "picks 0<x<2 (idx2)"),
]

# ---------------------------------------------------------------------------
# SINGLE-VALUE problems: hints + numeric misconceptions + guided_steps + figure
# ---------------------------------------------------------------------------
# gold[4]: x^2-6x+5<0, roots 1,5, 1<x<5, integers 2,3,4 -> 3
g5 = pb["gold"][4]
assert g5["solutions"] == [3]
g5["hint"] = "Factorise to (x−1)(x−5), giving 1<x<5, then count the whole numbers inside."
g5["display"] = (numberline_svg(0, 6, 1, 5, [2, 3, 4],
    "Number line from 0 to 6 with open circles at 1 and 5 and filled dots at 2, 3, 4")
    + CAP + " Solve \\(x^2 - 6x + 5 < 0\\). How many integer values of \\(x\\) satisfy this?")
g5["misconceptions"] = [
    mc("included_endpoints", 5,
       "\\(x = 1\\) and \\(x = 5\\) make the expression equal 0, not less than 0, so "
       "they are excluded. Only 2, 3 and 4 count, which is 3 values.",
       "counts 1..5 inclusive = 5"),
    mc("gap_width", 4,
       "Do not just subtract the roots. \\(5 - 1 = 4\\) is the gap, but the integers "
       "strictly inside are 2, 3 and 4, so the count is 3.",
       "answers 5-1=4"),
]
g5["guided_steps"] = [
    {"say": "First solve the inequality, then count. Factorise: \\(x^2 - 6x + 5 = (x-1)(x-5)\\)."},
    {"pre": "Smaller root: x = ", "post": "", "answer": 1,
     "hint": "Set the bracket (x − 1) to zero."},
    {"pre": "Larger root: x = ", "post": "", "answer": 5,
     "hint": "Set the bracket (x − 5) to zero."},
    {"say": "Positive \\(x^2\\), so a U-shape. It is below zero BETWEEN the roots: "
            "\\(1 < x < 5\\). Both signs are strict, so 1 and 5 are NOT included."},
    {"phase": "substitute", "pre": "Smallest whole number above 1: x = ", "post": "",
     "answer": 2, "hint": "1 is excluded, so start at the next integer up."},
    {"pre": "Largest whole number below 5: x = ", "post": "", "answer": 4,
     "hint": "5 is excluded, so stop at the integer just below it."},
    {"pre": "Count the integers 2, 3, 4. How many? ", "post": "", "answer": 3,
     "done": "Three integer values, so the answer is 3.",
     "hint": "Count them one by one: 2, 3, 4."},
]

# silver[4]: x^2-3x-10<0, roots 5,-2, -2<x<5, integers -1,0,1,2,3,4 -> 6
s5 = pb["silver"][4]
assert s5["solutions"] == [6]
s5["hint"] = "Factorise to (x−5)(x+2), giving −2<x<5, then count the whole numbers inside."
s5["display"] = (numberline_svg(-3, 6, -2, 5, [-1, 0, 1, 2, 3, 4],
    "Number line from -3 to 6 with open circles at -2 and 5 and filled dots at -1, 0, 1, 2, 3, 4")
    + CAP + " Find the integer values of \\(x\\) satisfying \\(x^2 - 3x - 10 < 0\\). How many are there?")
s5["misconceptions"] = [
    mc("included_endpoints", 8,
       "The ends \\(x = -2\\) and \\(x = 5\\) give 0, not less than 0, so they are "
       "excluded. Counting them makes 8; the correct count is 6.",
       "counts -2..5 inclusive = 8"),
    mc("forgot_zero", 5,
       "Do not skip 0. The integers are \\(-1, 0, 1, 2, 3, 4\\), and 0 is one of "
       "them, giving 6 values.",
       "misses 0 -> 5"),
]
s5["guided_steps"] = [
    {"say": "Solve first, then count. Factorise: \\(x^2 - 3x - 10 = (x-5)(x+2)\\)."},
    {"pre": "Smaller root: x = ", "post": "", "answer": -2,
     "hint": "Set the bracket (x + 2) to zero: x = −2."},
    {"pre": "Larger root: x = ", "post": "", "answer": 5,
     "hint": "Set the bracket (x − 5) to zero."},
    {"say": "U-shape below zero between the roots: \\(-2 < x < 5\\), ends excluded."},
    {"phase": "substitute", "pre": "Smallest whole number above −2: x = ", "post": "",
     "answer": -1, "hint": "−2 is excluded, so start at −1."},
    {"pre": "Largest whole number below 5: x = ", "post": "", "answer": 4,
     "hint": "5 is excluded, so stop at 4."},
    {"pre": "Count −1, 0, 1, 2, 3, 4. How many? ", "post": "", "answer": 6,
     "done": "Six integer values, so the answer is 6.",
     "hint": "Count each, and do not forget 0."},
]

# ---------------------------------------------------------------------------
# TIER GUIDES
# ---------------------------------------------------------------------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: reading a squared inequality",
        "steps": [
            "Bronze inequalities compare a square to a number, like \\(x^2 < 9\\), or arrive already factorised.",
            "Find the two edges (roots). For \\(x^2 = 9\\) the roots are \\(x = 3\\) and \\(x = -3\\): every square has a positive AND a negative root.",
            "For \\(< 0\\) the answer is BETWEEN the roots; for \\(> 0\\) it is OUTSIDE them. Use \\(\\le\\) or \\(\\ge\\) only when the line sits under the sign.",
        ],
        "example": {
            "question": "Solve \\(x^2 - 4 < 0\\)",
            "steps": [
                {"label": "Roots", "content": "<p>\\(x^2 = 4\\), so \\(x = 2\\) or \\(x = -2\\)</p>"},
                {"label": "Region", "content": "<p>\\(< 0\\) means between the roots</p>"},
                {"label": "Check", "content": "<p>\\(0^2 - 4 = -4 < 0\\), and 0 is between</p>"},
                {"label": "Answer", "content": "<p>\\(-2 < x < 2\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: factorise, then choose the region",
        "steps": [
            "Silver quadratics need factorising first, like \\(x^2 - 5x + 6\\): two numbers that multiply to the constant and add to the middle coefficient.",
            "The brackets give the roots. \\((x-2)(x-3)\\) has roots \\(x = 2\\) and \\(x = 3\\).",
            "Below zero between the roots, above zero outside. Match the sign to pick the region, keeping \\(\\le\\) or \\(\\ge\\) if equality is allowed.",
        ],
        "example": {
            "question": "Solve \\(x^2 - 7x + 10 \\le 0\\)",
            "steps": [
                {"label": "Factorise", "content": "<p>\\((x-2)(x-5) \\le 0\\)</p>"},
                {"label": "Roots", "content": "<p>\\(x = 2\\) and \\(x = 5\\)</p>"},
                {"label": "Check", "content": "<p>\\(3^2 - 7(3) + 10 = -2 \\le 0\\), and 3 is between</p>"},
                {"label": "Answer", "content": "<p>\\(2 \\le x \\le 5\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: rearrange, then interpret",
        "steps": [
            "Gold problems hide the standard form. Rearrange so one side is 0 first, and if you multiply by \\(-1\\) flip the inequality sign.",
            "Some add a follow-up: count the integers in the region, combine with another condition, or use the discriminant \\(b^2 - 4ac\\) for the number of roots.",
            "Finish by reading the region from the U-shape, then answer exactly what was asked.",
        ],
        "example": {
            "question": "Solve \\(x^2 - 2x > 3\\)",
            "steps": [
                {"label": "Rearrange", "content": "<p>\\(x^2 - 2x - 3 > 0\\)</p>"},
                {"label": "Factorise", "content": "<p>\\((x-3)(x+1) > 0\\), roots 3 and \\(-1\\)</p>"},
                {"label": "Check", "content": "<p>\\(4^2 - 2(4) = 8 > 3\\), and 4 is outside</p>"},
                {"label": "Answer", "content": "<p>\\(x < -1\\) or \\(x > 3\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# GUIDED: opener + teach walks (with figures)
# ---------------------------------------------------------------------------
opener = {
    "label": "Before any algebra",
    "display": "Which numbers, when squared, come out less than 9?",
    "steps": [
        {"say": "No algebra yet, just arithmetic. We want \\(x^2 < 9\\).",
         "pre": "What is 2 × 2? ", "post": "", "answer": 4,
         "hint": "Two twos."},
        {"say": "4 is less than 9, so \\(x = 2\\) works. Now the sneaky one.",
         "pre": "What is (−2) × (−2)? ", "post": "", "answer": 4,
         "hint": "A negative times a negative is positive."},
        {"say": "Also 4, also under 9, so \\(x = -2\\) works too. Negatives count. Now the edge.",
         "pre": "What is 3 × 3? ", "post": "", "answer": 9,
         "hint": "Three threes."},
        {"say": "9 is not less than 9, so \\(x = 3\\) is the edge, not inside. Everything from "
                "\\(-3\\) up to 3 works: \\(-3 < x < 3\\). That is the whole trick: the answer to "
                "\\(x^2 < 9\\) sits BETWEEN the two edges \\(-3\\) and 3, negatives included. "
                "Those edges are the roots."},
    ],
}

# Bronze teach: x^2-16<0, roots -4,4, between
bt_fig = parabola_svg(-4, 4, -6, 6, "between", False,
    "U-shaped parabola crossing the x-axis at -4 and 4 with the region between them shaded")
teach_bronze = {
    "display": bt_fig + CAP + " Solve \\(x^2 - 16 < 0\\)",
    "label": "Together: your first one",
    "steps": [
        {"say": "Find the edges first. \\(x^2 - 16 = 0\\) means \\(x^2 = 16\\).",
         "pre": "One root is x = ", "post": "", "answer": 4, "hint": "The square root of 16."},
        {"pre": "The other root (the negative one) is x = ", "post": "", "answer": -4,
         "hint": "A square has two roots, one negative."},
        {"say": "Positive \\(x^2\\) draws a U. It dips BELOW zero between the roots, so the "
                "answer looks like \\(-4 < x < 4\\). Let us confirm.",
         "pre": "Test x = 0: 0² − 16 = ", "post": "", "answer": -16,
         "hint": "Square 0, then subtract 16."},
        {"say": "−16 is below zero, and 0 sits between −4 and 4, so the inside region is right.",
         "pre": "Now the edge x = 4: 4² − 16 = ", "post": "", "answer": 0,
         "done": "Zero, not below zero, so 4 is excluded. Strict < gives −4 < x < 4.",
         "hint": "Square 4, then subtract 16."},
    ],
}

# Silver teach: x^2-x-12>0, roots -3,4, outside
st_fig = parabola_svg(-3, 4, -5, 6, "outside", False,
    "U-shaped parabola crossing the x-axis at -3 and 4 with the two outside regions shaded")
teach_silver = {
    "display": st_fig + CAP + " Solve \\(x^2 - x - 12 > 0\\)",
    "label": "Together: the silver move",
    "steps": [
        {"say": "Factorise \\(x^2 - x - 12\\). Two numbers multiplying to −12 and adding to −1 "
                "are −4 and +3, so it is \\((x-4)(x+3)\\).",
         "pre": "Larger root, from (x − 4) = 0: x = ", "post": "", "answer": 4,
         "hint": "What makes the first bracket zero?"},
        {"pre": "Smaller root, from (x + 3) = 0: x = ", "post": "", "answer": -3,
         "hint": "What makes the second bracket zero?"},
        {"say": "This is \\(> 0\\). A U-shape is ABOVE zero OUTSIDE the roots, so the answer looks "
                "like \\(x < -3\\) or \\(x > 4\\). Let us test a point outside.",
         "pre": "Test x = 5: 5² − 5 − 12 = ", "post": "", "answer": 8,
         "hint": "25 − 5 − 12."},
        {"say": "8 is above zero and 5 is outside (past 4), so that region is in.",
         "pre": "Test x = 0 (inside): 0² − 0 − 12 = ", "post": "", "answer": -12,
         "done": "−12 is below zero, so 0 is NOT a solution. Outside the roots is right: x < −3 or x > 4.",
         "hint": "Just the constant, −12."},
    ],
}

# Gold teach: 2x^2+3x-5<=0, roots -2.5,1, between inclusive
gt_fig = parabola_svg(-2.5, 1, -4, 3, "between", True,
    "U-shaped parabola crossing the x-axis at -2.5 and 1 with the region between them shaded")
teach_gold = {
    "display": gt_fig + CAP + " Solve \\(2x^2 + 3x - 5 \\le 0\\)",
    "label": "Together: the gold move",
    "steps": [
        {"say": "Factorise \\(2x^2 + 3x - 5\\). It splits as \\((2x+5)(x-1)\\).",
         "pre": "From (x − 1) = 0, one root x = ", "post": "", "answer": 1,
         "hint": "What makes (x − 1) zero?"},
        {"say": "The other bracket gives \\(2x + 5 = 0\\), so \\(2x = -5\\).",
         "pre": "That root is x = ", "post": "", "answer": -2.5,
         "hint": "Divide −5 by 2."},
        {"say": "\\(\\le 0\\) with a U-shape means BETWEEN the roots, ends included: "
                "\\(-2.5 \\le x \\le 1\\). Test a point inside.",
         "pre": "Test x = 0: 2(0)² + 3(0) − 5 = ", "post": "", "answer": -5,
         "hint": "Only the constant survives."},
        {"say": "−5 is below zero and 0 is between the roots, so the inside region is right.",
         "pre": "Now the edge x = 1: 2(1)² + 3(1) − 5 = ", "post": "", "answer": 0,
         "done": "2 + 3 − 5 = 0. On the boundary, and ≤ allows equality, so 1 is included.",
         "hint": "2 + 3 − 5."},
    ],
}

pd["guided"] = {
    "opener": opener,
    "teach": {"bronze": teach_bronze, "silver": teach_silver, "gold": teach_gold},
}

# ---------------------------------------------------------------------------
# ARITHMETIC SELF-VERIFICATION
# ---------------------------------------------------------------------------
def q(a, b, c, x):  # a x^2 + b x + c
    return a * x * x + b * x + c
# teach box checks
assert q(1, 0, -16, 4) == 0 and q(1, 0, -16, 0) == -16
assert q(1, -1, -12, 5) == 8 and q(1, -1, -12, 0) == -12
assert q(2, 3, -5, 0) == -5 and q(2, 3, -5, 1) == 0
assert (2 * (-2.5) + 5) == 0 and (-2.5 - 1) < 0
# single_value counts
assert len([i for i in range(-100, 100) if q(1, -6, 5, i) < 0]) == 3
assert len([i for i in range(-100, 100) if q(1, -3, -10, i) < 0]) == 6
# opener
assert 2 * 2 == 4 and (-2) * (-2) == 4 and 3 * 3 == 9

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT)
print("arithmetic self-checks passed")
