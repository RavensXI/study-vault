# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_live_algebra-L01.json", encoding="utf-8"))

# ---------------------------------------------------------------------------
# 1. method_card (slim) -----------------------------------------------------
pd["method_card"]["title"] = "Simplifying Expressions"
pd["method_card"]["steps"] = [
    "Collect like terms: same letter, same power. Add or subtract only the coefficients.",
    "Multiplying terms: multiply the coefficients and add the indices.",
    "Dividing terms: divide the coefficients and subtract the indices.",
    "Power of a power: multiply the indices, and apply the power to the coefficient too.",
]
pd["method_card"]["content"] = (
    "<p><strong>Simplifying</strong> means writing an expression in its shortest form. "
    "<strong>Like terms</strong> share the same letter and the same power, so \\(3x\\) and "
    "\\(5x\\) combine but \\(3x\\) and \\(3x^2\\) do not.</p>"
    "<p>Collect like terms by adding or subtracting their coefficients; the letter and its "
    "power stay the same. To multiply terms, multiply the coefficients and add the indices. "
    "To divide, divide the coefficients and subtract the indices.</p>"
    "<p>Index laws: \\(x^a \\times x^b = x^{a+b}\\), \\(x^a \\div x^b = x^{a-b}\\), "
    "\\((x^a)^b = x^{ab}\\).</p>"
)
# keep method_card.example as-is (no em dashes present)

# ---------------------------------------------------------------------------
# 2. worked_examples: remove em dashes from labels --------------------------
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and isinstance(st["label"], str):
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---------------------------------------------------------------------------
# 3. Replace silver[6] with a mixed multiply-then-divide problem ------------
pd["problem_bank"]["silver"][6] = {
    "display": "Simplify \\((12m^5 \\times 2m) \\div 4m^3\\)",
    "options": ["\\(6m^3\\)", "\\(24m^3\\)", "\\(6m^9\\)", "\\(3m^2\\)"],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Multiply the top two terms first, then divide by the bottom term.",
    "misconceptions": [],  # filled below
}

# ---------------------------------------------------------------------------
# 4. Hints per problem ------------------------------------------------------
HINTS = {
    ("bronze", 0): "Add the number parts of the two x-terms; the x stays as it is.",
    ("bronze", 1): "Subtract the coefficients: 8 take away 3.",
    ("bronze", 2): "Add the first two terms, then subtract the last one.",
    ("bronze", 3): "Collect the x-terms together and the plain numbers together, separately.",
    ("bronze", 4): "Work left to right, remembering the lone m counts as 1m.",
    ("bronze", 5): "Collect the p-terms and the q-terms in two separate groups.",
    ("bronze", 6): "Combine the t-terms; the plain number 3 stays on its own.",
    ("bronze", 7): "Group the x-terms and the y-terms separately, watching the minus sign.",
    ("silver", 0): "Collect the x-squared terms and the x-terms in separate groups.",
    ("silver", 1): "Multiply the numbers, then add the powers of x.",
    ("silver", 2): "Multiply the coefficients and add the indices.",
    ("silver", 3): "Divide the numbers, then subtract the powers.",
    ("silver", 4): "Keep the a-squared terms and the a-terms separate; the lone a is 1a.",
    ("silver", 5): "Multiply the coefficients and add the indices of x.",
    ("silver", 6): "Multiply the top two terms first, then divide by the bottom term.",
    ("gold", 0): "Divide the numbers and subtract the powers of x.",
    ("gold", 1): "Square both the 2 and the power of x.",
    ("gold", 2): "Multiply the first two terms, then divide the result by the last.",
    ("gold", 3): "Cube the 3 and multiply the power of a by 3.",
    ("gold", 4): "Multiply the two top terms, then divide by the bottom term.",
}

# ---------------------------------------------------------------------------
# 5. Misconceptions per problem (expect = wrong OPTION index) ---------------
def mc(pattern, expect, message, note):
    return {"pattern": pattern, "expect": expect, "message": message, "note": note}

