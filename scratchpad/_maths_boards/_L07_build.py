# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_L07_live.json", encoding="utf-8"))
pd = live["practice_data"]
pb = pd["problem_bank"]

MINUS = "−"  # true minus sign

# ---------------------------------------------------------------------------
# method_card (slim reference)
# ---------------------------------------------------------------------------
pd["method_card"] = {
    "title": "Indices, Surds and Bounds",
    "steps": [
        "Multiplying: add the indices. Dividing: subtract. Power of a power: multiply.",
        "Fractional index: the bottom is the root, the top is the power. Root first.",
        "Surd: pull out the biggest square factor; rationalise by multiplying by the surd.",
        "Bound: a rounded value hides half a unit each side.",
    ],
    "content": (
        "<p><strong>Index laws:</strong> \\(a^{m}\\times a^{n}=a^{m+n}\\), "
        "\\(a^{m}\\div a^{n}=a^{m-n}\\), \\((a^{m})^{n}=a^{mn}\\), "
        "\\(a^{1/n}=\\sqrt[n]{a}\\), \\(a^{-n}=\\frac{1}{a^{n}}\\).</p>"
        "<p><strong>Surds:</strong> simplify with the biggest square factor, so "
        "\\(\\sqrt{72}=6\\sqrt2\\). Rationalise \\(\\frac{a}{\\sqrt b}\\) by "
        "multiplying top and bottom by \\(\\sqrt b\\).</p>"
        "<p><strong>Bounds:</strong> for 1 d.p. the half unit is 0.05, so "
        "\\(6.4\\) lies in \\(6.35\\le x<6.45\\).</p>"
    ),
    "example": (
        "<p><strong>Simplify</strong> \\(\\frac{6}{\\sqrt3}\\)</p>"
        "<p>Multiply top and bottom by \\(\\sqrt3\\): "
        "\\(\\frac{6\\sqrt3}{3}=2\\sqrt3\\).</p>"
    ),
}

# ---------------------------------------------------------------------------
# helper to set a problem's fields
# ---------------------------------------------------------------------------
def setp(tier, i, **kw):
    p = pb[tier][i]
    for k, v in kw.items():
        p[k] = v
    return p

# ===========================================================================
# BRONZE
# ===========================================================================
# [0] 3^2 x 3^4 -> power 6
setp("bronze", 0,
    hint="Same base, so add the indices when multiplying.",
    misconceptions=[{
        "pattern": "multiply_indices", "check": "multiply_indices", "expect": 8,
        "message": "Multiplying powers ADDS the indices, it does not multiply them. 2 + 4 = 6, so the answer is 3⁶.",
    }],
    guided_steps=[
        {"say": "Same base 3, so multiplying means ADD the indices: \\(3^{2}\\times3^{4}=3^{2+4}\\)."},
        {"pre": "As numbers, 3² × 3⁴ = 9 × 81 = ", "answer": 729, "hint": "Nine times eighty-one."},
        {"pre": "By the law, add the indices: 2 + 4 = ", "answer": 6, "hint": "Add the two small numbers.", "phase": "substitute"},
        {"pre": "Check: 3⁶ = ", "answer": 729, "hint": "3 to the power 6.", "done": "3⁶ = 729, so the power is 6."},
    ])

# [1] 5^7 / 5^3 -> power 4
setp("bronze", 1,
    hint="Same base, so subtract the indices when dividing.",
    misconceptions=[{
        "pattern": "add_indices", "check": "add_indices", "expect": 10,
        "message": "Dividing powers SUBTRACTS the indices. 7 − 3 = 4, so the answer is 5⁴, not 5¹⁰.",
    }],
    guided_steps=[
        {"say": "Same base 5, so dividing means SUBTRACT the indices: \\(5^{7}\\div5^{3}=5^{7-3}\\)."},
        {"pre": "Write the top index (from 5⁷): ", "answer": 7, "hint": "The small number in 5⁷."},
        {"pre": "Subtract the bottom index 3: 7 − 3 = ", "answer": 4, "hint": "Take 3 away from 7.", "phase": "substitute"},
        {"pre": "So 5⁷ ÷ 5³ = 5⁴. Count check: 7 − 3 = ", "answer": 4, "hint": "Confirm the subtraction.", "done": "Four 5s remain, so the power is 4."},
    ])

