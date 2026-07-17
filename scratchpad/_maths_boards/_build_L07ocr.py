# -*- coding: utf-8 -*-
import json, copy

live = json.load(open("_L07ocr_live.json", encoding="utf-8"))
pd = copy.deepcopy(live)
pb = pd["problem_bank"]

# ---------- helpers ----------
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say: d["say"] = say
    if done: d["done"] = done
    if phase: d["phase"] = phase
    return d

def say(text):
    return {"say": text}

# ---------- tier descriptions ----------
pb["bronze_description"] = "Simplify a single surd, add like surds, or find one bound with a half-unit step."
pb["silver_description"] = "Combine surds (multiply, divide, rationalise, difference of two squares) or bound a sum or difference."
pb["gold_description"] = "Rationalise with a conjugate, expand a surd square, or find a bound of a quotient."

# ================= BRONZE =================
def simplify_surd_walk(n, sq, other, coeff):
    root = int(round(coeff))
    return [
        box(f"The largest square number that divides {n} is ", sq,
            f"Try {sq}: {sq} times {other} = {n}."),
        box(f"{n} ÷ {sq} = ", other, "Divide to find what is left under the root."),
        say(f"So \\(\\sqrt{{{n}}} = \\sqrt{{{sq}}} \\times \\sqrt{{{other}}}\\)."),
        box(f"\\(\\sqrt{{{sq}}}\\) = ", root, f"What number times itself makes {sq}?", phase="substitute"),
        box(f"So \\(\\sqrt{{{n}}}\\) = ", root, "Bring that number outside the root.",
            post=f"√{other}"),
        box(f"Check: {root}² × {other} = ", n, "Square your answer, then times the number under the root.",
            done=f"It rebuilds {n}, so \\(\\sqrt{{{n}}} = {root}\\sqrt{{{other}}}\\) is right."),
    ]

pb["bronze"][0]["hint"] = "Find the largest square number that divides 50, then take its root outside."
pb["bronze"][0]["guided_steps"] = simplify_surd_walk(50, 25, 2, 5)
pb["bronze"][0]["misconceptions"] = [
    {"pattern": "wrong_factor", "expect": None,
     "message": "Use the largest square factor: 50 = 25 × 2, and √25 = 5, so √50 = 5√2."},
    {"pattern": "small_factor", "expect": None,
     "message": "Do not stop at a small factor. 50 = 25 × 2 gives 5√2, fully simplified."},
]

pb["bronze"][1]["hint"] = "Split 18 as 9 times 2, then take the root of 9."
pb["bronze"][1]["guided_steps"] = simplify_surd_walk(18, 9, 2, 3)
pb["bronze"][1]["misconceptions"] = [
    {"pattern": "wrong_factor", "expect": None,
     "message": "18 = 9 × 2, and √9 = 3, so √18 = 3√2."},
    {"pattern": "small_factor", "expect": None,
     "message": "Use the largest square factor 9, not 2 or 3. √18 = 3√2."},
]

pb["bronze"][2]["hint"] = "Split 75 as 25 times 3, then take the root of 25."
pb["bronze"][2]["guided_steps"] = simplify_surd_walk(75, 25, 3, 5)
pb["bronze"][2]["misconceptions"] = [
    {"pattern": "wrong_factor", "expect": None,
     "message": "75 = 25 × 3, and √25 = 5, so √75 = 5√3."},
    {"pattern": "small_factor", "expect": None,
     "message": "Use the largest square factor 25. √75 = 5√3."},
]

pb["bronze"][3]["hint"] = "Same root, so just add the numbers in front and keep the root."
pb["bronze"][3]["guided_steps"] = [
    box("Both terms are lots of √3, so add the numbers in front: 2 + 5 = ", 7,
        "Add only the coefficients."),
    say("The √3 stays the same. You never add the numbers under the root."),
    box("So the total is ", 7, "Keep the same root.", post="√3", phase="substitute"),
    box("Check by taking one lot back off: 7 − 5 = ", 2,
        "Subtract the 5 lots you added.",
        done="That returns the 2√3 you started with, so 7√3 is right."),
]
pb["bronze"][3]["misconceptions"] = [
    {"pattern": "add_under_root", "expect": None,
     "message": "Keep the root: 2√3 + 5√3 = 7√3. Do not add the 3s under the root."},
    {"pattern": "wrong", "expect": None,
     "message": "Same root means add the coefficients: 2 + 5 = 7, giving 7√3."},
]

