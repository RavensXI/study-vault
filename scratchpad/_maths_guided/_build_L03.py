# -*- coding: utf-8 -*-
"""Build guided-learning practice_data for graphs-L03 (Quadratic Graphs)."""
import json, io

live = json.load(io.open("_live_graphs-L03.json", encoding="utf-8"))
pb = live["problem_bank"]

# ---------- helpers ----------
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {}
    if say is not None:
        d["say"] = say
    d["pre"] = pre
    d["post"] = post
    d["answer"] = answer
    d["hint"] = hint
    if done is not None:
        d["done"] = done
    if phase is not None:
        d["phase"] = phase
    return d

def say(text):
    return {"say": text}

# ================= METHOD CARD (slim) =================
live["method_card"] = {
    "title": "Quadratic Graphs",
    "steps": [
        "To find a y-value, substitute the x-value: square it first, then multiply and add or subtract.",
        "Roots are the x-axis crossings: set y = 0 and factorise, or read them off the graph.",
        "The turning point (vertex) is at \\(x = \\frac{-b}{2a}\\); substitute back for its y-value.",
        "The y-intercept is the constant c. If a > 0 the curve opens upward (U); if a < 0, downward (∩)."
    ],
    "content": "<p>A <strong>quadratic</strong> \\(y = ax^2 + bx + c\\) draws a U-shaped <strong>parabola</strong>, or ∩-shaped when \\(a < 0\\). The <strong>roots</strong> are where it crosses the x-axis (\\(y = 0\\)); there are 0, 1 or 2. The <strong>turning point</strong> is the minimum or maximum, and the <strong>y-intercept</strong> is \\(c\\). To plot, substitute x-values into a table and join the points with a smooth curve, never a ruler.</p>",
    "example": "<p><strong>Plot \\(y = x^2 - 4\\).</strong> At \\(x = 0\\), \\(y = -4\\) (the turning point). Setting \\(y = 0\\): \\(x^2 = 4\\), so the roots are \\(x = -2\\) and \\(x = 2\\).</p>"
}

# ================= TIER DESCRIPTIONS =================
pb["bronze_description"] = "Substitute an x-value into a quadratic to find y, and read basic features like the y-intercept and which way the curve opens."
pb["silver_description"] = "Find the roots by setting y = 0 and factorising, and locate the turning point using x = −b ÷ (2a)."
pb["gold_description"] = "Work backwards from a turning point or roots, and handle quadratics where a is not 1 or is negative."

# ================= HINTS =================
hints = {
    ("bronze", 0): "Square the 3 first, then add 2.",
    ("bronze", 1): "Square the −2 to get +4, then subtract 5.",
    ("bronze", 2): "The y-intercept is the constant term; put x = 0.",
    ("bronze", 3): "The turning point of y = x squared is its lowest point, at the origin.",
    ("bronze", 4): "Work out 4 squared, then subtract 9.",
    ("bronze", 5): "A negative number in front of x squared flips the U upside down.",
    ("bronze", 6): "Square the −3 to get +9, then add 1.",
    ("bronze", 7): "Square the 4 first, then multiply by 2.",
    ("silver", 0): "Set y = 0, so x squared = 4, then take both square roots.",
    ("silver", 1): "Find two numbers that multiply to 6 and add to −5.",
    ("silver", 2): "Find the turning-point x with −b over 2a, then substitute back for y.",
    ("silver", 3): "Set y = 0, so x squared = 9, giving both square roots.",
    ("silver", 4): "Factorise; a perfect square gives one repeated root.",
    ("silver", 5): "Use x = −b over 2a with a = 1 and b = −4.",
    ("silver", 6): "Find two numbers that multiply to −12 and add to 1.",
    ("gold", 0): "Find the turning-point x with −b over 2a, then substitute back for y.",
    ("gold", 1): "The turning point is at x = −b over 2, so solve for b.",
    ("gold", 2): "a is negative; use −b over 2a to find x, then substitute for the maximum y.",
    ("gold", 3): "Build y = (x − 1)(x − 5) and read the constant term.",
    ("gold", 4): "Use −b over 2a but remember a = 2, not 1.",
}
for (t, i), h in hints.items():
    pb[t][i]["hint"] = h

