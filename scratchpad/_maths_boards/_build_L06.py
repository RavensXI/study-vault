# -*- coding: utf-8 -*-
import json, io
from _svgs import figs  # b0,b1,b4 gradient SVGs

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

def load():
    return json.load(io.open("_live_L06.json", encoding="utf-8"))

pd = load()

# ---------- method_card: trim steps 5->4 ----------
pd["method_card"]["steps"] = [
    "Rate of change = gradient = rise ÷ run (draw a tangent first on a curve)",
    "Iteration: substitute x₀ into the formula to get x₁",
    "Then substitute x₁ to get x₂, and keep going",
    "Stop when the answer is stable to the required decimal places",
]

pb = pd["problem_bank"]
B = pb["bronze"]; S = pb["silver"]; G = pb["gold"]

# ---------- tier descriptions ----------
pb["bronze_description"] = "Read a rate of change from a tangent's gradient, or take one iteration step by putting the current value into the rule."
pb["silver_description"] = "Iterate with fraction or surd formulas and round to given decimal places, keeping full accuracy between steps."
pb["gold_description"] = "Run several iterations of a cube-root or Newton-style formula, or link an iteration formula back to the equation it solves."

# =========================================================
# BRONZE
# =========================================================
# idx0 gradient (1,3),(5,11) -> 2  [+SVG]
B[0]["display"] = figs["b0"] + CAP + " A tangent passes through \\((1, 3)\\) and \\((5, 11)\\). Find the rate of change."
B[0]["hint"] = "Rate of change is the gradient: change in y divided by change in x."
B[0]["misconceptions"] = [{
    "pattern": "rise_run_inverted",
    "message": "That is run ÷ rise. Gradient is rise ÷ run: (11 − 3) ÷ (5 − 1) = 8 ÷ 4 = 2.",
    "expect": 0.5}]
B[0]["guided_steps"] = [
    {"say": "A straight tangent's rate of change is its gradient: rise over run."},
    {"pre": "Change in y: 11 − 3 = ", "post": "", "answer": 8, "hint": "Subtract the two y-values."},
    {"pre": "Change in x: 5 − 1 = ", "post": "", "answer": 4, "hint": "Subtract the two x-values."},
    {"say": "Gradient = rise ÷ run.", "phase": "substitute",
     "pre": "8 ÷ 4 = ", "post": "", "answer": 2, "hint": "Divide the change in y by the change in x.", "done": "Rate of change = 2."},
    {"pre": "Check from (1, 3): 3 + 4 × 2 = ", "post": "", "answer": 11,
     "hint": "Go 4 across, rising 2 each step.", "done": "Lands on (5, 11), so the gradient is 2."},
]

# idx1 gradient (0,4),(2,10) -> 3  [+SVG]
B[1]["display"] = figs["b1"] + CAP + " A tangent passes through \\((0, 4)\\) and \\((2, 10)\\). Find the rate of change."
B[1]["hint"] = "Gradient is change in y divided by change in x."
B[1]["misconceptions"] = [{
    "pattern": "rise_run_inverted",
    "message": "That is run ÷ rise. Gradient is rise ÷ run: (10 − 4) ÷ (2 − 0) = 6 ÷ 2 = 3.",
    "expect": 0.333}]
B[1]["guided_steps"] = [
    {"pre": "Change in y: 10 − 4 = ", "post": "", "answer": 6, "hint": "Subtract the y-values."},
    {"pre": "Change in x: 2 − 0 = ", "post": "", "answer": 2, "hint": "Subtract the x-values."},
    {"say": "Gradient = rise ÷ run.", "phase": "substitute",
     "pre": "6 ÷ 2 = ", "post": "", "answer": 3, "hint": "Divide rise by run.", "done": "Rate of change = 3."},
    {"pre": "Check from (0, 4): 4 + 2 × 3 = ", "post": "", "answer": 10,
     "hint": "Go 2 across, rising 3 each step.", "done": "Reaches (2, 10), gradient 3 confirmed."},
]