pb["bronze"][6]["hint"] = "Split 12 as 4 times 3, then take the root of 4."
pb["bronze"][6]["guided_steps"] = simplify_surd_walk(12, 4, 3, 2)
pb["bronze"][6]["misconceptions"] = [
    {"pattern": "wrong_factor", "expect": None,
     "message": "12 = 4 × 3, and √4 = 2, so √12 = 2√3."},
    {"pattern": "small_factor", "expect": None,
     "message": "Use the square factor 4. √12 = 2√3."},
]

# ---- bronze bounds ----
pb["bronze"][4]["hint"] = "Nearest 1 cm means the half unit is 0.5; take it off the value."
pb["bronze"][4]["guided_steps"] = [
    box("Rounded to the nearest 1 cm, so the half unit is ", 0.5, "Half of 1 is 0.5."),
    say("The lower bound is the value minus the half unit."),
    box("12 − 0.5 = ", 11.5, "Subtract 0.5 from 12.", phase="substitute"),
    box("The upper bound is 12 + 0.5 = ", 12.5, "Add 0.5 to 12.",
        done="The true length lies between 11.5 and 12.5, so the lower bound is 11.5."),
]
pb["bronze"][4]["misconceptions"] = [
    {"pattern": "used_upper", "expect": 12.5,
     "message": "That is the upper bound. The lower bound subtracts the half unit: 12 − 0.5 = 11.5."},
    {"pattern": "whole_unit", "expect": 11,
     "message": "The half unit is 0.5, not 1. Lower bound = 12 − 0.5 = 11.5."},
]

pb["bronze"][5]["hint"] = "One decimal place means the half unit is 0.05; add it for the upper bound."
pb["bronze"][5]["guided_steps"] = [
    box("Rounded to 1 d.p., so the half unit is ", 0.05, "Half of 0.1 is 0.05."),
    say("The upper bound is the value plus the half unit."),
    box("3.2 + 0.05 = ", 3.25, "Add 0.05 to 3.2.", phase="substitute"),
    box("The lower bound is 3.2 − 0.05 = ", 3.15, "Subtract 0.05 from 3.2.",
        done="The true mass lies between 3.15 and 3.25, so the upper bound is 3.25."),
]
pb["bronze"][5]["misconceptions"] = [
    {"pattern": "used_lower", "expect": 3.15,
     "message": "That is the lower bound. The upper bound adds the half unit: 3.2 + 0.05 = 3.25."},
    {"pattern": "wrong_half", "expect": 3.7,
     "message": "For 1 d.p. the half unit is 0.05, not 0.5. Upper bound = 3.2 + 0.05 = 3.25."},
]

pb["bronze"][7]["hint"] = "Nearest 5 means the half unit is 2.5; take it off for the lower bound."
pb["bronze"][7]["guided_steps"] = [
    box("Rounded to the nearest 5 mph, so the half unit is ", 2.5, "Half of 5 is 2.5."),
    say("The lower bound is the value minus the half unit."),
    box("45 − 2.5 = ", 42.5, "Subtract 2.5 from 45.", phase="substitute"),
    box("The upper bound is 45 + 2.5 = ", 47.5, "Add 2.5 to 45.",
        done="The true speed lies between 42.5 and 47.5, so the lower bound is 42.5."),
]
pb["bronze"][7]["misconceptions"] = [
    {"pattern": "used_upper", "expect": 47.5,
     "message": "That is the upper bound. The lower bound subtracts the half unit: 45 − 2.5 = 42.5."},
    {"pattern": "wrong_half", "expect": 44.5,
     "message": "Rounded to the nearest 5, so the half unit is 2.5, not 0.5. Lower bound = 45 − 2.5 = 42.5."},
]

# ================= SILVER =================
pb["silver"][0]["hint"] = "Multiply top and bottom by root 3, then simplify the fraction."
pb["silver"][0]["guided_steps"] = [
    box("Multiply top and bottom by √3. Bottom: √3 × √3 = ", 3,
        "A root times itself removes the root."),
    say("The top becomes 6√3, so the fraction is now 6√3 over 3."),
    box("6 ÷ 3 = ", 2, "Divide the whole number by 3.", post="√3", phase="substitute"),
    box("Check: 2√3 × √3 = 2 × 3 = ", 6, "Multiply your answer back by √3.",
        done="It returns the 6 on top, so 6/√3 = 2√3."),
]
pb["silver"][0]["misconceptions"] = [
    {"pattern": "no_simplify", "expect": None,
     "message": "Simplify the fraction: 6√3 ÷ 3 = 2√3, not 6√3."},
    {"pattern": "wrong", "expect": None,
     "message": "Multiply top and bottom by √3: 6√3/3 = 2√3."},
]

