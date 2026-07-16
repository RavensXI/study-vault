# -*- coding: utf-8 -*-
import json, io

SRC = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_live_graphs-L07.json"
OUT = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\lesson_graphs-L07.json"

pd = json.load(io.open(SRC, encoding="utf-8"))

MINUS = "−"  # proper minus sign
TIMES = "×"

# ---------------------------------------------------------------------------
# 8. method_card (slim reference only)
# ---------------------------------------------------------------------------
pd["method_card"] = {
    "title": "Transforming Graphs with Function Notation",
    "steps": [
        "Outside the bracket changes y and does what it says: f(x) + a moves UP, " + MINUS + "f(x) reflects in the x-axis.",
        "Inside the bracket changes x and does the OPPOSITE: f(x + a) moves LEFT, f(" + MINUS + "x) reflects in the y-axis.",
        "Apply the rule to each key point, shifting or flipping its coordinates.",
        "Check a known point lands sensibly before sketching the new curve."
    ],
    "content": ("<p>Graph transformations use <strong>function notation</strong> \\(f(x)\\). "
                "Four moves matter. <strong>\\(f(x) + a\\)</strong> shifts up by \\(a\\). "
                "<strong>\\(f(x + a)\\)</strong> shifts left by \\(a\\), because inside the bracket "
                "does the opposite. <strong>\\(-f(x)\\)</strong> reflects in the \\(x\\)-axis. "
                "<strong>\\(f(-x)\\)</strong> reflects in the \\(y\\)-axis. "
                "In short: outside the bracket affects \\(y\\) and behaves as expected, while "
                "inside affects \\(x\\) and does the opposite.</p>"),
    "example": ("<p><strong>The point (3, 5) lies on \\(y = f(x)\\). Find its image on \\(y = f(x + 2)\\).</strong></p>"
                "<p>The \\(+2\\) is inside the bracket, so it moves the point LEFT by 2: "
                "\\(x = 3 - 2 = 1\\). The \\(y\\)-coordinate is unchanged, so the image is \\((1, 5)\\).</p>")
}

