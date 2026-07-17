# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_rp06.json", encoding="utf-8"))

# ---- preserve byte-for-byte ----
topic_links = live["topic_links"]
related_videos = live["related_videos"]
worked_examples = live["worked_examples"]

# ---------- OPENER SVG (distance-time chord) ----------
OPENER_SVG = (
 '<svg viewBox="0 0 240 170" role="img" aria-label="Distance-time graph: 20 km at 1 pm rising to 80 km at 3 pm, with a straight chord joining the two points">'
 '<line x1="40" y1="18" x2="40" y2="140" stroke="currentColor" stroke-width="1"/>'
 '<line x1="40" y1="140" x2="222" y2="140" stroke="currentColor" stroke-width="1"/>'
 '<line x1="40" y1="112.5" x2="210" y2="30" stroke="#3b82f6" stroke-width="2"/>'
 '<circle cx="40" cy="112.5" r="3.5" fill="#3b82f6"/>'
 '<circle cx="210" cy="30" r="3.5" fill="#3b82f6"/>'
 '<text x="16" y="116" font-family="Inter, sans-serif" font-size="11" fill="currentColor">20</text>'
 '<text x="16" y="34" font-family="Inter, sans-serif" font-size="11" fill="currentColor">80</text>'
 '<text x="28" y="155" font-family="Inter, sans-serif" font-size="11" fill="currentColor">1 pm</text>'
 '<text x="192" y="155" font-family="Inter, sans-serif" font-size="11" fill="currentColor">3 pm</text>'
 '<text x="6" y="14" font-family="Inter, sans-serif" font-size="10" fill="currentColor">km</text>'
 '</svg>'
)

opener = {
 "display": OPENER_SVG + "<p>A car is 20 km from home at 1 pm, and 80 km from home at 3 pm.</p>",
 "steps": [
  {"pre": "How many more km from home is the car at 3 pm than at 1 pm? 80 − 20 = ", "post": "", "answer": 60,
   "hint": "Subtract the two distances."},
  {"pre": "How many hours passed between 1 pm and 3 pm? ", "post": "", "answer": 2,
   "hint": "From 1 pm to 3 pm."},
  {"pre": "So on average, how many km did it travel each hour? 60 ÷ 2 = ", "post": "", "answer": 30,
   "hint": "Divide the distance by the time."},
  {"say": "That is a <strong>rate of change</strong>: the change in distance divided by the change in time, 60 ÷ 2 = 30 km/h. In maths we write it as \\(\\frac{f(b)-f(a)}{b-a}\\), the change in output over the change in input. It is the gradient of the straight line (the chord) joining the two points on the graph."}
 ]
}

# ---------- TEACH WALKS ----------
teach = {
 "bronze": {
  "display": "Find the average rate of change of \\(y = x^2\\) between \\(x = 1\\) and \\(x = 4\\).",
  "steps": [
   {"say": "Average rate of change = (change in y) ÷ (change in x). Work out both y-values first."},
   {"pre": "f(1) = 1² = ", "post": "", "answer": 1, "hint": "Square 1."},
   {"pre": "f(4) = 4² = ", "post": "", "answer": 16, "hint": "Square 4."},
   {"pre": "Change in y = 16 − 1 = ", "post": "", "answer": 15, "hint": "Subtract the y-values."},
   {"pre": "Change in x = 4 − 1 = ", "post": "", "answer": 3, "hint": "Subtract the x-values."},
   {"pre": "Rate = 15 ÷ 3 = ", "post": "", "answer": 5, "hint": "Divide change in y by change in x.",
    "done": "The chord from (1,1) to (4,16) has gradient 5. That is the whole method."}
  ]
 },
 "silver": {
  "display": "Show that \\(f(x) = x^3 - 2x - 5\\) has a root between \\(x = 2\\) and \\(x = 3\\).",
  "steps": [
   {"say": "A root sits where f changes sign. Evaluate f at each end, watching the powers."},
   {"pre": "First 2³ = ", "post": "", "answer": 8, "hint": "2 × 2 × 2."},
   {"pre": "f(2) = 8 − 2(2) − 5 = 8 − 4 − 5 = ", "post": "", "answer": -1, "hint": "8 − 4 − 5."},
   {"pre": "Now 3³ = ", "post": "", "answer": 27, "hint": "3 × 3 × 3."},
   {"pre": "f(3) = 27 − 2(3) − 5 = 27 − 6 − 5 = ", "post": "", "answer": 16, "hint": "27 − 6 − 5.",
    "done": "f(2) = −1 (negative), f(3) = 16 (positive): a sign change, so a root lies between 2 and 3. That is the whole point."}
  ]
 },
 "gold": {
  "display": "Using \\(x_{n+1} = \\sqrt{2x_n + 6}\\) with \\(x_0 = 3\\), find \\(x_2\\) to 3 d.p.",
  "steps": [
   {"say": "Iteration feeds each answer back in. Keep enough decimals as you go."},
   {"pre": "Inside the first root: 2 × 3 + 6 = ", "post": "", "answer": 12, "hint": "2 times x0, plus 6."},
   {"pre": "x₁ = √12 to 3 d.p. = ", "post": "", "answer": 3.464, "hint": "Square root of 12."},
   {"pre": "Now use x₁ = 3.464. Inside the next root: 2 × 3.464 + 6 = ", "post": "", "answer": 12.928, "hint": "2 times 3.464, plus 6."},
   {"pre": "x₂ = √12.928 to 3 d.p. = ", "post": "", "answer": 3.596, "hint": "Square root of 12.928.",
    "done": "The values 3, 3.464, 3.596 are climbing toward the fixed point (the root of x² = 2x + 6). That is the whole point of iterating."}
  ]
 }
}

