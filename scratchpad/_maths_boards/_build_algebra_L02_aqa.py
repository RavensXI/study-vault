# -*- coding: utf-8 -*-
import json, io

SRC = "_live_algebra-L02.json"
OUT = "lesson_maths-aqa_algebra-L02.json"

pd = json.load(io.open(SRC, encoding="utf-8"))

# ---- method_card: trim content <=140 words, remove em dash ----
pd["method_card"]["content"] = (
    "<p><strong>Single brackets:</strong> multiply every term inside by the term outside. "
    "\\(3(2x + 5) = 6x + 15\\).</p>"
    "<p><strong>Double brackets:</strong> FOIL, every term in the first bracket times every term "
    "in the second, then collect the middle terms. \\((x+3)(x-5) = x^2 - 2x - 15\\).</p>"
    "<p><strong>Squaring:</strong> \\((a + b)^2 = a^2 + 2ab + b^2\\). Keep the middle term \\(2ab\\); "
    "do not just square each part.</p>"
    "<p><strong>Difference of two squares:</strong> \\((a + b)(a - b) = a^2 - b^2\\), the middle "
    "terms cancel.</p>"
)

pb = pd["problem_bank"]

pb["bronze_description"] = "Single brackets: multiply the term outside by each term inside, keeping every sign."
pb["silver_description"] = "Two brackets (FOIL): multiply every term in the first by every term in the second, then collect the middle terms."
pb["gold_description"] = "Harder expansions: squared brackets, difference of two squares, triple brackets and surds. Keep every term."

def setp(tier, i, hint, mis):
    p = pb[tier][i]
    p["hint"] = hint
    p["misconceptions"] = mis

def mc(pattern, expect, message):
    return {"pattern": pattern, "expect": expect, "message": message,
            "note": "expect = original option index of this distractor"}

# BRONZE
setp("bronze", 0, "Multiply the 3 by the x and by the 4 separately.", [
    mc("forget_second", 1, "The 3 must multiply BOTH parts. You kept the 4 unchanged, but 3 × 4 = 12, so the answer is 3x + 12."),
    mc("added_not_multiplied", 2, "It looks like you added 3 + 4 = 7. The 3 multiplies the 4, it is not added to it: 3 × 4 = 12."),
])
setp("bronze", 1, "Multiply the 5 by both terms, and keep the minus on the 3.", [
    mc("forget_second", 1, "The 5 has to reach the 3 as well: 5 × 3 = 15, so the answer is 10x − 15. You left the 3 untouched."),
    mc("sign_error", 3, "5 × (−3) = −15, not +15. The minus sign inside the bracket stays with the term."),
])
setp("bronze", 2, "Multiply −2 by both terms; a negative times a positive is negative.", [
    mc("sign_error", 1, "−2 × 6 = −12, not +12. A negative times a positive stays negative, so both terms are negative."),
    mc("forget_second", 3, "The −2 must multiply the 6 too: −2 × 6 = −12. You left the 6 unchanged."),
])
setp("bronze", 3, "x times x is x squared, and x times 7 is 7x.", [
    mc("forget_x", 1, "The x outside multiplies the 7 as well: x × 7 = 7x, so the answer is x² + 7x. You left the 7 with no x."),
    mc("x_times_x", 2, "x × x is x², not 2x. Multiplying two x terms adds the powers, it does not double the x."),
])
setp("bronze", 4, "Multiply 4x by 2x and by −1; remember x times x is x squared.", [
    mc("forget_multiply_x", 1, "The 4x must multiply the −1 too: 4x × (−1) = −4x, so the answer is 8x² − 4x. You left the 1 with no x."),
    mc("lost_square", 3, "4x × 2x = 8x², not 8x. Multiplying the two x terms gives x², so the first term is squared."),
])
setp("bronze", 5, "Expand both brackets, then add the x terms and the numbers separately.", [
    mc("added_constants", 1, "The constants are 3 × 2 = 6 and 2 × 5 = 10, giving 6 + 10 = 16, not 7. It looks like the 2 and 5 were added directly."),
    mc("dropped_first", 2, "You have only the 10 from the second bracket. The first bracket also gives 3 × 2 = 6, so the total is 6 + 10 = 16."),
])
setp("bronze", 6, "The second bracket has −2 in front, so both its terms are subtracted.", [
    mc("sign_error", 1, "−2 × 3 = −6, not +6. Both terms in the second bracket are multiplied by −2, so it is 5x − 5 − 2x − 6 = 3x − 11."),
    mc("lost_minus_x", 2, "The second bracket has −2 in front, so its x term is −2x. That gives 5x − 2x = 3x, not 7x."),
])
setp("bronze", 7, "Multiply −3 by both terms; negative times negative is positive.", [
    mc("sign_error", 1, "−3 × (−4) = +12, not −12. A negative times a negative is positive."),
    mc("forget_second", 3, "The −3 must multiply the 4 too: −3 × (−4) = +12. You left the 4 nearly unchanged."),
])

