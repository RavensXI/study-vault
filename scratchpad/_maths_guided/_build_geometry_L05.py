# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_geometry_L05.json", encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post:
        d["post"] = post
    if say is not None:
        d["say"] = say
    if done:
        d["done"] = done
    if phase:
        d["phase"] = phase
    return d

def sayonly(text):
    return {"say": text}

# ---------------- METHOD CARD (trimmed) ----------------
method_card = {
    "title": "How to Use Pythagoras & SOHCAHTOA",
    "steps": [
        "Label the sides: hypotenuse (longest, opposite the right angle), then opposite and adjacent relative to the angle.",
        "Two sides and no angle: use Pythagoras. An angle is involved: use SOHCAHTOA.",
        "Substitute into the formula and solve: square root for Pythagoras, or inverse trig for an angle."
    ],
    "content": "<p><strong>Pythagoras:</strong> in a right-angled triangle \\(a^2 + b^2 = c^2\\), where \\(c\\) is the hypotenuse (the longest side, opposite the right angle). To find the hypotenuse, \\(c = \\sqrt{a^2 + b^2}\\); to find a shorter side, subtract: \\(a = \\sqrt{c^2 - b^2}\\).</p><p><strong>SOHCAHTOA</strong> links an angle to two sides: \\(\\sin\\theta = \\frac{O}{H}\\), \\(\\cos\\theta = \\frac{A}{H}\\), \\(\\tan\\theta = \\frac{O}{A}\\). To find a side, rearrange; to find an angle, use \\(\\sin^{-1}\\), \\(\\cos^{-1}\\) or \\(\\tan^{-1}\\). Keep the calculator in degrees.</p>",
    "example": "<p><strong>Find the hypotenuse of a right triangle with sides 5 cm and 12 cm.</strong></p><p>\\(c = \\sqrt{5^2 + 12^2} = \\sqrt{25 + 144} = \\sqrt{169} = 13\\) cm</p>"
}

# ---------------- BRONZE ----------------
bronze = []

# B0: 3,4 -> 5
bronze.append({
    "display": "Find the hypotenuse: sides 3 cm and 4 cm.",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "Square both sides, add them, then square root: the answer is the square root of 3 squared plus 4 squared.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 7,
        "message": "You added the sides: 3 + 4 = 7. Pythagoras squares first: c = √(3² + 4²) = √(9 + 16) = √25 = 5."
    }],
    "guided_steps": [
        box("3² = ", 9, "Three squared is 3 × 3."),
        box("4² = ", 16, "Four squared is 4 × 4."),
        box("Add the squares: 9 + 16 = ", 25, "Just add the two squares."),
        box("Square root to get the hypotenuse: √25 = ", 5, "What number times itself makes 25?", phase="substitute"),
        box("Check: work out 5² = ", 25, "Five squared is 5 × 5.", done="25 matches 9 + 16, so the hypotenuse is 5 cm.")
    ]
})

# B1: 7,24 -> 25 (replaces duplicate 5,12,13)
bronze.append({
    "display": "Find the hypotenuse: sides 7 cm and 24 cm.",
    "solutions": [25], "calculator": False, "input_type": "single_value",
    "hint": "Square both sides, add them, then square root.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 31,
        "message": "You added the sides: 7 + 24 = 31. Square first: c = √(7² + 24²) = √(49 + 576) = √625 = 25."
    }],
    "guided_steps": [
        box("7² = ", 49, "Seven squared is 7 × 7."),
        box("24² = ", 576, "Twenty-four squared is 24 × 24."),
        box("Add the squares: 49 + 576 = ", 625, "Just add the two squares."),
        box("√625 = ", 25, "What number times itself makes 625? Try 25.", phase="substitute"),
        box("Check: work out 25² = ", 625, "25 × 25.", done="625 matches 49 + 576, so the hypotenuse is 25 cm.")
    ]
})