guided = {"opener": opener, "teach": teach}

# ---------- TIER GUIDES ----------
tier_guides = {
 "bronze": {
  "title": "Bronze: average rate and first steps",
  "steps": [
   "<strong>Average rate of change</strong> between two x-values is the change in y divided by the change in x: \\(\\frac{f(b)-f(a)}{b-a}\\).",
   "Work out both y-values, subtract them, then divide by how far apart the x-values are.",
   "For an iteration like \\(x_{n+1}=x_n+3\\), just put the current value in to get the next one."
  ],
  "example": {
   "question": "Average rate of change of y = x² between x = 1 and x = 4",
   "steps": [
    {"label": "Find the y-values", "content": "f(1) = 1, f(4) = 16"},
    {"label": "Change in y over change in x", "content": "(16 − 1) ÷ (4 − 1) = 15 ÷ 3"},
    {"label": "Check", "content": "3 × 5 = 15, matching the change in y"},
    {"label": "Answer", "content": "= 5", "isAnswer": True, "is_answer": True}
   ]
  }
 },
 "silver": {
  "title": "Silver: sign changes and single iterations",
  "steps": [
   "A <strong>sign change</strong> locates a root: if \\(f(a)\\) and \\(f(b)\\) have opposite signs, the curve crosses zero between them.",
   "Substitute each value carefully, watching the negatives, then compare the signs.",
   "For one iteration, work out the inside first, then apply the root or fraction once."
  ],
  "example": {
   "question": "f(x) = x³ − 2x − 5, show a root between x = 2 and x = 3",
   "steps": [
    {"label": "f(2)", "content": "8 − 4 − 5 = −1"},
    {"label": "f(3)", "content": "27 − 6 − 5 = 16"},
    {"label": "Check the signs", "content": "−1 is negative, 16 is positive"},
    {"label": "Answer", "content": "Sign change, so a root lies between 2 and 3", "isAnswer": True, "is_answer": True}
   ]
  }
 },
 "gold": {
  "title": "Gold: iterating to accuracy and real rates",
  "steps": [
   "Each <strong>iteration</strong> feeds the previous answer back in. Keep full accuracy between steps and round only at the end.",
   "For a real-life model the average rate of change is still \\(\\frac{f(b)-f(a)}{b-a}\\), using the two given inputs.",
   "Round to the accuracy the question asks for, such as 3 decimal places."
  ],
  "example": {
   "question": "Iterate x_{n+1} = √(2x_n + 6) from x₀ = 3, find x₂ to 3 d.p.",
   "steps": [
    {"label": "x₁", "content": "√(2×3 + 6) = √12 = 3.464"},
    {"label": "x₂", "content": "√(2×3.464 + 6) = √12.928"},
    {"label": "Check", "content": "3.596² ≈ 12.93, matching the inside"},
    {"label": "Answer", "content": "x₂ = 3.596", "isAnswer": True, "is_answer": True}
   ]
  }
 }
}

