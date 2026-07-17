# -*- coding: utf-8 -*-
"""Build guided + diagrams practice_data for maths-eduqas graphs-L05.
Writes two shard files (guided, guided+diagrams). No PATCH here."""
import json, copy, os

OUTDIR = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards"

# ---- verified opener SVG (exponential 2^x, count vs hours) ----
OPENER_SVG = (
 '<svg viewBox="0 0 260 200" role="img" aria-label="Exponential curve of bacteria count against hours: 1 at hour 0, doubling to 2, 4, 8, 16 and 32 by hour 5" style="max-width:260px" font-family="Inter, sans-serif">'
 '<line x1="40" y1="15" x2="40" y2="165" stroke="currentColor" stroke-width="1.2"/>'
 '<line x1="40" y1="165" x2="235" y2="165" stroke="currentColor" stroke-width="1.2"/>'
 '<line x1="37" y1="165.0" x2="40" y2="165.0" stroke="currentColor" stroke-width="1"/><text x="33" y="168.0" font-size="9" fill="currentColor" text-anchor="end">0</text>'
 '<line x1="37" y1="127.5" x2="40" y2="127.5" stroke="currentColor" stroke-width="1"/><text x="33" y="130.5" font-size="9" fill="currentColor" text-anchor="end">8</text>'
 '<line x1="37" y1="90.0" x2="40" y2="90.0" stroke="currentColor" stroke-width="1"/><text x="33" y="93.0" font-size="9" fill="currentColor" text-anchor="end">16</text>'
 '<line x1="37" y1="52.5" x2="40" y2="52.5" stroke="currentColor" stroke-width="1"/><text x="33" y="55.5" font-size="9" fill="currentColor" text-anchor="end">24</text>'
 '<line x1="37" y1="15.0" x2="40" y2="15.0" stroke="currentColor" stroke-width="1"/><text x="33" y="18.0" font-size="9" fill="currentColor" text-anchor="end">32</text>'
 '<line x1="40.0" y1="165" x2="40.0" y2="168" stroke="currentColor" stroke-width="1"/><text x="40.0" y="178" font-size="9" fill="currentColor" text-anchor="middle">0</text>'
 '<line x1="79.0" y1="165" x2="79.0" y2="168" stroke="currentColor" stroke-width="1"/><text x="79.0" y="178" font-size="9" fill="currentColor" text-anchor="middle">1</text>'
 '<line x1="118.0" y1="165" x2="118.0" y2="168" stroke="currentColor" stroke-width="1"/><text x="118.0" y="178" font-size="9" fill="currentColor" text-anchor="middle">2</text>'
 '<line x1="157.0" y1="165" x2="157.0" y2="168" stroke="currentColor" stroke-width="1"/><text x="157.0" y="178" font-size="9" fill="currentColor" text-anchor="middle">3</text>'
 '<line x1="196.0" y1="165" x2="196.0" y2="168" stroke="currentColor" stroke-width="1"/><text x="196.0" y="178" font-size="9" fill="currentColor" text-anchor="middle">4</text>'
 '<line x1="235.0" y1="165" x2="235.0" y2="168" stroke="currentColor" stroke-width="1"/><text x="235.0" y="178" font-size="9" fill="currentColor" text-anchor="middle">5</text>'
 '<text x="137" y="193" font-size="9" fill="currentColor" text-anchor="middle">hours (x)</text>'
 '<text x="12" y="90" font-size="9" fill="currentColor" text-anchor="middle" transform="rotate(-90 12 90)">count (y)</text>'
 '<polyline points="40.0,160.3 79.0,155.6 118.0,146.2 157.0,127.5 196.0,90.0 235.0,15.0" fill="none" stroke="#f59e0b" stroke-width="2"/>'
 '<circle cx="40.0" cy="160.3" r="2.6" fill="#f59e0b"/><circle cx="79.0" cy="155.6" r="2.6" fill="#f59e0b"/><circle cx="118.0" cy="146.2" r="2.6" fill="#f59e0b"/>'
 '<circle cx="157.0" cy="127.5" r="2.6" fill="#f59e0b"/><circle cx="196.0" cy="90.0" r="2.6" fill="#f59e0b"/><circle cx="235.0" cy="15.0" r="2.6" fill="#f59e0b"/></svg>'
 '<span class="figure-caption">Bacteria doubling every hour</span>'
 '<p>One bacterium splits into two every hour. Start with 1, then 2, then 4, then 8...</p>'
)

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def say(text):
    return {"say": text}

def mc(msg):
    return [{"pattern": "confusion", "check": "confusion", "expect": None, "message": msg, "note": "MC"}]

def mis(pattern, expect, msg, note):
    return [{"pattern": pattern, "check": pattern, "expect": expect, "message": msg, "note": note}]

# ============ BRONZE ============
bronze = []

