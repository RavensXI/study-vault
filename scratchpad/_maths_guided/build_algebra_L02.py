# -*- coding: utf-8 -*-
"""Build guided-learning practice_data for algebra-L02 (Expanding Brackets)."""
import json, io

SRC = "_live_algebra_L02.json"
OUT = "lesson_algebra-L02.json"

pd = json.load(io.open(SRC, encoding="utf-8"))

# ---------------------------------------------------------------------------
# Helper to build a misconception entry
def mc(pattern, expect, message, note=None):
    d = {"check": pattern, "expect": expect, "message": message, "pattern": pattern}
    if note:
        d["note"] = note
    return d

# ===========================================================================
# 1 + 2. Repair bank problems: hints + rebuilt misconceptions + G0 replace + B5 display
# ===========================================================================
pb = pd["problem_bank"]

# ---- BRONZE (single brackets) --------------------------------------------
bronze = pb["bronze"]

# B0  3(x+4) = 3x+12   opts: 0:3x+12*, 1:3x+4, 2:x+12, 3:3x+7
bronze[0]["hint"] = "Multiply the 3 by both the x and the 4."
bronze[0]["misconceptions"] = [
    mc("missed_term", 1,
       "You only multiplied one term. The 3 outside must multiply every term inside the bracket, so \\(3(x + 4) = 3x + 12\\)."),
    mc("added_not_multiplied", 3,
       "The 3 must be multiplied by the 4, not added to it: \\(3 \\times 4 = 12\\), not \\(3 + 4 = 7\\)."),
]

# B1  5(2x-1) = 10x-5  opts: 0:10x-1, 1:7x-5, 2:10x-5*, 3:10x+5
bronze[1]["hint"] = "Multiply the 5 by 2x and by minus 1, keeping the minus."
bronze[1]["misconceptions"] = [
    mc("missed_term", 0,
       "You only multiplied the first term. The 5 must also multiply the \\(-1\\): \\(5 \\times (-1) = -5\\)."),
    mc("sign_error", 3,
       "Watch the sign: \\(5 \\times (-1) = -5\\), not \\(+5\\). A positive times a negative is negative."),
    mc("added_not_multiplied", 1,
       "Multiply the coefficients: \\(5 \\times 2x = 10x\\), not \\(5 + 2 = 7\\)."),
]

# B2  2(3x+7) = 6x+14  opts: 0:6x+14*, 1:6x+7, 2:5x+14, 3:6x+9
bronze[2]["hint"] = "Multiply the 2 by 3x and by 7."
bronze[2]["misconceptions"] = [
    mc("missed_term", 1,
       "You only multiplied the first term. The 2 must also multiply the 7: \\(2 \\times 7 = 14\\)."),
    mc("added_not_multiplied", 3,
       "Multiply the 2 by the 7, do not add: \\(2 \\times 7 = 14\\), not \\(2 + 7 = 9\\)."),
]

# B3  -3(x-4) = -3x+12  opts: 0:-3x-12, 1:-3x+12*, 2:3x-12, 3:-3x-4
bronze[3]["hint"] = "Multiply minus 3 by both terms; remember minus 3 times minus 4 is positive."
bronze[3]["misconceptions"] = [
    mc("missed_term", 3,
       "You only multiplied the first term. The \\(-3\\) must also multiply the \\(-4\\): \\(-3 \\times (-4) = +12\\)."),
    mc("sign_error", 0,
       "Two negatives multiply to a positive: \\(-3 \\times (-4) = +12\\), not \\(-12\\)."),
]

# B4  4(2x+3) = 8x+12  opts: 0:8x+12*, 1:8x+3, 2:6x+12, 3:8x+7
bronze[4]["hint"] = "Multiply the 4 by 2x and by 3."
bronze[4]["misconceptions"] = [
    mc("missed_term", 1,
       "You only multiplied the first term. The 4 must also multiply the 3: \\(4 \\times 3 = 12\\)."),
    mc("added_not_multiplied", 3,
       "Multiply the 4 by the 3, do not add: \\(4 \\times 3 = 12\\), not \\(4 + 3 = 7\\)."),
]

# B5  x(x+5) = x^2+5x  opts: 0:x^2+5, 1:x^2+5x*, 2:x+5x, 3:6x  (display gets "and simplify")
bronze[5]["display"] = "Expand and simplify \\(x(x + 5)\\)"
bronze[5]["hint"] = "Multiply x by x to get x squared, then x by 5."
bronze[5]["misconceptions"] = [
    mc("missed_term", 0,
       "You only multiplied the first term. The \\(x\\) must also multiply the 5: \\(x \\times 5 = 5x\\)."),
    mc("forgot_squared", 2,
       "When you multiply \\(x\\) by \\(x\\) you get \\(x^2\\), not \\(x\\). Multiplying is not the same as adding."),
]