pb["silver"][1]["hint"] = "Multiply under one root to get root 48, then simplify."
pb["silver"][1]["guided_steps"] = [
    box("Multiply under one root: 8 × 6 = ", 48, "Multiply the numbers under the roots."),
    say("So √8 × √6 = √48. Now simplify √48."),
    box("The largest square factor of 48 is 16, and 48 ÷ 16 = ", 3,
        "16 times 3 is 48.", phase="substitute"),
    box("√16 = ", 4, "What number times itself makes 16?"),
    box("Check: 4² × 3 = ", 48, "Square the 4, then times 3.",
        done="It rebuilds 48, so √48 = 4√3."),
]
pb["silver"][1]["misconceptions"] = [
    {"pattern": "no_simplify", "expect": None,
     "message": "√48 is not fully simplified: 48 = 16 × 3, so √48 = 4√3."},
    {"pattern": "wrong", "expect": None,
     "message": "Combine under one root then simplify: √8 × √6 = √48 = 4√3."},
]

pb["silver"][2]["hint"] = "This is (a plus b)(a minus b), so work out a squared minus b squared."
pb["silver"][2]["guided_steps"] = [
    box("This is (a + b)(a − b) = a² − b². Here a = 3, so a² = ", 9, "Square the 3."),
    box("b = √2, so b² = (√2)² = ", 2, "A root squared removes the root."),
    say("Difference of two squares: a² − b²."),
    box("9 − 2 = ", 7, "Subtract.", phase="substitute"),
    box("Check the middle terms cancel: −3√2 + 3√2 = ", 0,
        "Opposite surds add to zero.",
        done="The surds cancel, leaving 7."),
]
pb["silver"][2]["misconceptions"] = [
    {"pattern": "added", "expect": 11,
     "message": "It is a difference of two squares: 3² − (√2)² = 9 − 2 = 7, not 9 + 2."},
    {"pattern": "forgot_second", "expect": 9,
     "message": "Subtract b²: (√2)² = 2, so 9 − 2 = 7."},
]

pb["silver"][3]["hint"] = "For the smallest sum, add the lower bound of each value."
pb["silver"][3]["guided_steps"] = [
    box("Half unit for 1 d.p. = ", 0.05, "Half of 0.1."),
    box("Lower bound of a = 5.4 − 0.05 = ", 5.35, "Subtract 0.05 from 5.4."),
    say("For the smallest possible sum, use the lower bound of each value."),
    box("Lower bound of b = 3.8 − 0.05 = ", 3.75, "Subtract 0.05 from 3.8.", phase="substitute"),
    box("5.35 + 3.75 = ", 9.1, "Add the two lower bounds.",
        done="The smallest possible a + b is 9.1."),
]
pb["silver"][3]["misconceptions"] = [
    {"pattern": "used_upper", "expect": 9.3,
     "message": "For the smallest sum, use the lower bounds: 5.35 + 3.75 = 9.1, not the upper bounds."},
    {"pattern": "used_rounded", "expect": 9.2,
     "message": "Use the lower bounds, not the rounded values: 5.35 + 3.75 = 9.1."},
]

pb["silver"][4]["hint"] = "Divide under one root: 20 over 5, then take the root."
pb["silver"][4]["guided_steps"] = [
    box("Combine under one root: 20 ÷ 5 = ", 4, "Divide the numbers under the roots."),
    say("So √20 / √5 = √4."),
    box("√4 = ", 2, "What number times itself makes 4?", phase="substitute"),
    box("Check: 2 × √5 = √20 because 2² × 5 = ", 20,
        "Square the 2, then times 5.",
        done="It rebuilds √20, so the answer is 2."),
]
pb["silver"][4]["misconceptions"] = [
    {"pattern": "wrong", "expect": None,
     "message": "Combine under one root: √(20/5) = √4 = 2."},
]

