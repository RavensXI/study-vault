# -*- coding: utf-8 -*-
"""Build the full guided + diagrams practice_data for maths-eduqas graphs-L07."""
import json, io, copy

SRC = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_eduqas_graphs-L07.json"
OUT = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_graphs-L07.json"

pd = json.load(io.open(SRC, encoding="utf-8"))

# ---------- helpers ----------
def sv(x): return "\\(" + x + "\\)"

def parabola(fn, xs):
    return [{"x": x, "y": fn(x)} for x in xs]

def chart_two(blue_pts, orange_pts, xmin, xmax, ymin, ymax, xstep=1, ystep=2):
    return {
        "type": "scatter",
        "data": {"datasets": [
            {"data": blue_pts, "fill": False, "type": "line", "tension": 0.4,
             "borderColor": "#3b82f6", "pointRadius": 3, "pointBackgroundColor": "#3b82f6"},
            {"data": orange_pts, "fill": False, "type": "line", "tension": 0.4,
             "borderColor": "#f59e0b", "pointRadius": 3, "pointBackgroundColor": "#f59e0b"},
        ]},
        "options": {"scales": {
            "x": {"min": xmin, "max": xmax, "grid": {"color": "rgba(128,128,128,0.15)"},
                  "ticks": {"stepSize": xstep}, "title": {"text": "x", "display": True}},
            "y": {"min": ymin, "max": ymax, "grid": {"color": "rgba(128,128,128,0.15)"},
                  "ticks": {"stepSize": ystep}, "title": {"text": "y", "display": True}},
        }, "plugins": {"legend": {"display": False}}},
    }

# ======================================================================
# 1. METHOD CARD (slim, <=4 steps, <=140 words, no em dash)
# ======================================================================
pd["method_card"] = {
    "title": "Transforming Graphs with Function Notation",
    "steps": [
        "Outside the bracket changes y and behaves as written: f(x) + a moves UP, −f(x) reflects in the x-axis, af(x) stretches y by a.",
        "Inside the bracket changes x and does the OPPOSITE: f(x + a) moves LEFT, f(−x) reflects in the y-axis, f(ax) divides x by a.",
        "Apply the rule to each key point, shifting, flipping or scaling its coordinates.",
        "Check a known point lands sensibly before sketching the new curve.",
    ],
    "content": ("<p>Graph transformations use <strong>function notation</strong> \\(f(x)\\). "
                "Changes <strong>outside</strong> the bracket affect \\(y\\) and behave as written: "
                "\\(f(x) + a\\) shifts up by \\(a\\), \\(-f(x)\\) reflects in the \\(x\\)-axis, and "
                "\\(af(x)\\) stretches vertically by scale factor \\(a\\). Changes <strong>inside</strong> "
                "the bracket affect \\(x\\) and do the opposite: \\(f(x + a)\\) shifts left by \\(a\\), "
                "\\(f(-x)\\) reflects in the \\(y\\)-axis, and \\(f(ax)\\) compresses horizontally by "
                "scale factor \\(\\frac{1}{a}\\). In short: outside affects \\(y\\) as expected, inside "
                "affects \\(x\\) inversely.</p>"),
    "example": ("<p><strong>The point (3, 5) lies on \\(y = f(x)\\). Find its image on "
                "\\(y = f(x + 2)\\).</strong></p><p>The \\(+2\\) is inside the bracket, so it moves the "
                "point LEFT by 2: \\(x = 3 - 2 = 1\\). The \\(y\\)-coordinate is unchanged, so the image "
                "is \\((1, 5)\\).</p>"),
}

# ======================================================================
# 2. WORKED EXAMPLES: fix em-dash labels (preserve everything else)
# ======================================================================
for we in pd["worked_examples"]:
    for st in we["steps"]:
        if "label" in st:
            st["label"] = st["label"].replace(" — ", ": ")

# ======================================================================
# 3. PROBLEM BANK repairs + guided_steps + honest misconceptions
# ======================================================================
pb = pd["problem_bank"]

