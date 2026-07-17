# -*- coding: utf-8 -*-
"""Full guided-learning + opener-figure conversion for maths-ocr number-L06
'Powers, Roots & Standard Form'. Fresh-solved every problem; repairs the one
validator-fatal duplicate (silver 16^(3/4)->81^(3/4)); adds guided_steps,
hints, tier_guides, opener (with SVG), teach walks; slims method_card;
preserves topic_links / related_videos / worked_examples."""
import json, io

SRC = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_numL06_ocr.json"
OUT = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_number-L06.json"

live = json.load(io.open(SRC, encoding="utf-8"))

# ---- preserved fields ----
topic_links = live["topic_links"]
related_videos = live["related_videos"]
worked_examples = live["worked_examples"]
# Preserved worked_examples carry legacy em dashes in step labels
# (e.g. "Step 1 — Expand"); the style law bans them. Minimal fix: em dash -> colon.
for we in worked_examples:
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---- slim method_card ----
method_card = {
    "title": "Powers, Roots & Standard Form",
    "steps": [
        "Power: aⁿ multiplies a by itself n times. Add indices to multiply, subtract to divide, multiply them for a power of a power.",
        "Root: √ undoes a square, ∛ undoes a cube. A fractional power a^(m/n) is the n-th root, then raised to the power m.",
        "Negative index means reciprocal: a⁻ⁿ = 1/aⁿ, and a⁰ = 1.",
        "Standard form: A × 10ⁿ with 1 ≤ A < 10. Combine the A values and the powers, then slide A back into range.",
    ],
    "content": (
        "<p><strong>Powers</strong> follow index laws: add indices to multiply, subtract "
        "to divide, and multiply them for a power of a power. \\(a^0 = 1\\) and a negative "
        "index means reciprocal. <strong>Roots</strong> undo powers, and a fractional power "
        "is a root then a power: do the root first. <strong>Standard form</strong> is "
        "\\(A \\times 10^n\\) with A between 1 and 10; count the places the point moves for "
        "n, negative for small numbers. To multiply or divide, combine the A values and the "
        "powers, then slide A back into range.</p>"
    ),
    "example": (
        "<p><strong>Write</strong> \\(0.00034\\) in standard form.</p>"
        "<p>Slide the point right to 3.4, moving 4 places, so n = −4.</p>"
        "<p>Answer: \\(3.4 \\times 10^{-4}\\).</p>"
    ),
}

# ================= PROBLEM BANK =================

