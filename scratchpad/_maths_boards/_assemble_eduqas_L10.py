# -*- coding: utf-8 -*-
import json
from _build_eduqas_L10 import (std_parabola, horizontal, common_factor,
                               circle_divide, hyperbola, factor_latex, quad_latex, bracket)

def mc_signflip(quad_tex, fac_tex, r1, r2):
    return {
        "note": "sign-flipped factorisation of %s" % quad_tex,
        "expect": [-r1, -r2],
        "message": ("Check the signs inside your brackets. \\(%s\\) factorises as \\(%s = 0\\), giving \\(x = %g\\) and \\(x = %g\\). Reversing those signs gives \\(x = %g\\) and \\(x = %g\\), which do not fit the equations."
                    % (quad_tex, fac_tex, r1, r2, -r1, -r2)),
        "pattern": "factor_sign_flip",
    }

def disp(eqs):
    return "Solve %s. Give the two x-values." % eqs

live = json.load(open("_live_eduqas_L10.json", encoding="utf-8"))
pd = {}
pd["topic_links"] = live.get("topic_links", {"prerequisites": []})
pd["related_videos"] = live.get("related_videos", [])
pd["worked_examples"] = live.get("worked_examples", [])

bronze, silver, gold = [], [], []

def add(bank, display, sols, steps, misc, hint):
    bank.append({"hint": hint, "display": display, "solutions": sols,
                 "calculator": False, "input_type": "two_solutions",
                 "guided_steps": steps, "misconceptions": misc})

HINT_STD = "Set the two right-hand sides equal, rearrange to a quadratic equal to zero, then factorise."
HINT_HORIZ = "The line is horizontal: set it equal to the curve, isolate x squared, then take both square roots."
HINT_CIRCLE = "Rearrange the line to make y the subject, substitute into the circle, and expand the bracket in full."
HINT_HYP = "Make y the subject of the line, substitute into xy, expand, then solve the quadratic."

def one_root_only(k):
    return {"expect": None, "pattern": "one_root_only",
            "message": "\\(x^2 = %g\\) has two square roots, \\(x = %g\\) and \\(x = %g\\). Giving only the positive root loses half the answer." % (k, k**0.5, -(k**0.5))}

def divide_by_x(coef):
    return {"expect": None, "pattern": "divide_by_x",
            "message": "When you reach \\(x^2 - %gx = 0\\), factorise as \\(x(x - %g) = 0\\) rather than dividing both sides by x. Dividing by x throws away the solution \\(x = 0\\)." % (coef, coef)}

def sq_bracket(bracket_tex, wrong_tex, extra=""):
    return {"expect": None, "pattern": "square_bracket_error",
            "message": "Expand \\(%s\\) in full; do not write \\(%s\\), or the middle term is lost.%s" % (bracket_tex, wrong_tex, extra)}

# ---- BRONZE ----
s, sol = common_factor(1, 0, 0, 1, "x", "x^2", "1^2")
add(bronze, disp("\\(y = x\\) and \\(y = x^2\\)"), sol, s, [divide_by_x(1)], HINT_STD)

s, sol = common_factor(2, 0, 0, 2, "2x", "x^2", "2^2")
add(bronze, disp("\\(y = 2x\\) and \\(y = x^2\\)"), sol, s, [divide_by_x(2)], HINT_STD)

s, sol = horizontal(3, -1, 4, 2, "x^2 - 1", "2^2 - 1")
add(bronze, disp("\\(y = 3\\) and \\(y = x^2 - 1\\)"), sol, s, [one_root_only(4)], HINT_HORIZ)

s, sol, _ = std_parabola(1, 2, 0, 0, 2, -1, "x + 2", "x^2", "2^2")
add(bronze, disp("\\(y = x + 2\\) and \\(y = x^2\\)"), sol, s,
    [mc_signflip("x^2 - x - 2", "(x - 2)(x + 1)", 2, -1)], HINT_STD)

s, sol = horizontal(10, 1, 9, 3, "x^2 + 1", "3^2 + 1")
add(bronze, disp("\\(y = 10\\) and \\(y = x^2 + 1\\)"), sol, s, [one_root_only(9)], HINT_HORIZ)

s, sol, _ = std_parabola(1, 6, 0, 0, 3, -2, "x + 6", "x^2", "3^2")
add(bronze, disp("\\(y = x + 6\\) and \\(y = x^2\\)"), sol, s,
    [mc_signflip("x^2 - x - 6", "(x - 3)(x + 2)", 3, -2)], HINT_STD)