# B6  2x(3x-4) = 6x^2-8x  opts: 0:6x^2-8x*, 1:6x-8x, 2:6x^2-4, 3:5x^2-8x
bronze[6]["hint"] = "Multiply 2x by 3x and by minus 4; 2x times 3x is 6x squared."
bronze[6]["misconceptions"] = [
    mc("missed_term", 2,
       "You only multiplied the first term. The \\(2x\\) must also multiply the \\(-4\\): \\(2x \\times (-4) = -8x\\)."),
    mc("forgot_squared", 1,
       "When you multiply \\(2x\\) by \\(3x\\) you get \\(6x^2\\), not \\(6x\\). Multiplying two \\(x\\) terms gives \\(x^2\\)."),
    mc("added_not_multiplied", 3,
       "Multiply the coefficients: \\(2x \\times 3x = 6x^2\\), not \\(5x^2\\). Do not add 2 and 3."),
]

# B7  -2(5x+1) = -10x-2  opts: 0:-10x+2, 1:-10x-2*, 2:10x-2, 3:-7x-2
bronze[7]["hint"] = "Multiply minus 2 by 5x and by 1, keeping both signs negative."
bronze[7]["misconceptions"] = [
    mc("sign_error", 0,
       "Watch the sign: \\(-2 \\times (+1) = -2\\), not \\(+2\\). A negative times a positive is negative."),
    mc("added_not_multiplied", 3,
       "Multiply the coefficients: \\(-2 \\times 5x = -10x\\), not \\(-7x\\). Do not add \\(-2\\) and 5."),
]

# ---- SILVER (double brackets) --------------------------------------------
silver = pb["silver"]

# S0  (x+2)(x+5) = x^2+7x+10  opts: 0:*, 1:x^2+7x+7, 2:x^2+10x+7, 3:2x+7
silver[0]["hint"] = "Four products: multiply out, then add the two x terms."
silver[0]["misconceptions"] = [
    mc("constant_error", 1,
       "The last term is the two constants multiplied: \\(2 \\times 5 = 10\\), not \\(2 + 5 = 7\\)."),
    mc("role_swap", 2,
       "You have swapped the roles. The middle term is \\(2x + 5x = 7x\\); the last term is \\(2 \\times 5 = 10\\)."),
]

# S1  (x+3)(x-4) = x^2-x-12  opts: 0:x^2+x-12, 1:x^2-x+12, 2:*, 3:x^2-7x-12
silver[1]["hint"] = "Four products; the last term is 3 times minus 4."
silver[1]["misconceptions"] = [
    mc("middle_term", 0,
       "The cross-products are \\(+3x\\) and \\(-4x\\), which add to \\(-x\\), not \\(+x\\)."),
    mc("sign_error", 1,
       "The last terms are \\(+3\\) and \\(-4\\), so \\(3 \\times (-4) = -12\\), not \\(+12\\)."),
    mc("middle_term", 3,
       "Only one cross-product is negative: \\(3x + (-4x) = -x\\), not \\(-7x\\)."),
]

# S2  (x-1)(x+8) = x^2+7x-8  opts: 0:*, 1:x^2-7x-8, 2:x^2+9x-8, 3:x^2+7x+8
silver[2]["hint"] = "Four products; watch the minus on the 1."
silver[2]["misconceptions"] = [
    mc("middle_term", 2,
       "The inner product is \\((-1) \\times x = -x\\), so the middle is \\(8x + (-x) = 7x\\), not \\(9x\\)."),
    mc("sign_error", 3,
       "The last terms are \\(-1\\) and \\(+8\\), so \\((-1) \\times 8 = -8\\), not \\(+8\\)."),
    mc("middle_term", 1,
       "The middle is \\(8x + (-x) = +7x\\), not \\(-7x\\). The larger cross-product \\(8x\\) is positive."),
]