# ================= MISCONCEPTION FIXES (audit) =================
# bronze[0] substitution_error -> real error path
pb["bronze"][0]["misconceptions"] = [{
    "pattern": "squaring_error",
    "check": "common",
    "expect": 8,
    "message": "Did you work out 3² as 3 × 2 = 6? Squaring means 3 × 3 = 9, so y = 9 + 2 = 11.",
    "note": "Slip: 3x2=6 then 6+2=8."
}]
# bronze[3] MC confused_root_tp -> plugging_in_one (x=1 gives (1,1) = option index 3)
pb["bronze"][3]["misconceptions"] = [{
    "pattern": "plugging_in_one",
    "check": "common",
    "expect": 3,
    "message": "Did you substitute x = 1? That gives the point (1, 1), which sits on the curve but is not the lowest point. The turning point is the minimum: put x = 0 to get (0, 0).",
    "note": "Option index 3 is (1,1); plugging x=1 into y=x^2 gives y=1."
}]

# ================= BRONZE[4]: replace degenerate problem (x=0 -> x=4) =================
pb["bronze"][4]["display"] = "For \\(y = x^2 - 9\\), find \\(y\\) when \\(x = 4\\)."
pb["bronze"][4]["solutions"] = [7]
pb["bronze"][4]["misconceptions"] = [{
    "pattern": "squaring_error",
    "check": "common",
    "expect": -1,
    "message": "Did you work out 4² as 4 × 2 = 8? Squaring means 4 × 4 = 16, so y = 16 − 9 = 7.",
    "note": "Slip: 4x2=8 then 8-9=-1."
}]

# silver[3]: duplicate answer [-2,2] clashes with silver[0]; retune to -x^2+9 -> [-3,3]
pb["silver"][3]["display"] = "The graph of \\(y = -x^2 + 9\\) has roots at which x-values?"
pb["silver"][3]["solutions"] = [-3, 3]
pb["silver"][3]["misconceptions"] = [{
    "pattern": "sign_error",
    "check": "common",
    "expect": None,
    "message": "Set y = 0: −x² + 9 = 0 → x² = 9 → x = ±3.",
    "note": "A sign slip gives x^2 = 9 (same) or x^2 = -9 (no real root); no single determinate wrong integer."
}]

# silver[2] confused_root_tp message rewrite (keep expect=1, x-not-y error)
pb["silver"][2]["misconceptions"] = [{
    "pattern": "gave_x_not_y",
    "check": "common",
    "expect": 1,
    "message": "You found the turning-point x = 1, but the question asks for the y-value there. Substitute back: y = 1 − 2 − 8 = −9.",
    "note": "Student stops at x-coordinate x=1 instead of substituting for y."
}]

# ================= GUIDED_STEPS per bank problem =================
GS = {}