s, sol, _ = std_parabola(-1, 0, 0, -2, -2, 1, "-x", "x^2 - 2", "(-2)^2 - 2")
add(bronze, disp("\\(y = -x\\) and \\(y = x^2 - 2\\)"), sol, s,
    [mc_signflip("x^2 + x - 2", "(x + 2)(x - 1)", -2, 1)], HINT_STD)

s, sol, _ = std_parabola(4, 0, 0, 3, 1, 3, "4x", "x^2 + 3", "1^2 + 3")
add(bronze, disp("\\(y = 4x\\) and \\(y = x^2 + 3\\)"), sol, s,
    [mc_signflip("x^2 - 4x + 3", "(x - 1)(x - 3)", 1, 3)], HINT_STD)

# ---- SILVER ----
s, sol, _ = std_parabola(1, 3, 0, 1, 2, -1, "x + 3", "x^2 + 1", "2^2 + 1")
add(silver, disp("\\(y = x + 3\\) and \\(y = x^2 + 1\\)"), sol, s,
    [mc_signflip("x^2 - x - 2", "(x - 2)(x + 1)", 2, -1)], HINT_STD)

s, sol, _ = std_parabola(-1, 2, 0, -4, 2, -3, "2 - x", "x^2 - 4", "2^2 - 4")
add(silver, disp("\\(y = 2 - x\\) and \\(y = x^2 - 4\\)"), sol, s,
    [mc_signflip("x^2 + x - 6", "(x - 2)(x + 3)", 2, -3)], HINT_STD)

s, sol, _ = std_parabola(2, -1, -2, 2, 1, 3, "2x - 1", "x^2 - 2x + 2", "1^2 - 2 + 2")
add(silver, disp("\\(y = 2x - 1\\) and \\(y = x^2 - 2x + 2\\)"), sol, s,
    [mc_signflip("x^2 - 4x + 3", "(x - 1)(x - 3)", 1, 3)], HINT_STD)

s, sol, _ = std_parabola(1, 1, -1, -2, 3, -1, "x + 1", "x^2 - x - 2", "3^2 - 3 - 2")
add(silver, disp("\\(y = x + 1\\) and \\(y = x^2 - x - 2\\)"), sol, s,
    [mc_signflip("x^2 - 2x - 3", "(x - 3)(x + 1)", 3, -1)], HINT_STD)

s, sol, _ = std_parabola(3, 0, 0, 2, 1, 2, "3x", "x^2 + 2", "1^2 + 2")
add(silver, disp("\\(y = 3x\\) and \\(y = x^2 + 2\\)"), sol, s,
    [mc_signflip("x^2 - 3x + 2", "(x - 1)(x - 2)", 1, 2)], HINT_STD)

s, sol, _ = std_parabola(1, 0, -4, 4, 1, 4, "x", "x^2 - 4x + 4", "1^2 - 4 + 4")
add(silver, disp("\\(y = x\\) and \\(y = x^2 - 4x + 4\\)"), sol, s,
    [mc_signflip("x^2 - 5x + 4", "(x - 1)(x - 4)", 1, 4)], HINT_STD)

s, sol, _ = std_parabola(-2, 5, 0, -3, 2, -4, "5 - 2x", "x^2 - 3", "2^2 - 3")
add(silver, disp("\\(y = 5 - 2x\\) and \\(y = x^2 - 3\\)"), sol, s,
    [mc_signflip("x^2 + 2x - 8", "(x - 2)(x + 4)", 2, -4)], HINT_STD)

