# -*- coding: utf-8 -*-
import json, io

MINUS = "−"  # unicode minus

live = json.load(io.open("_live_algebra-L07.json", encoding="utf-8"))

def num(n):
    if n < 0:
        return MINUS + str(abs(n))
    return str(n)

def bracket(p):
    if p < 0:
        return "x " + MINUS + " " + str(abs(p))
    return "x + " + str(p)

def factor_pair(b, c):
    for p in range(-40, 41):
        q = b - p
        if p * q == c and p <= q:
            return p, q
    raise ValueError((b, c))

def check_pre_monic(sol, b, c):
    s = "Check x = " + num(sol) + ": (" + num(sol) + ")²"
    if b > 0:
        s += " + " + str(b) + "×(" + num(sol) + ")"
    elif b < 0:
        s += " " + MINUS + " " + str(abs(b)) + "×(" + num(sol) + ")"
    if c > 0:
        s += " + " + str(c)
    elif c < 0:
        s += " " + MINUS + " " + str(abs(c))
    s += " = "
    return s

def monic_steps(display, b, c, sols):
    p, q = factor_pair(b, c)
    s1, s2 = -p, -q
    assert set([s1, s2]) == set(sols), (display, s1, s2, sols)
    cstr = num(c); bstr = num(b)
    core = display.replace("\\(", "").replace("\\)", "")
    steps = []
    steps.append({"say": "Solve \\(" + core + "\\) by finding two numbers that multiply to \\(" +
                  cstr + "\\) and add to \\(" + bstr + "\\)."})
    steps.append({"pre": "The smaller of the two numbers is ", "post": "", "answer": p,
                  "hint": "List pairs that multiply to " + num(c) + "; take the pair that adds to " + num(b) + ", then the smaller one."})
    steps.append({"pre": "The larger of the two numbers is ", "post": "", "answer": q,
                  "hint": "The two numbers add to " + num(b) + ", and the smaller was " + num(p) + "."})
    steps.append({"say": "So it factorises to \\((" + bracket(p) + ")(" + bracket(q) + ") = 0\\). Each bracket can be zero."})
    steps.append({"phase": "substitute",
                  "pre": "First bracket zero: " + bracket(p) + " = 0, so x = ", "post": "", "answer": s1,
                  "hint": ("Move " + num(p) + " across; the sign flips.") if p != 0 else "x = 0."})
    steps.append({"phase": "substitute",
                  "pre": "Second bracket zero: " + bracket(q) + " = 0, so x = ", "post": "", "answer": s2,
                  "hint": "Move " + num(q) + " across; the sign flips."})
    steps.append({"pre": check_pre_monic(s1, b, c), "post": "", "answer": 0,
                  "hint": "Work out the arithmetic; a correct root gives 0.",
                  "done": "It gives 0, so x = " + num(s1) + " is right, and x = " + num(s2) + " checks the same way."})
    return steps, (p, q), (s1, s2)

def merged_misconception(sols, p, q):
    expect = [-s for s in sols]
    if set(expect) == set(sols):
        return None
    b1 = bracket(p); b2 = bracket(q)
    msg = ("Those are the numbers that go inside the brackets, not the answers. "
           "Set each bracket to zero: " + b1 + " = 0 gives x = " + num(-p) + ", and " +
           b2 + " = 0 gives x = " + num(-q) + ". The solutions are " + num(-p) + " and " + num(-q) + ".")
    return {"pattern": "factor_pair_not_solved", "check": "negated", "expect": expect,
            "message": msg,
            "note": "Both the sign-flip slip and reporting the raw factor pair land on the negation of the solutions; merged (was duplicate sign_swap + factors_not_solutions)."}

def one_correct_misconception():
    return {"pattern": "one_correct", "check": "partial", "expect": None,
            "message": "One of your two answers is right, but the other is not. Recheck your number pair: they must multiply to the constant AND add to the coefficient of x.",
            "note": "No single determinate wrong answer; fires only via the partial check."}

