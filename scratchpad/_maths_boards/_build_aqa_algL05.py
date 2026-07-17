# -*- coding: utf-8 -*-
"""Build guided-learning practice_data for maths-aqa algebra-L05 (Solving Linear Equations)."""
import json, io

M = "−"   # minus sign
AR = "  →  "  # arrow with spaces

live = json.load(io.open("_live_aqa_algL05.json", encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase: d["phase"] = phase
    if done: d["done"] = done
    return d

def say(text):
    return {"say": text}

# ---------------- PROBLEM BANK ----------------
bronze = [
 # b0: 3x = 18, x=6
 {"display": "Solve \\(3x = 18\\)", "solutions": [6], "calculator": False, "input_type": "single_value",
  "hint": "The 3 is multiplying x, so divide both sides by 3.",
  "misconceptions": [
    {"pattern": "subtract_instead_of_divide", "expect": 15,
     "message": "The 3 is multiplying \\(x\\), not added to it. Undo a multiply with a divide: \\(18 \\div 3 = 6\\), not \\(18 - 3\\).",
     "note": "18-3=15"}],
  "guided_steps": [
    box("The 3 multiplies x. To undo it, divide both sides by 3. 18 ÷ 3 = ", 6, "Divide 18 by 3."),
    box("So x = ", 6, "It equals the value you just found.", phase="substitute"),
    box("Check by multiplying back: 3 × 6 = ", 18, "Multiply your answer by 3.", phase="substitute",
        done="It gives 18, the original right side, so x = 6.")]},
 # b1: x + 7 = 15, x=8
 {"display": "Solve \\(x + 7 = 15\\)", "solutions": [8], "calculator": False, "input_type": "single_value",
  "hint": "7 is added to x, so subtract 7 from both sides.",
  "misconceptions": [
    {"pattern": "added_instead_of_subtracted", "expect": 22,
     "message": "To undo the \\(+7\\) you subtract 7, not add it: \\(15 - 7 = 8\\). Adding gives 22, which is too big.",
     "note": "15+7=22"}],
  "guided_steps": [
    box("7 is added to x. Undo it by subtracting 7 from both sides. 15 " + M + " 7 = ", 8, "Take 7 off 15."),
    box("So x = ", 8, "The value you just found.", phase="substitute"),
    box("Check by adding back: 8 + 7 = ", 15, "Add 7 to your answer.", phase="substitute",
        done="Gives 15, so x = 8.")]},
 # b2 FIXED: 2x - 5 = 13, x=9  (was 2x-5=11, x=8 dup with b1)
 {"display": "Solve \\(2x - 5 = 13\\)", "solutions": [9], "calculator": False, "input_type": "single_value",
  "hint": "Add 5 to both sides, then divide by 2.",
  "misconceptions": [
    {"pattern": "moved_constant_wrong_sign", "expect": 4,
     "message": "The 5 is subtracted, so undo it by adding: \\(13 + 5 = 18\\), giving \\(x = 9\\). Subtracting 5 instead leads to \\(x = 4\\).",
     "note": "(13-5)/2=4"},
    {"pattern": "coefficient_ignored", "expect": 18,
     "message": "\\(2x = 18\\) means 2 times \\(x\\), so divide by 2: \\(x = 9\\). Leaving \\(x = 18\\) skips the last step.",
     "note": "stops at 2x=18"}],
  "guided_steps": [
    box("First undo the minus 5. Add 5 to both sides. 13 + 5 = ", 18, "Add 5 to the right side. Now 2x = 18."),
    box("18 ÷ 2 = ", 9, "Half of 18.", say="Now 2x = 18. The 2 multiplies x, so divide both sides by 2.", phase="substitute"),
    box("So x = ", 9, "The value you just found.", phase="substitute"),
    box("Check: 2 × 9 " + M + " 5 = ", 13, "Work out 2×9 then subtract 5.", phase="substitute",
        done="Gives 13, so x = 9.")]},
 # b3: 4x + 3 = 19, x=4
 {"display": "Solve \\(4x + 3 = 19\\)", "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "Subtract 3 from both sides, then divide by 4.",
  "misconceptions": [
    {"pattern": "moved_constant_wrong_sign", "expect": 5.5,
     "message": "The 3 is added, so undo it by subtracting: \\(19 - 3 = 16\\), giving \\(x = 4\\). Adding 3 gives a messy \\(5.5\\), a sign the move went the wrong way.",
     "note": "(19+3)/4=5.5"},
    {"pattern": "coefficient_ignored", "expect": 16,
     "message": "\\(4x = 16\\) still has 4 multiplying \\(x\\): divide by 4 to get \\(x = 4\\). Stopping at \\(x = 16\\) misses the final step.",
     "note": "stops at 4x=16"}],
  "guided_steps": [
    box("Undo the +3 first. Subtract 3 from both sides. 19 " + M + " 3 = ", 16, "Take 3 off 19. Now 4x = 16."),
    box("16 ÷ 4 = ", 4, "How many 4s in 16?", say="Now 4x = 16. Divide both sides by 4.", phase="substitute"),
    box("So x = ", 4, "The value you just found.", phase="substitute"),
    box("Check: 4 × 4 + 3 = ", 19, "Work out 4×4 then add 3.", phase="substitute",
        done="Gives 19, so x = 4.")]},
 # b4: x/3 = 7, x=21
 {"display": "Solve \\(\\frac{x}{3} = 7\\)", "solutions": [21], "calculator": False, "input_type": "single_value",
  "hint": "x is divided by 3, so multiply both sides by 3.",
  "misconceptions": [
    {"pattern": "wrong_inverse", "expect": 4,
     "message": "\\(x\\) is divided by 3, so undo it by multiplying: \\(7 \\times 3 = 21\\). Subtracting 3 (giving 4) does not undo a divide.",
     "note": "7-3=4"}],
  "guided_steps": [
    box("x is divided by 3. Undo it by multiplying both sides by 3. 7 × 3 = ", 21, "Multiply 7 by 3."),
    box("So x = ", 21, "The value you just found.", phase="substitute"),
    box("Check: 21 ÷ 3 = ", 7, "Divide your answer by 3.", phase="substitute",
        done="Gives 7, so x = 21.")]},
 # b5: 20 - 3x = 5, x=5
 {"display": "Solve \\(20 - 3x = 5\\)", "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Add 3x to both sides so the x term is positive, then solve.",
  "misconceptions": [
    {"pattern": "sign_slip_negative_coeff", "expect": -5,
     "message": "From \\(-3x = -15\\), dividing by \\(-3\\) gives \\(x = 5\\) (negative divided by negative is positive). Getting \\(-5\\) keeps one minus sign too many.",
     "note": "-15/-3=5, slip gives -5"}],
  "guided_steps": [
    box("The x term is negative, so add 3x to both sides. That gives 20 = 5 + 3x. Now subtract 5 from both sides: 20 " + M + " 5 = ", 15, "Take 5 off 20. Now 3x = 15.",
        say="The x term is negative, so add 3x to both sides to make it positive."),
    box("15 ÷ 3 = ", 5, "How many 3s in 15?", say="Now 3x = 15. Divide both sides by 3.", phase="substitute"),
    box("So x = ", 5, "The value you just found.", phase="substitute"),
    box("Check: 20 " + M + " 3 × 5 = ", 5, "Work out 3×5, then take it from 20.", phase="substitute",
        done="Gives 5, so x = 5.")]},
 # b6 FIXED: 5x + 2 = 3x + 16, x=7  (was =3x+10, x=4 dup with b3)
 {"display": "Solve \\(5x + 2 = 3x + 16\\)", "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "Subtract 3x from both sides, then solve the two step equation left.",
  "misconceptions": [
    {"pattern": "constant_wrong_side_sign", "expect": 9,
     "message": "Moving the \\(+2\\) across makes it \\(-2\\): \\(2x = 16 - 2 = 14\\), so \\(x = 7\\). Adding it (giving \\(2x = 18\\)) flips the sign the wrong way.",
     "note": "2x=18 -> 9"}],
  "guided_steps": [
    box("5x " + M + " 3x = ", 2, "Subtract the numbers in front: 5 " + M + " 3. Now 2x + 2 = 16.", post="x",
        say="Both sides have x. Take the smaller x term (3x) off both sides."),
    box("16 " + M + " 2 = ", 14, "Take 2 off 16. Now 2x = 14.", say="Now 2x + 2 = 16. Subtract 2 from both sides.", phase="substitute"),
    box("14 ÷ 2 = ", 7, "Half of 14.", say="Now 2x = 14. Divide both sides by 2.", phase="substitute"),
    box("So x = ", 7, "The value you just found.", phase="substitute"),
    box("Check: 5 × 7 + 2 = ", 37, "Work out 5×7 then add 2.", phase="substitute",
        done="And 3 × 7 + 16 = 37 too. Both sides match, so x = 7.")]},
 # b7 FIXED: 7x - 1 = 4x + 8, x=3  (was =4x+14, x=5 dup with b5)
 {"display": "Solve \\(7x - 1 = 4x + 8\\)", "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "Subtract 4x from both sides, then solve.",
  "misconceptions": [],
  "guided_steps": [
    box("7x " + M + " 4x = ", 3, "Subtract the numbers in front: 7 " + M + " 4. Now 3x " + M + " 1 = 8.", post="x",
        say="Both sides have x. Take the smaller x term (4x) off both sides."),
    box("8 + 1 = ", 9, "Add 1 to 8. Now 3x = 9.", say="Now 3x " + M + " 1 = 8. Add 1 to both sides.", phase="substitute"),
    box("9 ÷ 3 = ", 3, "How many 3s in 9?", say="Now 3x = 9. Divide both sides by 3.", phase="substitute"),
    box("So x = ", 3, "The value you just found.", phase="substitute"),
    box("Check: 7 × 3 " + M + " 1 = ", 20, "Work out 7×3 then subtract 1.", phase="substitute",
        done="And 4 × 3 + 8 = 20 too. Both sides match, so x = 3.")]},
]

silver = [
 # s0: 3(x+4)=27, x=5
 {"display": "Solve \\(3(x + 4) = 27\\)", "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Expand the bracket first, then subtract 12 and divide by 3.",
  "misconceptions": [
    {"pattern": "moved_constant_wrong_sign", "expect": 13,
     "message": "The \\(+12\\) is undone by subtracting: \\(27 - 12 = 15\\), so \\(x = 5\\). Adding 12 instead gives \\(x = 13\\).",
     "note": "(27+12)/3=13"}],
  "guided_steps": [
    box("Expand the bracket. 3 × 4 = ", 12, "Multiply the 3 by the 4 inside. Now 3x + 12 = 27.",
        say="Expand the bracket: multiply everything inside by 3."),
    box("27 " + M + " 12 = ", 15, "Take 12 off 27. Now 3x = 15.", say="Now 3x + 12 = 27. Subtract 12 from both sides.", phase="substitute"),
    box("15 ÷ 3 = ", 5, "How many 3s in 15?", say="Now 3x = 15. Divide both sides by 3.", phase="substitute"),
    box("So x = ", 5, "The value you just found.", phase="substitute"),
    box("Check: 3 × (5 + 4) = ", 27, "Add inside the bracket first: 5+4, then times 3.", phase="substitute",
        done="Gives 27, so x = 5.")]},
 # s1: 2(3x-1)=5x+7, x=9
 {"display": "Solve \\(2(3x - 1) = 5x + 7\\)", "solutions": [9], "calculator": False, "input_type": "single_value",
  "hint": "Expand the bracket, then collect x terms on one side.",
  "misconceptions": [
    {"pattern": "incomplete_expansion", "expect": 8,
     "message": "Both terms inside get multiplied: \\(2 \\times (-1) = -2\\), not \\(-1\\). Using \\(6x - 2 = 5x + 7\\) gives \\(x = 9\\); leaving it as \\(-1\\) gives \\(x = 8\\).",
     "note": "6x-1=5x+7 -> 8"}],
  "guided_steps": [
    box("Expand the bracket on the left: multiply 3x and " + M + "1 by 2. 2 × 3x = ", 6, "2 times 3. Now the left is 6x " + M + " 2.", post="x",
        say="Expand the bracket on the left: multiply 3x and " + M + "1 by 2."),
    box("6x " + M + " 5x = ", 1, "6 " + M + " 5 in front of x. Now x " + M + " 2 = 7.", post="x",
        say="So the left is 6x " + M + " 2, and 2 × (" + M + "1) = " + M + "2. Now 6x " + M + " 2 = 5x + 7. Both sides have x; take 5x off both sides.", phase="substitute"),
    box("7 + 2 = ", 9, "Add 2 to 7.", say="Now x " + M + " 2 = 7. Add 2 to both sides.", phase="substitute"),
    box("So x = ", 9, "The value you just found.", phase="substitute"),
    box("Check: 2 × (3 × 9 " + M + " 1) = ", 52, "Inside first: 3×9" + M + "1 = 26, then ×2.", phase="substitute",
        done="And 5 × 9 + 7 = 52 too. Both sides match, so x = 9.")]},
 # s2: 4(x+2)=3(x+5), x=7
 {"display": "Solve \\(4(x + 2) = 3(x + 5)\\)", "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "Expand both brackets, then collect x terms.",
  "misconceptions": [
    {"pattern": "incomplete_expansion", "expect": -3,
     "message": "The right bracket gives \\(3 \\times 5 = 15\\), not 5. Using \\(4x + 8 = 3x + 15\\) gives \\(x = 7\\); leaving 5 gives \\(x = -3\\).",
     "note": "4x+8=3x+5 -> -3"}],
  "guided_steps": [
    box("Expand both brackets. Left: 4 × x and 4 × 2. 4 × 2 = ", 8, "Left becomes 4x + 8.",
        say="Expand both brackets. Left: 4 × x and 4 × 2."),
    box("4x " + M + " 3x = ", 1, "4 " + M + " 3 in front of x. Now x + 8 = 15.", post="x",
        say="Right: 3 × (x + 5) = 3x + 15, since 3 × 5 = 15. Now 4x + 8 = 3x + 15. Take 3x off both sides.", phase="substitute"),
    box("15 " + M + " 8 = ", 7, "Take 8 off 15.", say="Now x + 8 = 15. Subtract 8 from both sides.", phase="substitute"),
    box("So x = ", 7, "The value you just found.", phase="substitute"),
    box("Check: 4 × (7 + 2) = ", 36, "Inside first: 7+2 = 9, then ×4.", phase="substitute",
        done="And 3 × (7 + 5) = 36 too. Both sides match, so x = 7.")]},
 # s3: (x+5)/2 = 8, x=11
 {"display": "Solve \\(\\frac{x + 5}{2} = 8\\)", "solutions": [11], "calculator": False, "input_type": "single_value",
  "hint": "Multiply both sides by 2 to clear the fraction, then subtract 5.",
  "misconceptions": [
    {"pattern": "did_not_clear_fraction", "expect": 3,
     "message": "Multiply the whole right side by 2 as well: \\(8 \\times 2 = 16\\), so \\(x + 5 = 16\\) and \\(x = 11\\). Forgetting the \\(\\times 2\\) gives \\(x = 3\\).",
     "note": "x+5=8 -> 3"}],
  "guided_steps": [
    box("The whole left side is divided by 2. Multiply both sides by 2 to clear it. 8 × 2 = ", 16, "Now x + 5 = 16.",
        say="The whole left side is divided by 2. Multiply both sides by 2 to clear it."),
    box("16 " + M + " 5 = ", 11, "Take 5 off 16.", say="Now x + 5 = 16. Subtract 5 from both sides.", phase="substitute"),
    box("So x = ", 11, "The value you just found.", phase="substitute"),
    box("Check: (11 + 5) ÷ 2 = ", 8, "Add inside first: 11+5 = 16, then ÷2.", phase="substitute",
        done="Gives 8, so x = 11.")]},
 # s4 FIXED: (2x-3)/5 = 5, x=14  (was =3, x=9 dup with s1)
 {"display": "Solve \\(\\frac{2x - 3}{5} = 5\\)", "solutions": [14], "calculator": False, "input_type": "single_value",
  "hint": "Multiply both sides by 5, then add 3 and divide by 2.",
  "misconceptions": [
    {"pattern": "did_not_clear_fraction", "expect": 4,
     "message": "Multiply the whole right side by 5 too: \\(5 \\times 5 = 25\\), giving \\(x = 14\\). Forgetting it leaves \\(2x - 3 = 5\\) and \\(x = 4\\).",
     "note": "2x-3=5 -> 4"}],
  "guided_steps": [
    box("The whole left side is divided by 5. Multiply both sides by 5 to clear it. 5 × 5 = ", 25, "Now 2x " + M + " 3 = 25.",
        say="The whole left side is divided by 5. Multiply both sides by 5 to clear it."),
    box("25 + 3 = ", 28, "Add 3 to 25. Now 2x = 28.", say="Now 2x " + M + " 3 = 25. Add 3 to both sides.", phase="substitute"),
    box("28 ÷ 2 = ", 14, "Half of 28.", say="Now 2x = 28. Divide both sides by 2.", phase="substitute"),
    box("So x = ", 14, "The value you just found.", phase="substitute"),
    box("Check: (2 × 14 " + M + " 3) ÷ 5 = ", 5, "Top first: 2×14" + M + "3 = 25, then ÷5.", phase="substitute",
        done="Gives 5, so x = 14.")]},
 # s5: 5(2x+1) - 3(x-2) = 25, x=2
 {"display": "Solve \\(5(2x + 1) - 3(x - 2) = 25\\)", "solutions": [2], "calculator": False, "input_type": "single_value",
  "hint": "Expand carefully; minus times minus 2 gives plus 6. Then simplify and solve.",
  "misconceptions": [],
  "guided_steps": [
    box("Expand both brackets. First 5(2x + 1) = 10x + 5. Now the tricky one: " + M + "3 × (" + M + "2) = ", 6, "Minus times minus is plus. So " + M + "3(x" + M + "2) = " + M + "3x + 6.",
        say="Expand both brackets. First 5(2x + 1) = 10x + 5."),
    box("25 " + M + " 11 = ", 14, "Take 11 off 25. Now 7x = 14.",
        say="Putting it together: 10x + 5 " + M + " 3x + 6 = 25. Combine the x terms: 10x " + M + " 3x = 7x, and 5 + 6 = 11. So 7x + 11 = 25. Subtract 11 from both sides.", phase="substitute"),
    box("14 ÷ 7 = ", 2, "How many 7s in 14?", say="Now 7x = 14. Divide both sides by 7.", phase="substitute"),
    box("So x = ", 2, "The value you just found.", phase="substitute"),
    box("Check: 5 × (2 × 2 + 1) " + M + " 3 × (2 " + M + " 2) = ", 25, "Brackets first: (2×2+1)=5 and (2" + M + "2)=0.", phase="substitute",
        done="5×5 " + M + " 3×0 = 25, so x = 2.")]},
 # s6: 3x/4 = 9, x=12
 {"display": "Solve \\(\\frac{3x}{4} = 9\\)", "solutions": [12], "calculator": False, "input_type": "single_value",
  "hint": "Multiply both sides by 4, then divide by 3.",
  "misconceptions": [
    {"pattern": "coefficient_ignored", "expect": 36,
     "message": "After multiplying by 4 you have \\(3x = 36\\), and 3 still multiplies \\(x\\): divide by 3 to get \\(x = 12\\). Stopping at \\(x = 36\\) skips that step.",
     "note": "stops at 3x=36"}],
  "guided_steps": [
    box("The 3x is divided by 4. Multiply both sides by 4 to clear the fraction. 9 × 4 = ", 36, "Now 3x = 36.",
        say="The 3x is divided by 4. Multiply both sides by 4 to clear the fraction."),
    box("36 ÷ 3 = ", 12, "How many 3s in 36?", say="Now 3x = 36. Divide both sides by 3.", phase="substitute"),
    box("So x = ", 12, "The value you just found.", phase="substitute"),
    box("Check: 3 × 12 ÷ 4 = ", 9, "3×12 = 36, then ÷4.", phase="substitute",
        done="36 ÷ 4 = 9, so x = 12.")]},
]

gold = [
 # g0 FIXED: (x+1)/3 + (x-1)/4 = 3, x=5  (was (x-2)/4, stored 5 but actually 38/7 WRONG)
 {"display": "Solve \\(\\frac{x+1}{3} + \\frac{x-1}{4} = 3\\)", "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Multiply every term by 12 (the common denominator), then expand and solve.",
  "misconceptions": [],
  "guided_steps": [
    box("Clear both fractions at once. The bottoms are 3 and 4, and the number both divide into is 12. Multiply every term by 12. For the first fraction: 12 ÷ 3 = ", 4, "So it becomes 4 × (x + 1).",
        say="Clear both fractions at once. The bottoms are 3 and 4, and the number both divide into is 12. Multiply every term by 12."),
    box("For the second fraction: 12 ÷ 4 = ", 3, "So it becomes 3 × (x " + M + " 1). The right side: 3 × 12 = 36."),
    box("36 " + M + " 1 = ", 35, "Take 1 off 36. Now 7x = 35.",
        say="Now 4(x + 1) + 3(x " + M + " 1) = 36. Expand: 4x + 4 + 3x " + M + " 3 = 36. Combine: 7x + 1 = 36. Subtract 1 from both sides.", phase="substitute"),
    box("35 ÷ 7 = ", 5, "How many 7s in 35?", say="Now 7x = 35. Divide both sides by 7.", phase="substitute"),
    box("So x = ", 5, "The value you just found.", phase="substitute"),
    box("Check: (5 + 1) ÷ 3 + (5 " + M + " 1) ÷ 4 = ", 3, "6÷3 = 2 and 4÷4 = 1, add them.", phase="substitute",
        done="6/3 + 4/4 = 2 + 1 = 3, so x = 5.")]},
 # g1: (5x+2)/3 = (3x+8)/2, x=20
 {"display": "Solve \\(\\frac{5x + 2}{3} = \\frac{3x + 8}{2}\\)", "solutions": [20], "calculator": False, "input_type": "single_value",
  "hint": "Cross multiply (×2 and ×3), expand fully, then collect x terms.",
  "misconceptions": [
    {"pattern": "incomplete_expansion", "expect": 6,
     "message": "Multiply the whole bracket: \\(2(5x + 2) = 10x + 4\\) and \\(3(3x + 8) = 9x + 24\\). That gives \\(x = 20\\). Multiplying only the \\(x\\) terms gives \\(x = 6\\).",
     "note": "10x+2=9x+8 -> 6"}],
  "guided_steps": [
    box("Two single fractions equal each other, so cross multiply: multiply the left top by 2 and the right top by 3. Left side: 2 × (5x + 2). First 2 × 2 = ", 4, "So 2(5x+2) = 10x + 4.",
        say="Two single fractions equal each other, so cross multiply: the left top times 2, the right top times 3."),
    box("Right side: 3 × (3x + 8). 3 × 8 = ", 24, "So 3(3x+8) = 9x + 24."),
    box("10x " + M + " 9x = ", 1, "10 " + M + " 9 in front of x. Now x + 4 = 24.", post="x",
        say="Now 10x + 4 = 9x + 24. Take 9x off both sides.", phase="substitute"),
    box("24 " + M + " 4 = ", 20, "Take 4 off 24.", say="Now x + 4 = 24. Subtract 4 from both sides.", phase="substitute"),
    box("So x = ", 20, "The value you just found.", phase="substitute"),
    box("Check: (5 × 20 + 2) ÷ 3 = ", 34, "Top: 5×20+2 = 102, then ÷3.", phase="substitute",
        done="And (3 × 20 + 8) ÷ 2 = 68/2 = 34 too. Both sides 34, so x = 20.")]},
 # g2: 2(x-1)/5 = (x+3)/2, x=-19
 {"display": "Solve \\(\\frac{2(x-1)}{5} = \\frac{x+3}{2}\\)", "solutions": [-19], "calculator": False, "input_type": "single_value",
  "hint": "Cross multiply, expand both sides, then collect x terms. The answer is negative.",
  "misconceptions": [
    {"pattern": "sign_slip_negative", "expect": 19,
     "message": "Rearranging \\(4x - 4 = 5x + 15\\) gives \\(-x = 19\\), so \\(x = -19\\). Dropping the minus and writing \\(19\\) is a common slip; check by substituting.",
     "note": "answer is -19 not 19"}],
  "guided_steps": [
    box("Cross multiply: the left top times 2, the right top times 5. Left: 2 × 2(x " + M + " 1) = 4(x " + M + " 1). Expand the left: 4 × (" + M + "1) = ", -4, "So 4(x" + M + "1) = 4x " + M + " 4.",
        say="Cross multiply: the left top times 2, the right top times 5. Left: 2 × 2(x " + M + " 1) = 4(x " + M + " 1). Right: 5 × (x + 3)."),
    box("Expand the right: 5 × 3 = ", 15, "So 5(x+3) = 5x + 15."),
    box("5x " + M + " 4x = ", 1, "5 " + M + " 4 in front of x. Now " + M + "4 = x + 15.", post="x",
        say="Now 4x " + M + " 4 = 5x + 15. Take 4x off both sides.", phase="substitute"),
    box(M + "4 " + M + " 15 = ", -19, "Two negatives add to a bigger negative.",
        say="Now " + M + "4 = x + 15. Subtract 15 from both sides: " + M + "4 " + M + " 15 = x.", phase="substitute"),
    box("So x = ", -19, "The value you just found.", phase="substitute"),
    box("Check: 2 × (" + M + "19 " + M + " 1) ÷ 5 = ", -8, "Top: 2×(" + M + "20) = " + M + "40, then ÷5.", phase="substitute",
        done="2×(" + M + "20)/5 = " + M + "40/5 = " + M + "8, and (" + M + "19 + 3)/2 = " + M + "16/2 = " + M + "8 too. Both sides " + M + "8, so x = " + M + "19.")]},
 # g3 FIXED: 3(2x+1) = 2(4x-3) + 3, x=3  (was +1, x=4 dup with g4)
 {"display": "Solve \\(3(2x + 1) = 2(4x - 3) + 3\\)", "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "Expand both sides carefully (watch the +3 on the right), then collect x terms.",
  "misconceptions": [],
  "guided_steps": [
    box("Expand both sides. Left: 3(2x + 1) = 6x + 3. Right: 2 × (4x " + M + " 3) then + 3. 2 × (" + M + "3) = ", -6, "So 2(4x" + M + "3) = 8x " + M + " 6, then + 3 gives 8x " + M + " 3.",
        say="Expand both sides. Left: 3(2x + 1) = 6x + 3."),
    box("8x " + M + " 6x = ", 2, "8 " + M + " 6 in front of x. Now 3 = 2x " + M + " 3.", post="x",
        say="Now 6x + 3 = 8x " + M + " 3. Take 6x off both sides.", phase="substitute"),
    box("3 + 3 = ", 6, "Now 2x = 6.", say="Now 3 = 2x " + M + " 3. Add 3 to both sides: 3 + 3 = 2x.", phase="substitute"),
    box("6 ÷ 2 = ", 3, "Half of 6.", say="So 2x = 6. Divide both sides by 2.", phase="substitute"),
    box("So x = ", 3, "The value you just found.", phase="substitute"),
    box("Check: 3 × (2 × 3 + 1) = ", 21, "Inside: 2×3+1 = 7, then ×3.", phase="substitute",
        done="3×7 = 21, and 2×(4×3" + M + "3) + 3 = 2×9 + 3 = 21 too. Both sides 21, so x = 3.")]},
 # g4: (7-x)/3 = (x+1)/5, x=4
 {"display": "Solve \\(\\frac{7-x}{3} = \\frac{x+1}{5}\\)", "solutions": [4], "calculator": False, "input_type": "single_value",
  "hint": "Cross multiply (×5 and ×3), then gather x terms on one side.",
  "misconceptions": [
    {"pattern": "sign_error_collecting", "expect": -16,
     "message": "Move \\(-5x\\) across as \\(+5x\\): \\(35 = 8x + 3\\), giving \\(x = 4\\). Subtracting \\(5x\\) from the right by mistake gives \\(-2x = 32\\) and the wrong \\(x = -16\\).",
     "note": "sign error -> -16"}],
  "guided_steps": [
    box("Cross multiply: left top times 5, right top times 3. Left: 5 × (7 " + M + " x). 5 × 7 = ", 35, "So 5(7" + M + "x) = 35 " + M + " 5x.",
        say="Cross multiply: left top times 5, right top times 3."),
    box("Right: 3 × (x + 1). 3 × 1 = ", 3, "So 3(x+1) = 3x + 3."),
    box("35 " + M + " 3 = ", 32, "Take 3 off 35. Now 8x = 32.",
        say="Now 35 " + M + " 5x = 3x + 3. Add 5x to both sides so the x term is positive: 35 = 8x + 3. Subtract 3 from both sides.", phase="substitute"),
    box("32 ÷ 8 = ", 4, "How many 8s in 32?", say="Now 8x = 32. Divide both sides by 8.", phase="substitute"),
    box("So x = ", 4, "The value you just found.", phase="substitute"),
    box("Check: (7 " + M + " 4) ÷ 3 = ", 1, "Top: 7" + M + "4 = 3, then ÷3.", phase="substitute",
        done="3/3 = 1, and (4 + 1)/5 = 5/5 = 1 too. Both sides 1, so x = 4.")]},
]

# ---------------- TIER GUIDES ----------------
tier_guides = {
 "bronze": {
  "title": "Bronze: undo one step at a time",
  "steps": [
    "<strong>Undo in reverse.</strong> Whatever was done to \\(x\\) last, undo first. Work back until \\(x\\) is on its own.",
    "Do the same to <strong>both sides</strong> every time: add, subtract, multiply or divide to keep the balance.",
    "If \\(x\\) is on both sides, take the smaller \\(x\\) term off both sides first, then finish as normal."],
  "example": {
    "question": "Solve 3x " + M + " 4 = 11",
    "steps": [
      {"label": "Add 4 to both sides", "content": "<p>\\(3x = 15\\)</p>"},
      {"label": "Divide by 3", "content": "<p>\\(x = 5\\)</p>"},
      {"label": "Check", "content": "<p>\\(3(5) - 4 = 11\\) ✓</p>"},
      {"label": "Answer", "content": "<p>\\(x = 5\\)</p>", "isAnswer": True, "is_answer": True}]}},
 "silver": {
  "title": "Silver: clear brackets or a fraction first",
  "steps": [
    "<strong>Expand brackets first.</strong> Multiply everything inside by the number outside, then collect like terms.",
    "For a single fraction, <strong>multiply both sides</strong> by the bottom number to clear it.",
    "Then solve the two step equation left behind, and check your answer."],
  "example": {
    "question": "Solve 2(x + 3) = 16",
    "steps": [
      {"label": "Expand", "content": "<p>\\(2x + 6 = 16\\)</p>"},
      {"label": "Subtract 6", "content": "<p>\\(2x = 10\\)</p>"},
      {"label": "Divide by 2", "content": "<p>\\(x = 5\\)</p>"},
      {"label": "Check", "content": "<p>\\(2(5 + 3) = 16\\) ✓</p>"},
      {"label": "Answer", "content": "<p>\\(x = 5\\)</p>", "isAnswer": True, "is_answer": True}]}},
 "gold": {
  "title": "Gold: clear fractions on both sides",
  "steps": [
    "<strong>Clear every fraction first.</strong> Multiply <strong>both sides</strong> by the common denominator, the number both bottoms divide into.",
    "Expand any brackets that appear, then collect the \\(x\\) terms on one side.",
    "Solve, then check by putting your answer back into both original fractions."],
  "example": {
    "question": "Solve (x + 3)/2 = (x + 9)/4",
    "steps": [
      {"label": "Multiply by 4", "content": "<p>\\(2(x + 3) = x + 9\\)</p>"},
      {"label": "Expand", "content": "<p>\\(2x + 6 = x + 9\\)</p>"},
      {"label": "Solve", "content": "<p>\\(x = 3\\)</p>"},
      {"label": "Check", "content": "<p>\\(\\frac{3+3}{2} = 3\\) and \\(\\frac{3+9}{4} = 3\\) ✓</p>"},
      {"label": "Answer", "content": "<p>\\(x = 3\\)</p>", "isAnswer": True, "is_answer": True}]}},
}

# ---------------- GUIDED (opener + teach) ----------------
guided = {
 "opener": {
  "label": "Before any algebra",
  "display": "A magician says:<br><strong>“Think of a number. Triple it, add 4, and tell me the total.”</strong><br>You say 19. The magician instantly names your number. How? Work backwards.",
  "steps": [
    {"say": "No algebra needed, just undo the magician's moves in reverse. The last thing they did was add 4, so take it off.",
     "pre": "19 " + M + " 4 = ", "post": "", "answer": 15,
     "hint": "Take 4 off 19."},
    {"say": "Before that, they tripled the number (multiplied by 3). Undo a multiply with a divide.",
     "pre": "15 ÷ 3 = ", "post": "", "answer": 5,
     "hint": "How many 3s in 15?"},
    {"say": "The number was 5. You just solved \\(3x + 4 = 19\\) by working backwards, undoing each step in reverse order. That is exactly what solving a linear equation means: peel off the operations until \\(x\\) stands alone."}]},
 "teach": {
  "bronze": {
   "display": "Solve \\(6x + 1 = 4x + 9\\)",
   "label": "Together: x on both sides",
   "steps": [
     {"say": "Both sides have an x term. The new move: get all the x on one side. Take the smaller one, 4x, off both sides.",
      "pre": "6x " + M + " 4x = ", "post": "x", "answer": 2,
      "hint": "Subtract the numbers in front: 6 " + M + " 4."},
     {"say": "The right side loses its 4x, leaving just 9. So now 2x + 1 = 9. Undo the +1.",
      "pre": "9 " + M + " 1 = ", "post": "", "answer": 8,
      "hint": "Take 1 off 9. Now 2x = 8."},
     {"say": "Now 2x = 8. Divide both sides by 2.",
      "pre": "8 ÷ 2 = ", "post": "", "answer": 4,
      "hint": "Half of 8."},
     {"say": "Last thing: check x = 4 in the original.",
      "pre": "6 × 4 + 1 = ", "post": "", "answer": 25,
      "done": "And 4 × 4 + 9 = 25 too. Both sides equal, so x = 4. Collecting x on one side was the whole point.",
      "hint": "Work out 6×4 then add 1."}]},
  "silver": {
   "display": "Solve \\(5(x - 2) = 3x + 4\\)",
   "label": "Together: expand the bracket",
   "steps": [
     {"say": "The new move: expand the bracket before anything else. Multiply both terms inside by 5. First 5 × x.",
      "pre": "5 × x = ", "post": "x", "answer": 5,
      "hint": "5 times x is 5x."},
     {"say": "Now the second term inside, keeping the minus.",
      "pre": "5 × (" + M + "2) = ", "post": "", "answer": -10,
      "hint": "5 times 2 is 10, and the sign stays minus. So the left is 5x " + M + " 10."},
     {"say": "Now 5x " + M + " 10 = 3x + 4. Take 3x off both sides.",
      "pre": "5x " + M + " 3x = ", "post": "x", "answer": 2,
      "hint": "5 " + M + " 3 in front of x. Now 2x " + M + " 10 = 4."},
     {"say": "Now 2x " + M + " 10 = 4. Add 10 to both sides.",
      "pre": "4 + 10 = ", "post": "", "answer": 14,
      "hint": "Now 2x = 14."},
     {"say": "Now 2x = 14. Divide both sides by 2.",
      "pre": "14 ÷ 2 = ", "post": "", "answer": 7,
      "hint": "Half of 14."},
     {"say": "Check x = 7 in the original.",
      "pre": "5 × (7 " + M + " 2) = ", "post": "", "answer": 25,
      "done": "And 3 × 7 + 4 = 25. Balanced, so x = 7. Expanding the bracket unlocked it.",
      "hint": "Inside first: 7" + M + "2 = 5, then ×5."}]},
  "gold": {
   "display": "Solve \\(\\frac{x + 4}{2} = \\frac{2x - 1}{3}\\)",
   "label": "Together: clear fractions both sides",
   "steps": [
     {"say": "The new move: clear both fractions at once. The bottoms are 2 and 3, so multiply both sides by 6. Left: 6 ÷ 2 = 3, so 3(x + 4). Expand it: 3 × 4.",
      "pre": "3 × 4 = ", "post": "", "answer": 12,
      "hint": "So the left becomes 3x + 12."},
     {"say": "Right: 6 ÷ 3 = 2, so 2(2x " + M + " 1). Expand it, keeping the minus.",
      "pre": "2 × (" + M + "1) = ", "post": "", "answer": -2,
      "hint": "So the right becomes 4x " + M + " 2."},
     {"say": "Now 3x + 12 = 4x " + M + " 2. Take 3x off both sides.",
      "pre": "4x " + M + " 3x = ", "post": "x", "answer": 1,
      "hint": "4 " + M + " 3 in front of x. Now 12 = x " + M + " 2."},
     {"say": "Now 12 = x " + M + " 2. Add 2 to both sides.",
      "pre": "12 + 2 = ", "post": "", "answer": 14,
      "hint": "This gives x."},
     {"say": "Check x = 14 in the original.",
      "pre": "(14 + 4) ÷ 2 = ", "post": "", "answer": 9,
      "done": "And (2 × 14 " + M + " 1) ÷ 3 = 27/3 = 9 too. Both sides 9, so x = 14. Clearing the fractions turned it into an ordinary equation.",
      "hint": "Top first: 14+4 = 18, then ÷2."}]},
 },
}

# ---------------- METHOD CARD (slim) ----------------
method_card = {
 "title": "How to Solve Linear Equations",
 "steps": [
   "Expand any brackets and clear fractions first",
   "Collect the unknown on one side, constants on the other",
   "Simplify each side by combining like terms",
   "Divide by the coefficient of the unknown, then check"],
 "content": "<p>A <strong>linear equation</strong> has \\(x\\) to the power 1. Solving means finding the value that makes it true.</p><p>Undo the operations in reverse, doing the same to <strong>both sides</strong>. Expand brackets first, and clear fractions by multiplying every term by the common denominator. If \\(x\\) is on both sides, collect it on one side, then divide to finish. Always check by substituting your answer back in.</p>",
 "example": "<p><strong>Solve</strong> \\(3(2x - 1) = 4x + 9\\)</p><p><strong>Expand:</strong> \\(6x - 3 = 4x + 9\\)</p><p><strong>Collect:</strong> \\(2x = 12\\)</p><p><strong>Divide:</strong> \\(x = 6\\)</p>",
}

# ---------------- ASSEMBLE ----------------
pd = {
 "method_card": method_card,
 "topic_links": live.get("topic_links", {"prerequisites": []}),
 "problem_bank": {
   "bronze": bronze, "silver": silver, "gold": gold,
   "bronze_description": "One and two step equations: undo the operations in reverse, including equations with x on both sides.",
   "silver_description": "Expand brackets or clear a single fraction first, then solve the equation left behind.",
   "gold_description": "Clear fractions on both sides by multiplying by the common denominator, then expand and solve.",
 },
 "tier_guides": tier_guides,
 "guided": guided,
 "related_videos": live.get("related_videos", []),
 "worked_examples": live.get("worked_examples", []),
}

json.dump(pd, io.open("lesson_maths-aqa_algebra-L05.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_maths-aqa_algebra-L05.json")

# quick self-check: word count of method_card content
def words(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
print("method_card.content words:", words(method_card["content"]))
for t in ("bronze","silver","gold"):
    print(t, "tier_guide steps words:", sum(words(s) for s in tier_guides[t]["steps"]))
