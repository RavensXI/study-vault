# -*- coding: utf-8 -*-
"""Build the full guided practice_data for maths-eduqas algebra-L08
   (Quadratic Formula & Completing the Square)."""
import json, io

live = json.load(io.open('_live_algebra-L08.json', encoding='utf-8'))

def box(pre, ans, hint, post="", **kw):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    d.update(kw)
    return d
def say(text, **kw):
    d = {"say": text}; d.update(kw); return d

# ---------------- METHOD CARD ----------------
method_card = {
    "title": "Quadratic Formula & Completing the Square",
    "steps": [
        "Read off \\(a\\), \\(b\\), \\(c\\) from \\(ax^2 + bx + c = 0\\), signs included.",
        "Formula: \\(x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}\\).",
        "Complete the square: halve the \\(x\\) coefficient, square it, adjust the constant.",
        "Discriminant \\(b^2 - 4ac\\): positive gives 2 roots, zero gives 1, negative gives none.",
    ],
    "content": live["method_card"]["content"],
    "example": live["method_card"]["example"],
}

# ---------------- OPENER (area model of x^2 + 6x) ----------------
opener_svg = (
    '<svg viewBox="0 0 240 200" role="img" '
    'aria-label="A square of side x with area x squared, two 3-by-x strips added to '
    'the right and bottom, and a dashed 3 by 3 corner square of area 9 needed to '
    'complete a bigger square of side x plus 3." '
    'font-family="Inter, sans-serif" font-size="11">'
    '<rect x="30" y="30" width="100" height="100" fill="#60a5fa" fill-opacity="0.3" '
    'stroke="currentColor"/>'
    '<rect x="130" y="30" width="30" height="100" fill="#34d399" fill-opacity="0.3" '
    'stroke="currentColor"/>'
    '<rect x="30" y="130" width="100" height="30" fill="#34d399" fill-opacity="0.3" '
    'stroke="currentColor"/>'
    '<rect x="130" y="130" width="30" height="30" fill="#f59e0b" fill-opacity="0.3" '
    'stroke="currentColor" stroke-dasharray="4 3"/>'
    '<text x="80" y="84" text-anchor="middle" fill="currentColor">x²</text>'
    '<text x="145" y="84" text-anchor="middle" fill="currentColor">3x</text>'
    '<text x="80" y="149" text-anchor="middle" fill="currentColor">3x</text>'
    '<text x="145" y="149" text-anchor="middle" fill="currentColor">9</text>'
    '<text x="80" y="22" text-anchor="middle" fill="currentColor">x</text>'
    '<text x="145" y="22" text-anchor="middle" fill="currentColor">3</text>'
    '<text x="20" y="84" text-anchor="middle" fill="currentColor">x</text>'
    '<text x="20" y="149" text-anchor="middle" fill="currentColor">3</text>'
    '</svg>'
)
opener = {
    "label": "Before any algebra",
    "display": opener_svg + '<br>Turn <strong>x² + 6x</strong> into one perfect square.',
    "steps": [
        say("Here is a square tile of side x, so its area is x². Next to it is a "
            "strip worth 6x. We will cut and rearrange the whole thing into ONE bigger "
            "square. First, split the 6x strip into two equal strips for two sides."),
        box("Split the strip evenly: 6 ÷ 2 = ", 3,
            "Halve the 6 so each side gets the same."),
        say("Stick a 3-wide strip on the right and a 3-wide strip on the bottom. They "
            "almost build a big square of side (x + 3), but the little corner is empty."),
        box("The empty corner is a 3 by 3 square, so its area is 3 × 3 = ", 9,
            "Three squared."),
        say("So x² + 6x, plus that 9 corner, is exactly (x + 3)². That means "
            "\\(x^2 + 6x = (x+3)^2 - 9\\). You just <strong>completed the square</strong>: "
            "halve the middle number (6 becomes 3), square it (9), and take it back off. "
            "The quadratic formula is this same trick done once, in general, on "
            "\\(ax^2 + bx + c = 0\\)."),
    ],
}