# SILVER
setp("silver", 0, "Use FOIL, then add the two middle terms.", [
    mc("swap_terms", 1, "The middle and last terms are swapped. The middle is 4x + 3x = 7x and the constant is 4 × 3 = 12, so it is x² + 7x + 12."),
    mc("added_constants", 2, "The constant is 4 × 3 = 12, not 4 + 3 = 7. Multiply the two numbers for the last term."),
])
setp("silver", 1, "Use FOIL and add the middle terms with their signs: −2x + 6x.", [
    mc("middle_sign", 1, "The middle term is −2x + 6x = +4x, not −4x. Add the two middle products with their signs."),
    mc("constant_sign", 2, "−2 × 6 = −12, not +12. The last term keeps the minus sign."),
])
setp("silver", 2, "Use FOIL; negative times negative gives a positive constant.", [
    mc("constant_sign", 1, "−5 × (−3) = +15, not −15. A negative times a negative is positive."),
    mc("middle_sign", 2, "The middle term is −5x − 3x = −8x, not +8x. Both middle products are negative."),
])
setp("silver", 3, "Use FOIL and combine −8x with +3x for the middle term.", [
    mc("middle_sign", 1, "The middle term is −8x + 3x = −5x, not +5x. Keep the sign from 2x × (−4)."),
    mc("constant_sign", 2, "1 × (−4) = −4, not +4. The last term keeps the minus."),
])
setp("silver", 4, "Square the bracket as (x+5)(x+5); the middle term is 2 times 5 times x.", [
    mc("no_middle", 1, "You squared each term separately. \\((x+5)^2\\) needs the middle term 2 × 5 × x = 10x, giving x² + 10x + 25."),
    mc("half_middle", 2, "The middle term is 2 × 5 × x = 10x, not 5x. Squaring a bracket doubles that product."),
])
setp("silver", 5, "Square the bracket in full; the middle term is 2 times −4 times x.", [
    mc("no_middle", 1, "You squared each term separately. The middle term 2 × (−4) × x = −8x is missing, so it is x² − 8x + 16."),
    mc("constant_sign", 2, "(−4)² = +16, not −16. Squaring a negative gives a positive constant."),
])
setp("silver", 6, "This is the difference of two squares, so the middle terms cancel.", [
    mc("keep_middle", 2, "The middle terms +3x and −3x cancel, so there is no x term. Also 3 × (−3) = −9, giving just x² − 9."),
    mc("constant_sign", 1, "3 × (−3) = −9, not +9. This is the difference of two squares: x² − 9."),
])

# GOLD
setp("gold", 0, "Use FOIL and combine +15x with −4x for the middle term.", [
    mc("middle_sign", 1, "The middle term is +15x − 4x = +11x, not −11x. Add the two middle products with their signs."),
    mc("constant_sign", 2, "−2 × 5 = −10, not +10. The last term keeps the minus sign."),
])
setp("gold", 1, "Square (2x+3) in full; do not forget the 12x middle term, and (2x)² is 4x².", [
    mc("no_middle", 1, "You squared each term only. The middle term 2 × 2x × 3 = 12x is missing, giving 4x² + 12x + 9."),
    mc("lost_square", 3, "(2x)² = 4x², not 2x². Square both the 2 and the x."),
])
setp("gold", 2, "Expand two brackets first, then multiply that result by the third.", [
    mc("wrong_x_coeff", 1, "The x term is wrong. After expanding fully the coefficient of x is 11, not 6: x³ + 6x² + 11x + 6."),
    mc("wrong_x2_coeff", 3, "The x² coefficient is 1 + 2 + 3 = 6, not 3. Collect every x² term from the expansion."),
])
setp("gold", 3, "Expand both squares fully, subtract, then read off the number in front of x.", [
    mc("gave_b", 12, "12 is b, the constant. The question asks for a, the number in front of x, which is 4."),
    mc("no_middle", 0, "It looks like the middle terms were dropped. Keep them: (x+4)² = x² + 8x + 16 and (x+2)² = x² + 4x + 4, so the difference is 4x + 12 and a = 4."),
])
setp("gold", 4, "Difference of two squares: square the √3 to get 3.", [
    mc("no_square_surd", 1, "The √3 must be squared: (√3)² = 3, so the answer is x² − 3, not x² − √3."),
    mc("constant_sign", 2, "The last term is +√3 × −√3 = −3, so it is x² − 3. The result is negative."),
])