# idx2 x_{n+1}=x_n+3, x0=1, x2 -> 7
B[2]["hint"] = "Find x₁ first, then feed it back into the rule for x₂."
B[2]["misconceptions"] = [{
    "pattern": "stopped_early",
    "message": "That is only x₁. The question asks for x₂, so apply the rule again: x₂ = 4 + 3 = 7.",
    "expect": 4}]
B[2]["guided_steps"] = [
    {"say": "Iteration: put the current value in, take the next one out."},
    {"pre": "x₁ = 1 + 3 = ", "post": "", "answer": 4, "hint": "Add 3 to x₀ = 1."},
    {"say": "Now feed x₁ = 4 back in.", "phase": "substitute",
     "pre": "x₂ = 4 + 3 = ", "post": "", "answer": 7, "hint": "Add 3 to x₁ = 4.", "done": "Two applications done: x₂ = 7."},
    {"pre": "Check the gap: 7 − 4 = ", "post": "", "answer": 3,
     "hint": "Each step should add 3.", "done": "The gap is 3, matching the +3 rule."},
]

# idx3 2x-1, x0=3, x1 -> 5
B[3]["hint"] = "Multiply x₀ by 2, then subtract 1."
B[3]["misconceptions"] = [{
    "pattern": "dropped_constant",
    "message": "That is just 2 × 3. Do not drop the − 1: x₁ = 2 × 3 − 1 = 5.",
    "expect": 6}]
B[3]["guided_steps"] = [
    {"pre": "2 × 3 = ", "post": "", "answer": 6, "hint": "Multiply x₀ = 3 by 2."},
    {"say": "Now subtract 1.", "phase": "substitute",
     "pre": "6 − 1 = ", "post": "", "answer": 5, "hint": "Take 1 off.", "done": "x₁ = 5."},
    {"pre": "Undo it: (5 + 1) ÷ 2 = ", "post": "", "answer": 3,
     "hint": "Add 1, then halve, to return to x₀.", "done": "Back to x₀ = 3, so x₁ = 5 is right."},
]

# idx4 gradient (1,-2),(5,14) -> 4  [CHANGED from (5,6)->2] [+SVG]
B[4]["display"] = figs["b4"] + CAP + " A tangent at \\(x = 3\\) passes through \\((1, -2)\\) and \\((5, 14)\\). Find the gradient."
B[4]["solutions"] = [4]
B[4]["hint"] = "Gradient is change in y over change in x; subtracting −2 adds 2."
B[4]["misconceptions"] = [{
    "pattern": "rise_run_inverted",
    "message": "That is run ÷ rise. Gradient is rise ÷ run: (14 − (−2)) ÷ (5 − 1) = 16 ÷ 4 = 4.",
    "expect": 0.25}]
B[4]["guided_steps"] = [
    {"pre": "Change in y: 14 − (−2) = ", "post": "", "answer": 16, "hint": "Subtracting −2 adds 2, so 14 + 2."},
    {"pre": "Change in x: 5 − 1 = ", "post": "", "answer": 4, "hint": "Subtract the x-values."},
    {"say": "Gradient = rise ÷ run.", "phase": "substitute",
     "pre": "16 ÷ 4 = ", "post": "", "answer": 4, "hint": "Divide rise by run.", "done": "Gradient = 4."},
    {"pre": "Check from (1, −2): −2 + 4 × 4 = ", "post": "", "answer": 14,
     "hint": "Go 4 across, rising 4 each step.", "done": "Reaches (5, 14), gradient 4 confirmed."},
]

