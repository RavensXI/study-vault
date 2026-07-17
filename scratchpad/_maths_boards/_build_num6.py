# -*- coding: utf-8 -*-
"""Assemble the full guided-learning practice_data for maths-aqa number-L06
(Powers, Roots & Standard Form). Bank maths was fresh-solved and is correct;
this adds opener, teach walks, tier_guides, guided_steps, hints, misconception
expects, tier descriptions, a slim method_card, and one opener figure."""
import json, io

# ---- opener figure: 384000 with the three trailing zeros highlighted ----
OPENER_SVG = (
    '<div style="text-align:center"><svg viewBox="0 0 240 74" role="img" '
    'aria-label="The number 384000 with its three trailing zeros highlighted, '
    'showing three zeros make ten cubed">'
    '<text x="120" y="18" font-family="Inter, sans-serif" font-size="11" '
    'fill="currentColor" text-anchor="middle">Distance to the Moon (km)</text>'
    '<rect x="128" y="30" width="78" height="30" fill="#60a5fa" fill-opacity="0.3"/>'
    '<text x="120" y="51" font-family="Inter, sans-serif" font-size="22" '
    'fill="currentColor" text-anchor="middle" letter-spacing="3">384000</text>'
    '<text x="167" y="70" font-family="Inter, sans-serif" font-size="10" '
    'fill="currentColor" text-anchor="middle">3 zeros = ×10³</text>'
    '</svg></div>'
)

def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {}
    if say is not None:
        d["say"] = say
    d["pre"] = pre
    if post:
        d["post"] = post
    d["answer"] = answer
    d["hint"] = hint
    if phase:
        d["phase"] = phase
    if done:
        d["done"] = done
    return d

def say(text):
    return {"say": text}

def prob(display, solutions, input_type, calculator, hint, misconceptions, guided_steps):
    return {
        "display": display,
        "solutions": solutions,
        "calculator": calculator,
        "input_type": input_type,
        "hint": hint,
        "misconceptions": misconceptions,
        "guided_steps": guided_steps,
    }

def mc(pattern, expect, message):
    return {"pattern": pattern, "expect": expect, "message": message}

