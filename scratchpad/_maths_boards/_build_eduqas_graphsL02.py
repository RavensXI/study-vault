# -*- coding: utf-8 -*-
"""Build the full guided-learning + diagrams practice_data for
maths-eduqas graphs-L02 'Equation of a Line'. Starts from the live row,
preserves untouched fields, adds guided pieces, repairs misconceptions,
fixes em dashes, and embeds two programmatically-generated figures."""
import json, io

LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_eduqas_graphsL02.json"
OUT  = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_graphs-L02.json"

pd = json.load(io.open(LIVE, encoding="utf-8"))

MINUS = "−"  # unicode minus

# ---------- figure generators (programmatic, from the numbers) ----------
def opener_svg():
    # taxi: cost vs miles, points (0,3) and (5,13), line y=2x+3
    # x: 0..5 miles -> screen 40..220 (px=40+miles*36)
    # y: 0..15 cost -> screen 150..30 (py=150-cost*8)
    def px(m): return 40 + m*36
    def py(c): return 150 - c*8
    x0,y0 = px(0),py(3)     # 40,126
    x1,y1 = px(5),py(13)    # 220,46
    return (
        '<svg viewBox="0 0 260 180" role="img" aria-label="Line graph of taxi '
        'cost against miles: it starts at three pounds at zero miles and rises '
        'to thirteen pounds at five miles" style="max-width:260px">'
        '<line x1="40" y1="22" x2="40" y2="150" stroke="currentColor" stroke-width="1"/>'
        '<line x1="40" y1="150" x2="252" y2="150" stroke="currentColor" stroke-width="1"/>'
        f'<line x1="{x0:g}" y1="{y0:g}" x2="{x1:g}" y2="{y1:g}" stroke="#60a5fa" stroke-width="2.5" fill="none"/>'
        f'<circle cx="{x0:g}" cy="{y0:g}" r="3.5" fill="currentColor"/>'
        f'<circle cx="{x1:g}" cy="{y1:g}" r="3.5" fill="currentColor"/>'
        f'<text x="48" y="122" font-family="Inter,sans-serif" font-size="11" fill="currentColor">(0, £3)</text>'
        f'<text x="150" y="42" font-family="Inter,sans-serif" font-size="11" fill="currentColor">(5, £13)</text>'
        '<text x="150" y="171" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">miles</text>'
        '<text x="14" y="88" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle" transform="rotate(-90 14 88)">cost (£)</text>'
        '<text x="40" y="164" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">0</text>'
        '<text x="220" y="164" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">5</text>'
        '</svg><br>A taxi charges £3 to get in, then £2 for every mile.'
    )

def grid_svg_two_points(ax,ay,bx,by,labelA,labelB):
    # generic coordinate grid with axes through origin; plot A,B and join.
    # x domain -3..5 -> 30..210 ; y domain -6..8 -> 200..20
    def sx(x): return 30 + (x-(-3)) * (210-30)/(5-(-3))
    def sy(y): return 200 - (y-(-6)) * (200-20)/(8-(-6))
    ox, oy = sx(0), sy(0)
    Ax,Ay = sx(ax),sy(ay); Bx,By = sx(bx),sy(by)
    return (
        '<svg viewBox="0 0 240 220" role="img" aria-label="Coordinate grid with '
        f'points {labelA} and {labelB} joined by a straight line" style="max-width:240px">'
        f'<line x1="{ox:.1f}" y1="20" x2="{ox:.1f}" y2="200" stroke="currentColor" stroke-width="1"/>'
        f'<line x1="24" y1="{oy:.1f}" x2="216" y2="{oy:.1f}" stroke="currentColor" stroke-width="1"/>'
        f'<line x1="{Ax:.1f}" y1="{Ay:.1f}" x2="{Bx:.1f}" y2="{By:.1f}" stroke="#60a5fa" stroke-width="2" fill="none"/>'
        f'<circle cx="{Ax:.1f}" cy="{Ay:.1f}" r="3.5" fill="currentColor"/>'
        f'<circle cx="{Bx:.1f}" cy="{By:.1f}" r="3.5" fill="currentColor"/>'
        f'<text x="{Ax-4:.1f}" y="{Ay-6:.1f}" font-family="Inter,sans-serif" font-size="11" fill="currentColor">{labelA}</text>'
        f'<text x="{Bx+4:.1f}" y="{By+12:.1f}" font-family="Inter,sans-serif" font-size="11" fill="currentColor">{labelB}</text>'
        f'<text x="209" y="{oy-4:.1f}" font-family="Inter,sans-serif" font-size="10" fill="currentColor">x</text>'
        f'<text x="{ox+4:.1f}" y="28" font-family="Inter,sans-serif" font-size="10" fill="currentColor">y</text>'
        f'<text x="{ox+3:.1f}" y="{oy+11:.1f}" font-family="Inter,sans-serif" font-size="10" fill="currentColor">0</text>'
        '</svg>'
    )