# b0 y=x^3 x=2 -> 8  (completion problem)
bronze.append({
 "display": "For \\(y = x^3\\), find \\(y\\) when \\(x = 2\\).",
 "solutions": [8], "calculator": False, "input_type": "single_value",
 "hint": "Cube 2 by multiplying it by itself three times.",
 "misconceptions": mis("cube_as_times_3", 6,
   "A cube means multiply the number by itself three times: 2³ = 2 × 2 × 2 = 8. If you got 6 you did 2 × 3.",
   "error: 2x3=6"),
 "guided_steps": [
   say("Cubing means multiplying the number by itself three times."),
   box("First two 2s: 2 × 2 = ", 4, "Two times two."),
   box("Now the third 2: 4 × 2 = ", 8, "Multiply your answer by 2 again.", phase="substitute"),
   box("Count them back, 2 × 2 × 2 = ", 8, "All three twos multiplied.", phase="substitute", done="Three 2s multiplied give 8, so y = 8."),
 ]})

# b1 y=x^3 x=-2 -> -8
bronze.append({
 "display": "For \\(y = x^3\\), find \\(y\\) when \\(x = -2\\).",
 "solutions": [-8], "calculator": False, "input_type": "single_value",
 "hint": "Cube −2: three negatives multiplied give a negative.",
 "misconceptions": mis("neg_cube_sign", 8,
   "A negative number cubed stays negative: (−2)³ = (−2)(−2)(−2) = −8. Getting +8 means a minus sign was lost.",
   "error: sign dropped -> +8"),
 "guided_steps": [
   say("A negative number cubed: multiply three negatives together."),
   box("First two: (−2) × (−2) = ", 4, "Negative times negative is positive."),
   box("Now times the third (−2): 4 × (−2) = ", -8, "Positive times negative is negative.", phase="substitute"),
   box("Three minuses give a minus, so type y: ", -8, "Odd number of minuses stays negative.", phase="substitute", done="An odd number of negatives stays negative: y = −8."),
 ]})

# b2 MC type of y=4/x -> index 2
bronze.append({
 "display": "What type of graph does \\(y = \\frac{4}{x}\\) produce?",
 "options": ["Straight line", "Parabola (U shape)", "Reciprocal (two branches)", "Cubic (S shape)"],
 "solutions": [2], "calculator": False, "input_type": "multiple_choice",
 "hint": "Think which curve splits into two branches either side of the y-axis.",
 "misconceptions": mc("a/x gives a reciprocal graph, two separate curves either side of the y-axis.")})

# b3 y=2^x x=0 -> 1
bronze.append({
 "display": "For \\(y = 2^x\\), find \\(y\\) when \\(x = 0\\).",
 "solutions": [1], "calculator": False, "input_type": "single_value",
 "hint": "Any number to the power 0 is 1.",
 "misconceptions": mis("zero_power_zero", 0,
   "Any number to the power 0 equals 1, not 0. So 2⁰ = 1.", "error: thinks 2^0=0"),
 "guided_steps": [
   say("Let us build down the powers of 2 to see what 2⁰ must be."),
   box("2² = 2 × 2 = ", 4, "Two times two."),
   box("2¹ = ", 2, "Just 2 itself."),
   box("Each step down halves, so 2⁰ = 2 ÷ 2 = ", 1, "Two divided by two.", phase="substitute"),
   box("So any base to the power 0 equals ", 1, "The pattern lands on 1.", phase="substitute", done="2⁰ = 1, and the same is true for any base."),
 ]})

# b4 y=2^x x=4 -> 16  (FIXED from x=3->8 duplicate)
bronze.append({
 "display": "For \\(y = 2^x\\), find \\(y\\) when \\(x = 4\\).",
 "solutions": [16], "calculator": False, "input_type": "single_value",
 "hint": "2⁴ means four 2s multiplied together.",
 "misconceptions": mis("power_as_times", 8,
   "A power means repeated multiplication: 2⁴ = 2 × 2 × 2 × 2 = 16. Doing 2 × 4 gives 8.", "error: 2x4=8"),
 "guided_steps": [
   say("A power tells you how many 2s to multiply. 2⁴ is four 2s."),
   box("First two 2s: 2 × 2 = ", 4, "Two times two."),
   box("Times the third 2: 4 × 2 = ", 8, "Double it.", phase="substitute"),
   box("Times the fourth 2: 8 × 2 = ", 16, "Double once more.", phase="substitute", done="Four 2s multiplied give 16, so y = 16."),
 ]})

