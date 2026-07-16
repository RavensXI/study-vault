# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_L07.json", encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post: d["post"] = post
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def say(text):
    return {"say": text}

def mc(pattern, expect, message):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}

# ---------------------------------------------------------------- BRONZE
bronze = [
 {  # B0  16^(1/2) = 4
  "display": "Evaluate \\(16^{\\frac{1}{2}}\\)",
  "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "A power of a half means take the square root.",
  "misconceptions": [
    mc("halve", 8, "A power of a half means square root, not halving. Half of 16 is 8, but the square root of 16 is 4."),
    mc("wrong_root", None, "The bottom of the fraction is the root. It is 2, so take the square root: the square root of 16 is 4."),
  ],
  "guided_steps": [
    say("A power of ½ means a square root, so read \\(16^{1/2}\\) as \\(\\sqrt{16}\\)."),
    box("√16 asks which number squared makes 16. Work out 4 × 4 = ", 16, "Multiply 4 by itself."),
    box("That lands on 16, so √16 = ", 4, "It is the number you just squared.", phase="substitute"),
    box("Check by squaring: 4 × 4 = ", 16, "Multiply 4 by itself once more.", done="Squares back to 16, so 16^(1/2) = 4."),
  ],
 },
 {  # B1  8^(1/3) = 2
  "display": "Evaluate \\(8^{\\frac{1}{3}}\\)",
  "solutions": [2], "calculator": False, "input_type": "single_value",
  "hint": "A power of a third means take the cube root.",
  "misconceptions": [
    mc("divide_by_3", None, "A power of a third is a cube root, not dividing by 3. The cube root of 8 is 2 because 2 times 2 times 2 is 8."),
  ],
  "guided_steps": [
    say("A power of ⅓ means a cube root: which number cubed gives 8?"),
    box("Try 2: 2 × 2 × 2 = ", 8, "Multiply 2 by itself, then by 2 again."),
    box("That lands on 8, so ∛8 = ", 2, "It is the number you just cubed.", phase="substitute"),
    box("Check: 2 × 2 × 2 = ", 8, "Cube the 2 once more.", done="Rebuilds 8, so 8^(1/3) = 2."),
  ],
 },
 {  # B2  3^-2 = 1/9
  "display": "Evaluate \\(3^{-2}\\)",
  "solutions": [1, 9], "calculator": False, "input_type": "fraction",
  "hint": "A negative power means one over the positive power, so find 3 squared first.",
  "misconceptions": [
    mc("negative_answer", -9, "A negative index means a reciprocal, not a negative answer. 3 to the power negative 2 is 1 over 3 squared, which is 1 over 9."),
    mc("subtract", 1, "The index is not a subtraction. 3 to the power negative 2 is 1 over 9, not 3 minus 2."),
  ],
  "guided_steps": [
    say("A negative power flips it: \\(3^{-2} = \\frac{1}{3^{2}}\\)."),
    box("First the bottom: 3² = 3 × 3 = ", 9, "Multiply 3 by itself."),
    box("The flip puts 1 on top. Numerator = ", 1, "A reciprocal always has 1 on top.", phase="substitute"),
    box("Denominator = ", 9, "It is the 3 squared you just found.", done="So 3⁻² = 1/9."),
  ],
 },
 {  # B3  sqrt50 = 5 root2
  "display": "Simplify \\(\\sqrt{50}\\). Enter the number in front of \\(\\sqrt{2}\\).",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Pull out the biggest square factor of 50, which is 25.",
  "misconceptions": [
    mc("divide_not_factor", 25, "Do not just divide 50 by 2. Simplify with the biggest square factor: 50 is 25 times 2, and the square root of 25 is 5, so the answer is 5 root 2."),
    mc("not_simplified", None, "Find the biggest square factor of 50, which is 25, so root 50 is 5 root 2."),
  ],
  "guided_steps": [
    say("Look for the biggest square number that divides 50. That is 25, and \\(25 = 5^2\\)."),
    box("Split it: 50 = 25 × ", 2, "50 ÷ 25."),
    box("√25 = ", 5, "5 × 5 = 25.", phase="substitute"),
    box("So √50 = 5√2. Rebuild to check: 5 × 5 × 2 = ", 50, "25 × 2.", done="Rebuilds 50, so the number in front is 5."),
  ],
 },
 {  # B4  2^-3 = 1/8
  "display": "Evaluate \\(2^{-3}\\)",
  "solutions": [1, 8], "calculator": False, "input_type": "fraction",
  "hint": "A negative power means one over the positive power, so find 2 cubed first.",
  "misconceptions": [
    mc("negative_answer", -8, "A negative index means a reciprocal, not a negative answer. 2 to the power negative 3 is 1 over 2 cubed, which is 1 over 8."),
    mc("wrong_calc", None, "2 cubed is 8, so 2 to the power negative 3 is 1 over 8."),
  ],
  "guided_steps": [
    say("A negative power flips it: \\(2^{-3} = \\frac{1}{2^{3}}\\)."),
    box("First the bottom: 2³ = 2 × 2 × 2 = ", 8, "Multiply 2 by itself twice."),
    box("The flip puts 1 on top. Numerator = ", 1, "A reciprocal always has 1 on top.", phase="substitute"),
    box("Denominator = ", 8, "It is the 2 cubed you just found.", done="So 2⁻³ = 1/8."),
  ],
 },
 {  # B5  12.4 lower bound = 12.35
  "display": "A length is \\(12.4\\) cm rounded to 1 d.p. Find the lower bound.",
  "solutions": [12.35], "calculator": False, "input_type": "single_value",
  "hint": "For 1 decimal place the half unit is 0.05; take it off for the lower bound.",
  "misconceptions": [
    mc("wrong_half_unit", 12.3, "Half a unit for 1 decimal place is 0.05, not 0.1. Lower bound is 12.4 minus 0.05, which is 12.35."),
    mc("subtract_1", 11.4, "Do not subtract 1. The half unit for 1 decimal place is 0.05, so 12.4 minus 0.05 is 12.35."),
  ],
  "guided_steps": [
    say("1 d.p. means rounded to the nearest 0.1, so the true value can be up to half of 0.1 away."),
    box("Half unit = 0.1 ÷ 2 = ", 0.05, "Split 0.1 in two."),
    box("Lower bound = 12.4 − 0.05 = ", 12.35, "Take the half unit off.", phase="substitute"),
    box("Check the gap: 12.4 − 12.35 = ", 0.05, "Subtract to see the distance.", done="Exactly half a unit below, so the lower bound is 12.35."),
  ],
 },
 {  # B6  sqrt18 = 3 root2
  "display": "Simplify \\(\\sqrt{18}\\). Enter the number in front of \\(\\sqrt{2}\\).",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "Pull out the biggest square factor of 18, which is 9.",
  "misconceptions": [
    mc("divide_not_factor", 9, "Do not just divide 18 by 2. The biggest square factor of 18 is 9, and the square root of 9 is 3, so the answer is 3 root 2."),
    mc("not_simplified", None, "The biggest square factor of 18 is 9, so root 18 is 3 root 2."),
  ],
  "guided_steps": [
    say("Look for the biggest square number that divides 18. That is 9, and \\(9 = 3^2\\)."),
    box("Split it: 18 = 9 × ", 2, "18 ÷ 9."),
    box("√9 = ", 3, "3 × 3 = 9.", phase="substitute"),
    box("So √18 = 3√2. Rebuild to check: 3 × 3 × 2 = ", 18, "9 × 2.", done="Rebuilds 18, so the number in front is 3."),
  ],
 },
 {  # B7  36^(1/2) = 6   (was 25^(1/2)=5, changed to remove duplicate 5)
  "display": "Evaluate \\(36^{\\frac{1}{2}}\\)",
  "solutions": [6], "calculator": False, "input_type": "single_value",
  "hint": "A power of a half means take the square root.",
  "misconceptions": [
    mc("halve", 18, "A power of a half means square root, not halving. Half of 36 is 18, but the square root of 36 is 6."),
    mc("wrong_root", None, "The bottom of the fraction is the root, here 2, so take the square root: the square root of 36 is 6."),
  ],
  "guided_steps": [
    say("A power of ½ means a square root, so read \\(36^{1/2}\\) as \\(\\sqrt{36}\\)."),
    box("√36 asks which number squared makes 36. Work out 6 × 6 = ", 36, "Multiply 6 by itself."),
    box("That lands on 36, so √36 = ", 6, "It is the number you just squared.", phase="substitute"),
    box("Check by squaring: 6 × 6 = ", 36, "Multiply 6 by itself once more.", done="Squares back to 36, so 36^(1/2) = 6."),
  ],
 },
]

