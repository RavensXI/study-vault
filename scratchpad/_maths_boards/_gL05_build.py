# -*- coding: utf-8 -*-
import json, io

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

def mc(m, exp, msg, pat):
    return {"check": "common", "expect": exp, "message": msg, "pattern": pat}

# ---------- chart helpers ----------
def line_ds(points, color="#3b82f6", tension=0.35):
    return {"type": "line", "data": [{"x": round(x, 4), "y": round(y, 4)} for x, y in points],
            "tension": tension, "fill": False, "borderColor": color, "borderWidth": 2, "pointRadius": 0}

def chart(datasets, xmin, xmax, xstep, ymin, ymax, ystep):
    return {"type": "scatter", "data": {"datasets": datasets},
            "options": {"plugins": {"legend": {"display": False}},
                        "scales": {
                            "x": {"min": xmin, "max": xmax, "ticks": {"stepSize": xstep},
                                  "grid": {"color": "rgba(128,128,128,0.15)"}, "title": {"text": "x", "display": True}},
                            "y": {"min": ymin, "max": ymax, "ticks": {"stepSize": ystep},
                                  "grid": {"color": "rgba(128,128,128,0.15)"}, "title": {"text": "y", "display": True}}}}}

# reciprocal y = 6/x for b5
def frange(a, b, step):
    xs = []; x = a
    while x <= b + 1e-9:
        xs.append(round(x, 4)); x += step
    return xs

neg = [(x, 6.0/x) for x in frange(-6, -1, 0.5)]
pos = [(x, 6.0/x) for x in frange(1, 6, 0.5)]
chart_b5 = chart([line_ds(neg), line_ds(pos)], -6, 6, 1, -6, 6, 1)

# decay y = 0.5^x for s4
decay = [(x, 0.5**x) for x in frange(-2, 5, 0.25)]
chart_s4 = chart([line_ds(decay)], -2, 5, 1, 0, 4, 1)

# cubic y = x^3 - 9x for g1
cub = [(x, x**3 - 9*x) for x in frange(-3.4, 3.4, 0.2)]
chart_g1 = chart([line_ds(cub)], -3.5, 3.5, 1, -12, 12, 2)