# B2: 8,15 -> 17
bronze.append({
    "display": "Find the hypotenuse: sides 8 cm and 15 cm.",
    "solutions": [17], "calculator": False, "input_type": "single_value",
    "hint": "Square both sides, add them, then square root.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 23,
        "message": "You added the sides: 8 + 15 = 23. Pythagoras squares first: c = √(8² + 15²) = √(64 + 225) = √289 = 17."
    }],
    "guided_steps": [
        box("8² = ", 64, "Eight squared is 8 × 8."),
        box("15² = ", 225, "Fifteen squared is 15 × 15."),
        box("Add the squares: 64 + 225 = ", 289, "Just add the two squares."),
        box("√289 = ", 17, "What number times itself makes 289? Try 17.", phase="substitute"),
        box("Check: work out 17² = ", 289, "17 × 17.", done="289 matches 64 + 225, so the hypotenuse is 17 cm.")
    ]
})

# B3: hyp10, side6 -> 8
bronze.append({
    "display": "Hypotenuse is 10 cm, one side is 6 cm. Find the other side.",
    "solutions": [8], "calculator": False, "input_type": "single_value",
    "hint": "The hypotenuse is known, so subtract: square root of 10 squared minus 6 squared.",
    "misconceptions": [{
        "pattern": "forgot_step", "check": "common", "expect": 11.7,
        "message": "You added: √(10² + 6²) = √136 ≈ 11.7. When the hypotenuse is already known you SUBTRACT: a = √(10² − 6²) = √(100 − 36) = √64 = 8."
    }],
    "guided_steps": [
        box("10² = ", 100, "Ten squared is 10 × 10."),
        box("6² = ", 36, "Six squared is 6 × 6."),
        box("Subtract, because the hypotenuse is known: 100 − 36 = ", 64, "Bigger square minus smaller square."),
        box("√64 = ", 8, "What number times itself makes 64?", phase="substitute"),
        box("Check: 8² + 6² = ", 100, "64 + 36.", done="100 = 10², so the missing side is 8 cm.")
    ]
})

# B4: hyp26, side10 -> 24 (replaces 9,12,15 which was a 3-4-5 scaling)
bronze.append({
    "display": "Hypotenuse is 26 cm, one side is 10 cm. Find the other side.",
    "solutions": [24], "calculator": False, "input_type": "single_value",
    "hint": "The hypotenuse is known, so subtract: square root of 26 squared minus 10 squared.",
    "misconceptions": [{
        "pattern": "forgot_step", "check": "common", "expect": 27.9,
        "message": "You added: √(26² + 10²) = √776 ≈ 27.9. The hypotenuse is known, so SUBTRACT: a = √(26² − 10²) = √(676 − 100) = √576 = 24."
    }],
    "guided_steps": [
        box("26² = ", 676, "Twenty-six squared is 26 × 26."),
        box("10² = ", 100, "Ten squared is 10 × 10."),
        box("Subtract, because the hypotenuse is known: 676 − 100 = ", 576, "Bigger square minus smaller square."),
        box("√576 = ", 24, "What number times itself makes 576? Try 24.", phase="substitute"),
        box("Check: 24² + 10² = ", 676, "576 + 100.", done="676 = 26², so the other side is 24 cm.")
    ]
})

# B5: sin30=0.5, hyp20 -> opp 10
bronze.append({
    "display": "\\(\\sin 30° = 0.5\\). The hypotenuse is 20 cm. Find the opposite side.",
    "solutions": [10], "calculator": False, "input_type": "single_value",
    "hint": "The opposite side is the hypotenuse times the sine: 20 × 0.5.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 40,
        "message": "You divided: 20 ÷ 0.5 = 40. To find the opposite you MULTIPLY: O = H × sin30° = 20 × 0.5 = 10 cm."
    }],
    "guided_steps": [
        box("sin30° = 0.5, and the opposite is the hypotenuse times this. First write the hypotenuse: ", 20, "The longest side, given as 20 cm."),
        box("O = 20 × 0.5 = ", 10, "Multiply, do not divide.", phase="substitute"),
        box("Check: O ÷ H = 10 ÷ 20 = ", 0.5, "Ten divided by twenty.", done="0.5 = sin30°, so the opposite side is 10 cm.")
    ]
})