# [2] change (2^3)^2 -> (2^4)^2 to break duplicate; power 8
setp("bronze", 2,
    display="Simplify \\((2^4)^2\\). Give the power of 2.",
    solutions=[8],
    hint="A power raised to a power: multiply the indices.",
    misconceptions=[{
        "pattern": "add_not_multiply", "check": "add_not_multiply", "expect": 6,
        "message": "A power of a power MULTIPLIES the indices. 4 × 2 = 8, so the answer is 2⁸, not 2⁶.",
    }],
    guided_steps=[
        {"say": "A power raised to a power MULTIPLIES the indices: \\((2^{4})^{2}=2^{4\\times2}\\)."},
        {"pre": "First work out 2⁴ = ", "answer": 16, "hint": "2 × 2 × 2 × 2."},
        {"pre": "Now (2⁴)² = 16², and as a power of 2 the index is 4 × 2 = ", "answer": 8, "hint": "Multiply the indices.", "phase": "substitute"},
        {"pre": "Check: 16² = 256 and 2⁸ = ", "answer": 256, "hint": "2 to the power 8.", "done": "Both give 256, so the power is 8."},
    ])

# [3] change 16^(1/2) -> 49^(1/2) to break duplicate; = 7
setp("bronze", 3,
    display="Evaluate \\(49^{\\frac{1}{2}}\\).",
    solutions=[7],
    hint="A power of a half means take the square root.",
    misconceptions=[{
        "pattern": "halve", "check": "halve", "expect": 24.5,
        "message": "A power of a half means square root, not halving. Half of 49 is 24.5, but the square root of 49 is 7.",
    }],
    guided_steps=[
        {"say": "A power of a half means a square root, so read \\(49^{1/2}\\) as \\(\\sqrt{49}\\)."},
        {"pre": "Which number squared makes 49? Try 7: 7 × 7 = ", "answer": 49, "hint": "Multiply 7 by itself."},
        {"pre": "That lands on 49, so √49 = ", "answer": 7, "hint": "The number you just squared.", "phase": "substitute"},
        {"pre": "Check by squaring: 7 × 7 = ", "answer": 49, "hint": "Multiply 7 by itself once more.", "done": "Squares back to 49, so 49^(1/2) = 7."},
    ])

# [4] 27^(1/3) = 3
setp("bronze", 4,
    hint="A power of a third means take the cube root.",
    misconceptions=[{
        "pattern": "divide_by_3", "check": "divide_by_3", "expect": 9,
        "message": "A power of a third is a cube root, not dividing by 3. The cube root of 27 is 3 because 3 × 3 × 3 = 27.",
    }],
    guided_steps=[
        {"say": "A power of a third means a cube root: which number cubed gives 27?"},
        {"pre": "Try 3: 3 × 3 × 3 = ", "answer": 27, "hint": "Multiply 3 by itself twice."},
        {"pre": "That lands on 27, so ∛27 = ", "answer": 3, "hint": "The number you just cubed.", "phase": "substitute"},
        {"pre": "Check: 3 × 3 × 3 = ", "answer": 27, "hint": "Cube the 3 once more.", "done": "Rebuilds 27, so 27^(1/3) = 3."},
    ])

# [5] mass 45 g nearest gram, LB = 44.5
setp("bronze", 5,
    hint="Nearest gram means a half unit of 0.5; take it off for the lower bound.",
    misconceptions=[{
        "pattern": "wrong_half", "check": "wrong_half", "expect": 44,
        "message": "The half unit is 0.5, not 1. Lower bound = 45 − 0.5 = 44.5.",
    }],
    guided_steps=[
        {"say": "Nearest gram means rounded to the nearest 1, so the true value can be up to half of 1 away."},
        {"pre": "Half unit = 1 ÷ 2 = ", "answer": 0.5, "hint": "Split 1 in two."},
        {"pre": "Lower bound = 45 − 0.5 = ", "answer": 44.5, "hint": "Take the half unit off.", "phase": "substitute"},
        {"pre": "Check the gap: 45 − 44.5 = ", "answer": 0.5, "hint": "Subtract to see the distance.", "done": "Exactly half a unit below, so the lower bound is 44.5 g."},
    ])