# S3  (x-3)(x-6) = x^2-9x+18  opts: 0:x^2-9x-18, 1:x^2+9x+18, 2:*, 3:x^2-3x+18
silver[3]["hint"] = "Two negatives multiply to a positive last term."
silver[3]["misconceptions"] = [
    mc("sign_error", 0,
       "Two negatives multiply to a positive: \\((-3) \\times (-6) = +18\\), not \\(-18\\)."),
    mc("missed_term", 3,
       "You used only one cross-product. Both \\(-3x\\) and \\(-6x\\) count, giving \\(-9x\\), not \\(-3x\\)."),
    mc("middle_term", 1,
       "Both cross-products are negative here: \\(-6x + (-3x) = -9x\\), not \\(+9x\\)."),
]

# S4  (x+4)(x+4) = x^2+8x+16  opts: 0:*, 1:x^2+4x+16, 2:x^2+8x+8, 3:2x+8
silver[4]["hint"] = "Both cross terms are 4x, so the middle is 8x."
silver[4]["misconceptions"] = [
    mc("missed_term", 1,
       "There are two identical cross-products, \\(4x\\) and \\(4x\\). Add both to get \\(8x\\), not \\(4x\\)."),
    mc("constant_error", 2,
       "The last term is \\(4 \\times 4 = 16\\), not \\(4 + 4 = 8\\)."),
]

# S5  (x-2)(x+9) = x^2+7x-18  opts: 0:x^2-7x-18, 1:x^2+11x-18, 2:*, 3:x^2+7x+18
silver[5]["hint"] = "Four products; the last term is minus 2 times 9."
silver[5]["misconceptions"] = [
    mc("middle_term", 1,
       "The inner product is \\((-2) \\times x = -2x\\), so \\(9x + (-2x) = 7x\\), not \\(11x\\)."),
    mc("sign_error", 3,
       "The last terms are \\(-2\\) and \\(+9\\), so \\((-2) \\times 9 = -18\\), not \\(+18\\)."),
    mc("middle_term", 0,
       "The middle is \\(9x + (-2x) = +7x\\), not \\(-7x\\). The larger cross-product \\(9x\\) is positive."),
]

# S6  (x+6)(x-1) = x^2+5x-6  opts: 0:x^2+5x+6, 1:*, 2:x^2-5x-6, 3:x^2+7x-6
silver[6]["hint"] = "Four products; the last term is 6 times minus 1."
silver[6]["misconceptions"] = [
    mc("sign_error", 0,
       "The last terms are \\(+6\\) and \\(-1\\), so \\(6 \\times (-1) = -6\\), not \\(+6\\)."),
    mc("middle_term", 3,
       "The outer product is \\(x \\times (-1) = -x\\), so \\(6x + (-x) = 5x\\), not \\(7x\\)."),
    mc("middle_term", 2,
       "The middle is \\(6x + (-x) = +5x\\), not \\(-5x\\). The larger cross-product \\(6x\\) is positive."),
]

# ---- GOLD -----------------------------------------------------------------
gold = pb["gold"]

# G0 REPLACED: (2x+3)(2x-3) = 4x^2-9   opts: 0:4x^2+9, 1:4x^2-12x-9, 2:*, 3:2x^2-9
gold[0] = {
    "display": "Expand and simplify \\((2x + 3)(2x - 3)\\)",
    "options": [
        "\\(4x^2 + 9\\)",
        "\\(4x^2 - 12x - 9\\)",
        "\\(4x^2 - 9\\)",
        "\\(2x^2 - 9\\)",
    ],
    "solutions": [2],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Difference of two squares: the x terms cancel, leaving first squared minus last squared.",
    "misconceptions": [
        mc("sign_error", 0,
           "The last terms are \\(+3\\) and \\(-3\\), so \\(3 \\times (-3) = -9\\), not \\(+9\\)."),
        mc("middle_term", 1,
           "The cross-products are \\(-6x\\) and \\(+6x\\), which cancel to 0. They do not add to \\(-12x\\)."),
        mc("forgot_squared", 3,
           "Square the whole first term: \\((2x)^2 = 2x \\times 2x = 4x^2\\), not \\(2x^2\\)."),
    ],
}

# G1  (x-3)^2 = x^2-6x+9  opts: 0:*, 1:x^2+6x+9, 2:x^2-9, 3:x^2-3x+9
gold[1]["hint"] = "Write it as (x minus 3)(x minus 3); do not forget the middle term."
gold[1]["misconceptions"] = [
    mc("sign_error", 1,
       "The middle term is \\(2 \\times x \\times (-3) = -6x\\), not \\(+6x\\)."),
    mc("missed_term", 2,
       "Squaring a bracket is not difference of two squares. \\((x - 3)^2\\) has a middle term, \\(-6x\\)."),
    mc("middle_term", 3,
       "There are two identical cross-products, \\(-3x\\) and \\(-3x\\), giving \\(-6x\\), not \\(-3x\\)."),
]