# ---------- METHOD CARD (slim) ----------
method_card = {
 "title": "How to Work with Rates of Change & Iteration",
 "steps": [
  "Average rate of change = (change in y) ÷ (change in x), the gradient of the chord.",
  "To solve f(x) = 0 by iteration, rearrange it into x = g(x).",
  "Start at x₀ and repeatedly apply xₙ₊₁ = g(xₙ) until the values settle.",
  "A sign change in f between two x-values shows a root lies between them."
 ],
 "content": "<p>A <strong>rate of change</strong> measures how one quantity changes with another. The <strong>average rate of change</strong> between two points is the gradient of the chord joining them, \\(\\frac{f(b)-f(a)}{b-a}\\).</p><p><strong>Iteration</strong> solves an equation by repeated substitution: rearrange \\(f(x)=0\\) into \\(x=g(x)\\), then apply \\(x_{n+1}=g(x_n)\\) from a start value until the sequence converges.</p>",
 "example": "<p><strong>Iterate \\(x_{n+1} = \\sqrt{2x_n + 6}\\) with \\(x_0 = 3\\).</strong></p><p>\\(x_1 = \\sqrt{2(3)+6} = \\sqrt{12} \\approx 3.464\\)</p><p>\\(x_2 = \\sqrt{2(3.464)+6} = \\sqrt{12.928} \\approx 3.596\\)</p>"
}

# ---------- PROBLEM BANK ----------
def P(display, sols, calc, it, hint, gs, misc):
    d = {"display": display, "solutions": sols, "calculator": calc,
         "input_type": it, "hint": hint, "misconceptions": misc}
    if gs is not None:
        d["guided_steps"] = gs
    return d