# ---------- method_card (trim + fix em dashes) ----------
pd["method_card"] = {
    "title": "How to Find the Equation of a Line",
    "steps": [
        "Read \\(m\\) and \\(c\\) straight from \\(y = mx + c\\), or rearrange the equation into that form first.",
        "From two points, gradient \\(m\\) = (change in y) ÷ (change in x), then substitute one point to find \\(c\\).",
        "Parallel lines share the same gradient \\(m\\).",
        "A perpendicular gradient is the negative reciprocal, \\(-\\frac{1}{m}\\): flip the fraction and change the sign.",
    ],
    "content": "<p>A straight line is \\(y = mx + c\\): \\(m\\) is the gradient (steepness) and \\(c\\) is the y-intercept (where it crosses the y-axis).</p><p><strong>Parallel</strong> lines share the same gradient. <strong>Perpendicular</strong> gradients multiply to \\(-1\\), so flip the fraction and change the sign: \\(m \\to -\\frac{1}{m}\\).</p><p>If a line is written as \\(ax + by = c\\), rearrange to make \\(y\\) the subject before reading the gradient.</p>",
    "example": "<p><strong>Find the equation of the line through \\((2, 5)\\) and \\((4, 11)\\).</strong></p><p>\\(m = \\frac{11-5}{4-2} = 3\\), then \\(5 = 3(2) + c\\), so \\(c = -1\\).</p><p><strong>Answer:</strong> \\(y = 3x - 1\\)</p>",
}

# ---------- worked_examples: fix em dashes in labels ----------
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---------- problem_bank: add hint, guided_steps, honest misconceptions ----------
pb = pd["problem_bank"]

def H(text): return text  # hint passthrough

# --- BRONZE ---
bronze = pb["bronze"]

bronze[0]["hint"] = "The y-intercept given in the question IS c."
bronze[0]["misconceptions"] = [{
    "pattern": "confused_m_and_c", "expect": 4,
    "message": "The y-intercept is c, given here as 1. The 4 is the gradient m, not c.",
    "note": "swap m and c: read gradient 4"}]
bronze[0]["guided_steps"] = [
    {"say": "In \\(y = mx + c\\), the gradient goes in the m slot and the y-intercept in the c slot.",
     "pre": "the gradient goes in the m slot: m = ", "post": "", "answer": 4, "hint": "The gradient is given as 4."},
    {"say": "The y-intercept is c, and it is given directly.", "phase": "substitute",
     "pre": "the y-intercept given is c = ", "post": "", "answer": 1, "hint": "The y-intercept IS c."},
    {"pre": "check the equation y = 4x + 1 at x = 0: y = 4×0 + 1 = ", "post": "", "answer": 1,
     "done": "It crosses at (0, 1), so c = 1.", "hint": "4 times 0 is 0, leaving 1."}]

bronze[1]["hint"] = "Substitute the point into y = mx + c, then solve for c."
bronze[1]["misconceptions"] = [{
    "pattern": "add_not_subtract", "expect": 15,
    "message": "Substitute (2, 9): 9 = 6 + c, so c = 9 − 6 = 3. Adding the 6 instead gives 15, which does not fit the point.",
    "note": "9+6=15"}]
bronze[1]["guided_steps"] = [
    {"say": "Substitute the point \\((2, 9)\\) into \\(y = 3x + c\\).",
     "pre": "the x part: m×x = 3×2 = ", "post": "", "answer": 6, "hint": "Multiply the gradient by the x-value."},
    {"say": "So \\(9 = 6 + c\\). Take 6 off both sides.", "phase": "substitute",
     "pre": "c = 9 − 6 = ", "post": "", "answer": 3, "hint": "Subtract 6 from 9."},
    {"pre": "check: 3×2 + 3 = ", "post": "", "answer": 9, "done": "It gives 9, so c = 3.", "hint": "6 plus 3."}]

bronze[2]["hint"] = "The point (0, c) sits on the y-axis, so it gives c directly."
bronze[2]["misconceptions"] = [{
    "pattern": "sign_dropped", "expect": 5,
    "message": "The line crosses the y-axis at (0, −5), so c = −5. Dropping the minus sign gives 5 by mistake.",
    "note": "drop minus"}]
bronze[2]["guided_steps"] = [
    {"say": "The point \\((0, -5)\\) has x = 0, so it is on the y-axis.",
     "pre": "read the y-value of (0, −5): ", "post": "", "answer": -5, "hint": "Second number in (0, −5), keep the minus."},
    {"say": "The y-intercept c is exactly that y-value.", "phase": "substitute",
     "pre": "so c = ", "post": "", "answer": -5, "hint": "Same value, with its sign."},
    {"pre": "check y = 2x − 5 at x = 0: y = 2×0 − 5 = ", "post": "", "answer": -5,
     "done": "It crosses at (0, −5), so c = −5.", "hint": "2 times 0 is 0, leaving −5."}]