# idx5 48/x_n, x0=8, x1 -> 6  [CHANGED from 10/x x0=2 ->5]
B[5]["display"] = "\\(x_{n+1} = \\frac{48}{x_n}\\). \\(x_0 = 8\\). Find \\(x_1\\)."
B[5]["solutions"] = [6]
B[5]["hint"] = "Divide 48 by the current value x₀ = 8."
B[5]["misconceptions"] = []
B[5]["guided_steps"] = [
    {"say": "The rule divides 48 by the current value."},
    {"pre": "Read the start value: x₀ = ", "post": "", "answer": 8, "hint": "It is given in the question."},
    {"say": "Apply the rule 48 ÷ x₀.", "phase": "substitute",
     "pre": "48 ÷ 8 = ", "post": "", "answer": 6, "hint": "How many 8s are in 48.", "done": "x₁ = 6."},
    {"pre": "Check: 6 × 8 = ", "post": "", "answer": 48,
     "hint": "Multiply back to undo the division.", "done": "Gives 48 back, so x₁ = 6 is right."},
]

# idx6 48/x_n, x0=8, x2 -> 8  [CHANGED from 10/x x0=2 ->2]
B[6]["display"] = "\\(x_{n+1} = \\frac{48}{x_n}\\). \\(x_0 = 8\\). Find \\(x_2\\)."
B[6]["solutions"] = [8]
B[6]["hint"] = "Find x₁ = 48 ÷ 8 first, then feed it back in."
B[6]["misconceptions"] = [{
    "pattern": "stopped_early",
    "message": "That is x₁. The question asks for x₂: feed x₁ = 6 back in, x₂ = 48 ÷ 6 = 8.",
    "expect": 6}]
B[6]["guided_steps"] = [
    {"pre": "x₁ = 48 ÷ 8 = ", "post": "", "answer": 6, "hint": "First iteration."},
    {"say": "Now feed x₁ = 6 back in.", "phase": "substitute",
     "pre": "x₂ = 48 ÷ 6 = ", "post": "", "answer": 8, "hint": "Divide 48 by x₁ = 6.", "done": "Back to 8: the sequence oscillates 8, 6, 8, 6."},
    {"pre": "Check: 8 × 6 = ", "post": "", "answer": 48,
     "hint": "Multiply back to undo the division.", "done": "48 ÷ 6 = 8 confirmed."},
]

# idx7 x_n^2 - 2, x0=4, x1 -> 14  [CHANGED from x0=2 ->2]
B[7]["display"] = "\\(x_{n+1} = x_n^2 - 2\\). \\(x_0 = 4\\). Find \\(x_1\\)."
B[7]["solutions"] = [14]
B[7]["hint"] = "Square x₀ first, then subtract 2."
B[7]["misconceptions"] = [{
    "pattern": "dropped_constant",
    "message": "That is just x₀². Do not drop the − 2: x₁ = 4² − 2 = 16 − 2 = 14.",
    "expect": 16}]
B[7]["guided_steps"] = [
    {"pre": "Square x₀: 4² = ", "post": "", "answer": 16, "hint": "4 × 4."},
    {"say": "Now subtract 2.", "phase": "substitute",
     "pre": "16 − 2 = ", "post": "", "answer": 14, "hint": "Take 2 off the square.", "done": "x₁ = 14."},
    {"pre": "Undo it: 14 + 2 = ", "post": "", "answer": 16,
     "hint": "Add 2 back; you should reach a square number.", "done": "16 is 4², so x₁ = 14 is right."},
]

# =========================================================
# SILVER
# =========================================================
# idx0 (x^2+5)/(2x), x0=3, x1 -> 2.333
S[0]["hint"] = "Work out the top and the bottom separately, then divide and round to 3 d.p."
S[0]["misconceptions"] = [{
    "pattern": "single_denominator",
    "message": "The denominator is 2x, not x: 14 ÷ (2 × 3) = 14 ÷ 6 = 2.333, not 14 ÷ 3.",
    "expect": 4.667}]