bronze = [
    {
        "display": "Evaluate \\(3^4\\)",
        "solutions": [81],
        "calculator": False,
        "input_type": "single_value",
        "hint": "A power means repeated multiplying: 3⁴ is 3 × 3 × 3 × 3, not 3 × 4.",
        "misconceptions": [
            {"pattern": "multiply_base_power", "expect": 12,
             "message": "3⁴ means 3 × 3 × 3 × 3 = 81, not 3 × 4 = 12.", "note": "3*4=12"}
        ],
        "guided_steps": [
            {"say": "A power tells you how many of the base to multiply. 3⁴ is four 3s.",
             "pre": "3 × 3 = ", "post": "", "answer": 9, "hint": "Two 3s make 9."},
            {"phase": "substitute", "pre": "Now the third 3: 9 × 3 = ", "post": "",
             "answer": 27, "hint": "9 times 3."},
            {"phase": "substitute", "pre": "And the fourth: 27 × 3 = ", "post": "",
             "answer": 81, "done": "Four 3s multiplied give 81.", "hint": "27 times 3."},
        ],
    },
    {
        "display": "Evaluate \\(\\sqrt{144}\\)",
        "solutions": [12],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Ask what number times itself gives 144.",
        "misconceptions": [
            {"pattern": "half", "expect": 72,
             "message": "A square root is not halving. Ask what number times itself gives 144: that is 12.",
             "note": "144/2=72"}
        ],
        "guided_steps": [
            {"say": "A square root asks: what number times itself gives 144? Try 10.",
             "pre": "10 × 10 = ", "post": "", "answer": 100, "hint": "Ten squared."},
            {"say": "Too small, go higher. Try 12.", "phase": "substitute",
             "pre": "12 × 12 = ", "post": "", "answer": 144, "hint": "Twelve squared."},
            {"phase": "substitute", "pre": "So √144 = ", "post": "", "answer": 12,
             "done": "12 × 12 = 144, so the square root is 12.",
             "hint": "The number that squared to 144."},
        ],
    },
    {
        "display": "Evaluate \\(10^3\\)",
        "solutions": [1000],
        "calculator": False,
        "input_type": "single_value",
        "hint": "10³ is three 10s multiplied: count the zeros.",
        "misconceptions": [
            {"pattern": "multiply_base_power", "expect": 30,
             "message": "10³ = 10 × 10 × 10 = 1000, not 10 × 3 = 30.", "note": "10*3=30"}
        ],
        "guided_steps": [
            {"say": "10³ is three 10s multiplied.", "pre": "10 × 10 = ", "post": "",
             "answer": 100, "hint": "Ten squared."},
            {"phase": "substitute", "pre": "Now the third 10: 100 × 10 = ", "post": "",
             "answer": 1000, "hint": "100 times 10."},
            {"phase": "substitute", "pre": "The power 3 gives this many zeros: ", "post": "",
             "answer": 3, "done": "10³ = 1000, and the power equals the number of zeros.",
             "hint": "One zero for each 10."},
        ],
    },
    {
        "display": "Evaluate \\(\\sqrt[3]{27}\\)",
        "solutions": [3],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Ask what number cubed (times itself three times) gives 27.",
        "misconceptions": [
            {"pattern": "divide_by_3", "expect": 9,
             "message": "A cube root is not dividing by 3. Ask what number cubed gives 27: 3 × 3 × 3 = 27, so ∛27 = 3.",
             "note": "27/3=9"}
        ],
        "guided_steps": [
            {"say": "A cube root asks: what number cubed gives 27? Try 2.",
             "pre": "2 × 2 × 2 = ", "post": "", "answer": 8, "hint": "Two cubed."},
            {"say": "Too small. Try 3.", "phase": "substitute", "pre": "3 × 3 × 3 = ",
             "post": "", "answer": 27, "hint": "Three cubed."},
            {"phase": "substitute", "pre": "So ∛27 = ", "post": "", "answer": 3,
             "done": "3³ = 27, so the cube root is 3.",
             "hint": "The number that cubed to 27."},
        ],
    },
    {
        "display": "Write \\(56\\,000\\) in standard form",
        "solutions": [5.6, 4],
        "calculator": False,
        "input_type": "standard_form",
        "hint": "Make A between 1 and 10, then count the places the point moves.",
        "misconceptions": [
            {"pattern": "wrong_A", "expect": [56, 3],
             "message": "A must be between 1 and 10. Move the point 4 places to get 5.6 × 10⁴, not 56 × 10³.",
             "note": "stops at 56, n=3"}
        ],
        "guided_steps": [
            {"say": "Standard form is A × 10ⁿ with A between 1 and 10. Slide the point left until one non-zero digit sits in front.",
             "pre": "56000 becomes A = ", "post": "", "answer": 5.6,
             "hint": "5.6, with the point after the 5."},
            {"say": "Count how many places the point moved.", "phase": "substitute",
             "pre": "Places the point moved = ", "post": "", "answer": 4,
             "hint": "From 56000. to 5.6 is 4 hops left."},
            {"phase": "substitute", "pre": "Check: 5.6 × 10000 = ", "post": "",
             "answer": 56000, "done": "56000 = 5.6 × 10⁴, so A = 5.6 and n = 4.",
             "hint": "10⁴ is 10000."},
        ],
    },
    {
        "display": "Write \\(0.003\\) in standard form",
        "solutions": [3, -3],
        "calculator": False,
        "input_type": "standard_form",
        "hint": "Small numbers use a negative power; count the places right.",
        "misconceptions": [
            {"pattern": "positive_power", "expect": [3, 3],
             "message": "Small numbers have negative powers. 0.003 → 3 (move 3 places right), so n = −3: 3 × 10⁻³.",
             "note": "sign error, +3"}
        ],
        "guided_steps": [
            {"say": "Move the point right until one non-zero digit is in front. 0.003 becomes 3.",
             "pre": "A = ", "post": "", "answer": 3, "hint": "Just the digit 3."},
            {"say": "Count the places the point moved: 0.003 to 3.", "phase": "substitute",
             "pre": "Places moved = ", "post": "", "answer": 3, "hint": "Three hops right."},
            {"phase": "substitute", "pre": "Small number, so n is negative. n = ", "post": "",
             "answer": -3, "done": "0.003 = 3 × 10⁻³.",
             "hint": "Moving right means a negative power."},
        ],
    },
    {
        "display": "Evaluate \\(5^2 + 3^2\\)",
        "solutions": [34],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Square each number first, then add.",
        "misconceptions": [
            {"pattern": "add_then_square", "expect": 64,
             "message": "Square each first, then add: 25 + 9 = 34. Do not add 5 + 3 and then square.",
             "note": "8^2=64"}
        ],
        "guided_steps": [
            {"say": "Powers come before adding. Square each number first.",
             "pre": "5 × 5 = ", "post": "", "answer": 25, "hint": "Five squared."},
            {"say": "Now the other square.", "pre": "3 × 3 = ", "post": "", "answer": 9,
             "hint": "Three squared."},
            {"say": "Now add the two squares.", "phase": "substitute", "pre": "25 + 9 = ",
             "post": "", "answer": 34, "hint": "Add them."},
            {"phase": "substitute",
             "pre": "The trap is adding first: (5 + 3)² = 8² = 64. Our correct total is ",
             "post": "", "answer": 34, "done": "Square first, then add: 25 + 9 = 34, not 64.",
             "hint": "The squares-then-add answer."},
        ],
    },
    {
        "display": "Write \\(8.1 \\times 10^5\\) as an ordinary number",
        "solutions": [810000],
        "calculator": False,
        "input_type": "single_value",
        "hint": "10⁵ moves the point 5 places right.",
        "misconceptions": [
            {"pattern": "off_by_one_place", "expect": 8100000,
             "message": "10⁵ moves the point 5 places, giving 810000. 8100000 would be 10⁶.",
             "note": "one extra zero"}
        ],
        "guided_steps": [
            {"say": "10⁵ moves the decimal point 5 places to the right. First move:",
             "pre": "8.1 × 10 = ", "post": "", "answer": 81, "hint": "One place right."},
            {"phase": "substitute", "pre": "Now 4 more places (× 10000): 81 × 10000 = ",
             "post": "", "answer": 810000, "hint": "Add four zeros."},
            {"phase": "substitute", "pre": "Total places the point moved for 10⁵ = ", "post": "",
             "answer": 5, "done": "8.1 × 10⁵ = 810000.", "hint": "Five places for 10⁵."},
        ],
    },
]