# ---- BRONZE ----
GS[("bronze", 0)] = [  # y=x^2+2, x=3 -> 11
    box("3² = 3 × 3 = ", 9, "Multiply 3 by itself.",
        say="Substitute x = 3. Square first, then add 2."),
    box("Add the constant: 9 + 2 = ", 11, "Add 2 to your squared value.", phase="substitute"),
    box("Symmetry check: the vertex is at x = 0, so x = −3 gives the same y. (−3)² + 2 = ", 11,
        "A negative squared is positive: (−3)² = 9.", phase="substitute",
        done="Same y at x = −3, exactly as a parabola should. y = 11."),
]
GS[("bronze", 1)] = [  # y=x^2-5, x=-2 -> -1
    box("(−2)² = (−2) × (−2) = ", 4, "A negative times a negative is positive.",
        say="Substitute x = −2. Square the negative first."),
    box("Subtract 5: 4 − 5 = ", -1, "4 take away 5 goes below zero.", phase="substitute"),
    box("Symmetry check: x = +2 gives the same y. 2² − 5 = ", -1,
        "2² = 4, then 4 − 5.", phase="substitute",
        done="Matches, so y = −1."),
]
GS[("bronze", 2)] = [  # y-intercept of x^2+3x-7 -> -7
    box("The x² term when x = 0: 0² = ", 0, "Zero squared is zero.",
        say="The y-intercept is where the curve meets the y-axis, so x = 0. Substitute x = 0."),
    box("The 3x term: 3 × 0 = ", 0, "Anything times zero is zero.", phase="substitute"),
    box("So y = 0 + 0 − 7 = ", -7, "Only the constant is left.", phase="substitute"),
    box("Quick check: the y-intercept is always the constant c. Read c from y = x² + 3x − 7: c = ", -7,
        "The number with no x attached.", phase="substitute",
        done="Both routes give −7."),
]
GS[("bronze", 4)] = [  # y=x^2-9, x=4 -> 7
    box("4² = 4 × 4 = ", 16, "Multiply 4 by itself.",
        say="Substitute x = 4. Square first, then subtract 9."),
    box("Subtract 9: 16 − 9 = ", 7, "Take 9 from your squared value.", phase="substitute"),
    box("Symmetry check: x = −4 gives the same y. (−4)² − 9 = ", 7,
        "(−4)² = 16, then 16 − 9.", phase="substitute",
        done="Matches, so y = 7."),
]
GS[("bronze", 6)] = [  # y=x^2+1, x=-3 -> 10
    box("(−3)² = (−3) × (−3) = ", 9, "A negative times a negative is positive.",
        say="Substitute x = −3. Square the negative first."),
    box("Add 1: 9 + 1 = ", 10, "Add 1 to your squared value.", phase="substitute"),
    box("Symmetry check: x = +3 gives the same y. 3² + 1 = ", 10,
        "3² = 9, then 9 + 1.", phase="substitute",
        done="Matches, so y = 10."),
]
GS[("bronze", 7)] = [  # y=2x^2, x=4 -> 32
    box("Square x first: 4² = ", 16, "Multiply 4 by itself before touching the 2.",
        say="Substitute x = 4. Square FIRST, then multiply by 2 (order matters)."),
    box("Now multiply by 2: 2 × 16 = ", 32, "Double your squared value.", phase="substitute"),
    box("Symmetry check: x = −4 gives the same y. 2 × (−4)² = 2 × 16 = ", 32,
        "(−4)² = 16, then times 2.", phase="substitute",
        done="Matches, so y = 32."),
]