S[0]["guided_steps"] = [
    {"pre": "x₀²: 3² = ", "post": "", "answer": 9, "hint": "Square x₀ = 3."},
    {"pre": "Numerator: 9 + 5 = ", "post": "", "answer": 14, "hint": "Add 5 to x₀²."},
    {"say": "Denominator is 2 × x₀.", "phase": "substitute",
     "pre": "Denominator: 2 × 3 = ", "post": "", "answer": 6, "hint": "Double x₀ = 3."},
    {"pre": "x₁ = 14 ÷ 6 = ", "post": "", "answer": 2.333, "hint": "Divide and round to 3 d.p.", "done": "x₁ = 2.333."},
    {"say": "Check: this formula settles near \\(\\sqrt{5} ≈ 2.236\\), and 2.333 is one step in, so it is sensible."},
]

# idx1 sqrt(8+x), x0=3, x1 -> 3.317
S[1]["hint"] = "Add x₀ to 8 inside the root, then square root and round to 3 d.p."
S[1]["misconceptions"] = [{
    "pattern": "forgot_root",
    "message": "You need the square root of 8 + 3. √11 = 3.317, not 11 itself.",
    "expect": 11}]
S[1]["guided_steps"] = [
    {"pre": "Inside the root: 8 + 3 = ", "post": "", "answer": 11, "hint": "Add x₀ = 3 to 8."},
    {"say": "Now take the square root.", "phase": "substitute",
     "pre": "√11 = ", "post": "", "answer": 3.317, "hint": "Square root, round to 3 d.p.", "done": "x₁ = 3.317."},
    {"pre": "Check: 3.317² to the nearest whole number = ", "post": "", "answer": 11,
     "hint": "Squaring undoes the root.", "done": "Returns 11, so x₁ = 3.317 is right."},
]

# idx2 sqrt(8+x), x0=3, x2 -> 3.364 [FIXED from 3.363]
S[2]["solutions"] = [3.364]
S[2]["hint"] = "Find x₁ = √11 first, then feed it back into the root for x₂."
S[2]["misconceptions"] = [{
    "pattern": "stopped_early",
    "message": "That is x₁. For x₂, feed x₁ = 3.317 back in: x₂ = √(8 + 3.317) = √11.317 = 3.364.",
    "expect": 3.317}]
S[2]["guided_steps"] = [
    {"pre": "x₁ inside: 8 + 3 = ", "post": "", "answer": 11, "hint": "Add x₀ = 3 to 8."},
    {"pre": "x₁ = √11 = ", "post": "", "answer": 3.317, "hint": "Square root, 3 d.p."},
    {"say": "Now feed x₁ back in.", "phase": "substitute",
     "pre": "Inside: 8 + 3.317 = ", "post": "", "answer": 11.317, "hint": "Add x₁ to 8."},
    {"pre": "x₂ = √11.317 = ", "post": "", "answer": 3.364, "hint": "Square root, round to 3 d.p.", "done": "x₂ = 3.364."},
    {"say": "Check: the terms 3.317, 3.364 are creeping up towards the fixed point near 3.372, so x₂ = 3.364 is sensible."},
]

# idx3 MC population rate -> keep, add hint, expect null
S[3]["hint"] = "Continuous doubling gives an initial rate of about 100 × ln2 ÷ 3 per hour."
S[3]["misconceptions"] = [{
    "pattern": "confused",
    "message": "Doubling in 3 hours gives an initial rate of about 100 × ln2 ÷ 3 ≈ 23 per hour, not 100 or 200.",
    "expect": None}]

# idx4 6/(x+1), x0=2, x1 -> 2
S[4]["hint"] = "Work out the denominator x₀ + 1 first, then divide 6 by it."
S[4]["misconceptions"] = [{
    "pattern": "order_of_operations",
    "message": "The whole of x + 1 is the denominator: 6 ÷ (2 + 1) = 6 ÷ 3 = 2, not 6 ÷ 2 + 1.",
    "expect": 4}]