pb["silver"][5]["hint"] = "For the biggest difference, use the upper bound of a and the lower bound of b."
pb["silver"][5]["guided_steps"] = [
    box("Half unit for the nearest integer = ", 0.5, "Half of 1."),
    box("Upper bound of a = 8 + 0.5 = ", 8.5, "Add 0.5 to 8."),
    say("For the biggest difference, make a as large as possible and b as small as possible."),
    box("Lower bound of b = 3 − 0.5 = ", 2.5, "Subtract 0.5 from 3.", phase="substitute"),
    box("8.5 − 2.5 = ", 6, "Subtract the lower b from the upper a.",
        done="The largest possible a − b is 6."),
]
pb["silver"][5]["misconceptions"] = [
    {"pattern": "same_direction", "expect": 5,
     "message": "For the biggest difference, take a large but b small: 8.5 − 2.5 = 6, not 8.5 − 3.5."},
    {"pattern": "reversed", "expect": 4,
     "message": "Use upper a and lower b: 8.5 − 2.5 = 6, not lower a and upper b."},
]

pb["silver"][6]["hint"] = "Multiply top and bottom by root 2, then simplify."
pb["silver"][6]["guided_steps"] = [
    box("Multiply top and bottom by √2. Bottom: √2 × √2 = ", 2,
        "A root times itself removes the root."),
    say("The top becomes 4√2, so the fraction is now 4√2 over 2."),
    box("4 ÷ 2 = ", 2, "Divide the whole number by 2.", post="√2", phase="substitute"),
    box("Check: 2√2 × √2 = 2 × 2 = ", 4, "Multiply your answer back by √2.",
        done="It returns the 4 on top, so 4/√2 = 2√2."),
]
pb["silver"][6]["misconceptions"] = [
    {"pattern": "no_simplify", "expect": None,
     "message": "Simplify: 4√2 ÷ 2 = 2√2, not 4√2."},
    {"pattern": "wrong", "expect": None,
     "message": "Multiply top and bottom by √2: 4√2/2 = 2√2."},
]

# ================= GOLD =================
pb["gold"][0]["hint"] = "Multiply top and bottom by the conjugate 3 minus root 2."
pb["gold"][0]["guided_steps"] = [
    box("Multiply top and bottom by the conjugate 3 − √2. Bottom: 3² = ", 9, "Square the 3."),
    box("(√2)² = ", 2, "A root squared removes the root."),
    say("The bottom is 3² − (√2)², a difference of two squares."),
    box("9 − 2 = ", 7, "Subtract to get the new denominator.", phase="substitute"),
    box("The top is 1 × (3 − √2) = 3 − √2. Check the surds cancel: −3√2 + 3√2 = ", 0,
        "Opposite surds add to zero.",
        done="No surd left below, so the answer is (3 − √2)/7."),
]
pb["gold"][0]["misconceptions"] = [
    {"pattern": "wrong_conjugate", "expect": None,
     "message": "The conjugate of 3 + √2 is 3 − √2, giving a denominator 3² − (√2)² = 7."},
    {"pattern": "wrong", "expect": None,
     "message": "Multiply by (3 − √2)/(3 − √2): numerator 3 − √2, denominator 7."},
]

pb["gold"][1]["hint"] = "Square it as (2 plus root 5)(2 plus root 5); do not forget the middle term."
pb["gold"][1]["guided_steps"] = [
    box("(2 + √5)² = 2² + 2×2×√5 + (√5)². First term 2² = ", 4, "Square the 2."),
    box("Last term (√5)² = ", 5, "A root squared removes the root."),
    say("Middle term: 2 × 2 × √5 = 4√5."),
    box("Whole-number part: 4 + 5 = ", 9, "Add the two whole-number terms.", phase="substitute"),
    box("Surd coefficient: 2 × 2 = ", 4, "Double the 2 for the middle term.",
        done="So (2 + √5)² = 9 + 4√5."),
]
pb["gold"][1]["misconceptions"] = [
    {"pattern": "miss_middle", "expect": None,
     "message": "Do not forget the middle term 2×2×√5 = 4√5. Answer: 9 + 4√5."},
    {"pattern": "squared_terms_only", "expect": None,
     "message": "(2 + √5)² = 4 + 4√5 + 5 = 9 + 4√5, not 4 + 5."},
]