# ---- BRONZE ----
bronze = pb["bronze"]
# b0 (5,3) f(x)+6 -> 9  (unchanged numbers)
bronze[0]["guided_steps"] = [
    {"say": "The +6 is OUTSIDE the bracket, so it changes the y-coordinate only. x stays at 5."},
    {"pre": "The graph moves UP. By how many units? ", "post": "", "answer": 6,
     "hint": "The number outside the bracket, 6."},
    {"say": "Add that to the y-coordinate."},
    {"pre": "New y = 3 + 6 = ", "post": "", "answer": 9, "phase": "substitute",
     "hint": "Add 6 onto 3."},
    {"pre": "Check how far y rose: 9 − 3 = ", "post": "", "answer": 6, "phase": "substitute",
     "hint": "New y minus old y.", "done": "Up 6, exactly f(x) + 6, so the image y is 9."},
]
bronze[0]["misconceptions"] = [
    {"pattern": "wrong_direction", "expect": -3, "note": "3-6 subtracted, wrong direction",
     "message": "The +6 is outside the bracket and moves the graph UP, so add: 3 + 6 = 9. Subtracting to get −3 goes the wrong way."}]

# b1 (4,8) f(x)-5 -> 3
bronze[1]["guided_steps"] = [
    {"say": "The −5 is OUTSIDE the bracket, so it changes the y-coordinate only. x stays at 4."},
    {"pre": "The graph moves DOWN. By how many units? ", "post": "", "answer": 5,
     "hint": "The size of the number outside, 5."},
    {"say": "Take that off the y-coordinate."},
    {"pre": "New y = 8 − 5 = ", "post": "", "answer": 3, "phase": "substitute",
     "hint": "8 take away 5."},
    {"pre": "Check the drop: 8 − 3 = ", "post": "", "answer": 5, "phase": "substitute",
     "hint": "Old y minus new y.", "done": "Down 5, exactly f(x) − 5, so the image y is 3."},
]
bronze[1]["misconceptions"] = [
    {"pattern": "wrong_direction", "expect": 13, "note": "8+5 added, wrong direction",
     "message": "The −5 outside moves the graph DOWN, so subtract: 8 − 5 = 3. Adding to get 13 is the wrong direction."}]

# b2 REPAIR: was f(x-3)->9 (dup with b0). Change to f(x-5)-> x=11
bronze[2]["display"] = "The point \\((6, 2)\\) is on \\(y = f(x)\\). What is the x-coordinate of the corresponding point on \\(y = f(x - 5)\\)?"
bronze[2]["solutions"] = [11]
bronze[2]["guided_steps"] = [
    {"say": "The −5 is INSIDE the bracket, so it changes x, and inside does the OPPOSITE: f(x − 5) moves RIGHT by 5. y stays at 2."},
    {"pre": "Moving right means we add. Add how many? ", "post": "", "answer": 5,
     "hint": "The number inside the bracket, 5."},
    {"say": "Add that to the x-coordinate."},
    {"pre": "New x = 6 + 5 = ", "post": "", "answer": 11, "phase": "substitute",
     "hint": "6 add 5."},
    {"pre": "Check: y is untouched, so how far did y move? ", "post": "", "answer": 0, "phase": "substitute",
     "hint": "Inside the bracket never changes y.", "done": "x moved right 5, y stayed put, so the image x is 11."},
]
bronze[2]["misconceptions"] = [
    {"pattern": "inside_bracket", "expect": 1, "note": "6-5 left shift",
     "message": "f(x − 5) moves RIGHT by 5 (inside does the opposite of the minus), so add: 6 + 5 = 11. Subtracting to get 1 is the left-shift error."}]

# b3 REPAIR: was f(x+4)->3 (dup with b1). Change to f(x+2)-> x=5
bronze[3]["display"] = "The point \\((7, 1)\\) is on \\(y = f(x)\\). What is the x-coordinate of the corresponding point on \\(y = f(x + 2)\\)?"
bronze[3]["solutions"] = [5]
bronze[3]["guided_steps"] = [
    {"say": "The +2 is INSIDE the bracket, so inside does the OPPOSITE: f(x + 2) moves LEFT by 2. y stays at 1."},
    {"pre": "Moving left means we subtract. By how many? ", "post": "", "answer": 2,
     "hint": "The number inside the bracket, 2."},
    {"say": "Take that off the x-coordinate."},
    {"pre": "New x = 7 − 2 = ", "post": "", "answer": 5, "phase": "substitute",
     "hint": "7 take away 2."},
    {"pre": "Check: y is untouched, so how far did y move? ", "post": "", "answer": 0, "phase": "substitute",
     "hint": "Inside the bracket never changes y.", "done": "x moved left 2, y stayed put, so the image x is 5."},
]
bronze[3]["misconceptions"] = [
    {"pattern": "inside_bracket", "expect": 9, "note": "7+2 right shift",
     "message": "f(x + 2) has +2 inside the bracket, so it moves LEFT by 2: 7 − 2 = 5. Adding to get 9 is the right-shift error."}]