bronze_meta = [
    ("\\(x^2 + 5x + 6 = 0\\)", 5, 6, [-2, -3]),
    ("\\(x^2 + 7x + 10 = 0\\)", 7, 10, [-2, -5]),
    ("\\(x^2 + 8x + 15 = 0\\)", 8, 15, [-3, -5]),
    ("\\(x^2 + 6x + 8 = 0\\)", 6, 8, [-2, -4]),
    ("\\(x^2 + 9x + 14 = 0\\)", 9, 14, [-2, -7]),
    ("\\(x^2 + 10x + 21 = 0\\)", 10, 21, [-3, -7]),
    ("\\(x^2 + 11x + 24 = 0\\)", 11, 24, [-3, -8]),
    ("\\(x^2 + 3x + 2 = 0\\)", 3, 2, [-1, -2]),
]
bronze_hint = "Find two numbers that multiply to the last number and add to the middle number, then flip their signs."

silver_meta = [
    ("\\(x^2 - 3x - 10 = 0\\)", -3, -10, [5, -2]),
    ("\\(x^2 + 2x - 15 = 0\\)", 2, -15, [3, -5]),
    ("\\(x^2 - x - 12 = 0\\)", -1, -12, [4, -3]),
    ("\\(x^2 - 7x + 12 = 0\\)", -7, 12, [3, 4]),
    ("\\(x^2 - 2x - 8 = 0\\)", -2, -8, [4, -2]),
    ("\\(x^2 + x - 20 = 0\\)", 1, -20, [4, -5]),
    ("\\(x^2 - 9 = 0\\)", 0, -9, [3, -3]),
]
def silver_hint(b):
    if b == 0:
        return "There is no middle term, so it is a difference of two squares: split into (x + 3)(x - 3)."
    return "Find two numbers that multiply to the constant and add to the coefficient of x; one of them will be negative."

problem_bank = {}
problem_bank["bronze_description"] = live["problem_bank"]["bronze_description"]
problem_bank["silver_description"] = live["problem_bank"]["silver_description"]
problem_bank["gold_description"] = live["problem_bank"]["gold_description"]

bronze = []
for disp, b, c, sols in bronze_meta:
    steps, (p, q), _ = monic_steps(disp, b, c, sols)
    mis = []
    m = merged_misconception(sols, p, q)
    if m: mis.append(m)
    mis.append(one_correct_misconception())
    bronze.append({"display": disp, "solutions": sols, "calculator": False,
                   "input_type": "two_solutions", "hint": bronze_hint,
                   "misconceptions": mis, "guided_steps": steps})

silver = []
for disp, b, c, sols in silver_meta:
    steps, (p, q), _ = monic_steps(disp, b, c, sols)
    mis = []
    m = merged_misconception(sols, p, q)
    if m: mis.append(m)
    mis.append(one_correct_misconception())
    silver.append({"display": disp, "solutions": sols, "calculator": False,
                   "input_type": "two_solutions", "hint": silver_hint(b),
                   "misconceptions": mis, "guided_steps": steps})

def gold_rearrange(moved_steps, rearranged_say, b, c, sols):
    p, q = factor_pair(b, c)
    s1, s2 = -p, -q
    assert set([s1, s2]) == set(sols), (s1, s2, sols)
    steps = [{"say": "First rearrange so one side is 0. Move every term on the right across to the left; each one changes sign."}]
    steps.extend(moved_steps)
    steps.append({"say": rearranged_say})
    steps.append({"pre": "The smaller of the two numbers is ", "post": "", "answer": p,
                  "hint": "Two numbers multiply to " + num(c) + " and add to " + num(b) + "; take the smaller."})
    steps.append({"pre": "The larger of the two numbers is ", "post": "", "answer": q,
                  "hint": "They add to " + num(b) + ", and the smaller was " + num(p) + "."})
    steps.append({"say": "So \\((" + bracket(p) + ")(" + bracket(q) + ") = 0\\)."})
    steps.append({"phase": "substitute", "pre": "First bracket zero: " + bracket(p) + " = 0, so x = ", "post": "",
                  "answer": s1, "hint": "Move " + num(p) + " across; the sign flips."})
    steps.append({"phase": "substitute", "pre": "Second bracket zero: " + bracket(q) + " = 0, so x = ", "post": "",
                  "answer": s2, "hint": "Move " + num(q) + " across; the sign flips."})
    steps.append({"pre": check_pre_monic(s1, b, c), "post": "", "answer": 0,
                  "hint": "Work out the arithmetic; a correct root gives 0.",
                  "done": "It gives 0, so x = " + num(s1) + " is right, and x = " + num(s2) + " checks the same way."})
    return steps