bronze = [
 # B0
 P("Find the average rate of change of \\(y = x^2\\) between \\(x = 1\\) and \\(x = 3\\).",
   [4], False, "single_value",
   "Work out the two y-values, subtract, then divide by the change in x.",
   [
    {"say": "Average rate of change = (change in y) ÷ (change in x)."},
    {"pre": "f(1) = 1² = ", "post": "", "answer": 1, "hint": "Square 1."},
    {"pre": "f(3) = 3² = ", "post": "", "answer": 9, "hint": "Square 3."},
    {"pre": "Change in y = 9 − 1 = ", "post": "", "answer": 8, "hint": "Subtract the y-values.", "phase": "substitute"},
    {"pre": "Change in x = 3 − 1 = ", "post": "", "answer": 2, "hint": "Subtract the x-values."},
    {"pre": "Rate = 8 ÷ 2 = ", "post": "", "answer": 4, "hint": "Divide change in y by change in x.",
     "done": "The curve rises 8 over a run of 2, so the average gradient is 4."}
   ],
   [{"pattern": "forgot_divide", "expect": 8,
     "message": "8 is the change in y only. Divide by the change in x, 3 − 1 = 2, giving 8 ÷ 2 = 4."}]),
 # B1  (fixed: was y=2x+3 giving 2, duplicated B3; now y=3x+1 giving 3)
 P("Find the average rate of change of \\(y = 3x + 1\\) between \\(x = 0\\) and \\(x = 5\\).",
   [3], False, "single_value",
   "For a line the rate of change is its gradient, but you can still do change in y over change in x.",
   [
    {"say": "For a straight line the average rate of change equals its gradient. Let's compute it directly."},
    {"pre": "f(0) = 3(0) + 1 = ", "post": "", "answer": 1, "hint": "Put x = 0 in."},
    {"pre": "f(5) = 3(5) + 1 = ", "post": "", "answer": 16, "hint": "3 times 5, plus 1."},
    {"pre": "Change in y = 16 − 1 = ", "post": "", "answer": 15, "hint": "Subtract the y-values.", "phase": "substitute"},
    {"pre": "Change in x = 5 − 0 = ", "post": "", "answer": 5, "hint": "Subtract the x-values."},
    {"pre": "Rate = 15 ÷ 5 = ", "post": "", "answer": 3, "hint": "Divide change in y by change in x.",
     "done": "y = 3x + 1 has gradient 3, matching our answer."}
   ],
   [{"pattern": "forgot_divide", "expect": 15,
     "message": "15 is the change in y. Divide by the change in x (5 − 0 = 5): 15 ÷ 5 = 3."}]),
 # B2
 P("Show there is a root of \\(x^2 - 7 = 0\\) between \\(x = 2\\) and \\(x = 3\\). What is \\(f(2)\\)?",
   [-3], False, "single_value",
   "Put x = 2 into x squared minus 7.",
   [
    {"say": "f(x) = x² − 7. Put x = 2 in, step by step."},
    {"pre": "First 2² = ", "post": "", "answer": 4, "hint": "2 × 2."},
    {"pre": "Now subtract 7: 4 − 7 = ", "post": "", "answer": -3, "hint": "4 − 7 is negative.", "phase": "substitute"},
    {"pre": "Check by rebuilding: (−3) + 7 = ", "post": "", "answer": 4, "hint": "Add 7 back on.",
     "done": "(−3) + 7 = 4 = 2², so f(2) = −3. It is negative, and f(3) is positive, so a root lies between 2 and 3."}
   ],
   [{"pattern": "sign_flip", "expect": 3,
     "message": "3 means you worked out 7 − 4. The function is x² − 7, so it is 4 − 7 = −3."}]),
 # B3
 P("For the same equation, what is \\(f(3)\\)?",
   [2], False, "single_value",
   "Put x = 3 into x squared minus 7.",
   [
    {"say": "Same function f(x) = x² − 7. Now put x = 3 in."},
    {"pre": "First 3² = ", "post": "", "answer": 9, "hint": "3 × 3."},
    {"pre": "Now subtract 7: 9 − 7 = ", "post": "", "answer": 2, "hint": "9 − 7.", "phase": "substitute"},
    {"pre": "Check by rebuilding: 2 + 7 = ", "post": "", "answer": 9, "hint": "Add 7 back on.",
     "done": "2 + 7 = 9 = 3², so f(3) = 2. f(2) = −3 < 0 and f(3) = 2 > 0: a sign change, root between 2 and 3."}
   ],
   [{"pattern": "sign_flip", "expect": -2,
     "message": "−2 comes from 7 − 9. Read it as x² − 7 = 9 − 7 = 2."}]),
 # B4
 P("Using \\(x_{n+1} = x_n + 3\\) with \\(x_0 = 2\\), find \\(x_1\\).",
   [5], False, "single_value",
   "Add 3 to the starting value.",
   [
    {"say": "Iteration means putting the current value into the formula to get the next one. Here x_{n+1} = x_n + 3."},
    {"pre": "The starting value is x₀ = 2. What do we add each time? ", "post": "", "answer": 3, "hint": "Read it off the formula."},
    {"pre": "x₁ = x₀ + 3 = 2 + 3 = ", "post": "", "answer": 5, "hint": "2 + 3.", "phase": "substitute"},
    {"pre": "Check: x₁ − x₀ should equal 3. Work out 5 − 2 = ", "post": "", "answer": 3, "hint": "Subtract the start.",
     "done": "5 − 2 = 3, the step size, so x₁ = 5."}
   ],
   [{"pattern": "multiplied", "expect": 6,
     "message": "6 is 2 × 3. The formula adds 3, so x₁ = 2 + 3 = 5."}]),
 # B5
 P("Using \\(x_{n+1} = x_n + 3\\) with \\(x_0 = 2\\), find \\(x_2\\).",
   [8], False, "single_value",
   "Add 3 again, this time to x sub 1.",
   [
    {"say": "Apply the same rule again, now to x₁ = 5, to get x₂."},
    {"pre": "The current value is x₁ = ", "post": "", "answer": 5, "hint": "From the previous step."},
    {"pre": "x₂ = x₁ + 3 = 5 + 3 = ", "post": "", "answer": 8, "hint": "5 + 3.", "phase": "substitute"},
    {"pre": "Check: x₂ − x₁ should be 3. Work out 8 − 5 = ", "post": "", "answer": 3, "hint": "Subtract x1.",
     "done": "8 − 5 = 3, so x₂ = 8. The sequence goes 2, 5, 8, adding 3 each time."}
   ],
   [{"pattern": "reused_start", "expect": 5,
     "message": "5 is x₁, not x₂. Apply the rule to x₁: x₂ = 5 + 3 = 8."}]),
 # B6
 P("Find the average rate of change of \\(y = x^2\\) between \\(x = 2\\) and \\(x = 4\\).",
   [6], False, "single_value",
   "Subtract the y-values, then divide by 4 minus 2.",
   [
    {"say": "Average rate = (change in y) ÷ (change in x)."},
    {"pre": "f(2) = 2² = ", "post": "", "answer": 4, "hint": "Square 2."},
    {"pre": "f(4) = 4² = ", "post": "", "answer": 16, "hint": "Square 4."},
    {"pre": "Change in y = 16 − 4 = ", "post": "", "answer": 12, "hint": "Subtract the y-values.", "phase": "substitute"},
    {"pre": "Change in x = 4 − 2 = ", "post": "", "answer": 2, "hint": "Subtract the x-values."},
    {"pre": "Rate = 12 ÷ 2 = ", "post": "", "answer": 6, "hint": "Divide change in y by change in x.",
     "done": "The chord from (2,4) to (4,16) has gradient 6."}
   ],
   [{"pattern": "forgot_divide", "expect": 12,
     "message": "12 is the change in y. Divide by 4 − 2 = 2: 12 ÷ 2 = 6."}]),
 # B7 MC
 P("What does a positive rate of change mean on a graph?",
   [0], False, "multiple_choice",
   "A positive gradient means the line slopes upward.",
   None,
   [{"pattern": "meaning", "expect": None,
     "message": "A positive rate of change is a positive gradient: the graph goes up as x increases."}]),
]
bronze[7]["options"] = ["The graph is increasing", "The graph is decreasing",
                        "The graph is flat", "The graph has a turning point"]