# b5 y=6/x x=3 -> 2
bronze.append({
 "display": "For \\(y = \\frac{6}{x}\\), find \\(y\\) when \\(x = 3\\).",
 "solutions": [2], "calculator": False, "input_type": "single_value",
 "hint": "Divide the top number by x: 6 ÷ 3.",
 "misconceptions": mis("reciprocal_flip", 0.5,
   "Divide 6 by x, not x by 6: y = 6 ÷ 3 = 2. Doing 3 ÷ 6 gives 0.5.", "error: 3/6=0.5"),
 "guided_steps": [
   say("A reciprocal means divide the top number by x. Here that is 6 ÷ 3."),
   box("6 ÷ 3 = ", 2, "Six shared into three."),
   box("Check by multiplying back: 2 × 3 = ", 6, "Should rebuild the 6 on top.", phase="substitute"),
   box("It rebuilds 6, so type the value of y: ", 2, "The division result.", phase="substitute", done="y = 2, confirmed by the check."),
 ]})

# b6 MC shape of y=x^3-1 -> index 1 (S shape)
bronze.append({
 "display": "What shape does the graph \\(y = x^3 - 1\\) have?",
 "options": ["U shape", "S shape", "Two branches", "Straight line"],
 "solutions": [1], "calculator": False, "input_type": "multiple_choice",
 "hint": "The highest power is x³, which gives an S-shaped curve.",
 "misconceptions": mc("The highest power is x³, so this is a cubic, an S-shaped curve.")})

# b7 y=3^x x=2 -> 9
bronze.append({
 "display": "For \\(y = 3^x\\), find \\(y\\) when \\(x = 2\\).",
 "solutions": [9], "calculator": False, "input_type": "single_value",
 "hint": "3² means 3 × 3, not 3 × 2.",
 "misconceptions": mis("power_as_times", 6,
   "3² means two 3s multiplied: 3 × 3 = 9. Doing 3 × 2 gives 6.", "error: 3x2=6"),
 "guided_steps": [
   say("A power of 2 means multiply the base by itself once."),
   box("Write it out: 3 × 3 = ", 9, "Three times three."),
   box("See the trap route: 3 × 2 = ", 6, "This is what NOT to do.", phase="substitute"),
   box("The power route is correct, so type the real y: ", 9, "Use the 3 × 3 answer.", phase="substitute", done="3² = 3 × 3 = 9, not 6. So y = 9."),
 ]})

# ============ SILVER (reordered: walkable first, MC last) ============
silver = []

# s0 y=x^3-8 x=2 -> 0 (completion problem)
silver.append({
 "display": "For \\(y = x^3 - 8\\), find \\(y\\) when \\(x = 2\\).",
 "solutions": [0], "calculator": False, "input_type": "single_value",
 "hint": "Cube the 2 first, then subtract 8.",
 "misconceptions": mis("cube_as_times_3", -2,
   "Cube the x, do not multiply it by 3: 2³ = 8, so y = 8 − 8 = 0. Using 3 × 2 = 6 gives −2.", "error: 3x -> 6-8=-2"),
 "guided_steps": [
   say("Work out the cube first, then subtract 8."),
   box("Cube the 2: 2 × 2 × 2 = ", 8, "Three 2s multiplied."),
   box("Subtract 8: 8 − 8 = ", 0, "Take eight from eight.", phase="substitute"),
   box("So x = 2 gives y = ", 0, "Eight minus eight.", phase="substitute", done="y = 0, so the curve crosses the x-axis at x = 2."),
 ]})

# s1 y=-3/x x=-1 -> 3
silver.append({
 "display": "For \\(y = \\frac{-3}{x}\\), find \\(y\\) when \\(x = -1\\).",
 "solutions": [3], "calculator": False, "input_type": "single_value",
 "hint": "Divide −3 by −1, keeping track of the signs.",
 "misconceptions": mis("neg_div_sign", -3,
   "Negative divided by negative is positive: −3 ÷ (−1) = 3. Keeping it negative gives −3.", "error: neg/neg kept neg -> -3"),
 "guided_steps": [
   say("Divide, watching the two negative signs."),
   box("Ignore signs first: 3 ÷ 1 = ", 3, "Three shared into one."),
   box("Negative ÷ negative is positive, so y = ", 3, "Two minuses make a plus.", phase="substitute"),
   box("Check: 3 × (−1) = ", -3, "This should rebuild the −3 on top.", phase="substitute", done="It rebuilds −3 on top, so y = 3."),
 ]})

# s2 y=5*2^x x=3 -> 40
silver.append({
 "display": "For \\(y = 5 \\times 2^x\\), find \\(y\\) when \\(x = 3\\).",
 "solutions": [40], "calculator": False, "input_type": "single_value",
 "hint": "Work out 2³ first, then multiply by 5.",
 "misconceptions": mis("power_as_times", 30,
   "Work out the power first: 2³ = 8, then 5 × 8 = 40. Doing 5 × 2 × 3 = 30 treats the power as a multiply.", "error: 5x2x3=30"),
 "guided_steps": [
   say("Do the power first, then multiply by 5."),
   box("Work out 2³: 2 × 2 × 2 = ", 8, "Three 2s multiplied."),
   box("Multiply by 5: 5 × 8 = ", 40, "Five eights.", phase="substitute"),
   box("So y = ", 40, "The product of 5 and 8.", phase="substitute", done="2³ = 8 and 5 × 8 = 40, so y = 40."),
 ]})