# ---- GOLD ----
g1_steps = [
 {"pre": "The middle term, 2 × 2x × 1, is ", "post": "x", "answer": 4,
  "say": "Substitute \\(y = 2x + 1\\) into the circle: \\(x^2 + (2x + 1)^2 = 10\\). Expand \\((2x + 1)^2 = 4x^2 + 4x + 1\\).",
  "hint": "2 times 2 times 1 is 4."},
 {"pre": "Collect the x² terms: 1 + 4 = ", "post": "x²", "answer": 5,
  "say": "So \\(x^2 + 4x^2 + 4x + 1 = 10\\).",
  "hint": "One x² from the first part, four from the bracket."},
 {"pre": "The constant, 1 − 10, becomes ", "post": "", "answer": -9,
  "say": "That gives \\(5x^2 + 4x + 1 = 10\\). Take 10 across.",
  "hint": "1 minus 10 is negative 9."},
 {"pre": "From x − 1 = 0, the first root is x = ", "post": "", "phase": "substitute", "answer": 1,
  "say": "So \\(5x^2 + 4x - 9 = 0\\). This factorises as \\((5x + 9)(x - 1) = 0\\).",
  "hint": "Set x − 1 = 0."},
 {"pre": "So the second root is x = ", "post": "", "answer": -1.8,
  "say": "From \\(5x + 9 = 0\\), \\(5x = -9\\).",
  "hint": "Negative 9 divided by 5 is negative 1.8."},
 {"pre": "At x = 1: y = ", "post": "", "answer": 3,
  "say": "Each x gets its y from \\(y = 2x + 1\\).",
  "hint": "2 times 1, plus 1."},
 {"pre": "At x = −1.8: y = ", "post": "", "answer": -2.6,
  "hint": "2 times negative 1.8 is negative 3.6, plus 1."},
 {"pre": "Check (1, 3) in the circle: 1² + 3² = ", "post": "", "answer": 10,
  "done": "It equals 10, so (1, 3) is right and (−1.8, −2.6) checks the same way.",
  "hint": "1 + 9."},
]
add(gold, disp("\\(y = 2x + 1\\) and \\(x^2 + y^2 = 10\\)"), [1, -1.8], g1_steps,
    [{"note": "sign-flipped factorisation of 5x^2+4x-9", "expect": [-1, 1.8],
      "message": "\\(5x^2 + 4x - 9 = 0\\) factorises as \\((5x + 9)(x - 1) = 0\\), giving \\(x = 1\\) and \\(x = -1.8\\). Reversing the signs gives \\(x = -1\\) and \\(x = 1.8\\), which do not satisfy the circle.",
      "pattern": "factor_sign_flip"},
     {"expect": None, "pattern": "square_bracket_error",
      "message": "Expand \\((2x + 1)^2\\) in full as \\(4x^2 + 4x + 1\\); squaring the terms separately to \\(4x^2 + 1\\) loses the middle term 4x."}],
    HINT_CIRCLE)

s, sol = circle_divide(-1, 5, 13, 2, 3,
   "Rearrange the line: \\(x + y = 5\\) becomes \\(y = 5 - x\\). Substitute into \\(x^2 + y^2 = 13\\): \\(x^2 + (5 - x)^2 = 13\\).",
   "2 × 5 × (−1)", "(5 - x)^2 = 25 - 10x + x^2", "x^2 + 25 - 10x + x^2 = 13")
add(gold, disp("\\(x + y = 5\\) and \\(x^2 + y^2 = 13\\)"), sol, s,
    [mc_signflip("x^2 - 5x + 6", "(x - 2)(x - 3)", 2, 3),
     sq_bracket("(5 - x)^2 = 25 - 10x + x^2", "25 + x^2")], HINT_CIRCLE)

s, sol = circle_divide(1, -1, 25, 4, -3,
   "Substitute \\(y = x - 1\\) into the circle: \\(x^2 + (x - 1)^2 = 25\\).",
   "2 × x × (−1)", "(x - 1)^2 = x^2 - 2x + 1", "x^2 + x^2 - 2x + 1 = 25")
add(gold, disp("\\(y = x - 1\\) and \\(x^2 + y^2 = 25\\)"), sol, s,
    [mc_signflip("x^2 - x - 12", "(x - 4)(x + 3)", 4, -3),
     sq_bracket("(x - 1)^2 = x^2 - 2x + 1", "x^2 - 1")], HINT_CIRCLE)

s, sol = hyperbola(-1, 3, 2, 1, 2, "", "y = 3 - x", "x(3 - x) = 2")
add(gold, disp("\\(y = 3 - x\\) and \\(xy = 2\\)"), sol, s,
    [mc_signflip("x^2 - 3x + 2", "(x - 1)(x - 2)", 1, 2)], HINT_HYP)

s, sol = hyperbola(-1, 7, 10, 2, 5, "", "y = 7 - x", "x(7 - x) = 10")
add(gold, disp("\\(x + y = 7\\) and \\(xy = 10\\)"), sol, s,
    [mc_signflip("x^2 - 7x + 10", "(x - 2)(x - 5)", 2, 5)], HINT_HYP)