# ---- SILVER ----
GS[("silver", 0)] = [  # roots of x^2-4 -> -2, 2
    box("x² = 4, so x is a square root of 4. Positive root: ", 2, "What number times itself is 4?",
        say="Roots are where y = 0. So x² − 4 = 0, giving x² = 4."),
    box("The other root is the negative one: x = ", -2, "The negative number that squares to 4.",
        phase="substitute"),
    box("Check x = 2: 2² − 4 = ", 0, "Square 2, then subtract 4.", phase="substitute",
        done="Zero confirms x = 2 is a root; x = −2 too by symmetry."),
]
GS[("silver", 1)] = [  # roots of x^2-5x+6 -> 2, 3
    box("Two numbers multiply to +6 and add to −5: they are −2 and −3. Product: (−2) × (−3) = ", 6,
        "Two negatives multiply to a positive.",
        say="Set y = 0 and factorise. Find two numbers that multiply to +6 and add to −5."),
    box("First root, from (x − 2) = 0: x = ", 2, "What makes x − 2 equal zero?", phase="substitute"),
    box("Second root, from (x − 3) = 0: x = ", 3, "What makes x − 3 equal zero?", phase="substitute"),
    box("Check: the roots should add to −b = 5. 2 + 3 = ", 5, "Add your two roots.",
        phase="substitute", done="Sum is 5, matching −b = 5. Roots are 2 and 3."),
]
GS[("silver", 2)] = [  # turning point y-value of x^2-2x-8 -> -9
    box("x = 2 ÷ 2 = ", 1, "Divide by 2.",
        say="Turning-point x first: x = −b ÷ (2a) = −(−2) ÷ (2 × 1) = 2 ÷ 2."),
    box("Substitute x = 1: the square term 1² = ", 1, "1 times itself.", phase="substitute"),
    box("Now y = 1 − 2(1) − 8 = 1 − 2 − 8 = ", -9, "Work left to right: 1 − 2 = −1, then −1 − 8.",
        phase="substitute"),
    box("Check via the roots: (x − 4)(x + 2) gives roots 4 and −2; midpoint (4 + (−2)) ÷ 2 = ", 1,
        "Add the roots, then halve.", phase="substitute",
        done="Midpoint 1 matches the turning-point x. a = 1 > 0, a minimum, so y = −9."),
]
GS[("silver", 3)] = [  # roots of -x^2+9 -> -3, 3
    box("x² = 9. Positive root: x = ", 3, "What number times itself is 9?",
        say="Set y = 0: −x² + 9 = 0, so x² = 9."),
    box("Negative root: x = ", -3, "The negative number that squares to 9.", phase="substitute"),
    box("Check x = 3: −(3²) + 9 = −9 + 9 = ", 0, "Square 3, make it negative, then add 9.",
        phase="substitute", done="Zero, so x = 3 is a root; x = −3 by symmetry."),
]
GS[("silver", 4)] = [  # how many roots of x^2+6x+9 -> 1
    box("Two numbers multiply to 9 and add to 6: both are 3, so (x + 3)(x + 3). The root from x + 3 = 0: x = ",
        -3, "What makes x + 3 equal zero?",
        say="Factorise x² + 6x + 9. Find two numbers that multiply to 9 and add to 6."),
    box("Because both brackets are identical, there is only ONE distinct root. Number of roots: ", 1,
        "How many different x-values did you get?", phase="substitute"),
    box("Check: substitute x = −3 into x² + 6x + 9: 9 − 18 + 9 = ", 0, "The curve just touches the axis.",
        phase="substitute", done="It touches at exactly one point, so 1 root."),
]
GS[("silver", 5)] = [  # x-coord turning point of x^2-4x -> 2
    box("The formula needs −b: −(−4) = ", 4, "Two minuses make a plus.",
        say="Use x = −b ÷ (2a). Here a = 1 and b = −4."),
    box("Divide by 2a = 2: x = 4 ÷ 2 = ", 2, "Halve your value.", phase="substitute"),
    box("Check with the roots: x(x − 4) = 0 gives roots 0 and 4; midpoint (0 + 4) ÷ 2 = ", 2,
        "Add the roots, then halve.", phase="substitute",
        done="Midpoint 2 matches the turning-point x."),
]
GS[("silver", 6)] = [  # roots of x^2+x-12 -> -4, 3
    box("Two numbers multiply to −12 and add to +1: they are +4 and −3. Product: 4 × (−3) = ", -12,
        "A positive times a negative is negative.",
        say="Set y = 0 and factorise. Find two numbers that multiply to −12 and add to +1."),
    box("First root, from (x + 4) = 0: x = ", -4, "What makes x + 4 equal zero?", phase="substitute"),
    box("Second root, from (x − 3) = 0: x = ", 3, "What makes x − 3 equal zero?", phase="substitute"),
    box("Check: the roots should add to −b = −1. (−4) + 3 = ", -1, "Add your two roots.",
        phase="substitute", done="Sum is −1, matching −b = −1. Roots are −4 and 3."),
]