# s3 y=-x^3 x=3 -> -27
silver.append({
 "display": "For \\(y = -x^3\\), find \\(y\\) when \\(x = 3\\).",
 "solutions": [-27], "calculator": False, "input_type": "single_value",
 "hint": "Cube 3 first, then apply the minus sign.",
 "misconceptions": mis("neg_sign_dropped", 27,
   "Cube first, then apply the minus: −(3³) = −27. Forgetting the minus gives 27.", "error: forgets minus -> 27"),
 "guided_steps": [
   say("Cube the 3 first, then put the minus sign on."),
   box("Cube: 3 × 3 × 3 = ", 27, "Three 3s multiplied."),
   box("Apply the minus: −(27) = ", -27, "Make it negative.", phase="substitute"),
   box("So y = ", -27, "The negative of 27.", phase="substitute", done="y = −(3³) = −27."),
 ]})

# s4 MC quadrants of y=1/x -> index 0
silver.append({
 "display": "For \\(y = \\frac{1}{x}\\), which two quadrants do the branches appear in?",
 "options": ["Q1 and Q3 (top-right and bottom-left)", "Q1 and Q2 (top-right and top-left)",
             "Q2 and Q4 (top-left and bottom-right)", "Q3 and Q4 (bottom-left and bottom-right)"],
 "solutions": [0], "calculator": False, "input_type": "multiple_choice",
 "hint": "Check the sign of y when x is positive, and when x is negative.",
 "misconceptions": mc("For y = 1/x (positive a), when x > 0 then y > 0 (Q1), and when x < 0 then y < 0 (Q3).")})

# s5 MC growth or decay y=0.7^x -> index 1 (Decay)
silver.append({
 "display": "Does the graph \\(y = 0.7^x\\) show growth or decay?",
 "options": ["Growth", "Decay"],
 "solutions": [1], "calculator": False, "input_type": "multiple_choice",
 "hint": "A base between 0 and 1 makes the curve fall as x increases.",
 "misconceptions": mc("The base 0.7 is between 0 and 1, so the graph shows exponential decay.")})

# s6 MC asymptotes of y=2/x -> index 0
silver.append({
 "display": "What are the asymptotes of \\(y = \\frac{2}{x}\\)?",
 "options": ["x = 0 and y = 0", "x = 2 and y = 0", "x = 0 and y = 2", "No asymptotes"],
 "solutions": [0], "calculator": False, "input_type": "multiple_choice",
 "hint": "A reciprocal curve never touches either axis.",
 "misconceptions": mc("All reciprocal graphs y = a/x have asymptotes at x = 0 (the y-axis) and y = 0 (the x-axis).")})

# ============ GOLD ============
gold = []

# g0 y=12/x x=-4 -> -3 (completion problem)
gold.append({
 "display": "For \\(y = \\frac{12}{x}\\), find \\(y\\) when \\(x = -4\\).",
 "solutions": [-3], "calculator": False, "input_type": "single_value",
 "hint": "Divide 12 by −4, keeping the minus sign.",
 "misconceptions": mis("div_sign_dropped", 3,
   "Positive divided by negative is negative: 12 ÷ (−4) = −3. Keeping it positive gives 3.", "error: sign dropped -> 3"),
 "guided_steps": [
   say("Divide 12 by the negative x, keeping the sign."),
   box("Ignore signs first: 12 ÷ 4 = ", 3, "Twelve shared into four."),
   box("Positive ÷ negative is negative, so y = ", -3, "Give the answer a minus sign.", phase="substitute"),
   box("Check: (−3) × (−4) = ", 12, "Negative times negative is positive.", phase="substitute", done="It rebuilds 12, so y = −3."),
 ]})

# g1 y=(x-1)^3 x=3 -> 8
gold.append({
 "display": "For \\(y = (x - 1)^3\\), find \\(y\\) when \\(x = 3\\).",
 "solutions": [8], "calculator": False, "input_type": "single_value",
 "hint": "Work out the bracket first, then cube it.",
 "misconceptions": mis("bracket_ignored", 26,
   "Work out the bracket first: (3 − 1)³ = 2³ = 8. Cubing before subtracting, as 3³ − 1 = 26, is the slip.", "error: 27-1=26"),
 "guided_steps": [
   say("Brackets first: work out (x − 1), then cube the result."),
   box("Inside the bracket: 3 − 1 = ", 2, "Subtract inside first."),
   box("Cube it: 2 × 2 × 2 = ", 8, "Three 2s multiplied.", phase="substitute"),
   box("So y = ", 8, "The cube of 2.", phase="substitute", done="(3 − 1)³ = 2³ = 8, so y = 8."),
 ]})