# ---------------- TEACH WALKS ----------------
teach = {
    "bronze": {
        "display": "Find the discriminant of \\(x^2 + 4x - 1 = 0\\)",
        "label": "Together: your first discriminant",
        "steps": [
            say("Line the equation up with ax² + bx + c and read each number."),
            box("a, in front of x² = ", 1, "There is an invisible 1."),
            box("b, in front of x = ", 4, "The x coefficient."),
            box("c, on its own = ", -1, "Keep the minus sign."),
            say("The discriminant is b² − 4ac. Take it in pieces.", phase="substitute"),
            box("b² = 4 × 4 = ", 16, "Square b."),
            box("4ac = 4 × 1 × (−1) = ", -4, "Multiply 4, a and c, keeping the minus."),
            box("b² − 4ac = 16 − (−4) = ", 20,
                "Minus a negative adds.", done="Positive, so two real roots."),
        ],
    },
    "silver": {
        "display": "Solve \\(x^2 + 2x - 4 = 0\\) with the formula. Positive root to 2 d.p. (calculator)",
        "label": "Together: the silver move",
        "steps": [
            say("Read off a = 1, b = 2, c = −4, then use the formula."),
            box("Discriminant b² − 4ac = 4 − 4 × 1 × (−4) = ", 20,
                "Minus a negative adds: 4 + 16."),
            box("√20 to 2 d.p. = ", 4.47, "Square root on the calculator."),
            say("The positive root uses +√, all over 2a = 2.", phase="substitute"),
            box("(−2 + √20) ÷ 2 = (2 d.p.) ", 1.24,
                "Use the un-rounded root, then divide by 2."),
            box("The other root: (−2 − √20) ÷ 2 = (2 d.p.) ", -3.24,
                "Same working with a minus.", done="So the positive root is 1.24."),
        ],
    },
    "gold": {
        "display": "Write \\(2x^2 + 8x + 3\\) in the form \\(a(x+p)^2 + q\\). Find q.",
        "label": "Together: the gold move",
        "steps": [
            say("Factor the 2 out of the x² and x terms only."),
            box("Inside the bracket: 8 ÷ 2 = ", 4,
                "Divide the x coefficient by the 2 you took out."),
            say("Now complete the square on x² + 4x: halve the 4."),
            box("4 ÷ 2 = ", 2, "This is p."),
            box("Square it: 2² = ", 4, "The amount subtracted inside."),
            say("Inside becomes (x + 2)² − 4. Multiply the −4 back by 2, then add the 3.",
                phase="substitute"),
            box("2 × (−4) = ", -8, "The −4 was inside a bracket times 2."),
            box("q = −8 + 3 = ", -5, "Add the leftover 3.", done="So q = −5."),
        ],
    },
}