pb["gold"][2]["hint"] = "For the biggest quotient, divide the upper bound of a by the lower bound of b."
pb["gold"][2]["guided_steps"] = [
    box("Half unit for 1 d.p. = ", 0.05, "Half of 0.1."),
    box("Upper bound of a = 6.0 + 0.05 = ", 6.05, "Add 0.05 to 6.0."),
    say("For the biggest quotient, make the top as large and the bottom as small as possible."),
    box("Lower bound of b = 2.0 − 0.05 = ", 1.95, "Subtract 0.05 from 2.0.", phase="substitute"),
    box("6.05 ÷ 1.95 = (2 d.p.) ", 3.1, "Divide, then round to 2 d.p.",
        done="The largest possible a/b is 3.10."),
]
pb["gold"][2]["misconceptions"] = [
    {"pattern": "used_rounded", "expect": 3,
     "message": "Use the bounds, not the rounded values: 6.05 ÷ 1.95 ≈ 3.10, not 6.0 ÷ 2.0."},
    {"pattern": "upper_over_upper", "expect": 2.95,
     "message": "For the biggest quotient, divide by the smallest b: 6.05 ÷ 1.95 ≈ 3.10."},
]

pb["gold"][3]["hint"] = "Simplify root 12 to 2 root 3, add the numerator, then divide by root 3."
pb["gold"][3]["guided_steps"] = [
    box("Simplify √12: 12 = 4 × 3, so √12 = 2√3. The coefficient is ", 2,
        "√4 = 2."),
    say("The numerator is 2√3 + √3 = 3√3."),
    box("Add the coefficients: 2 + 1 = ", 3, "There is 1 lot of √3 in the second term.",
        post="√3", phase="substitute"),
    box("Divide by √3: 3√3 ÷ √3 = ", 3, "The √3 cancels, leaving the number in front.",
        done="So the expression equals 3."),
]
pb["gold"][3]["misconceptions"] = [
    {"pattern": "dropped_term", "expect": 2,
     "message": "Divide both terms by √3: √12/√3 = 2 and √3/√3 = 1, giving 2 + 1 = 3."},
    {"pattern": "multiplied", "expect": 9,
     "message": "Divide by √3, do not multiply: 3√3 ÷ √3 = 3."},
]

pb["gold"][4]["hint"] = "Simplify root 8, then divide both terms on top by 2."
pb["gold"][4]["guided_steps"] = [
    box("Simplify √8: 8 = 4 × 2, so √8 = 2√2. The coefficient is ", 2, "√4 = 2."),
    say("So the top is 6 + 2√2, all over 2."),
    box("Divide the first term: 6 ÷ 2 = ", 3, "Divide the whole number by 2.", phase="substitute"),
    box("Divide the surd term: 2√2 ÷ 2 = ", 1, "Divide the coefficient by 2.",
        post="√2",
        done="So (6 + √8)/2 = 3 + √2."),
]
pb["gold"][4]["misconceptions"] = [
    {"pattern": "only_first", "expect": None,
     "message": "Divide both terms by 2: 6/2 + 2√2/2 = 3 + √2."},
    {"pattern": "no_simplify_root", "expect": None,
     "message": "Simplify √8 = 2√2 first, then (6 + 2√2)/2 = 3 + √2."},
]

# ================= GUIDED (opener + teach) =================
svg = ('<svg viewBox="0 0 140 148" role="img" aria-label="A square made of a 3 by 3 grid '
       'of unit tiles, total area 9 tiles, so each side is 3 tiles long">'
       '<rect x="25" y="12" width="90" height="90" fill="#60a5fa" fill-opacity="0.3" '
       'stroke="currentColor" stroke-width="1.5"/>'
       '<line x1="55" y1="12" x2="55" y2="102" stroke="currentColor" stroke-width="1"/>'
       '<line x1="85" y1="12" x2="85" y2="102" stroke="currentColor" stroke-width="1"/>'
       '<line x1="25" y1="42" x2="115" y2="42" stroke="currentColor" stroke-width="1"/>'
       '<line x1="25" y1="72" x2="115" y2="72" stroke="currentColor" stroke-width="1"/>'
       '<text x="70" y="120" font-family="Inter, sans-serif" font-size="11" '
       'fill="currentColor" text-anchor="middle">Area = 9 tiles</text>'
       '<text x="70" y="136" font-family="Inter, sans-serif" font-size="11" '
       'fill="currentColor" text-anchor="middle">Each tile is 1 cm by 1 cm</text>'
       '</svg>')

