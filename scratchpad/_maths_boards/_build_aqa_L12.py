# -*- coding: utf-8 -*-
"""Full guided + diagrams conversion for maths-aqa algebra-L12 (Quadratic
Inequalities & Regions). Fetches fresh, builds, writes shard."""
import json, io, os, urllib.request

LID = "4a7608b6-4426-4d97-97b4-551e408f6951"
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
HDR = {"apikey": KEY, "Authorization": "Bearer " + KEY}
DIR = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards"
EDX = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\lesson_algebra-L12_diagrams.json"


def fetch():
    req = urllib.request.Request(BASE + "?id=eq." + LID + "&select=practice_data", headers=HDR)
    return json.load(urllib.request.urlopen(req))[0]["practice_data"]


pd = fetch()
json.dump(pd, io.open(DIR + r"\_aqa_L12_fresh.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# Reuse the three verified teach walks (with theme-safe SVG sketches) from the
# Edexcel sibling: identical quadratics, identical exam-realism figures.
edx = json.load(io.open(EDX, encoding="utf-8"))
teach = edx["guided"]["teach"]

# ---- opener (fresh: (x-1)(x-4) machine) ----
opener = {"steps": [
    {"say": "Here is a number machine. It multiplies \\((x - 1)\\) by \\((x - 4)\\). We want the values of x that make the answer come out BELOW zero (negative). Let us test a few."},
    {"pre": "Try x = 5. First bracket:  5 - 1 = ", "post": "", "answer": 4, "hint": "5 take away 1."},
    {"say": "The second bracket is \\(5 - 4 = 1\\). Both are positive, so \\(4 \\times 1 = 4\\), above zero. Now slide x down to 2.5, in between 1 and 4."},
    {"pre": "First bracket:  2.5 - 1 = ", "post": "", "answer": 1.5, "hint": "2.5 take away 1."},
    {"pre": "Second bracket:  2.5 - 4 = ", "post": "", "answer": -1.5, "hint": "2.5 is less than 4, so this drops below zero."},
    {"say": "One bracket is positive, the other negative, and a positive times a negative is always NEGATIVE. So the answer is below zero, and that only happens when x sits BETWEEN 1 and 4. That is the whole method for a quadratic inequality: factorise to two brackets, find the two roots, and the expression is below zero between them, above zero outside them. In algebra, \\((x-1)(x-4) < 0\\) has the solution \\(1 < x < 4\\)."},
]}

# ---- tier guides ----
tier_guides = {
 "bronze": {
   "title": "Bronze: reading between or outside the roots",
   "steps": [
     "Find the two roots: square-root a difference of squares (\\(x^2 = k\\) gives \\(x = \\pm\\sqrt{k}\\)), or read them off a factorised pair.",
     "Sketch the U-shape crossing at the roots. For \\(< 0\\) or \\(\\leq 0\\) take BETWEEN the roots; for \\(> 0\\) or \\(\\geq 0\\) take OUTSIDE them.",
     "Write both bounds. A between answer is \\(a < x < b\\); an outside answer is \\(x < a\\) or \\(x > b\\)."
   ],
   "example": {
     "question": "Solve \\(x^2 - 16 < 0\\). Give the upper bound.",
     "steps": [
       {"label": "Find roots", "content": "\\(x^2 = 16\\), so \\(x = \\pm 4\\)."},
       {"label": "Choose the region", "content": "\\(< 0\\) means between the roots: \\(-4 < x < 4\\)."},
       {"label": "Check", "content": "At \\(x = 0\\): \\(0 - 16 = -16\\), below zero. Correct."},
       {"label": "Answer", "content": "The upper bound is \\(4\\).", "isAnswer": True, "is_answer": True}
     ]
   }
 },
 "silver": {
   "title": "Silver: below and above zero, including \\(\\leq\\) and \\(\\geq\\)",
   "steps": [
     "Factorise the three-term quadratic to find the two roots.",
     "For \\(< 0\\) or \\(\\leq 0\\) the curve is below the axis BETWEEN the roots; for \\(> 0\\) or \\(\\geq 0\\) it is above OUTSIDE them.",
     "Use \\(\\leq\\) or \\(\\geq\\) (closed bounds) when the sign includes equals; count integers strictly inside for a count question."
   ],
   "example": {
     "question": "Solve \\(x^2 + 2x - 15 > 0\\). Give the smaller critical value.",
     "steps": [
       {"label": "Factorise", "content": "\\((x+5)(x-3) = 0\\), roots \\(-5\\) and \\(3\\)."},
       {"label": "Choose the region", "content": "\\(> 0\\) means outside the roots: \\(x < -5\\) or \\(x > 3\\)."},
       {"label": "Check", "content": "At \\(x = 4\\): \\(16 + 8 - 15 = 9 > 0\\). Correct."},
       {"label": "Answer", "content": "The smaller critical value is \\(-5\\).", "isAnswer": True, "is_answer": True}
     ]
   }
 },
 "gold": {
   "title": "Gold: rearranging, \\(a \\neq 1\\), discriminants and combined conditions",
   "steps": [
     "Rearrange so one side is 0 first; if you multiply by \\(-1\\), flip the inequality sign.",
     "When \\(x^2\\) has a coefficient, split the middle term to factorise; roots may be fractions.",
     "For a no-real-roots question use the discriminant \\(b^2 - 4ac < 0\\); for a combined condition, solve each part then take the overlap."
   ],
   "example": {
     "question": "Solve \\(2x^2 - x - 3 \\geq 0\\). Give the smaller critical value.",
     "steps": [
       {"label": "Split the middle term", "content": "\\(2x^2 - x - 3 = (2x-3)(x+1)\\), roots \\(-1\\) and \\(\\tfrac{3}{2}\\)."},
       {"label": "Choose the region", "content": "\\(\\geq 0\\) means outside the roots: \\(x \\leq -1\\) or \\(x \\geq \\tfrac{3}{2}\\)."},
       {"label": "Check", "content": "At \\(x = 2\\): \\(8 - 2 - 3 = 3 \\geq 0\\). Correct."},
       {"label": "Answer", "content": "The smaller critical value is \\(-1\\).", "isAnswer": True, "is_answer": True}
     ]
   }
 }
}

# ---- method card (slim) ----
method_card = {
 "title": "Solving Quadratic Inequalities",
 "steps": [
   "Rearrange so one side is 0, then factorise to find the two roots.",
   "Sketch the U-shape (positive \\(x^2\\)) crossing the x-axis at the roots.",
   "For \\(< 0\\) or \\(\\leq 0\\) take BETWEEN the roots; for \\(> 0\\) or \\(\\geq 0\\) take OUTSIDE them.",
   "Use \\(\\leq\\) or \\(\\geq\\) for an inclusive sign, \\(<\\) or \\(>\\) for a strict one."
 ],
 "content": "<p>A <strong>quadratic inequality</strong> asks which values of \\(x\\) make a quadratic above or below zero. Solve the matching equation for the roots, sketch the parabola, then read off the region.</p><p><strong>Below zero</strong> (\\(< 0\\), \\(\\leq 0\\)) sits between the roots; <strong>above zero</strong> (\\(> 0\\), \\(\\geq 0\\)) sits outside them.</p>",
 "example": "<p><strong>Solve</strong> \\(x^2 - 3x - 4 > 0\\).</p><p>\\((x-4)(x+1) = 0\\) gives roots \\(-1\\) and \\(4\\). Above zero is outside the roots, so \\(x < -1\\) or \\(x > 4\\).</p>"
}

# ---- per-problem enrichment: hints + honest-diagnosis misconceptions ----
# expect for multiple_choice = the OPTION INDEX the described error selects.
def mc(pattern, expect, message):
    return {"pattern": pattern, "expect": expect, "message": message}

bronze_enrich = [
 {"hint": "Solve \\(x^2 = 9\\) for roots ±3, then take between them for < 0.",
  "misc": [mc("wrong_region", 3, "For \\(< 0\\) the U-shape dips below the axis BETWEEN the roots \\(\\pm 3\\), so \\(-3 < x < 3\\). Outside the roots is where it is above zero."),
           mc("one_branch", 1, "The roots are \\(+3\\) and \\(-3\\), so you need both bounds: \\(-3 < x < 3\\). Keeping only \\(x < 3\\) drops the lower bound.")]},
 {"hint": "Solve \\(x^2 = 4\\) for roots ±2, then take outside them for > 0.",
  "misc": [mc("wrong_region", 1, "For \\(> 0\\) the curve is above the axis OUTSIDE the roots \\(\\pm 2\\): \\(x < -2\\) or \\(x > 2\\). Between the roots is where it is below zero."),
           mc("wrong_roots", 3, "Square-root \\(x^2 = 4\\) to get roots \\(\\pm 2\\), not 4. The roots are the numbers that square to give 4.")]},
 {"hint": "The roots are ±1; for ≤ 0 take between them, inclusive.",
  "misc": [mc("wrong_region", 3, "For \\(\\leq 0\\) the curve is on or below the axis BETWEEN the roots \\(\\pm 1\\): \\(-1 \\leq x \\leq 1\\). Outside the roots is where it is above zero."),
           mc("one_branch", 1, "You need both bounds: \\(-1 \\leq x \\leq 1\\). Keeping only \\(x \\leq 1\\) drops the lower bound.")]},
 {"hint": "The roots are 1 and 5; for < 0 take between them.",
  "misc": [mc("wrong_region", 1, "For \\(< 0\\) the product is negative BETWEEN the roots 1 and 5: \\(1 < x < 5\\). Outside the roots both brackets share a sign, giving a positive product.")]},
 {"hint": "The roots are −3 and 2; for > 0 take outside them.",
  "misc": [mc("wrong_region", 1, "For \\(> 0\\) the product is positive OUTSIDE the roots \\(-3\\) and 2: \\(x < -3\\) or \\(x > 2\\). Between the roots the product is negative."),
           mc("one_branch", 2, "You need both pieces: \\(x < -3\\) or \\(x > 2\\). Keeping only \\(x > 2\\) drops the left-hand piece.")]},
 {"hint": "Solve \\(x^2 = 25\\) for roots ±5, then take between them.",
  "misc": [mc("no_sqrt", 2, "Square-root both sides: \\(x^2 < 25\\) gives \\(|x| < 5\\), so \\(-5 < x < 5\\), not \\(x < 25\\)."),
           mc("one_branch", 1, "You need both bounds: \\(-5 < x < 5\\). Keeping only \\(x < 5\\) drops the lower bound.")]},
 {"hint": "The roots are −2 and 4; for ≥ 0 take outside them, inclusive.",
  "misc": [mc("wrong_region", 1, "For \\(\\geq 0\\) the product is positive or zero OUTSIDE the roots \\(-2\\) and 4: \\(x \\leq -2\\) or \\(x \\geq 4\\). Between the roots the product is negative.")]},
 {"hint": "Solve \\(x^2 = 36\\) for roots ±6, then take outside them.",
  "misc": [mc("wrong_region", 1, "For \\(x^2 \\geq 36\\) the values lie OUTSIDE the roots \\(\\pm 6\\): \\(x \\leq -6\\) or \\(x \\geq 6\\). Between them \\(x^2\\) is less than 36."),
           mc("wrong_roots", 3, "Square-root \\(x^2 = 36\\) to get roots \\(\\pm 6\\), not 36.")]},
]

silver_enrich = [
 {"hint": "Factorise to \\((x-2)(x-3)\\); for < 0 take between the roots.",
  "misc": [mc("wrong_region", 1, "\\((x-2)(x-3) < 0\\): for \\(< 0\\) take BETWEEN the roots, \\(2 < x < 3\\). Outside the roots the product is positive.")]},
 {"hint": "Factorise to \\((x+3)(x-2)\\); for > 0 take outside the roots.",
  "misc": [mc("wrong_region", 1, "\\((x+3)(x-2) > 0\\): for \\(> 0\\) take OUTSIDE the roots, \\(x < -3\\) or \\(x > 2\\). Between the roots the product is negative.")]},
 {"hint": "Factorise to \\((x-2)(x-5)\\); for ≤ 0 take between, inclusive.",
  "misc": [mc("wrong_region", 1, "\\((x-2)(x-5) \\leq 0\\): for \\(\\leq 0\\) take BETWEEN the roots, \\(2 \\leq x \\leq 5\\). Outside is where the product is positive."),
           mc("notation", 3, "The sign is \\(\\leq\\), so the endpoints are included: \\(2 \\leq x \\leq 5\\). Strict bounds would wrongly leave out \\(x = 2\\) and \\(x = 5\\).")]},
 {"hint": "Factorise to \\((x-6)(x+2)\\); for ≥ 0 take outside, inclusive.",
  "misc": [mc("wrong_region", 1, "\\((x-6)(x+2) \\geq 0\\): for \\(\\geq 0\\) take OUTSIDE the roots, \\(x \\leq -2\\) or \\(x \\geq 6\\). Between them the product is negative."),
           mc("one_branch", 3, "You need both pieces: \\(x \\leq -2\\) or \\(x \\geq 6\\). Keeping only \\(x \\leq -2\\) drops the right-hand piece.")]},
 {"hint": "Factorise, find the roots, then count the whole numbers strictly between them.",
  "misc": [mc("notation", 8, "The inequality is strict (\\(< 0\\)), so the roots \\(-2\\) and 5 are excluded. Counting them as well (using \\(\\leq\\)) gives 8, but only \\(-1\\) to 4 belong."),
           mc("off_by_one", 7, "Count the integers strictly between \\(-2\\) and 5: they are \\(-1, 0, 1, 2, 3, 4\\), which is 6, not 7. Watch for an off-by-one when counting.")]},
 {"hint": "Split the middle term to factorise \\((2x+1)(x-3)\\); for ≤ 0 take between.",
  "misc": [mc("wrong_region", 1, "\\((2x+1)(x-3) \\leq 0\\): for \\(\\leq 0\\) take BETWEEN the roots \\(-\\tfrac{1}{2}\\) and 3, so \\(-\\tfrac{1}{2} \\leq x \\leq 3\\). Outside is where it is positive."),
           mc("wrong_roots", 3, "Factorise to \\((2x+1)(x-3)\\): the roots are \\(-\\tfrac{1}{2}\\) and 3, not \\(-3\\) and \\(\\tfrac{1}{2}\\). Divide by the coefficient of \\(x\\) correctly.")]},
 {"hint": "Factorise to \\((x+4)(x-1)\\); for > 0 take outside the roots.",
  "misc": [mc("wrong_region", 1, "\\((x+4)(x-1) > 0\\): for \\(> 0\\) take OUTSIDE the roots, \\(x < -4\\) or \\(x > 1\\). Between them the product is negative.")]},
]

gold_enrich = [
 {"hint": "Multiply through by −1 and flip the sign first, then factorise.",
  "misc": [mc("sign_flip", 1, "Multiplying by \\(-1\\) flips the sign: \\(x^2 + x - 6 < 0\\), so \\((x+3)(x-2) < 0\\) gives BETWEEN the roots, \\(-3 < x < 2\\). Forgetting to flip the sign gives the outside region."),
           mc("wrong_roots", 3, "Rewrite as \\(x^2 + x - 6 < 0\\) and factorise to \\((x+3)(x-2)\\): the roots are \\(-3\\) and 2, not \\(-2\\) and 3.")]},
 {"hint": "Rearrange to \\(x^2 - 2x - 3 > 0\\) first, then factorise and take outside.",
  "misc": [mc("wrong_region", 1, "Rearrange to \\(x^2 - 2x - 3 > 0\\) first, then \\((x-3)(x+1) > 0\\) gives OUTSIDE the roots, \\(x < -1\\) or \\(x > 3\\). Between the roots the expression is below 3."),
           mc("one_branch", 2, "You need both pieces: \\(x < -1\\) or \\(x > 3\\). Keeping only \\(x > 3\\) drops the left-hand piece.")]},
 {"hint": "No real roots means the discriminant \\(b^2 - 4ac < 0\\); solve \\(k^2 - 36 < 0\\).",
  "misc": [mc("wrong_disc", 1, "No real roots needs the discriminant \\(< 0\\): \\(k^2 - 36 < 0\\) gives \\(-6 < k < 6\\). A discriminant \\(> 0\\) gives the outside range and TWO real roots."),
           mc("one_branch", 2, "\\(k^2 < 36\\) gives a symmetric range \\(-6 < k < 6\\). Do not drop the lower bound.")]},
 {"hint": "Solve the quadratic first, then keep only the part where \\(x > 0\\).",
  "misc": [mc("forgot_condition", 1, "\\((x+4)(x-2) \\leq 0\\) gives \\(-4 \\leq x \\leq 2\\), but you must also keep \\(x > 0\\). Combining leaves \\(0 < x \\leq 2\\)."),
           mc("notation", 2, "The quadratic sign is \\(\\leq\\), so \\(x = 2\\) is included: the answer is \\(0 < x \\leq 2\\). Only the \\(x > 0\\) end is strict.")]},
 {"hint": "Factorise, find the roots, then count the whole numbers strictly between them.",
  "misc": [mc("notation", 5, "The inequality is strict (\\(< 0\\)), so the roots 1 and 5 are excluded. Counting them as well (using \\(\\leq\\)) gives 5, but only 2, 3, 4 belong."),
           mc("off_by_one", 4, "Count the integers strictly between 1 and 5: they are 2, 3, 4, which is 3, not 4. Watch for an off-by-one.")]},
]

# guided_steps for the two single_value problems (silver[4] count=6, gold[4] count=3)
gs_silver4 = [
 {"say": "Factorise \\(x^2 - 3x - 10\\). Two numbers multiply to \\(-10\\) and add to \\(-3\\): they are \\(-5\\) and \\(+2\\), giving \\((x-5)(x+2)\\)."},
 {"pre": "From x - 5 = 0:  x = ", "post": "", "answer": 5, "hint": "x - 5 = 0 gives x = 5."},
 {"pre": "From x + 2 = 0:  x = ", "post": "", "answer": -2, "hint": "x + 2 = 0 gives x = -2."},
 {"say": "For \\(< 0\\) the solution is between the roots: \\(-2 < x < 5\\). Count the whole numbers strictly between \\(-2\\) and 5."},
 {"pre": "They are -1, 0, 1, 2, 3, 4.  How many?  ", "post": "", "phase": "substitute", "answer": 6, "hint": "Count from -1 up to 4."},
 {"pre": "Check the endpoint x = 5:  5² - 3(5) - 10 = ", "post": "", "phase": "substitute", "answer": 0,
  "done": "It equals 0, not below zero, so 5 is not counted. Only -1 to 4 count: 6 integers.", "hint": "25 - 15 - 10. It should be 0."},
]
gs_gold4 = [
 {"say": "Factorise \\(x^2 - 6x + 5\\). Two numbers multiply to \\(+5\\) and add to \\(-6\\): they are \\(-1\\) and \\(-5\\), giving \\((x-1)(x-5)\\)."},
 {"pre": "From x - 1 = 0:  x = ", "post": "", "answer": 1, "hint": "x - 1 = 0 gives x = 1."},
 {"pre": "From x - 5 = 0:  x = ", "post": "", "answer": 5, "hint": "x - 5 = 0 gives x = 5."},
 {"say": "For \\(< 0\\) the solution is between the roots: \\(1 < x < 5\\). Count the whole numbers strictly between 1 and 5."},
 {"pre": "They are 2, 3, 4.  How many?  ", "post": "", "phase": "substitute", "answer": 3, "hint": "Count from 2 up to 4."},
 {"pre": "Check the endpoint x = 1:  1² - 6(1) + 5 = ", "post": "", "phase": "substitute", "answer": 0,
  "done": "It equals 0, not below zero, so 1 is not counted. Only 2, 3, 4 count: 3 integers.", "hint": "1 - 6 + 5. It should be 0."},
]

pb = pd["problem_bank"]

def apply(tier, enrich, gs_map):
    for i, e in enumerate(pb[tier]):
        e["hint"] = enrich[i]["hint"]
        e["misconceptions"] = enrich[i]["misc"]
        if i in gs_map:
            e["guided_steps"] = gs_map[i]

apply("bronze", bronze_enrich, {})
apply("silver", silver_enrich, {4: gs_silver4})
apply("gold", gold_enrich, {4: gs_gold4})

pb["bronze_description"] = "Difference of squares and simple factors, reading between or outside the roots"
pb["silver_description"] = "Factorise three-term quadratics, strict and inclusive signs, integer counts"
pb["gold_description"] = "Rearranging, coefficient of x², discriminants and combined conditions"

pd["guided"] = {"opener": opener, "teach": teach}
pd["tier_guides"] = tier_guides
pd["method_card"] = method_card

json.dump(pd, io.open(DIR + r"\lesson_maths-aqa_algebra-L12.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written; tiers:", {t: len(pb[t]) for t in ("bronze", "silver", "gold")})