# ---------- BRONZE ----------
bronze = [
 { "hint": "Cube the 3: multiply it by itself three times.",
   "display": "For \\(y = x^3\\), find \\(y\\) when \\(x = 3\\).",
   "solutions": [27], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("Reading a value off the curve means substituting x into the equation. Here y = x³ with x = 3, so multiply three 3's."),
     box("Square it first: 3 × 3 = ", 9, "Three times three."),
     box("Now the third 3: 9 × 3 = ", 27, "Nine times three.", phase="substitute"),
     box("Check by counting the copies: 3 × 3 × 3 = ", 27, "Three 3's multiplied.", done="27 sits high on the steep cubic, so (3, 27) is on the curve.", phase="substitute")],
   "misconceptions": [mc("common", 9, "y = x³ means 3 × 3 × 3 = 27, not 3 × 3 = 9. Cubing multiplies the number by itself three times.", "wrong_power")] },

 { "hint": "Cube the minus two; an odd power keeps the negative sign.",
   "display": "For \\(y = x^3\\), find \\(y\\) when \\(x = -2\\).",
   "solutions": [-8], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("Substitute x = −2 into y = x³. Cube it, tracking the sign."),
     box("(−2) × (−2) = ", 4, "Negative times negative is positive."),
     box("Now × (−2) again: 4 × (−2) = ", -8, "Positive times negative is negative.", phase="substitute"),
     box("Check the rule: an odd power keeps the sign, so (−2)³ = ", -8, "The minus survives cubing.", done="Odd power keeps the minus: y = −8.", phase="substitute")],
   "misconceptions": [mc("common", 8, "(−2)³ = −8, not +8. An odd power keeps the negative sign.", "sign_error")] },

 { "hint": "Divide 12 by 4.",
   "display": "For \\(y = \\frac{12}{x}\\), find \\(y\\) when \\(x = 4\\).",
   "solutions": [3], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("In y = 12/x the 12 sits on top and you divide it by x = 4."),
     box("The number on top of the fraction is ", 12, "It is 12/x, so 12 is the numerator."),
     box("Divide by x = 4: 12 ÷ 4 = ", 3, "How many 4's make 12?", phase="substitute"),
     box("Check by reversing it: 3 × 4 = ", 12, "It should rebuild the 12 on top.", done="3 × 4 = 12 rebuilds the top, so y = 3.", phase="substitute")],
   "misconceptions": [mc("common", 48, "y = 12/4 = 3, not 12 × 4 = 48. The x sits underneath, so you divide by it.", "wrong_formula")] },

 { "hint": "Double 2 three times; it is not 2 times 3.",
   "display": "For \\(y = 2^x\\), find \\(y\\) when \\(x = 3\\).",
   "solutions": [8], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("y = 2ˣ means multiply 2 by itself x times. Here x = 3, so three 2's."),
     box("First pair: 2 × 2 = ", 4, "Two twos."),
     box("Third 2: 4 × 2 = ", 8, "Four doubled.", phase="substitute"),
     box("Check it is not 2 × 3: three 2's give 2 × 2 × 2 = ", 8, "Three 2's multiplied.", done="2³ = 8, not 2 × 3 = 6.", phase="substitute")],
   "misconceptions": [mc("common", 6, "y = 2³ = 2 × 2 × 2 = 8, not 2 × 3 = 6. The power means repeated multiplication.", "wrong_power")] },

 { "hint": "Any non-zero number raised to the power 0 equals 1.",
   "display": "For \\(y = 3^x\\), find \\(y\\) when \\(x = 0\\).",
   "solutions": [1], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("The zero-power rule is quick once you see why it works. Build 3⁰ from 3¹."),
     box("Start from 3¹, that is just ", 3, "Any number to the power 1 is itself."),
     box("Going down one power divides by 3: 3 ÷ 3 = ", 1, "Three divided by three.", phase="substitute"),
     box("So any non-zero number to the power 0 equals ", 1, "The same landing value, 1.", done="By the zero-power rule, 3⁰ = 1.", phase="substitute")],
   "misconceptions": [mc("common", 0, "Any non-zero number to the power 0 equals 1, not 0.", "wrong_power")] },

 { "hint": "Only one of these curves has both axes as lines it never touches.",
   "display": "Which graph type has asymptotes at \\(x = 0\\) and \\(y = 0\\)?",
   "options": ["Cubic", "Quadratic", "Reciprocal", "Exponential"],
   "solutions": [2], "calculator": False, "input_type": "multiple_choice",
   "misconceptions": [mc("common", 3, "Only the reciprocal y = a/x has both axes as asymptotes. The exponential has just one (the x-axis, y = 0).", "confused_type")],
   "chart": chart_b5 },

 { "hint": "Divide 10 by minus 2; a positive over a negative is negative.",
   "display": "For \\(y = \\frac{10}{x}\\), find \\(y\\) when \\(x = -2\\).",
   "solutions": [-5], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("In y = 10/x divide the 10 on top by x = −2, minding the sign."),
     box("The number on top of the fraction is ", 10, "It is 10/x, so 10 is the numerator."),
     box("Divide by x = −2: 10 ÷ (−2) = ", -5, "Positive divided by negative is negative.", phase="substitute"),
     box("Check by reversing it: (−5) × (−2) = ", 10, "It should rebuild the 10 on top.", done="(−5) × (−2) = 10, so y = −5.", phase="substitute")],
   "misconceptions": [mc("common", 5, "y = 10/(−2) = −5. A positive divided by a negative gives a negative.", "sign_error")] },

 { "hint": "Cube the minus one first (watch the sign), then add 1.",
   "display": "For \\(y = x^3 + 1\\), find \\(y\\) when \\(x = -1\\).",
   "solutions": [0], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("Substitute x = −1 into y = x³ + 1. Cube first, then add 1."),
     box("(−1) × (−1) = ", 1, "Negative times negative is positive."),
     box("× (−1) again: 1 × (−1) = ", -1, "That is (−1)³; the minus survives.", phase="substitute"),
     box("Now add 1: −1 + 1 = ", 0, "Count up one from −1.", done="(−1)³ + 1 = −1 + 1 = 0.", phase="substitute")],
   "misconceptions": [mc("common", 2, "(−1)³ = −1, not +1, so (−1)³ + 1 = −1 + 1 = 0. An odd power keeps the minus.", "sign_error")] },
]