# B6: cos60=0.5, hyp14 -> adj 7  (changed from hyp16->8 to avoid duplicate answer 8 with B3)
bronze.append({
    "display": "\\(\\cos 60° = 0.5\\). The hypotenuse is 14 cm. Find the adjacent side.",
    "solutions": [7], "calculator": False, "input_type": "single_value",
    "hint": "The adjacent side is the hypotenuse times the cosine: 14 × 0.5.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 28,
        "message": "You divided: 14 ÷ 0.5 = 28. To find the adjacent you MULTIPLY: A = H × cos60° = 14 × 0.5 = 7 cm."
    }],
    "guided_steps": [
        box("cos60° = 0.5, and the adjacent is the hypotenuse times this. First write the hypotenuse: ", 14, "The longest side, given as 14 cm."),
        box("A = 14 × 0.5 = ", 7, "Multiply, do not divide.", phase="substitute"),
        box("Check: A ÷ H = 7 ÷ 14 = ", 0.5, "Seven divided by fourteen.", done="0.5 = cos60°, so the adjacent side is 7 cm.")
    ]
})

# B7: tan = 5/12 -> theta 22.6
bronze.append({
    "display": "\\(\\tan\\theta = \\frac{5}{12}\\). Find \\(\\theta\\) to 1 d.p.",
    "solutions": [22.6], "calculator": True, "input_type": "single_value",
    "hint": "Use the inverse tan button on the ratio: the answer is inverse tan of 5 divided by 12.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 67.4,
        "message": "You may have used 12 ÷ 5 by mistake: tan⁻¹(12 ÷ 5) ≈ 67.4°. The ratio here is 5 over 12, so θ = tan⁻¹(5 ÷ 12) ≈ 22.6°."
    }],
    "guided_steps": [
        box("First work out the ratio: 5 ÷ 12, to 2 d.p. = ", 0.42, "Divide 5 by 12."),
        box("Inverse tan turns the ratio into the angle: θ = tan⁻¹(5 ÷ 12) = ", 22.6, "Press tan⁻¹, then 5 ÷ 12; keep full accuracy, not the rounded 0.42.", phase="substitute"),
        box("Check by going forward: tan22.6°, to 2 d.p. = ", 0.42, "Type tan(22.6) and round to 2 d.p.", done="0.42 matches the ratio, so θ = 22.6°.")
    ]
})

# ---------------- SILVER ----------------
silver = []

# S0: c=13, b=5 -> a=12
silver.append({
    "display": "Find the length of side \\(a\\) in a right triangle where \\(c = 13\\) and \\(b = 5\\).",
    "solutions": [12], "calculator": False, "input_type": "single_value",
    "hint": "c is the hypotenuse, so subtract: a = square root of 13 squared minus 5 squared.",
    "misconceptions": [{
        "pattern": "forgot_step", "check": "common", "expect": 13.9,
        "message": "You added: √(13² + 5²) = √194 ≈ 13.9. Because c is the hypotenuse you SUBTRACT: a = √(13² − 5²) = √(169 − 25) = √144 = 12."
    }],
    "guided_steps": [
        box("13² = ", 169, "Thirteen squared is 13 × 13."),
        box("5² = ", 25, "Five squared is 5 × 5."),
        box("c is the hypotenuse, so subtract: 169 − 25 = ", 144, "Bigger square minus smaller square."),
        box("√144 = ", 12, "What number times itself makes 144?", phase="substitute"),
        box("Check: 12² + 5² = ", 169, "144 + 25.", done="169 = 13², so a = 12.")
    ]
})

# S1: opp8, adj6 -> theta 53.1
silver.append({
    "display": "The opposite side is 8 cm and the adjacent side is 6 cm. Find \\(\\theta\\) to 1 d.p.",
    "solutions": [53.1], "calculator": True, "input_type": "single_value",
    "hint": "Opposite and adjacent point to tan: the answer is inverse tan of 8 divided by 6.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 36.9,
        "message": "You may have divided 6 by 8: tan⁻¹(6 ÷ 8) ≈ 36.9°. Opposite over adjacent is 8 over 6, so θ = tan⁻¹(8 ÷ 6) ≈ 53.1°."
    }],
    "guided_steps": [
        box("Opposite over adjacent: 8 ÷ 6, to 2 d.p. = ", 1.33, "Divide 8 by 6."),
        box("θ = tan⁻¹(8 ÷ 6) = ", 53.1, "Press tan⁻¹, then 8 ÷ 6; keep full accuracy.", phase="substitute"),
        box("Check: tan53.1°, to 2 d.p. = ", 1.33, "Type tan(53.1) and round to 2 d.p.", done="1.33 matches 8 ÷ 6, so θ = 53.1°.")
    ]
})