# g2 P=500*1.05^t t=0 -> 500
gold.append({
 "display": "A population model is \\(P = 500 \\times 1.05^t\\). What is the initial population (at \\(t = 0\\))?",
 "solutions": [500], "calculator": False, "input_type": "single_value",
 "hint": "Anything to the power 0 is 1, so 1.05⁰ = 1.",
 "misconceptions": mis("growth_step_added", 525,
   "At t = 0, 1.05⁰ = 1, so P = 500 × 1 = 500. Doing 500 × 1.05 = 525 adds a year of growth that has not happened yet.", "error: 500x1.05=525"),
 "guided_steps": [
   say("The initial population is the value when t = 0. Work out 1.05⁰ first."),
   box("Any number to the power 0 is 1, so 1.05⁰ = ", 1, "Power 0 always gives 1."),
   box("Multiply: 500 × 1 = ", 500, "Five hundred times one.", phase="substitute"),
   box("So the initial population is ", 500, "The starting value.", phase="substitute", done="1.05⁰ = 1, so P = 500 × 1 = 500."),
 ]})

# g3 y=2^x x=-3 -> 1/8 (fraction, solutions [1,8])
gold.append({
 "display": "For \\(y = 2^x\\), find \\(y\\) when \\(x = -3\\).",
 "solutions": [1, 8], "calculator": False, "input_type": "fraction",
 "hint": "A negative power means one over the positive power: 2⁻³ = 1 over 2³.",
 "misconceptions": mis("neg_power_as_times", [1, 6],
   "A negative power means one over the positive power: 2⁻³ = 1/2³ = 1/8. Writing 1/(2 × 3) = 1/6 treats the power as a multiply.", "error: 2x3=6 -> 1/6"),
 "guided_steps": [
   say("A negative power means the reciprocal: 2⁻³ = 1 over 2³."),
   box("Work out the positive power 2³: 2 × 2 × 2 = ", 8, "Three 2s multiplied."),
   box("The reciprocal is 1 over that. Type the bottom number of the fraction: ", 8, "The denominator is 2³.", phase="substitute"),
   box("And the top number of the fraction is ", 1, "A reciprocal has 1 on top.", phase="substitute", done="2⁻³ = 1/8, so the fraction is 1 over 8."),
 ]})

# g4 y=a/x through (4,-2) -> a=-8
gold.append({
 "display": "The graph \\(y = \\frac{a}{x}\\) passes through \\((4, -2)\\). Find \\(a\\).",
 "solutions": [-8], "calculator": False, "input_type": "single_value",
 "hint": "Multiply both sides by 4: a = −2 × 4.",
 "misconceptions": mis("divide_not_multiply", -0.5,
   "Substitute the point: −2 = a/4, so a = −2 × 4 = −8. Dividing instead, −2 ÷ 4 = −0.5, is the slip.", "error: -2/4=-0.5"),
 "guided_steps": [
   say("Substitute the point (4, −2) into y = a/x, which gives −2 = a ÷ 4."),
   box("To undo the ÷ 4, multiply both sides by 4. Left side: −2 × 4 = ", -8, "Negative two times four."),
   box("So a = ", -8, "The left-hand result.", phase="substitute"),
   box("Check: −8 ÷ 4 = ", -2, "This should give the −2 from the point.", phase="substitute", done="−8 ÷ 4 = −2 matches the point, so a = −8."),
 ]})