# ---------- SILVER ----------
silver = [
 { "hint": "Work out each term at x = −1 separately, minding the double negative.",
   "display": "For \\(y = x^3 - 3x\\), find \\(y\\) when \\(x = -1\\).",
   "solutions": [2], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("Take the two terms of x³ − 3x at x = −1, then combine."),
     box("The cube: (−1)³ = ", -1, "An odd power keeps the minus."),
     box("The −3x term: −3 × (−1) = ", 3, "Negative times negative is positive.", phase="substitute"),
     box("Add the two terms: −1 + 3 = ", 2, "Count up 3 from −1.", done="y = 2; the double negative made −3x into + 3.", phase="substitute")],
   "misconceptions": [mc("common", -4, "y = (−1)³ − 3(−1) = −1 + 3 = 2. Getting −4 misses that −3 × (−1) = +3, not −3.", "sign_error")] },

 { "hint": "A negative power means the reciprocal, so 2 to the minus 2 is one quarter.",
   "display": "For \\(y = 2^x\\), find \\(y\\) when \\(x = -2\\). Give as a decimal.",
   "solutions": [0.25], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("A negative power means 'one over'. Build 2⁻² from 2²."),
     box("First 2² = 2 × 2 = ", 4, "Two squared."),
     box("So 2⁻² = 1 ÷ 4 = ", 0.25, "A quarter as a decimal.", phase="substitute"),
     box("Check by reversing: 0.25 × 4 = ", 1, "It should rebuild the 1 on top.", done="2⁻² = 1/4 = 0.25.", phase="substitute")],
   "misconceptions": [mc("common", -4, "2⁻² = 1/2² = 1/4 = 0.25, not −4. A negative power means the reciprocal, not a negative answer.", "wrong_power")] },

 { "hint": "The point gives 5 = k/3, so multiply 5 by 3.",
   "display": "\\(y = \\frac{k}{x}\\) passes through \\((3, 5)\\). Find \\(k\\).",
   "solutions": [15], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("The point (3, 5) means x = 3 gives y = 5. Put those into y = k/x."),
     box("The equation becomes 5 = k ÷ 3. Read off the y value on the left: ", 5, "The point's y-coordinate."),
     box("Multiply both sides by 3 to free k: k = 5 × 3 = ", 15, "Five times three.", phase="substitute"),
     box("Check: k ÷ x = 15 ÷ 3 = ", 5, "It should rebuild the 5.", done="15 ÷ 3 = 5 matches the point, so k = 15.", phase="substitute")],
   "misconceptions": [mc("common", 0.6, "The point gives 5 = k/3, so k = 5 × 3 = 15. Writing 5 = 3/k instead gives k = 0.6, which is wrong: k is on top.", "wrong_formula")] },

 { "hint": "Cube the 2, then subtract 12 times 2.",
   "display": "For \\(y = x^3 - 12x\\), when \\(x = 2\\), \\(y = ?\\)",
   "solutions": [-16], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("Take the two terms of x³ − 12x at x = 2, then combine."),
     box("The cube: 2³ = 2 × 2 × 2 = ", 8, "Three 2's multiplied."),
     box("The 12x term: 12 × 2 = ", 24, "Multiply the 12 by x.", phase="substitute"),
     box("Subtract: 8 − 24 = ", -16, "Count down 24 from 8.", done="y = 8 − 24 = −16.", phase="substitute")],
   "misconceptions": [mc("common", -4, "y = 2³ − 12(2) = 8 − 24 = −16. Using −12 instead of −12 × 2 gives −4. Multiply the 12 by x first.", "wrong_sub")] },

 { "hint": "A base between 0 and 1 makes the curve shrink as x grows.",
   "display": "Which equation matches a graph that decays toward 0 as x increases?",
   "options": ["\\(y = 2^x\\)", "\\(y = 0.5^x\\)", "\\(y = x^3\\)", "\\(y = \\frac{1}{x}\\)"],
   "solutions": [1], "calculator": False, "input_type": "multiple_choice",
   "misconceptions": [mc("common", 0, "y = 0.5ˣ decays because the base 0.5 is between 0 and 1. y = 2ˣ grows, since its base is above 1.", "confused_type")],
   "chart": chart_s4 },

 { "hint": "Square the 5: multiply it by itself, not by 2.",
   "display": "For \\(y = 5^x\\), find \\(y\\) when \\(x = 2\\).",
   "solutions": [25], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("y = 5ˣ means multiply 5 by itself x times, so 5² is two 5's."),
     box("Write it out: 5² = 5 × 5. Read the base being multiplied: ", 5, "The number in the power is 5."),
     box("Now multiply the two 5's: 5 × 5 = ", 25, "Five times five.", phase="substitute"),
     box("Check it is not 5 × 2: two 5's give ", 25, "Not 10; it is 5 × 5.", done="5² = 25, not 5 × 2 = 10.", phase="substitute")],
   "misconceptions": [mc("common", 10, "y = 5² = 5 × 5 = 25, not 5 × 2 = 10. The power means multiply 5 by itself twice.", "wrong_power")] },

 { "hint": "Divide minus 8 by 2; the minus on top stays.",
   "display": "For \\(y = \\frac{-8}{x}\\), find \\(y\\) when \\(x = 2\\).",
   "solutions": [-4], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("In y = −8/x the top is −8. Divide it by x = 2."),
     box("The number on top of the fraction is ", -8, "The numerator is −8, including its sign."),
     box("Divide by x = 2: −8 ÷ 2 = ", -4, "A negative divided by a positive is negative.", phase="substitute"),
     box("Check by reversing it: (−4) × 2 = ", -8, "It should rebuild the −8 on top.", done="(−4) × 2 = −8, so y = −4.", phase="substitute")],
   "misconceptions": [mc("common", 4, "y = −8/2 = −4. The minus on top stays, so the answer is negative.", "sign_error")] },
]