# S2: theta=40, hyp=12 -> adjacent 9.2
silver.append({
    "display": "Find the adjacent side when \\(\\theta = 40°\\) and hypotenuse = 12 cm. Give answer to 1 d.p.",
    "solutions": [9.2], "calculator": True, "input_type": "single_value",
    "hint": "Adjacent with hypotenuse points to cos: A = 12 × cos40°.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 7.7,
        "message": "You may have used sine: 12 × sin40° ≈ 7.7. Adjacent with hypotenuse means cosine: A = 12 × cos40° = 12 × 0.766 ≈ 9.2 cm."
    }],
    "guided_steps": [
        box("cos40°, to 2 d.p. = ", 0.77, "Type cos(40) on the calculator."),
        box("A = 12 × cos40° = ", 9.2, "Multiply the hypotenuse by cos40°, keeping full accuracy.", phase="substitute"),
        box("Check: A ÷ H = 9.2 ÷ 12, to 2 d.p. = ", 0.77, "9.2 divided by 12.", done="0.77 = cos40°, so the adjacent side is 9.2 cm.")
    ]
})

# S3: theta=35, adj=10 -> opposite 7.0  (solutions fix [7,7] -> [7.0])
silver.append({
    "display": "Find the opposite side when \\(\\theta = 35°\\) and adjacent = 10 cm. Give answer to 1 d.p.",
    "solutions": [7.0], "calculator": True, "input_type": "single_value",
    "hint": "Opposite with adjacent points to tan: O = 10 × tan35°.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 5.7,
        "message": "You may have used sine: 10 × sin35° ≈ 5.7. Opposite with adjacent means tangent: O = 10 × tan35° = 10 × 0.700 ≈ 7.0 cm."
    }],
    "guided_steps": [
        box("tan35°, to 2 d.p. = ", 0.7, "Type tan(35) on the calculator."),
        box("O = 10 × tan35° = ", 7.0, "Multiply the adjacent by tan35°.", phase="substitute"),
        box("Check: O ÷ A = 7 ÷ 10 = ", 0.7, "Seven divided by ten.", done="0.70 = tan35°, so the opposite side is 7.0 cm.")
    ]
})

# S4: ladder 6, base 2 -> height 5.7
silver.append({
    "display": "A ladder 6 m long leans against a wall. Its base is 2 m from the wall. How high up the wall does it reach? (to 1 d.p.)",
    "solutions": [5.7], "calculator": True, "input_type": "single_value",
    "hint": "The ladder is the hypotenuse, so subtract: height = square root of 6 squared minus 2 squared.",
    "misconceptions": [{
        "pattern": "forgot_step", "check": "common", "expect": 6.3,
        "message": "You added: √(6² + 2²) = √40 ≈ 6.3. The ladder is the hypotenuse, so SUBTRACT: h = √(6² − 2²) = √(36 − 4) = √32 ≈ 5.7 m."
    }],
    "guided_steps": [
        box("6² = ", 36, "Six squared is 6 × 6."),
        box("2² = ", 4, "Two squared is 2 × 2."),
        box("The ladder is the hypotenuse, so subtract: 36 − 4 = ", 32, "Bigger square minus smaller square."),
        box("√32, to 1 d.p. = ", 5.7, "Square root of 32 on the calculator.", phase="substitute"),
        box("Check: 5.7² + 2², to the nearest whole number, = ", 36, "Work out 5.7² + 4 and round.", done="36 = 6², so the height 5.7 m checks out.")
    ]
})

# S5: opp12, hyp20 -> theta 36.9
silver.append({
    "display": "Find angle \\(\\theta\\) if opposite = 12 cm and hypotenuse = 20 cm. Give to 1 d.p.",
    "solutions": [36.9], "calculator": True, "input_type": "single_value",
    "hint": "Opposite with hypotenuse points to sin: the answer is inverse sin of 12 divided by 20.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 53.1,
        "message": "You may have used cos⁻¹: cos⁻¹(12 ÷ 20) ≈ 53.1°. Opposite with hypotenuse means sine: θ = sin⁻¹(12 ÷ 20) = sin⁻¹(0.6) ≈ 36.9°."
    }],
    "guided_steps": [
        box("Opposite over hypotenuse: 12 ÷ 20 = ", 0.6, "Divide 12 by 20."),
        box("θ = sin⁻¹(0.6) = ", 36.9, "Press sin⁻¹, then 0.6.", phase="substitute"),
        box("Check: sin36.9°, to 1 d.p. = ", 0.6, "Type sin(36.9) and round to 1 d.p.", done="0.6 matches 12 ÷ 20, so θ = 36.9°.")
    ]
})