# =========================== BRONZE ===========================
bronze = [
    prob(
        "Calculate \\(5^3\\)", [125], "single_value", False,
        "Cubing means multiplying the number by itself three times.",
        [mc("multiply_by_index", 15,
            "15 comes from 5 × 3. A power means repeated multiplying, so 5³ = 5 × 5 × 5 = 125.")],
        [
            say("A power counts how many of the same number are multiplied. \\(5^3\\) means three 5s."),
            box("Start with the first two: 5 × 5 =", 25, "5 × 5 = 25."),
            box("Now multiply by the third 5: 25 × 5 =", 125,
                "25 × 5 = 125.", phase="substitute"),
            box("Confirm the three factors: 5 × 5 × 5 =", 125,
                "It comes to 125.", done="5³ = 125."),
        ],
    ),
    prob(
        "Calculate \\(\\sqrt{144}\\)", [12], "single_value", False,
        "Ask what number times itself gives 144.",
        [mc("halved", 72,
            "72 halves 144. A square root asks what number times itself gives 144, and 12 × 12 = 144.")],
        [
            say("A square root reverses squaring: it asks what number times itself gives 144."),
            box("Try 11 × 11 =", 121, "11 × 11 = 121, a little too small."),
            box("Try the next one: 12 × 12 =", 144, "12 × 12 = 144.", phase="substitute"),
            box("12 lands on 144, so write \\(\\sqrt{144}\\).", 12,
                "It is 12.", done="√144 = 12, since 12² = 144."),
        ],
    ),
    prob(
        "Calculate \\(\\sqrt[3]{27}\\)", [3], "single_value", False,
        "Ask what number multiplied by itself three times gives 27.",
        [mc("square_root", 9,
            "9 divides 27 by 3. A cube root asks what number cubed gives 27, and 3 × 3 × 3 = 27.")],
        [
            say("A cube root asks what number times itself three times gives 27."),
            box("Try 2 × 2 × 2 =", 8, "2³ = 8, too small."),
            box("Try 3 × 3 × 3 =", 27, "3³ = 27.", phase="substitute"),
            box("3 cubed lands on 27, so write \\(\\sqrt[3]{27}\\).", 3,
                "It is 3.", done="³√27 = 3."),
        ],
    ),
    prob(
        "Calculate \\(2^5\\)", [32], "single_value", False,
        "Multiply 2 by itself five times, one factor at a time.",
        [mc("multiply_by_index", 10,
            "10 comes from 2 × 5. A power multiplies repeatedly, so 2⁵ = 2 × 2 × 2 × 2 × 2 = 32.")],
        [
            say("\\(2^5\\) means five 2s multiplied together."),
            box("First three 2s: 2 × 2 × 2 =", 8, "2 × 2 × 2 = 8."),
            box("Multiply by the fourth 2: 8 × 2 =", 16, "8 × 2 = 16.", phase="substitute"),
            box("Multiply by the fifth 2: 16 × 2 =", 32, "16 × 2 = 32.", done="2⁵ = 32."),
        ],
    ),
    prob(
        "Write \\(56\\,000\\) in standard form. Enter the power of 10.", [4], "single_value", False,
        "Write it as 5.6 times a power of 10, then count the places the decimal moved.",
        [mc("count_zeros", 3,
            "3 counts only the zeros. Count the places the decimal moves to sit after the first digit: 56000 becomes 5.6 × 10⁴, so the power is 4.")],
        [
            say("Standard form needs a front number A between 1 and 10, times a power of 10."),
            box("Place the point after the first digit of 56000 to get the front A.", 5.6,
                "56000 becomes 5.6."),
            box("Count how many places the point moved from 56000 to 5.6.", 4,
                "56000, 5600, 560, 56, 5.6 is 4 moves.", phase="substitute"),
            box("The number is bigger than 1, so the power is positive. Write it.", 4,
                "The power is 4.", done="56000 = 5.6 × 10⁴, power 4."),
        ],
    ),
    prob(
        "Write \\(0.0034\\) in standard form. Enter the power of 10.", [-3], "single_value", False,
        "The number is less than 1, so the power will be negative.",
        [mc("positive_power", 3,
            "3 forgets the sign. Numbers below 1 take a negative power: 0.0034 = 3.4 × 10⁻³, so the power is −3.")],
        [
            say("Standard form needs a front number A between 1 and 10."),
            box("Place the point after the first non-zero digit of 0.0034 to get A.", 3.4,
                "0.0034 becomes 3.4."),
            box("Count how many places the point moved from 0.0034 to 3.4.", 3,
                "It moved 3 places right.", phase="substitute"),
            box("The number is below 1, so the power is negative. Enter it.", -3,
                "The power is −3.", done="0.0034 = 3.4 × 10⁻³, power −3."),
        ],
    ),
    prob(
        "Write \\(8.2 \\times 10^3\\) as an ordinary number", [8200], "single_value", False,
        "A positive power makes the number bigger, so move the decimal point right.",
        [mc("wrong_direction", 0.0082,
            "0.0082 moves the point the wrong way. A positive power makes the number bigger, so move 3 places right: 8200.")],
        [
            say("A power of 3 means move the decimal point 3 places. A positive power makes it bigger, so move right."),
            box("First place right: 8.2 × 10 =", 82, "8.2 × 10 = 82."),
            box("Second place: 82 × 10 =", 820, "82 × 10 = 820.", phase="substitute"),
            box("Third place: 820 × 10 =", 8200, "820 × 10 = 8200.", done="8.2 × 10³ = 8200."),
        ],
    ),
    prob(
        "Write \\(4.5 \\times 10^{-2}\\) as an ordinary number", [0.045], "single_value", False,
        "A negative power makes the number smaller, so move the decimal point left.",
        [mc("wrong_direction", 450,
            "450 moves the point right. A negative power makes the number smaller, so move 2 places left: 0.045.")],
        [
            say("A negative power means move the decimal point left, making the number smaller."),
            box("First place left: 4.5 ÷ 10 =", 0.45, "4.5 ÷ 10 = 0.45."),
            box("Second place: 0.45 ÷ 10 =", 0.045, "0.45 ÷ 10 = 0.045.", phase="substitute"),
            box("So 4.5 × 10⁻², two places left, gives:", 0.045,
                "It is 0.045.", done="4.5 × 10⁻² = 0.045."),
        ],
    ),
]