bronze[3]["hint"] = "Substitute the point into y = mx + c, then solve for c."
bronze[3]["misconceptions"] = [{
    "pattern": "add_not_subtract", "expect": 10,
    "message": "Substitute (3, 7): 7 = 3 + c, so c = 7 − 3 = 4. Adding the 3 instead gives 10.",
    "note": "7+3=10"}]
bronze[3]["guided_steps"] = [
    {"say": "Substitute the point \\((3, 7)\\) into \\(y = 1x + c\\).",
     "pre": "the x part: m×x = 1×3 = ", "post": "", "answer": 3, "hint": "Gradient 1 times the x-value 3."},
    {"say": "So \\(7 = 3 + c\\). Take 3 off both sides.", "phase": "substitute",
     "pre": "c = 7 − 3 = ", "post": "", "answer": 4, "hint": "Subtract 3 from 7."},
    {"pre": "check: 1×3 + 4 = ", "post": "", "answer": 7, "done": "It gives 7, so c = 4.", "hint": "3 plus 4."}]

bronze[4]["hint"] = "The gradient is the number in front of x."
bronze[4]["misconceptions"] = [{
    "pattern": "confused_m_and_c", "expect": -3,
    "message": "The gradient is the number in front of x, which is 6. The −3 is the y-intercept, not the gradient.",
    "note": "reads c"}]
bronze[4]["guided_steps"] = [
    {"say": "In \\(y = mx + c\\), the gradient is the number multiplying \\(x\\).",
     "pre": "the number in front of x in y = 6x − 3 is ", "post": "", "answer": 6, "hint": "What multiplies x here."},
    {"say": "That number IS the gradient. The −3 is the y-intercept, not part of the gradient.", "phase": "substitute",
     "pre": "so the gradient m = ", "post": "", "answer": 6, "hint": "Same number in front of x."},
    {"pre": "check: at x = 0, y = −3; at x = 1, y = 3. The rise for 1 across is 3 − (−3) = ", "post": "", "answer": 6,
     "done": "Up 6 for every 1 across is exactly the gradient.", "hint": "3 minus negative 3."}]

bronze[5]["hint"] = "Watch the sign: gradient −2 times 1 is −2."
bronze[5]["misconceptions"] = [{
    "pattern": "sign_error", "expect": 3,
    "message": "The x part is −2×1 = −2, so 5 = −2 + c and c = 7. Treating it as +2 gives c = 3, which does not fit the point.",
    "note": "5-2=3"}]
bronze[5]["guided_steps"] = [
    {"say": "Substitute the point \\((1, 5)\\) into \\(y = -2x + c\\).",
     "pre": "the x part: m×x = −2×1 = ", "post": "", "answer": -2, "hint": "−2 times 1, keep the minus."},
    {"say": "So \\(5 = -2 + c\\). Add 2 to both sides.", "phase": "substitute",
     "pre": "c = 5 + 2 = ", "post": "", "answer": 7, "hint": "5 minus negative 2 is 5 + 2."},
    {"pre": "check: −2×1 + 7 = ", "post": "", "answer": 5, "done": "It gives 5, so c = 7.", "hint": "−2 plus 7."}]

bronze[6]["hint"] = "Work out half of 6 first, then solve for c."
bronze[6]["misconceptions"] = [{
    "pattern": "add_not_subtract", "expect": 11,
    "message": "Substitute (6, 8): 8 = 3 + c, so c = 8 − 3 = 5. Adding the 3 instead gives 11.",
    "note": "8+3=11"}]
bronze[6]["guided_steps"] = [
    {"say": "Substitute the point \\((6, 8)\\) into \\(y = \\frac{1}{2}x + c\\).",
     "pre": "the x part: ½×6 = ", "post": "", "answer": 3, "hint": "Half of 6."},
    {"say": "So \\(8 = 3 + c\\). Take 3 off both sides.", "phase": "substitute",
     "pre": "c = 8 − 3 = ", "post": "", "answer": 5, "hint": "Subtract 3 from 8."},
    {"pre": "check: ½×6 + 5 = ", "post": "", "answer": 8, "done": "It gives 8, so c = 5.", "hint": "3 plus 5."}]

bronze[7]["hint"] = "The y-intercept is the constant term, c."
bronze[7]["misconceptions"] = [{
    "pattern": "confused_m_and_c", "expect": -4,
    "message": "The y-intercept is the constant term c = 11. The −4 is the gradient, not the y-intercept.",
    "note": "reads m"}]