gold = []

g0_moved = [
    {"pre": "The 5x on the right moves left and becomes ", "post": "x", "answer": -5,
     "hint": "It is +5x on the right, so subtracting it from both sides makes it −5x on the left."},
    {"pre": "The −6 on the right moves left and becomes +", "post": "", "answer": 6,
     "hint": "Adding 6 to both sides turns the −6 into +6 on the left."},
]
gold.append({"display": "\\(x^2 = 5x - 6\\)", "solutions": [2, 3], "calculator": False,
             "input_type": "two_solutions", "hint": "Rearrange to = 0 first, then factorise.",
             "misconceptions": None,
             "guided_steps": gold_rearrange(g0_moved,
                "So \\(x^2 − 5x + 6 = 0\\). Now two numbers multiply to \\(6\\) and add to \\(−5\\).",
                -5, 6, [2, 3])})

g1_steps = [
    {"say": "Both terms share a common factor. Take out the largest one, which is \\(2x\\)."},
    {"pre": "Divide the second term by 2x: 6x ÷ 2x = ", "post": "", "answer": 3,
     "hint": "6 ÷ 2 = 3, and x ÷ x = 1."},
    {"say": "So \\(2x(x + 3) = 0\\). Either factor can be zero."},
    {"phase": "substitute", "pre": "First factor: 2x = 0, so x = ", "post": "", "answer": 0,
     "hint": "2 times x is 0 only when x itself is 0."},
    {"phase": "substitute", "pre": "Second factor: x + 3 = 0, so x = ", "post": "", "answer": -3,
     "hint": "Subtract 3 from both sides."},
    {"pre": "Check x = −3: 2×(−3)² + 6×(−3) = ", "post": "", "answer": 0,
     "hint": "2×9 = 18, and 6×(−3) = −18.",
     "done": "18 − 18 = 0, so x = −3 is right, and x = 0 also gives 0."},
]
gold.append({"display": "\\(2x^2 + 6x = 0\\)", "solutions": [0, -3], "calculator": False,
             "input_type": "two_solutions", "hint": "Both terms share a common factor; take it out first.",
             "misconceptions": None, "guided_steps": g1_steps})

g2_moved = [
    {"pre": "The 5 on the right moves left and becomes ", "post": "", "answer": -5,
     "hint": "Subtracting 5 from both sides turns +5 into −5 on the left."},
]
gold.append({"display": "\\(x^2 - 4x = 5\\)", "solutions": [5, -1], "calculator": False,
             "input_type": "two_solutions", "hint": "Rearrange to = 0 first, then factorise.",
             "misconceptions": None,
             "guided_steps": gold_rearrange(g2_moved,
                "So \\(x^2 − 4x − 5 = 0\\). Now two numbers multiply to \\(−5\\) and add to \\(−4\\).",
                -4, -5, [5, -1])})

g3_steps = [
    {"say": "Both terms share a common factor, which is \\(3x\\). Take it out."},
    {"pre": "Divide the second term by 3x: 12x ÷ 3x = ", "post": "", "answer": 4,
     "hint": "12 ÷ 3 = 4, and x ÷ x = 1."},
    {"say": "So \\(3x(x − 4) = 0\\). Either factor can be zero."},
    {"phase": "substitute", "pre": "First factor: 3x = 0, so x = ", "post": "", "answer": 0,
     "hint": "3 times x is 0 only when x itself is 0."},
    {"phase": "substitute", "pre": "Second factor: x − 4 = 0, so x = ", "post": "", "answer": 4,
     "hint": "Add 4 to both sides."},
    {"pre": "Check x = 4: 3×(4)² − 12×(4) = ", "post": "", "answer": 0,
     "hint": "3×16 = 48, and 12×4 = 48.",
     "done": "48 − 48 = 0, so x = 4 is right, and x = 0 also gives 0."},
]
gold.append({"display": "\\(3x^2 - 12x = 0\\)", "solutions": [0, 4], "calculator": False,
             "input_type": "two_solutions", "hint": "Both terms share a common factor; take it out first.",
             "misconceptions": None, "guided_steps": g3_steps})