S[4]["guided_steps"] = [
    {"pre": "Denominator first: x₀ + 1 = 2 + 1 = ", "post": "", "answer": 3, "hint": "Add 1 to x₀ = 2."},
    {"say": "Now divide 6 by the whole denominator.", "phase": "substitute",
     "pre": "x₁ = 6 ÷ 3 = ", "post": "", "answer": 2, "hint": "Divide 6 by 3.", "done": "x₁ = 2, a fixed point here."},
    {"pre": "Check: 2 × 3 = ", "post": "", "answer": 6,
     "hint": "Multiply back to 6.", "done": "6 ÷ 3 = 2 confirmed."},
]

# idx5 (x^3+2)/(3x^2), x0=1, x1 -> 1
S[5]["hint"] = "Work out the top (x₀³ + 2) and bottom (3x₀²) separately, then divide."
S[5]["misconceptions"] = []
S[5]["guided_steps"] = [
    {"pre": "x₀³: 1³ = ", "post": "", "answer": 1, "hint": "Cube x₀ = 1."},
    {"pre": "Numerator: 1 + 2 = ", "post": "", "answer": 3, "hint": "Add 2 to x₀³."},
    {"say": "Denominator is 3 × x₀².", "phase": "substitute",
     "pre": "Denominator: 3 × 1² = ", "post": "", "answer": 3, "hint": "3 times x₀ squared."},
    {"pre": "x₁ = 3 ÷ 3 = ", "post": "", "answer": 1, "hint": "Divide numerator by denominator.", "done": "x₁ = 1, a fixed point: it maps to itself."},
]

# idx6 5/(x+2), x0=1, x1 -> 1.667
S[6]["hint"] = "Work out the denominator x₀ + 2 first, then divide 5 by it, to 3 d.p."
S[6]["misconceptions"] = [{
    "pattern": "order_of_operations",
    "message": "The whole of x + 2 is the denominator: 5 ÷ (1 + 2) = 5 ÷ 3 = 1.667, not 5 ÷ 1 + 2.",
    "expect": 7}]
S[6]["guided_steps"] = [
    {"pre": "Denominator: x₀ + 2 = 1 + 2 = ", "post": "", "answer": 3, "hint": "Add 2 to x₀ = 1."},
    {"say": "Now divide 5 by the whole denominator.", "phase": "substitute",
     "pre": "x₁ = 5 ÷ 3 = ", "post": "", "answer": 1.667, "hint": "Divide and round to 3 d.p.", "done": "x₁ = 1.667."},
    {"pre": "Check: 1.667 × 3 to the nearest whole number = ", "post": "", "answer": 5,
     "hint": "Multiply your answer by 3.", "done": "Returns 5, so x₁ = 1.667 is right."},
]

# =========================================================
# GOLD
# =========================================================
# idx0 cbrt(5x+4), x0=2, x3 -> 2.552  [FIXED from 2.408]
G[0]["solutions"] = [2.552]
G[0]["hint"] = "Cube-root three times: x₁, then x₂, then x₃; keep extra digits until the last round."
G[0]["misconceptions"] = [{
    "pattern": "stopped_early",
    "message": "That is x₁ = ∛14. You need x₃: iterate twice more, x₂ ≈ 2.5225 then x₃ = 2.552.",
    "expect": 2.410}]
G[0]["guided_steps"] = [
    {"say": "Cube-root iteration. Keep 4 d.p. between steps, round only at the end."},
    {"pre": "x₁ inside: 5 × 2 + 4 = ", "post": "", "answer": 14, "hint": "5 times x₀ plus 4."},
    {"pre": "x₁ = ∛14 = ", "post": "", "answer": 2.4101, "hint": "Cube root, keep 4 d.p."},
    {"say": "x₂ from x₁: 5 × 2.4101 + 4 = 16.0505, then cube root.",
     "pre": "x₂ = ∛16.0505 = ", "post": "", "answer": 2.5225, "hint": "Cube root, keep 4 d.p."},
    {"say": "Last step, x₃ from x₂.", "phase": "substitute",
     "pre": "5 × 2.5225 + 4 = ", "post": "", "answer": 16.6125, "hint": "5 times x₂ plus 4."},
    {"pre": "x₃ = ∛16.6125 = ", "post": "", "answer": 2.552, "hint": "Cube root, round to 3 d.p.", "done": "x₃ = 2.552 to 3 d.p."},
]