bronze[7]["guided_steps"] = [
    {"say": "The y-intercept is \\(c\\), the constant at the end of \\(y = mx + c\\).",
     "pre": "the constant at the end of y = −4x + 11 is ", "post": "", "answer": 11, "hint": "The number after the x term."},
    {"say": "That constant is the y-intercept.", "phase": "substitute",
     "pre": "so the y-intercept c = ", "post": "", "answer": 11, "hint": "Same constant."},
    {"pre": "check y = −4x + 11 at x = 0: y = −4×0 + 11 = ", "post": "", "answer": 11,
     "done": "It crosses at (0, 11), so c = 11.", "hint": "−4 times 0 is 0, leaving 11."}]

# --- SILVER ---
silver = pb["silver"]

silver[0]["hint"] = "Find the gradient from the two points, then substitute to find c."
silver[0]["misconceptions"] = [{
    "pattern": "wrong_formula", "expect": 11,
    "message": "From 5 = 6 + c, subtract 6: c = −1. Adding the 6 gives 11, which does not fit the points.",
    "note": "5+6=11"}]
silver[0]["guided_steps"] = [
    {"say": "Two points and no gradient, so find \\(m\\) first: (change in y) over (change in x).",
     "pre": "change in y = 11 − 5 = ", "post": "", "answer": 6, "hint": "Top y minus bottom y."},
    {"pre": "change in x = 4 − 2 = ", "post": "", "answer": 2, "hint": "Right x minus left x."},
    {"pre": "m = 6 ÷ 2 = ", "post": "", "answer": 3, "hint": "Divide the change in y by the change in x."},
    {"say": "Substitute \\((2, 5)\\) into \\(y = 3x + c\\). The x part is 3×2 = 6, so \\(5 = 6 + c\\):", "phase": "substitute",
     "pre": "c = 5 − 6 = ", "post": "", "answer": -1, "hint": "Take the x part off both sides."},
    {"pre": "check with (4, 11): 3×4 + (−1) = ", "post": "", "answer": 11,
     "done": "It gives 11, so c = −1.", "hint": "12 minus 1."}]

silver[1]["hint"] = "Find the gradient, then substitute a point to find c."
silver[1]["misconceptions"] = [{
    "pattern": "wrong_formula", "expect": 6,
    "message": "From 3 = 3 + c, subtract 3: c = 0. Adding gives 6, which does not fit the points.",
    "note": "3+3=6"}]
silver[1]["guided_steps"] = [
    {"say": "Two points, no gradient, so find \\(m\\) first: (change in y) over (change in x).",
     "pre": "change in y = 15 − 3 = ", "post": "", "answer": 12, "hint": "Top y minus bottom y."},
    {"pre": "change in x = 5 − 1 = ", "post": "", "answer": 4, "hint": "Right x minus left x."},
    {"pre": "m = 12 ÷ 4 = ", "post": "", "answer": 3, "hint": "Divide."},
    {"say": "Substitute \\((1, 3)\\) into \\(y = 3x + c\\). The x part is 3×1 = 3, so \\(3 = 3 + c\\):", "phase": "substitute",
     "pre": "c = 3 − 3 = ", "post": "", "answer": 0, "hint": "Take the x part off both sides."},
    {"pre": "check with (5, 15): 3×5 + 0 = ", "post": "", "answer": 15,
     "done": "It gives 15, so c = 0. The line is y = 3x.", "hint": "15 plus 0."}]

silver[2]["hint"] = "Parallel lines have the same gradient; substitute the point to find c."
silver[2]["misconceptions"] = [{
    "pattern": "sign_error", "expect": 13,
    "message": "Parallel means m = 5. Then 3 = 10 + c, so c = 3 − 10 = −7. Adding gives 13 instead.",
    "note": "3+10=13"}]
silver[2]["guided_steps"] = [
    {"say": "Parallel lines share the same gradient as \\(y = 5x - 2\\).",
     "pre": "the gradient is m = ", "post": "", "answer": 5, "hint": "Same as y = 5x − 2."},
    {"pre": "the x part: m×x = 5×2 = ", "post": "", "answer": 10, "hint": "5 times 2."},
    {"say": "So \\(3 = 10 + c\\). Take 10 off both sides.", "phase": "substitute",
     "pre": "c = 3 − 10 = ", "post": "", "answer": -7, "hint": "3 minus 10."},
    {"pre": "check: 5×2 + (−7) = ", "post": "", "answer": 3, "done": "It gives 3, so c = −7.", "hint": "10 minus 7."}]

silver[3]["hint"] = "Gradient is (change in y) over (change in x); keep the minus."
silver[3]["misconceptions"] = [{
    "pattern": "rise_run_inverted", "expect": -0.5,
    "message": "Divide change in y by change in x: −8 ÷ 4 = −2. Doing 4 ÷ −8 = −0.5 flips the fraction.",
    "note": "inverted"}]