# [6] mass 45 g nearest gram, UB = 45.5
setp("bronze", 6,
    hint="Nearest gram means a half unit of 0.5; add it on for the upper bound.",
    misconceptions=[{
        "pattern": "wrong_half", "check": "wrong_half", "expect": 46,
        "message": "The half unit is 0.5, not 1. Upper bound = 45 + 0.5 = 45.5.",
    }],
    guided_steps=[
        {"say": "Nearest gram means rounded to the nearest 1, so the true value can be up to half of 1 away."},
        {"pre": "Half unit = 1 ÷ 2 = ", "answer": 0.5, "hint": "Split 1 in two."},
        {"pre": "Upper bound = 45 + 0.5 = ", "answer": 45.5, "hint": "Add the half unit on.", "phase": "substitute"},
        {"pre": "Check the gap: 45.5 − 45 = ", "answer": 0.5, "hint": "Subtract to see the distance.", "done": "Exactly half a unit above, so the upper bound is 45.5 g."},
    ])

# [7] 7^0 = 1
setp("bronze", 7,
    hint="Any non-zero number to the power 0 is 1.",
    misconceptions=[{
        "pattern": "zero_power", "check": "equals_0", "expect": 0,
        "message": "Any non-zero number to the power 0 is 1, not 0.",
    }],
    guided_steps=[
        {"say": "Anything except 0 to the power 0 equals 1. See why with the division law."},
        {"pre": "7⁰ equals 7² ÷ 7². The top is 49, so 49 ÷ 49 = ", "answer": 1, "hint": "Any number divided by itself."},
        {"pre": "By the index law, 2 − 2 = 0, and 7⁰ = ", "answer": 1, "hint": "The value you just found.", "phase": "substitute"},
        {"pre": "Check with 5⁰: 5 ÷ 5 = ", "answer": 1, "hint": "A number over itself.", "done": "Every non-zero base to the power 0 is 1."},
    ])

# ===========================================================================
# SILVER
# ===========================================================================
# [0] MC sqrt50 -> 5 sqrt2 (idx0). Options already distinct. Add hint + misc.
setp("silver", 0,
    hint="Split 50 into 25 × 2 and take the square root of 25.",
    misconceptions=[{
        "pattern": "no_root_of_factor", "check": "wrong", "expect": 2,
        "message": "√50 = √25 × √2. The √25 becomes 5, not 25. Answer: 5√2.",
    }])

# [1] MC sqrt72 -> 6 sqrt2. FIX degenerate distractors.
setp("silver", 1,
    options=["\\(6\\sqrt{2}\\)", "\\(36\\sqrt{2}\\)", "\\(6\\sqrt{3}\\)", "\\(8\\sqrt{3}\\)"],
    solutions=[0],
    hint="The biggest square factor of 72 is 36. Take its square root.",
    misconceptions=[{
        "pattern": "no_root_of_factor", "check": "wrong", "expect": 1,
        "message": "√72 = √36 × √2. The √36 becomes 6, not 36. Answer: 6√2.",
    }])

# [2] 8^(2/3) = 4
setp("silver", 2,
    hint="Take the cube root of 8 first, then square the result.",
    misconceptions=[
        {"pattern": "stop_at_root", "check": "wrong", "expect": 2,
         "message": "You found the cube root, ∛8 = 2, but stopped. The top number 2 means square it: 2² = 4."},
        {"pattern": "multiply_fraction", "check": "wrong", "expect": None,
         "message": "Do not multiply 8 by two thirds. Take the cube root first (2), then square it: 2² = 4."},
    ],
    guided_steps=[
        {"say": "The bottom of the fraction is the root, the top is the power. Do the root first."},
        {"pre": "Cube root first: ∛8 = ", "answer": 2, "hint": "Which number cubed gives 8?"},
        {"pre": "Now the power 2: 2² = ", "answer": 4, "hint": "2 × 2.", "phase": "substitute"},
        {"pre": "Rebuild the root: 2 × 2 × 2 = ", "answer": 8, "hint": "Cube the 2.", "done": "∛8 = 2 confirmed, so 8^(2/3) = 4."},
    ])