# G2  (2x+1)(x+3) = 2x^2+7x+3  opts: 0:*, 1:2x^2+5x+3, 2:2x^2+7x+4, 3:3x^2+7x+3
gold[2]["hint"] = "Multiply the coefficients for the first term: 2x times x is 2x squared."
gold[2]["misconceptions"] = [
    mc("middle_term", 1,
       "The cross-products are \\(6x\\) and \\(+x\\), which add to \\(7x\\), not \\(5x\\)."),
    mc("constant_error", 2,
       "The last term is \\(1 \\times 3 = 3\\), not \\(1 + 3 = 4\\)."),
    mc("leading_coeff", 3,
       "The first term is \\(2x \\times x = 2x^2\\), not \\(3x^2\\). Multiply the coefficients, do not add them."),
]

# G3  (3x-2)(2x+5) = 6x^2+11x-10  opts: 0:6x^2+11x+10, 1:6x^2-11x-10, 2:5x^2+11x-10, 3:*
gold[3]["hint"] = "Multiply the coefficients; 3x times 2x is 6x squared."
gold[3]["misconceptions"] = [
    mc("sign_error", 0,
       "The last terms are \\(-2\\) and \\(+5\\), so \\((-2) \\times 5 = -10\\), not \\(+10\\)."),
    mc("middle_term", 1,
       "The cross-products are \\(+15x\\) and \\(-4x\\), adding to \\(+11x\\), not \\(-11x\\)."),
    mc("leading_coeff", 2,
       "The first term is \\(3x \\times 2x = 6x^2\\), not \\(5x^2\\). Multiply the coefficients, do not add them."),
]

# G4  (2x+3)^2 = 4x^2+12x+9  opts: 0:4x^2+6x+9, 1:*, 2:2x^2+12x+9, 3:4x^2+9
gold[4]["hint"] = "Write it as (2x+3)(2x+3); square 2x to get 4x squared."
gold[4]["misconceptions"] = [
    mc("missed_term", 0,
       "There are two identical cross-products, \\(6x\\) and \\(6x\\), giving \\(12x\\), not \\(6x\\)."),
    mc("forgot_squared", 2,
       "Square the whole first term: \\((2x)^2 = 2x \\times 2x = 4x^2\\), not \\(2x^2\\)."),
    mc("missed_term", 3,
       "\\((2x + 3)^2\\) is not \\(4x^2 + 9\\). Squaring a bracket has a middle term, \\(+12x\\)."),
]

# ===========================================================================
# 3. Descriptions (keep existing, they are fine)
# ===========================================================================
# bronze/silver/gold_description already present.