silver = [
    {
        "display": "Simplify \\(2^3 \\times 2^5\\). Give your answer as a power of 2.",
        "solutions": [8],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Same base multiplied: add the indices.",
        "misconceptions": [
            {"pattern": "multiply_powers", "expect": 15,
             "message": "When multiplying with the same base, ADD the indices: 3 + 5 = 8, giving 2⁸.",
             "note": "3*5=15"}
        ],
        "guided_steps": [
            {"say": "Same base, so combine by counting the 2s. 2³ has three 2s.",
             "pre": "Number of 2s in 2³ = ", "post": "", "answer": 3, "hint": "The index 3."},
            {"say": "2⁵ has five 2s.", "pre": "Number of 2s in 2⁵ = ", "post": "",
             "answer": 5, "hint": "The index 5."},
            {"say": "Multiplying puts them together.", "phase": "substitute",
             "pre": "3 + 5 = ", "post": "", "answer": 8, "hint": "Add the indices."},
            {"phase": "substitute", "pre": "So the answer is 2 to the power ", "post": "",
             "answer": 8, "done": "Same base multiplied: add indices, 2³ × 2⁵ = 2⁸.",
             "hint": "The combined index."},
        ],
    },
    {
        "display": "Simplify \\(5^7 \\div 5^3\\). Give your answer as a power of 5.",
        "solutions": [4],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Same base divided: subtract the indices.",
        "misconceptions": [
            {"pattern": "add_powers", "expect": 10,
             "message": "When dividing with the same base, SUBTRACT the indices: 7 − 3 = 4, giving 5⁴.",
             "note": "adds instead: 7+3=10"}
        ],
        "guided_steps": [
            {"say": "Dividing cancels matching 5s. Seven on top, three underneath.",
             "pre": "Fives on top = ", "post": "", "answer": 7, "hint": "The index 7."},
            {"phase": "substitute", "pre": "Cancel the three underneath: 7 − 3 = ", "post": "",
             "answer": 4, "hint": "Subtract the indices."},
            {"phase": "substitute", "pre": "So the answer is 5 to the power ", "post": "",
             "answer": 4, "done": "Same base divided: subtract indices, 5⁷ ÷ 5³ = 5⁴.",
             "hint": "The leftover index."},
        ],
    },
    {
        "display": "Evaluate \\(4^{-2}\\). Give your answer as a fraction.",
        "solutions": [1, 16],
        "calculator": False,
        "input_type": "fraction",
        "hint": "A negative index means one over the positive power.",
        "misconceptions": [
            {"pattern": "times_index", "expect": [1, 8],
             "message": "The 2 still means squared: 4⁻² = 1/4² = 1/16, not 1/(4 × 2).",
             "note": "1/8 error"}
        ],
        "guided_steps": [
            {"say": "A negative index means 'one over'. Flip it: 4⁻² = 1 over 4². First find 4².",
             "pre": "4 × 4 = ", "post": "", "answer": 16, "hint": "Four squared."},
            {"phase": "substitute", "pre": "Put it under 1, so the numerator (top) is ",
             "post": "", "answer": 1, "hint": "A reciprocal has 1 on top."},
            {"phase": "substitute", "pre": "and the denominator (bottom) is ", "post": "",
             "answer": 16, "done": "4⁻² = 1/16.", "hint": "The 4² you found."},
        ],
    },
    {
        "display": "Calculate \\((4 \\times 10^3) \\times (3 \\times 10^5)\\)",
        "solutions": [1.2, 9],
        "calculator": False,
        "input_type": "standard_form",
        "hint": "Multiply the numbers, add the powers, then adjust if A reaches 10.",
        "misconceptions": [
            {"pattern": "no_adjust", "expect": [12, 8],
             "message": "4 × 3 = 12 is not between 1 and 10. Adjust: 12 × 10⁸ = 1.2 × 10⁹.",
             "note": "unadjusted 12x10^8"}
        ],
        "guided_steps": [
            {"say": "Multiply the numbers, add the powers. Numbers first.",
             "pre": "4 × 3 = ", "post": "", "answer": 12, "hint": "Twelve."},
            {"say": "Now the powers.", "pre": "3 + 5 = ", "post": "", "answer": 8,
             "hint": "Add the indices."},
            {"say": "So far 12 × 10⁸, but 12 is not between 1 and 10. Rewrite 12 as 1.2 × 10.",
             "phase": "substitute", "pre": "The new A is ", "post": "", "answer": 1.2,
             "hint": "12 = 1.2 × 10."},
            {"phase": "substitute", "pre": "That extra 10 lifts the power: 8 + 1 = ",
             "post": "", "answer": 9, "done": "1.2 × 10⁹.", "hint": "Add one to the power."},
        ],
    },
    {
        "display": "Evaluate \\(27^{1/3}\\)",
        "solutions": [3],
        "calculator": False,
        "input_type": "single_value",
        "hint": "A power of 1/3 is the cube root, not dividing by 3.",
        "misconceptions": [
            {"pattern": "divide", "expect": 9,
             "message": "a^(1/3) means the cube root, not ÷ 3. ∛27 = 3 because 3³ = 27.",
             "note": "27/3=9"}
        ],
        "guided_steps": [
            {"say": "A power of 1/3 means the cube root. What cubed gives 27? Try 3.",
             "pre": "3 × 3 × 3 = ", "post": "", "answer": 27, "hint": "Three cubed."},
            {"phase": "substitute", "pre": "That matches, so 27^(1/3) = ", "post": "",
             "answer": 3, "hint": "The cube root of 27."},
            {"phase": "substitute",
             "pre": "It is not ÷ 3 (that would give 9). The cube root is ", "post": "",
             "answer": 3, "done": "27^(1/3) = ∛27 = 3, not 27 ÷ 3.", "hint": "The cube root, 3."},
        ],
    },
    {
        "display": "Calculate \\((8 \\times 10^6) \\div (2 \\times 10^2)\\)",
        "solutions": [4, 4],
        "calculator": False,
        "input_type": "standard_form",
        "hint": "Divide the numbers, subtract the powers.",
        "misconceptions": [
            {"pattern": "add_powers", "expect": [4, 8],
             "message": "Dividing means SUBTRACT the powers: 6 − 2 = 4, giving 4 × 10⁴.",
             "note": "adds powers: 6+2=8"}
        ],
        "guided_steps": [
            {"say": "Divide the numbers, subtract the powers. Numbers first.",
             "pre": "8 ÷ 2 = ", "post": "", "answer": 4, "hint": "Four."},
            {"phase": "substitute", "pre": "Now the powers: 6 − 2 = ", "post": "",
             "answer": 4, "hint": "Subtract the indices."},
            {"phase": "substitute",
             "pre": "A is 4 (between 1 and 10), so no adjusting. The power n = ", "post": "",
             "answer": 4, "done": "4 × 10⁴.", "hint": "The power you found, 4."},
        ],
    },
    {
        "display": "Evaluate \\(81^{3/4}\\)",
        "solutions": [27],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Take the 4th root first, then cube the result.",
        "misconceptions": [
            {"pattern": "root_only", "expect": 3,
             "message": "After the 4th root you get 3, but the power 3 still applies: 3³ = 27.",
             "note": "forgot to cube"}
        ],
        "guided_steps": [
            {"say": "Do the root (bottom number) first. The bottom is 4, so take the 4th root of 81. What to the 4th power gives 81? Try 3.",
             "pre": "3 × 3 × 3 × 3 = ", "post": "", "answer": 81, "hint": "Three to the fourth."},
            {"say": "So the 4th root of 81 is 3. Now apply the top number, the power 3.",
             "phase": "substitute", "pre": "3³ = 3 × 3 × 3 = ", "post": "", "answer": 27,
             "hint": "Three cubed."},
            {"phase": "substitute", "pre": "So 81^(3/4) = ", "post": "", "answer": 27,
             "done": "Root first (⁴√81 = 3), then power (3³ = 27).", "hint": "The final value, 27."},
        ],
    },
]