silver = [
 # S0 fraction
 P("Using \\(x_{n+1} = \\frac{10}{x_n + 1}\\) with \\(x_0 = 2\\), find \\(x_1\\). Give answer as a fraction.",
   [10, 3], False, "fraction",
   "The denominator is x sub 0 plus 1, so work that out first.",
   [
    {"say": "Iterate x_{n+1} = 10/(x_n + 1) once, from x₀ = 2."},
    {"pre": "Work out the denominator: x₀ + 1 = 2 + 1 = ", "post": "", "answer": 3, "hint": "2 + 1."},
    {"pre": "So x₁ = 10 ÷ 3. The numerator is ", "post": "", "answer": 10, "hint": "Top of the fraction.", "phase": "substitute"},
    {"pre": "And the denominator is ", "post": "", "answer": 3, "hint": "Bottom of the fraction.",
     "done": "x₁ = 10/3. It does not simplify, as 10 and 3 share no common factor."}
   ],
   [{"pattern": "wrong_denominator", "expect": [10, 2],
     "message": "10/2 uses x₀ instead of x₀ + 1. The denominator is 2 + 1 = 3, giving 10/3."}]),
 # S1
 P("\\(f(x) = x^3 - 4x - 1\\). Find \\(f(2)\\).",
   [-1], False, "single_value",
   "Cube 2, then subtract 4 times 2, then subtract 1.",
   [
    {"say": "Substitute x = 2 into f(x) = x³ − 4x − 1, piece by piece."},
    {"pre": "2³ = ", "post": "", "answer": 8, "hint": "2 × 2 × 2."},
    {"pre": "4 × 2 = ", "post": "", "answer": 8, "hint": "The 4x term."},
    {"pre": "f(2) = 8 − 8 − 1 = ", "post": "", "answer": -1, "hint": "8 − 8 − 1.", "phase": "substitute"},
    {"pre": "Check: 8 − 8 = 0, then 0 − 1 = ", "post": "", "answer": -1, "hint": "Take 1 off zero.",
     "done": "f(2) = −1."}
   ],
   [{"pattern": "forgot_constant", "expect": 0,
     "message": "0 forgets the −1. f(2) = 8 − 8 − 1 = −1."}]),
 # S2
 P("For \\(f(x) = x^3 - 4x - 1\\), find \\(f(3)\\).",
   [14], False, "single_value",
   "Cube 3, then subtract 4 times 3, then subtract 1.",
   [
    {"say": "Same function, now x = 3."},
    {"pre": "3³ = ", "post": "", "answer": 27, "hint": "3 × 3 × 3."},
    {"pre": "4 × 3 = ", "post": "", "answer": 12, "hint": "The 4x term."},
    {"pre": "f(3) = 27 − 12 − 1 = ", "post": "", "answer": 14, "hint": "27 − 12 − 1.", "phase": "substitute"},
    {"pre": "Check: 27 − 12 = 15, then 15 − 1 = ", "post": "", "answer": 14, "hint": "Take 1 off 15.",
     "done": "f(3) = 14. f(2) = −1 (negative), f(3) = 14 (positive): a sign change, root between 2 and 3."}
   ],
   [{"pattern": "squared_not_cubed", "expect": -4,
     "message": "Using 3² = 9 gives −4. You need 3³ = 27, so f(3) = 27 − 12 − 1 = 14."}]),
 # S3
 P("Using \\(x_{n+1} = \\sqrt[3]{4x_n + 1}\\) with \\(x_0 = 2\\), find \\(x_1\\) to 3 d.p.",
   [2.08], True, "single_value",
   "It is a cube root: work out 4 times 2 plus 1, then take the cube root.",
   [
    {"say": "One iteration of x_{n+1} = ∛(4x_n + 1) from x₀ = 2."},
    {"pre": "Inside the cube root: 4 × 2 + 1 = ", "post": "", "answer": 9, "hint": "4 times 2, plus 1."},
    {"pre": "x₁ = ∛9. To 3 d.p. this is ", "post": "", "answer": 2.08, "hint": "Cube root of 9.", "phase": "substitute"},
    {"pre": "Check: cube your answer. 2.08³ to the nearest whole number = ", "post": "", "answer": 9, "hint": "Cube 2.08.",
     "done": "2.08³ ≈ 9, so x₁ = ∛9 ≈ 2.080."}
   ],
   [{"pattern": "used_square_root", "expect": 3,
     "message": "3 is √9. The formula is a cube root: ∛9 ≈ 2.080."}]),
 # S4
 P("Find the average rate of change of \\(y = x^3\\) between \\(x = 1\\) and \\(x = 2\\).",
   [7], False, "single_value",
   "Cube both x-values, subtract, then divide by 2 minus 1.",
   [
    {"say": "Average rate = (change in y) ÷ (change in x) for y = x³."},
    {"pre": "f(1) = 1³ = ", "post": "", "answer": 1, "hint": "Cube 1."},
    {"pre": "f(2) = 2³ = ", "post": "", "answer": 8, "hint": "Cube 2."},
    {"pre": "Change in y = 8 − 1 = ", "post": "", "answer": 7, "hint": "Subtract the y-values.", "phase": "substitute"},
    {"pre": "Change in x = 2 − 1 = ", "post": "", "answer": 1, "hint": "Subtract the x-values."},
    {"pre": "Rate = 7 ÷ 1 = ", "post": "", "answer": 7, "hint": "Divide by 1.",
     "done": "Average rate of change is 7."}
   ],
   [{"pattern": "cubed_wrong", "expect": 5,
     "message": "5 comes from treating 2³ as 6. It is 2 × 2 × 2 = 8, so the rate is 8 − 1 = 7."}]),
 # S5 (fixed: was x^2-3x+1 giving f(1)=-1 (dup with S1); now x^2-4x+1)
 P("Show that \\(x^2 - 4x + 1 = 0\\) has a root between \\(x = 0\\) and \\(x = 1\\). What is \\(f(0)\\)?",
   [1], False, "single_value",
   "Put x = 0 in, so only the constant term is left.",
   [
    {"say": "f(x) = x² − 4x + 1. Substitute x = 0."},
    {"pre": "0² = ", "post": "", "answer": 0, "hint": "Zero squared."},
    {"pre": "4 × 0 = ", "post": "", "answer": 0, "hint": "The 4x term."},
    {"pre": "f(0) = 0 − 0 + 1 = ", "post": "", "answer": 1, "hint": "Only the constant is left.", "phase": "substitute"},
    {"pre": "Check: with x = 0 only the constant term survives. That constant is ", "post": "", "answer": 1, "hint": "The +1.",
     "done": "f(0) = 1."}
   ],
   [{"pattern": "zero_all", "expect": 0,
     "message": "Putting x = 0 leaves the constant term: f(0) = 0 − 0 + 1 = 1, not 0."}]),
 # S6 (fixed pair)
 P("For the same equation, what is \\(f(1)\\)?",
   [-2], False, "single_value",
   "Put x = 1 in and take care with the minus sign on 4x.",
   [
    {"say": "Same function f(x) = x² − 4x + 1, now x = 1."},
    {"pre": "1² = ", "post": "", "answer": 1, "hint": "One squared."},
    {"pre": "4 × 1 = ", "post": "", "answer": 4, "hint": "The 4x term."},
    {"pre": "f(1) = 1 − 4 + 1 = ", "post": "", "answer": -2, "hint": "1 − 4 + 1.", "phase": "substitute"},
    {"pre": "Check: 1 − 4 = −3, then −3 + 1 = ", "post": "", "answer": -2, "hint": "Add 1 to negative 3.",
     "done": "f(1) = −2. f(0) = 1 > 0 and f(1) = −2 < 0: a sign change, root between 0 and 1."}
   ],
   [{"pattern": "added_middle", "expect": 6,
     "message": "6 adds 4x instead of subtracting it. f(1) = 1 − 4 + 1 = −2."}]),
]