# ---------------------------------------------------------------- SILVER
silver = [
 {  # S0  27^(2/3) = 9
  "display": "Evaluate \\(27^{\\frac{2}{3}}\\)",
  "solutions": [9], "calculator": False, "input_type": "single_value",
  "hint": "Take the cube root first, then square the result.",
  "misconceptions": [
    mc("wrong_base", 3, "You found the cube root, root 27 is 3, but stopped. The top number 2 means square it: 3 squared is 9."),
    mc("multiply_fraction", 18, "Do not multiply 27 by two thirds. The fraction means a root and a power: the cube root of 27 is 3, then 3 squared is 9."),
  ],
  "guided_steps": [
    say("The bottom of the fraction is the root, the top is the power. Do the root first."),
    box("Cube root first: ∛27 = ", 3, "Which number cubed gives 27?"),
    box("Now the power 2: 3² = ", 9, "3 × 3.", phase="substitute"),
    box("Rebuild the root to check: 3 × 3 × 3 = ", 27, "Cube the 3.", done="∛27 = 3 confirmed, so 27^(2/3) = 9."),
  ],
 },
 {  # S1  16^(3/4) = 8
  "display": "Evaluate \\(16^{\\frac{3}{4}}\\)",
  "solutions": [8], "calculator": False, "input_type": "single_value",
  "hint": "Take the fourth root first, then cube the result.",
  "misconceptions": [
    mc("wrong_root", 64, "The bottom number 4 means the fourth root, which is 2 because 2 to the power 4 is 16. Using the square root gives 4, then 4 cubed is 64, which is the slip."),
    mc("multiply_fraction", 12, "Do not multiply 16 by three quarters. Take the fourth root first, which is 2, then cube it: 2 cubed is 8."),
  ],
  "guided_steps": [
    say("The bottom 4 is a fourth root, the top 3 is a power. Root first."),
    box("Fourth root first: which number to the power 4 gives 16? 2 × 2 × 2 × 2 = ", 16, "Multiply 2 by itself four times."),
    box("So 16^(1/4) = 2. Now the power 3: 2³ = ", 8, "2 × 2 × 2.", phase="substitute"),
    box("Check the root: 2 × 2 × 2 × 2 = ", 16, "Raise 2 to the fourth power again.", done="16^(1/4) = 2 confirmed, so 16^(3/4) = 8."),
  ],
 },
 {  # S2  sqrt200 = 10 root2
  "display": "Simplify \\(\\sqrt{200}\\). Enter the number in front of \\(\\sqrt{2}\\).",
  "solutions": [10], "calculator": False, "input_type": "single_value",
  "hint": "The biggest square factor of 200 is 100.",
  "misconceptions": [
    mc("not_fully_simplified", 2, "Using the factor 4 gives root 200 as 2 root 50, which is not finished. The biggest square factor is 100, so root 200 is 10 root 2."),
    mc("divide_not_factor", 100, "Do not just divide 200 by 2. The biggest square factor is 100, and the square root of 100 is 10, so root 200 is 10 root 2."),
  ],
  "guided_steps": [
    say("Look for the biggest square number that divides 200. That is 100, and \\(100 = 10^2\\)."),
    box("Split it: 200 = 100 × ", 2, "200 ÷ 100."),
    box("√100 = ", 10, "10 × 10 = 100.", phase="substitute"),
    box("So √200 = 10√2. Rebuild to check: 10 × 10 × 2 = ", 200, "100 × 2.", done="Rebuilds 200, so the number in front is 10."),
  ],
 },
 {  # S3  6/sqrt2 = 3 root2   (was 4/sqrt2=2, changed to remove duplicate 2)
  "display": "Rationalise \\(\\frac{6}{\\sqrt{2}}\\). Give the number in front of \\(\\sqrt{2}\\).",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "Multiply top and bottom by root 2, then simplify.",
  "misconceptions": [
    mc("no_rationalise", 6, "Rationalise by multiplying top and bottom by root 2: 6 root 2 over 2 is 3 root 2. The number in front is 3, not 6."),
    mc("wrong_simplify", None, "After multiplying, 6 root 2 over 2 simplifies to 3 root 2 because 6 divided by 2 is 3."),
  ],
  "guided_steps": [
    say("Clear the surd on the bottom by multiplying top and bottom by \\(\\sqrt{2}\\)."),
    box("Bottom becomes √2 × √2 = ", 2, "A root times itself is just the number inside."),
    box("Top becomes 6√2, so divide the whole numbers: 6 ÷ 2 = ", 3, "6 divided by 2.", phase="substitute"),
    box("So 6/√2 = 3√2. Check: (3√2)² = 9 × 2 = 18, and (6/√2)² = 36 ÷ 2 = ", 18, "Square 6 then divide by 2.", done="Both give 18, so the number in front is 3."),
  ],
 },
 {  # S4  3.6 upper bound = 3.65
  "display": "A weight is \\(3.6\\) kg rounded to 1 d.p. Find the upper bound.",
  "solutions": [3.65], "calculator": False, "input_type": "single_value",
  "hint": "For 1 decimal place the half unit is 0.05; add it on for the upper bound.",
  "misconceptions": [
    mc("wrong_half_unit", 3.7, "Half a unit for 1 decimal place is 0.05, not 0.1. Upper bound is 3.6 plus 0.05, which is 3.65."),
    mc("add_1", 4.6, "Do not add 1. The half unit for 1 decimal place is 0.05, so the upper bound is 3.6 plus 0.05, which is 3.65."),
  ],
  "guided_steps": [
    say("1 d.p. means rounded to the nearest 0.1, so the true value can be up to half of 0.1 away."),
    box("Half unit = 0.1 ÷ 2 = ", 0.05, "Split 0.1 in two."),
    box("Upper bound = 3.6 + 0.05 = ", 3.65, "Add the half unit on.", phase="substitute"),
    box("Check the gap: 3.65 − 3.6 = ", 0.05, "Subtract to see the distance.", done="Exactly half a unit above, so the upper bound is 3.65."),
  ],
 },
 {  # S5  3 sqrt8 = 6 root2
  "display": "Simplify \\(3\\sqrt{8}\\). Express as \\(a\\sqrt{2}\\). Find \\(a\\).",
  "solutions": [6], "calculator": False, "input_type": "single_value",
  "hint": "Simplify root 8 to 2 root 2 first, then multiply by the 3.",
  "misconceptions": [
    mc("no_simplify", 3, "Simplify root 8 first. Root 8 is 2 root 2, so 3 root 8 is 3 times 2 root 2, which is 6 root 2, giving a as 6. Leaving it as 3 misses the simplifying step."),
    mc("wrong_root", None, "Simplify root 8 to 2 root 2, then multiply by the 3 outside to get 6 root 2."),
  ],
  "guided_steps": [
    say("Simplify \\(\\sqrt{8}\\) first, then multiply by the 3 in front."),
    box("8 = 4 × 2 and √4 = ", 2, "The square root of 4."),
    box("So √8 = 2√2. Multiply the outside numbers: 3 × 2 = ", 6, "3 times the 2 from 2 root 2.", phase="substitute"),
    box("So 3√8 = 6√2. Check: 6² × 2 = 72, and (3√8)² = 9 × 8 = ", 72, "Square 3 then times 8.", done="Both give 72, so a = 6."),
  ],
 },
 {  # S6  (1/4)^(-1/2) = 2
  "display": "Evaluate \\(\\left(\\frac{1}{4}\\right)^{-\\frac{1}{2}}\\)",
  "solutions": [2], "calculator": False, "input_type": "single_value",
  "hint": "The negative power flips the fraction to 4, then take the square root.",
  "misconceptions": [
    mc("no_flip", 0.5, "The negative power flips the fraction first. Without flipping you take the square root of a quarter, which is a half. Flipping gives 4, then root 4 is 2."),
    mc("wrong_order", None, "Flip the fraction because of the negative power: a quarter becomes 4, then the half power gives root 4, which is 2."),
  ],
  "guided_steps": [
    say("A negative power flips the fraction: \\(\\left(\\frac{1}{4}\\right)^{-1/2} = 4^{1/2}\\)."),
    box("Flip 1/4 to get ", 4, "Turn the fraction upside down."),
    box("Now the ½ power means a square root: √4 = ", 2, "What number squared gives 4?", phase="substitute"),
    box("Check: 2 × 2 = ", 4, "Square the 2.", done="√4 = 2, so the answer is 2."),
  ],
 },
]