# b4 MC f(x)+a -> Up (0)
bronze[4]["misconceptions"] = [
    {"pattern": "inside_bracket", "expect": 3, "note": "chose Right, inside/outside confusion",
     "message": "The +a is OUTSIDE the bracket, so it changes y and moves the graph UP, not sideways. Only changes inside the bracket move it left or right."}]

# b5 MC f(x+a) -> Left (2)
bronze[5]["misconceptions"] = [
    {"pattern": "inside_bracket", "expect": 3, "note": "chose Right, forgot inside opposite",
     "message": "f(x + a) has +a inside the bracket, and inside does the opposite, so the graph moves LEFT by a, not right."}]

# b6 (0,5) f(x)+10 -> 15
bronze[6]["guided_steps"] = [
    {"say": "The +10 is OUTSIDE the bracket, so it changes the y-coordinate only. x stays at 0."},
    {"pre": "The graph moves UP. By how many units? ", "post": "", "answer": 10,
     "hint": "The number outside the bracket, 10."},
    {"say": "Add that to the y-coordinate."},
    {"pre": "New y = 5 + 10 = ", "post": "", "answer": 15, "phase": "substitute",
     "hint": "Add 10 onto 5."},
    {"pre": "Check how far y rose: 15 − 5 = ", "post": "", "answer": 10, "phase": "substitute",
     "hint": "New y minus old y.", "done": "Up 10, exactly f(x) + 10, so the image y is 15."},
]
bronze[6]["misconceptions"] = [
    {"pattern": "wrong_direction", "expect": -5, "note": "5-10 subtracted",
     "message": "The +10 outside moves the graph UP, so add: 5 + 10 = 15. Subtracting to get −5 is the wrong direction."}]

# b7 (3,-2) f(x-7) -> x=10
bronze[7]["guided_steps"] = [
    {"say": "The −7 is INSIDE the bracket, so inside does the OPPOSITE: f(x − 7) moves RIGHT by 7. y stays at −2."},
    {"pre": "Moving right means we add. Add how many? ", "post": "", "answer": 7,
     "hint": "The number inside the bracket, 7."},
    {"say": "Add that to the x-coordinate."},
    {"pre": "New x = 3 + 7 = ", "post": "", "answer": 10, "phase": "substitute",
     "hint": "3 add 7."},
    {"pre": "Check: y is untouched, so how far did y move? ", "post": "", "answer": 0, "phase": "substitute",
     "hint": "Inside the bracket never changes y.", "done": "x moved right 7, y stayed put, so the image x is 10."},
]
bronze[7]["misconceptions"] = [
    {"pattern": "inside_bracket", "expect": -4, "note": "3-7 left shift",
     "message": "f(x − 7) moves RIGHT by 7 (inside does the opposite of the minus), so add: 3 + 7 = 10. Subtracting to get −4 is the left-shift error."}]

# ---- SILVER ----
silver = pb["silver"]
# s0 (2,6) -f(x) -> -6
silver[0]["guided_steps"] = [
    {"say": "The minus is OUTSIDE the bracket, so −f(x) reflects the graph in the x-axis: every y-value flips sign. x stays at 2."},
    {"pre": "The y-coordinate before flipping is ", "post": "", "answer": 6,
     "hint": "Read it from the point (2, 6)."},
    {"say": "Reflecting multiplies that by −1."},
    {"pre": "New y = 6 × (−1) = ", "post": "", "answer": -6, "phase": "substitute",
     "hint": "Just change the sign."},
    {"pre": "Check the two heights cancel: 6 + (−6) = ", "post": "", "answer": 0, "phase": "substitute",
     "hint": "A number plus its negative.", "done": "Equal and opposite about the x-axis, so the image y is −6."},
]
silver[0]["misconceptions"] = [
    {"pattern": "sign_error", "expect": 6, "note": "no sign change",
     "message": "−f(x) reflects in the x-axis, so the y-coordinate changes sign: 6 becomes −6. Leaving it as 6 misses the reflection."}]

# s1 (-3,4) f(-x) -> x=3
silver[1]["guided_steps"] = [
    {"say": "The minus is INSIDE the bracket, so f(−x) reflects the graph in the y-axis: every x-value flips sign. y stays at 4."},
    {"pre": "The x-coordinate before flipping is ", "post": "", "answer": -3,
     "hint": "Read it from the point (−3, 4)."},
    {"say": "Reflecting multiplies that by −1."},
    {"pre": "New x = (−3) × (−1) = ", "post": "", "answer": 3, "phase": "substitute",
     "hint": "Two negatives make a positive."},
    {"pre": "Check the two x-values cancel: (−3) + 3 = ", "post": "", "answer": 0, "phase": "substitute",
     "hint": "A number plus its negative.", "done": "Equal and opposite about the y-axis, so the image x is 3."},
]
silver[1]["misconceptions"] = [
    {"pattern": "sign_error", "expect": -3, "note": "no sign change",
     "message": "f(−x) reflects in the y-axis, so x changes sign: −3 becomes +3. Leaving it as −3 misses the reflection."}]