# idx1 rearrangement, constant term -> -4
G[1]["hint"] = "Cube both sides to get x³ = 5x + 4, then move everything to one side."
G[1]["misconceptions"] = [{
    "pattern": "sign_error",
    "message": "Moving + 4 across the equals sign makes it − 4. The equation is x³ − 5x − 4 = 0, constant − 4.",
    "expect": 4}]
G[1]["guided_steps"] = [
    {"say": "Cube both sides of x = ∛(5x + 4) to get x³ = 5x + 4."},
    {"pre": "The coefficient of x³ is ", "post": "", "answer": 1, "hint": "There is one x³, so the coefficient is 1."},
    {"say": "Move 5x and 4 to the left.", "phase": "substitute",
     "pre": "The coefficient of x becomes ", "post": "", "answer": -5, "hint": "5x moves across to −5x."},
    {"pre": "The constant term becomes ", "post": "", "answer": -4, "hint": "+4 moves across to −4.", "done": "x³ − 5x − 4 = 0, constant −4."},
]

# idx2 (x^2+7)/(2x), x0=3, x2 -> 2.6458
G[2]["hint"] = "Find x₁ first, then feed it back into (x² + 7)/(2x); round x₂ to 4 d.p."
G[2]["misconceptions"] = [{
    "pattern": "stopped_early",
    "message": "That is x₁ = 16 ÷ 6 = 2.6667. The question asks for x₂: feed x₁ back in to get 2.6458.",
    "expect": 2.6667}]
G[2]["guided_steps"] = [
    {"say": "x₀² = 9, so the numerator is 9 + 7."},
    {"pre": "x₁ numerator: 9 + 7 = ", "post": "", "answer": 16, "hint": "Add 7 to x₀²."},
    {"pre": "x₁ = 16 ÷ 6 = ", "post": "", "answer": 2.6667, "hint": "Denominator is 2 × 3 = 6; keep 4 d.p."},
    {"say": "Now x₂ from x₁ = 2.6667.", "phase": "substitute",
     "pre": "x₁²: 2.6667² = ", "post": "", "answer": 7.1113, "hint": "Square x₁, keep 4 d.p."},
    {"pre": "New numerator: 7.1113 + 7 = ", "post": "", "answer": 14.1113, "hint": "Add 7."},
    {"pre": "x₂ = 14.1113 ÷ 5.3334 = ", "post": "", "answer": 2.6458, "hint": "Denominator is 2 × 2.6667 = 5.3334; round to 4 d.p.", "done": "x₂ = 2.6458."},
]

# idx3 MC converges to 2.646 -> add hint, expect null
G[3]["hint"] = "Square 2.646 and see which value it gives."
G[3]["misconceptions"] = [{
    "pattern": "confused",
    "message": "2.646² ≈ 7.00, so the iteration solves x² = 7 (that is x = √7).",
    "expect": None}]

# idx4 3 + 1/x^2, x0=3, x1 -> 3.111
G[4]["hint"] = "Square x₀, take one over it, then add 3; round to 3 d.p."
G[4]["misconceptions"] = [{
    "pattern": "wrong_power",
    "message": "It is 1 over x squared, not 1 over x: 3 + 1 ÷ 9 = 3.111, not 3 + 1 ÷ 3 = 3.333.",
    "expect": 3.333}]
G[4]["guided_steps"] = [
    {"pre": "x₀²: 3² = ", "post": "", "answer": 9, "hint": "Square x₀ = 3."},
    {"say": "Now take one over that.", "phase": "substitute",
     "pre": "1 ÷ 9 = ", "post": "", "answer": 0.111, "hint": "One over x₀ squared, to 3 d.p."},
    {"pre": "x₁ = 3 + 0.111 = ", "post": "", "answer": 3.111, "hint": "Add to 3.", "done": "x₁ = 3.111."},
]