pd["problem_bank"] = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "Both equations are y = something; substitute one into the other and factorise",
    "silver_description": "Rearrange with care after substituting, collecting x-terms from both sides",
    "gold_description": "Circles \\(x^2 + y^2 = r^2\\) or products \\(xy = k\\); substitute and expand in full",
}

# ---- TEACH walks (fresh, NOT in bank) ----
tb_steps, tb_sol, _ = std_parabola(5, 0, 0, 4, 1, 4, "5x", "x^2 + 4", "1^2 + 4")
ts_steps, ts_sol, _ = std_parabola(4, -5, -1, 1, 2, 3, "4x - 5", "x^2 - x + 1", "2^2 - 2 + 1")
tg_steps, tg_sol = circle_divide(-1, 6, 20, 2, 4,
   "Rearrange the line: \\(x + y = 6\\) becomes \\(y = 6 - x\\). Substitute into \\(x^2 + y^2 = 20\\): \\(x^2 + (6 - x)^2 = 20\\).",
   "2 × 6 × (−1)", "(6 - x)^2 = 36 - 12x + x^2", "x^2 + 36 - 12x + x^2 = 20")

pd["guided"] = {
  "opener": {
    "label": "Before any algebra",
    "display": "I square my number and get 12 more than the number itself.",
    "steps": [
      {"pre": "One number that works is ", "post": "", "answer": 4,
       "say": "A guess-the-number puzzle, no algebra needed. I am thinking of a number. When I square it, I get 12 more than the number I started with.",
       "hint": "Try 4: four squared is 16, and 16 is 12 more than 4."},
      {"pre": "The other number is ", "post": "", "answer": -3,
       "say": "Good. There is a second number that also works, and it is negative.",
       "hint": "Try −3: negative three squared is 9, and 9 is 12 more than −3."},
      {"say": "You just solved \\(x^2 = x + 12\\) and found BOTH answers, \\(x = 4\\) and \\(x = -3\\). That is the whole topic: an equation with a square in it usually has TWO answers. In algebra it appears as a line \\(y = x + 12\\) crossing a curve \\(y = x^2\\); they meet at two points, so there are two x-values to find."},
    ],
  },
  "teach": {
    "bronze": {"label": "Together: your first one", "display": "Solve \\(y = 5x\\) and \\(y = x^2 + 4\\)", "steps": tb_steps},
    "silver": {"label": "Together: the silver move", "display": "Solve \\(y = 4x - 5\\) and \\(y = x^2 - x + 1\\)", "steps": ts_steps},
    "gold":   {"label": "Together: the gold move", "display": "Solve \\(x + y = 6\\) and \\(x^2 + y^2 = 20\\)", "steps": tg_steps},
  },
}