# ---- guided_steps: silver[0], gold[0] (completion + lifeline), gold[3] (required) ----
pb["silver"][0]["guided_steps"] = [
    {"say": "FOIL. First is x × x = x², the x² term. Now the Outer and Inner products."},
    {"pre": "Outer: x × 3 = ", "post": "x", "answer": 3, "hint": "Multiply the first x by the 3."},
    {"pre": "Inner: 4 × x = ", "post": "x", "answer": 4, "hint": "Multiply the 4 by the x."},
    {"pre": "Last: 4 × 3 = ", "post": "", "answer": 12, "hint": "Multiply the two numbers."},
    {"say": "Collect the two middle terms: 3x + 4x."},
    {"phase": "substitute", "pre": "3 + 4 = ", "post": "x", "answer": 7, "hint": "Add the two middle coefficients."},
    {"phase": "substitute", "pre": "So the expansion is x² + 7x + ", "post": "", "answer": 12, "hint": "The last term you worked out."},
    {"say": "Check by putting x = 1 into the original brackets.", "pre": "(1+4)(1+3) = 5 × 4 = ", "post": "", "answer": 20, "hint": "Work out each bracket at x = 1, then multiply."},
    {"pre": "and 1 + 7 + 12 = ", "post": "", "answer": 20, "done": "Both give 20, so x² + 7x + 12 is right.", "hint": "Add the three terms at x = 1."},
]

pb["gold"][0]["guided_steps"] = [
    {"say": "FOIL. First is 3x × 2x = 6x², the x² term. Now the Outer and Inner products."},
    {"pre": "Outer: 3x × 5 = ", "post": "x", "answer": 15, "hint": "Multiply 3x by 5."},
    {"pre": "Inner: −2 × 2x = ", "post": "x", "answer": -4, "hint": "Multiply −2 by 2x and keep the minus."},
    {"pre": "Last: −2 × 5 = ", "post": "", "answer": -10, "hint": "Multiply −2 by 5."},
    {"say": "Collect the two middle terms: 15x and −4x."},
    {"phase": "substitute", "pre": "15 + (−4) = ", "post": "x", "answer": 11, "hint": "Add the two middle coefficients."},
    {"phase": "substitute", "pre": "So the expansion is 6x² + 11x + ", "post": "", "answer": -10, "hint": "The last term you worked out, with its sign."},
    {"say": "Check by putting x = 1 into the original brackets.", "pre": "(3−2)(2+5) = 1 × 7 = ", "post": "", "answer": 7, "hint": "Work out each bracket at x = 1, then multiply."},
    {"pre": "and 6 + 11 − 10 = ", "post": "", "answer": 7, "done": "Both give 7, so 6x² + 11x − 10 is right.", "hint": "Add the three terms at x = 1."},
]

pb["gold"][3]["guided_steps"] = [
    {"say": "Expand each square fully, keeping the middle term. Start with \\((x+4)^2\\)."},
    {"pre": "Middle term of (x+4)²: 2 × 4 = ", "post": "x", "answer": 8, "hint": "The middle term is 2 times the number inside."},
    {"pre": "Constant of (x+4)²: 4 × 4 = ", "post": "", "answer": 16, "hint": "Square the number inside."},
    {"say": "So \\((x+4)^2 = x^2 + 8x + 16\\). Now \\((x+2)^2\\)."},
    {"pre": "Middle term of (x+2)²: 2 × 2 = ", "post": "x", "answer": 4, "hint": "The middle term is 2 times the number inside."},
    {"pre": "Constant of (x+2)²: 2 × 2 = ", "post": "", "answer": 4, "hint": "Square the number inside."},
    {"say": "Subtract: \\((x^2 + 8x + 16) - (x^2 + 4x + 4)\\). The x² terms cancel.", "phase": "substitute", "pre": "x terms: 8 − 4 = ", "post": "x", "answer": 4, "hint": "Subtract the middle coefficients."},
    {"phase": "substitute", "pre": "constants: 16 − 4 = ", "post": "", "answer": 12, "hint": "Subtract the constants."},
    {"say": "So it simplifies to 4x + 12, which matches ax + b."},
    {"pre": "The question asks for a, the number in front of x. a = ", "post": "", "answer": 4, "done": "a = 4 (and b would be 12).", "hint": "Read off the coefficient of x."},
]