gold = [
    {
        "display": "Calculate \\((6 \\times 10^4) \\times (5 \\times 10^{-2})\\)",
        "solutions": [3, 3],
        "calculator": False,
        "input_type": "standard_form",
        "hint": "Multiply the numbers, add the powers with their signs, then adjust A.",
        "misconceptions": [
            {"pattern": "no_adjust", "expect": [30, 2],
             "message": "30 is not between 1 and 10. Adjust: 30 × 10² = 3 × 10³.",
             "note": "unadjusted 30x10^2"},
            {"pattern": "sign", "expect": [3, 7],
             "message": "Add the indices with their signs: 4 + (−2) = 2, not 6.",
             "note": "4+2=6 then 30x10^6=3x10^7"},
        ],
        "guided_steps": [
            {"say": "Numbers first, then powers.", "pre": "6 × 5 = ", "post": "",
             "answer": 30, "hint": "Thirty."},
            {"say": "Add the powers, keeping the sign: 4 + (−2).", "pre": "4 + (−2) = ",
             "post": "", "answer": 2, "hint": "Four take away two."},
            {"say": "So far 30 × 10², but 30 is not between 1 and 10. Rewrite 30 as 3 × 10.",
             "phase": "substitute", "pre": "The new A is ", "post": "", "answer": 3,
             "hint": "30 = 3 × 10."},
            {"phase": "substitute", "pre": "The extra 10 lifts the power: 2 + 1 = ", "post": "",
             "answer": 3, "done": "3 × 10³.", "hint": "Add one to the power."},
        ],
    },
    {
        "display": "Simplify \\((3^2)^4\\). Give your answer as a power of 3.",
        "solutions": [8],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Power of a power: multiply the indices.",
        "misconceptions": [
            {"pattern": "add_powers", "expect": 6,
             "message": "For a power raised to a power, MULTIPLY the indices: 2 × 4 = 8, giving 3⁸.",
             "note": "2+4=6"}
        ],
        "guided_steps": [
            {"say": "(3²)⁴ means 3² written four times: 3² × 3² × 3² × 3². Same base, so add those indices.",
             "pre": "2 + 2 + 2 + 2 = ", "post": "", "answer": 8, "hint": "Four twos."},
            {"phase": "substitute", "pre": "That is the same as multiplying: 2 × 4 = ",
             "post": "", "answer": 8, "hint": "Index times index."},
            {"phase": "substitute", "pre": "So (3²)⁴ = 3 to the power ", "post": "",
             "answer": 8, "done": "Power of a power: multiply indices, 2 × 4 = 8.",
             "hint": "The combined index, 8."},
        ],
    },
    {
        "display": "Evaluate \\(125^{-2/3}\\). Give your answer as a fraction.",
        "solutions": [1, 25],
        "calculator": False,
        "input_type": "fraction",
        "hint": "Cube root, then square, then take the reciprocal for the negative sign.",
        "misconceptions": [
            {"pattern": "ignore_negative", "expect": [25, 1],
             "message": "The negative index means take the reciprocal: 125^(−2/3) = 1/25, not 25.",
             "note": "ignored sign: 25"},
            {"pattern": "times_two", "expect": [1, 10],
             "message": "The 2 on top means squared, not × 2: (∛125)² = 5² = 25, so the answer is 1/25.",
             "note": "5*2=10 then reciprocal 1/10"},
        ],
        "guided_steps": [
            {"say": "Take it in pieces. The bottom 3 means cube root: ∛125. What cubed gives 125? Try 5.",
             "pre": "5 × 5 × 5 = ", "post": "", "answer": 125, "hint": "Five cubed."},
            {"say": "So ∛125 = 5. The top 2 means square it.", "pre": "5 × 5 = ", "post": "",
             "answer": 25, "hint": "Five squared."},
            {"say": "The negative sign means take the reciprocal (1 over it).",
             "phase": "substitute", "pre": "The top of the fraction is ", "post": "",
             "answer": 1, "hint": "A reciprocal has 1 on top."},
            {"phase": "substitute", "pre": "The bottom of the fraction is ", "post": "",
             "answer": 25, "done": "125^(−2/3) = 1/25.", "hint": "The 25 you found."},
        ],
    },
    {
        "display": "Calculate \\((2 \\times 10^5) + (3.5 \\times 10^4)\\)",
        "solutions": [2.35, 5],
        "calculator": False,
        "input_type": "standard_form",
        "hint": "Rewrite both with the same power of ten before adding the A values.",
        "misconceptions": [
            {"pattern": "add_A_directly", "expect": [5.5, 5],
             "message": "Convert to the same power first: 2 × 10⁵ = 20 × 10⁴, then 20 + 3.5 = 23.5 × 10⁴ = 2.35 × 10⁵. Do not add 2 + 3.5 directly.",
             "note": "5.5x10^5 error"}
        ],
        "guided_steps": [
            {"say": "You cannot add until the powers match. Change 2 × 10⁵ into 10⁴ form: 2 × 10⁵ = 20 × 10⁴.",
             "pre": "So the A becomes 2 × 10 = ", "post": "", "answer": 20,
             "hint": "Drop one power, so A is ten times bigger."},
            {"say": "Now both are × 10⁴, so add the A parts.", "phase": "substitute",
             "pre": "20 + 3.5 = ", "post": "", "answer": 23.5, "hint": "Add the two A values."},
            {"say": "That gives 23.5 × 10⁴, but 23.5 is not between 1 and 10. Rewrite as 2.35 × 10.",
             "phase": "substitute", "pre": "New A = ", "post": "", "answer": 2.35,
             "hint": "23.5 = 2.35 × 10."},
            {"phase": "substitute", "pre": "The extra 10 lifts the power: 4 + 1 = ",
             "post": "", "answer": 5, "done": "2.35 × 10⁵.", "hint": "Add one to the power."},
        ],
    },
    {
        "display": "Evaluate \\(8^{2/3} \\times 4^{-1/2}\\). Give your answer as a fraction.",
        "solutions": [2, 1],
        "calculator": False,
        "input_type": "fraction",
        "hint": "Work out each power separately, then multiply.",
        "misconceptions": [
            {"pattern": "ignore_negative", "expect": [8, 1],
             "message": "The negative index makes 4^(−1/2) = 1/2, so multiply 4 × 1/2 = 2, not 4 × 2.",
             "note": "4*2=8"}
        ],
        "guided_steps": [
            {"say": "Work out each power separately. 8^(2/3): cube root first, ∛8 = 2, then square.",
             "pre": "2 × 2 = ", "post": "", "answer": 4, "hint": "∛8 = 2, then squared."},
            {"say": "Now 4^(−1/2): the 1/2 is a square root, √4 = 2, and the minus flips it to 1/2. Multiply the two results.",
             "phase": "substitute", "pre": "4 × 1/2 = ", "post": "", "answer": 2,
             "hint": "Half of 4."},
            {"phase": "substitute", "pre": "As a fraction that is 2/1, so the numerator is ",
             "post": "", "answer": 2, "hint": "2 whole."},
            {"phase": "substitute", "pre": "and the denominator is ", "post": "", "answer": 1,
             "done": "8^(2/3) × 4^(−1/2) = 4 × 1/2 = 2.", "hint": "Over 1."},
        ],
    },
]