# s2 (4,-1) f(x+2)-3 -> y=-4
silver[2]["guided_steps"] = [
    {"say": "Two moves. The +2 inside changes x; the −3 outside changes y. We want the y-coordinate, which the outside part controls."},
    {"pre": "The x-part first: +2 inside moves LEFT, so new x = 4 − 2 = ", "post": "", "answer": 2,
     "hint": "Inside does the opposite: subtract 2."},
    {"say": "Now the y-coordinate, from the −3 outside."},
    {"pre": "New y = −1 − 3 = ", "post": "", "answer": -4, "phase": "substitute",
     "hint": "Take 3 off −1, going further below zero."},
    {"pre": "Check the drop in y: (−1) − (−4) = ", "post": "", "answer": 3, "phase": "substitute",
     "hint": "Old y minus new y.", "done": "Down 3, so the point is (2, −4) and the y-coordinate is −4."},
]
silver[2]["misconceptions"] = [
    {"pattern": "wrong_formula", "expect": -1, "note": "forgot vertical shift",
     "message": "The −3 outside lowers y by 3: −1 − 3 = −4. Leaving y at −1 misses the vertical shift."}]

# s3 MC -f(x) reflection axis -> x-axis (0). ADD CHART y=x^2 & y=-x^2
xs = [-3, -2, -1, 0, 1, 2, 3]
silver[3]["chart"] = chart_two(
    parabola(lambda x: x*x, xs), parabola(lambda x: -x*x, xs),
    -4, 4, -10, 10, xstep=1, ystep=2)
silver[3]["misconceptions"] = [
    {"pattern": "confusion", "expect": 1, "note": "chose y-axis, swapped",
     "message": "−f(x) has the minus OUTSIDE the bracket, so it reflects in the x-axis. f(−x), with the minus inside, is the one that reflects in the y-axis."}]

# s4 REPAIR: was (0,-4) constant -4 (dup with s2). Change vector to (0,-5) -> constant -5. ADD CHART.
silver[4]["display"] = "The curve \\(y = x^2\\) is translated by the vector \\(\\begin{pmatrix} 0 \\\\ -5 \\end{pmatrix}\\). Write the new equation. What is the constant term?"
silver[4]["solutions"] = [-5]
silver[4]["chart"] = chart_two(
    parabola(lambda x: x*x, xs), parabola(lambda x: x*x - 5, xs),
    -4, 4, -6, 10, xstep=1, ystep=2)
silver[4]["guided_steps"] = [
    {"say": "A translation by the vector (0, −5) shifts the curve straight down by 5. So y = x² becomes y = x² − 5."},
    {"pre": "The curve moves DOWN. By how many units? ", "post": "", "answer": 5,
     "hint": "The size of the bottom number in the vector."},
    {"say": "That amount is subtracted from the whole function."},
    {"pre": "The constant term of y = x² − 5 is ", "post": "", "answer": -5, "phase": "substitute",
     "hint": "It is 0 minus 5."},
    {"pre": "Check where the vertex lands: 0 − 5 = ", "post": "", "answer": -5, "phase": "substitute",
     "hint": "The lowest point drops from 0 by 5.", "done": "The vertex falls from (0, 0) to (0, −5), so the constant term is −5."},
]
silver[4]["misconceptions"] = [
    {"pattern": "translation_vector", "expect": 5, "note": "read -5 as up 5",
     "message": "The vector (0, −5) shifts the curve DOWN 5, giving y = x² − 5. The constant term is −5, not +5."}]

# s5 (1,5) f(x-1)+2 -> y=7
silver[5]["guided_steps"] = [
    {"say": "Two moves. The −1 inside changes x; the +2 outside changes y. We want the y-coordinate, from the outside part."},
    {"pre": "The x-part first: −1 inside moves RIGHT, so new x = 1 + 1 = ", "post": "", "answer": 2,
     "hint": "Inside does the opposite: add 1."},
    {"say": "Now the y-coordinate, from the +2 outside."},
    {"pre": "New y = 5 + 2 = ", "post": "", "answer": 7, "phase": "substitute",
     "hint": "Add 2 onto 5."},
    {"pre": "Check the rise in y: 7 − 5 = ", "post": "", "answer": 2, "phase": "substitute",
     "hint": "New y minus old y.", "done": "Up 2, so the point is (2, 7) and the y-coordinate is 7."},
]
silver[5]["misconceptions"] = [
    {"pattern": "wrong_formula", "expect": 5, "note": "forgot vertical shift",
     "message": "The +2 outside lifts y by 2: 5 + 2 = 7. Leaving y at 5 misses the vertical shift."}]