# ---------- GOLD ----------
gold = [
 { "hint": "Work out 3 to the power 4 first, then multiply by 2.",
   "display": "\\(y = 2 \\times 3^x\\). Find \\(y\\) when \\(x = 4\\).",
   "solutions": [162], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("Do the power first, then multiply by 2. Never combine 2 and 3 before the power."),
     box("Build 3⁴ step by step: 3 × 3 = ", 9, "Three squared."),
     box("× 3 again: 9 × 3 = ", 27, "That is 3³."),
     box("× 3 once more: 27 × 3 = ", 81, "That is 3⁴.", phase="substitute"),
     box("Now multiply by 2: 2 × 81 = ", 162, "Double 81.", done="y = 2 × 3⁴ = 2 × 81 = 162.", phase="substitute")],
   "misconceptions": [mc("common", 1296, "Work the power first: 3⁴ = 81, then × 2 = 162. Doing (2 × 3)⁴ = 6⁴ = 1296 multiplies before the power, which is wrong.", "wrong_power")] },

 { "hint": "Factor out x, then solve x squared equals 9 for the positive root.",
   "display": "\\(y = x^3 - 9x\\). Find the value of \\(x\\) (positive) where \\(y = 0\\) and \\(x \\neq 0\\).",
   "solutions": [3], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("Set y = 0 and factor: x³ − 9x = x(x² − 9). Look for the positive root."),
     box("Factor out x. The bracket x² − 9 is zero when x² = ", 9, "Set x² − 9 = 0, so x² = 9."),
     box("Take the positive square root: x = √9 = ", 3, "What number squared is 9?", phase="substitute"),
     box("Check: 3³ − 9 × 3 = 27 − 27 = ", 0, "It should give y = 0.", done="x = 3 gives y = 0 and is positive, so x = 3.", phase="substitute")],
   "misconceptions": [mc("common", 9, "x³ − 9x = x(x² − 9) = 0 gives x² = 9, so x = 3. Stopping at x² = 9 and writing 9 forgets the square root.", "wrong_factoring")],
   "chart": chart_g1 },

 { "hint": "Take the + 2 across first, then multiply by 4.",
   "display": "\\(y = \\frac{a}{x} + 2\\) passes through \\((4, 5)\\). Find \\(a\\).",
   "solutions": [12], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("The point (4, 5) means x = 4 gives y = 5. Put those into y = a/x + 2."),
     box("The equation is 5 = a ÷ 4 + 2. Subtract the 2: a ÷ 4 = 5 − 2 = ", 3, "Take the + 2 across first."),
     box("Multiply both sides by 4 to free a: a = 3 × 4 = ", 12, "Three times four.", phase="substitute"),
     box("Check: a ÷ 4 + 2 = 12 ÷ 4 + 2 = 3 + 2 = ", 5, "It should rebuild the 5.", done="12 ÷ 4 + 2 = 5 matches the point, so a = 12.", phase="substitute")],
   "misconceptions": [mc("common", 20, "5 = a/4 + 2, so a/4 = 3 and a = 12. Forgetting the + 2 gives a/4 = 5 and a = 20.", "wrong_formula")] },

 { "hint": "The base is below 1, so just work out 10 times 0.8.",
   "display": "For \\(y = 10 \\times 0.8^x\\), find \\(y\\) when \\(x = 1\\).",
   "solutions": [8], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("The base 0.8 is below 1, so this is decay. At x = 1 you only need 0.8¹."),
     box("0.8 to the power 1 is just ", 0.8, "Any number to the power 1 is itself."),
     box("Multiply by 10: 10 × 0.8 = ", 8, "Ten times eight tenths.", phase="substitute"),
     box("Check it fell from the start value: it began at 10 and dropped to ", 8, "Decay means it gets smaller.", done="y = 10 × 0.8 = 8, a fall of 20%.", phase="substitute")],
   "misconceptions": [mc("common", 12, "0.8 is below 1, so this is decay: y = 10 × 0.8 = 8. Treating it as 20% growth (× 1.2) gives 12, which is wrong.", "confused_type")] },

 { "hint": "Work out each term at x = 2, then add and subtract.",
   "display": "For \\(y = x^3 + x^2 - 6x\\), find \\(y\\) when \\(x = 2\\).",
   "solutions": [0], "calculator": False, "input_type": "single_value",
   "guided_steps": [
     sayonly("Work out the three terms of x³ + x² − 6x at x = 2, then combine."),
     box("The cube: 2³ = ", 8, "Three 2's multiplied."),
     box("The square: 2² = ", 4, "Two squared."),
     box("The −6x term: 6 × 2 = ", 12, "Multiply the 6 by x.", phase="substitute"),
     box("Combine: 8 + 4 − 12 = ", 0, "Add the first two, then take 12.", done="y = 8 + 4 − 12 = 0, so x = 2 is a root.", phase="substitute")],
   "misconceptions": [mc("common", 6, "y = 2³ + 2² − 6(2) = 8 + 4 − 12 = 0. Using −6 instead of −6 × 2 gives 6. Multiply the 6 by x.", "wrong_sub")] },
]