# =========================== SILVER ===========================
silver = [
    prob(
        "Calculate \\((4 \\times 10^3) \\times (3 \\times 10^5)\\). Give your answer in standard form.",
        [1.2, 9], "standard_form", False,
        "Multiply the front numbers, add the powers, then adjust if the front reaches 10.",
        [mc("no_adjust", [12, 8],
            "12 × 10⁸ is right but not in standard form: A must be below 10. Move one place: 1.2 × 10⁹.")],
        [
            say("For a product in standard form: multiply the fronts, add the powers, then fix the front if needed."),
            box("Multiply the fronts: 4 × 3 =", 12, "4 × 3 = 12."),
            box("Add the powers: 3 + 5 =", 8, "3 + 5 = 8."),
            box("That is 12 × 10⁸, but A must be below 10. Write 12 as 1.2 × 10, so the new A is:",
                1.2, "12 becomes 1.2.", phase="substitute"),
            box("Moving 12 down to 1.2 adds 1 to the power: 8 + 1 =", 9,
                "8 + 1 = 9.", done="1.2 × 10⁹. Check: 4000 × 300000 = 1.2 × 10⁹."),
        ],
    ),
    prob(
        "Calculate \\((9 \\times 10^7) \\div (3 \\times 10^4)\\). Give your answer in standard form.",
        [3, 3], "standard_form", False,
        "Divide the front numbers and subtract the powers.",
        [mc("added_powers", [3, 11],
            "Adding the powers gives 3 × 10¹¹. Division subtracts them: 7 − 4 = 3, so 3 × 10³.")],
        [
            say("For a quotient in standard form: divide the fronts and subtract the powers."),
            box("Divide the fronts: 9 ÷ 3 =", 3, "9 ÷ 3 = 3."),
            box("Subtract the powers: 7 − 4 =", 3, "7 − 4 = 3.", phase="substitute"),
            box("Check with ordinary numbers: 90000000 ÷ 30000 =", 3000,
                "90000000 ÷ 30000 = 3000.", done="3000 = 3 × 10³, so A = 3 and the power is 3."),
        ],
    ),
    prob(
        "Calculate \\((5 \\times 10^{-3}) \\times (8 \\times 10^6)\\). Give your answer in standard form.",
        [4, 4], "standard_form", False,
        "Multiply the fronts and add the powers, keeping the minus, then adjust.",
        [
            mc("no_adjust", [40, 3],
               "40 × 10³ needs adjusting: A must be below 10. 40 = 4 × 10, so 4 × 10⁴."),
            mc("dropped_minus", [4, 10],
               "Treating −3 as +3 gives 4 × 10¹⁰. Keep the minus: −3 + 6 = 3, then adjust 40 × 10³ to 4 × 10⁴."),
        ],
        [
            say("Multiply the fronts, add the powers (mind the minus), then fix the front."),
            box("Multiply the fronts: 5 × 8 =", 40, "5 × 8 = 40."),
            box("Add the powers, keeping the minus: −3 + 6 =", 3, "−3 + 6 = 3."),
            box("That is 40 × 10³, but A must be below 10. Write 40 as 4 × 10, so the new A is:",
                4, "40 becomes 4.", phase="substitute"),
            box("Moving 40 down to 4 adds 1 to the power: 3 + 1 =", 4,
                "3 + 1 = 4.", done="4 × 10⁴. Check: 0.005 × 8000000 = 40000 = 4 × 10⁴."),
        ],
    ),
    prob(
        "Calculate \\(\\sqrt{169}\\)", [13], "single_value", False,
        "Ask what number times itself gives 169.",
        [mc("halved", 84.5,
            "84.5 halves 169. A square root asks what number times itself gives 169, and 13 × 13 = 169.")],
        [
            say("A square root asks what number times itself gives 169."),
            box("Try 12 × 12 =", 144, "12 × 12 = 144, too small."),
            box("Try 13 × 13 =", 169, "13 × 13 = 169.", phase="substitute"),
            box("13 lands on 169, so write \\(\\sqrt{169}\\).", 13,
                "It is 13.", done="√169 = 13."),
        ],
    ),
    prob(
        "Calculate \\(\\sqrt[3]{125}\\)", [5], "single_value", False,
        "Ask what number multiplied by itself three times gives 125.",
        [],
        [
            say("A cube root asks what number times itself three times gives 125."),
            box("Try 4 × 4 × 4 =", 64, "4³ = 64, too small."),
            box("Try 5 × 5 × 5 =", 125, "5³ = 125.", phase="substitute"),
            box("5 cubed lands on 125, so write \\(\\sqrt[3]{125}\\).", 5,
                "It is 5.", done="³√125 = 5."),
        ],
    ),
    prob(
        "Calculate \\(4^{-2}\\) as a fraction. Give the denominator.", [16], "single_value", False,
        "A negative power means one over the positive power.",
        [mc("multiply_by_index", 8,
            "8 comes from 4 × 2. A power multiplies repeatedly: 4⁻² = 1 ÷ (4 × 4) = 1/16, so the denominator is 16.")],
        [
            say("A negative power flips the number: \\(4^{-2}\\) means one over \\(4^2\\)."),
            box("Work out the positive power first: 4 × 4 =", 16, "4 × 4 = 16."),
            box("So 4⁻² = 1/16. Write the denominator of the fraction.", 16,
                "The bottom of the fraction is 16.", phase="substitute"),
            box("Confirm the denominator is 4 squared: 4 × 4 =", 16,
                "4 × 4 = 16.", done="4⁻² = 1/16, denominator 16."),
        ],
    ),
    prob(
        "Calculate \\((2 \\times 10^4) + (3 \\times 10^3)\\). Give your answer in standard form.",
        [2.3, 4], "standard_form", False,
        "The powers are different, so write both as ordinary numbers and add.",
        [mc("added_fronts", [5, 4],
            "Adding the front numbers gives 5 × 10⁴, but the powers differ so you cannot add directly. Line them up: 20000 + 3000 = 23000 = 2.3 × 10⁴.")],
        [
            say("You can only add standard-form numbers directly when the powers match. Here they differ, so expand first."),
            box("Write the first as an ordinary number: 2 × 10⁴ =", 20000, "2 × 10⁴ = 20000."),
            box("Write the second: 3 × 10³ =", 3000, "3 × 10³ = 3000."),
            box("Add them: 20000 + 3000 =", 23000, "20000 + 3000 = 23000."),
            box("Write 23000 in standard form. Enter A, a number below 10.", 2.3,
                "23000 becomes 2.3.", phase="substitute"),
            box("Count the places from 23000 back to 2.3 for the power.", 4,
                "It moved 4 places.", done="2.3 × 10⁴. Check: 2.3 × 10000 = 23000."),
        ],
    ),
]