# s6 MC f(-x) reflection axis -> y-axis (1)
silver[6]["misconceptions"] = [
    {"pattern": "confusion", "expect": 0, "note": "chose x-axis, swapped",
     "message": "f(−x) has the minus INSIDE the bracket, affecting x, so it reflects in the y-axis. The x-axis reflection is −f(x)."}]

# ---- GOLD ----
gold = pb["gold"]
# g0 (3,2) 4f(x) -> 8 (vertical stretch x4)
gold[0]["guided_steps"] = [
    {"say": "4f(x) multiplies every y-coordinate by 4. This is a vertical stretch, scale factor 4. x stays at 3."},
    {"pre": "The stretch factor is the number in front of f, which is ", "post": "", "answer": 4,
     "hint": "Read the 4 in 4f(x)."},
    {"say": "Multiply the y-coordinate by it."},
    {"pre": "New y = 2 × 4 = ", "post": "", "answer": 8, "phase": "substitute",
     "hint": "Two multiplied by four."},
    {"pre": "Check by dividing back: 8 ÷ 4 = ", "post": "", "answer": 2, "phase": "substitute",
     "hint": "New y divided by the stretch factor.", "done": "Dividing back gives the original 2, confirming the ×4 stretch, so the image y is 8."},
]
gold[0]["misconceptions"] = [
    {"pattern": "stretch", "expect": 6, "note": "2+4 added instead of multiplied",
     "message": "4f(x) MULTIPLIES the y-coordinate by 4: 2 × 4 = 8. Adding 4 to get 6 treats it as a shift, not a stretch."}]

# g1 (6,5) f(2x) -> x=3 (horizontal compression x1/2)
gold[1]["guided_steps"] = [
    {"say": "f(2x) compresses the graph horizontally, scale factor ½: every x-coordinate is divided by 2. y stays at 5."},
    {"pre": "We divide x by the multiplier inside the bracket, which is ", "post": "", "answer": 2,
     "hint": "The 2 in f(2x)."},
    {"say": "Divide the x-coordinate by it."},
    {"pre": "New x = 6 ÷ 2 = ", "post": "", "answer": 3, "phase": "substitute",
     "hint": "Six divided by two."},
    {"pre": "Check by multiplying back: 3 × 2 = ", "post": "", "answer": 6, "phase": "substitute",
     "hint": "New x times the factor.", "done": "Doubling back gives the original 6, confirming the ÷2, so the image x is 3."},
]
gold[1]["misconceptions"] = [
    {"pattern": "stretch", "expect": 12, "note": "6*2 multiplied instead of divided",
     "message": "f(2x) DIVIDES x by 2: 6 ÷ 2 = 3. Multiplying to get 12 goes the wrong way; inside the bracket affects x inversely."}]

# g2 (4,-3) -f(x)+1 -> y=4
gold[2]["guided_steps"] = [
    {"say": "Two moves on y. First reflect (−f(x) flips the sign), then add 1. x stays at 4."},
    {"pre": "Reflect: −f(x) flips the sign of y, so −3 becomes ", "post": "", "answer": 3,
     "hint": "Change the sign of −3."},
    {"say": "Now the +1 lifts that reflected y."},
    {"pre": "New y = 3 + 1 = ", "post": "", "answer": 4, "phase": "substitute",
     "hint": "Add 1 onto 3."},
    {"pre": "Check the lift: 4 − 3 = ", "post": "", "answer": 1, "phase": "substitute",
     "hint": "New y minus the reflected y.", "done": "Up 1 from the reflected point, so the final y is 4."},
]
gold[2]["misconceptions"] = [
    {"pattern": "combined", "expect": 3, "note": "stopped after reflection",
     "message": "You may have stopped after the reflection. −f(x) gives y = 3, but the +1 then lifts it: 3 + 1 = 4."},
    {"pattern": "combined", "expect": -2, "note": "-3+1 forgot to reflect",
     "message": "−f(x) flips −3 to +3 first, then the +1 gives 4. Adding 1 to −3 (skipping the reflection) gives −2."}]