# ============ tier_guides ============
tier_guides = {
 "bronze": {
   "title": "Bronze: reading one value off a curve",
   "steps": [
     "Cube by multiplying three times: \\(2^3 = 2 × 2 × 2 = 8\\). A power like \\(2^4\\) means four 2s multiplied.",
     "Reciprocal \\(y = \\frac{a}{x}\\): divide a by x, so \\(y = \\frac{6}{3} = 2\\).",
     "Any number to the power 0 is 1. Reciprocal curves have two branches and never touch the axes."
   ],
   "example": {"question": "For y = 3ˣ, find y when x = 2.", "steps": [
     {"label": "Write it out", "content": "3 × 3"},
     {"label": "Multiply", "content": "= 9"},
     {"label": "Check", "content": "Powers of 3: 3, 9, 27"},
     {"label": "Answer", "content": "y = 9", "isAnswer": True, "is_answer": True},
   ]}},
 "silver": {
   "title": "Silver: negatives, powers and curve features",
   "steps": [
     "A negative number cubed stays negative: \\((-2)^3 = -8\\). For \\(-x^3\\), cube first, then apply the minus.",
     "Keep signs when dividing: \\(\\frac{-3}{-1} = 3\\). A reciprocal has asymptotes at \\(x = 0\\) and \\(y = 0\\).",
     "A base between 0 and 1 (like \\(0.7^x\\)) decays; a base above 1 grows."
   ],
   "example": {"question": "For y = x³ − 8, find y when x = 2.", "steps": [
     {"label": "Cube", "content": "2³ = 8"},
     {"label": "Subtract 8", "content": "8 − 8"},
     {"label": "Check", "content": "Cube first, then subtract"},
     {"label": "Answer", "content": "y = 0", "isAnswer": True, "is_answer": True},
   ]}},
 "gold": {
   "title": "Gold: models, brackets and finding constants",
   "steps": [
     "Exponential models: at \\(t = 0\\) the power is 0, so \\(k^0 = 1\\) and you get the starting amount.",
     "Brackets first: \\((x-1)^3\\) means work out \\(x - 1\\), then cube it.",
     "A negative power is a reciprocal: \\(2^{-3} = \\frac{1}{2^3} = \\frac{1}{8}\\). To find a in \\(y = \\frac{a}{x}\\), substitute the point."
   ],
   "example": {"question": "For y = (x − 1)³, find y when x = 3.", "steps": [
     {"label": "Bracket", "content": "3 − 1 = 2"},
     {"label": "Cube", "content": "2³ = 8"},
     {"label": "Check", "content": "Bracket before cube"},
     {"label": "Answer", "content": "y = 8", "isAnswer": True, "is_answer": True},
   ]}},
}

# ============ guided (opener + teach) ============
guided = {
 "opener": {
   "display": OPENER_SVG,
   "steps": [
     box("Carry on doubling. How many bacteria after 4 hours? ", 16, "Double the 8."),
     box("And after 5 hours? ", 32, "Double the 16."),
     say("You just followed an <strong>exponential</strong> curve, \\(y = 2^x\\): it starts almost flat, always passes through \\((0, 1)\\), then shoots up. This lesson also meets <strong>cubic</strong> curves \\(y = x^3\\) (an S-shape) and <strong>reciprocal</strong> curves \\(y = \\frac{a}{x}\\), whose two branches never touch the axes."),
   ]},
 "teach": {
   "bronze": {
     "display": "For \\(y = \\frac{8}{x}\\), find \\(y\\) when \\(x = 2\\), and again when \\(x = -4\\).",
     "steps": [
       say("For a reciprocal, divide the top number by x."),
       box("Divide 8 by 2: 8 ÷ 2 = ", 4, "Eight shared into two."),
       box("Now the negative x: 8 ÷ (−4) = ", -2, "Positive divided by negative is negative."),
       box("How many branches does the reciprocal curve have? ", 2, "One in quadrant 1, one in quadrant 3."),
       box("How many axes does the curve ever touch? ", 0, "Asymptotes mean it never touches.", done="Zero: reciprocal curves have asymptotes at x = 0 and y = 0, so they never touch either axis."),
     ]},
   "silver": {
     "display": "For \\(y = 4^x\\), find \\(y\\) when \\(x = 2\\), when \\(x = 0\\), and when \\(x = -1\\).",
     "steps": [
       say("A power tells you how many 4s to multiply."),
       box("Two 4s multiplied: 4 × 4 = ", 16, "Four times four."),
       box("Anything to the power 0: 4⁰ = ", 1, "Any number to the power 0 is 1."),
       box("A negative power is the reciprocal: 4⁻¹ = 1 ÷ 4 = ", 0.25, "One quarter as a decimal."),
       box("So every curve y = aˣ passes through (0, 1). Type that shared y-value: ", 1, "They all share the same y when x = 0.", done="Every exponential curve goes through (0, 1), because a⁰ = 1 for any base."),
     ]},
   "gold": {
     "display": "For \\(y = \\frac{1}{x} + 3\\), find the horizontal asymptote by seeing what happens as x gets very large.",
     "steps": [
       say("As x grows huge, the fraction 1/x shrinks towards 0. Let us watch it."),
       box("When x = 10: 1 ÷ 10 = ", 0.1, "One tenth."),
       box("Add the 3: 0.1 + 3 = ", 3.1, "Just add three."),
       box("When x = 1000: 1 ÷ 1000 = 0.001, add 3 = ", 3.001, "Almost exactly three."),
       box("The fraction is heading to 0, so y heads to which value? ", 3, "0 plus 3.", done="The +3 lifts the whole curve up 3, so the horizontal asymptote is y = 3."),
     ]},
 }}