# [3] 2^-3 = 1/8 (fraction)
setp("silver", 3,
    hint="A negative power means one over the positive power, so find 2 cubed first.",
    misconceptions=[
        {"pattern": "negative_answer", "check": "wrong", "expect": -8,
         "message": "A negative index means a reciprocal, not a negative answer. 2⁻³ = 1/2³ = 1/8."},
        {"pattern": "forgot_flip", "check": "wrong", "expect": 8,
         "message": "The negative sign flips it to a fraction. 2³ = 8, and the flip gives 1/8, not 8."},
    ],
    guided_steps=[
        {"say": "A negative power flips it: \\(2^{-3}=\\frac{1}{2^{3}}\\)."},
        {"pre": "First the bottom: 2³ = 2 × 2 × 2 = ", "answer": 8, "hint": "Multiply 2 by itself twice."},
        {"pre": "The flip puts 1 on top. Numerator = ", "answer": 1, "hint": "A reciprocal always has 1 on top.", "phase": "substitute"},
        {"pre": "Denominator = ", "answer": 8, "hint": "It is the 2 cubed you just found.", "done": "So 2⁻³ = 1/8."},
    ])

# [4] MC sqrt12 + sqrt27 -> 5 sqrt3 (idx0). Options distinct.
setp("silver", 4,
    hint="Simplify each surd to a multiple of √3, then add.",
    misconceptions=[{
        "pattern": "add_under_root", "check": "wrong", "expect": 2,
        "message": "You cannot add under the root. √12 = 2√3 and √27 = 3√3, so the sum is 5√3.",
    }])

# [5] length 6.4 cm (1 d.p.) UB = 6.45
setp("silver", 5,
    hint="For 1 decimal place the half unit is 0.05; add it on for the upper bound.",
    misconceptions=[
        {"pattern": "wrong_half_unit", "check": "wrong", "expect": 6.5,
         "message": "Half a unit for 1 decimal place is 0.05, not 0.1. Upper bound is 6.4 + 0.05 = 6.45."},
        {"pattern": "half_of_1", "check": "wrong", "expect": 6.9,
         "message": "The half unit is 0.05, not 0.5. Upper bound is 6.4 + 0.05 = 6.45."},
    ],
    guided_steps=[
        {"say": "1 d.p. means rounded to the nearest 0.1, so the true value can be up to half of 0.1 away."},
        {"pre": "Half unit = 0.1 ÷ 2 = ", "answer": 0.05, "hint": "Split 0.1 in two."},
        {"pre": "Upper bound = 6.4 + 0.05 = ", "answer": 6.45, "hint": "Add the half unit on.", "phase": "substitute"},
        {"pre": "Check the gap: 6.45 − 6.4 = ", "answer": 0.05, "hint": "Subtract to see the distance.", "done": "Exactly half a unit above, so the upper bound is 6.45 cm."},
    ])

# [6] 125^(2/3) = 25
setp("silver", 6,
    hint="Take the cube root of 125 first, then square the result.",
    misconceptions=[
        {"pattern": "stop_at_root", "check": "wrong", "expect": 5,
         "message": "You found the cube root, ∛125 = 5, but stopped. The top number 2 means square it: 5² = 25."},
        {"pattern": "multiply_fraction", "check": "wrong", "expect": None,
         "message": "Do not multiply 125 by two thirds. Take the cube root first (5), then square it: 5² = 25."},
    ],
    guided_steps=[
        {"say": "The bottom of the fraction is the root, the top is the power. Do the root first."},
        {"pre": "Cube root first: ∛125 = ", "answer": 5, "hint": "Which number cubed gives 125?"},
        {"pre": "Now the power 2: 5² = ", "answer": 25, "hint": "5 × 5.", "phase": "substitute"},
        {"pre": "Rebuild the root: 5 × 5 × 5 = ", "answer": 125, "hint": "Cube the 5.", "done": "∛125 = 5 confirmed, so 125^(2/3) = 25."},
    ])