# g3 (8,2) f(4x) -> x=2 (horizontal compression x1/4)
gold[3]["guided_steps"] = [
    {"say": "f(4x) compresses the graph horizontally, scale factor ¼: every x-coordinate is divided by 4. y stays at 2."},
    {"pre": "We divide x by the multiplier inside the bracket, which is ", "post": "", "answer": 4,
     "hint": "The 4 in f(4x)."},
    {"say": "Divide the x-coordinate by it."},
    {"pre": "New x = 8 ÷ 4 = ", "post": "", "answer": 2, "phase": "substitute",
     "hint": "Eight divided by four."},
    {"pre": "Check by multiplying back: 2 × 4 = ", "post": "", "answer": 8, "phase": "substitute",
     "hint": "New x times the factor.", "done": "Multiplying back gives the original 8, confirming the ÷4, so the image x is 2."},
]
gold[3]["misconceptions"] = [
    {"pattern": "stretch", "expect": 32, "note": "8*4 multiplied instead of divided",
     "message": "f(4x) DIVIDES x by 4: 8 ÷ 4 = 2. Multiplying to get 32 goes the wrong way; inside the bracket affects x inversely."}]

# g4 MC describe y=x^2 -> (x-3)^2+5 -> right 3 up 5 (0). ADD CHART.
gold[4]["chart"] = chart_two(
    parabola(lambda x: x*x, [-3, -2, -1, 0, 1, 2, 3]),
    parabola(lambda x: (x - 3)**2 + 5, [0, 1, 2, 3, 4, 5, 6]),
    -4, 7, 0, 15, xstep=1, ystep=3)
gold[4]["misconceptions"] = [
    {"pattern": "inside_bracket", "expect": 1, "note": "chose left 3, inside-opposite confusion",
     "message": "(x − 3)² has −3 inside the bracket, which moves the curve RIGHT by 3, not left. With +5 outside it also moves up 5."},
    {"pattern": "confusion", "expect": 2, "note": "chose down 5, sign of +5",
     "message": "The +5 is outside the bracket and positive, so the curve moves UP by 5, not down. The inside −3 moves it right 3."}]

# tier descriptions (keep, they are fine and dash-free) but refine gold desc to mention stretches
pb["bronze_description"] = "One transformation applied to one point: a single vertical or horizontal shift written in function notation."
pb["silver_description"] = "Combined shifts, reflections, and transformations of named points such as a maximum, minimum or vertex."
pb["gold_description"] = "Stretches, reflections combined with shifts, translation vectors, and describing a transformation."