problem_bank = {
    "bronze": bronze,
    "silver": silver,
    "gold": gold,
    "bronze_description": "Evaluate powers and roots, and write numbers in standard form.",
    "silver_description": "Apply the index laws, fractional and negative powers, and multiply or divide in standard form.",
    "gold_description": "Standard form arithmetic including adjusting A, and harder fractional-power calculations.",
}

# ================= TIER GUIDES =================

tier_guides = {
    "bronze": {
        "title": "Bronze: powers, roots and standard form basics",
        "steps": [
            "A power like 3⁴ means multiply the base by itself: 3 × 3 × 3 × 3 = 81. The small number (index) counts the copies, so 10³ = 1000.",
            "A root undoes a power. √144 asks what number squared gives 144 (12), and ∛27 asks what number cubed gives 27 (3).",
            "Standard form writes a number as A × 10ⁿ with A between 1 and 10. Slide the point to make A, then count the places moved: 56000 = 5.6 × 10⁴, and 0.003 = 3 × 10⁻³ (negative for small numbers).",
        ],
        "example": {
            "question": "Write 56000 in standard form",
            "steps": [
                {"label": "Find A", "content": "<p>Slide the point: 5.6</p>"},
                {"label": "Count moves", "content": "<p>4 places, and it is large so n = 4</p>"},
                {"label": "Check", "content": "<p>5.6 × 10000 = 56000 ✓</p>"},
                {"label": "Answer", "content": "<p><strong>5.6 × 10⁴</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: index laws and fractional powers",
        "steps": [
            "Same base multiplied? <strong>Add</strong> the indices: 2³ × 2⁵ = 2⁸. Same base divided? <strong>Subtract</strong> them: 5⁷ ÷ 5³ = 5⁴.",
            "A negative index means reciprocal: 4⁻² = 1/4² = 1/16, and any base to the power 0 is 1.",
            "A fractional power is a root: the bottom is the root, the top is the power. So 81^(3/4) = (⁴√81)³ = 3³ = 27. Do the root first to keep the numbers small.",
        ],
        "example": {
            "question": "Simplify 2³ × 2⁵ as a power of 2",
            "steps": [
                {"label": "Same base", "content": "<p>Multiplying, so add the indices</p>"},
                {"label": "Add", "content": "<p>3 + 5 = 8</p>"},
                {"label": "Check", "content": "<p>Eight 2s in total</p>"},
                {"label": "Answer", "content": "<p><strong>2⁸</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: standard form arithmetic and harder powers",
        "steps": [
            "Multiplying in standard form: multiply the A values and add the powers. Dividing: divide the A values and subtract the powers.",
            "If the new A is not between 1 and 10, adjust: 30 × 10² = 3 × 10³ (A ÷ 10, power + 1). Check this every time.",
            "Adding or subtracting? First rewrite so both have the SAME power of ten, then add the A values and adjust if needed.",
        ],
        "example": {
            "question": "Calculate (6 × 10⁴) × (5 × 10⁻²)",
            "steps": [
                {"label": "Numbers", "content": "<p>6 × 5 = 30</p>"},
                {"label": "Powers", "content": "<p>4 + (−2) = 2</p>"},
                {"label": "Adjust", "content": "<p>30 × 10² = 3 × 10³</p>"},
                {"label": "Answer", "content": "<p><strong>3 × 10³</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ================= GUIDED (opener + teach) =================

opener_svg = (
    '<svg viewBox="0 0 260 130" role="img" aria-label="The Sun at a distance of '
    '150 000 000 km from a small planet, the same as 1.5 times ten to the power 8 km">'
    '<circle cx="40" cy="55" r="22" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    '<line x1="64" y1="55" x2="216" y2="55" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 3"/>'
    '<text x="140" y="42" font-family="Inter, sans-serif" font-size="13" text-anchor="middle" fill="currentColor">150 000 000 km</text>'
    '<text x="140" y="78" font-family="Inter, sans-serif" font-size="12" text-anchor="middle" fill="currentColor">= 1.5 × 10⁸ km</text>'
    '<circle cx="226" cy="55" r="6" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    '</svg>'
)

guided = {
    "opener": {
        "label": "Before any formulas",
        "display": opener_svg,
        "steps": [
            {"say": "Big numbers are a pain to write with all their zeros. Look at 1000000 (a million). No formulas, just count.",
             "pre": "Number of zeros in 1000000 = ", "post": "", "answer": 6,
             "hint": "Count every 0 in 1000000."},
            {"say": "Each zero is one more 10 multiplied in, so a million is 10 to some power.",
             "pre": "A million = 10 to the power ", "post": "", "answer": 6,
             "hint": "One power for each zero."},
            {"say": "Now a number that does not start with 1. The Sun is 150000000 km away. We write one digit before the point (1.5), then slide the point back to the end. Count the hops.",
             "pre": "Places the point moves from 150000000 to 1.5 = ", "post": "", "answer": 8,
             "hint": "1.5, then 8 more places to reach 150000000."},
            {"say": "You just wrote 150000000 as <strong>1.5 × 10⁸</strong>. That shorthand is <strong>standard form</strong>: A × 10ⁿ, where A is between 1 and 10 and n is the number of places the point moves. This whole topic is powers of that kind: a power counts repeated multiplying, a root undoes a power, and standard form uses powers of ten to tame huge and tiny numbers."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Evaluate \\(4^3\\)",
            "label": "Together: your first one",
            "steps": [
                {"say": "4³ means three 4s multiplied. Start with two.",
                 "pre": "4 × 4 = ", "post": "", "answer": 16, "hint": "Four squared."},
                {"say": "Now the third 4.", "pre": "16 × 4 = ", "post": "", "answer": 64,
                 "hint": "16 times 4."},
                {"say": "See the trap: 4³ is not 4 × 3.", "pre": "4 × 3 = ", "post": "",
                 "answer": 12, "hint": "This is the WRONG route, just to see it."},
                {"say": "The real answer is the repeated multiply.", "pre": "So 4³ = ",
                 "post": "", "answer": 64,
                 "done": "Three 4s give 64, not 4 × 3 = 12. That is the whole idea of a power.",
                 "hint": "64."},
            ],
        },
        "silver": {
            "display": "Simplify \\(7^6 \\times 7^2 \\div 7^3\\). Give your answer as a power of 7.",
            "label": "Together: the silver move",
            "steps": [
                {"say": "Same base throughout, so just track the indices. Multiplying adds them.",
                 "pre": "6 + 2 = ", "post": "", "answer": 8, "hint": "Add for multiply."},
                {"say": "Dividing subtracts: now take away the 3.", "pre": "8 − 3 = ",
                 "post": "", "answer": 5, "hint": "Subtract for divide."},
                {"say": "So the single index is 5. The answer is 7 to the power ",
                 "pre": "Power = ", "post": "", "answer": 5, "hint": "The combined index."},
                {"say": "Check by counting: six 7s times two 7s is eight 7s, then cancel three.",
                 "pre": "8 − 3 = ", "post": "", "answer": 5,
                 "done": "Add then subtract indices: 7⁵. Gone.", "hint": "Five 7s left."},
            ],
        },
        "gold": {
            "display": "Calculate \\((5 \\times 10^7) \\times (4 \\times 10^{-3})\\)",
            "label": "Together: the gold move",
            "steps": [
                {"say": "Numbers first.", "pre": "5 × 4 = ", "post": "", "answer": 20,
                 "hint": "Twenty."},
                {"say": "Add the powers with their signs: 7 + (−3).", "pre": "7 + (−3) = ",
                 "post": "", "answer": 4, "hint": "Seven minus three."},
                {"say": "So far 20 × 10⁴, but 20 is not between 1 and 10. Rewrite 20 as 2 × 10.",
                 "pre": "New A = ", "post": "", "answer": 2, "hint": "20 = 2 × 10."},
                {"say": "The extra 10 lifts the power.", "pre": "4 + 1 = ", "post": "",
                 "answer": 5,
                 "done": "2 × 10⁵. Adjusting A when it reaches 10 or more is the gold move. Gone.",
                 "hint": "Add one to the power."},
            ],
        },
    },
}

# ================= ASSEMBLE =================

pd = {
    "method_card": method_card,
    "topic_links": topic_links,
    "problem_bank": problem_bank,
    "related_videos": related_videos,
    "worked_examples": worked_examples,
    "tier_guides": tier_guides,
    "guided": guided,
}

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written", OUT)