# ---- tier_guides ----
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one bracket",
        "steps": [
            "A single bracket like \\(3(x + 4)\\) means 3 times everything inside. Multiply the outside term by <strong>each</strong> term in the bracket.",
            "Keep the signs. A negative outside, or a minus inside, changes the sign of that term: \\(3 × 4 = 12\\) but \\(-3 × 4 = -12\\).",
            "One bracket has nothing to collect. If two brackets are added, expand both, then combine the like terms.",
        ],
        "example": {
            "question": "Expand \\(4(2x - 3)\\)",
            "steps": [
                {"label": "Multiply the first term", "content": "<p>\\(4 × 2x = 8x\\)</p>"},
                {"label": "Multiply the second term", "content": "<p>\\(4 × (-3) = -12\\)</p>"},
                {"label": "Check with x = 1", "content": "<p>\\(4(2 - 3) = 4 × (-1) = -4\\), and \\(8 - 12 = -4\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(8x - 12\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: two brackets",
        "steps": [
            "Two brackets multiplied, like \\((x + 4)(x + 3)\\), need <strong>FOIL</strong>: First, Outer, Inner, Last. Every term in the first bracket multiplies every term in the second.",
            "That gives four terms. The two middle ones are like terms, so add them: \\(3x + 4x = 7x\\).",
            "Watch the signs. A minus inside a bracket travels through every product it touches.",
        ],
        "example": {
            "question": "Expand and simplify \\((x + 2)(x + 5)\\)",
            "steps": [
                {"label": "First", "content": "<p>\\(x × x = x^2\\)</p>"},
                {"label": "Outer and Inner", "content": "<p>\\(5x + 2x = 7x\\)</p>"},
                {"label": "Last", "content": "<p>\\(2 × 5 = 10\\)</p>"},
                {"label": "Check with x = 1", "content": "<p>\\((3)(6) = 18\\), and \\(1 + 7 + 10 = 18\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(x^2 + 7x + 10\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: squares, surds and triples",
        "steps": [
            "Squaring is FOIL with itself: \\((x + 6)^2 = x^2 + 12x + 36\\). The middle term \\(2 × 6 × x\\) is the one people drop.",
            "Difference of two squares: \\((a + b)(a - b) = a^2 - b^2\\). The middle terms cancel, so no \\(x\\) term is left.",
            "For triple brackets, expand two first, then multiply the result by the third, collecting like terms at each stage.",
        ],
        "example": {
            "question": "Expand \\((x + 5)^2\\)",
            "steps": [
                {"label": "First", "content": "<p>\\(x × x = x^2\\)</p>"},
                {"label": "Middle (twice)", "content": "<p>\\(2 × 5 × x = 10x\\)</p>"},
                {"label": "Last", "content": "<p>\\(5 × 5 = 25\\)</p>"},
                {"label": "Check with x = 1", "content": "<p>\\((6)^2 = 36\\), and \\(1 + 10 + 25 = 36\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(x^2 + 10x + 25\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---- guided: opener (area model + SVG) + teach walks ----
opener_svg = (
    '<svg viewBox="0 0 260 116" role="img" aria-label="A rectangle 3 tall, split into a part 10 wide and a part 4 wide">'
    '<rect x="14" y="20" width="150" height="54" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    '<rect x="164" y="20" width="60" height="54" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    '<text x="89" y="51" font-family="Inter, sans-serif" font-size="12" text-anchor="middle" fill="currentColor">3 × 10</text>'
    '<text x="194" y="51" font-family="Inter, sans-serif" font-size="12" text-anchor="middle" fill="currentColor">3 × 4</text>'
    '<text x="89" y="92" font-family="Inter, sans-serif" font-size="11" text-anchor="middle" fill="currentColor">10</text>'
    '<text x="194" y="92" font-family="Inter, sans-serif" font-size="11" text-anchor="middle" fill="currentColor">4</text>'
    '<text x="6" y="51" font-family="Inter, sans-serif" font-size="11" text-anchor="middle" fill="currentColor">3</text>'
    '</svg>'
)

pd["guided"] = {
    "opener": {
        "label": "Before any algebra",
        "display": opener_svg + "<br>A rectangle 3 tall is split into a part 10 wide and a part 4 wide.",
        "steps": [
            {"say": "Area is just width × height, and a split rectangle's total is its parts added up. Take the left block first: 3 tall, 10 wide.",
             "pre": "Left block area = 3 × 10 = ", "post": "", "answer": 30, "hint": "Three rows of ten."},
            {"say": None, "pre": "Right block area = 3 × 4 = ", "post": "", "answer": 12, "hint": "Three rows of four."},
            {"say": "Add the two parts to get the whole rectangle.",
             "pre": "30 + 12 = ", "post": "", "answer": 42, "hint": "Put the two areas together."},
            {"say": "Multiplying the whole width at once, 3 × 14, also gives 42. Splitting then adding matches multiplying. Now swap the 10 for \\(x\\) and the SAME rule expands the bracket: \\(3(x + 4) = 3x + 12\\). The 3 multiplies each part inside. That is all expanding a bracket is."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Expand \\(4(x + 5)\\)",
            "label": "Together: your first one",
            "steps": [
                {"say": "The 4 multiplies each term inside, one at a time.",
                 "pre": "4 × x = ", "post": "x", "answer": 4, "hint": "Multiply the number in front."},
                {"pre": "4 × 5 = ", "post": "", "answer": 20, "hint": "Multiply the 4 by the 5."},
                {"say": "So \\(4(x + 5) = 4x + 20\\). Check it by putting x = 1 into both forms.",
                 "pre": "4(1 + 5) = 4 × 6 = ", "post": "", "answer": 24, "hint": "Work out the bracket first, then multiply."},
                {"pre": "and 4 × 1 + 20 = ", "post": "", "answer": 24, "done": "Both give 24, so the expansion is right.", "hint": "Put x = 1 into 4x + 20."},
            ],
        },
        "silver": {
            "display": "Expand and simplify \\((x + 2)(x + 5)\\)",
            "label": "Together: the silver move",
            "steps": [
                {"say": "FOIL. First is x × x = x², the x² term. Now the Outer and Inner products.",
                 "pre": "Outer: x × 5 = ", "post": "x", "answer": 5, "hint": "Multiply the first x by the 5."},
                {"pre": "Inner: 2 × x = ", "post": "x", "answer": 2, "hint": "Multiply the 2 by the x."},
                {"pre": "Last: 2 × 5 = ", "post": "", "answer": 10, "hint": "Multiply the two numbers."},
                {"say": "Collect the middle terms: 5x + 2x.",
                 "pre": "5 + 2 = ", "post": "x", "answer": 7, "hint": "Add the two middle coefficients."},
                {"say": "So \\(x^2 + 7x + 10\\). Check with x = 2.",
                 "pre": "(2 + 2)(2 + 5) = 4 × 7 = ", "post": "", "answer": 28, "hint": "Work out each bracket at x = 2, then multiply."},
                {"pre": "and 4 + 14 + 10 = ", "post": "", "answer": 28, "done": "Both give 28, so it checks out.", "hint": "Put x = 2 into x² + 7x + 10."},
            ],
        },
        "gold": {
            "display": "Expand \\((x + 6)^2\\)",
            "label": "Together: the gold move",
            "steps": [
                {"say": "Squaring means \\((x + 6)(x + 6)\\). First is x × x = x². The trap is the middle term, so watch it.",
                 "pre": "Middle term: 2 × 6 = ", "post": "x", "answer": 12, "hint": "There are two lots of x × 6, so double the 6."},
                {"pre": "Last: 6 × 6 = ", "post": "", "answer": 36, "hint": "Square the 6."},
                {"say": "So \\(x^2 + 12x + 36\\). Check with x = 1.",
                 "pre": "(1 + 6)² = 7 × 7 = ", "post": "", "answer": 49, "hint": "Work out the bracket first, then square it."},
                {"pre": "and 1 + 12 + 36 = ", "post": "", "answer": 49, "done": "Both give 49. The middle term 12x is what most people drop.", "hint": "Put x = 1 into x² + 12x + 36."},
            ],
        },
    },
}

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT)
raw = io.open(OUT, encoding="utf-8").read()
print("em dashes:", raw.count("—"))