pd["tier_guides"] = {
  "bronze": {
    "title": "Bronze: substitute, factorise, two answers",
    "steps": [
      "Both equations are written as <strong>y = …</strong>, so set the two right-hand sides equal to each other.",
      "Move every term to one side to get a quadratic equal to zero, then factorise it.",
      "Each bracket gives one x-value. Put each x back into the linear equation to find its y.",
    ],
    "example": {"question": "Solve \\(y = x + 1\\) and \\(y = x^2 - 1\\)", "steps": [
      {"label": "Set equal", "content": "<p>\\(x + 1 = x^2 - 1\\)</p>"},
      {"label": "Rearrange", "content": "<p>\\(x^2 - x - 2 = 0\\)</p>"},
      {"label": "Factorise", "content": "<p>\\((x - 2)(x + 1) = 0\\), so \\(x = 2\\) or \\(x = -1\\)</p>"},
      {"label": "Find y", "content": "<p>\\(x = 2: y = 3\\). \\(x = -1: y = 0\\).</p>"},
      {"label": "Check", "content": "<p>\\(x = 2\\) in \\(y = x^2 - 1\\): \\(4 - 1 = 3\\) ✓</p>"},
      {"label": "Answer", "content": "<p>\\(x = 2, y = 3\\) and \\(x = -1, y = 0\\)</p>", "isAnswer": True, "is_answer": True},
    ]},
  },
  "silver": {
    "title": "Silver: rearrange with care, then solve",
    "steps": [
      "The linear part may be \\(y = 2x - 3\\) or \\(x + y = 4\\); rearrange it to \\(y = …\\) first if needed.",
      "After substituting, gather x-terms and numbers from <strong>both</strong> sides before you factorise.",
      "Watch every sign as terms cross the equals sign; one slip changes the whole quadratic.",
    ],
    "example": {"question": "Solve \\(y = x + 1\\) and \\(y = x^2 - 4x + 5\\)", "steps": [
      {"label": "Set equal", "content": "<p>\\(x + 1 = x^2 - 4x + 5\\)</p>"},
      {"label": "Rearrange", "content": "<p>\\(x^2 - 5x + 4 = 0\\)</p>"},
      {"label": "Factorise", "content": "<p>\\((x - 1)(x - 4) = 0\\), so \\(x = 1\\) or \\(x = 4\\)</p>"},
      {"label": "Find y", "content": "<p>\\(x = 1: y = 2\\). \\(x = 4: y = 5\\).</p>"},
      {"label": "Check", "content": "<p>\\(x = 4\\) in \\(y = x^2 - 4x + 5\\): \\(16 - 16 + 5 = 5\\) ✓</p>"},
      {"label": "Answer", "content": "<p>\\(x = 1, y = 2\\) and \\(x = 4, y = 5\\)</p>", "isAnswer": True, "is_answer": True},
    ]},
  },
  "gold": {
    "title": "Gold: circles and products",
    "steps": [
      "For a circle \\(x^2 + y^2 = r^2\\), rearrange the line to \\(y = …\\) and substitute, squaring the bracket in full.",
      "\\((a - x)^2 = a^2 - 2ax + x^2\\): never square the two terms separately.",
      "For a product \\(xy = k\\), substitute the line straight in, then rearrange to a quadratic equal to zero.",
    ],
    "example": {"question": "Solve \\(x + y = 7\\) and \\(x^2 + y^2 = 29\\)", "steps": [
      {"label": "Rearrange line", "content": "<p>\\(y = 7 - x\\)</p>"},
      {"label": "Substitute", "content": "<p>\\(x^2 + (7 - x)^2 = 29\\) → \\(2x^2 - 14x + 20 = 0\\)</p>"},
      {"label": "Simplify and factorise", "content": "<p>\\(x^2 - 7x + 10 = 0\\) → \\((x - 2)(x - 5) = 0\\), so \\(x = 2\\) or \\(x = 5\\)</p>"},
      {"label": "Find y", "content": "<p>\\(x = 2: y = 5\\). \\(x = 5: y = 2\\).</p>"},
      {"label": "Check", "content": "<p>\\((2, 5)\\): \\(4 + 25 = 29\\) ✓</p>"},
      {"label": "Answer", "content": "<p>\\(x = 2, y = 5\\) and \\(x = 5, y = 2\\)</p>", "isAnswer": True, "is_answer": True},
    ]},
  },
}

pd["method_card"] = {
  "title": "Simultaneous Equations (One Linear, One Quadratic)",
  "steps": [
    "Rearrange the linear equation to make one letter the subject.",
    "Substitute it into the quadratic, expanding any bracket in full.",
    "Rearrange to a quadratic equal to zero, then factorise or use the formula.",
    "Substitute each x back into the linear equation for its y, and give both pairs.",
  ],
  "content": "<p>When one equation is a straight line and the other is a curve (a quadratic, or a circle \\(x^2 + y^2 = r^2\\)), use <strong>substitution</strong>. The line usually crosses the curve at two points, so expect two pairs of answers.</p><p>Make a letter the subject of the line, substitute it in, and simplify to a quadratic equal to zero. Solve it, then find each matching value from the line. Always give answers as pairs.</p>",
  "example": "<p><strong>Solve</strong> \\(y = x + 1\\) and \\(y = x^2 - 1\\)</p><p>\\(x + 1 = x^2 - 1 \\Rightarrow x^2 - x - 2 = 0 \\Rightarrow (x - 2)(x + 1) = 0\\), so \\(x = 2\\) or \\(x = -1\\). Then \\(y = 3\\) or \\(y = 0\\): the pairs are \\((2, 3)\\) and \\((-1, 0)\\).</p>",
}

json.dump(pd, open("lesson_maths-eduqas_algebra-L10.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ASSEMBLED. bronze", len(bronze), "silver", len(silver), "gold", len(gold))
print("teach sols:", tb_sol, ts_sol, tg_sol)