# =========================================================
# tier_guides
# =========================================================
pd["tier_guides"] = {
  "bronze": {
    "title": "Bronze: one step at a time",
    "steps": [
      "A straight line's <strong>rate of change</strong> is its gradient: change in y divided by change in x between two points.",
      "An <strong>iteration</strong> puts the current value \\(x_n\\) into the rule, and the answer becomes the next value \\(x_{n+1}\\).",
      "For \\(x_2\\), do the rule twice: find \\(x_1\\) first, then feed it back in."
    ],
    "example": {
      "question": "\\(x_{n+1} = 2x_n + 1\\), \\(x_0 = 3\\). Find \\(x_2\\).",
      "steps": [
        {"label": "Step 1", "content": "<p>\\(x_1 = 2(3) + 1 = 7\\)</p>"},
        {"label": "Step 2", "content": "<p>\\(x_2 = 2(7) + 1 = 15\\)</p>"},
        {"label": "Check", "content": "<p>Each step doubles and adds 1, so 7 then 15 is right.</p>"},
        {"label": "Answer", "content": "<p>\\(x_2 = 15\\)</p>", "isAnswer": True, "is_answer": True}
      ]
    }
  },
  "silver": {
    "title": "Silver: iterate and round",
    "steps": [
      "Silver formulas are fractions or surds, like \\(\\sqrt{8 + x_n}\\) or \\(\\frac{x_n^2 + 5}{2x_n}\\).",
      "Work the top and bottom (or inside the root) separately, then combine. Round only at the end to the stated decimal places.",
      "For \\(x_2\\), keep extra digits of \\(x_1\\) so the final rounding stays accurate."
    ],
    "example": {
      "question": "\\(x_{n+1} = \\sqrt{5 + x_n}\\), \\(x_0 = 4\\). Find \\(x_1\\) to 3 d.p.",
      "steps": [
        {"label": "Inside", "content": "<p>\\(5 + 4 = 9\\)</p>"},
        {"label": "Root", "content": "<p>\\(\\sqrt{9} = 3.000\\)</p>"},
        {"label": "Check", "content": "<p>\\(3^2 = 9\\), which matches, so the root is right.</p>"},
        {"label": "Answer", "content": "<p>\\(x_1 = 3.000\\)</p>", "isAnswer": True, "is_answer": True}
      ]
    }
  },
  "gold": {
    "title": "Gold: many steps and rearranging",
    "steps": [
      "Gold uses cube-roots or Newton-style formulas and asks for \\(x_2\\) or \\(x_3\\), so you iterate several times.",
      "Carry full calculator accuracy through every step, rounding only the final answer.",
      "Some questions run backwards: rearrange \\(x^3 = 5x + 4\\) into \\(x = \\sqrt[3]{5x + 4}\\) to build the formula."
    ],
    "example": {
      "question": "\\(x_{n+1} = \\sqrt[3]{4x_n + 1}\\), \\(x_0 = 2\\). Find \\(x_2\\) to 3 d.p.",
      "steps": [
        {"label": "Step 1", "content": "<p>\\(x_1 = \\sqrt[3]{4(2) + 1} = \\sqrt[3]{9} = 2.0801\\)</p>"},
        {"label": "Step 2", "content": "<p>\\(x_2 = \\sqrt[3]{4(2.0801) + 1} = \\sqrt[3]{9.3204} = 2.104\\)</p>"},
        {"label": "Check", "content": "<p>The terms are rising slowly towards the root, so 2.104 is sensible.</p>"},
        {"label": "Answer", "content": "<p>\\(x_2 = 2.104\\)</p>", "isAnswer": True, "is_answer": True}
      ]
    }
  }
}