# ---------------------------------------------------------------- GOLD
gold = [
 {  # G0  8^(-2/3) denominator = 4
  "display": "Evaluate \\(8^{-\\frac{2}{3}}\\). Express as a fraction. Enter the denominator.",
  "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "Flip the negative power, take the cube root, then square.",
  "misconceptions": [
    mc("wrong_power", 2, "After the cube root, root 8 is 2, you must square it: 2 squared is 4. Stopping at 2 gives the wrong denominator."),
    mc("no_flip", None, "The negative power flips it to 1 over 8 to the two thirds. The denominator is the cube root of 8 squared, which is 2 squared, so 4."),
  ],
  "guided_steps": [
    say("A negative power flips it: \\(8^{-2/3} = \\frac{1}{8^{2/3}}\\). Work the bottom."),
    box("Cube root first: ∛8 = ", 2, "Which number cubed gives 8?"),
    box("Then square it: 2² = ", 4, "2 × 2.", phase="substitute"),
    box("So the fraction is 1/4. Rebuild the root: 2 × 2 × 2 = ", 8, "Cube the 2.", done="∛8 = 2 confirmed, so the denominator is 4."),
  ],
 },
 {  # G1  10/sqrt5 = 2 root5
  "display": "Simplify \\(\\frac{10}{\\sqrt{5}}\\). Give the number in front of \\(\\sqrt{5}\\).",
  "solutions": [2], "calculator": False, "input_type": "single_value",
  "hint": "Multiply top and bottom by root 5, then simplify.",
  "misconceptions": [
    mc("no_rationalise", 10, "Rationalise by multiplying top and bottom by root 5: 10 root 5 over 5 is 2 root 5. The number in front is 2, not 10."),
    mc("wrong_simplify", None, "10 root 5 over 5 simplifies to 2 root 5 because 10 divided by 5 is 2."),
  ],
  "guided_steps": [
    say("Clear the surd on the bottom by multiplying top and bottom by \\(\\sqrt{5}\\)."),
    box("Bottom becomes √5 × √5 = ", 5, "A root times itself is just the number inside."),
    box("Top becomes 10√5, so divide the whole numbers: 10 ÷ 5 = ", 2, "10 divided by 5.", phase="substitute"),
    box("So 10/√5 = 2√5. Check: (2√5)² = 4 × 5 = 20, and (10/√5)² = 100 ÷ 5 = ", 20, "Square 10 then divide by 5.", done="Both give 20, so the number in front is 2."),
  ],
 },
 {  # G2  rectangle lower bound area = 26.6175
  "display": "A rectangle is \\(8.5\\) cm by \\(3.2\\) cm (both to 1 d.p.). Find the lower bound of the area.",
  "solutions": [26.6175], "calculator": True, "input_type": "single_value",
  "hint": "The smallest area uses the lower bound of each side.",
  "misconceptions": [
    mc("use_given", 27.2, "Using the given sizes 8.5 times 3.2 gives 27.2, but the smallest area uses the lower bounds: 8.45 times 3.15 is 26.6175."),
    mc("wrong_bounds", None, "Lower bound of 8.5 is 8.45 and of 3.2 is 3.15, so the smallest area is 8.45 times 3.15, which is 26.6175."),
  ],
  "guided_steps": [
    say("Both sides are to 1 d.p., so each has a half unit of 0.05. The smallest area uses the smallest sides."),
    box("Lower bound of 8.5 = 8.5 − 0.05 = ", 8.45, "Take 0.05 off."),
    box("Lower bound of 3.2 = 3.2 − 0.05 = ", 3.15, "Take 0.05 off."),
    box("Smallest area = 8.45 × 3.15 = ", 26.6175, "Multiply the two lower bounds.", phase="substitute"),
    box("For comparison, the given-value area 8.5 × 3.2 = ", 27.2, "Multiply the rounded sides.", done="26.6175 is below 27.2, exactly as a lower bound should be."),
  ],
 },
 {  # G3  sqrt75 + sqrt27 = 8 root3, enter k=8  (reworded: reveal removed)
  "display": "Simplify \\(\\sqrt{75} + \\sqrt{27}\\), giving your answer in the form \\(k\\sqrt{3}\\). Enter \\(k\\).",
  "solutions": [8], "calculator": False, "input_type": "single_value",
  "hint": "Simplify each surd to a multiple of root 3, then add.",
  "misconceptions": [
    mc("not_simplified", 5, "You simplified root 75 to 5 root 3 but stopped. Root 27 is 3 root 3, so the total is 5 plus 3, which is 8, giving 8 root 3."),
    mc("wrong_factor", None, "Use square factors: 75 is 25 times 3 and 27 is 9 times 3, so 5 root 3 plus 3 root 3 is 8 root 3."),
  ],
  "guided_steps": [
    say("Simplify each surd to a multiple of \\(\\sqrt{3}\\), then add the coefficients."),
    box("√75 = √(25 × 3) = 5√3, so its coefficient is ", 5, "The square root of 25."),
    box("√27 = √(9 × 3) = 3√3, so its coefficient is ", 3, "The square root of 9."),
    box("Same √3, so add the coefficients: 5 + 3 = ", 8, "Add the two numbers in front.", phase="substitute"),
    box("So the answer is 8√3. Check by squaring: (8√3)² = 64 × 3 = ", 192, "Square 8 then times 3.", done="(√75 + √27)² = 75 + 27 + 2√2025 = 192 too, so k = 8."),
  ],
 },
 {  # G4  speed upper bound = 8.2
  "display": "A speed is \\(\\frac{\\text{distance}}{\\text{time}}\\). Distance = \\(100\\) m (nearest m), time = \\(12.3\\) s (nearest 0.1 s). Find the upper bound of speed to 1 d.p.",
  "solutions": [8.2], "calculator": True, "input_type": "single_value",
  "hint": "The biggest speed uses the largest distance divided by the smallest time.",
  "misconceptions": [
    mc("same_bounds", 8.1, "For the biggest speed divide by the smallest time, 12.25, not the largest. Using 12.35 gives 8.1; the answer is 100.5 divided by 12.25, which is 8.2."),
    mc("wrong_combination", None, "Biggest speed uses the largest distance over the smallest time: 100.5 divided by 12.25 is 8.2."),
  ],
  "guided_steps": [
    say("Speed = distance ÷ time. For the biggest speed, use the biggest distance and the smallest time."),
    box("Biggest distance: 100 to the nearest metre, upper bound = 100 + 0.5 = ", 100.5, "Half of 1 is 0.5."),
    box("Smallest time: 12.3 to 1 d.p., lower bound = 12.3 − 0.05 = ", 12.25, "Half of 0.1 is 0.05."),
    box("Biggest speed = 100.5 ÷ 12.25 = 8.204..., to 1 d.p. = ", 8.2, "Divide, then round to one decimal place.", phase="substitute"),
    box("The smallest speed uses 99.5 ÷ 12.35 = 8.056, to 1 d.p. = ", 8.1, "Smallest distance over biggest time.", done="Speed lies between 8.1 and 8.2, so the upper bound is 8.2."),
  ],
 },
]