# ===========================================================================
# 4. tier_guides
# ===========================================================================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: expanding a single bracket",
        "steps": [
            "One term sits outside the bracket. Multiply it by <strong>every</strong> term inside, one at a time.",
            "Keep each sign as you go: a minus outside flips the sign of whatever it multiplies.",
            "Write the products side by side. With a single bracket there is nothing to collect."
        ],
        "example": {
            "question": "Expand 4(2x − 5)",
            "steps": [
                {"label": "Multiply the first term", "content": "<p>\\(4 \\times 2x = 8x\\)</p>"},
                {"label": "Multiply the second term", "content": "<p>\\(4 \\times (-5) = -20\\)</p>"},
                {"label": "Check", "content": "<p>Put \\(x = 1\\): the bracket is \\(4(2 - 5) = -12\\), and \\(8(1) - 20 = -12\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(8x - 20\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: expanding double brackets",
        "steps": [
            "Every term in the first bracket multiplies every term in the second: four products in all (FOIL).",
            "The two middle products are like terms. Add them, keeping each sign, to get one middle term.",
            "Write it as \\(x^2 + (\\text{middle})x + (\\text{last})\\)."
        ],
        "example": {
            "question": "Expand and simplify (x + 5)(x − 2)",
            "steps": [
                {"label": "Four products", "content": "<p>\\(x \\times x = x^2\\), \\(x \\times (-2) = -2x\\), \\(5 \\times x = 5x\\), \\(5 \\times (-2) = -10\\)</p>"},
                {"label": "Collect the middle", "content": "<p>\\(-2x + 5x = 3x\\)</p>"},
                {"label": "Check", "content": "<p>Put \\(x = 1\\): \\((6)(-1) = -6\\), and \\(1 + 3 - 10 = -6\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(x^2 + 3x - 10\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: squares and difference of two squares",
        "steps": [
            "Squaring a bracket means writing it twice: \\((3x + 2)^2 = (3x + 2)(3x + 2)\\). Then expand as normal.",
            "Square the whole first term: \\((2x)^2 = 4x^2\\), not \\(2x^2\\). Multiply the coefficients too.",
            "Difference of two squares, \\((a + b)(a - b)\\), has cross-products that cancel, so the middle term is 0."
        ],
        "example": {
            "question": "Expand and simplify (3x + 2)²",
            "steps": [
                {"label": "Write it twice", "content": "<p>\\((3x + 2)^2 = (3x + 2)(3x + 2)\\)</p>"},
                {"label": "Four products", "content": "<p>\\(3x \\times 3x = 9x^2\\), \\(3x \\times 2 = 6x\\), \\(2 \\times 3x = 6x\\), \\(2 \\times 2 = 4\\)</p>"},
                {"label": "Collect the middle", "content": "<p>\\(6x + 6x = 12x\\)</p>"},
                {"label": "Check", "content": "<p>Put \\(x = 1\\): \\(5^2 = 25\\), and \\(9 + 12 + 4 = 25\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(9x^2 + 12x + 4\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ===========================================================================
# 5 + 6. guided (opener + teach)
# ===========================================================================
pd["guided"] = {
    "opener": {
        "label": "Before any algebra",
        "display": "Each party bag: 1 cupcake + 4 sweets<br>You buy 3 bags",
        "steps": [
            {
                "say": "A party-bag puzzle, no algebra needed. Each bag holds 1 cupcake and 4 sweets, and you buy 3 bags.",
                "pre": "Cupcakes in total: 3 bags × 1 cupcake = ",
                "post": "",
                "answer": 3,
                "hint": "Three bags, one cupcake in each."
            },
            {
                "say": "Now do the same for the sweets.",
                "pre": "Sweets in total: 3 bags × 4 sweets = ",
                "post": "",
                "answer": 12,
                "hint": "Three bags, four sweets in each."
            },
            {
                "say": "You multiplied the 3 bags across <strong>everything</strong> in the bag: 3 lots of (1 cupcake and 4 sweets) is 3 cupcakes and 12 sweets. Write the cupcake as \\(x\\) and that is exactly \\(3(x + 4) = 3x + 12\\). Expanding a bracket just shares the multiplier over every term inside."
            }
        ]
    },
    "teach": {
        "bronze": {
            "display": "Expand \\(5(2x + 3)\\)",
            "label": "Together: a single bracket",
            "steps": [
                {
                    "say": "One term outside, so multiply the 5 by every term inside \\(5(2x + 3)\\). Start with the \\(x\\) term.",
                    "pre": "5 × 2x = ",
                    "post": "x",
                    "answer": 10,
                    "hint": "Multiply the numbers in front: 5 × 2."
                },
                {
                    "pre": "and the 5 times the 3: 5 × 3 = ",
                    "post": "",
                    "answer": 15,
                    "hint": "Multiply 5 by the constant term.",
                    "done": "Both terms multiplied, so \\(5(2x + 3) = 10x + 15\\)."
                },
                {
                    "say": "Now check it. Put \\(x = 1\\) into the original bracket:",
                    "pre": "5 × (2 × 1 + 3) = ",
                    "post": "",
                    "answer": 25,
                    "hint": "Inside first: 2 × 1 + 3 = 5, then times 5."
                },
                {
                    "say": "And put \\(x = 1\\) into your answer:",
                    "pre": "10 × 1 + 15 = ",
                    "post": "",
                    "answer": 25,
                    "done": "Both give 25, so \\(10x + 15\\) is right.",
                    "hint": "10 lots of 1, plus 15."
                }
            ]
        },
        "silver": {
            "display": "Expand and simplify \\((x + 5)(x - 2)\\)",
            "label": "Together: two brackets",
            "steps": [
                {
                    "say": "Two brackets means four products. The first is \\(x \\times x = x^2\\). Now the two cross terms. Outer:",
                    "pre": "x × (−2) = ",
                    "post": "x",
                    "answer": -2,
                    "hint": "x times minus 2."
                },
                {
                    "pre": "Inner: 5 × x = ",
                    "post": "x",
                    "answer": 5,
                    "hint": "5 times x."
                },
                {
                    "say": "The two cross terms are like terms, so add them for the middle term:",
                    "pre": "−2x + 5x = ",
                    "post": "x",
                    "answer": 3,
                    "hint": "Add the coefficients: −2 + 5.",
                    "done": "That is the one new move: collecting the two middle terms."
                },
                {
                    "pre": "Last: 5 × (−2) = ",
                    "post": "",
                    "answer": -10,
                    "hint": "5 times minus 2."
                },
                {
                    "say": "So \\((x + 5)(x - 2) = x^2 + 3x - 10\\). Check with \\(x = 1\\): the brackets give \\((6)(-1) = -6\\).",
                    "pre": "And your answer: 1 + 3 − 10 = ",
                    "post": "",
                    "answer": -6,
                    "done": "Both give −6, so \\(x^2 + 3x - 10\\) is right.",
                    "hint": "Work out 1 + 3 − 10."
                }
            ]
        },
        "gold": {
            "display": "Expand and simplify \\((3x + 2)^2\\)",
            "label": "Together: squaring a bracket",
            "steps": [
                {
                    "say": "Squaring means writing the bracket twice: \\((3x + 2)^2 = (3x + 2)(3x + 2)\\). The new move is squaring the first term. Multiply the coefficients:",
                    "pre": "3x × 3x = ",
                    "post": "x²",
                    "answer": 9,
                    "hint": "Multiply the numbers in front: 3 × 3. The x times x makes x squared."
                },
                {
                    "say": "Now the two cross terms. Outer:",
                    "pre": "3x × 2 = ",
                    "post": "x",
                    "answer": 6,
                    "hint": "3 times 2."
                },
                {
                    "pre": "Inner: 2 × 3x = ",
                    "post": "x",
                    "answer": 6,
                    "hint": "2 times 3."
                },
                {
                    "say": "Add the two cross terms for the middle:",
                    "pre": "6x + 6x = ",
                    "post": "x",
                    "answer": 12,
                    "hint": "Add the coefficients: 6 + 6."
                },
                {
                    "pre": "Last: 2 × 2 = ",
                    "post": "",
                    "answer": 4,
                    "hint": "2 times 2."
                },
                {
                    "say": "So \\((3x + 2)^2 = 9x^2 + 12x + 4\\). Check with \\(x = 1\\): the bracket is \\(5^2 = 25\\).",
                    "pre": "And your answer: 9 + 12 + 4 = ",
                    "post": "",
                    "answer": 25,
                    "done": "Both give 25, so \\(9x^2 + 12x + 4\\) is right.",
                    "hint": "Add 9 + 12 + 4."
                }
            ]
        }
    }
}

# ===========================================================================
# 8. method_card (slim)
# ===========================================================================
pd["method_card"] = {
    "title": "How to Expand Brackets",
    "steps": [
        "Single bracket: multiply the outside term by every term inside.",
        "Double brackets: multiply each term in the first by each term in the second (four products).",
        "Collect the two middle terms.",
        "Know the patterns: \\((a + b)(a - b) = a^2 - b^2\\) and \\((x + a)^2 = x^2 + 2ax + a^2\\)."
    ],
    "content": "<p><strong>Expanding brackets</strong> means multiplying every term inside a bracket by the term (or terms) outside, which removes the brackets.</p><p>For a single bracket, \\(3(2x + 5) = 6x + 15\\): the 3 multiplies both terms. For double brackets, \\((x + 3)(x + 4)\\) gives four products; collect the two middle terms.</p><p>Two patterns to know: the difference of two squares, \\((a + b)(a - b) = a^2 - b^2\\), where the middle terms cancel, and squaring, \\((x + a)^2 = x^2 + 2ax + a^2\\). Never drop the middle term when squaring.</p>",
    "example": "<p><strong>Expand and simplify</strong> \\((x + 3)(x - 5)\\)</p><p><strong>Step 1:</strong> \\(x \\times x = x^2\\)</p><p><strong>Step 2:</strong> \\(x \\times (-5) = -5x\\)</p><p><strong>Step 3:</strong> \\(3 \\times x = 3x\\)</p><p><strong>Step 4:</strong> \\(3 \\times (-5) = -15\\)</p><p><strong>Collect:</strong> \\(x^2 - 5x + 3x - 15 = x^2 - 2x - 15\\)</p>"
}

# ===========================================================================
# 9. Preserve related_videos, topic_links, worked_examples.
#    Only forced edit: strip em dashes from worked_examples step labels
#    ("Step 1 — Multiply" -> "Step 1: Multiply") to satisfy the hard style
#    rule / validator. Content untouched otherwise.
# ===========================================================================
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str) and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT)