silver[3]["guided_steps"] = [
    {"say": "Gradient is (change in y) over (change in x). Use \\((0, 6)\\) and \\((4, -2)\\).",
     "pre": "change in y = −2 − 6 = ", "post": "", "answer": -8, "hint": "Second y minus first y."},
    {"pre": "change in x = 4 − 0 = ", "post": "", "answer": 4, "hint": "Right x minus left x."},
    {"say": "Now divide to get the gradient.", "phase": "substitute",
     "pre": "m = −8 ÷ 4 = ", "post": "", "answer": -2, "hint": "Divide, keep the minus."},
    {"pre": "check: from (0, 6), down 2 per 1 across, at x = 4 gives y = 6 + (−2)×4 = ", "post": "", "answer": -2,
     "done": "It lands on (4, −2), so m = −2.", "hint": "6 minus 8."}]

silver[4]["hint"] = "Subtract the coordinates carefully: two negatives make a positive."
silver[4]["misconceptions"] = [{
    "pattern": "sign_error", "expect": 6,
    "message": "The x-gap is 3 − (−1) = 4, not 3 − 1 = 2. Using 2 gives m = 6, which does not fit the points.",
    "note": "12/2=6"}]
silver[4]["guided_steps"] = [
    {"say": "Gradient is (change in y) over (change in x). Take \\((3, 1)\\) and \\((-1, -11)\\) in order.",
     "pre": "change in y = 1 − (−11) = ", "post": "", "answer": 12, "hint": "1 minus negative 11."},
    {"pre": "change in x = 3 − (−1) = ", "post": "", "answer": 4, "hint": "3 minus negative 1."},
    {"say": "Now divide to get the gradient.", "phase": "substitute",
     "pre": "m = 12 ÷ 4 = ", "post": "", "answer": 3, "hint": "Divide."},
    {"pre": "check: from (−1, −11), up 3 per 1 across, at x = 3 gives y = −11 + 3×4 = ", "post": "", "answer": 1,
     "done": "It lands on (3, 1), so m = 3.", "hint": "−11 plus 12."}]

silver[5]["hint"] = "Parallel lines share the gradient; substitute the point for c."
silver[5]["misconceptions"] = [{
    "pattern": "sign_error", "expect": -5,
    "message": "The x part is −2×3 = −6, so 1 = −6 + c and c = 7. Treating it as +6 gives c = −5.",
    "note": "1-6=-5"}]
silver[5]["guided_steps"] = [
    {"say": "Line Q is parallel to P, so it has the same gradient as \\(y = -2x + 9\\).",
     "pre": "the gradient of Q is m = ", "post": "", "answer": -2, "hint": "Same as line P."},
    {"pre": "the x part: m×x = −2×3 = ", "post": "", "answer": -6, "hint": "−2 times 3, keep the minus."},
    {"say": "So \\(1 = -6 + c\\). Add 6 to both sides.", "phase": "substitute",
     "pre": "c = 1 + 6 = ", "post": "", "answer": 7, "hint": "1 minus negative 6 is 1 + 6."},
    {"pre": "check: −2×3 + 7 = ", "post": "", "answer": 1, "done": "It gives 1, so c = 7.", "hint": "−6 plus 7."}]

silver[6]["hint"] = "Divide the whole equation by 2 to reach y = mx + c."
silver[6]["misconceptions"] = [{
    "pattern": "forgot_step", "expect": 8,
    "message": "Divide every term by 2 first: y = 4x − 3, gradient 4. Reading 8 straight off forgets to make y the subject.",
    "note": "reads 8"}]
silver[6]["guided_steps"] = [
    {"say": "The equation \\(2y = 8x - 6\\) is not in \\(y = mx + c\\) form. Divide every term by 2.",
     "pre": "the x coefficient: 8 ÷ 2 = ", "post": "", "answer": 4, "hint": "Divide 8 by 2."},
    {"pre": "the constant: −6 ÷ 2 = ", "post": "", "answer": -3, "hint": "Divide −6 by 2."},
    {"say": "So \\(y = 4x - 3\\). Read the gradient, the number in front of x.", "phase": "substitute",
     "pre": "the gradient is ", "post": "", "answer": 4, "hint": "Read m from y = 4x − 3."},
    {"pre": "check the y-intercept at x = 0: y = 4×0 − 3 = ", "post": "", "answer": -3,
     "done": "The gradient is 4, not the original 8.", "hint": "4 times 0 minus 3."}]

# --- GOLD ---
gold = pb["gold"]

gold[0]["hint"] = "Find the gradient first, watching the negative x-value, then substitute."
gold[0]["misconceptions"] = [{
    "pattern": "sign_error", "expect": -5,
    "message": "The x-gap is 4 − (−2) = 6, not 4 − 2 = 2. Using 2 gives m = −6 and then c = −5, which fits neither point.",
    "note": "m=-12/2=-6; 7=12+c -> c=-5"}]
