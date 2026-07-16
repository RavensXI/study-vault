# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_live_L06.json", encoding="utf-8"))
pb = pd["problem_bank"]

def b(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def s(say):
    return {"say": say}

bronze = pb["bronze"]

bronze[0]["hint"] = "Gradient = change in y divided by change in x (rise over run)."
bronze[0]["guided_steps"] = [
    b("Rise (top y minus bottom y): 13 − 5 = ", 8, "13 take away 5."),
    b("Run (right x minus left x): 6 − 2 = ", 4, "6 take away 2."),
    b("Gradient = rise ÷ run = 8 ÷ 4 = ", 2, "8 shared into 4.", phase="substitute",
      say="Now put the two together."),
    b("Check: a gradient of 2 over a run of 4 should climb 2 × 4 = ", 8,
      "Multiply the gradient by the run.", done="That matches the rise of 8, so the gradient is 2."),
]

bronze[1]["hint"] = "Gradient = rise ÷ run; the line falls, so expect a negative answer."
bronze[1]["guided_steps"] = [
    b("Rise (top y minus bottom y): 0 − 8 = ", -8, "0 take away 8 is negative."),
    b("Run: 4 − 0 = ", 4, "4 take away 0."),
    b("Gradient = −8 ÷ 4 = ", -2, "A negative divided by a positive stays negative.",
      phase="substitute", say="Divide, keeping the minus sign."),
    b("Check: −2 × 4 = ", -8, "Multiply gradient by run.",
      done="That matches the rise of −8, so the gradient is −2."),
]

bronze[2]["hint"] = "Add 3 each time: find x1, then x2, then x3."
bronze[2]["guided_steps"] = [
    b("x₁ = 2 + 3 = ", 5, "Start value 2, add 3."),
    b("x₂ = 5 + 3 = ", 8, "Feed x₁ back in, add 3.", phase="substitute",
      say="Feed each answer back into the same rule."),
    b("x₃ = 8 + 3 = ", 11, "Feed x₂ back in, add 3.", done="Three steps of +3 done."),
    b("Check: from the start, 3 jumps of 3 is 2 + 9 = ", 11,
      "Three lots of 3 is 9, added to the start.", done="Same answer, so x₃ = 11."),
]

bronze[3]["hint"] = "Apply the rule twice: x1 first, then x2."
bronze[3]["guided_steps"] = [
    b("x₁ = 2 × 3 − 1 = ", 5, "Double 3, then take 1."),
    b("x₂ = 2 × 5 − 1 = ", 9, "Feed x₁ back in: double 5, take 1.", phase="substitute",
      say="Now feed x₁ back into the same rule."),
    b("Check: reverse the rule, (9 + 1) ÷ 2 = ", 5,
      "Undo the rule: add 1, then halve.", done="That gives back x₁ = 5, so x₂ = 9 is right."),
]

bronze[4] = {
    "display": "A tangent passes through \\((1, 2)\\) and \\((5, 22)\\). What is the rate of change?",
    "solutions": [5],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Rate of change is the gradient: change in y divided by change in x.",
    "misconceptions": [
        {"check": "common", "expect": 0.2,
         "message": "Rate of change = rise ÷ run = (22 − 2) ÷ (5 − 1) = 20 ÷ 4 = 5. Dividing run by rise instead gives 0.2, which is upside down.",
         "pattern": "inverted_gradient"}
    ],
    "guided_steps": [
        b("Rise: 22 − 2 = ", 20, "22 take away 2."),
        b("Run: 5 − 1 = ", 4, "5 take away 1."),
        b("Rate of change = rise ÷ run = 20 ÷ 4 = ", 5, "20 shared into 4.",
          phase="substitute", say="Divide the rise by the run."),
        b("Check: 5 × 4 = ", 20, "Multiply gradient by run.",
          done="That matches the rise of 20, so the rate of change is 5."),
    ],
}

bronze[5] = {
    "display": "Use \\(x_{n+1} = \\frac{x_n}{2} + 4\\) with \\(x_0 = 6\\). Find \\(x_1\\).",
    "solutions": [7],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Halve the previous term, then add 4.",
    "misconceptions": [
        {"check": "common", "expect": 10,
         "message": "Halve first: 6 ÷ 2 = 3, then add 4 to get 7. Adding 4 to 6 without halving gives 10.",
         "pattern": "forgot_step"}
    ],
    "guided_steps": [
        b("Halve the start value: 6 ÷ 2 = ", 3, "6 shared into 2."),
        b("Then add 4: 3 + 4 = ", 7, "Add 4 to the half.", phase="substitute",
          say="The rule says halve, then add 4."),
        b("Check: 6 ÷ 2 + 4 = ", 7, "Halve, then add 4, in one line.",
          done="Yes, x₁ = 7."),
    ],
}

bronze[6]["hint"] = "Gradient = rise ÷ run between the two points."
bronze[6]["guided_steps"] = [
    b("Rise: 10 − 1 = ", 9, "10 take away 1."),
    b("Run: 5 − 2 = ", 3, "5 take away 2."),
    b("Gradient = 9 ÷ 3 = ", 3, "9 shared into 3.", phase="substitute",
      say="Divide the rise by the run."),
    b("Check: 3 × 3 = ", 9, "Multiply gradient by run.",
      done="That matches the rise of 9, so the gradient is 3."),
]

bronze[7]["hint"] = "Square the previous term first, then subtract 5."
bronze[7]["misconceptions"] = [
    {"check": "common", "expect": 9,
     "message": "Square first: 3² = 9, then subtract 5 to get 4. Stopping at 9 forgets the − 5.",
     "pattern": "forgot_step"}
]
bronze[7]["guided_steps"] = [
    b("Square the start value: 3² = ", 9, "3 times 3."),
    b("Then subtract 5: 9 − 5 = ", 4, "Take 5 from the square.", phase="substitute",
      say="The rule is: square, then take away 5."),
    b("Check: 3 × 3 − 5 = ", 4, "Square, then subtract, in one line.",
      done="So x₁ = 4."),
]

silver = pb["silver"]

silver[0]["hint"] = "Work out x1 first (keep the full value), then use it to find x2."
silver[0]["guided_steps"] = [
    b("First iteration, inside the root: 3 × 2 + 7 = ", 13, "3 × 2 = 6, then + 7."),
    s("So \\(x_1 = \\sqrt{13} = 3.6056\\). Keep this full value, do not round yet."),
    b("Second iteration: 3 × 3.6056 + 7 gives 17.8168 under the root, so x₂ = √17.8168 to 2 d.p. = ",
      4.22, "Square root of 17.8168, rounded to 2 d.p.", phase="substitute"),
    b("Check: 4.22² to 2 d.p. = ", 17.81, "4.22 × 4.22.",
      done="17.81 is essentially the 17.82 under the root, so x₂ = 4.22 is right."),
]

silver[1]["hint"] = "Speed is the gradient of the tangent: rise ÷ run."
silver[1]["guided_steps"] = [
    b("Rise (distance change): 11 − 3 = ", 8, "11 take away 3."),
    b("Run (time change): 6 − 2 = ", 4, "6 take away 2."),
    b("Speed = gradient = 8 ÷ 4 = ", 2, "8 shared into 4.", phase="substitute",
      say="Speed is the steepness of the distance-time line."),
    b("Check: 2 × 4 = ", 8, "Speed times time gives distance.",
      done="That matches the rise of 8, so the speed is 2 m/s."),
]

silver[2]["hint"] = "Cube the term, add 1, divide by 4. Do it three times."
silver[2]["misconceptions"] = [
    {"check": "common", "expect": 0.5,
     "message": "x₁ = (1 + 1) ÷ 4 = 0.5. x₂ = (0.125 + 1) ÷ 4 = 0.281. x₃ = (0.022 + 1) ÷ 4 ≈ 0.256. Stopping at x₁ gives 0.5.",
     "pattern": "forgot_step"}
]
silver[2]["guided_steps"] = [
    b("x₁ = (1³ + 1) ÷ 4 = 2 ÷ 4 = ", 0.5, "1 cubed is 1, plus 1 is 2, over 4."),
    b("x₂ = (0.5³ + 1) ÷ 4 = (0.125 + 1) ÷ 4 = ", 0.28125,
      "0.5³ = 0.125, add 1 to get 1.125, then divide by 4.", phase="substitute",
      say="Feed x₁ back in to reach x₂."),
    b("x₃ = (0.28125³ + 1) ÷ 4, to 3 d.p. = ", 0.256,
      "0.28125³ ≈ 0.0222, add 1, divide by 4.",
      done="The terms are settling near 0.256."),
]

silver[3]["hint"] = "The gradient of a velocity-time graph shows how fast the velocity is changing."

silver[4]["hint"] = "Add 1 to the term for the denominator, then divide 10 by it. Twice."
silver[4]["guided_steps"] = [
    b("x₁: denominator is 3 + 1 = 4, so 10 ÷ 4 = ", 2.5, "Bottom is 3 + 1 = 4, then 10 ÷ 4."),
    b("x₂: denominator is 2.5 + 1 = 3.5, so 10 ÷ 3.5 to 2 d.p. = ", 2.86,
      "10 ÷ 3.5 = 2.857..., round to 2 d.p.", phase="substitute",
      say="Feed x₁ back in to reach x₂."),
    b("Check: 2.86 × 3.5 = ", 10.01, "Should come back to about 10.",
      done="≈ 10, so x₂ = 2.86 is right."),
]

silver[5]["hint"] = "Gradient = rise ÷ run; subtracting −1 adds 1."
silver[5]["guided_steps"] = [
    b("Rise: 11 − (−1) = ", 12, "Subtracting −1 is the same as adding 1: 11 + 1."),
    b("Run: 4 − 0 = ", 4, "4 take away 0."),
    b("Gradient = 12 ÷ 4 = ", 3, "12 shared into 4.", phase="substitute",
      say="Divide the rise by the run."),
    b("Check: 3 × 4 = ", 12, "Multiply gradient by run.",
      done="That matches the rise of 12, so the gradient is 3."),
]

silver[6]["hint"] = "Work out 8x − 3 first, then take the cube root."
silver[6]["guided_steps"] = [
    b("Inside the cube root: 8 × 1 − 3 = ", 5, "8 × 1 = 8, then − 3."),
    b("x₁ = ∛5, to 3 d.p. = ", 1.71, "Cube root of 5 is about 1.710.",
      phase="substitute", say="Now take the cube root of that."),
    b("Check: 1.71³ to 2 d.p. = ", 5.0, "1.71 × 1.71 × 1.71.",
      done="≈ 5, matching the number under the cube root, so x₁ = 1.710."),
]

gold = pb["gold"]

gold[0]["hint"] = "Work the numerator and denominator separately, then divide. Repeat to x3."
gold[0]["misconceptions"] = [
    {"check": "equals_1.119", "expect": 1.119,
     "message": "It looks like the 2 in the numerator was left out. The top is \\(2x_n^3 + 5\\), not \\(x_n^3 + 5\\); redo each substitution with the full formula.",
     "pattern": "missing_numerator_coefficient"},
    {"check": "equals_1.750", "expect": 1.75,
     "message": "It looks like only one substitution was made. \\(x_3\\) needs the formula applied three times, feeding each answer back in.",
     "pattern": "single_substitution_only"},
]
gold[0]["guided_steps"] = [
    b("x₁ numerator: 2 × 2³ + 5 = 2 × 8 + 5 = ", 21, "2³ = 8, doubled is 16, plus 5."),
    b("x₁ denominator: 3 × 2² = 3 × 4 = ", 12, "2² = 4, times 3."),
    b("x₁ = 21 ÷ 12 = ", 1.75, "21 ÷ 12 = 1.75."),
    b("x₂ = (2 × 1.75³ + 5) ÷ (3 × 1.75²), to 4 d.p. = ", 1.7109,
      "1.75³ = 5.359, numerator 15.719, denominator 9.188.", phase="substitute",
      say="Feed x₁ back into the same formula for x₂."),
    b("x₃ = (2 × 1.7109³ + 5) ÷ (3 × 1.7109²), to 3 d.p. = ", 1.71,
      "The terms are settling; this is the cube root of 5, about 1.710."),
    b("Check: 1.71³ to 2 d.p. = ", 5.0, "1.71 × 1.71 × 1.71.",
      done="≈ 5, so x₃ solves x³ = 5. Answer 1.710."),
]

gold[1]["hint"] = "Substitute x = 2 into x³ − 5x + 1, then check the sign changes by x = 3."
gold[1]["misconceptions"] = [
    {"check": "common", "expect": -2,
     "message": "f(2) = 2³ − 5(2) + 1 = 8 − 10 + 1 = −1. Getting −2 misses the + 1 at the end.",
     "pattern": "forgot_constant"}
]
gold[1]["guided_steps"] = [
    b("First 2³ = ", 8, "2 × 2 × 2."),
    b("and 5 × 2 = ", 10, "Five twos."),
    b("f(2) = 8 − 10 + 1 = ", -1, "8 − 10 = −2, then + 1.", phase="substitute",
      say="Put the pieces together for f(2)."),
    b("Now f(3): 3³ − 5 × 3 + 1 = 27 − 15 + 1 = ", 13, "27 − 15 = 12, then + 1.",
      done="f(3) = 13, positive."),
    b("f(2) is negative and f(3) is positive, so a root lies between. The value asked for, f(2), is ",
      -1, "Read off f(2) from earlier.",
      done="Sign change from − to +, so a root sits between x = 2 and x = 3."),
]

gold[2]["hint"] = "Heights are 0, 1, 4, 9, 16; use ½ × width × (ends + 2 × middles)."
gold[2]["misconceptions"] = [
    {"check": "common", "expect": 15,
     "message": "Heights: 0, 1, 4, 9, 16. Area ≈ ½ × 1 × [(0 + 16) + 2(1 + 4 + 9)] = ½ × 44 = 22. Forgetting to double the middle heights gives 15.",
     "pattern": "forgot_double_middles"}
]
gold[2]["guided_steps"] = [
    b("Heights y = x² at x = 0, 1, 2, 3, 4. The one at x = 2 is 2² = ", 4, "2 squared."),
    b("and the one at x = 3 is 3² = ", 9, "3 squared."),
    b("Add the two end heights: 0 + 16 = ", 16, "First height plus last height.",
      phase="substitute", say="Now apply the trapezium rule."),
    b("Double the middle heights: 2 × (1 + 4 + 9) = ", 28, "1 + 4 + 9 = 14, then × 2."),
    b("Area = ½ × 1 × (16 + 28) = ", 22, "16 + 28 = 44, then halve.",
      done="The trapezium-rule estimate is 22 square units."),
]

gold[3]["hint"] = "Square the term, take its reciprocal, subtract from 5. Repeat to x3."
gold[3]["misconceptions"] = [
    {"check": "common", "expect": None,
     "message": "x₁ = 5 − 1/2² = 4.75. x₂ = 5 − 1/4.75² = 4.9557. x₃ = 5 − 1/4.9557² ≈ 4.9593.",
     "pattern": "wrong_formula"}
]
gold[3]["guided_steps"] = [
    b("x₁ = 5 − 1 ÷ 2² = 5 − 1 ÷ 4 = 5 − 0.25 = ", 4.75, "2² = 4, and 1 ÷ 4 = 0.25."),
    b("For x₂, the denominator 4.75² = ", 22.5625, "4.75 × 4.75."),
    b("x₂ = 5 − 1 ÷ 22.5625, to 4 d.p. = ", 4.9557,
      "1 ÷ 22.5625 = 0.0443, then 5 − 0.0443.", phase="substitute",
      say="Feed x₁ back in for x₂."),
    b("x₃ = 5 − 1 ÷ 4.9557², to 4 d.p. = ", 4.9593,
      "4.9557² = 24.559, 1 ÷ 24.559 = 0.0407, then 5 − 0.0407."),
    b("Check: 5 − 4.9593 = ", 0.0407, "The gap below 5.",
      done="That equals 1 ÷ x₂², confirming x₃ = 4.9593."),
]

gold[4]["hint"] = "Square both sides, rearrange to a quadratic, factorise, take the positive root."
gold[4]["misconceptions"] = [
    {"check": "common", "expect": -3,
     "message": "x² = 2x + 15 gives x² − 2x − 15 = 0 = (x − 5)(x + 3). The roots are 5 and −3; the positive one is 5.",
     "pattern": "wrong_root_sign"}
]
gold[4]["guided_steps"] = [
    s("When the iteration settles, x stops changing, so \\(x = \\sqrt{2x + 15}\\). Square both sides: \\(x^2 = 2x + 15\\), which rearranges to \\(x^2 - 2x - 15 = 0\\)."),
    b("We need two numbers that multiply to −15 and add to −2. One is −5, the other is ", 3,
      "−5 × 3 = −15 and −5 + 3 = −2."),
    b("So (x − 5)(x + 3) = 0. The negative root is x = ", -3,
      "x + 3 = 0 gives x = −3.", phase="substitute",
      say="Set each bracket to zero to find the roots."),
    b("The question wants the positive root, so x = ", 5, "5 is positive, −3 is not."),
    b("Check: put x = 5 into 2x + 15: 2 × 5 + 15 = ", 25,
      "2 × 5 = 10, plus 15.", done="√25 = 5 = x, so it balances and the positive root is 5."),
]

pb["bronze_description"] = "Read a rate of change (gradient) from two points, or run a short iteration by hand."
pb["silver_description"] = "Iterate with a calculator to x2 or x3, or read a rate of change from a real-life graph."
pb["gold_description"] = "Newton-Raphson iteration, sign-change root location, the trapezium rule, and forming equations."

pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: rates of change and simple iteration",
        "steps": [
            "<strong>Rate of change</strong> = gradient of the line: (change in y) ÷ (change in x), or rise ÷ run.",
            "<strong>Iteration</strong>: start at \\(x_0\\), put it in the formula for \\(x_1\\), then feed \\(x_1\\) back in for \\(x_2\\), and so on.",
            "Work one step at a time and write each term down. Watch the sign when a point or term is negative.",
        ],
        "example": {
            "question": "A tangent passes through \\((1, 3)\\) and \\((5, 15)\\). Find the gradient.",
            "steps": [
                {"label": "Rise", "content": "15 − 3 = 12"},
                {"label": "Run", "content": "5 − 1 = 4"},
                {"label": "Check", "content": "12 ÷ 4 divides exactly, since 4 × 3 = 12."},
                {"label": "Answer", "content": "Gradient = 12 ÷ 4 = 3", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: calculator iteration and real-life gradients",
        "steps": [
            "Keep the <strong>full calculator value</strong> for each term. Round only the final term, to the decimal places asked for.",
            "For \\(x_2\\) or \\(x_3\\), apply the formula that many times: each answer becomes the next input.",
            "On a distance-time graph the gradient is a <strong>speed</strong>; on a velocity-time graph it is an <strong>acceleration</strong>.",
        ],
        "example": {
            "question": "Use \\(x_{n+1} = \\sqrt{4x_n + 5}\\) with \\(x_0 = 1\\). Find \\(x_2\\) to 2 d.p.",
            "steps": [
                {"label": "x₁", "content": "\\(\\sqrt{4(1) + 5} = \\sqrt{9} = 3\\)"},
                {"label": "Inside for x₂", "content": "4 × 3 + 5 = 17"},
                {"label": "Check", "content": "√17 sits between √16 = 4 and √25 = 5, so expect about 4.1."},
                {"label": "Answer", "content": "\\(x_2 = \\sqrt{17} = 4.12\\) (2 d.p.)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: Newton-Raphson, sign change and trapezium rule",
        "steps": [
            "A <strong>Newton-Raphson</strong> formula is a fraction such as \\(\\frac{2x_n^3 + a}{3x_n^2}\\): work numerator and denominator separately, then divide.",
            "A <strong>sign change</strong> in \\(f(x)\\) between two x-values shows a root lies between them.",
            "<strong>Trapezium rule</strong>: ½ × strip width × (first height + last height + 2 × the middle heights).",
        ],
        "example": {
            "question": "Use \\(x_{n+1} = \\frac{2x_n^3 + 7}{3x_n^2}\\) with \\(x_0 = 2\\). Find \\(x_2\\) to 3 d.p.",
            "steps": [
                {"label": "Numerator", "content": "2 × 2³ + 7 = 16 + 7 = 23"},
                {"label": "Denominator", "content": "3 × 2² = 12"},
                {"label": "Check", "content": "23 ÷ 12 ≈ 1.92, close to ∛7 ≈ 1.91, so on track."},
                {"label": "Answer", "content": "\\(x_1 = 1.917\\); repeat once for \\(x_2 = 1.913\\) (3 d.p.)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

pd["guided"] = {
    "opener": {
        "steps": [
            s("A phone game gives you tokens. You start with 100. Each round the app halves your tokens, then hands you 30 bonus tokens. No algebra, just do the two sums."),
            b("After round 1 you have ", 80, "Halve 100 to get 50, then add the 30 bonus.", post=" tokens"),
            s("Now take that new total, 80, through the <strong>same</strong> rule again."),
            b("After round 2 you have ", 70, "Halve 80 to get 40, then add 30.", post=" tokens"),
            s("Each new total was the old total put through one rule: halve, then add 30. Feeding an answer back into the same rule, over and over, is called <strong>iteration</strong>. In algebra we write the rule as \\(x_{n+1} = \\frac{x_n}{2} + 30\\), with \\(x_0 = 100\\) the starting pile. The other half of this lesson reads a <strong>rate of change</strong> straight off a graph: the steepness (gradient) of the line, rise ÷ run."),
        ]
    },
    "teach": {
        "bronze": {
            "display": "A tangent to a curve passes through \\((1, 2)\\) and \\((4, 11)\\). Find the rate of change.",
            "steps": [
                s("Rate of change is the steepness of the line: how much y climbs for the x you move across. It is rise ÷ run."),
                b("Rise (top y minus bottom y): 11 − 2 = ", 9, "11 take away 2."),
                b("Run (right x minus left x): 4 − 1 = ", 3, "4 take away 1."),
                b("Rate of change = rise ÷ run = 9 ÷ 3 = ", 3, "9 shared into 3."),
                b("Check: a gradient of 3 over a run of 3 should climb 3 × 3 = ", 9,
                  "Multiply gradient by run.", done="That matches the rise of 9. Gone. That was the whole point: rise over run."),
            ],
        },
        "silver": {
            "display": "Use \\(x_{n+1} = \\frac{10}{x_n + 2}\\) with \\(x_0 = 2\\). Find \\(x_2\\) to 2 d.p.",
            "steps": [
                s("The new move here: iterate with a calculator, keeping full precision, and only round the last term."),
                b("x₁ denominator: 2 + 2 = ", 4, "Add 2 to the start value."),
                b("x₁ = 10 ÷ 4 = ", 2.5, "10 shared into 4."),
                b("x₂ denominator: 2.5 + 2 = ", 4.5, "Add 2 to x₁."),
                b("x₂ = 10 ÷ 4.5, to 2 d.p. = ", 2.22, "10 ÷ 4.5 = 2.222..., round to 2 d.p."),
                b("Check: 2.22 × 4.5 = ", 9.99, "Should come back to about 10.",
                  done="≈ 10, so x₂ = 2.22. That was the whole point: feed each answer back in."),
            ],
        },
        "gold": {
            "display": "Use \\(x_{n+1} = \\frac{2x_n^3 + 20}{3x_n^2}\\) with \\(x_0 = 3\\). Find \\(x_2\\) to 3 d.p.",
            "steps": [
                s("The new move: a Newton-Raphson formula. Work the numerator and denominator separately, then divide, and repeat."),
                b("x₁ numerator: 2 × 3³ + 20 = 2 × 27 + 20 = ", 74, "3³ = 27, doubled is 54, plus 20."),
                b("x₁ denominator: 3 × 3² = 3 × 9 = ", 27, "3² = 9, times 3."),
                b("x₁ = 74 ÷ 27, to 4 d.p. = ", 2.7407, "74 ÷ 27 = 2.7407..."),
                b("x₂ = (2 × 2.7407³ + 20) ÷ (3 × 2.7407²), to 3 d.p. = ", 2.715,
                  "Numerator ≈ 61.18, denominator ≈ 22.53."),
                b("Check: 2.715³ to 2 d.p. = ", 20.01, "2.715 × 2.715 × 2.715.",
                  done="≈ 20, so x₂ solves x³ = 20. Gone. That was the whole point of the Newton-Raphson step."),
            ],
        },
    },
}

# Preserved worked_examples carried an em dash in a label; the style gate forbids it.
for _we in pd.get("worked_examples", []):
    for _st in _we.get("steps", []):
        if isinstance(_st.get("label"), str) and "—" in _st["label"]:
            _st["label"] = _st["label"].replace(" — ", ": ").replace("—", ": ")

pd["method_card"]["title"] = "Rates of Change & Iteration (reference)"
pd["method_card"]["steps"] = [
    "Rate of change = gradient of the tangent: rise ÷ run between two points on it.",
    "Iteration: start at \\(x_0\\), apply \\(x_{n+1} = f(x_n)\\) repeatedly, feeding each answer back in.",
    "Keep full precision between steps; round only the final term to the decimal places asked.",
    "Trapezium rule for area: ½ × width × (first + last + 2 × middle heights).",
]
pd["method_card"]["content"] = "<p>The <strong>rate of change</strong> at a point is the gradient of the tangent there: pick two points on the tangent and compute rise ÷ run.</p><p>An <strong>iterative process</strong> uses \\(x_{n+1} = f(x_n)\\). Start at \\(x_0\\), substitute to get \\(x_1\\), then feed that back in for \\(x_2\\), and so on until the values settle. Keep the full calculator value between steps and round only at the end.</p><p>A <strong>sign change</strong> in \\(f(x)\\) locates a root; the <strong>trapezium rule</strong> estimates the area under a curve.</p>"

json.dump(pd, io.open("lesson_ratio-proportion-L06.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written OK")