# ======================================================================
# 4. tier_guides
# ======================================================================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one shift on one point",
        "steps": [
            "Outside the bracket changes y: <strong>f(x) + a</strong> adds a to the y-coordinate, <strong>f(x) − a</strong> subtracts a.",
            "Inside the bracket changes x and does the opposite: <strong>f(x + a)</strong> moves left (subtract from x), <strong>f(x − a)</strong> moves right (add to x).",
            "Leave the coordinate that is not affected exactly as it was.",
        ],
        "example": {
            "question": "The point (4, 7) lies on y = f(x). Find its image on y = f(x) + 3.",
            "steps": [
                {"label": "Outside the bracket", "content": "<p>\\(+3\\) is outside, so it changes the \\(y\\)-coordinate only.</p>"},
                {"label": "Add 3 to y", "content": "<p>\\(7 + 3 = 10\\); the \\(x\\)-coordinate stays at 4.</p>"},
                {"label": "Check", "content": "<p>Only \\(y\\) moved, by \\(+3\\), exactly what \\(f(x) + 3\\) does.</p>"},
                {"label": "Answer", "content": "<p>New position: <strong>(4, 10)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: combined shifts and named points",
        "steps": [
            "A curve can be shifted horizontally and vertically at once, for example <strong>f(x − 1) + 4</strong>.",
            "Split it: the inside part moves x in the opposite direction, the outside part moves y as written.",
            "A reflection flips a sign: <strong>−f(x)</strong> flips y, <strong>f(−x)</strong> flips x. A named point such as a minimum transforms the same way.",
        ],
        "example": {
            "question": "The minimum of y = f(x) is (2, −3). Find the minimum of y = f(x − 1) + 4.",
            "steps": [
                {"label": "Inside the bracket", "content": "<p>\\(-1\\) inside means move RIGHT by 1: \\(x\\) goes \\(2 \\to 3\\).</p>"},
                {"label": "Outside the bracket", "content": "<p>\\(+4\\) means move UP by 4: \\(y\\) goes \\(-3 \\to 1\\).</p>"},
                {"label": "Check", "content": "<p>Right 1 and up 4 matches \\(f(x - 1) + 4\\).</p>"},
                {"label": "Answer", "content": "<p>New minimum: <strong>(3, 1)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: stretches and describing transformations",
        "steps": [
            "A stretch changes the size of the curve: <strong>af(x)</strong> multiplies every y by a (vertical stretch, factor a).",
            "<strong>f(ax)</strong> divides every x by a (horizontal stretch, factor 1/a), because inside affects x inversely.",
            "To describe a transformation, name the type (translation, reflection or stretch) with its size and direction.",
        ],
        "example": {
            "question": "The point (2, 5) lies on y = f(x). Find its image on y = 2f(x).",
            "steps": [
                {"label": "Vertical stretch", "content": "<p>\\(2f(x)\\) multiplies \\(y\\) by 2: \\(5 \\to 10\\); \\(x\\) stays 2.</p>"},
                {"label": "Check", "content": "<p>\\(10 \\div 2 = 5\\) recovers the original height.</p>"},
                {"label": "Answer", "content": "<p>New position: <strong>(2, 10)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ======================================================================
# 5. guided (opener + teach)
# ======================================================================
opener_svg = ('<svg viewBox="0 0 200 180" role="img" aria-label="A kite 5 metres above calm water '
    'and its mirror reflection the same distance below the surface, marked with a question mark." '
    'style="max-width:280px;width:100%;font-family:Inter,sans-serif">'
    '<rect x="20" y="90" width="160" height="70" fill="#60a5fa" fill-opacity="0.18"/>'
    '<line x1="20" y1="90" x2="180" y2="90" stroke="currentColor" stroke-width="1.4"/>'
    '<text x="176" y="86" font-size="10" fill="currentColor" text-anchor="end">water</text>'
    '<line x1="100" y1="40" x2="100" y2="140" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 3" opacity="0.6"/>'
    '<path d="M100 33 L107 40 L100 47 L93 40 Z" fill="#f59e0b"/>'
    '<text x="112" y="43" font-size="10" fill="currentColor">kite</text>'
    '<text x="70" y="68" font-size="10" fill="currentColor" text-anchor="end">5 m</text>'
    '<path d="M100 133 L107 140 L100 147 L93 140 Z" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="2 2"/>'
    '<text x="112" y="143" font-size="11" fill="currentColor">?</text>'
    '<text x="70" y="118" font-size="10" fill="currentColor" text-anchor="end">5 m</text>'
    '</svg><div style="margin-top:6px">Reflection in the water surface</div>')

pd["guided"] = {
    "opener": {
        "display": opener_svg,
        "steps": [
            {"say": "No algebra, just picture it. A graph is a shape you can slide up or flip over, exactly like a real object."},
            {"pre": "A cable car logs its height each minute. A new sensor reads every height 3 m higher than the old log. At the 5 minute mark the old log said 24 m, so the corrected height is ",
             "post": " m", "answer": 27, "hint": "Add the extra 3 metres on: 24 + 3."},
            {"say": "Adding 3 to every reading slides the whole graph <strong>up</strong> by 3. In function notation that is \\(f(x) + 3\\): the +3 sits OUTSIDE the bracket, so it changes the y-values."},
            {"pre": "A kite flies 5 m above calm water. Its reflection sits the same distance below the surface. Measured as a height above the water, the reflection is at ",
             "post": " m", "answer": -5, "hint": "Below the surface counts as a negative height."},
            {"say": "Flipping every height to the opposite side of the water is a <strong>reflection in the x-axis</strong>. That is \\(-f(x)\\): every y-value is multiplied by −1. Sliding changes the numbers you add; reflecting changes their sign. That is the whole topic."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Solve: the point (2, 4) lies on \\(y = f(x)\\). Find its image on \\(y = f(x) + 5\\).",
            "steps": [
                {"say": "The +5 is OUTSIDE the bracket, so it changes only the y-coordinate. The x-coordinate does not move."},
                {"pre": "The x-coordinate stays the same: x = ", "post": "", "answer": 2, "hint": "Outside the bracket leaves x alone."},
                {"pre": "Add 5 to the y-coordinate: 4 + 5 = ", "post": "", "answer": 9, "hint": "Just add the 5 on."},
                {"say": "So the image is (2, 9)."},
                {"pre": "Check how far y rose: 9 − 4 = ", "post": "", "answer": 5, "hint": "New y minus old y."},
                {"pre": "And how far did x move? ", "post": "", "answer": 0,
                 "hint": "x was 2 and stayed 2.", "done": "Zero. Outside the bracket never moves x. Gone."},
            ],
        },
        "silver": {
            "display": "Solve: the point (1, 5) lies on \\(y = f(x)\\). Find its image on \\(y = f(x - 2) - 3\\).",
            "steps": [
                {"say": "Two moves at once. Split them: the −2 inside the bracket moves x, the −3 outside moves y."},
                {"pre": "Inside the bracket, −2 moves the graph RIGHT by 2, so x: 1 + 2 = ", "post": "", "answer": 3,
                 "hint": "Inside does the opposite, so −2 moves right, which adds."},
                {"pre": "Outside the bracket, −3 moves it DOWN by 3, so y: 5 − 3 = ", "post": "", "answer": 2,
                 "hint": "Subtract the 3 from 5."},
                {"say": "So the image is (3, 2)."},
                {"pre": "Check how far right x moved: 3 − 1 = ", "post": "", "answer": 2, "hint": "New x minus old x."},
                {"pre": "Check how far y moved: 2 − 5 = ", "post": "", "answer": -3,
                 "hint": "Down counts as negative.", "done": "Right 2, down 3, exactly f(x − 2) − 3. Gone."},
            ],
        },
        "gold": {
            "display": "Solve: the point (2, 3) lies on \\(y = f(x)\\). Find its image on \\(y = 3f(x)\\).",
            "steps": [
                {"say": "3f(x) multiplies every y-coordinate by 3. This is a vertical stretch, scale factor 3. The x-coordinate is untouched."},
                {"pre": "The x-coordinate stays the same: x = ", "post": "", "answer": 2, "hint": "A vertical stretch leaves x alone."},
                {"pre": "Multiply the y-coordinate by 3: 3 × 3 = ", "post": "", "answer": 9, "hint": "Three lots of 3."},
                {"say": "So the image is (2, 9)."},
                {"pre": "Check the stretch factor: 9 ÷ 3 = ", "post": "", "answer": 3, "hint": "New y divided by old y."},
                {"pre": "And how far did x move? ", "post": "", "answer": 0,
                 "hint": "x was 2 and stayed 2.", "done": "Zero. A vertical stretch never moves x. Gone."},
            ],
        },
    },
}

# ======================================================================
# 6. Per-problem hints (plain text, one sentence, method move)
# ======================================================================
hints = {
    "bronze": [
        "The +6 is outside the bracket, so add it to the y-coordinate.",
        "The −5 is outside the bracket, so subtract it from the y-coordinate.",
        "The −5 is inside the bracket, so move right: add 5 to the x-coordinate.",
        "The +2 is inside the bracket, so move left: subtract 2 from the x-coordinate.",
        "Outside the bracket changes y and does what it says.",
        "Inside the bracket changes x and does the opposite of the sign.",
        "The +10 is outside the bracket, so add it to the y-coordinate.",
        "The −7 is inside the bracket, so move right: add 7 to the x-coordinate.",
    ],
    "silver": [
        "The minus is outside the bracket, so flip the sign of the y-coordinate.",
        "The minus is inside the bracket, so flip the sign of the x-coordinate.",
        "Only the outside part changes y: subtract 3 from the y-coordinate.",
        "The minus is outside the bracket, affecting the y-values.",
        "A vector (0, k) shifts the curve vertically, so it changes the constant term.",
        "Only the outside part changes y: add 2 to the y-coordinate.",
        "The minus is inside the bracket, affecting the x-values.",
    ],
    "gold": [
        "4f(x) is a vertical stretch: multiply the y-coordinate by 4.",
        "f(2x) is a horizontal compression: divide the x-coordinate by 2.",
        "Flip the sign of y first, then add 1.",
        "f(4x) is a horizontal compression: divide the x-coordinate by 4.",
        "The −3 is inside the bracket and the +5 is outside the bracket.",
    ],
}
for t in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[t]):
        p["hint"] = hints[t][i]

# ---------- write ----------
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", OUT)

# quick internal checks
def wc(s):
    return len([w for w in s.replace("\\(", " ").replace("\\)", " ").split() if w])
for t in ("bronze", "silver", "gold"):
    tot = sum(wc(x) for x in pd["tier_guides"][t]["steps"])
    print("tier_guides", t, "steps words:", tot)
print("method_card content words:", wc(pd["method_card"]["content"]), "steps:", len(pd["method_card"]["steps"]))
for t in ("bronze", "silver", "gold"):
    sols = [tuple(p["solutions"]) for p in pb[t] if p.get("input_type") != "multiple_choice"]
    print(t, "single_value sols:", sols, "unique:", len(set(sols)) == len(sols))