# S6: isosceles equal sides 10, base 12 -> height 8
silver.append({
    "display": "An isosceles triangle has two equal sides of 10 cm and a base of 12 cm. Find the height to 1 d.p.",
    "solutions": [8], "calculator": False, "input_type": "single_value",
    "hint": "Split it down the middle: the height, half the base (6) and a slant side (10) form a right triangle.",
    "misconceptions": [{
        "pattern": "forgot_step", "check": "common", "expect": None,
        "message": "Drop the height to the middle of the base. That makes a right triangle with hypotenuse 10 and base 6 (half of 12): h = √(10² − 6²) = √64 = 8 cm. Using the full base of 12 has no real answer, so always halve it first.",
        "note": "Forgetting to halve gives sqrt(100-144) which is not real, so no single determinate wrong value: expect null."
    }],
    "guided_steps": [
        box("Half the base: 12 ÷ 2 = ", 6, "The height splits the base into two equal halves."),
        box("The slant side is the hypotenuse: 10² = ", 100, "Ten squared is 10 × 10."),
        box("6² = ", 36, "Six squared is 6 × 6."),
        box("Subtract: 100 − 36 = ", 64, "Bigger square minus smaller square."),
        box("√64 = ", 8, "What number times itself makes 64?", phase="substitute"),
        box("Check: 8² + 6² = ", 100, "64 + 36.", done="100 = 10², so the height is 8 cm.")
    ]
})

# ---------------- GOLD ----------------
gold = []

# G0: ship 15 east, 20 north -> 25
gold.append({
    "display": "A ship sails 15 km east then 20 km north. Find the direct distance back to start (to 1 d.p.).",
    "solutions": [25], "calculator": False, "input_type": "single_value",
    "hint": "The two legs are 15 and 20; the direct distance is the hypotenuse.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 35,
        "message": "You added the distances: 15 + 20 = 35. The straight line back is the hypotenuse: d = √(15² + 20²) = √(225 + 400) = √625 = 25 km."
    }],
    "guided_steps": [
        box("East leg squared: 15² = ", 225, "Fifteen squared is 15 × 15."),
        box("North leg squared: 20² = ", 400, "Twenty squared is 20 × 20."),
        box("Add: 225 + 400 = ", 625, "Just add the two squares."),
        box("√625 = ", 25, "What number times itself makes 625? Try 25.", phase="substitute"),
        box("Check: 25² = ", 625, "25 × 25.", done="625 = 225 + 400, so the ship is 25 km from the start.")
    ]
})

# G1: elevation, 50 away, height 30 -> 31.0  (solutions fix [31,30.96,31] -> [31.0])
gold.append({
    "display": "Find the angle of elevation from a point 50 m from a tower, to the top of the tower (height 30 m). Give to 1 d.p.",
    "solutions": [31.0], "calculator": True, "input_type": "single_value",
    "hint": "Height is opposite, distance is adjacent, so use tan: the answer is inverse tan of 30 divided by 50.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 36.9,
        "message": "You may have used sin⁻¹, treating 50 m as the hypotenuse: sin⁻¹(30 ÷ 50) ≈ 36.9°. But 50 m is the horizontal distance (adjacent), so use tan: θ = tan⁻¹(30 ÷ 50) ≈ 31.0°."
    }],
    "guided_steps": [
        box("Opposite (height) over adjacent (distance): 30 ÷ 50 = ", 0.6, "Divide 30 by 50."),
        box("θ = tan⁻¹(0.6) = ", 31.0, "Press tan⁻¹, then 0.6.", phase="substitute"),
        box("Check: tan31°, to 1 d.p. = ", 0.6, "Type tan(31) and round to 1 d.p.", done="0.6 matches 30 ÷ 50, so the angle of elevation is 31.0°.")
    ]
})