# =========================== GOLD ===========================
gold = [
    prob(
        "Calculate \\((6 \\times 10^4) \\times (5 \\times 10^{-2})\\). Give your answer in standard form.",
        [3, 3], "standard_form", False,
        "Multiply the fronts, add the powers, then adjust 30 back below 10.",
        [mc("no_adjust", [30, 2],
            "30 × 10² is not standard form: A must be below 10. 30 = 3 × 10, so 3 × 10³.")],
        [
            say("Multiply the fronts, add the powers (keep the minus), then fix the front."),
            box("Multiply the fronts: 6 × 5 =", 30, "6 × 5 = 30."),
            box("Add the powers: 4 + (−2) =", 2, "4 − 2 = 2."),
            box("That is 30 × 10², but A must be below 10. Write 30 as 3 × 10, so the new A is:",
                3, "30 becomes 3.", phase="substitute"),
            box("Moving 30 down to 3 adds 1 to the power: 2 + 1 =", 3,
                "2 + 1 = 3.", done="3 × 10³. Check: 60000 × 0.05 = 3000 = 3 × 10³."),
        ],
    ),
    prob(
        "Calculate \\(\\frac{3.6 \\times 10^8}{1.2 \\times 10^{-3}}\\). Give your answer in standard form.",
        [3, 11], "standard_form", False,
        "Divide the fronts and subtract the powers, minding the double negative.",
        [mc("subtract_wrong", [3, 5],
            "8 − 3 = 5 forgets the minus on the second power. Subtracting −3 adds: 8 − (−3) = 11, so 3 × 10¹¹.")],
        [
            say("Divide the fronts and subtract the powers. Watch the second power: it is negative."),
            box("Divide the fronts: 3.6 ÷ 1.2 =", 3, "3.6 ÷ 1.2 = 3."),
            box("Subtract the powers. Subtracting a negative adds: 8 − (−3) = 8 + 3 =", 11,
                "8 + 3 = 11.", phase="substitute"),
            box("3 is already below 10, so no adjusting. Enter the power to finish 3 × 10 to the n.", 11,
                "The power is 11.", done="3 × 10¹¹. Check: 360000000 ÷ 0.0012 = 3 × 10¹¹."),
        ],
    ),
    prob(
        "The mass of a proton is \\(1.67 \\times 10^{-27}\\) kg. Find the mass of \\(3 \\times 10^{23}\\) protons in standard form. Enter the A value.",
        [5.01], "single_value", True,
        "Multiply the two front numbers; the powers set the size.",
        [mc("added_fronts", 4.67,
            "4.67 adds 1.67 and 3. Finding the mass of many protons multiplies: 1.67 × 3 = 5.01.")],
        [
            say("Total mass is the mass of one proton times the number of protons, so multiply."),
            box("Multiply the fronts: 1.67 × 3 =", 5.01, "1.67 × 3 = 5.01."),
            box("Add the powers: −27 + 23 =", -4, "−27 + 23 = −4.", phase="substitute"),
            box("So the mass is 5.01 × 10⁻⁴ kg. The question wants the A value. Enter it.", 5.01,
                "A = 5.01.", done="Mass 5.01 × 10⁻⁴ kg, so A = 5.01."),
        ],
    ),
    prob(
        "Calculate \\((8 \\times 10^5) + (4.5 \\times 10^4)\\). Give your answer in standard form.",
        [8.45, 5], "standard_form", False,
        "The powers differ, so write both as ordinary numbers before adding.",
        [mc("added_fronts", [12.5, 5],
            "Adding the front numbers gives 12.5 × 10⁵, but the powers differ. Write them out: 800000 + 45000 = 845000 = 8.45 × 10⁵.")],
        [
            say("The powers differ, so you cannot add the fronts directly. Expand both first."),
            box("Write the first as an ordinary number: 8 × 10⁵ =", 800000, "8 × 10⁵ = 800000."),
            box("Write the second: 4.5 × 10⁴ =", 45000, "4.5 × 10⁴ = 45000."),
            box("Add them: 800000 + 45000 =", 845000, "800000 + 45000 = 845000."),
            box("Write 845000 in standard form. Enter A, a number below 10.", 8.45,
                "845000 becomes 8.45.", phase="substitute"),
            box("Count the places from 845000 back to 8.45 for the power.", 5,
                "It moved 5 places.", done="8.45 × 10⁵. Check: 8.45 × 100000 = 845000."),
        ],
    ),
    prob(
        "Light travels at \\(3 \\times 10^8\\) m/s. How far does it travel in \\(5 \\times 10^2\\) seconds? Give the power of 10.",
        [11], "single_value", False,
        "Distance is speed times time; multiply the fronts and add the powers, then adjust.",
        [mc("no_adjust", 10,
            "Stopping at 15 × 10¹⁰ gives power 10, but 15 is not below 10. Adjust to 1.5 × 10¹¹, so the power is 11.")],
        [
            say("Distance is speed × time. Multiply the fronts and add the powers, then fix the front."),
            box("Multiply the fronts: 3 × 5 =", 15, "3 × 5 = 15."),
            box("Add the powers: 8 + 2 =", 10, "8 + 2 = 10."),
            box("That is 15 × 10¹⁰, but 15 is not below 10. Writing 15 as 1.5 × 10 adds 1 to the power: 10 + 1 =",
                11, "10 + 1 = 11.", phase="substitute"),
            box("So the distance is 1.5 × 10¹¹ m. The question wants the power. Enter it.", 11,
                "The power is 11.", done="1.5 × 10¹¹ m, power 11."),
        ],
    ),
]