# ---------------- TIER GUIDES ----------------
tier_guides = {
    "bronze": {
        "title": "Bronze: read off a, b, c and the discriminant",
        "steps": [
            "Every quadratic \\(ax^2 + bx + c = 0\\) has three numbers: \\(a\\) in front of "
            "\\(x^2\\), \\(b\\) in front of \\(x\\), \\(c\\) on its own. Signs count.",
            "The <strong>discriminant</strong> \\(b^2 - 4ac\\) tells you the roots: positive "
            "gives 2, zero gives 1, negative gives none.",
            "To start completing the square on \\(x^2 + bx\\): halve \\(b\\) to get \\(p\\), "
            "then subtract \\(p^2\\), giving \\((x+p)^2 - p^2\\).",
        ],
        "example": {
            "question": "Find the discriminant of x² + 3x + 1 = 0",
            "steps": [
                {"label": "Identify", "content": "<p>\\(a = 1\\), \\(b = 3\\), \\(c = 1\\)</p>"},
                {"label": "b²", "content": "<p>\\(3^2 = 9\\)</p>"},
                {"label": "4ac", "content": "<p>\\(4 \\times 1 \\times 1 = 4\\)</p>"},
                {"label": "Subtract", "content": "<p>\\(9 - 4 = 5\\)</p>"},
                {"label": "Answer", "content": "<p>Discriminant \\(= 5\\) (two real roots)</p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: use the formula, or complete the square",
        "steps": [
            "The <strong>quadratic formula</strong> \\(x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\\) "
            "solves any quadratic. With a calculator, find the discriminant first, then each root.",
            "The \\(+\\) gives the larger root, the \\(-\\) gives the smaller. Round only at the end.",
            "To complete the square on \\(x^2 + bx + c\\): halve \\(b\\) for \\(p\\), then "
            "\\(q = c - p^2\\). The least value of the expression is \\(q\\).",
        ],
        "example": {
            "question": "Complete the square for x² + 6x + 1",
            "steps": [
                {"label": "Halve", "content": "<p>\\(6 \\div 2 = 3\\), so \\(p = 3\\)</p>"},
                {"label": "Square", "content": "<p>\\(3^2 = 9\\)</p>"},
                {"label": "Adjust", "content": "<p>\\(q = 1 - 9 = -8\\)</p>"},
                {"label": "Answer", "content": "<p>\\((x+3)^2 - 8\\); least value \\(-8\\)</p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: leading coefficients, conditions and turning points",
        "steps": [
            "When \\(a \\neq 1\\), factor \\(a\\) out of the \\(x^2\\) and \\(x\\) terms first, "
            "complete the square inside, then multiply back and tidy the constant.",
            "The discriminant is also a condition: one solution needs \\(b^2-4ac=0\\); no real "
            "roots needs \\(b^2-4ac<0\\).",
            "Completing the square gives the turning point of \\(y = x^2 + bx + c\\) at "
            "\\((-p,\\ q)\\). The two roots add up to \\(-b/a\\).",
        ],
        "example": {
            "question": "Find the turning point of y = x² − 2x + 5",
            "steps": [
                {"label": "Halve", "content": "<p>\\(-2 \\div 2 = -1\\), so \\(p = -1\\)</p>"},
                {"label": "Adjust", "content": "<p>\\(q = 5 - (-1)^2 = 4\\)</p>"},
                {"label": "Read off", "content": "<p>Turning point at \\((-p,\\ q) = (1,\\ 4)\\)</p>"},
                {"label": "Answer", "content": "<p>\\((1,\\ 4)\\); y-coordinate \\(4\\)</p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

def mc(pattern, expect, message):
    return {"pattern": pattern, "expect": expect, "message": message}

# ---------------- BRONZE ----------------
bronze = [
 {"display": "For \\(x^2 + 7x - 5 = 0\\), state the values of \\(a\\), \\(b\\), \\(c\\). What is \\(b\\)?",
  "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "b is the number in front of x, with its sign.",
  "misconceptions": [mc("read_c_not_b", [-5],
     "b is the coefficient of x, which is 7. The value −5 is c, the constant.")],
  "guided_steps": [
     say("Compare \\(x^2 + 7x - 5\\) with \\(ax^2 + bx + c\\), matching term by term."),
     box("a, from the x² term = ", 1, "There is an invisible 1."),
     box("c, the constant with its sign = ", -5, "Keep the minus."),
     say("b is the coefficient of the x term, and that is what the question wants.",
         phase="substitute"),
     box("b = ", 7, "The number multiplying x."),
     box("Check: rebuild it as 1x² + __x − 5. The blank is ", 7,
         "It must match the b you found.", done="So b = 7."),
  ]},
 {"display": "Find the discriminant of \\(x^2 + 4x + 1 = 0\\).",
  "solutions": [12], "calculator": False, "input_type": "single_value",
  "hint": "Work out b² − 4ac.",
  "misconceptions": [mc("added_not_subtracted", [20],
     "The discriminant subtracts: 16 − 4 = 12. Adding the two parts gives 20.")],
  "guided_steps": [
     say("Read off a = 1, b = 4, c = 1."),
     box("b² = 4 × 4 = ", 16, "Square b."),
     box("4ac = 4 × 1 × 1 = ", 4, "Multiply 4, a and c."),
     say("Now subtract to get the discriminant.", phase="substitute"),
     box("b² − 4ac = 16 − 4 = ", 12, "Subtract 4ac from b²."),
     box("Enter the number of real roots: ", 2,
         "A positive discriminant means two.", done="12 is positive, so two real roots."),
  ]},
 {"display": "Find the discriminant of \\(x^2 - 6x + 9 = 0\\).",
  "solutions": [0], "calculator": False, "input_type": "single_value",
  "hint": "b is −6, and (−6)² is positive.",
  "misconceptions": [mc("added_not_subtracted", [72],
     "The discriminant is 36 − 36 = 0. Adding the parts gives 72.")],
  "guided_steps": [
     say("Read off a = 1, b = −6, c = 9."),
     box("b² = (−6) × (−6) = ", 36, "A minus times a minus is a plus."),
     box("4ac = 4 × 1 × 9 = ", 36, "Multiply 4, a and c."),
     say("Now subtract.", phase="substitute"),
     box("b² − 4ac = 36 − 36 = ", 0, "Same numbers, so zero."),
     box("Number of real roots when the discriminant is 0: ", 1,
         "Zero means one repeated root.", done="A perfect square, one repeated root."),
  ]},
 {"display": "Find the discriminant of \\(x^2 + 2x + 5 = 0\\).",
  "solutions": [-16], "calculator": False, "input_type": "single_value",
  "hint": "b² is small here, 4ac is large.",
  "misconceptions": [mc("added_not_subtracted", [24],
     "The discriminant subtracts: 4 − 20 = −16. Adding the parts gives 24.")],
  "guided_steps": [
     say("Read off a = 1, b = 2, c = 5."),
     box("b² = 2 × 2 = ", 4, "Square b."),
     box("4ac = 4 × 1 × 5 = ", 20, "Multiply 4, a and c."),
     say("Now subtract. The answer will be negative.", phase="substitute"),
     box("b² − 4ac = 4 − 20 = ", -16, "4 minus 20 is negative."),
     box("Number of real roots when the discriminant is negative: ", 0,
         "Negative means none.", done="−16 is negative, so no real roots."),
  ]},
 {"display": "Complete the square: \\(x^2 + 6x\\). Write as \\((x+p)^2 - q\\). What is \\(p\\)?",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "p is half of the x coefficient.",
  "misconceptions": [mc("no_halve", [6],
     "p is half of 6, which is 3. Using the 6 itself skips the halving.")],
  "guided_steps": [
     say("For \\(x^2 + 6x = (x+p)^2 - q\\), find p by halving the 6."),
     box("6 ÷ 2 = ", 3, "Halve the x coefficient."),
     say("Square that to get the q you would subtract.", phase="substitute"),
     box("3² = ", 9, "This is q."),
     box("Check: expand (x+3)² − 9 = x² + 6x + 9 − 9. The x coefficient is ", 6,
         "It must match the original 6x.", done="So p = 3."),
  ]},
 {"display": "Complete the square: \\(x^2 + 6x\\). Write as \\((x+p)^2 - q\\). What is \\(q\\)?",
  "solutions": [9], "calculator": False, "input_type": "single_value",
  "hint": "q is the halved coefficient, squared.",
  "misconceptions": [mc("no_square", [3],
     "q is p squared: 3² = 9. Stopping at p = 3 forgets to square.")],
  "guided_steps": [
     say("For \\(x^2 + 6x = (x+p)^2 - q\\), halve the 6 for p."),
     box("6 ÷ 2 = ", 3, "Halve the x coefficient."),
     say("Now q is p squared.", phase="substitute"),
     box("3² = ", 9, "Square the p you found."),
     box("Check: (x+3)² − 9 = x² + 6x + 9 − 9. The constant left is ", 0,
         "It should return the original with no constant.", done="So the subtracted q is 9."),
  ]},
 {"display": "Discriminant of \\(2x^2 + 3x - 1 = 0\\)?",
  "solutions": [17], "calculator": False, "input_type": "single_value",
  "hint": "Here a = 2 and c = −1, so keep the signs.",
  "misconceptions": [mc("dropped_c_sign", [1],
     "c is −1, so 4ac = −8 and 9 − (−8) = 17. Treating c as +1 gives 9 − 8 = 1.")],
  "guided_steps": [
     say("Read off a = 2, b = 3, c = −1."),
     box("b² = 3 × 3 = ", 9, "Square b."),
     box("4ac = 4 × 2 × (−1) = ", -8, "Keep the minus from c."),
     say("Now subtract 4ac from b². Watch the double negative.", phase="substitute"),
     box("9 − (−8) = ", 17, "Minus a negative adds."),
     box("Number of real roots when the discriminant is positive: ", 2,
         "Positive means two.", done="17 is positive, so two real roots."),
  ]},
 {"display": "How many real roots does \\(x^2 + 5x + 2 = 0\\) have?",
  "solutions": [2], "calculator": False, "input_type": "single_value",
  "hint": "Find the discriminant first, then read its sign.",
  "misconceptions": [mc("gave_discriminant", [17],
     "The discriminant is 17, but the question asks how many roots. Positive means 2.")],
  "guided_steps": [
     say("The number of roots comes from the sign of the discriminant. a = 1, b = 5, c = 2."),
     box("b² = 5 × 5 = ", 25, "Square b."),
     box("4ac = 4 × 1 × 2 = ", 8, "Multiply 4, a and c."),
     say("Subtract, then read the sign.", phase="substitute"),
     box("b² − 4ac = 25 − 8 = ", 17, "25 minus 8."),
     box("17 is positive, so the number of real roots is ", 2,
         "Positive discriminant means two distinct roots.", done="Two real roots."),
  ]},
]

# ---------------- SILVER ----------------
silver = [
 {"display": "Solve \\(x^2 + 4x - 3 = 0\\) using the formula. Give the positive root to 2 d.p.",
  "solutions": [0.65], "calculator": True, "input_type": "single_value",
  "hint": "The positive root uses the + in the formula.",
  "misconceptions": [mc("wrong_sign_root", [-4.65],
     "The positive root uses +√28: (−4 + 5.29) ÷ 2 = 0.65. Using −√ gives −4.65.")],
  "guided_steps": [
     say("a = 1, b = 4, c = −3. Start with the discriminant."),
     box("b² − 4ac = 16 − 4 × 1 × (−3) = 16 − (−12) = ", 28,
         "Minus a negative adds."),
     box("√28 to 2 d.p. = ", 5.29, "Square root on the calculator."),
     say("The positive root uses +√, all over 2a = 2.", phase="substitute"),
     box("(−4 + √28) ÷ 2 = (2 d.p.) ", 0.65, "Use the un-rounded root, divide by 2."),
     box("The other root: (−4 − √28) ÷ 2 = (2 d.p.) ", -4.65,
         "Same working with a minus.", done="Positive root 0.65."),
  ]},
 {"display": "Solve \\(x^2 - 6x + 4 = 0\\). Give the larger root to 2 d.p.",
  "solutions": [5.24], "calculator": True, "input_type": "single_value",
  "hint": "The larger root uses the + in the formula.",
  "misconceptions": [mc("smaller_root", [0.76],
     "The larger root uses +√20: (6 + 4.47) ÷ 2 = 5.24. The smaller root is 0.76.")],
  "guided_steps": [
     say("a = 1, b = −6, c = 4. Note −b = 6."),
     box("b² − 4ac = (−6)² − 4 × 1 × 4 = 36 − 16 = ", 20, "(−6)² is +36."),
     box("√20 to 2 d.p. = ", 4.47, "Square root on the calculator."),
     say("The larger root uses +√, all over 2a = 2, with −b = 6.", phase="substitute"),
     box("(6 + √20) ÷ 2 = (2 d.p.) ", 5.24, "Un-rounded root, divide by 2."),
     box("The smaller root: (6 − √20) ÷ 2 = (2 d.p.) ", 0.76,
         "Same working with a minus.", done="Larger root 5.24."),
  ]},
 {"display": "Complete the square for \\(x^2 + 8x + 5\\). Write as \\((x+p)^2 + q\\). What is \\(q\\)?",
  "solutions": [-11], "calculator": False, "input_type": "single_value",
  "hint": "q is c minus p squared.",
  "misconceptions": [mc("forgot_constant", [-16],
     "q = c − p² = 5 − 16 = −11. Forgetting the +5 leaves −16.")],
  "guided_steps": [
     say("Halve the 8 to get p."),
     box("8 ÷ 2 = ", 4, "Half of 8."),
     box("p² = 4² = ", 16, "Square p."),
     say("Now q = c − p², and c = 5 here.", phase="substitute"),
     box("q = 5 − 16 = ", -11, "5 minus 16."),
     box("Check: (x+4)² − 11 = x² + 8x + 16 − 11. The constant is 16 − 11 = ", 5,
         "It must match the +5 in the original.", done="So q = −11."),
  ]},
 {"display": "Complete the square for \\(x^2 - 10x + 3\\). What is the minimum value of the expression?",
  "solutions": [-22], "calculator": False, "input_type": "single_value",
  "hint": "The least value is c minus p squared.",
  "misconceptions": [mc("forgot_constant", [-25],
     "Minimum = 3 − 25 = −22. Dropping the +3 gives −25.")],
  "guided_steps": [
     say("Halve the −10 for p. Keep the minus."),
     box("−10 ÷ 2 = ", -5, "Half of −10."),
     box("p² = (−5)² = ", 25, "A minus squared is positive."),
     say("The least value is c − p², and c = 3.", phase="substitute"),
     box("3 − 25 = ", -22, "3 minus 25."),
     box("Check: (x−5)² − 22 is smallest when (x−5)² = 0, giving ", -22,
         "The square is least at 0, leaving q.", done="Minimum value −22."),
  ]},
 {"display": "Solve \\(2x^2 + 3x - 4 = 0\\). Give the positive root to 2 d.p.",
  "solutions": [0.85], "calculator": True, "input_type": "single_value",
  "hint": "Here a = 2, so divide by 2a = 4.",
  "misconceptions": [mc("wrong_sign_root", [-2.35],
     "The positive root uses +√41: (−3 + 6.40) ÷ 4 = 0.85. Using −√ gives −2.35.")],
  "guided_steps": [
     say("a = 2, b = 3, c = −4. The divisor is 2a = 4."),
     box("b² − 4ac = 9 − 4 × 2 × (−4) = 9 − (−32) = ", 41, "Minus a negative adds."),
     box("√41 to 2 d.p. = ", 6.40, "Square root on the calculator."),
     say("The positive root uses +√, all over 2a = 4.", phase="substitute"),
     box("(−3 + √41) ÷ 4 = (2 d.p.) ", 0.85, "Divide by 4, not 2."),
     box("The other root: (−3 − √41) ÷ 4 = (2 d.p.) ", -2.35,
         "Same working with a minus.", done="Positive root 0.85."),
  ]},
 {"display": "Solve \\(x^2 + 5x + 2 = 0\\). Give the larger root to 2 d.p.",
  "solutions": [-0.44], "calculator": True, "input_type": "single_value",
  "hint": "Both roots are negative; the larger is closer to zero.",
  "misconceptions": [mc("smaller_root", [-4.56],
     "The larger root uses +√17: (−5 + 4.12) ÷ 2 = −0.44. The smaller root is −4.56.")],
  "guided_steps": [
     say("a = 1, b = 5, c = 2."),
     box("b² − 4ac = 25 − 4 × 1 × 2 = 25 − 8 = ", 17, "25 minus 8."),
     box("√17 to 2 d.p. = ", 4.12, "Square root on the calculator."),
     say("The larger root uses +√, all over 2a = 2, with −b = −5.", phase="substitute"),
     box("(−5 + √17) ÷ 2 = (2 d.p.) ", -0.44, "Un-rounded root, divide by 2."),
     box("The smaller root: (−5 − √17) ÷ 2 = (2 d.p.) ", -4.56,
         "Same working with a minus.", done="Larger root −0.44."),
  ]},
 {"display": "Complete the square for \\(x^2 + 2x - 7\\). Write as \\((x+p)^2 + q\\). What is \\(q\\)?",
  "solutions": [-8], "calculator": False, "input_type": "single_value",
  "hint": "q is c minus p squared.",
  "misconceptions": [mc("forgot_constant", [-1],
     "q = c − p² = −7 − 1 = −8. Dropping the −7 leaves −1.")],
  "guided_steps": [
     say("Halve the 2 to get p."),
     box("2 ÷ 2 = ", 1, "Half of 2."),
     box("p² = 1² = ", 1, "Square p."),
     say("Now q = c − p², and c = −7 here.", phase="substitute"),
     box("q = −7 − 1 = ", -8, "Negative seven minus one."),
     box("Check: (x+1)² − 8 = x² + 2x + 1 − 8. The constant is 1 − 8 = ", -7,
         "It must match the −7 in the original.", done="So q = −8."),
  ]},
]

# ---------------- GOLD ----------------
gold = [
 {"display": "Solve \\(3x^2 - 5x + 1 = 0\\). Give the sum of both solutions as a fraction.",
  "solutions": [5, 3], "calculator": False, "input_type": "fraction",
  "hint": "The two roots of ax²+bx+c=0 always add to −b/a.",
  "misconceptions": [mc("sign_slip", [-5, 3],
     "The sum is −b/a. With b = −5, −b = +5, so the sum is 5/3, positive. A leftover minus gives −5/3.")],
  "guided_steps": [
     say("There is a shortcut: for ax² + bx + c = 0 the two roots always add to −b/a. No solving needed."),
     box("a = ", 3, "The number in front of x²."),
     box("b = ", -5, "The number in front of x, with its sign."),
     say("The sum is −b ÷ a. Work out −b first.", phase="substitute"),
     box("−b = −(−5) = ", 5, "Change the sign of b."),
     box("So the sum is 5 over a. The denominator a = ", 3,
         "Same a as before.", done="Sum of roots = 5/3."),
  ]},
 {"display": "For what value of \\(k\\) does \\(x^2 + 6x + k = 0\\) have exactly one solution?",
  "solutions": [9], "calculator": False, "input_type": "single_value",
  "hint": "One solution means the discriminant is zero.",
  "misconceptions": [mc("no_final_divide", [36],
     "Setting the discriminant to zero gives 4k = 36, so k = 9. Stopping at 4k = 36 leaves k as 36.")],
  "guided_steps": [
     say("One solution means the discriminant is exactly 0. Here a = 1, b = 6, c = k."),
     box("b² = 6 × 6 = ", 36, "Square b."),
     say("The discriminant is 36 − 4k. Set it to 0, so 4k = 36.", phase="substitute"),
     box("4k = ", 36, "Move 4k across: it equals 36."),
     box("k = 36 ÷ 4 = ", 9, "Divide by 4.", done="k = 9 gives a repeated root."),
  ]},
 {"display": "Write \\(2x^2 + 12x + 5\\) in the form \\(a(x+p)^2 + q\\). What is \\(q\\)?",
  "solutions": [-13], "calculator": False, "input_type": "single_value",
  "hint": "Factor the 2 out first, complete the square, then add the 5.",
  "misconceptions": [
     mc("forgot_add_c", [-18],
        "After doubling the −9 you get −18, then add the +5 to reach −13. Stopping at −18 forgets the +5."),
     mc("no_multiply_back", [-4],
        "The −9 sits inside a bracket multiplied by 2, so it becomes −18 before adding 5. Leaving it as −9 gives −4."),
  ],
  "guided_steps": [
     say("Factor the 2 out of the x² and x terms only."),
     box("Inside: 12 ÷ 2 = ", 6, "Divide the x coefficient by the 2."),
     say("Complete the square on x² + 6x: halve the 6."),
     box("6 ÷ 2 = ", 3, "This is p."),
     box("Square it: 3² = ", 9, "The amount subtracted inside."),
     say("Inside becomes (x+3)² − 9. Multiply the −9 back by 2, then add the 5.",
         phase="substitute"),
     box("2 × (−9) = ", -18, "The −9 was inside the bracket times 2."),
     box("q = −18 + 5 = ", -13, "Add the leftover 5.", done="So q = −13."),
  ]},
 {"display": "Show that \\(kx^2 + 8x + (k+6) = 0\\) has no real roots when \\(k = 5\\). Find the discriminant.",
  "solutions": [-156], "calculator": False, "input_type": "single_value",
  "hint": "Put k = 5 into a and c first, then use b² − 4ac.",
  "misconceptions": [mc("forgot_add_six", [-36],
     "c is k+6 = 11, not 5. Using c = 5 gives 64 − 100 = −36 instead of −156.")],
  "guided_steps": [
     say("Put k = 5 into every k. a = k, b = 8, c = k + 6."),
     box("a = k = ", 5, "k is 5."),
     box("c = k + 6 = 5 + 6 = ", 11, "Add 6 to the 5."),
     say("Now the discriminant, b² − 4ac.", phase="substitute"),
     box("b² = 8 × 8 = ", 64, "Square the 8."),
     box("4ac = 4 × 5 × 11 = ", 220, "Multiply 4, 5 and 11."),
     box("b² − 4ac = 64 − 220 = ", -156,
         "64 minus 220 is negative.", done="Negative, so no real roots, as required."),
  ]},
 {"display": "By completing the square, find the coordinates of the turning point of \\(y = x^2 - 4x + 7\\). What is the \\(y\\)-coordinate?",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "The turning point falls straight out of the completed square.",
  "misconceptions": [mc("gave_x_coord", [2],
     "The turning point is (2, 3). The question asks for the y-coordinate, which is 3. Answering 2 gives the x-coordinate.")],
  "guided_steps": [
     say("Complete the square: the turning point pops straight out. Halve the −4."),
     box("−4 ÷ 2 = ", -2, "Half of −4. This is p."),
     box("Square it: (−2)² = ", 4, "A minus squared is positive."),
     say("The y-coordinate is c − p², and c = 7.", phase="substitute"),
     box("y = 7 − 4 = ", 3, "7 minus 4."),
     box("The turning point sits at x = −p = −(−2) = ", 2,
         "The x-coordinate is −p.", done="Turning point (2, 3); the y-coordinate is 3."),
  ]},
]

problem_bank = {
    "bronze_description": "Read off a, b, c and work out the discriminant b² − 4ac, or halve-and-square to start completing the square.",
    "silver_description": "Put a, b, c into the quadratic formula and evaluate to 2 d.p., or complete the square to find q and the minimum value.",
    "gold_description": "Harder quadratics: a leading coefficient above 1, a discriminant condition on an unknown, turning points and the sum of the roots.",
    "bronze": bronze, "silver": silver, "gold": gold,
}

practice_data = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "problem_bank": problem_bank,
    "related_videos": live["related_videos"],
    "worked_examples": live["worked_examples"],
    "tier_guides": tier_guides,
    "guided": {"opener": opener, "teach": teach},
}

with io.open('lesson_maths-eduqas_algebra-L08.json', 'w', encoding='utf-8') as f:
    json.dump(practice_data, f, ensure_ascii=False, indent=1)
print("written lesson_maths-eduqas_algebra-L08.json")