pd["guided"] = {
    "opener": {
        "label": "Before any surds",
        "display": svg,
        "steps": [
            box("This square tile has an area of 9 cm². How many cm long is each side? ", 3,
                "Count the tiles along one edge, or ask what number times itself makes 9.",
                post=" cm"),
            box("A different square has an area of 25 cm². How long is each side? ", 5,
                "5 times 5 makes 25.", post=" cm"),
            say("Finding the side of a square from its area is taking a <strong>square root</strong>: "
                "\\(\\sqrt{9} = 3\\), \\(\\sqrt{25} = 5\\). When the area is not a perfect square, like 50, "
                "hunt for the biggest square hiding inside it: \\(50 = 25 \\times 2\\), so "
                "\\(\\sqrt{50} = \\sqrt{25} \\times \\sqrt{2} = 5\\sqrt{2}\\). Pulling out that square factor "
                "is <strong>simplifying a surd</strong>, the first move in this lesson."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "Simplify \\(\\sqrt{32}\\)",
            "label": "Together: your first surd",
            "steps": [
                box("The largest square number that divides 32 is ", 16, "Try 16: 16 times 2 is 32."),
                box("32 ÷ 16 = ", 2, "Divide to find what is left under the root."),
                say("So \\(\\sqrt{32} = \\sqrt{16} \\times \\sqrt{2}\\)."),
                box("\\(\\sqrt{16}\\) = ", 4, "4 times 4 is 16.", phase="substitute"),
                box("So \\(\\sqrt{32}\\) = ", 4, "Bring the 4 outside the root.", post="√2"),
                box("Check: 4² × 2 = ", 32, "Square the 4, then times 2.",
                    done="It rebuilds 32, so \\(\\sqrt{32} = 4\\sqrt{2}\\)."),
            ],
        },
        "silver": {
            "display": "Rationalise \\(\\frac{10}{\\sqrt{5}}\\)",
            "label": "Together: clear the surd from the bottom",
            "steps": [
                box("Multiply top and bottom by √5. Bottom: √5 × √5 = ", 5,
                    "A root times itself removes the root."),
                box("Top: 10 × √5 = 10√5, so we have 10√5 over ", 5,
                    "The new denominator is 5."),
                say("Now simplify 10√5 over 5."),
                box("10 ÷ 5 = ", 2, "Divide the whole number by 5.", post="√5", phase="substitute"),
                box("Check: 2√5 × √5 = 2 × 5 = ", 10, "Multiply your answer back by √5.",
                    done="It returns the 10 on top, so 10/√5 = 2√5."),
            ],
        },
        "gold": {
            "display": "Rationalise \\(\\frac{1}{4 + \\sqrt{3}}\\)",
            "label": "Together: use the conjugate",
            "steps": [
                box("Multiply top and bottom by the conjugate 4 − √3. Bottom: 4² = ", 16,
                    "Square the 4."),
                box("(√3)² = ", 3, "A root squared removes the root."),
                say("The middle surd terms cancel, leaving 4² − (√3)² = 16 − 3."),
                box("16 − 3 = ", 13, "Subtract to get the new denominator.", phase="substitute"),
                box("The top is 1 × (4 − √3) = 4 − √3. Check the surds cancel: −4√3 + 4√3 = ",
                    0, "Opposite surds add to zero.",
                    done="No surd left below, so the answer is (4 − √3)/13."),
            ],
        },
    },
}

# ================= tier_guides =================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one surd or one bound",
        "steps": [
            "<strong>Simplify a surd</strong>: find the largest square number that divides it, then take its root outside. \\(\\sqrt{50} = \\sqrt{25 \\times 2} = 5\\sqrt{2}\\).",
            "<strong>Add or subtract</strong> only surds with the same root: add the numbers in front, keep the root. \\(2\\sqrt{3} + 5\\sqrt{3} = 7\\sqrt{3}\\).",
            "<strong>Bounds</strong>: half a unit each side of the rounded value. To the nearest cm the half unit is 0.5; to 1 d.p. it is 0.05.",
        ],
        "example": {
            "question": "Simplify \\(\\sqrt{45}\\)",
            "steps": [
                {"label": "Square factor", "content": "<p>45 = 9 × 3, and 9 is a square number.</p>"},
                {"label": "Take the root", "content": "<p>\\(\\sqrt{45} = \\sqrt{9} \\times \\sqrt{5} = 3\\sqrt{5}\\)</p>"},
                {"label": "Check", "content": "<p>3² × 5 = 45 ✓</p>"},
                {"label": "Answer", "content": "<p><strong>\\(3\\sqrt{5}\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: combine surds or bound a sum",
        "steps": [
            "<strong>Multiply or divide</strong>: combine under one root, then simplify. \\(\\sqrt{8} \\times \\sqrt{6} = \\sqrt{48} = 4\\sqrt{3}\\).",
            "<strong>Rationalise</strong> \\(\\frac{n}{\\sqrt{a}}\\): multiply top and bottom by \\(\\sqrt{a}\\), then simplify the fraction.",
            "<strong>Bounds of a sum</strong>: for the smallest \\(a + b\\), add both lower bounds; for the largest, add both upper bounds.",
        ],
        "example": {
            "question": "Simplify \\(\\frac{\\sqrt{50}}{\\sqrt{2}}\\)",
            "steps": [
                {"label": "Combine", "content": "<p>\\(\\frac{\\sqrt{50}}{\\sqrt{2}} = \\sqrt{50 \\div 2} = \\sqrt{25}\\)</p>"},
                {"label": "Root", "content": "<p>\\(\\sqrt{25} = 5\\)</p>"},
                {"label": "Check", "content": "<p>5² × 2 = 50, so 5 × √2 = √50 ✓</p>"},
                {"label": "Answer", "content": "<p><strong>5</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: conjugates, surd squares and bounds of a quotient",
        "steps": [
            "<strong>Rationalise \\(\\frac{1}{a + \\sqrt{b}}\\)</strong>: multiply top and bottom by the conjugate \\(a - \\sqrt{b}\\). The denominator becomes \\(a^2 - b\\), a whole number.",
            "<strong>Square a surd</strong>: \\((a + \\sqrt{b})^2 = a^2 + 2a\\sqrt{b} + b\\). Keep the middle term.",
            "<strong>Bound of \\(\\frac{a}{b}\\)</strong>: the largest value uses upper \\(a\\) and lower \\(b\\); the smallest uses lower \\(a\\) and upper \\(b\\).",
        ],
        "example": {
            "question": "Expand \\((1 + \\sqrt{3})^2\\)",
            "steps": [
                {"label": "Square each part", "content": "<p>\\(1^2 = 1\\), \\((\\sqrt{3})^2 = 3\\)</p>"},
                {"label": "Middle term", "content": "<p>\\(2 \\times 1 \\times \\sqrt{3} = 2\\sqrt{3}\\)</p>"},
                {"label": "Add", "content": "<p>\\(1 + 3 + 2\\sqrt{3} = 4 + 2\\sqrt{3}\\)</p>"},
                {"label": "Answer", "content": "<p><strong>\\(4 + 2\\sqrt{3}\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ================= method_card (slim) =================
pd["method_card"] = {
    "title": "Indices, Surds & Bounds",
    "steps": [
        "Simplify a surd by pulling out the largest square factor",
        "Rationalise: multiply by the surd, or by the conjugate for a two-term denominator",
        "Bounds: half a unit above and below the rounded value",
        "Largest value of a/b: use upper a and lower b",
    ],
    "content": ("<p><strong>Surds</strong> are exact square roots such as \\(\\sqrt{2}\\). "
                "Simplify by pulling out the largest square factor: "
                "\\(\\sqrt{50} = 5\\sqrt{2}\\). Add only like surds: "
                "\\(2\\sqrt{3} + 5\\sqrt{3} = 7\\sqrt{3}\\).</p>"
                "<p><strong>Rationalise</strong> by multiplying top and bottom by the surd, "
                "or by the conjugate \\(a - \\sqrt{b}\\) for a two-term denominator.</p>"
                "<p><strong>Bounds</strong> lie half a unit each side of a rounded value. "
                "To make \\(\\frac{a}{b}\\) largest, use the upper bound of a and the lower bound of b.</p>"),
    "example": pd["method_card"].get("example"),
}

# ================= preserve: fix em dashes in worked_examples labels =================
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

json.dump(pd, open("lesson_maths-ocr_number-L07.json", "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
print("written lesson_maths-ocr_number-L07.json")