# G2: NEW algebraic Pythagoras, sides x, x+1, hyp x+2 -> x=3  (replaces broken surd problem)
gold.append({
    "display": "A right-angled triangle has shorter sides \\(x\\) and \\(x + 1\\), and hypotenuse \\(x + 2\\). Find \\(x\\).",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Write Pythagoras as x² + (x+1)² = (x+2)², expand every bracket, then solve the equation.",
    "misconceptions": [{
        "pattern": "added_not_squared", "check": "common", "expect": 1,
        "message": "You may have added the sides without squaring: x + (x+1) = x+2 gives x = 1. Pythagoras squares each side: x² + (x+1)² = (x+2)², which gives x = 3.",
        "note": "Linear (unsquared) x+(x+1)=x+2 -> 2x+1=x+2 -> x=1. Also dropping the (x+2)^2 middle term gives x=1."
    }],
    "guided_steps": [
        box("Expand (x + 1)² = x² + ?x + 1. The middle number (2 × 1) is ", 2, "Twice the product: 2 × 1 = 2, so the term is 2x."),
        box("Expand (x + 2)² = x² + ?x + 4. The middle number (2 × 2) is ", 4, "Twice the product: 2 × 2 = 4, so the term is 4x."),
        sayonly("So the equation is x² + (x² + 2x + 1) = x² + 4x + 4. On the left, x² + x² = 2x²; take x² from both sides and one x² is left. Now collect the x terms and the constants."),
        box("The x term: left has 2x, right has 4x. 2 − 4 = ", -2, "Two minus four."),
        box("The constant: left has 1, right has 4. 1 − 4 = ", -3, "One minus four."),
        box("That gives x² − 2x − 3 = 0, which factorises as (x − 3)(x + 1) = 0. The positive length is x = ", 3, "Two numbers multiplying to −3 and adding to −2 are −3 and +1; a length must be positive.", phase="substitute"),
        box("Check the sides 3, 4, 5: 3² + 4² = ", 25, "9 + 16.", done="25 = 5², so x = 3 gives a 3, 4, 5 triangle.")
    ]
})

# G3: cliff 40, depression 25 -> distance 85.8
gold.append({
    "display": "From the top of a 40 m cliff, the angle of depression to a boat is \\(25°\\). How far is the boat from the base of the cliff? (to 1 d.p.)",
    "solutions": [85.8], "calculator": True, "input_type": "single_value",
    "hint": "The 40 m height is opposite the 25° angle and the distance is adjacent, so distance = 40 ÷ tan25°.",
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": 18.7,
        "message": "You multiplied: 40 × tan25° ≈ 18.7. Here the height is opposite and the distance is adjacent, and the height is known, so DIVIDE: d = 40 ÷ tan25° ≈ 85.8 m."
    }],
    "guided_steps": [
        sayonly("The angle of depression from the top equals the angle of elevation at the boat, 25°. The height (40 m) is opposite that angle and the distance is adjacent, so tan25° = 40 ÷ distance, which rearranges to distance = 40 ÷ tan25°."),
        box("tan25°, to 3 d.p. = ", 0.466, "Type tan(25) on the calculator."),
        box("d = 40 ÷ tan25° = ", 85.8, "Divide 40 by tan25°, keeping full accuracy.", phase="substitute"),
        box("Check: 85.8 × tan25° ≈ ", 40, "85.8 × 0.466, rounded to the nearest whole number.", done="That returns the 40 m height, so the boat is 85.8 m away.")
    ]
})

# G4: rectangle diagonal 17, width 8 -> length 15
gold.append({
    "display": "A rectangle has diagonal 17 cm and width 8 cm. Find the length.",
    "solutions": [15], "calculator": False, "input_type": "single_value",
    "hint": "The diagonal is the hypotenuse of a right triangle with the width and length, so length = square root of 17 squared minus 8 squared.",
    "misconceptions": [{
        "pattern": "forgot_step", "check": "common", "expect": 18.8,
        "message": "You added: √(17² + 8²) = √353 ≈ 18.8. The diagonal is the hypotenuse, so SUBTRACT: length = √(17² − 8²) = √(289 − 64) = √225 = 15 cm."
    }],
    "guided_steps": [
        box("The diagonal is the hypotenuse: 17² = ", 289, "Seventeen squared is 17 × 17."),
        box("8² = ", 64, "Eight squared is 8 × 8."),
        box("Subtract: 289 − 64 = ", 225, "Bigger square minus smaller square."),
        box("√225 = ", 15, "What number times itself makes 225?", phase="substitute"),
        box("Check: 15² + 8² = ", 289, "225 + 64.", done="289 = 17², so the length is 15 cm.")
    ]
})