# ---- GOLD ----
GS[("gold", 0)] = [  # turning point y-coord of x^2-8x+12 -> -4
    box("x = 8 ÷ 2 = ", 4, "Divide by 2.",
        say="x-coordinate first: x = −b ÷ (2a) = −(−8) ÷ (2 × 1) = 8 ÷ 2."),
    box("Substitute x = 4: square it, 4² = ", 16, "4 times itself.", phase="substitute"),
    box("Now y = 16 − 8(4) + 12 = 16 − 32 + 12 = ", -4, "16 − 32 = −16, then −16 + 12.",
        phase="substitute"),
    box("Check via the roots: x² − 8x + 12 = (x − 2)(x − 6), roots 2 and 6; midpoint (2 + 6) ÷ 2 = ", 4,
        "Add the roots, then halve.", phase="substitute",
        done="Midpoint 4 matches the turning-point x, and y = −4 is the minimum."),
]
GS[("gold", 1)] = [  # turning point at x=-3 of x^2+bx+10 -> b=6
    box("Set up −3 = −b ÷ 2 and multiply both sides by 2: −b = −3 × 2 = ", -6,
        "Multiply the −3 by 2.",
        say="The turning point is at x = −b ÷ (2a). Here a = 1, so x = −b ÷ 2. We know x = −3."),
    box("So −b = −6, which means b = ", 6, "Change the sign of −6.", phase="substitute"),
    box("Check: with b = 6, x = −b ÷ (2a) = −6 ÷ 2 = ", -3, "Halve −6.", phase="substitute",
        done="That gives x = −3, matching the question. So b = 6."),
]
GS[("gold", 2)] = [  # max y of -x^2+6x-5 -> 4
    box("Denominator 2 × (−1) = −2, so x = −6 ÷ (−2) = ", 3,
        "A negative divided by a negative is positive.",
        say="a = −1 (opens downward, so a maximum). x = −b ÷ (2a) = −6 ÷ (2 × (−1))."),
    box("Substitute x = 3: square first, 3² = ", 9, "3 times itself.", phase="substitute"),
    box("y = −(9) + 6(3) − 5 = −9 + 18 − 5 = ", 4, "−9 + 18 = 9, then 9 − 5.", phase="substitute"),
    box("Check it is a maximum: a = −1 < 0, so the ∩ curve peaks here. Confirm 18 − 9 − 5 = ", 4,
        "Same three numbers, added in a different order.", phase="substitute",
        done="Same value, so the maximum y is 4."),
]
GS[("gold", 3)] = [  # roots 1 and 5, find c -> 5
    box("Expand (x − 1)(x − 5). The x terms: −5x − x = ", -6, "Add the two x terms.", post="x",
        say="A quadratic with roots 1 and 5 is y = (x − 1)(x − 5). Expand to read off c."),
    box("The constant term is (−1) × (−5) = ", 5, "Two negatives multiply to a positive. This is c.",
        phase="substitute"),
    box("Check x = 5 is a root: (5 − 1)(5 − 5) = 4 × 0 = ", 0, "Anything times zero is zero.",
        phase="substitute", done="Zero at x = 5 confirms a root, so c = 5."),
]
GS[("gold", 4)] = [  # x-coord turning point of 2x^2-12x+10 -> 3
    box("−b = −(−12) = ", 12, "Two minuses make a plus.",
        say="Use x = −b ÷ (2a). Careful: a = 2, not 1, and b = −12."),
    box("Denominator 2a = 2 × 2 = ", 4, "Double the a value.", phase="substitute"),
    box("x = 12 ÷ 4 = ", 3, "Divide.", phase="substitute"),
    box("Check with the roots: 2x² − 12x + 10 = 2(x − 1)(x − 5), roots 1 and 5; midpoint (1 + 5) ÷ 2 = ", 3,
        "Add the roots, then halve.", phase="substitute",
        done="Midpoint 3 matches. Using a = 1 by mistake would give 6."),
]

for (t, i), steps in GS.items():
    pb[t][i]["guided_steps"] = steps