# ---------- guided (opener + teach) ----------
opener = {
  "label": "Before any algebra",
  "display": "Day 0: 1p<br>Day 1: 2p<br>Day 2: 4p<br>Day 3: ?",
  "steps": [
    box("How many pence on day 3? ", 8, "Each day doubles: 1, 2, 4, then double once more.",
        say="A magic penny doubles every day. On day 0 you have 1p, and each day it doubles. No algebra, just keep doubling."),
    box("And on day 4? ", 16, "Double the 8.", say="Keep going, one more day."),
    sayonly("You just built y = 2ˣ: after x days you have 2ˣ pence, so 2⁴ = 16p. Doubling over and over is an <strong>exponential</strong>, and it grows terrifyingly fast. This lesson also meets <strong>cubes</strong> y = x³ (a number times itself three times) and <strong>sharing</strong> y = a/x. Every one is the same move: pick x, work out y.")
  ]
}

teach = {
  "bronze": {
    "label": "Together: your first one",
    "display": "Build points on \\(y = x^3\\)",
    "steps": [
      box("When x = 2: 2 × 2 = ", 4, "Two times two.",
          say="To sketch a curve you substitute x values and read off y. Take y = x³, where cubing means three copies multiplied."),
      box("then × 2 again: 4 × 2 = ", 8, "Four doubled.", done="That is 2³, so (2, 8) is on the curve."),
      box("When x = 4: 4 × 4 = ", 16, "Four times four."),
      box("then × 4 again: 16 × 4 = ", 64, "Sixteen times four.", done="Points (2, 8) and (4, 64) climb faster and faster: the S-shaped cubic.")
    ]
  },
  "silver": {
    "label": "Together: the silver move",
    "display": "Solve \\(y = x^3 + 2\\) at a negative input",
    "steps": [
      box("(−2) × (−2) = ", 4, "Negative times negative is positive.",
          say="Silver adds negative inputs and a shift. Take y = x³ + 2 at x = −2. Cube first, minding the sign, then add 2."),
      box("× (−2) again: 4 × (−2) = ", -8, "Positive times negative is negative.", done="An odd power keeps the minus, so (−2)³ = −8."),
      box("add the 2: −8 + 2 = ", -6, "Count up 2 from −8."),
      box("Check at x = 0: 0³ + 2 = ", 2, "Zero cubed is 0.", done="The + 2 lifts every point up by 2.")
    ]
  },
  "gold": {
    "label": "Together: the gold move",
    "display": "Solve \\(y = a \\cdot b^x\\) through (1, 12) and (2, 48)",
    "steps": [
      box("At x = 1: a × b = ", 12, "The point (1, 12) means y = 12.",
          say="Gold hides the numbers. y = a·bˣ passes through (1, 12) and (2, 48). Substitute both points."),
      box("At x = 2: a × b² = ", 48, "The point (2, 48) means y = 48."),
      box("b = 48 ÷ 12 = ", 4, "Divide the second by the first; the a cancels.",
          say="Divide the second equation by the first: the a cancels and one b cancels, leaving b.", done="The a vanished, giving b straight away."),
      box("then a = 12 ÷ b = 12 ÷ 4 = ", 3, "Use a × b = 12 with b = 4."),
      box("Check: a × b² = 3 × 4² = 3 × 16 = ", 48, "Three times sixteen.", done="Rebuilds 48, so a = 3, b = 4.")
    ]
  }
}