# ---------------------------------------------------------------- TIER GUIDES
tier_guides = {
 "bronze": {
  "title": "Bronze: one move with roots, powers and bounds",
  "steps": [
    "<strong>Fractional power means a root.</strong> The bottom number is the root: \\(a^{1/2}=\\sqrt{a}\\) and \\(a^{1/3}=\\sqrt[3]{a}\\). So \\(16^{1/2}=4\\).",
    "<strong>Negative power means flip.</strong> \\(a^{-n}=\\frac{1}{a^{n}}\\), so \\(2^{-3}=\\frac{1}{8}\\). It never makes the answer negative.",
    "<strong>Simplify a surd</strong> by pulling out the biggest square factor: \\(\\sqrt{50}=5\\sqrt{2}\\). <strong>Bounds:</strong> for 1 d.p. the half unit is 0.05.",
  ],
  "example": {
    "question": "Evaluate \\(49^{\\frac{1}{2}}\\)",
    "steps": [
      {"label": "Read the power", "content": "A power of a half means square root: \\(49^{1/2}=\\sqrt{49}\\)."},
      {"label": "Find the root", "content": "\\(7\\times7=49\\), so \\(\\sqrt{49}=7\\)."},
      {"label": "Check", "content": "\\(7^2=49\\), which is back to the start."},
      {"label": "Answer", "content": "<strong>7</strong>", "isAnswer": True, "is_answer": True},
    ],
  },
 },
 "silver": {
  "title": "Silver: two linked steps",
  "steps": [
    "<strong>Root then power.</strong> For \\(a^{m/n}\\), take the \\(n\\)th root first, then raise to \\(m\\): \\(27^{2/3}=(\\sqrt[3]{27})^{2}=3^{2}=9\\). Doing the root first keeps the numbers small.",
    "<strong>Simplify, then use.</strong> Tidy a surd before multiplying: \\(3\\sqrt{8}=3\\times2\\sqrt{2}=6\\sqrt{2}\\). To rationalise, multiply top and bottom by the surd.",
    "<strong>Bounds:</strong> for 1 d.p. the half unit is 0.05, so upper = value + 0.05 and lower = value − 0.05.",
  ],
  "example": {
    "question": "Evaluate \\(8^{\\frac{2}{3}}\\)",
    "steps": [
      {"label": "Root first", "content": "\\(\\sqrt[3]{8}=2\\)."},
      {"label": "Then the power", "content": "\\(2^2=4\\)."},
      {"label": "Check", "content": "\\(2^3=8\\), so the cube root of 8 really is 2."},
      {"label": "Answer", "content": "<strong>4</strong>", "isAnswer": True, "is_answer": True},
    ],
  },
 },
 "gold": {
  "title": "Gold: combine the skills",
  "steps": [
    "<strong>Negative fractional power:</strong> flip first, then root, then power. \\(8^{-2/3}=\\frac{1}{(\\sqrt[3]{8})^{2}}=\\frac{1}{4}\\).",
    "<strong>Add surds</strong> by simplifying each to the same root: \\(\\sqrt{75}+\\sqrt{27}=5\\sqrt3+3\\sqrt3=8\\sqrt3\\).",
    "<strong>Bounds in calculations:</strong> for the biggest result multiply the largest values, or divide the largest by the smallest; swap for the smallest result.",
  ],
  "example": {
    "question": "Find the upper bound of the area of a \\(6.4\\) cm by \\(2.5\\) cm rectangle (1 d.p.).",
    "steps": [
      {"label": "Biggest sides", "content": "Upper bounds: \\(6.45\\) cm and \\(2.55\\) cm."},
      {"label": "Multiply", "content": "\\(6.45\\times2.55=16.4475\\) cm²."},
      {"label": "Check", "content": "The rounded area \\(6.4\\times2.5=16\\), and \\(16.45\\) sits just above it."},
      {"label": "Answer", "content": "<strong>\\(16.4475\\) cm²</strong>", "isAnswer": True, "is_answer": True},
    ],
  },
 },
}