# ================= TIER GUIDES =================
live["tier_guides"] = {
    "bronze": {
        "title": "Bronze: Substituting and reading a parabola",
        "steps": [
            "To find y, replace every x with the number given, then work it out. <strong>Square first</strong>, then multiply and add or subtract.",
            "Watch negatives: \\((-3)^2 = 9\\), because a negative times a negative is positive.",
            "The <strong>y-intercept</strong> is the constant c (put x = 0). If the number in front of \\(x^2\\) is positive the curve opens upward (U); if negative, downward (∩)."
        ],
        "example": {
            "question": "For \\(y = x^2 - 3\\), find y when x = −2.",
            "steps": [
                {"label": "Square x first", "content": "<p>\\((-2)^2 = 4\\)</p>"},
                {"label": "Subtract 3", "content": "<p>\\(4 - 3 = 1\\)</p>"},
                {"label": "Check", "content": "<p>A negative squared is positive, so \\(4 - 3 = 1\\) is right.</p>"},
                {"label": "Answer", "content": "<p>\\(y = 1\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: Roots and turning points",
        "steps": [
            "<strong>Roots</strong> are where the curve meets the x-axis, so set \\(y = 0\\) and solve. Factorise \\(x^2 + bx + c\\) into two brackets; each bracket gives a root.",
            "The <strong>turning point</strong> sits halfway between the roots. Its x-value is \\(x = \\frac{-b}{2a}\\). Substitute that x back in to get the y-value.",
            "Signs matter: the roots of \\((x - 2)(x - 3)\\) are \\(x = 2\\) and \\(x = 3\\), the numbers that make each bracket zero."
        ],
        "example": {
            "question": "Find the roots of \\(y = x^2 - x - 6\\).",
            "steps": [
                {"label": "Set y = 0", "content": "<p>\\(x^2 - x - 6 = 0\\)</p>"},
                {"label": "Factorise", "content": "<p>\\((x - 3)(x + 2) = 0\\)</p>"},
                {"label": "Solve each bracket", "content": "<p>\\(x = 3\\) or \\(x = -2\\)</p>"},
                {"label": "Check", "content": "<p>Product \\((-2)(3) = -6\\) matches c, and \\(-2 + 3 = 1\\) matches \\(-b\\). Correct.</p>"},
                {"label": "Answer", "content": "<p>Roots: \\(x = -2\\) and \\(x = 3\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: Working backwards and harder curves",
        "steps": [
            "Given a turning-point x-value, use \\(x = \\frac{-b}{2a}\\) to find a missing b, or to handle \\(a \\neq 1\\). Rearrange it like any equation.",
            "Given the roots, build the quadratic: \\((x - r_1)(x - r_2)\\) expands to give b and c. The constant c is the product of the roots.",
            "When \\(a < 0\\) the parabola opens downward, so the turning point is a <strong>maximum</strong>. The vertex formula still works."
        ],
        "example": {
            "question": "For \\(y = x^2 - 6x + 5\\), find the turning point.",
            "steps": [
                {"label": "x-coordinate", "content": "<p>\\(x = \\frac{-b}{2a} = \\frac{6}{2} = 3\\)</p>"},
                {"label": "Substitute back", "content": "<p>\\(y = 9 - 18 + 5 = -4\\)</p>"},
                {"label": "Check", "content": "<p>The roots are \\(x = 1\\) and \\(x = 5\\); their midpoint is 3, confirming the x-value.</p>"},
                {"label": "Answer", "content": "<p>Turning point \\((3, -4)\\), a minimum</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ================= GUIDED (opener + teach) =================
live["guided"] = {
    "opener": {
        "label": "Before any algebra",
        "display": "A ball is thrown up. Its height in metres:<br>after 0s: 0 m<br>after 1s: 5 m<br>after 2s: 8 m<br>after 3s: 9 m<br>after 4s: 8 m<br>after 5s: 5 m<br>after 6s: 0 m",
        "steps": [
            box("It leaves the ground at 0 seconds. After how many seconds does it hit the ground again? ",
                6, "Find the second time the height is back to 0 metres.", post=" seconds",
                say="A ball is thrown straight up. The table shows its height each second. No formulas needed, just read it."),
            box("When is the ball highest? After ", 3, "Find the row with the biggest height.",
                post=" seconds",
                say="Those two moments when the height is 0, at 0 and 6 seconds, are the <strong>roots</strong>: where the graph crosses zero."),
            box("And how high does it get at that point? ", 9, "Read the height at 3 seconds.",
                post=" metres"),
            say("The very top of the flight is the <strong>turning point</strong>, here a maximum of 9 m. A curve like this has equation \\(y = ax^2 + bx + c\\). Everything in this lesson is finding those two things: the <strong>roots</strong> (where it crosses the axis) and the <strong>turning point</strong> (where it turns).")
        ]
    },
    "teach": {
        "bronze": {
            "display": "For \\(y = x^2 + 4\\), find y when x = 5.",
            "label": "Together: your first one",
            "steps": [
                box("Square x first: 5² = ", 25, "5 times itself.",
                    say="Substitute x = 5. Square first, then add 4."),
                box("Add the constant: 25 + 4 = ", 29, "Add 4 to your squared value."),
                box("Symmetry check: x = −5 gives the same y. (−5)² + 4 = ", 29,
                    "(−5)² = 25, then add 4.",
                    done="Matches, because a parabola is symmetric about its vertex."),
                box("And the y-intercept (put x = 0): 0² + 4 = ", 4, "Zero squared, then add 4.",
                    done="The +4 is the y-intercept, and squaring makes the U shape.")
            ]
        },
        "silver": {
            "display": "Find the roots of \\(y = x^2 - 7x + 10\\).",
            "label": "Together: the silver move",
            "steps": [
                box("Two numbers multiply to +10 and add to −7: they are −2 and −5. Product: (−2) × (−5) = ",
                    10, "Two negatives multiply to a positive.",
                    say="Set y = 0 and factorise. Find two numbers that multiply to +10 and add to −7."),
                box("Check the sum: (−2) + (−5) = ", -7, "Add the two numbers; it should match −b."),
                box("First root, from (x − 2) = 0: x = ", 2, "What makes x − 2 equal zero?"),
                box("Second root, from (x − 5) = 0: x = ", 5, "What makes x − 5 equal zero?"),
                box("Check: substitute x = 2 into x² − 7x + 10: 4 − 14 + 10 = ", 0,
                    "Square 2, then 7 times 2, then add 10.",
                    done="Zero, so x = 2 is a root; likewise x = 5.")
            ]
        },
        "gold": {
            "display": "The turning point of \\(y = x^2 + bx + 7\\) is at \\(x = 2\\). Find b.",
            "label": "Together: the gold move",
            "steps": [
                box("Set 2 = −b ÷ 2 and multiply both sides by 2: −b = 2 × 2 = ", 4, "Multiply 2 by 2.",
                    say="Use x = −b ÷ (2a) with a = 1, so x = −b ÷ 2. We know x = 2."),
                box("So −b = 4, which means b = ", -4, "Change the sign of 4."),
                box("Check the vertex: substitute x = 2 into y = x² − 4x + 7. Square: 2² = ", 4,
                    "2 times itself."),
                box("y = 4 − 8 + 7 = ", 3, "4 − 8 = −4, then −4 + 7.",
                    done="The vertex is (2, 3), and x = −b ÷ 2 = 2 confirms b = −4.")
            ]
        }
    }
}

# ===== Style repair: strip em dashes from preserved worked_examples (hard rule) =====
for we in live.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str):
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")
        if isinstance(st.get("content"), str):
            st["content"] = st["content"].replace(" — ", ", ").replace("—", ",")

with open("lesson_graphs-L03.json", "w", encoding="utf-8") as f:
    json.dump(live, f, ensure_ascii=False, indent=1)
print("written lesson_graphs-L03.json")