problem_bank = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "Put the given numbers straight into one formula: square, add or subtract and root for Pythagoras, or multiply by a given sine or cosine for a side.",
    "silver_description": "Decide the method first, then rearrange it: choose Pythagoras or the right trig ratio, substitute and solve, often with a calculator or inside a real shape.",
    "gold_description": "Turn a worded or real situation into a right-angled triangle, then finish with Pythagoras or trigonometry; some problems need a little algebra."
}

# ---------------- TIER GUIDES ----------------
tier_guides = {
    "bronze": {
        "title": "Bronze: one formula, straight in",
        "steps": [
            "Read the two known values straight off the triangle. No rearranging needed yet.",
            "For Pythagoras, square both sides then add for the hypotenuse, or subtract then square root for a shorter side.",
            "For a trig side you are given the ratio (like \\(\\sin 30° = 0.5\\)): multiply the hypotenuse by it. For an angle, use \\(\\tan^{-1}\\) on the ratio."
        ],
        "example": {
            "question": "Find the hypotenuse: sides 6 cm and 8 cm.",
            "steps": [
                {"label": "Square and add", "content": "<p>\\(6^2 + 8^2 = 36 + 64 = 100\\)</p>"},
                {"label": "Square root", "content": "<p>\\(c = \\sqrt{100} = 10\\)</p>"},
                {"label": "Check", "content": "<p>\\(6^2 + 8^2 = 100 = 10^2\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(c = 10\\) cm</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: choose and rearrange",
        "steps": [
            "Nothing is handed to you ready to use. First decide: Pythagoras (three sides, no angle) or a trig ratio (an angle is involved).",
            "Pick the ratio that pairs your two sides: \\(\\sin\\) for O and H, \\(\\cos\\) for A and H, \\(\\tan\\) for O and A. Rearrange to make the unknown the subject.",
            "Real shapes count too: split an isosceles triangle down the middle, or read the diagonal of a rectangle as a hypotenuse."
        ],
        "example": {
            "question": "Find the opposite side when \\(\\theta = 30°\\) and the hypotenuse is 14 cm.",
            "steps": [
                {"label": "Choose ratio", "content": "<p>Opposite and hypotenuse, so \\(\\sin\\theta = \\frac{O}{H}\\), giving \\(O = H\\sin\\theta\\).</p>"},
                {"label": "Substitute", "content": "<p>\\(O = 14 \\times \\sin 30° = 14 \\times 0.5 = 7\\)</p>"},
                {"label": "Check", "content": "<p>\\(7 \\div 14 = 0.5 = \\sin 30°\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(O = 7\\) cm</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: build the triangle from the words",
        "steps": [
            "The right triangle is hidden in a story or a shape. Sketch it and label the sides you are told.",
            "Journeys and bearings give two legs (find the hypotenuse). Elevation and depression give an angle with a height and a distance (use \\(\\tan\\)).",
            "Some problems are algebraic: write \\(a^2 + b^2 = c^2\\) with \\(x\\) in the sides, expand carefully, and solve the equation."
        ],
        "example": {
            "question": "A ship sails 9 km east then 12 km north. How far is it from the start?",
            "steps": [
                {"label": "Set up", "content": "<p>The two legs are 9 and 12; the direct distance is the hypotenuse.</p>"},
                {"label": "Pythagoras", "content": "<p>\\(9^2 + 12^2 = 81 + 144 = 225\\)</p>"},
                {"label": "Check", "content": "<p>\\(\\sqrt{225} = 15\\), and \\(15^2 = 225\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(15\\) km</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------- GUIDED (opener + teach) ----------------
guided = {
    "opener": {
        "label": "Before any formula",
        "display": "A right angle, with a tiled square on each side.<br>Short sides: a 3×3 square (9 tiles) and a 4×4 square (16 tiles).",
        "steps": [
            {
                "say": "Here is a right-angled triangle with a square tiled onto each side. No formula needed, just count and add.",
                "pre": "The two smaller squares hold 9 tiles and 16 tiles. Altogether that is 9 + 16 = ",
                "answer": 25,
                "hint": "Just add the two tile counts."
            },
            {
                "say": "The clever bit: the square on the longest side holds exactly that many tiles too, 25. That is Pythagoras, the two smaller squares add up to the biggest one.",
                "pre": "A square made of 25 tiles is how many tiles along each edge? ",
                "answer": 5,
                "hint": "What number times itself makes 25?"
            },
            {
                "say": "So the longest side is 5. In symbols, the short sides \\(a\\) and \\(b\\) and the longest side \\(c\\) obey \\(a^2 + b^2 = c^2\\). Squaring a side just counts the tiles in its square; square rooting turns the tile count back into a length."
            }
        ]
    },
    "teach": {
        "bronze": {
            "display": "Find the hypotenuse of a right triangle with shorter sides 12 cm and 16 cm.",
            "label": "Together: your first one",
            "steps": [
                sayonly("The two shorter sides are 12 and 16. Pythagoras says: square each, add, then square root."),
                box("12² = ", 144, "12 × 12."),
                box("16² = ", 256, "16 × 16."),
                box("Add the squares: 144 + 256 = ", 400, "Just add them."),
                box("Square root to get the hypotenuse: √400 = ", 20, "What number times itself makes 400? Try 20.", done="Square, add, root. That is the whole method."),
                box("Check: 20² = ", 400, "20 × 20.", done="400 = 144 + 256, so the hypotenuse is 20 cm.")
            ]
        },
        "silver": {
            "display": "In a right triangle the opposite side is 9 cm and the adjacent side is 12 cm. Find the angle \\(\\theta\\) to 1 d.p.",
            "label": "Together: the silver move",
            "steps": [
                sayonly("You know the opposite and the adjacent, so the ratio is tan. To get the angle back, use inverse tan, the new move at this level."),
                box("The ratio, opposite ÷ adjacent: 9 ÷ 12 = ", 0.75, "Divide 9 by 12."),
                box("Inverse tan turns that ratio into the angle: θ = tan⁻¹(0.75) = ", 36.9, "Press tan⁻¹, then 0.75.", done="Inverse tan undoes tan to reveal the angle. That was the point."),
                box("The two acute angles add to 90°, so the other one is 90 − 36.9 = ", 53.1, "Ninety minus 36.9."),
                box("Check: tan36.9°, to 2 d.p. = ", 0.75, "Type tan(36.9) and round to 2 d.p.", done="0.75 matches 9 ÷ 12, so θ = 36.9°.")
            ]
        },
        "gold": {
            "display": "A ramp rises 1.5 m over a horizontal run of 8 m. Find the angle the ramp makes with the ground, to 1 d.p.",
            "label": "Together: the gold move",
            "steps": [
                sayonly("Draw the right triangle out of the words: the rise, 1.5 m, is opposite the angle; the run, 8 m, is adjacent. Opposite and adjacent means tan."),
                box("The ratio, rise ÷ run: 1.5 ÷ 8, to 2 d.p. = ", 0.19, "Divide 1.5 by 8."),
                box("Inverse tan gives the angle: θ = tan⁻¹(1.5 ÷ 8) = ", 10.6, "Press tan⁻¹, then 1.5 ÷ 8; keep full accuracy.", done="Reading the triangle out of the words is the gold move."),
                box("Check: tan10.6°, to 2 d.p. = ", 0.19, "Type tan(10.6) and round to 2 d.p.", done="0.19 matches the ratio, so the ramp sits at 10.6°."),
                box("The ramp itself is the hypotenuse: √(1.5² + 8²) = √66.25, to 1 d.p. = ", 8.1, "Square root of 66.25 on the calculator.", done="Same triangle, Pythagoras gives the ramp's length: 8.1 m.")
            ]
        }
    }
}

# ---------------- ASSEMBLE (preserve untouched fields) ----------------
pd = dict(live)  # shallow copy preserves related_videos, topic_links, worked_examples
# Minimal style fix: an em dash in a preserved worked_examples label is banned by the
# hard no-em-dash rule (student-facing). Replace em dash with a colon in labels only.
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str) and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")
pd["method_card"] = method_card
pd["problem_bank"] = problem_bank
pd["tier_guides"] = tier_guides
pd["guided"] = guided

json.dump(pd, io.open("lesson_geometry-L05.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_geometry-L05.json")
print("bronze sols:", [p["solutions"] for p in bronze])
print("silver sols:", [p["solutions"] for p in silver])
print("gold sols:", [p["solutions"] for p in gold])