# ---------- tier_guides ----------
tier_guides = {
  "bronze": {
    "title": "Bronze: reading a value off a curve",
    "steps": [
      "<strong>Substitute</strong> the x value into the equation and work out y. A power means repeated multiplication: \\(x^3 = x \\times x \\times x\\).",
      "Know the three shapes: <strong>cubic</strong> \\(y=x^3\\) is an S-curve through the origin, <strong>reciprocal</strong> \\(y=\\frac{a}{x}\\) has two branches, and <strong>exponential</strong> \\(y=k^x\\) passes through \\((0,1)\\).",
      "An <strong>asymptote</strong> is a line the curve creeps towards but never touches. For \\(y=\\frac{1}{x}\\) both axes are asymptotes."
    ],
    "example": {
      "question": "Find y when x = 4 on the graph y = x³.",
      "steps": [
        {"label": "Substitute", "content": "<p>\\(y = 4^3 = 4 \\times 4 \\times 4\\).</p>"},
        {"label": "Compute", "content": "<p>\\(4 \\times 4 = 16\\), then \\(16 \\times 4 = 64\\).</p>"},
        {"label": "Check", "content": "<p>64 is large and positive, on the steep rising part of the S-curve.</p>"},
        {"label": "Answer", "content": "<p>\\(y = 64\\); the graph is a <strong>cubic</strong>.</p>", "isAnswer": True, "is_answer": True}
      ]
    }
  },
  "silver": {
    "title": "Silver: signs, shifts and decay",
    "steps": [
      "With <strong>negative</strong> inputs, track the sign. An odd power keeps the minus: \\((-2)^3 = -8\\). Squaring makes it positive.",
      "A number added on, like \\(y=x^3+1\\), <strong>shifts</strong> the whole curve up. Work out the power first, then add.",
      "A base between 0 and 1, like \\(0.5^x\\), is <strong>decay</strong>: y shrinks each step. A negative power means the reciprocal: \\(2^{-1}=\\frac{1}{2}\\)."
    ],
    "example": {
      "question": "Find y when x = -2 on y = x³ - 4.",
      "steps": [
        {"label": "Cube the sign", "content": "<p>\\((-2)^3 = -8\\). An odd power keeps the minus.</p>"},
        {"label": "Shift", "content": "<p>\\(-8 - 4 = -12\\).</p>"},
        {"label": "Check", "content": "<p>Negative and below the origin, as expected for \\(x<0\\) on a cubic pulled down by 4.</p>"},
        {"label": "Answer", "content": "<p>\\(y = -12\\).</p>", "isAnswer": True, "is_answer": True}
      ]
    }
  },
  "gold": {
    "title": "Gold: recover the rule, then solve",
    "steps": [
      "The equation hides unknown numbers. Substitute each given point to get equations, then combine them.",
      "For \\(y=a \\cdot b^x\\) through two points, <strong>divide</strong> one equation by the other: the \\(a\\) cancels and \\(b\\) drops out.",
      "For a <strong>root</strong>, set \\(y=0\\) and <strong>factor</strong>: \\(x^3-9x=x(x-3)(x+3)\\), so the curve crosses at those x-values."
    ],
    "example": {
      "question": "A curve y = a·bˣ passes through (1, 10) and (2, 50). Find b.",
      "steps": [
        {"label": "Substitute", "content": "<p>\\(a \\cdot b = 10\\) and \\(a \\cdot b^2 = 50\\).</p>"},
        {"label": "Divide", "content": "<p>\\(50 \\div 10 = b\\), so \\(b = 5\\).</p>"},
        {"label": "Check", "content": "<p>\\(a = 10 \\div 5 = 2\\), and \\(2 \\times 5^2 = 50\\).</p>"},
        {"label": "Answer", "content": "<p>\\(b = 5\\).</p>", "isAnswer": True, "is_answer": True}
      ]
    }
  }
}