g4_moved = [
    {"pre": "The 6 on the right moves left and becomes ", "post": "", "answer": -6,
     "hint": "Subtracting 6 from both sides turns +6 into −6 on the left."},
]
gold.append({"display": "\\(x^2 + x = 6\\)", "solutions": [2, -3], "calculator": False,
             "input_type": "two_solutions", "hint": "Rearrange to = 0 first, then factorise.",
             "misconceptions": None,
             "guided_steps": gold_rearrange(g4_moved,
                "So \\(x^2 + x − 6 = 0\\). Now two numbers multiply to \\(−6\\) and add to \\(1\\).",
                1, -6, [2, -3])})

def gold_mis(sols):
    expect = [-s for s in sols]
    if set(expect) == set(sols):
        return [one_correct_misconception()]
    p, q = expect[0], expect[1]
    b1 = bracket(p); b2 = bracket(q)
    msg = ("Those are the numbers inside the brackets, not the answers. "
           "Set each bracket to zero: " + b1 + " = 0 gives x = " + num(-p) + ", and " +
           b2 + " = 0 gives x = " + num(-q) + ". The solutions are " + num(-p) + " and " + num(-q) + ".")
    return [{"pattern": "factor_pair_not_solved", "check": "negated", "expect": expect, "message": msg,
             "note": "Merged sign-flip + raw-factor-pair error; both land on the negation of the solutions."},
            one_correct_misconception()]

for g in gold:
    g["misconceptions"] = gold_mis(g["solutions"])

problem_bank["bronze"] = bronze
problem_bank["silver"] = silver
problem_bank["gold"] = gold

tier_guides = {
    "bronze": {
        "title": "Bronze: quadratics already in the form \\(x^2 + bx + c = 0\\)",
        "steps": [
            "Find two numbers that <strong>multiply to \\(c\\)</strong> (the last number) and <strong>add to \\(b\\)</strong> (the middle number).",
            "Write them in brackets: \\((x + p)(x + q) = 0\\).",
            "Set each bracket to zero. \\(x + p = 0\\) gives \\(x = -p\\), so both signs flip."
        ],
        "example": {"question": "Solve \\(x^2 + 7x + 12 = 0\\)", "steps": [
            {"label": "Find the pair", "content": "<p>Two numbers multiply to \\(12\\) and add to \\(7\\): that is \\(3\\) and \\(4\\).</p>"},
            {"label": "Factorise", "content": "<p>\\((x + 3)(x + 4) = 0\\)</p>"},
            {"label": "Check", "content": "<p>Put \\(x = -3\\) into \\(x^2 + 7x + 12\\): \\(9 - 21 + 12 = 0\\) ✓</p>"},
            {"label": "Answer", "content": "<p><strong>\\(x = -3\\) or \\(x = -4\\)</strong></p>", "isAnswer": True, "is_answer": True}
        ]}
    },
    "silver": {
        "title": "Silver: negative terms and difference of two squares",
        "steps": [
            "Same routine, but now \\(c\\) can be negative, so one bracket number is negative. Two numbers multiply to \\(c\\) and add to \\(b\\).",
            "A <strong>difference of two squares</strong> like \\(x^2 - 9\\) has no middle term: it splits into \\((x + 3)(x - 3)\\).",
            "Set each bracket to zero, and keep a close eye on the signs."
        ],
        "example": {"question": "Solve \\(x^2 - 2x - 15 = 0\\)", "steps": [
            {"label": "Find the pair", "content": "<p>Two numbers multiply to \\(-15\\) and add to \\(-2\\): that is \\(3\\) and \\(-5\\).</p>"},
            {"label": "Factorise", "content": "<p>\\((x + 3)(x - 5) = 0\\)</p>"},
            {"label": "Check", "content": "<p>Put \\(x = 5\\) into \\(x^2 - 2x - 15\\): \\(25 - 10 - 15 = 0\\) ✓</p>"},
            {"label": "Answer", "content": "<p><strong>\\(x = -3\\) or \\(x = 5\\)</strong></p>", "isAnswer": True, "is_answer": True}
        ]}
    },
    "gold": {
        "title": "Gold: rearrange or take out a common factor first",
        "steps": [
            "If the equation is not \\(= 0\\), move every term to one side first. Each term changes sign as it crosses.",
            "If both terms share a factor, like \\(3x^2 - 12x\\), take it out: \\(3x(x - 4) = 0\\).",
            "Then finish with the zero product rule, exactly as before."
        ],
        "example": {"question": "Solve \\(x^2 = 4x + 12\\)", "steps": [
            {"label": "Rearrange", "content": "<p>Move everything left: \\(x^2 - 4x - 12 = 0\\).</p>"},
            {"label": "Factorise", "content": "<p>Multiply to \\(-12\\), add to \\(-4\\): \\(2\\) and \\(-6\\), so \\((x + 2)(x - 6) = 0\\).</p>"},
            {"label": "Check", "content": "<p>Put \\(x = 6\\): \\(36 - 24 - 12 = 0\\) ✓</p>"},
            {"label": "Answer", "content": "<p><strong>\\(x = -2\\) or \\(x = 6\\)</strong></p>", "isAnswer": True, "is_answer": True}
        ]}
    }
}