# ============ method_card (slim, <=4 steps, <=140 words) ============
method_card = {
 "title": "Recognising Cubic, Reciprocal & Exponential Graphs",
 "steps": [
   "Spot the type: \\(x^3\\) is cubic, \\(\\frac{a}{x}\\) is reciprocal, \\(a^x\\) is exponential.",
   "Make a table of values including negative x, then join with a smooth curve.",
   "Reciprocal: two branches, asymptotes at \\(x = 0\\) and \\(y = 0\\).",
   "Exponential \\(y = a^x\\): always through \\((0, 1)\\), asymptote \\(y = 0\\).",
 ],
 "content": "<p><strong>Cubic</strong> graphs \\(y = ax^3 + \\ldots\\) make an S-shape, rising from bottom-left to top-right when \\(a > 0\\).</p><p><strong>Reciprocal</strong> graphs \\(y = \\frac{a}{x}\\) have two branches and never touch the axes.</p><p><strong>Exponential</strong> graphs \\(y = a^x\\) pass through \\((0, 1)\\); they grow when \\(a > 1\\) and decay when \\(0 < a < 1\\).</p>",
 "example": "<p><strong>Sketch \\(y = \\frac{6}{x}\\).</strong> \\(x = 1 \\to 6\\), \\(x = 2 \\to 3\\), \\(x = 3 \\to 2\\), with the mirror branch in quadrant 3 for negative x. Two branches; the curve never meets the axes.</p>",
}

# ============ preserved: topic_links, related_videos, worked_examples (em-dash fixed) ============
topic_links = {"prerequisites": [{"slug": "graphs/3", "title": "Quadratic Graphs"}]}
related_videos = []
worked_examples = [
 {"steps": [
   {"label": "Step 1: Substitute", "content": "<p>\\(y = (-3)^3 = -27\\)</p>"},
   {"label": "Answer", "content": "<p>\\(y = -27\\)</p>", "isAnswer": True, "is_answer": True},
  ], "question": "For y = x³, find y when x = −3.", "difficulty": "Bronze"},
 {"steps": [
   {"label": "Step 1: Vertical asymptote", "content": "<p>\\(y = \\frac{5}{x}\\) is undefined when \\(x = 0\\), so \\(x = 0\\) (y-axis) is a vertical asymptote.</p>"},
   {"label": "Step 2: Horizontal asymptote", "content": "<p>As \\(x \\to \\pm\\infty\\), \\(\\frac{5}{x} \\to 0\\). So \\(y = 0\\) (x-axis) is a horizontal asymptote.</p>"},
   {"label": "Answer", "content": "<p>Asymptotes: \\(x = 0\\) and \\(y = 0\\).</p>", "isAnswer": True, "is_answer": True},
  ], "question": "Identify the asymptotes of y = 5/x.", "difficulty": "Silver"},
 {"steps": [
   {"label": "Step 1: Growth or decay", "content": "<p>Base = 0.5 (between 0 and 1), so <strong>exponential decay</strong>.</p>"},
   {"label": "Step 2: Calculate", "content": "<p>\\(y = 3 \\times 0.5^4 = 3 \\times 0.0625 = 0.1875\\)</p>"},
   {"label": "Answer", "content": "<p>Decay. When \\(x = 4\\), \\(y = 0.1875\\).</p>", "isAnswer": True, "is_answer": True},
  ], "question": "A curve has equation y = 3 × 0.5ˣ. State whether it shows growth or decay and find y when x = 4.", "difficulty": "Gold"},
]

# Reorder bronze so single_value problems precede the two multiple_choice ones.
# The validator's within-tier duplicate check shares one numeric space for MC
# option-indices and real answers; putting reals first (all distinct) and MCs
# last (which are exempt) avoids an index-vs-value false collision (MC index 2
# vs the real answer 2). Completion problem bronze[0] stays walkable & first.
bronze = [bronze[i] for i in (0, 1, 3, 4, 5, 7, 2, 6)]

problem_bank = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description": "Substitute a whole number into a cubic or exponential, and name the family from its equation.",
 "silver_description": "Handle negatives, scaled powers and curve features (quadrants, asymptotes, growth vs decay).",
 "gold_description": "Models, brackets, negative indices and finding a constant from a point on the curve.",
}

base_pd = {
 "method_card": method_card,
 "topic_links": topic_links,
 "problem_bank": problem_bank,
 "related_videos": related_videos,
 "worked_examples": worked_examples,
 "tier_guides": tier_guides,
 "guided": guided,
}

with open(os.path.join(OUTDIR, "lesson_maths-eduqas_graphs-L05.json"), "w", encoding="utf-8") as f:
    json.dump(base_pd, f, ensure_ascii=False, indent=1)

# ============ DIAGRAMS: charts on reciprocal/exponential feature MCs ============
def recip_branches(a, xs_pos):
    pos = [{"x": round(x, 4), "y": round(a / x, 4)} for x in xs_pos]
    neg = [{"x": round(-x, 4), "y": round(a / (-x), 4)} for x in xs_pos]
    return pos, neg