gold[0]["guided_steps"] = [
    {"say": "Two points, no gradient, so find \\(m\\) first: (change in y) over (change in x).",
     "pre": "change in y = −5 − 7 = ", "post": "", "answer": -12, "hint": "Second y minus first y."},
    {"pre": "change in x = 4 − (−2) = ", "post": "", "answer": 6, "hint": "4 minus negative 2."},
    {"pre": "m = −12 ÷ 6 = ", "post": "", "answer": -2, "hint": "Divide, keep the minus."},
    {"say": "Substitute \\((-2, 7)\\) into \\(y = -2x + c\\). The x part is −2×(−2) = 4, so \\(7 = 4 + c\\):", "phase": "substitute",
     "pre": "c = 7 − 4 = ", "post": "", "answer": 3, "hint": "Take the x part off both sides."},
    {"pre": "check with (4, −5): −2×4 + 3 = ", "post": "", "answer": -5,
     "done": "It gives −5, so c = 3.", "hint": "−8 plus 3."}]

gold[1]["hint"] = "Perpendicular gradient is the negative reciprocal of 4; then substitute."
gold[1]["misconceptions"] = [
    {"pattern": "no_flip", "expect": 37,
     "message": "The perpendicular gradient is the negative reciprocal, −¼, not −4. Using −4 gives c = 37. Flip 4 to a quarter AND change the sign.",
     "note": "5=-32+c -> c=37"},
    {"pattern": "sign_error", "expect": 3,
     "message": "The x part is −¼×8 = −2, so 5 = −2 + c and c = 7. Treating it as +2 gives c = 3.",
     "note": "5-2=3"}]
gold[1]["guided_steps"] = [
    {"say": "The gradient of \\(y = 4x - 1\\) is 4. Perpendicular gradient is the negative reciprocal, \\(-\\frac{1}{4}\\).",
     "pre": "the x part: −¼×8 = ", "post": "", "answer": -2, "hint": "A quarter of 8 is 2, keep the minus."},
    {"say": "So \\(5 = -2 + c\\). Add 2 to both sides.", "phase": "substitute",
     "pre": "c = 5 + 2 = ", "post": "", "answer": 7, "hint": "5 minus negative 2 is 5 + 2."},
    {"pre": "check: −¼×8 + 7 = ", "post": "", "answer": 5, "done": "It gives 5, so c = 7.", "hint": "−2 plus 7."}]

gold[2]["hint"] = "Substitute the point, then solve the equation for m."
gold[2]["misconceptions"] = [{
    "pattern": "sign_error", "expect": 3,
    "message": "From −3m = 9, divide by −3: m = −3. Dividing by +3 and dropping the minus gives 3, which does not fit the point.",
    "note": "9/3=3"}]
gold[2]["guided_steps"] = [
    {"say": "Substitute \\((-3, 12)\\) into \\(y = mx + 3\\): \\(12 = -3m + 3\\). Take 3 off both sides.",
     "pre": "−3m = 12 − 3 = ", "post": "", "answer": 9, "hint": "12 minus 3."},
    {"say": "So \\(-3m = 9\\). Divide by −3.", "phase": "substitute",
     "pre": "m = 9 ÷ (−3) = ", "post": "", "answer": -3, "hint": "9 divided by −3, keep the minus."},
    {"pre": "check: (−3)×(−3) + 3 = ", "post": "", "answer": 12, "done": "It gives 12, so m = −3.", "hint": "9 plus 3."}]

gold[3]["hint"] = "Perpendicular gradient is the negative reciprocal; the point is not needed."
gold[3]["misconceptions"] = [
    {"pattern": "no_sign", "expect": -2,
     "message": "Flip −½ to −2, then change the sign to get +2. Stopping at −2 forgets the sign change.",
     "note": "no sign change"},
    {"pattern": "no_flip", "expect": 0.5,
     "message": "The perpendicular gradient is the negative reciprocal: flip −½ AND change the sign, giving 2. Only changing the sign gives 0.5.",
     "note": "-(-1/2)=0.5"}]
gold[3]["guided_steps"] = [
    {"say": "The gradient of \\(y = -\\frac{1}{2}x + 6\\) is \\(-\\frac{1}{2}\\). Perpendicular gradients are negative reciprocals: flip and change sign.",
     "pre": "flip −½ (turn it upside down) to get ", "post": "", "answer": -2, "hint": "Turn −1/2 upside down: −2."},
    {"say": "Now change the sign.", "phase": "substitute",
     "pre": "the perpendicular gradient is −(−2) = ", "post": "", "answer": 2, "hint": "Negative of −2."},
    {"pre": "check: perpendicular gradients multiply to −1, so −½ × 2 = ", "post": "", "answer": -1,
     "done": "They multiply to −1, so the gradient is 2.", "hint": "−1/2 times 2."}]