opener = {"steps": [
    {"say": "Two quick puzzles, no algebra needed. First: I am thinking of two numbers that <strong>multiply to 12</strong> and <strong>add to 7</strong>."},
    {"pre": "The smaller of my two numbers is ", "post": "", "answer": 3,
     "hint": "Try pairs that multiply to 12: 1 and 12, 2 and 6, 3 and 4. Which pair adds to 7?"},
    {"say": "The pair is 3 and 4. Finding two numbers that multiply and add like that <strong>is</strong> factorising. For \\(x^2 + 7x + 12\\) you look for two numbers that multiply to 12 (the last number) and add to 7 (the middle number): 3 and 4. So it becomes \\((x + 3)(x + 4)\\)."},
    {"say": "Now the second half. If two numbers multiply together to give <strong>0</strong>, at least one of them must be 0. Suppose 5 times something equals 0."},
    {"pre": "5 × (something) = 0, so that something must be ", "post": "", "answer": 0,
     "hint": "5 times what gives 0?"},
    {"say": "That is the <strong>zero product rule</strong>. Once you have \\((x + 3)(x + 4) = 0\\), one bracket must be 0: \\(x + 3 = 0\\) gives \\(x = -3\\), and \\(x + 4 = 0\\) gives \\(x = -4\\). Finding the pair and using the zero rule are the whole method."}
]}

teach = {
    "bronze": {"display": "Solve \\(x^2 + 9x + 20 = 0\\)", "steps": [
        {"say": "It is already \\(= 0\\). Look for two numbers that multiply to 20 and add to 9."},
        {"pre": "The smaller number is ", "post": "", "answer": 4, "hint": "Pairs of 20: 1 and 20, 2 and 10, 4 and 5. Which adds to 9?"},
        {"pre": "The larger number is ", "post": "", "answer": 5, "hint": "9 − 4."},
        {"say": "So \\((x + 4)(x + 5) = 0\\). Each bracket can be zero."},
        {"pre": "x + 4 = 0, so x = ", "post": "", "answer": -4, "hint": "Subtract 4 from both sides; the sign flips.",
         "done": "The sign flips: a plus in the bracket becomes a minus in the answer. That is the whole point."},
        {"pre": "x + 5 = 0, so x = ", "post": "", "answer": -5, "hint": "Subtract 5 from both sides."},
        {"pre": "Check x = −4: (−4)² + 9×(−4) + 20 = ", "post": "", "answer": 0, "hint": "16 − 36 + 20.",
         "done": "It gives 0, so x = −4 works, and x = −5 works the same way."}
    ]},
    "silver": {"display": "Solve \\(x^2 - 2x - 15 = 0\\)", "steps": [
        {"say": "The constant is negative, so one of the two numbers is negative. They multiply to \\(−15\\) and add to \\(−2\\)."},
        {"pre": "The negative number is ", "post": "", "answer": -5, "hint": "Try 3 and −5: 3×(−5) = −15 and 3 + (−5) = −2."},
        {"pre": "The positive number is ", "post": "", "answer": 3, "hint": "−2 − (−5) = 3.",
         "done": "One negative, one positive: that is the new move when the constant is negative."},
        {"say": "So \\((x + 3)(x - 5) = 0\\)."},
        {"pre": "x + 3 = 0, so x = ", "post": "", "answer": -3, "hint": "Subtract 3 from both sides."},
        {"pre": "x − 5 = 0, so x = ", "post": "", "answer": 5, "hint": "Add 5 to both sides."},
        {"pre": "Check x = 5: (5)² − 2×(5) − 15 = ", "post": "", "answer": 0, "hint": "25 − 10 − 15.",
         "done": "It gives 0, so x = 5 works, and x = −3 works the same way."}
    ]},
    "gold": {"display": "Solve \\(x^2 = 4x + 12\\)", "steps": [
        {"say": "The new move: get everything on one side first. Move 4x and 12 to the left, each changing sign."},
        {"pre": "The middle term becomes ", "post": "x", "answer": -4, "hint": "+4x on the right becomes −4x on the left."},
        {"pre": "The constant becomes ", "post": "", "answer": -12, "hint": "+12 on the right becomes −12 on the left.",
         "done": "Everything is now on one side. That rearrangement is the whole new move."},
        {"say": "So \\(x^2 − 4x − 12 = 0\\). Now the usual routine: two numbers multiply to \\(−12\\) and add to \\(−4\\)."},
        {"pre": "The negative number is ", "post": "", "answer": -6, "hint": "−6 and 2: −6×2 = −12 and −6 + 2 = −4."},
        {"pre": "The positive number is ", "post": "", "answer": 2, "hint": "−4 − (−6) = 2."},
        {"say": "So \\((x - 6)(x + 2) = 0\\)."},
        {"pre": "x − 6 = 0, so x = ", "post": "", "answer": 6, "hint": "Add 6 to both sides."},
        {"pre": "x + 2 = 0, so x = ", "post": "", "answer": -2, "hint": "Subtract 2 from both sides."},
        {"pre": "Check x = 6: (6)² − 4×(6) − 12 = ", "post": "", "answer": 0, "hint": "36 − 24 − 12.",
         "done": "It gives 0, so x = 6 works, and x = −2 works the same way."}
    ]}
}