# ===========================================================================
# GOLD
# ===========================================================================
# [0] MC rationalise 6/sqrt3 -> 2 sqrt3. FIX degenerate distractor 6sqrt3/3.
setp("gold", 0,
    options=["\\(2\\sqrt{3}\\)", "\\(6\\sqrt{3}\\)", "\\(2\\)", "\\(3\\sqrt{2}\\)"],
    solutions=[0],
    hint="Multiply top and bottom by √3, then divide the whole numbers by 3.",
    misconceptions=[{
        "pattern": "forgot_divide", "check": "wrong", "expect": 1,
        "message": "Multiply top and bottom by √3 to get 6√3/3. Now divide by 3: 2√3. Stopping at 6√3 forgets the ÷3.",
    }])

# [1] (sqrt20 + sqrt45)/sqrt5 = 5
setp("gold", 1,
    hint="Simplify √20 and √45 to multiples of √5, add, then divide by √5.",
    misconceptions=[
        {"pattern": "wrong_simplify", "check": "wrong", "expect": 11,
         "message": "√45 = √9 × √5 = 3√5, not 9√5. So the sum is 5√5 and dividing by √5 gives 5."},
        {"pattern": "add_under_root", "check": "wrong", "expect": None,
         "message": "You cannot add under the root. Simplify first: 2√5 + 3√5 = 5√5, then divide by √5 to get 5."},
    ],
    guided_steps=[
        {"say": "Simplify each surd to a multiple of \\(\\sqrt5\\), then divide."},
        {"pre": "√20 = √(4 × 5) = 2√5, so its coefficient is ", "answer": 2, "hint": "The square root of 4."},
        {"pre": "√45 = √(9 × 5) = 3√5, so its coefficient is ", "answer": 3, "hint": "The square root of 9."},
        {"pre": "Add them: 2√5 + 3√5 = 5√5. Divide by √5: 5√5 ÷ √5 = ", "answer": 5, "hint": "The √5 cancels, leaving the number in front.", "phase": "substitute"},
        {"pre": "Numeric check: (4.472 + 6.708) ÷ 2.236 = ", "answer": 5, "hint": "Add the roots, then divide by √5 ≈ 2.236.", "done": "It gives 5 exactly, so the answer is 5."},
    ])

# [2] rectangle 5.3 x 8.7 (1 d.p.) LB of area, 4 s.f. = 45.41  (calculator)
#     FIGURE: labelled rectangle (exam would print one).
rect_svg = (
    '<svg viewBox="0 0 260 175" role="img" aria-label="Rectangle 8.7 cm wide and 5.3 cm tall, area unknown" '
    'style="max-width:280px">'
    '<rect x="34" y="34" width="188" height="104" fill="#60a5fa" fill-opacity="0.3" '
    'stroke="currentColor" stroke-width="1.5"/>'
    '<text x="128" y="24" fill="currentColor" font-family="Inter,sans-serif" font-size="12" '
    'text-anchor="middle">8.7 cm</text>'
    '<text x="20" y="90" fill="currentColor" font-family="Inter,sans-serif" font-size="12" '
    'text-anchor="middle" transform="rotate(-90 20 90)">5.3 cm</text>'
    '<text x="128" y="92" fill="currentColor" font-family="Inter,sans-serif" font-size="13" '
    'text-anchor="middle">Area = ?</text>'
    '</svg>'
    '<span class="figure-caption">Diagram not drawn accurately</span>'
)
setp("gold", 2,
    display=(rect_svg +
        "The sides of a rectangle are \\(5.3\\) cm and \\(8.7\\) cm (both 1 d.p.). "
        "Find the lower bound of the area. Give to 4 s.f."),
    hint="The smallest area uses the lower bound of each side; round to 4 s.f. at the end.",
    misconceptions=[
        {"pattern": "use_given", "check": "wrong", "expect": 46.11,
         "message": "Using the given sizes 5.3 × 8.7 gives 46.11, but the lower bound uses the smaller sides: 5.25 × 8.65 = 45.41."},
        {"pattern": "wrong_half_unit", "check": "wrong", "expect": 39.36,
         "message": "The half unit for 1 d.p. is 0.05, not 0.5. Lower bounds are 5.25 and 8.65, giving 45.41."},
    ],
    guided_steps=[
        {"say": "Both sides are to 1 d.p., so each has a half unit of 0.05. The smallest area uses the smallest sides."},
        {"pre": "Lower bound of 5.3 = 5.3 − 0.05 = ", "answer": 5.25, "hint": "Take 0.05 off."},
        {"pre": "Lower bound of 8.7 = 8.7 − 0.05 = ", "answer": 8.65, "hint": "Take 0.05 off."},
        {"pre": "Smallest area = 5.25 × 8.65 = 45.4125, to 4 s.f. = ", "answer": 45.41, "hint": "Round 45.4125 to four significant figures.", "phase": "substitute"},
        {"pre": "For comparison, the rounded-value area 5.3 × 8.7 = ", "answer": 46.11, "hint": "Multiply the given sides.", "done": "45.41 is below 46.11, exactly as a lower bound should be."},
    ])