MIS = {
    ("bronze", 0): [
        mc("coefficient_error", 1, "Add the numbers in front, do not multiply them. 6x plus 3x means 6 lots of x and 3 more, giving 9x. Multiplying 6 by 3 to get 18 is the slip.", "6x3=18 -> 18x, option 1"),
        mc("index_error", 2, "When you collect like terms the power of x does not change. 6x plus 3x is 9x, not 9x squared. Powers only grow when you multiply terms together.", "added indices -> 9x^2, option 2"),
        mc("dropped_term", 3, "Do not lose a term. Both 6x and 3x are added: 6 plus 3 is 9, so the answer is 9x.", "kept only 6x, option 3"),
    ],
    ("bronze", 1): [
        mc("sign_error", 0, "This is a subtraction. 8y minus 3y is 5y. Adding to get 11y ignores the minus sign.", "8+3=11 -> 11y, option 0"),
        mc("index_error", 2, "The power of y stays the same when collecting like terms, so 8y minus 3y is 5y, not 5y squared.", "changed power, option 2"),
        mc("coefficient_error", 3, "Check the subtraction: 8 minus 3 is 5, so the answer is 5y.", "arithmetic slip to 3y, option 3"),
    ],
    ("bronze", 2): [
        mc("sign_error", 1, "The last term is subtracted. 4a plus 5a minus 2a is 7a, not 11a. Do not turn the minus into a plus.", "treated -2a as +2a -> 11a, option 1"),
        mc("index_error", 2, "Collecting like terms keeps the power of a the same, so the answer is 7a, not 7a squared.", "changed power, option 2"),
        mc("dropped_term", 3, "Do not stop early: after 4a plus 5a you still subtract 2a, which gives 7a, not 9a.", "4+5=9, ignored -2a, option 3"),
    ],
    ("bronze", 3): [
        mc("unlike_terms", 3, "x-terms and plain numbers are unlike terms, so you cannot combine them into 17x. Collect the x-terms (3x plus 2x is 5x) apart from the numbers (7 plus 5 is 12).", "combined all as x -> 17x, option 3"),
        mc("coefficient_error", 1, "The 7 is a plain number, not an x-term, so it joins the 5 to make 12. Only 3x and 2x are x-terms, giving 5x.", "3+7=10x -> 10x+12, option 1"),
        mc("constant_error", 2, "Add the numbers: 7 plus 5 is 12, not 2. The answer is 5x plus 12.", "7-5=2 -> 5x+2, option 2"),
    ],
    ("bronze", 4): [
        mc("sign_error", 1, "Mind the minus. 9m minus 4m plus m is 6m. Adding all three to reach 14m ignores the subtraction.", "9+4+1=14, option 1"),
        mc("coefficient_error", 0, "The last term is plus m, so add it: 9 minus 4 is 5, plus 1 more makes 6m, not 4m.", "9-4-1=4, option 0"),
        mc("dropped_term", 3, "Do not drop the lone m, which counts as 1m: 5m plus 1m is 6m, not 5m.", "9-4=5, ignored +m, option 3"),
    ],
    ("bronze", 5): [
        mc("unlike_terms", 1, "p-terms and q-terms are unlike, so they cannot merge into 9pq. Collect them separately: 2p plus 3p is 5p, and 6q minus 2q is 4q.", "2+6+3-2=9pq, option 1"),
        mc("sign_error", 2, "Watch the minus on the q-terms: 6q minus 2q is 4q, not 8q.", "6+2=8q, option 2"),
        mc("sign_error", 3, "Collect the q-terms in order: 6q minus 2q is plus 4q, not minus 4q.", "2-6=-4q, option 3"),
    ],
    ("bronze", 6): [
        mc("sign_error", 3, "The 7t is subtracted: 10t minus 7t is 3t, not 17t.", "10+7=17t, option 3"),
        mc("unlike_terms", 1, "The 3 is a plain number, not a t-term, so it cannot join the t-count. 10t minus 7t is 3t, and the 3 stays separate, giving 3t plus 3.", "10-7+3=6t, option 1"),
        mc("constant_error", 2, "The 3 is added, so it stays positive. The answer is 3t plus 3, not 3t minus 3.", "made constant negative, option 2"),
    ],
    ("bronze", 7): [
        mc("sign_error", 0, "The third term is minus x, so 5x minus x is 4x, not 6x.", "5+1=6x, option 0"),
        mc("unlike_terms", 3, "x-terms and y-terms are unlike and cannot merge into 9xy. Collect separately: 5x minus x is 4x, and 2y plus 3y is 5y.", "5+2-1+3=9xy, option 3"),
        mc("sign_error", 2, "Add the y-terms: 2y plus 3y is 5y, not minus y.", "2-3=-y, option 2"),
    ],
    ("silver", 0): [
        mc("sign_error", 1, "The 2x is subtracted: 5x minus 2x is 3x, not 7x. The x-squared part, 4x squared, is right.", "5+2=7x, option 1"),
        mc("unlike_terms", 2, "x-squared and x are unlike terms, so they cannot be added into a single 7x-cubed term. Keep 4x squared and 3x apart.", "merged all -> 7x^3, option 2"),
        mc("coefficient_error", 3, "Collect the x-squared terms too: 3x squared plus x squared is 4x squared, not 3x squared.", "kept 3x^2, option 3"),
    ],
    ("silver", 1): [
        mc("index_error", 0, "Multiplying terms means adding the indices: x times x is x squared. So 4x times 3x is 12x squared, not 12x.", "multiplied indices 1x1=1, option 0"),
        mc("coefficient_error", 2, "Multiply the coefficients, do not add them: 4 times 3 is 12, giving 12x squared, not 7x squared.", "4+3=7, option 2"),
    ],
    ("silver", 2): [
        mc("index_error", 1, "Add the indices when multiplying, do not multiply them: 2 plus 3 is 5, so the answer is 10y to the power 5, not the power 6.", "2x3=6, option 1"),
        mc("coefficient_error", 2, "Multiply the coefficients: 5 times 2 is 10, not 7.", "5+2=7, option 2"),
    ],
    ("silver", 3): [
        mc("index_error", 0, "Dividing means subtracting the indices: x cubed divided by x is x squared, since 3 minus 1 is 2. The answer is 4x squared, not 4x cubed.", "kept x^3, option 0"),
        mc("coefficient_error", 1, "Divide the coefficients, do not subtract them: 20 divided by 5 is 4, not 15.", "20-5=15, option 1"),
    ],
    ("silver", 4): [
        mc("unlike_terms", 2, "a-squared and a are unlike terms, so they cannot merge into 8a cubed. Keep them apart: 4a squared and 4a.", "merged all -> 8a^3, option 2"),
        mc("coefficient_error", 1, "Do not forget the lone a, which means plus 1a: 3a plus a is 4a, not 2a.", "path to 4a^2+2a, option 1"),
        mc("coefficient_error", 3, "Collect the a-squared terms: 6a squared minus 2a squared is 4a squared, not 6a squared.", "kept 6a^2, option 3"),
    ],
    ("silver", 5): [
        mc("index_error", 0, "Add the indices when multiplying, do not multiply them: 1 plus 2 is 3, so the answer is 14x cubed, not 14x squared.", "1x2=2, option 0"),
        mc("coefficient_error", 1, "Multiply the coefficients: 7 times 2 is 14, not 9.", "7+2=9, option 1"),
    ],
    ("silver", 6): [
        mc("coefficient_error", 1, "Finish the division: 24 divided by 4 is 6, so the answer is 6m cubed, not 24m cubed.", "forgot to divide by 4, option 1"),
        mc("index_error", 2, "The last step divides, so subtract its index: 6 minus 3 is 3. The answer is 6m cubed, not 6m to the power 9.", "added divisor index 6+3=9, option 2"),
        mc("dropped_term", 3, "Do not skip the multiply step: 12m to the 5 times 2m is 24m to the 6, then dividing by 4m cubed gives 6m cubed.", "ignored x2m -> 12/4=3, 5-3=2, option 3"),
    ],
    ("gold", 0): [
        mc("index_error", 1, "Dividing means subtracting the indices: 5 minus 2 is 3, so the answer is 3x cubed. Adding to reach x to the 7 is the slip.", "5+2=7, option 1"),
        mc("coefficient_error", 2, "Divide the coefficients, do not subtract them: 12 divided by 4 is 3, not 8.", "12-4=8, option 2"),
    ],
    ("gold", 1): [
        mc("coefficient_error", 0, "The outer power applies to the 2 as well: 2 squared is 4, giving 4x to the 6, not 2x to the 6.", "forgot power on coefficient, option 0"),
        mc("index_error", 1, "Raising a power to a power multiplies the indices: 3 times 2 is 6, so x cubed squared is x to the 6, not x to the 5.", "3+2=5, option 1"),
        mc("index_error", 3, "Multiply the indices, do not square the index: 3 times 2 is 6, not 9.", "3^2=9, option 3"),
    ],
    ("gold", 2): [
        mc("index_error", 1, "The final step divides, so subtract its index: 2 plus 3 is 5, then minus 1 gives 4. The answer is 2x to the 4, not x to the 5.", "forgot to subtract divisor index, option 1"),
        mc("coefficient_error", 2, "Finish the division: 12 divided by 6 is 2, so the answer is 2x to the 4, not 12x to the 4.", "forgot to divide by 6, option 2"),
        mc("index_error", 3, "Do not add the divisor's index. After 2 plus 3 is 5, subtract the 1 to get 4, not add it to reach 6.", "2+3+1=6, option 3"),
    ],
    ("gold", 3): [
        mc("coefficient_error", 0, "The outer power applies to the 3 too: 3 cubed is 27, not 9. The answer is 27a to the 6.", "3^2=9, option 0"),
        mc("index_error", 2, "Raising a power to a power multiplies the indices: 2 times 3 is 6, so a squared cubed is a to the 6, not a to the 5.", "2+3=5, option 2"),
    ],
    ("gold", 4): [
        mc("index_error", 1, "Add the top indices first: 6 plus 1 is 7, then subtract 4 for the division to get x cubed, not x squared.", "6-4=2 missed +1, option 1"),
        mc("coefficient_error", 2, "Divide by the 12 as well: 24 divided by 12 is 2, so the answer is 2x cubed, not 24x cubed.", "forgot to divide by 12, option 2"),
        mc("index_error", 3, "The bottom divides, so subtract its index: 7 minus 4 is 3. The answer is 2x cubed, not x to the 10.", "over-added indices to 10, option 3"),
    ],
}

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        p["hint"] = HINTS[(tier, i)]
        p["misconceptions"] = MIS[(tier, i)]