gold[4]["hint"] = "Find the midpoint first, then substitute it into y = mx + c."
gold[4]["misconceptions"] = [{
    "pattern": "sign_error", "expect": -2,
    "message": "The x part is −2×4 = −8, so 6 = −8 + c and c = 14. Treating it as +8 gives c = −2.",
    "note": "6-8=-2"}]
gold[4]["guided_steps"] = [
    {"say": "First find the midpoint of \\(A(2, 3)\\) and \\(B(6, 9)\\): average the coordinates.",
     "pre": "the x of the midpoint: (2 + 6) ÷ 2 = ", "post": "", "answer": 4, "hint": "Average the x-values."},
    {"pre": "the y of the midpoint: (3 + 9) ÷ 2 = ", "post": "", "answer": 6, "hint": "Average the y-values."},
    {"say": "The midpoint is \\((4, 6)\\). The gradient is −2, so the x part is:",
     "pre": "m×x = −2×4 = ", "post": "", "answer": -8, "hint": "−2 times 4, keep the minus."},
    {"say": "So \\(6 = -8 + c\\). Add 8 to both sides.", "phase": "substitute",
     "pre": "c = 6 + 8 = ", "post": "", "answer": 14, "hint": "6 minus negative 8 is 6 + 8."},
    {"pre": "check: −2×4 + 14 = ", "post": "", "answer": 6,
     "done": "It gives 6, the midpoint's y-value, so c = 14.", "hint": "−8 plus 14."}]

# add the coordinate-grid figure to gold[0] (two named points, exam would print it)
gold[0]["display"] = grid_svg_two_points(-2, 7, 4, -5, "(−2, 7)", "(4, −5)") + \
    "Find the equation of the line through \\((-2, 7)\\) and \\((4, -5)\\). What is \\(c\\)?"