def chart_reciprocal(a, label, color="#3b82f6"):
    xs = [0.5, 0.7, 1, 1.5, 2, 3, 4, 5]
    if abs(a) >= 2:  # keep |y|<=4 window; start where a/x <= 4
        xs = [x for x in xs if abs(a) / x <= 4.001] or [abs(a)/4.0]
    pos, neg = recip_branches(a, xs)
    ds = [
      {"type": "line", "data": pos, "tension": 0.35, "fill": False, "borderColor": color, "pointRadius": 0, "label": label},
      {"type": "line", "data": neg, "tension": 0.35, "fill": False, "borderColor": color, "pointRadius": 0},
    ]
    return {"type": "scatter", "data": {"datasets": ds},
            "options": {"scales": {
              "x": {"min": -5, "max": 5, "ticks": {"stepSize": 1}, "grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": "x", "display": True}},
              "y": {"min": -4, "max": 4, "ticks": {"stepSize": 1}, "grid": {"color": "rgba(0,0,0,0.08)"}, "title": {"text": "y", "display": True}}}}}

# s4: y = 1/x  (quadrants Q1, Q3)
chart_s4 = chart_reciprocal(1, "y = 1/x", "#3b82f6")

# s6: y = 2/x with dashed asymptotes on the axes
chart_s6 = chart_reciprocal(2, "y = 2/x", "#3b82f6")
chart_s6["data"]["datasets"].append({"type": "line", "data": [{"x": -5, "y": 0}, {"x": 5, "y": 0}],
   "borderColor": "#9ca3af", "borderDash": [6, 4], "borderWidth": 1, "pointRadius": 0, "label": "asymptotes x = 0, y = 0"})
chart_s6["data"]["datasets"].append({"type": "line", "data": [{"x": 0, "y": -4}, {"x": 0, "y": 4}],
   "borderColor": "#9ca3af", "borderDash": [6, 4], "borderWidth": 1, "pointRadius": 0})

# s5: y = 0.7^x  (exponential decay)
xs = [-3, -2, -1, 0, 1, 2, 3, 4, 5]
pts = [{"x": x, "y": round(0.7 ** x, 4)} for x in xs]
chart_s5 = {"type": "scatter", "data": {"datasets": [
    {"type": "line", "data": pts, "tension": 0.35, "fill": False, "borderColor": "#f59e0b", "pointRadius": 0, "label": "y = 0.7^x"}]},
  "options": {"scales": {
    "x": {"min": -3, "max": 5, "ticks": {"stepSize": 1}, "grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"text": "x", "display": True}},
    "y": {"min": 0, "max": 3, "ticks": {"stepSize": 1}, "grid": {"color": "rgba(0,0,0,0.08)"}, "title": {"text": "y", "display": True}}}}}

diag_pd = copy.deepcopy(base_pd)
diag_pd["problem_bank"]["silver"][4]["chart"] = chart_s4  # s4 quadrants
diag_pd["problem_bank"]["silver"][5]["chart"] = chart_s5  # s5 decay
diag_pd["problem_bank"]["silver"][6]["chart"] = chart_s6  # s6 asymptotes

with open(os.path.join(OUTDIR, "lesson_maths-eduqas_graphs-L05_diagrams.json"), "w", encoding="utf-8") as f:
    json.dump(diag_pd, f, ensure_ascii=False, indent=1)

# ---- self-check: every guided box lands, every chart point satisfies its equation ----
import math
errs = []

def check_walk(steps, label):
    for i, st in enumerate(steps):
        if st.get("answer") is not None and not isinstance(st["answer"], (int, float)):
            errs.append(f"{label}[{i}] non-numeric answer")

for tier, probs in (("bronze", bronze), ("silver", silver), ("gold", gold)):
    for i, p in enumerate(probs):
        if p.get("guided_steps"):
            check_walk(p["guided_steps"], f"{tier}[{i}]")

# chart point verification
for pt in chart_s4["data"]["datasets"][0]["data"] + chart_s4["data"]["datasets"][1]["data"]:
    if abs(pt["y"] - 1 / pt["x"]) > 0.01: errs.append(f"s4 chart bad point {pt}")
for pt in chart_s6["data"]["datasets"][0]["data"] + chart_s6["data"]["datasets"][1]["data"]:
    if abs(pt["y"] - 2 / pt["x"]) > 0.01: errs.append(f"s6 chart bad point {pt}")
for pt in chart_s5["data"]["datasets"][0]["data"]:
    if abs(pt["y"] - 0.7 ** pt["x"]) > 0.01: errs.append(f"s5 chart bad point {pt}")

print("self-check errors:", errs if errs else "NONE")
print("wrote lesson_maths-eduqas_graphs-L05.json and _diagrams.json")