# ---------------------------------------------------------------- GUIDED (opener + teach)
guided = {
 "opener": {
  "display": "A square kitchen floor is covered in tiles.<br>Altogether it takes <strong>36 tiles</strong> to fill it, arranged in a perfect square.",
  "steps": [
    say("No algebra needed, just picture the square of tiles."),
    box("How many tiles fit along one edge? ", 6, "Six rows of six tiles make 36. What number times itself gives 36?"),
    say("Going from the area back to one side is a <strong>square root</strong>. You just found \\(\\sqrt{36}=6\\) in your head. In index form a square root is a power of one half: \\(\\sqrt{36}=36^{1/2}\\). The bottom of the fraction tells you which root to take."),
    box("Now a cube of 8 small blocks. How many blocks lie along one edge? ", 2, "2 × 2 × 2 = 8. What number cubed gives 8?"),
    say("That is a <strong>cube root</strong>: \\(\\sqrt[3]{8}=2\\), written \\(8^{1/3}\\). Roots and powers are the first strand of this lesson. Later you will tidy surds like \\(\\sqrt{50}\\) and handle rounded measurements, but it all starts with asking which number, multiplied by itself, gives this."),
  ],
 },
 "teach": {
  "bronze": {
    "display": "Evaluate \\(64^{\\frac{1}{2}}\\)",
    "steps": [
      say("A power of a half means a square root, so read \\(64^{1/2}\\) as \\(\\sqrt{64}\\)."),
      box("Which number squared makes 64? Try 7: 7 × 7 = ", 49, "Multiply 7 by itself."),
      box("A bit small, so try 8: 8 × 8 = ", 64, "Multiply 8 by itself."),
      box("It lands on 64, so √64 = ", 8, "The number you just squared."),
      box("Check by squaring: 8 × 8 = ", 64, "Multiply 8 by itself once more.", done="Gone. A half power is just a square root."),
    ],
  },
  "silver": {
    "display": "Evaluate \\(8^{\\frac{2}{3}}\\)",
    "steps": [
      say("Two moves. The bottom 3 is a cube root, the top 2 is a power. Root first."),
      box("Cube root first: ∛8 = ", 2, "Which number cubed gives 8?"),
      box("Now the power 2: 2² = ", 4, "2 × 2."),
      box("Check the root: 2 × 2 × 2 = ", 8, "Cube the 2 to rebuild 8."),
      box("So the answer is 8^(2/3) = ", 4, "The value after squaring.", done="Gone. Root first, then power: that is the new silver move."),
    ],
  },
  "gold": {
    "display": "Find the upper bound of the area of a rectangle \\(6.4\\) cm by \\(2.5\\) cm, both to 1 d.p.",
    "steps": [
      say("Both are to 1 d.p., so each has a half unit of 0.05. The biggest area uses the biggest side lengths."),
      box("Upper bound of 6.4 = 6.4 + 0.05 = ", 6.45, "Add the half unit."),
      box("Upper bound of 2.5 = 2.5 + 0.05 = ", 2.55, "Add the half unit."),
      box("Biggest area = 6.45 × 2.55 = ", 16.4475, "Multiply the two upper bounds."),
      box("The given-value area 6.4 × 2.5 = ", 16, "Multiply the rounded sides.", done="Gone. 16.45 sits just above 16, exactly as an upper bound should. Choosing which bound gives the max is the gold move."),
    ],
  },
 },
}