# ---------------------------------------------------------------------------
# 4. tier_guides
# ---------------------------------------------------------------------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one transformation, one point",
        "steps": [
            "Outside the bracket changes y: <strong>f(x) + a</strong> adds a to the y-coordinate, <strong>" + MINUS + "f(x)</strong> flips the sign of y.",
            "Inside the bracket changes x and does the opposite: <strong>f(x + a)</strong> moves left (subtract from x), <strong>f(" + MINUS + "x)</strong> flips the sign of x.",
            "Leave the coordinate that is not affected exactly as it was."
        ],
        "example": {
            "question": "The point (4, 7) lies on y = f(x). Find its image on y = f(x) + 3.",
            "steps": [
                {"label": "Outside the bracket", "content": "<p>\\(+3\\) is outside, so it changes the \\(y\\)-coordinate only.</p>"},
                {"label": "Add 3 to y", "content": "<p>\\(7 + 3 = 10\\); the \\(x\\)-coordinate stays at 4.</p>"},
                {"label": "Check", "content": "<p>Only \\(y\\) moved, and by \\(+3\\), exactly what \\(f(x) + 3\\) should do.</p>"},
                {"label": "Answer", "content": "<p>New position: <strong>(4, 10)</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: combined shifts and named points",
        "steps": [
            "A curve can be shifted horizontally and vertically at once, for example <strong>f(x " + MINUS + " 3) + 1</strong>.",
            "Split it: the inside part moves x in the opposite direction, the outside part moves y as written.",
            "A vertex, maximum or minimum moves with the curve, so transform its coordinates the same way."
        ],
        "example": {
            "question": "The minimum of y = f(x) is (2, −3). Find the minimum of y = f(x − 1) + 4.",
            "steps": [
                {"label": "Inside the bracket", "content": "<p>\\(-1\\) inside means move RIGHT by 1: \\(x\\) goes \\(2 \\to 3\\).</p>"},
                {"label": "Outside the bracket", "content": "<p>\\(+4\\) means move UP by 4: \\(y\\) goes \\(-3 \\to 1\\).</p>"},
                {"label": "Check", "content": "<p>Right 1 and up 4 matches \\(f(x - 1) + 4\\).</p>"},
                {"label": "Answer", "content": "<p>New minimum: <strong>(3, 1)</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: reflections combined with shifts",
        "steps": [
            "Reflections and translations can stack, for example <strong>" + MINUS + "f(x) + 3</strong> or <strong>f(x + 2) + 3</strong>.",
            "Do them in order: reflect first (flip the sign), then translate (add the shift).",
            "A root sits on the x-axis, so watch its y-value: any vertical shift lifts it off the axis."
        ],
        "example": {
            "question": "The point (2, 5) lies on y = f(x). Find its image on y = −f(x) + 1.",
            "steps": [
                {"label": "Reflect", "content": "<p>\\(-f(x)\\) flips \\(y\\): \\(5 \\to -5\\); \\(x\\) stays 2.</p>"},
                {"label": "Translate", "content": "<p>\\(+1\\) lifts \\(y\\) by 1: \\(-5 \\to -4\\).</p>"},
                {"label": "Check", "content": "<p>Reflect then add 1 gives \\((2, -4)\\).</p>"},
                {"label": "Answer", "content": "<p>New position: <strong>(2, −4)</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------------------------------------------------------------------
# 5. guided.opener + 6. guided.teach
# ---------------------------------------------------------------------------
pd["guided"] = {
    "opener": {
        "steps": [
            {"say": "No algebra, just picture it. A graph is a shape you can slide up or flip over, exactly like a real object."},
            {"pre": "A weather log records the temperature each hour. Today every reading turns out 3°C warmer than the log. At noon the log says 5°C, so today at noon it is ",
             "post": "°C", "answer": 8, "hint": "Add the extra 3 degrees on: 5 + 3."},
            {"say": "Adding 3 to every reading slides the whole graph <strong>up</strong> by 3. Written in function notation that is \\(f(x) + 3\\): the +3 sits OUTSIDE the bracket, so it changes the y-values."},
            {"pre": "A duck floats 5 cm above the water. Its mirror image sits the same distance below. Measured as a height above the water, the reflection is at ",
             "post": " cm", "answer": -5, "hint": "Below the surface counts as a negative height."},
            {"say": "Flipping every height to the opposite side of the water is a <strong>reflection in the x-axis</strong>. That is \\(-f(x)\\): every y-value is multiplied by −1. Sliding changes the numbers you add; reflecting changes their sign. That is the whole topic."}
        ]
    },
    "teach": {
        "bronze": {
            "display": "Solve: the point (2, 6) lies on \\(y = f(x)\\). Find its image on \\(y = f(x) + 5\\).",
            "steps": [
                {"say": "The +5 is OUTSIDE the bracket, so it changes only the y-coordinate. The x-coordinate does not move."},
                {"pre": "The x-coordinate stays the same: x = ", "post": "", "answer": 2, "hint": "Outside the bracket leaves x alone."},
                {"pre": "Add 5 to the y-coordinate: 6 + 5 = ", "post": "", "answer": 11, "hint": "Just add the 5 on."},
                {"say": "So the image is (2, 11)."},
                {"pre": "Check how far y rose: 11 " + MINUS + " 6 = ", "post": "", "answer": 5, "hint": "New y minus old y."},
                {"pre": "And how far did x move? ", "post": "", "answer": 0, "done": "Zero. Outside the bracket never moves x. Gone.", "hint": "x was 2 and stayed 2."}
            ]
        },
        "silver": {
            "display": "Solve: the point (1, 4) lies on \\(y = f(x)\\). Find its image on \\(y = f(x - 2) - 3\\).",
            "steps": [
                {"say": "Two moves at once. Split them: the −2 inside the bracket moves x, the −3 outside moves y."},
                {"pre": "Inside the bracket, " + MINUS + "2 moves the graph RIGHT by 2, so x: 1 + 2 = ", "post": "", "answer": 3, "hint": "Inside does the opposite, so subtracting 2 moves right, which adds."},
                {"pre": "Outside the bracket, " + MINUS + "3 moves it DOWN by 3, so y: 4 " + MINUS + " 3 = ", "post": "", "answer": 1, "hint": "Subtract the 3 from 4."},
                {"say": "So the image is (3, 1)."},
                {"pre": "Check how far right x moved: 3 " + MINUS + " 1 = ", "post": "", "answer": 2, "hint": "New x minus old x."},
                {"pre": "Check how far y moved: 1 " + MINUS + " 4 = ", "post": "", "answer": -3, "done": "Right 2, down 3, exactly f(x " + MINUS + " 2) " + MINUS + " 3. Gone.", "hint": "Down counts as negative."}
            ]
        },
        "gold": {
            "display": "Solve: the point (3, 2) lies on \\(y = f(x)\\). Find its image on \\(y = -f(x) + 5\\).",
            "steps": [
                {"say": "A reflection and a shift together. Do the reflection first, then the translation."},
                {"pre": "Reflect: " + MINUS + "f(x) multiplies y by " + MINUS + "1, so 2 becomes ", "post": "", "answer": -2, "hint": "Flip the sign of the y-coordinate."},
                {"pre": "The x-coordinate is untouched by both moves, so x = ", "post": "", "answer": 3, "hint": "Nothing here changes x."},
                {"pre": "Now translate: +5 adds 5 to y, so " + MINUS + "2 + 5 = ", "post": "", "answer": 3, "hint": "Add 5 to the reflected y."},
                {"say": "So the image is (3, 3)."},
                {"pre": "Check the lift from the reflection: 3 " + MINUS + " (" + MINUS + "2) = ", "post": "", "answer": 5, "done": "Up 5 from the reflected point (3, " + MINUS + "2), landing at (3, 3). Gone.", "hint": "New y minus reflected y."}
            ]
        }
    }
}

# ---------------------------------------------------------------------------
# 3. tier descriptions
# ---------------------------------------------------------------------------
pd["problem_bank"]["bronze_description"] = "One transformation applied to one point: a single shift or a single reflection, written in function notation."
pd["problem_bank"]["silver_description"] = "Combined shifts, or a transformation of a named point such as a maximum, minimum or vertex."
pd["problem_bank"]["gold_description"] = "Reflections stacked with shifts, translation vectors, and the effect of a shift on a root."

# ---------------------------------------------------------------------------
# Rebuild each tier's problems (preserving input_type/calculator, adding
# hint / guided_steps / repaired misconceptions / audit fixes).
# ---------------------------------------------------------------------------

def sub(d):
    d = dict(d)
    d["phase"] = "substitute"
    return d

bronze = [
    # B0 (2,5) f(x)+4 -> y = 9   [audit: rewrite misconception message]
    {
        "display": "The point \\((2, 5)\\) lies on \\(y = f(x)\\). Find the \\(y\\)-coordinate of its image on \\(y = f(x) + 4\\).",
        "solutions": [9], "calculator": False, "input_type": "single_value",
        "hint": "f(x) + 4 adds 4 to the y-coordinate only.",
        "misconceptions": [{
            "pattern": "wrong_formula", "check": "wrong_formula", "expect": 6,
            "message": "You may have used the x-coordinate (2) instead of the y-coordinate (5). f(x) + 4 only changes y: new y = 5 + 4 = 9, not 2 + 4 = 6.",
            "note": "expect 6 = 2 + 4, using x instead of y"}],
        "guided_steps": [
            {"say": "The +4 is OUTSIDE the bracket, so it changes the y-coordinate only. The x-coordinate stays at 2."},
            {"pre": "The graph moves UP. How many units up? ", "post": "", "answer": 4, "hint": "The number outside the bracket, +4."},
            {"say": "So add that to the y-coordinate."},
            sub({"pre": "New y = 5 + 4 = ", "post": "", "answer": 9, "hint": "Add the 4 onto 5."}),
            sub({"pre": "Check how far y rose: 9 " + MINUS + " 5 = ", "post": "", "answer": 4, "done": "Up 4, exactly what f(x) + 4 does, so the image y is 9.", "hint": "New y minus old y."})
        ]
    },
    # B1 (3,1) f(x)-2 -> y = -1  [audit-style message rewrite]
    {
        "display": "The point \\((3, 1)\\) lies on \\(y = f(x)\\). Find the \\(y\\)-coordinate of its image on \\(y = f(x) - 2\\).",
        "solutions": [-1], "calculator": False, "input_type": "single_value",
        "hint": "f(x) − 2 lowers the y-coordinate by 2.",
        "misconceptions": [{
            "pattern": "confusion", "check": "confusion", "expect": 3,
            "message": "f(x) − 2 moves the graph DOWN, so subtract: 1 − 2 = −1. Adding the 2 instead gives 3, which is the wrong direction.",
            "note": "expect 3 = 1 + 2, translating up instead of down"}],
        "guided_steps": [
            {"say": "The −2 is OUTSIDE the bracket, so it changes the y-coordinate only. x stays at 3."},
            {"pre": "The graph moves DOWN. By how many units? ", "post": "", "answer": 2, "hint": "The size of the number outside, 2."},
            {"say": "So subtract that from the y-coordinate."},
            sub({"pre": "New y = 1 " + MINUS + " 2 = ", "post": "", "answer": -1, "hint": "1 take away 2 goes below zero."}),
            sub({"pre": "Check the drop: 1 " + MINUS + " (" + MINUS + "1) = ", "post": "", "answer": 2, "done": "Down 2, exactly f(x) " + MINUS + " 2. The image y is " + MINUS + "1.", "hint": "Old y minus new y."})
        ]
    },
    # B2 MC direction f(x)+3 -> Up (0)
    {
        "display": "\\(y = f(x) + 3\\) is a translation. Which direction does the graph move?",
        "options": ["Up", "Down", "Left", "Right"],
        "solutions": [0], "calculator": False, "input_type": "multiple_choice",
        "hint": "The +3 is outside the bracket, so it changes y, not x.",
        "misconceptions": [{
            "pattern": "confusion", "check": "confusion", "expect": 3,
            "message": "The +3 is OUTSIDE the bracket, so it changes y and moves the graph UP, not sideways. Only changes inside the bracket move it left or right.",
            "note": "expect 3 = Right, outside/inside confusion"}]
    },
    # B3 MC direction f(x+4) -> Left (2)
    {
        "display": "\\(y = f(x + 4)\\) is a translation. Which direction does the graph move?",
        "options": ["Up", "Down", "Left", "Right"],
        "solutions": [2], "calculator": False, "input_type": "multiple_choice",
        "hint": "Inside the bracket does the opposite of the sign shown.",
        "misconceptions": [{
            "pattern": "confusion", "check": "confusion", "expect": 3,
            "message": "f(x + 4) has +4 inside the bracket, and inside does the opposite: the graph moves LEFT by 4, not right.",
            "note": "expect 3 = Right, forgetting inside is opposite"}]
    },
    # B4 (6,2) f(x+3) x -> 3
    {
        "display": "The point \\((6, 2)\\) lies on \\(y = f(x)\\). Find the \\(x\\)-coordinate of its image on \\(y = f(x + 3)\\).",
        "solutions": [3], "calculator": False, "input_type": "single_value",
        "hint": "f(x + 3) moves the point left 3, so subtract from x.",
        "misconceptions": [{
            "pattern": "confusion", "check": "confusion", "expect": 9,
            "message": "f(x + 3) moves the point LEFT by 3, so subtract: 6 − 3 = 3. Adding to get 9 is the right-shift error.",
            "note": "expect 9 = 6 + 3"}],
        "guided_steps": [
            {"say": "The +3 is INSIDE the bracket, so it changes the x-coordinate, and inside does the OPPOSITE: it moves LEFT. y stays at 2."},
            {"pre": "Moving left means we subtract. By how many? ", "post": "", "answer": 3, "hint": "The number inside the bracket, 3."},
            {"say": "Take that off the x-coordinate."},
            sub({"pre": "New x = 6 " + MINUS + " 3 = ", "post": "", "answer": 3, "hint": "6 take away 3."}),
            sub({"pre": "Check: y is untouched, so how far did y move? ", "post": "", "answer": 0, "done": "x moved left 3, y stayed put. The image x is 3.", "hint": "Inside the bracket never changes y."})
        ]
    },
    # B5 MC -f(x) axis -> x-axis (0)
    {
        "display": "\\(y = -f(x)\\) is a reflection. In which axis?",
        "options": ["x-axis", "y-axis", "line y = x", "line y = -x"],
        "solutions": [0], "calculator": False, "input_type": "multiple_choice",
        "hint": "A negative outside the bracket flips y, reflecting in the x-axis.",
        "misconceptions": [{
            "pattern": "confusion", "check": "confusion", "expect": 1,
            "message": "−f(x) has the minus OUTSIDE the bracket, so it reflects in the x-axis. f(−x), with the minus inside, is the one that reflects in the y-axis.",
            "note": "expect 1 = y-axis, swapping the two reflections"}]
    },
    # B6 MC f(-x) axis -> y-axis (1)
    {
        "display": "\\(y = f(-x)\\) is a reflection. In which axis?",
        "options": ["x-axis", "y-axis", "line y = x", "line y = -x"],
        "solutions": [1], "calculator": False, "input_type": "multiple_choice",
        "hint": "A negative inside the bracket flips x, reflecting in the y-axis.",
        "misconceptions": [{
            "pattern": "confusion", "check": "confusion", "expect": 0,
            "message": "f(−x) has the minus INSIDE the bracket, affecting x, so it reflects in the y-axis. The x-axis reflection is −f(x).",
            "note": "expect 0 = x-axis, swapping the two reflections"}]
    },
    # B7 (5,8) -f(x) y -> -8
    {
        "display": "The point \\((5, 8)\\) lies on \\(y = f(x)\\). Find the \\(y\\)-coordinate of its image on \\(y = -f(x)\\).",
        "solutions": [-8], "calculator": False, "input_type": "single_value",
        "hint": "−f(x) flips the sign of the y-coordinate.",
        "misconceptions": [{
            "pattern": "sign_error", "check": "sign_error", "expect": 8,
            "message": "−f(x) reflects in the x-axis, so the y-coordinate changes sign: 8 becomes −8. Leaving it as 8 misses the reflection.",
            "note": "expect 8 = no sign change"}],
        "guided_steps": [
            {"say": "The minus is OUTSIDE the bracket, so " + MINUS + "f(x) reflects the graph in the x-axis: every y-value flips sign. x stays at 5."},
            {"pre": "Before flipping, the y-coordinate is ", "post": "", "answer": 8, "hint": "Read it straight from the point (5, 8)."},
            {"say": "Reflecting multiplies that by −1."},
            sub({"pre": "New y = 8 " + TIMES + " (" + MINUS + "1) = ", "post": "", "answer": -8, "hint": "Just change the sign."}),
            sub({"pre": "Check the two heights cancel: 8 + (" + MINUS + "8) = ", "post": "", "answer": 0, "done": "Equal and opposite about the x-axis, so the image y is " + MINUS + "8.", "hint": "A number plus its negative."})
        ]
    }
]

silver = [
    # S0 (-1,4) f(-x) x -> 1
    {
        "display": "The point \\((-1, 4)\\) lies on \\(y = f(x)\\). Find the \\(x\\)-coordinate of its image on \\(y = f(-x)\\).",
        "solutions": [1], "calculator": False, "input_type": "single_value",
        "hint": "f(−x) flips the sign of the x-coordinate.",
        "misconceptions": [{
            "pattern": "confusion", "check": "confusion", "expect": -1,
            "message": "f(−x) reflects in the y-axis, so x changes sign: −1 becomes +1. Leaving it as −1 misses the reflection.",
            "note": "expect -1 = no sign change"}],
        "guided_steps": [
            {"say": "The minus is INSIDE the bracket, so f(" + MINUS + "x) reflects the graph in the y-axis: every x-value flips sign. y stays at 4."},
            {"pre": "Before flipping, the x-coordinate is ", "post": "", "answer": -1, "hint": "Read it from the point (" + MINUS + "1, 4)."},
            {"say": "Reflecting multiplies that by −1."},
            sub({"pre": "New x = (" + MINUS + "1) " + TIMES + " (" + MINUS + "1) = ", "post": "", "answer": 1, "hint": "Two negatives make a positive."}),
            sub({"pre": "Check the two x-values cancel: (" + MINUS + "1) + 1 = ", "post": "", "answer": 0, "done": "Equal and opposite about the y-axis, so the image x is 1.", "hint": "A number plus its negative."})
        ]
    },
    # S1 max (3,7) f(x)-5 y -> 2
    {
        "display": "The maximum point of \\(y = f(x)\\) is \\((3, 7)\\). Find the \\(y\\)-coordinate of the maximum of \\(y = f(x) - 5\\).",
        "solutions": [2], "calculator": False, "input_type": "single_value",
        "hint": "f(x) − 5 lowers the maximum's y by 5.",
        "misconceptions": [{
            "pattern": "wrong_formula", "check": "wrong_formula", "expect": 7,
            "message": "f(x) − 5 lowers the maximum by 5: 7 − 5 = 2. Leaving y at 7 forgets the downward shift.",
            "note": "expect 7 = no shift applied"}],
        "guided_steps": [
            {"say": "The maximum point moves with the curve. The −5 is OUTSIDE, so it lowers the y-coordinate; x stays at 3."},
            {"pre": "The graph moves DOWN by how many? ", "post": "", "answer": 5, "hint": "The number outside the bracket, 5."},
            {"say": "Take that off the maximum's y-coordinate."},
            sub({"pre": "New y = 7 " + MINUS + " 5 = ", "post": "", "answer": 2, "hint": "7 take away 5."}),
            sub({"pre": "Check the drop: 7 " + MINUS + " 2 = ", "post": "", "answer": 5, "done": "Down 5, so the new maximum y is 2.", "hint": "Old y minus new y."})
        ]
    },
    # S2 min (2,-3) f(x-4) x -> 6
    {
        "display": "The minimum point of \\(y = f(x)\\) is \\((2, -3)\\). Find the \\(x\\)-coordinate of the minimum of \\(y = f(x - 4)\\).",
        "solutions": [6], "calculator": False, "input_type": "single_value",
        "hint": "f(x − 4) moves the minimum right 4, so add to x.",
        "misconceptions": [{
            "pattern": "confusion", "check": "confusion", "expect": -2,
            "message": "f(x − 4) moves RIGHT by 4 (inside does the opposite), so add: 2 + 4 = 6. Subtracting to get −2 is the left-shift error.",
            "note": "expect -2 = 2 - 4"}],
        "guided_steps": [
            {"say": "The minimum moves with the curve. The −4 is INSIDE, and inside does the OPPOSITE, so the graph moves RIGHT; y stays at −3."},
            {"pre": "Moving right means we add. Add how many? ", "post": "", "answer": 4, "hint": "The number inside the bracket, 4."},
            {"say": "Add that to the x-coordinate."},
            sub({"pre": "New x = 2 + 4 = ", "post": "", "answer": 6, "hint": "2 add 4."}),
            sub({"pre": "Check how far right it moved: 6 " + MINUS + " 2 = ", "post": "", "answer": 4, "done": "Right 4, so the new minimum x is 6.", "hint": "New x minus old x."})
        ]
    },
    # S3 vector x-component  [audit: reworded display, 'single' removed]
    {
        "display": "The curve \\(y = x^2\\) is transformed to \\(y = (x - 3)^2 + 1\\) by a translation. Give the \\(x\\)-component of the translation vector.",
        "solutions": [3], "calculator": False, "input_type": "single_value",
        "hint": "The number added outside is the y-shift; inside gives the x-shift in the opposite direction.",
        "misconceptions": [{
            "pattern": "confusion", "check": "confusion", "expect": -3,
            "message": "(x − 3) has −3 inside the bracket, which means move RIGHT by 3 (inside does the opposite). The x-component is +3, not −3.",
            "note": "expect -3 = reading the inside sign literally"}],
        "guided_steps": [
            {"say": "A translation vector is written as (x-shift, y-shift). Find each part from the equation."},
            {"pre": "The +1 outside the bracket shifts the curve up. That is the y-component: ", "post": "", "answer": 1, "hint": "The number added outside, +1."},
            {"say": "Now the horizontal part, from inside the bracket."},
            sub({"pre": "Inside is (x " + MINUS + " 3). Inside does the opposite, so the curve moves RIGHT by ", "post": "", "answer": 3, "hint": "The size of the number inside the bracket, 3."}),
            sub({"pre": "Check: a point at x = 0 on y = x² lands at x = ", "post": "", "answer": 3, "done": "Moved right 3, so the x-component is 3. Vector (3, 1).", "hint": "0 shifted right by 3."})
        ]
    },
    # S4 (0,5) f(x+2)-1 y -> 4   [changed from (0,4) to break duplicate solution with S3]
    {
        "display": "The graph \\(y = f(x)\\) passes through \\((0, 5)\\). What point does \\(y = f(x + 2) - 1\\) pass through? Give the \\(y\\)-coordinate.",
        "solutions": [4], "calculator": False, "input_type": "single_value",
        "hint": "The −1 outside lowers the y-coordinate by 1.",
        "misconceptions": [{
            "pattern": "wrong_formula", "check": "wrong_formula", "expect": 5,
            "message": "The −1 outside lowers y by 1: 5 − 1 = 4. Leaving y at 5 misses the vertical shift.",
            "note": "expect 5 = no vertical shift"}],
        "guided_steps": [
            {"say": "Two moves. The +2 inside changes x; the −1 outside changes y. We want the y-coordinate, which the outside part controls."},
            {"pre": "The x-part first: +2 inside moves LEFT, so new x = 0 " + MINUS + " 2 = ", "post": "", "answer": -2, "hint": "Inside does the opposite: subtract 2."},
            {"say": "Now the y-coordinate, from the −1 outside."},
            sub({"pre": "New y = 5 " + MINUS + " 1 = ", "post": "", "answer": 4, "hint": "Take 1 off the 5."}),
            sub({"pre": "Check the drop in y: 5 " + MINUS + " 4 = ", "post": "", "answer": 1, "done": "Down 1, so the point is (" + MINUS + "2, 4) and the y-coordinate is 4.", "hint": "Old y minus new y."})
        ]
    },
    # S5 (4,-2) reflect y-axis new x -> -4
    {
        "display": "The point \\((4, -2)\\) lies on \\(y = f(x)\\). It is reflected in the \\(y\\)-axis to give \\(y = f(-x)\\). What is the new \\(x\\)-coordinate?",
        "solutions": [-4], "calculator": False, "input_type": "single_value",
        "hint": "Reflecting in the y-axis changes the sign of x.",
        "misconceptions": [{
            "pattern": "sign_error", "check": "sign_error", "expect": 4,
            "message": "Reflecting in the y-axis changes the sign of x: 4 becomes −4. Leaving it as 4 misses the reflection.",
            "note": "expect 4 = no sign change"}],
        "guided_steps": [
            {"say": "Reflecting in the y-axis flips the sign of every x-coordinate. y stays at −2."},
            {"pre": "The x-coordinate before reflecting is ", "post": "", "answer": 4, "hint": "Read it from (4, " + MINUS + "2)."},
            {"say": "Multiply that by −1."},
            sub({"pre": "New x = 4 " + TIMES + " (" + MINUS + "1) = ", "post": "", "answer": -4, "hint": "Change the sign."}),
            sub({"pre": "Check the two x-values cancel: 4 + (" + MINUS + "4) = ", "post": "", "answer": 0, "done": "Equal and opposite about the y-axis, so the new x is " + MINUS + "4.", "hint": "A number plus its negative."})
        ]
    },
    # S6 (-3,6) -f(x) y -> -6
    {
        "display": "The point \\((-3, 6)\\) lies on \\(y = f(x)\\). Find the \\(y\\)-coordinate of its image on \\(y = -f(x)\\).",
        "solutions": [-6], "calculator": False, "input_type": "single_value",
        "hint": "−f(x) changes the sign of y.",
        "misconceptions": [{
            "pattern": "sign_error", "check": "sign_error", "expect": 6,
            "message": "−f(x) reflects in the x-axis, so y changes sign: 6 becomes −6. Leaving it as 6 misses the reflection.",
            "note": "expect 6 = no sign change"}],
        "guided_steps": [
            {"say": "−f(x) reflects in the x-axis, flipping the sign of every y-coordinate. x stays at −3."},
            {"pre": "The y-coordinate before reflecting is ", "post": "", "answer": 6, "hint": "Read it from (" + MINUS + "3, 6)."},
            {"say": "Multiply that by −1."},
            sub({"pre": "New y = 6 " + TIMES + " (" + MINUS + "1) = ", "post": "", "answer": -6, "hint": "Change the sign."}),
            sub({"pre": "Check the two y-values cancel: 6 + (" + MINUS + "6) = ", "post": "", "answer": 0, "done": "Equal and opposite about the x-axis, so the new y is " + MINUS + "6.", "hint": "A number plus its negative."})
        ]
    }
]

gold = [
    # G0 (x+1)^2 - 4 vertex y -> -4
    {
        "display": "The curve \\(y = x^2\\) is transformed to \\(y = (x + 1)^2 - 4\\). State the coordinates of the vertex of the new curve. Give the \\(y\\)-coordinate.",
        "solutions": [-4], "calculator": False, "input_type": "single_value",
        "hint": "The vertex of y = x² is (0, 0); apply the shifts to it.",
        "misconceptions": [{
            "pattern": "confusion", "check": "confusion", "expect": 0,
            "message": "You may have found only the horizontal shift. The vertex of y = x² starts at (0, 0); (x + 1)² moves it left to (−1, 0), and the −4 then drops it to (−1, −4). The y-coordinate is −4, not 0.",
            "note": "expect 0 = vertical shift ignored"}],
        "guided_steps": [
            {"say": "Start from the vertex of y = x², which sits at (0, 0). Apply the two moves to it."},
            {"pre": "Inside is (x + 1). Inside does the opposite, so the vertex moves LEFT by 1: new x = 0 " + MINUS + " 1 = ", "post": "", "answer": -1, "hint": "0 minus 1."},
            {"say": "Now the vertical move, from the −4 outside. We want this y-coordinate."},
            sub({"pre": "New y = 0 " + MINUS + " 4 = ", "post": "", "answer": -4, "hint": "The vertex y drops by 4."}),
            sub({"pre": "Check the drop: 0 " + MINUS + " (" + MINUS + "4) = ", "post": "", "answer": 4, "done": "Down 4 from the origin, so the vertex is (" + MINUS + "1, " + MINUS + "4) and its y-coordinate is " + MINUS + "4.", "hint": "Old y minus new y."})
        ]
    },
    # G1 MC sin reflected in x-axis -> -sin x (1)
    {
        "display": "The graph of \\(y = \\sin x\\) is reflected in the \\(x\\)-axis. Write the equation of the new graph. Which of these is correct?",
        "options": ["y = sin(-x)", "y = -sin x", "y = sin x + 1", "y = cos x"],
        "solutions": [1], "calculator": False, "input_type": "multiple_choice",
        "hint": "Reflection in the x-axis multiplies the whole function by −1.",
        "misconceptions": [{
            "pattern": "confusion", "check": "confusion", "expect": 0,
            "message": "Reflection in the x-axis multiplies the output by −1, giving y = −sin x. y = sin(−x) is a reflection in the y-axis instead.",
            "note": "expect 0 = y = sin(-x), the y-axis reflection"}]
    },
    # G2 -f(x) then +3, (2,5) final y -> -2
    {
        "display": "Two transformations are applied: first \\(y = f(x)\\) becomes \\(y = -f(x)\\), then that becomes \\(y = -f(x) + 3\\). The point \\((2, 5)\\) is on the original. Find the final \\(y\\)-coordinate.",
        "solutions": [-2], "calculator": False, "input_type": "single_value",
        "hint": "Reflect the y-value first, then add 3.",
        "misconceptions": [{
            "pattern": "wrong_formula", "check": "wrong_formula", "expect": -5,
            "message": "You may have stopped after the reflection. −f(x) gives y = −5, but the +3 then lifts it: −5 + 3 = −2.",
            "note": "expect -5 = reflection only, +3 forgotten"}],
        "guided_steps": [
            {"say": "Two steps on the y-coordinate. First reflect, then add 3. x stays at 2."},
            {"pre": "Reflect: " + MINUS + "f(x) flips the sign of y, so 5 becomes ", "post": "", "answer": -5, "hint": "Change the sign of 5."},
            {"say": "Now the +3 lifts that reflected y."},
            sub({"pre": "New y = (" + MINUS + "5) + 3 = ", "post": "", "answer": -2, "hint": "Start at " + MINUS + "5 and add 3."}),
            sub({"pre": "Check the lift: (" + MINUS + "2) " + MINUS + " (" + MINUS + "5) = ", "post": "", "answer": 3, "done": "Up 3 from the reflection, so the final y is " + MINUS + "2.", "hint": "New y minus reflected y."})
        ]
    },
    # G3 MC  [audit: rebuilt broken/ambiguous MC + updated solution]
    {
        "display": "The point \\((a, b)\\) on \\(y = f(x)\\) maps to \\((-a, -b)\\). Which two transformations produce this?",
        "options": ["−f(x) then f(−x)", "−f(x) only", "f(−x) only", "f(x) + b then f(x + a)"],
        "solutions": [0], "calculator": False, "input_type": "multiple_choice",
        "hint": "Flipping BOTH coordinates needs BOTH reflections, one for x and one for y.",
        "misconceptions": [
            {"pattern": "confusion", "check": "confusion", "expect": 1,
             "message": "−f(x) on its own only flips y, giving (a, −b). To flip x as well you also need f(−x). Both reflections together give (−a, −b).",
             "note": "expect 1 = -f(x) only"},
            {"pattern": "confusion", "check": "confusion", "expect": 2,
             "message": "f(−x) on its own only flips x, giving (−a, b). You also need −f(x) to flip y. Both reflections together give (−a, −b).",
             "note": "expect 2 = f(-x) only"}
        ]
    },
    # G4 MC root  [audit: fixed contradictory distractor + removed em dashes]
    {
        "display": "The curve \\(y = f(x)\\) has a root at \\(x = 5\\). After the transformation \\(y = f(x + 2) + 3\\), does the curve still pass through the \\(x\\)-axis at \\(x = 3\\)?",
        "options": [
            "Yes, it still crosses the x-axis at x = 3",
            "No, the point that was the root is now at (3, 3)",
            "No, the point that was the root is now at (5, 3)",
            "No, the point that was the root is now at (7, 3)"
        ],
        "solutions": [1], "calculator": False, "input_type": "multiple_choice",
        "hint": "Move the root (5, 0) left 2, then up 3.",
        "misconceptions": [
            {"pattern": "confusion", "check": "confusion", "expect": 0,
             "message": "The +3 outside lifts every point up by 3, so the old root at (3, 0) rises to (3, 3). It no longer touches the x-axis, so the answer is not Yes.",
             "note": "expect 0 = Yes, vertical shift forgotten"},
            {"pattern": "confusion", "check": "confusion", "expect": 3,
             "message": "f(x + 2) has +2 inside the bracket, so the graph moves LEFT by 2: the root's x goes 5 to 3, not 7. Adding the +3 lands it at (3, 3).",
             "note": "expect 3 = shifted right instead of left"},
            {"pattern": "confusion", "check": "confusion", "expect": 2,
             "message": "The +2 inside the bracket moves the root LEFT, from x = 5 to x = 3. With the +3 up, the point is at (3, 3), not (5, 3).",
             "note": "expect 2 = horizontal shift forgotten"}
        ]
    }
]

pd["problem_bank"]["bronze"] = bronze
pd["problem_bank"]["silver"] = silver
pd["problem_bank"]["gold"] = gold

# Mandatory style fix: strip em dashes from the preserved worked_examples
# (validator enforces no em dashes in any student-facing string).
EM = "—"
for we in pd.get("worked_examples") or []:
    for st in we.get("steps") or []:
        if isinstance(st.get("label"), str):
            st["label"] = st["label"].replace(" " + EM + " ", ": ").replace(EM, ":")
        if isinstance(st.get("content"), str):
            st["content"] = st["content"].replace(" " + EM + " ", ", ").replace(EM, ",")

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written", OUT)
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