# =========================== tier_guides ===========================
tier_guides = {
    "bronze": {
        "title": "Bronze: Powers, roots and writing standard form",
        "steps": [
            "A <strong>power</strong> is repeated multiplying: \\(5^3 = 5 \\times 5 \\times 5\\). A <strong>square root</strong> undoes squaring, a <strong>cube root</strong> undoes cubing.",
            "<strong>Standard form</strong> is \\(A \\times 10^n\\) with A between 1 and 10. Move the point to sit after the first digit and count the places.",
            "Big numbers (above 1) get a positive power; small numbers (below 1) get a negative power.",
        ],
        "example": {
            "question": "Write 3200 in standard form",
            "steps": [
                {"label": "Front", "content": "Point after the first digit: 3.2"},
                {"label": "Count", "content": "3200 to 3.2 is 3 places, and 3200 is above 1."},
                {"label": "Check", "content": "3.2 × 1000 = 3200."},
                {"label": "Answer", "content": "\\(3.2 \\times 10^3\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: Multiplying and dividing in standard form",
        "steps": [
            "<strong>Multiply:</strong> multiply the fronts and <strong>add</strong> the powers. <strong>Divide:</strong> divide the fronts and <strong>subtract</strong> the powers.",
            "Then <strong>adjust</strong>: if the front reaches 10 or more, move it below 10 and add 1 to the power.",
            "A <strong>negative index</strong> means one over the positive power: \\(4^{-2} = \\frac{1}{4^2} = \\frac{1}{16}\\).",
        ],
        "example": {
            "question": "Calculate (6 × 10³) × (4 × 10⁴)",
            "steps": [
                {"label": "Fronts", "content": "6 × 4 = 24"},
                {"label": "Powers", "content": "3 + 4 = 7, giving 24 × 10⁷"},
                {"label": "Adjust", "content": "24 = 2.4 × 10, so add 1 to the power."},
                {"label": "Answer", "content": "\\(2.4 \\times 10^8\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: Adjusting, adding and real contexts",
        "steps": [
            "After multiplying or dividing, always <strong>adjust</strong> the front back between 1 and 10. A front below 1 (like 0.8) means take 1 off the power.",
            "To <strong>add or subtract</strong>, the powers must match. If they differ, write both as ordinary numbers, combine, then rewrite in standard form.",
            "In word problems, pick the operation first (distance is speed × time), then work the fronts and powers.",
        ],
        "example": {
            "question": "Calculate (7.2 × 10⁵) ÷ (9 × 10⁻²)",
            "steps": [
                {"label": "Fronts", "content": "7.2 ÷ 9 = 0.8"},
                {"label": "Powers", "content": "5 − (−2) = 7, giving 0.8 × 10⁷"},
                {"label": "Adjust", "content": "0.8 is below 1, so 8 × 10⁻¹ × 10⁷ = 8 × 10⁶."},
                {"label": "Answer", "content": "\\(8 \\times 10^6\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# =========================== guided (opener + teach) ===========================
guided = {
    "opener": {
        "label": "Before any powers",
        "display": OPENER_SVG +
                   "The Moon is about <strong>384,000 km</strong> away. Writing all those "
                   "zeros is slow and easy to slip on, so scientists pack them into a "
                   "power of 10.<br>The highlighted part is the three trailing zeros.",
        "steps": [
            box("How many zeros are on the end of 384,000?", 3,
                "384, then a 0, a 0 and a 0."),
            box("Each zero is one ×10. Three zeros multiplied is 10 to the power of what?", 3,
                "Three 10s multiplied is 10³."),
            say("Those three zeros are exactly \\(10^3\\), so \\(384{,}000 = 384 \\times 10^3\\). "
                "Tidy the front to a single digit and it becomes <strong>\\(3.84 \\times 10^5\\)</strong>. "
                "That is <strong>standard form</strong>: one digit before the point, times a power of 10, "
                "where the power counts how far the point moved. Big numbers get positive powers, "
                "tiny numbers get negative ones."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "Write 47000 in standard form.",
            "label": "Together: your first one",
            "steps": [
                say("Standard form is \\(A \\times 10^n\\) with A between 1 and 10. Find A first."),
                box("Place the point after the first digit of 47000 to get the front A.", 4.7,
                    "47000 becomes 4.7."),
                box("Count how many places the point moved from 47000 to 4.7.", 4,
                    "47000, 4700, 470, 47, 4.7 is 4 moves."),
                box("The number is above 1, so the power is positive. Write the power.", 4,
                    "The power is 4."),
                box("Check by expanding: 4.7 × 10000 =", 47000,
                    "4.7 × 10000 = 47000.", done="47000 = 4.7 × 10⁴. That was the whole point."),
            ],
        },
        "silver": {
            "display": "Calculate \\((7 \\times 10^4) \\times (4 \\times 10^3)\\). Give your answer in standard form.",
            "label": "Together: the silver move",
            "steps": [
                say("Multiply the fronts, add the powers, then adjust the front if it reaches 10."),
                box("Multiply the fronts: 7 × 4 =", 28, "7 × 4 = 28."),
                box("Add the powers: 4 + 3 =", 7, "4 + 3 = 7."),
                box("28 is not below 10. Write it as 2.8 × 10, so the new front A is:", 2.8,
                    "28 becomes 2.8."),
                box("Adjusting 28 to 2.8 adds 1 to the power: 7 + 1 =", 8,
                    "7 + 1 = 8.", done="2.8 × 10⁸. Check: 70000 × 4000 = 280000000 = 2.8 × 10⁸."),
            ],
        },
        "gold": {
            "display": "Calculate \\((7.2 \\times 10^5) \\div (9 \\times 10^{-2})\\). Give your answer in standard form.",
            "label": "Together: the gold move",
            "steps": [
                say("Divide the fronts, subtract the powers, then adjust, even when the front comes out below 1."),
                box("Divide the fronts: 7.2 ÷ 9 =", 0.8, "7.2 ÷ 9 = 0.8."),
                box("Subtract the powers. Subtracting a negative adds: 5 − (−2) = 5 + 2 =", 7,
                    "5 + 2 = 7."),
                box("0.8 is below 1, so it is not standard form. Write 0.8 as 8 × 10⁻¹, giving new A:", 8,
                    "0.8 becomes 8."),
                box("Moving 0.8 up to 8 takes 1 off the power: 7 − 1 =", 6,
                    "7 − 1 = 6.", done="8 × 10⁶. Check: 720000 ÷ 0.09 = 8000000 = 8 × 10⁶."),
            ],
        },
    },
}

# =========================== method_card (slim) ===========================
method_card = {
    "title": "Powers, Roots and Standard Form",
    "steps": [
        "A power is repeated multiplying; a root undoes it. Learn the squares to 15² and cubes to 5³.",
        "Standard form is A × 10 to the n, with A between 1 and 10; the power counts the decimal places moved.",
        "Multiply: multiply fronts, add powers. Divide: divide fronts, subtract powers.",
        "Always adjust the front back between 1 and 10 and change the power to match.",
    ],
    "content": "<p><strong>Powers</strong> are repeated multiplying: \\(a^n\\) is \\(n\\) copies of \\(a\\). "
               "<strong>Roots</strong> reverse them, so \\(\\sqrt{}\\) undoes squaring and \\(\\sqrt[3]{}\\) undoes cubing. "
               "A <strong>negative index</strong> means one over the positive power.</p>"
               "<p><strong>Standard form</strong> writes a number as \\(A \\times 10^n\\) with \\(1 \\le A < 10\\). "
               "Big numbers take a positive \\(n\\), numbers below 1 take a negative \\(n\\). "
               "To multiply, multiply the fronts and add the powers; to divide, divide the fronts and subtract the powers, "
               "then adjust \\(A\\) back below 10.</p>",
    "example": "<p><strong>Write 0.00045 in standard form.</strong></p>"
               "<p>Move the point after the first non-zero digit to get \\(4.5\\); it moved 4 places right, "
               "and the number is below 1, so \\(n = -4\\).</p>"
               "<p><strong>Answer:</strong> \\(4.5 \\times 10^{-4}\\)</p>",
}

# preserved fields (from live)
topic_links = {"prerequisites": []}
related_videos = []
worked_examples = [
    {
        "steps": [
            {"label": "Move decimal", "content": "<p>\\(3.7\\) (moved 6 places left)</p>"},
            {"label": "Answer", "content": "<p>\\(3.7 \\times 10^6\\)</p>", "isAnswer": True},
        ],
        "question": "Write 3 700 000 in standard form",
        "difficulty": "Bronze",
    },
    {
        "steps": [
            {"label": "Multiply A values", "content": "<p>\\(4 \\times 2 = 8\\)</p>"},
            {"label": "Add powers", "content": "<p>\\(3 + 5 = 8\\)</p>"},
            {"label": "Answer", "content": "<p>\\(8 \\times 10^8\\) (already in standard form since \\(1 \\le 8 < 10\\))</p>", "isAnswer": True},
        ],
        "question": "Calculate (4 × 10³) × (2 × 10⁵)",
        "difficulty": "Silver",
    },
    {
        "steps": [
            {"label": "Multiply A values", "content": "<p>\\(6 \\times 5 = 30\\)</p>"},
            {"label": "Add powers", "content": "<p>\\(4 + (-2) = 2\\)</p>"},
            {"label": "Adjust", "content": "<p>\\(30 \\times 10^2 = 3.0 \\times 10^3\\) (since 30 ≥ 10, divide by 10 and add 1 to power)</p>", "isAnswer": True},
        ],
        "question": "Calculate (6 × 10⁴) × (5 × 10⁻²). Give answer in standard form.",
        "difficulty": "Gold",
    },
]

practice_data = {
    "method_card": method_card,
    "topic_links": topic_links,
    "problem_bank": {
        "bronze": bronze,
        "silver": silver,
        "gold": gold,
        "bronze_description": "Work out powers and square or cube roots, and convert between ordinary numbers and standard form.",
        "silver_description": "Multiply and divide numbers in standard form, and handle negative indices.",
        "gold_description": "Adjust answers back into standard form, add numbers in standard form, and solve real-life problems.",
    },
    "related_videos": related_videos,
    "worked_examples": worked_examples,
    "tier_guides": tier_guides,
    "guided": guided,
}

with io.open("lesson_maths-aqa_number-L06.json", "w", encoding="utf-8") as f:
    json.dump(practice_data, f, indent=1, ensure_ascii=False)
print("written lesson_maths-aqa_number-L06.json")
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