# =========================================================
# guided: opener + teach
# =========================================================
pd["guided"] = {
  "opener": {
    "label": "Before any formulas",
    "display": "Picture a number machine. Whatever you put in, it <strong>halves it, then adds 3</strong>, and shows the answer.<br>You feed that answer straight back in.<br>Start with <strong>10</strong>.",
    "steps": [
      {"say": "No algebra, just do it in your head.",
       "pre": "First output: 10 ÷ 2 + 3 = ", "post": "", "answer": 8,
       "hint": "Half of 10 is 5, then add 3."},
      {"say": "Now feed the 8 back in.",
       "pre": "Next output: 8 ÷ 2 + 3 = ", "post": "", "answer": 7,
       "hint": "Half of 8 is 4, then add 3."},
      {"say": "That move, taking each answer and feeding it back in, is an <strong>iteration</strong>. You just built the sequence \\(x_{n+1} = \\tfrac{x_n}{2} + 3\\): 10, 8, 7, 6.5... It keeps closing in on <strong>6</strong>, the solution of \\(x = \\tfrac{x}{2} + 3\\). That settling-down is the whole idea of iteration."}
    ]
  },
  "teach": {
    "bronze": {
      "label": "Together: a rate of change",
      "display": "A tangent passes through \\((2, 1)\\) and \\((6, 9)\\). Find the rate of change.",
      "steps": [
        {"say": "Rate of change is the gradient: rise over run.",
         "pre": "Change in y: 9 − 1 = ", "post": "", "answer": 8, "hint": "Subtract the y-values."},
        {"pre": "Change in x: 6 − 2 = ", "post": "", "answer": 4, "hint": "Subtract the x-values."},
        {"say": "Gradient = rise ÷ run.",
         "pre": "8 ÷ 4 = ", "post": "", "answer": 2, "hint": "Divide rise by run.",
         "done": "Rate of change = 2. That is the whole move."},
        {"pre": "Check from (2, 1): 1 + 4 × 2 = ", "post": "", "answer": 9,
         "hint": "Go 4 across, rising 2 each step.", "done": "Reaches (6, 9), so 2 is right."}
      ]
    },
    "silver": {
      "label": "Together: a fraction iteration",
      "display": "\\(x_{n+1} = \\frac{x_n^2 + 3}{2x_n}\\). \\(x_0 = 2\\). Find \\(x_1\\) to 3 d.p.",
      "steps": [
        {"say": "Build the top and bottom separately.",
         "pre": "x₀²: 2² = ", "post": "", "answer": 4, "hint": "Square x₀ = 2."},
        {"pre": "Numerator: 4 + 3 = ", "post": "", "answer": 7, "hint": "Add 3 to x₀²."},
        {"pre": "Denominator: 2 × 2 = ", "post": "", "answer": 4, "hint": "Double x₀ = 2."},
        {"say": "Now divide and round.",
         "pre": "x₁ = 7 ÷ 4 = ", "post": "", "answer": 1.75, "hint": "Divide, to 3 d.p. that is 1.750.",
         "done": "x₁ = 1.750. Splitting top from bottom is the new move."}
      ]
    },
    "gold": {
      "label": "Together: a cube-root iteration",
      "display": "\\(x_{n+1} = \\sqrt[3]{7x_n + 20}\\). \\(x_0 = 1\\). Find \\(x_2\\) to 3 d.p.",
      "steps": [
        {"say": "One step at a time. Inside first.",
         "pre": "7 × 1 + 20 = ", "post": "", "answer": 27, "hint": "7 times x₀ plus 20."},
        {"pre": "x₁ = ∛27 = ", "post": "", "answer": 3, "hint": "Cube root of 27 is exact."},
        {"say": "Now x₂ from x₁ = 3.",
         "pre": "7 × 3 + 20 = ", "post": "", "answer": 41, "hint": "7 times x₁ plus 20."},
        {"pre": "x₂ = ∛41 = ", "post": "", "answer": 3.448, "hint": "Cube root, round to 3 d.p.",
         "done": "x₂ = 3.448. Running several exact steps is the gold move."}
      ]
    }
  }
}

# ---------- write ----------
with open("lesson_maths-ocr_ratio-proportion-L06.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written. top keys:", list(pd.keys()))