# ---------- tier_guides ----------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: reading y = mx + c",
        "steps": [
            "In \\(y = mx + c\\), the gradient is \\(m\\), the number in front of \\(x\\), and the y-intercept is \\(c\\), the value where the line crosses the y-axis.",
            "To find \\(c\\) from a gradient and a point, put the numbers into \\(y = mx + c\\) and solve, keeping every minus sign.",
            "A point of the form \\((0, c)\\) sits on the y-axis, so it gives \\(c\\) straight away.",
        ],
        "example": {
            "question": "A line has gradient 3 and passes through (2, 8). Find c.",
            "steps": [
                {"label": "Substitute the point", "content": "<p>\\(8 = 3(2) + c\\)</p>"},
                {"label": "Solve for c", "content": "<p>\\(8 = 6 + c\\), so \\(c = 2\\)</p>"},
                {"label": "Check", "content": "<p>\\(3(2) + 2 = 8\\)</p>"},
                {"label": "Answer", "content": "<p>\\(c = 2\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: two points and parallel lines",
        "steps": [
            "With two points, find the gradient first: change in y divided by change in x, keeping the points in the same order top and bottom.",
            "Then substitute one point into \\(y = mx + c\\) and solve for \\(c\\).",
            "Parallel lines share the same gradient. Rearrange any equation into \\(y = mx + c\\) form before reading \\(m\\).",
        ],
        "example": {
            "question": "Find the equation of the line through (1, 4) and (3, 10). Give c.",
            "steps": [
                {"label": "Gradient", "content": "<p>\\(m = \\frac{10-4}{3-1} = \\frac{6}{2} = 3\\)</p>"},
                {"label": "Find c", "content": "<p>\\(4 = 3(1) + c\\), so \\(c = 1\\)</p>"},
                {"label": "Check", "content": "<p>\\(3(3) + 1 = 10\\)</p>"},
                {"label": "Answer", "content": "<p>\\(y = 3x + 1\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: perpendicular lines and unknowns",
        "steps": [
            "A perpendicular gradient is the negative reciprocal: flip the fraction and change the sign, so \\(m \\to -\\frac{1}{m}\\).",
            "Rearrange \\(ax + by = c\\) into \\(y = mx + c\\) before reading a gradient.",
            "For an unknown gradient or coordinate, substitute the point into the equation and solve.",
        ],
        "example": {
            "question": "A line is perpendicular to y = 2x + 1 and passes through (4, 3). Find c.",
            "steps": [
                {"label": "Perpendicular gradient", "content": "<p>Flip and change sign: \\(m = -\\frac{1}{2}\\).</p>"},
                {"label": "Find c", "content": "<p>\\(3 = -\\frac{1}{2}(4) + c = -2 + c\\), so \\(c = 5\\)</p>"},
                {"label": "Check", "content": "<p>\\(-\\frac{1}{2}(4) + 5 = 3\\)</p>"},
                {"label": "Answer", "content": "<p>\\(y = -\\frac{1}{2}x + 5\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------- guided: opener + teach ----------
pd["guided"] = {
    "opener": {
        "label": "Before any algebra",
        "display": opener_svg(),
        "steps": [
            {"say": "No algebra, just the price list. A taxi charges £3 to get in, then £2 per mile.",
             "pre": "A ride of no distance at all (0 miles) still costs £", "post": "", "answer": 3,
             "hint": "You still pay the £3 just to get in, even for 0 miles."},
            {"say": "That £3 you always pay, the cost before any distance, is the <strong>y-intercept</strong>, the value when \\(x = 0\\).",
             "pre": "Each extra mile adds £", "post": "", "answer": 2, "hint": "The rate is £2 for every mile."},
            {"say": "That £2 per mile, the steady climb, is the <strong>gradient</strong>. So a 5-mile ride costs 3 + 2×5:",
             "pre": "£", "post": "", "answer": 13, "hint": "Start at £3, then add £2 five times: 3 + 10."},
            {"say": "Write miles as \\(x\\) and cost as \\(y\\) and you have a line: \\(y = 2x + 3\\). The gradient \\(m = 2\\) is the rate per mile, the intercept \\(c = 3\\) is the start cost. Every line equation reads the same way."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "A line has gradient 2 and crosses the y-axis at \\((0, -4)\\). Write it as \\(y = mx + c\\).",
            "label": "Together: your first one",
            "steps": [
                {"say": "In \\(y = mx + c\\), \\(m\\) is the gradient and \\(c\\) is where the line meets the y-axis.",
                 "pre": "the gradient goes in the m slot: m = ", "post": "", "answer": 2, "hint": "The gradient is given as 2."},
                {"pre": "the line crosses the y-axis at (0, −4), so c = ", "post": "", "answer": -4,
                 "hint": "Read the y-value where x = 0, keep the minus."},
                {"say": "So the equation is \\(y = 2x - 4\\). Test it at \\(x = 3\\):",
                 "pre": "y = 2×3 − 4 = ", "post": "", "answer": 2, "hint": "6 minus 4."},
                {"pre": "and at x = 0: y = 2×0 − 4 = ", "post": "", "answer": -4,
                 "done": "That is the y-intercept, exactly c. Reading m and c is the whole bronze move.", "hint": "2 times 0 is 0, leaving −4."},
            ],
        },
        "silver": {
            "display": "Find the equation of the line through \\((3, 8)\\) with gradient 2. Give \\(c\\).",
            "label": "Together: the silver move",
            "steps": [
                {"say": "You know \\(m = 2\\) but not \\(c\\). Substitute the point \\((3, 8)\\) into \\(y = mx + c\\).",
                 "pre": "the x part: m×x = 2×3 = ", "post": "", "answer": 6, "hint": "Multiply the gradient by the x-value."},
                {"say": "So \\(8 = 6 + c\\). Take 6 off both sides:",
                 "pre": "c = 8 − 6 = ", "post": "", "answer": 2, "hint": "Subtract 6 from 8."},
                {"say": "The equation is \\(y = 2x + 2\\). Check it lands on the point:",
                 "pre": "2×3 + 2 = ", "post": "", "answer": 8, "hint": "6 plus 2."},
                {"pre": "and the y-intercept, at x = 0: y = 2×0 + 2 = ", "post": "", "answer": 2,
                 "done": "The point fits and c = 2. Substituting a point to find c is the silver move.", "hint": "2 times 0 is 0, leaving 2."},
            ],
        },
        "gold": {
            "display": "Find the equation of the line through \\((1, 4)\\) and \\((5, 16)\\). Give \\(c\\).",
            "label": "Together: the gold move",
            "steps": [
                {"say": "Two points and no gradient, so find \\(m\\) first from (change in y) over (change in x).",
                 "pre": "change in y = 16 − 4 = ", "post": "", "answer": 12, "hint": "Top y minus bottom y."},
                {"pre": "change in x = 5 − 1 = ", "post": "", "answer": 4, "hint": "Right x minus left x."},
                {"pre": "m = 12 ÷ 4 = ", "post": "", "answer": 3, "hint": "Divide the change in y by the change in x."},
                {"say": "Now substitute \\((1, 4)\\) into \\(y = 3x + c\\). The x part is 3×1 = 3, so \\(4 = 3 + c\\):",
                 "pre": "c = 4 − 3 = ", "post": "", "answer": 1, "hint": "Subtract 3 from 4."},
                {"say": "Check with the other point \\((5, 16)\\):",
                 "pre": "3×5 + 1 = ", "post": "", "answer": 16,
                 "done": "It gives 16, so c = 1. Finding m from two points then substituting is the gold move.", "hint": "15 plus 1."},
            ],
        },
    },
}

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT)
print("bronze", len(pb["bronze"]), "silver", len(pb["silver"]), "gold", len(pb["gold"]))