# ---------------------------------------------------------------- METHOD CARD (slim)
method_card = {
 "title": "Indices, Surds and Bounds",
 "steps": [
   "Fractional index: the bottom is the root, the top is the power. Root first.",
   "Negative index: flip to a fraction, then work the positive power.",
   "Surd: pull out the biggest square factor; rationalise by multiplying by the surd.",
   "Bound: a rounded value hides a range of half a unit each side.",
 ],
 "content": "<p><strong>Fractional indices:</strong> the bottom is the root, the top is the power: \\(a^{m/n}=(\\sqrt[n]{a})^{m}\\). <strong>Negative indices</strong> flip to a fraction: \\(a^{-n}=\\frac{1}{a^{n}}\\).</p><p><strong>Surds</strong> stay exact. Simplify with the biggest square factor: \\(\\sqrt{50}=5\\sqrt2\\). Rationalise \\(\\frac{a}{\\sqrt b}\\) by multiplying top and bottom by \\(\\sqrt b\\).</p><p><strong>Bounds:</strong> a rounded value hides a range of half a unit each side. For 1 d.p. that is 0.05. In a calculation, pick the bounds that make the result biggest or smallest.</p>",
 "example": live["method_card"]["example"],
}

# ---------------------------------------------------------------- ASSEMBLE
out = dict(live)  # preserves related_videos, topic_links; worked_examples labels de-em-dashed
# Style rule (validator-enforced): no em dashes in student-facing strings.
# The stored worked_examples labels use em dashes; replace with colons only.
for we in out.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and isinstance(st["label"], str):
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")
out["method_card"] = method_card
out["problem_bank"] = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": "One operation: take a single root, a negative power, one surd to simplify, or one rounded value's bound.",
  "silver_description": "Two linked steps: a root then a power, simplify a surd then use it, or a bound with a half-unit calculation.",
  "gold_description": "Combine skills: negative fractional powers, adding simplified surds, or bounds inside a multiply or divide.",
}
out["tier_guides"] = tier_guides
out["guided"] = guided

json.dump(out, io.open("lesson_number-L07.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written lesson_number-L07.json")