# [3] (3 + sqrt5)(3 - sqrt5) = 4
setp("gold", 3,
    hint="Use the difference of two squares: 3² − (√5)².",
    misconceptions=[
        {"pattern": "sign_slip", "check": "wrong", "expect": 14,
         "message": "The last term is −(√5)² = −5, not +5. So 9 − 5 = 4, not 9 + 5."},
        {"pattern": "square_surd_wrong", "check": "wrong", "expect": -16,
         "message": "(√5)² = 5, not 25. Squaring a square root removes it. So 9 − 5 = 4."},
    ],
    guided_steps=[
        {"say": "This is a difference of two squares: \\((a+b)(a-b)=a^{2}-b^{2}\\)."},
        {"pre": "First square: 3² = ", "answer": 9, "hint": "3 × 3."},
        {"pre": "Second square: (√5)² = ", "answer": 5, "hint": "A root squared is the number inside."},
        {"pre": "Subtract: 9 − 5 = ", "answer": 4, "hint": "Take 5 from 9.", "phase": "substitute"},
        {"pre": "Expand fully to check: 9 − 3√5 + 3√5 − 5 = ", "answer": 4, "hint": "The surd terms cancel, leaving 9 − 5.", "done": "The √5 terms cancel, so the answer is 4."},
    ])

# [4] 16^(3/4) / 2^3 = 1
setp("gold", 4,
    hint="Simplify 16^(3/4) to 2³ = 8, then divide by 2³.",
    misconceptions=[
        {"pattern": "wrong_root", "check": "wrong", "expect": 8,
         "message": "The bottom number 4 means the fourth root, which is 2, not the square root 4. Top = 2³ = 8, and 8 ÷ 8 = 1."},
        {"pattern": "multiply_index", "check": "wrong", "expect": 1.5,
         "message": "Do not multiply 16 by three quarters. The fourth root of 16 is 2, cubed is 8, and 8 ÷ 8 = 1."},
    ],
    guided_steps=[
        {"say": "Work the top first: \\(16^{3/4}\\) means the fourth root of 16, then cubed."},
        {"pre": "Fourth root: which number to the power 4 gives 16? 2 × 2 × 2 × 2 = ", "answer": 16, "hint": "Multiply 2 four times."},
        {"pre": "So 16^(1/4) = 2. Now cube it: 2³ = ", "answer": 8, "hint": "2 × 2 × 2."},
        {"pre": "The bottom is 2³ = 8. Divide: 8 ÷ 8 = ", "answer": 1, "hint": "A number over itself.", "phase": "substitute"},
        {"pre": "Check the top as a power of 2: 16^(3/4) = 2³ = 8, and bottom 2³ = ", "answer": 8, "hint": "Cube the 2.", "done": "Top and bottom are both 8, so the answer is 1."},
    ])

# ---------------------------------------------------------------------------
# tier descriptions
# ---------------------------------------------------------------------------
pb["bronze_description"] = "One law at a time: a single index rule, a simple root, or one rounded value's bound."
pb["silver_description"] = "Two linked steps: a root then a power, a surd simplified, or a bound with a half-unit calculation."
pb["gold_description"] = "Combine skills: rationalise or expand surds, negative or stacked indices, and bounds inside area calculations."