# ---------- method_card (4 steps, slim) ----------
method_card = {
  "title": "Cubic, Reciprocal & Exponential Graphs",
  "steps": [
    "Substitute x values into the equation to get points; a power means repeated multiplication.",
    "Cubic \\(y=x^3\\): an S-curve through the origin. A negative coefficient flips it.",
    "Reciprocal \\(y=\\frac{a}{x}\\): two branches, with both axes as asymptotes.",
    "Exponential \\(y=k^x\\): passes through \\((0,1)\\), growing if \\(k>1\\) and decaying if \\(0<k<1\\)."
  ],
  "content": "<p>These three curves each come from a rule you substitute into. A <strong>cubic</strong> \\(y=x^3\\) makes an S-shape through the origin, rising steeply. A <strong>reciprocal</strong> \\(y=\\frac{a}{x}\\) splits into two branches that hug the axes but never touch them (the axes are <strong>asymptotes</strong>). An <strong>exponential</strong> \\(y=k^x\\) passes through \\((0,1)\\) and either grows fast (\\(k>1\\)) or decays (\\(0<k<1\\)), with the x-axis as an asymptote.</p>",
  "example": "<p><strong>Sketch \\(y=2^x\\).</strong> It is exponential growth (\\(k=2\\)). Key points: \\((0,1)\\), \\((1,2)\\), \\((2,4)\\), \\((-1,0.5)\\). The curve rises steeply to the right and creeps towards the x-axis (its asymptote) on the left.</p>"
}

# ---------- worked_examples (preserve content, fix em dashes -> colon) ----------
worked_examples = [
  {"question": "For \\(y = x^3 - 4x\\), find y when x = 2.", "difficulty": "Bronze",
   "steps": [
     {"label": "Step 1: Substitute", "content": "<p>\\(y = (2)^3 - 4(2) = 8 - 8 = 0\\)</p>"},
     {"label": "Answer", "content": "<p>\\(y = 0\\) (so \\(x = 2\\) is a root)</p>", "isAnswer": True, "is_answer": True}]},
  {"question": "For \\(y = \\frac{6}{x}\\), find y when x = 3.", "difficulty": "Silver",
   "steps": [
     {"label": "Step 1: Substitute", "content": "<p>\\(y = \\frac{6}{3} = 2\\)</p>"},
     {"label": "Answer", "content": "<p>\\(y = 2\\)</p>", "isAnswer": True, "is_answer": True}]},
  {"question": "For \\(y = 2^x\\), find y when x = 5.", "difficulty": "Gold",
   "steps": [
     {"label": "Step 1: Calculate", "content": "<p>\\(y = 2^5 = 32\\)</p>"},
     {"label": "Answer", "content": "<p>\\(y = 32\\)</p>", "isAnswer": True, "is_answer": True}]}
]

pd = {
  "guided": {"teach": teach, "opener": opener},
  "method_card": method_card,
  "tier_guides": tier_guides,
  "topic_links": {"prerequisites": []},
  "problem_bank": {
    "gold": gold, "bronze": bronze, "silver": silver,
    "gold_description": "Recover unknown constants from given points, evaluate multi-term cubics, and solve growth or root problems in several steps.",
    "bronze_description": "Substitute a simple value into a cubic, reciprocal or exponential, and recognise each graph's shape and asymptotes.",
    "silver_description": "Handle negative inputs, shifted cubics, exponential decay and negative powers, and reason about signs and quadrants."
  },
  "related_videos": [],
  "worked_examples": worked_examples
}

with io.open("lesson_maths-ocr_graphs-L05.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("written. pb counts", {t: len(pd['problem_bank'][t]) for t in ['bronze','silver','gold']})
print("charts on:", [(t,i) for t in ['bronze','silver','gold'] for i,p in enumerate(pd['problem_bank'][t]) if 'chart' in p])