guided = {"opener": opener, "teach": teach}

method_card = {
    "title": "How to Solve Quadratics by Factorising",
    "steps": [
        "Write the equation in the form \\(ax^2 + bx + c = 0\\)",
        "Find two numbers that multiply to \\(c\\) and add to \\(b\\)",
        "Write as \\((x + p)(x + q) = 0\\)",
        "Set each bracket equal to zero and solve for \\(x\\)"
    ],
    "content": ("<p>A <strong>quadratic</strong> looks like \\(ax^2 + bx + c = 0\\). To solve by factorising, "
                "find two numbers that <strong>multiply to \\(c\\)</strong> and <strong>add to \\(b\\)</strong>, "
                "then write the two brackets.</p>"
                "<p>Use the <strong>zero product rule</strong>: if two things multiply to 0, one of them must be 0. "
                "Set each bracket to 0 and solve. Setting \\(x + 3 = 0\\) gives \\(x = -3\\), so the sign flips.</p>"
                "<p>If the equation is not already \\(= 0\\), rearrange first. If both terms share a factor "
                "(like \\(2x^2 + 6x\\)), take it out first.</p>"),
    "example": ("<p><strong>Solve</strong> \\(x^2 + 5x + 6 = 0\\).</p>"
                "<p>Two numbers multiply to 6 and add to 5: that is 2 and 3, so \\((x + 2)(x + 3) = 0\\). "
                "Setting each bracket to zero gives \\(x = -2\\) or \\(x = -3\\).</p>")
}

# worked_examples preserved, but strip em dashes from labels (style gate; dash reads as minus)
worked_examples = live["worked_examples"]
def strip_em(obj):
    if isinstance(obj, dict):
        return {k: strip_em(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip_em(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace(" — ", ": ").replace("—", ": ")
    return obj
worked_examples = strip_em(worked_examples)

out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "problem_bank": problem_bank,
    "tier_guides": tier_guides,
    "guided": guided,
    "related_videos": live["related_videos"],
    "worked_examples": worked_examples,
}

json.dump(out, io.open("lesson_algebra-L07.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written lesson_algebra-L07.json")

for disp, b, c, sols in bronze_meta + silver_meta:
    p, q = factor_pair(b, c)
    assert p + q == b and p * q == c
    assert set([-p, -q]) == set(sols)
print("all monic factorisations verified")