# ---------------------------------------------------------------------------
# 6. tier_guides ------------------------------------------------------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: Collecting like terms",
        "steps": [
            "<strong>Like terms</strong> have the same letter and the same power. \\(6x\\) and \\(3x\\) are like terms; an \\(x\\) and a plain number are not.",
            "Group the like terms, then add or subtract only the number in front (the coefficient). The letter and its power stay exactly the same.",
            "Watch each sign: a term with a minus in front stays negative when you collect.",
        ],
        "example": {
            "question": "Simplify 7x + 4 + 2x + 3",
            "steps": [
                {"label": "Collect the x-terms", "content": "<p>\\(7x + 2x = 9x\\)</p>"},
                {"label": "Collect the numbers", "content": "<p>\\(4 + 3 = 7\\)</p>"},
                {"label": "Check", "content": "<p>x-terms and numbers are unlike, so they stay in separate groups.</p>"},
                {"label": "Answer", "content": "<p><strong>\\(9x + 7\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: Powers, and multiplying or dividing terms",
        "steps": [
            "To <strong>multiply</strong> terms, multiply the coefficients and <strong>add</strong> the indices: \\(4x \\times 3x = 12x^2\\).",
            "To <strong>divide</strong>, divide the coefficients and <strong>subtract</strong> the indices: \\(20x^3 \\div 5x = 4x^2\\).",
            "When collecting mixed terms, \\(x^2\\) and \\(x\\) are unlike, so keep them in separate groups.",
        ],
        "example": {
            "question": "Simplify 3x^2 * 5x^4",
            "steps": [
                {"label": "Multiply the coefficients", "content": "<p>\\(3 \\times 5 = 15\\)</p>"},
                {"label": "Add the indices", "content": "<p>\\(x^2 \\times x^4 = x^{2+4} = x^6\\)</p>"},
                {"label": "Check", "content": "<p>Multiplying adds indices, so the power climbs to 6.</p>"},
                {"label": "Answer", "content": "<p><strong>\\(15x^6\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: Index laws and multi-step simplifying",
        "steps": [
            "To raise a power to a power, <strong>multiply</strong> the indices, and apply the outer power to the coefficient too: \\((2x^3)^2 = 4x^6\\).",
            "For a multi-step expression, deal with the multiplication first, then the division.",
            "Multiply or divide the coefficients as normal; add indices for a multiply, subtract them for a divide.",
        ],
        "example": {
            "question": "Simplify (3x^4)^2",
            "steps": [
                {"label": "Power the coefficient", "content": "<p>\\(3^2 = 9\\)</p>"},
                {"label": "Multiply the indices", "content": "<p>\\((x^4)^2 = x^{4 \\times 2} = x^8\\)</p>"},
                {"label": "Check", "content": "<p>The outer power hits both the 3 and the \\(x^4\\).</p>"},
                {"label": "Answer", "content": "<p><strong>\\(9x^8\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# 7. guided (opener + teach walks) ------------------------------------------
pd["guided"] = {
    "opener": {
        "label": "Before any algebra",
        "display": "5 apples, then 3 more apples...<br>then 2 bananas.",
        "steps": [
            {
                "say": "A shopping puzzle, no algebra needed. You have 5 apples in a basket and drop in 3 more apples.",
                "pre": "How many apples now? ",
                "post": "",
                "answer": 8,
                "hint": "Add the apples together: 5 and 3.",
            },
            {
                "say": "Simple, because they are the same fruit. Now you add 2 bananas to those 8 apples.",
                "pre": "How many apples do you have now? ",
                "post": "",
                "answer": 8,
                "hint": "Bananas are a different fruit, so the number of apples does not change.",
                "done": "The apple count is still 8. Bananas cannot be folded in.",
            },
            {
                "say": "You could not merge apples and bananas into one number, because they are different things. That is exactly what <strong>like terms</strong> means. Algebra just writes apples as \\(x\\) and bananas as \\(y\\): \\(5x + 3x = 8x\\), but \\(8x + 2y\\) has to stay as \\(8x + 2y\\), since \\(x\\) and \\(y\\) are unlike.",
            },
        ],
    },
    "teach": {
        "bronze": {
            "display": "Simplify \\(7x + 5 + 4x + 2\\)",
            "label": "Together: your first one",
            "steps": [
                {
                    "say": "Collect the like terms. Start with the x-terms, 7x and 4x, and add the numbers in front.",
                    "pre": "7x + 4x = ",
                    "post": "x",
                    "answer": 11,
                    "hint": "Add the coefficients: 7 plus 4.",
                },
                {
                    "say": "Now the plain numbers, 5 and 2. They are like terms with each other.",
                    "pre": "5 + 2 = ",
                    "post": "",
                    "answer": 7,
                    "done": "x-terms and numbers are unlike, so they stay apart: 11x + 7.",
                    "hint": "Add the two constants.",
                },
                {
                    "say": "So the expression tidies to 11x + 7. Check it by putting x = 1 into the original.",
                    "pre": "7 + 5 + 4 + 2 = ",
                    "post": "",
                    "answer": 18,
                    "hint": "At x = 1 each x is just 1, so add all four numbers.",
                },
                {
                    "pre": "and your answer at x = 1: 11 + 7 = ",
                    "post": "",
                    "answer": 18,
                    "done": "Both give 18, so 11x + 7 is right.",
                    "hint": "Add 11 and 7.",
                },
            ],
        },
        "silver": {
            "display": "Simplify \\(6x^2 \\times 4x^3\\)",
            "label": "Together: your first one",
            "steps": [
                {
                    "say": "Multiplying terms works in two parts. First multiply the coefficients, the numbers in front.",
                    "pre": "6 × 4 = ",
                    "post": "",
                    "answer": 24,
                    "hint": "Multiply 6 by 4.",
                },
                {
                    "say": "Now the powers of x. Multiplying terms means you ADD the indices.",
                    "pre": "2 + 3 = ",
                    "post": "",
                    "answer": 5,
                    "done": "Multiply is add for indices. That is the whole point.",
                    "hint": "Add the two powers, 2 and 3.",
                },
                {
                    "say": "So the answer is 24x to the power 5, written 24x^5. Check the index by counting the x factors: x^2 is x times x, and x^3 is x times x times x.",
                    "pre": "count the x's: 2 + 3 = ",
                    "post": "",
                    "answer": 5,
                    "hint": "There are 2 then 3 of them.",
                },
                {
                    "pre": "and the coefficient once more: 6 × 4 = ",
                    "post": "",
                    "answer": 24,
                    "done": "Coefficient 24 and index 5 confirm 24x^5.",
                    "hint": "Multiply 6 by 4 again to be sure.",
                },
            ],
        },
        "gold": {
            "display": "Simplify \\((2x^4)^3\\)",
            "label": "Together: your first one",
            "steps": [
                {
                    "say": "A power outside the bracket hits everything inside. Start with the number: raise 2 to the power 3.",
                    "pre": "2 × 2 × 2 = ",
                    "post": "",
                    "answer": 8,
                    "hint": "Multiply three 2's together.",
                },
                {
                    "say": "Now the power of x. A power raised to a power means MULTIPLY the indices.",
                    "pre": "4 × 3 = ",
                    "post": "",
                    "answer": 12,
                    "done": "Power to a power multiplies indices. That is the gold move.",
                    "hint": "Multiply the two indices, 4 and 3.",
                },
                {
                    "say": "So (2x^4)^3 = 8x^12. Check the index by expanding: (x^4)^3 = x^4 × x^4 × x^4, which adds indices.",
                    "pre": "4 + 4 + 4 = ",
                    "post": "",
                    "answer": 12,
                    "hint": "Add three lots of 4.",
                },
                {
                    "pre": "and the coefficient: 2 × 2 × 2 = ",
                    "post": "",
                    "answer": 8,
                    "done": "8 and index 12 confirm 8x^12.",
                    "hint": "Multiply three 2's.",
                },
            ],
        },
    },
}

# ---------------------------------------------------------------------------
json.dump(pd, io.open("lesson_algebra-L01.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written lesson_algebra-L01.json")