# ---------------------------------------------------------------------------
# tier_guides
# ---------------------------------------------------------------------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one index law or one bound",
        "steps": [
            "<strong>Multiplying?</strong> Same base, ADD the indices: \\(3^{2}\\times3^{4}=3^{6}\\). <strong>Dividing?</strong> SUBTRACT them: \\(5^{7}\\div5^{3}=5^{4}\\). A power of a power MULTIPLIES: \\((2^{4})^{2}=2^{8}\\).",
            "<strong>Fractional power means a root:</strong> \\(49^{1/2}=\\sqrt{49}=7\\) and \\(27^{1/3}=\\sqrt[3]{27}=3\\). Anything to the power 0 is 1.",
            "<strong>Bounds:</strong> a rounded value hides half a unit each side. To the nearest gram the half unit is 0.5, so 45 g lies between 44.5 g and 45.5 g.",
        ],
        "example": {
            "question": "Simplify \\(3^{2}\\times3^{4}\\), giving the power of 3.",
            "steps": [
                {"label": "Read the law", "content": "Same base, so add the indices: \\(3^{2}\\times3^{4}=3^{2+4}\\)."},
                {"label": "Add", "content": "\\(2+4=6\\), so the answer is \\(3^{6}\\)."},
                {"label": "Check", "content": "\\(3^{6}=729\\) and \\(9\\times81=729\\) too."},
                {"label": "Answer", "content": "<strong>6</strong>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: two linked steps",
        "steps": [
            "<strong>Root then power.</strong> For \\(a^{m/n}\\), take the \\(n\\)th root first, then raise to \\(m\\): \\(8^{2/3}=(\\sqrt[3]{8})^{2}=2^{2}=4\\). The root first keeps the numbers small.",
            "<strong>Simplify surds</strong> with the biggest square factor: \\(\\sqrt{72}=6\\sqrt{2}\\). A negative power flips to a fraction: \\(2^{-3}=\\frac{1}{8}\\).",
            "<strong>Bounds:</strong> for 1 d.p. the half unit is 0.05, so upper = value + 0.05 and lower = value − 0.05.",
        ],
        "example": {
            "question": "Evaluate \\(8^{\\frac{2}{3}}\\).",
            "steps": [
                {"label": "Root first", "content": "\\(\\sqrt[3]{8}=2\\)."},
                {"label": "Then the power", "content": "\\(2^{2}=4\\)."},
                {"label": "Check", "content": "\\(2^{3}=8\\), so the cube root of 8 really is 2."},
                {"label": "Answer", "content": "<strong>4</strong>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: combine the skills",
        "steps": [
            "<strong>Rationalise</strong> \\(\\frac{a}{\\sqrt b}\\) by multiplying top and bottom by \\(\\sqrt b\\), then simplify: \\(\\frac{6}{\\sqrt3}=\\frac{6\\sqrt3}{3}=2\\sqrt3\\).",
            "<strong>Add or expand surds</strong> after simplifying each: \\(\\frac{\\sqrt{20}+\\sqrt{45}}{\\sqrt5}=\\frac{5\\sqrt5}{\\sqrt5}=5\\). Use the difference of two squares for \\((3+\\sqrt5)(3-\\sqrt5)=4\\).",
            "<strong>Bounds in area:</strong> the smallest area multiplies the two lower bounds; the largest uses the two upper bounds.",
        ],
        "example": {
            "question": "Rationalise \\(\\frac{6}{\\sqrt3}\\).",
            "steps": [
                {"label": "Multiply", "content": "Multiply top and bottom by \\(\\sqrt3\\): \\(\\frac{6\\sqrt3}{3}\\)."},
                {"label": "Simplify", "content": "\\(6\\div3=2\\), so \\(\\frac{6}{\\sqrt3}=2\\sqrt3\\)."},
                {"label": "Check", "content": "\\((2\\sqrt3)^{2}=12\\) and \\((6/\\sqrt3)^{2}=36\\div3=12\\)."},
                {"label": "Answer", "content": "<strong>\\(2\\sqrt3\\)</strong>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# guided: opener + teach
# ---------------------------------------------------------------------------
pd["guided"] = {
    "opener": {
        "display": "A square patio is paved with square slabs.<br>Altogether it takes <strong>81 slabs</strong> to fill it, laid in a perfect square.",
        "steps": [
            {"say": "No algebra needed, just picture the square of slabs."},
            {"pre": "How many slabs run along one edge? ", "answer": 9, "hint": "Nine rows of nine make 81. What number times itself gives 81?"},
            {"say": "Going from the whole square back to one side is a <strong>square root</strong>. You just found \\(\\sqrt{81}=9\\) in your head. In index form a square root is a power of one half: \\(\\sqrt{81}=81^{1/2}\\). The bottom of the fraction says which root to take."},
            {"pre": "Now a cube built from 27 small blocks. How many lie along one edge? ", "answer": 3, "hint": "3 × 3 × 3 = 27. What number cubed gives 27?"},
            {"say": "That is a <strong>cube root</strong>: \\(\\sqrt[3]{27}=3\\), written \\(27^{1/3}\\). Roots and powers are the first strand of this lesson. Later you will tidy surds like \\(\\sqrt{72}\\) and handle rounded measurements, but it all begins with asking which number, multiplied by itself, gives this."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Evaluate \\(100^{\\frac{1}{2}}\\)",
            "label": "Together: your first one",
            "steps": [
                {"say": "A power of a half means a square root, so read \\(100^{1/2}\\) as \\(\\sqrt{100}\\)."},
                {"pre": "Which number squared makes 100? Try 9: 9 × 9 = ", "answer": 81, "hint": "Multiply 9 by itself."},
                {"pre": "A bit small, so try 10: 10 × 10 = ", "answer": 100, "hint": "Multiply 10 by itself."},
                {"pre": "It lands on 100, so √100 = ", "answer": 10, "hint": "The number you just squared."},
                {"pre": "Check by squaring: 10 × 10 = ", "answer": 100, "hint": "Multiply 10 by itself once more.", "done": "Gone. A half power is just a square root."},
            ],
        },
        "silver": {
            "display": "Evaluate \\(27^{\\frac{2}{3}}\\)",
            "label": "Together: the new move",
            "steps": [
                {"say": "Two moves. The bottom 3 is a cube root, the top 2 is a power. Root first."},
                {"pre": "Cube root first: ∛27 = ", "answer": 3, "hint": "Which number cubed gives 27?"},
                {"pre": "Now the power 2: 3² = ", "answer": 9, "hint": "3 × 3."},
                {"pre": "Check the root: 3 × 3 × 3 = ", "answer": 27, "hint": "Cube the 3 to rebuild 27."},
                {"pre": "So the answer is 27^(2/3) = ", "answer": 9, "hint": "The value after squaring.", "done": "Gone. Root first, then power: that is the silver move."},
            ],
        },
        "gold": {
            "display": "Rationalise \\(\\frac{10}{\\sqrt5}\\)",
            "label": "Together: the new move",
            "steps": [
                {"say": "Clear the surd on the bottom by multiplying top and bottom by \\(\\sqrt5\\)."},
                {"pre": "Bottom becomes √5 × √5 = ", "answer": 5, "hint": "A root times itself is the number inside."},
                {"pre": "Top becomes 10√5, so divide the whole numbers: 10 ÷ 5 = ", "answer": 2, "hint": "10 divided by 5."},
                {"pre": "So 10/√5 = 2√5. Check: (2√5)² = 4 × 5 = ", "answer": 20, "hint": "Square 2, then times 5."},
                {"pre": "And (10/√5)² = 100 ÷ 5 = ", "answer": 20, "hint": "Square 10, then divide by 5.", "done": "Both give 20, so 10/√5 = 2√5. Rationalising is the gold move."},
            ],
        },
    },
}

out = "lesson_maths-eduqas_number-L07.json"
json.dump(pd, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out)
print("bronze sols:", [p["solutions"] for p in pb["bronze"]])
print("silver sols:", [p["solutions"] for p in pb["silver"]])
print("gold sols:", [p["solutions"] for p in pb["gold"]])