gold = [
 # G0 (fixed: was x0=2 giving 2.351 (dup with G4); now x0=3)
 P("Using \\(x_{n+1} = \\sqrt[3]{5x_n + 3}\\) with \\(x_0 = 3\\), find \\(x_1\\) to 3 d.p.",
   [2.621], True, "single_value",
   "Take the cube root of 5 times 3 plus 3.",
   [
    {"say": "One iteration of x_{n+1} = ∛(5x_n + 3) from x₀ = 3."},
    {"pre": "Inside the cube root: 5 × 3 + 3 = ", "post": "", "answer": 18, "hint": "5 times 3, plus 3."},
    {"pre": "x₁ = ∛18. To 3 d.p. = ", "post": "", "answer": 2.621, "hint": "Cube root of 18.", "phase": "substitute"},
    {"pre": "Check: cube 2.621 to the nearest whole number = ", "post": "", "answer": 18, "hint": "Cube your answer.",
     "done": "2.621³ ≈ 18, so x₁ ≈ 2.621."}
   ],
   [{"pattern": "used_square_root", "expect": 4.243,
     "message": "4.243 is √18. This is a cube root: ∛18 ≈ 2.621."}]),
 # G1
 P("\\(f(x) = x^3 + 2x - 7\\). Show a root lies between 1 and 2. What is \\(f(1.5)\\) to 3 d.p.?",
   [-0.625], True, "single_value",
   "Check f(1) and f(2) for the sign change, then work out 1.5 cubed plus 3 minus 7.",
   [
    {"say": "f(x) = x³ + 2x − 7. First check the interval, then find f(1.5)."},
    {"pre": "f(1) = 1 + 2 − 7 = ", "post": "", "answer": -4, "hint": "1 + 2 − 7."},
    {"pre": "f(2) = 8 + 4 − 7 = ", "post": "", "answer": 5, "hint": "8 + 4 − 7."},
    {"pre": "Sign change between 1 and 2. Now 1.5³ = ", "post": "", "answer": 3.375, "hint": "1.5 × 1.5 × 1.5.", "phase": "substitute"},
    {"pre": "f(1.5) = 3.375 + 2(1.5) − 7 = 3.375 + 3 − 7 = ", "post": "", "answer": -0.625, "hint": "3.375 + 3 − 7.",
     "done": "f(1.5) = −0.625. It is negative, so the root lies between 1.5 and 2."}
   ],
   [{"pattern": "dropped_linear", "expect": -4.625,
     "message": "−4.625 forgets the +2x term. f(1.5) = 3.375 + 3 − 7 = −0.625."}]),
 # G2
 P("The population P of a town is modelled by \\(P = 5000 \\times 1.03^t\\). Find the average annual rate of change between \\(t = 0\\) and \\(t = 10\\). Give to the nearest whole number.",
   [172], True, "single_value",
   "Find P at both times, subtract, then divide by 10 years.",
   [
    {"say": "Average rate = (P at t = 10 − P at t = 0) ÷ (10 − 0)."},
    {"pre": "P(0) = 5000 × 1.03⁰ = ", "post": "", "answer": 5000, "hint": "Anything to the power 0 is 1."},
    {"pre": "P(10) = 5000 × 1.03¹⁰, to the nearest whole number = ", "post": "", "answer": 6720, "hint": "1.03 to the power 10, times 5000."},
    {"pre": "Change in P = 6720 − 5000 = ", "post": "", "answer": 1720, "hint": "Subtract the two populations.", "phase": "substitute"},
    {"pre": "Rate = 1720 ÷ 10 = ", "post": "", "answer": 172, "hint": "Divide by the 10 years.",
     "done": "The population grows by about 172 people per year on average."}
   ],
   [{"pattern": "forgot_divide", "expect": 1720,
     "message": "1720 is the total change over 10 years. Divide by 10: 1720 ÷ 10 = 172."}]),
 # G3
 P("Using \\(x_{n+1} = \\sqrt{3x_n + 1}\\) with \\(x_0 = 3\\), find \\(x_2\\) to 3 d.p.",
   [3.238], True, "single_value",
   "Do two rounds: find x sub 1 first, then feed it back in for x sub 2.",
   [
    {"say": "Two iterations of x_{n+1} = √(3x_n + 1) from x₀ = 3."},
    {"pre": "First iteration inside the root: 3 × 3 + 1 = ", "post": "", "answer": 10, "hint": "3 times 3, plus 1."},
    {"pre": "x₁ = √10 to 3 d.p. = ", "post": "", "answer": 3.162, "hint": "Square root of 10."},
    {"pre": "Now use x₁ = 3.162. Inside the next root: 3 × 3.162 + 1 = ", "post": "", "answer": 10.486, "hint": "3 times 3.162, plus 1.", "phase": "substitute"},
    {"pre": "x₂ = √10.486 to 3 d.p. = ", "post": "", "answer": 3.238, "hint": "Square root of 10.486.",
     "done": "x₂ ≈ 3.238."}
   ],
   [{"pattern": "stopped_at_x1", "expect": 3.162,
     "message": "3.162 is x₁. One more step is needed: x₂ = √(3 × 3.162 + 1) ≈ 3.238."}]),
 # G4
 P("The equation \\(x^3 - 5x - 3 = 0\\) can be rearranged to \\(x = \\sqrt[3]{5x + 3}\\). Using \\(x_0 = 2\\), find \\(x_1\\) to 3 d.p.",
   [2.351], True, "single_value",
   "Use the cube root form: cube root of 5 times 2 plus 3.",
   [
    {"say": "The rearrangement gives x_{n+1} = ∛(5x_n + 3). Iterate once from x₀ = 2."},
    {"pre": "Inside the cube root: 5 × 2 + 3 = ", "post": "", "answer": 13, "hint": "5 times 2, plus 3."},
    {"pre": "x₁ = ∛13 to 3 d.p. = ", "post": "", "answer": 2.351, "hint": "Cube root of 13.", "phase": "substitute"},
    {"pre": "Check: cube 2.351 to the nearest whole number = ", "post": "", "answer": 13, "hint": "Cube your answer.",
     "done": "2.351³ ≈ 13, so x₁ ≈ 2.351, heading toward the root of x³ − 5x − 3 = 0."}
   ],
   [{"pattern": "used_square_root", "expect": 3.606,
     "message": "3.606 is √13. The rearrangement uses a cube root: ∛13 ≈ 2.351."}]),
]

problem_bank = {
 "bronze": bronze,
 "silver": silver,
 "gold": gold,
 "bronze_description": "Find an average rate of change from two points, and take one step of a simple iteration or sign check.",
 "silver_description": "Evaluate functions to test for a sign change, and carry out a single iteration, including cube roots and fractions.",
 "gold_description": "Run iterations to a set number of decimal places, and find average rates of change from real-life models."
}

pd = {
 "method_card": method_card,
 "topic_links": topic_links,
 "problem_bank": problem_bank,
 "related_videos": related_videos,
 "worked_examples": worked_examples,
 "tier_guides": tier_guides,
 "guided": guided
}

io.open("lesson_maths-aqa_ratio-proportion-L06.json", "w", encoding="utf-8").write(
    json.dumps(pd, indent=1, ensure_ascii=False))
print("written")
