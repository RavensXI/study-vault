# -*- coding: utf-8 -*-
"""Builder for number-L02 (Fractions) guided-learning conversion."""
import json, io

MINUS = "−"  # unicode minus

def box(pre, answer, hint, post=None, say=None, done=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post is not None:
        d["post"] = post
    if say is not None:
        d["say"] = say
    if done is not None:
        d["done"] = done
    if phase is not None:
        d["phase"] = phase
    return d

def sy(s):
    return {"say": s}

def mis(pattern, expect, message, note):
    if expect is None:
        check = "wrong"
    elif isinstance(expect, list) and len(expect) == 2:
        check = "equals_%d_%d" % (expect[0], expect[1])
    else:
        v = expect[0] if isinstance(expect, list) else expect
        check = "equals_%s" % v
    return {"pattern": pattern, "check": check, "expect": expect,
            "message": message, "note": note}

# ---------------------------------------------------------------- BRONZE
bronze = []

# B0: 1/3 + 1/6 = 1/2
bronze.append({
 "display": "\\(\\frac{1}{3} + \\frac{1}{6}\\)",
 "solutions": [1, 2], "calculator": False, "input_type": "fraction",
 "hint": "Turn 1/3 into sixths, then add the tops.",
 "misconceptions": [
   mis("add_denominators", [2, 9],
       "Don't add the denominators. Find a common denominator first: 1/3 = 2/6, then 2/6 + 1/6 = 3/6 = 1/2.",
       "Student adds numerators AND denominators: (1+1)/(3+6) = 2/9."),
   mis("no_simplify", [3, 6],
       "3/6 is correct but needs simplifying. Divide top and bottom by 3 to get 1/2.",
       "Student adds correctly to 3/6 but stops without simplifying."),
 ],
 "guided_steps": [
   box("The lowest number both 3 and 6 divide into is the common denominator. It is ", 6,
       "The smallest number in both the 3 and the 6 times tables."),
   box("Convert 1/3 into sixths. 3 goes into 6 twice, so the new top is ", 2,
       "Multiply the top of 1/3 by 2."),
   sy("The second fraction, 1/6, is already in sixths."),
   box("Now add the tops: 2 + 1 = ", 3,
       "Add the numerators, keep the denominator 6.", phase="substitute"),
   box("That gives 3/6. Simplify by dividing top and bottom by 3. Top: 3 ÷ 3 = ", 1,
       "3 divided by 3."),
   box("Bottom: 6 ÷ 3 = ", 2,
       "6 divided by 3.", done="So 1/3 + 1/6 = 1/2."),
   box("Check: turn 1/2 back into sixths. 1 × 3 = ", 3,
       "If it gives 3/6, the answer matches the sum.", done="3/6 matches, so 1/2 is correct."),
 ]})

# B1: 5/6 - 1/6 = 2/3   (CHANGED from 3/4 - 1/4 to de-duplicate [1,2])
bronze.append({
 "display": "\\(\\frac{5}{6} - \\frac{1}{6}\\)",
 "solutions": [2, 3], "calculator": False, "input_type": "fraction",
 "hint": "Same denominator: subtract the tops, then simplify.",
 "misconceptions": [
   mis("subtract_denom", None,
       "The denominators are the same, so keep the 6. Just subtract the tops: 5 " + MINUS + " 1 = 4, then simplify 4/6 = 2/3.",
       "Subtracting denominators too gives 4/0, which is undefined; no single determinate wrong answer."),
   mis("no_simplify", [4, 6],
       "4/6 is correct but simplify by dividing top and bottom by 2 to get 2/3.",
       "Student subtracts correctly to 4/6 but stops without simplifying."),
 ],
 "guided_steps": [
   box("Both fractions are already sixths, so the answer keeps the denominator ", 6,
       "Same denominators stay the same when subtracting."),
   box("Subtract the tops: 5 " + MINUS + " 1 = ", 4,
       "Take 1 away from 5.", phase="substitute"),
   box("That gives 4/6. Simplify by dividing top and bottom by 2. Top: 4 ÷ 2 = ", 2,
       "4 divided by 2."),
   box("Bottom: 6 ÷ 2 = ", 3,
       "6 divided by 2.", done="So 5/6 " + MINUS + " 1/6 = 2/3."),
   box("Check: turn 2/3 back into sixths. 2 × 2 = ", 4,
       "If it gives 4/6, the answer matches.", done="4/6 matches, so 2/3 is correct."),
 ]})

# B2: 2/5 + 1/5 = 3/5
bronze.append({
 "display": "\\(\\frac{2}{5} + \\frac{1}{5}\\)",
 "solutions": [3, 5], "calculator": False, "input_type": "fraction",
 "hint": "Same denominator already: just add the tops.",
 "misconceptions": [
   mis("add_denominators", [3, 10],
       "Same denominator already! Just add the tops: 2 + 1 = 3, keeping /5. Answer: 3/5.",
       "Student adds numerators AND denominators: (2+1)/(5+5) = 3/10."),
   mis("arithmetic", None,
       "2/5 + 1/5 = 3/5. Same denominator, so just add the tops.",
       "Generic arithmetic slip, no single determinate wrong answer."),
 ],
 "guided_steps": [
   box("The denominators are both 5, so the answer's denominator is ", 5,
       "Same denominators stay the same when adding."),
   box("Add the tops: 2 + 1 = ", 3,
       "Add the numerators, keep the denominator 5.", phase="substitute"),
   box("Check by subtracting back: 3 " + MINUS + " 1 = ", 2,
       "Should give 2, the first fraction's top.", done="2/5 was the first fraction, so 3/5 is right."),
 ]})

# B3: 1/2 x 3/4 = 3/8
bronze.append({
 "display": "\\(\\frac{1}{2} \\times \\frac{3}{4}\\)",
 "solutions": [3, 8], "calculator": False, "input_type": "fraction",
 "hint": "Multiply straight across: tops together, bottoms together.",
 "misconceptions": [
   mis("common_denom", None,
       "You don't need a common denominator for multiplying. Just multiply across: 1×3 = 3, 2×4 = 8. Answer: 3/8.",
       "Student wrongly looks for an LCD before multiplying."),
   mis("arithmetic", None,
       "Multiply tops: 1 × 3 = 3. Multiply bottoms: 2 × 4 = 8. Answer: 3/8.",
       "Generic arithmetic slip, no single determinate wrong answer."),
 ],
 "guided_steps": [
   box("Multiplying needs no common denominator. Multiply the tops: 1 × 3 = ", 3,
       "Multiply the two numerators."),
   box("Multiply the bottoms: 2 × 4 = ", 8,
       "Multiply the two denominators.", phase="substitute"),
   box("Check by simplifying: the highest common factor of 3 and 8 is 1, so 3 ÷ 1 = ", 3,
       "Nothing cancels.", done="3/8 is already simplest, so it is the final answer."),
 ]})

# B4: 4/5 - 1/2 = 3/10
bronze.append({
 "display": "\\(\\frac{4}{5} - \\frac{1}{2}\\)",
 "solutions": [3, 10], "calculator": False, "input_type": "fraction",
 "hint": "Find the common denominator 10, convert both, then subtract.",
 "misconceptions": [
   mis("no_common_denom", None,
       "Different denominators, so find the LCD (10): 4/5 = 8/10 and 1/2 = 5/10. Then 8/10 " + MINUS + " 5/10 = 3/10.",
       "Student subtracts without converting; result varies, no single determinate answer."),
   mis("subtract_across", [3, 3],
       "You can't subtract tops and bottoms separately. Find a common denominator first.",
       "Student subtracts across: (4-1)/(5-2) = 3/3."),
 ],
 "guided_steps": [
   box("The common denominator of 5 and 2 is ", 10,
       "The smallest number in both the 5 and 2 times tables."),
   box("Convert 4/5 into tenths: 5 goes into 10 twice, so 4 × 2 = ", 8,
       "Multiply the top of 4/5 by 2."),
   box("Convert 1/2 into tenths: 2 goes into 10 five times, so 1 × 5 = ", 5,
       "Multiply the top of 1/2 by 5."),
   box("Subtract the tops: 8 " + MINUS + " 5 = ", 3,
       "Take 5 away from 8, keep the denominator 10.", phase="substitute"),
   box("The denominator stays ", 10,
       "Only the tops were subtracted.", done="So 4/5 " + MINUS + " 1/2 = 3/10."),
   box("Check: 3 and 10 share no factor, so 3/10 is simplest. Add back 3 + 5 = ", 8,
       "Should give 8, the first fraction in tenths.", done="8/10 = 4/5, so 3/10 is right."),
 ]})

# B5: 2/3 x 3/5 = 2/5
bronze.append({
 "display": "\\(\\frac{2}{3} \\times \\frac{3}{5}\\)",
 "solutions": [2, 5], "calculator": False, "input_type": "fraction",
 "hint": "Multiply across, then simplify the result.",
 "misconceptions": [
   mis("common_denom", None,
       "For multiplying, just multiply across: 2×3 = 6, 3×5 = 15. Simplify: 6/15 = 2/5.",
       "Student wrongly looks for an LCD before multiplying."),
   mis("no_simplify", [6, 15],
       "6/15 is correct but simplify by dividing both by 3 to get 2/5.",
       "Student multiplies correctly to 6/15 but stops without simplifying."),
 ],
 "guided_steps": [
   box("Multiply the tops: 2 × 3 = ", 6,
       "Multiply the two numerators."),
   box("Multiply the bottoms: 3 × 5 = ", 15,
       "Multiply the two denominators.", phase="substitute"),
   box("That gives 6/15. Simplify by dividing top and bottom by 3. Top: 6 ÷ 3 = ", 2,
       "6 divided by 3."),
   box("Bottom: 15 ÷ 3 = ", 5,
       "15 divided by 3.", done="So 2/3 × 3/5 = 2/5."),
   box("Check: turn 2/5 back up by 3. 2 × 3 = ", 6,
       "If it gives 6/15, the answer matches.", done="6/15 matches, so 2/5 is correct."),
 ]})

# B6: 1/3 + 1/4 = 7/12
bronze.append({
 "display": "\\(\\frac{1}{3} + \\frac{1}{4}\\)",
 "solutions": [7, 12], "calculator": False, "input_type": "fraction",
 "hint": "Convert both to twelfths, then add the tops.",
 "misconceptions": [
   mis("add_denominators", [2, 7],
       "Don't add denominators! LCD of 3 and 4 is 12: 4/12 + 3/12 = 7/12.",
       "Student adds numerators AND denominators: (1+1)/(3+4) = 2/7."),
   mis("arithmetic", None,
       "Convert to twelfths: 1/3 = 4/12 and 1/4 = 3/12. Add: 7/12.",
       "Generic arithmetic slip in conversion or addition."),
 ],
 "guided_steps": [
   box("The common denominator of 3 and 4 is ", 12,
       "The smallest number in both times tables: 3 × 4."),
   box("Convert 1/3 into twelfths: 3 goes into 12 four times, so 1 × 4 = ", 4,
       "Multiply the top of 1/3 by 4."),
   box("Convert 1/4 into twelfths: 4 goes into 12 three times, so 1 × 3 = ", 3,
       "Multiply the top of 1/4 by 3."),
   box("Add the tops: 4 + 3 = ", 7,
       "Add the numerators, keep the denominator 12.", phase="substitute"),
   box("The denominator stays ", 12,
       "Only the tops were added.", done="So 1/3 + 1/4 = 7/12."),
   box("Check: 7 and 12 share no factor, so 7/12 is simplest. Subtract back 7 " + MINUS + " 3 = ", 4,
       "Should give 4, the first fraction in twelfths.", done="4/12 = 1/3, so 7/12 is right."),
 ]})

# B7: 5/6 - 1/2 = 1/3   (CHANGED from 5/6 - 1/3 to de-duplicate [1,2])
bronze.append({
 "display": "\\(\\frac{5}{6} - \\frac{1}{2}\\)",
 "solutions": [1, 3], "calculator": False, "input_type": "fraction",
 "hint": "Convert 1/2 to sixths, subtract, then simplify.",
 "misconceptions": [
   mis("no_common_denom", None,
       "Convert 1/2 to sixths first: 1/2 = 3/6. Then 5/6 " + MINUS + " 3/6 = 2/6 = 1/3.",
       "Student subtracts without converting; result varies, no single determinate answer."),
   mis("subtract_across", [4, 4],
       "You can't subtract tops and bottoms separately. Use the common denominator 6.",
       "Student subtracts across: (5-1)/(6-2) = 4/4."),
 ],
 "guided_steps": [
   box("The common denominator of 6 and 2 is ", 6,
       "6 is already in the 2 times table."),
   box("Convert 1/2 into sixths: 2 goes into 6 three times, so 1 × 3 = ", 3,
       "Multiply the top of 1/2 by 3."),
   sy("The first fraction, 5/6, is already in sixths."),
   box("Subtract the tops: 5 " + MINUS + " 3 = ", 2,
       "Take 3 away from 5, keep the denominator 6.", phase="substitute"),
   box("That gives 2/6. Simplify by dividing top and bottom by 2. Top: 2 ÷ 2 = ", 1,
       "2 divided by 2."),
   box("Bottom: 6 ÷ 2 = ", 3,
       "6 divided by 2.", done="So 5/6 " + MINUS + " 1/2 = 1/3."),
   box("Check: turn 1/3 back into sixths. 1 × 2 = ", 2,
       "If it gives 2/6, the answer matches.", done="2/6 matches, so 1/3 is correct."),
 ]})

# ---------------------------------------------------------------- SILVER
silver = []

# S0: 3/4 / 1/2 = 3/2
silver.append({
 "display": "\\(\\frac{3}{4} \\div \\frac{1}{2}\\)",
 "solutions": [3, 2], "calculator": False, "input_type": "fraction",
 "hint": "Keep the first, flip the second, then multiply.",
 "misconceptions": [
   mis("no_flip", [3, 8],
       "For dividing, flip the second fraction then multiply: 3/4 × 2/1 = 6/4 = 3/2.",
       "Student multiplies without flipping: 3/4 × 1/2 = 3/8."),
   mis("flip_wrong", [2, 3],
       "Keep the first, flip the second: 3/4 × 2/1.",
       "Student flips the first fraction instead of the second: 4/3 × 1/2 = 4/6 = 2/3."),
 ],
 "guided_steps": [
   box("To divide, flip the second fraction. The reciprocal of 1/2 is 2 over 1, so its new top is ", 2,
       "Swap the top and bottom of 1/2."),
   sy("Now the sum is 3/4 × 2/1."),
   box("Multiply the tops: 3 × 2 = ", 6,
       "Multiply the two numerators.", phase="substitute"),
   box("Multiply the bottoms: 4 × 1 = ", 4,
       "Multiply the two denominators."),
   box("That gives 6/4. Simplify by dividing top and bottom by 2. Top: 6 ÷ 2 = ", 3,
       "6 divided by 2."),
   box("Bottom: 4 ÷ 2 = ", 2,
       "4 divided by 2.", done="So 3/4 ÷ 1/2 = 3/2 = 1 1/2."),
   box("Check: multiply the answer back. 3/2 × 1/2, tops: 3 × 1 = ", 3,
       "If it rebuilds 3/4, the answer is right.", done="3/2 × 1/2 = 3/4, so 3/2 is correct."),
 ]})

# S1: 2/3 + 5/8 = 31/24
silver.append({
 "display": "\\(\\frac{2}{3} + \\frac{5}{8}\\)",
 "solutions": [31, 24], "calculator": False, "input_type": "fraction",
 "hint": "The LCD of 3 and 8 is 24; convert both and add.",
 "misconceptions": [
   mis("add_denominators", [7, 11],
       "LCD of 3 and 8 is 24: 16/24 + 15/24 = 31/24.",
       "Student adds numerators AND denominators: (2+5)/(3+8) = 7/11."),
   mis("wrong_lcd", None,
       "The LCD of 3 and 8 is 24. Convert: 2/3 = 16/24 and 5/8 = 15/24.",
       "3×8 = 24 is the correct LCM here, so a wrong LCD gives unpredictable results."),
 ],
 "guided_steps": [
   box("The common denominator of 3 and 8 is ", 24,
       "3 × 8, since they share no factor."),
   box("Convert 2/3 into 24ths: 3 goes into 24 eight times, so 2 × 8 = ", 16,
       "Multiply the top of 2/3 by 8."),
   box("Convert 5/8 into 24ths: 8 goes into 24 three times, so 5 × 3 = ", 15,
       "Multiply the top of 5/8 by 3."),
   box("Add the tops: 16 + 15 = ", 31,
       "Add the numerators, keep the denominator 24.", phase="substitute"),
   box("The denominator stays ", 24,
       "Only the tops were added.", done="So 2/3 + 5/8 = 31/24 = 1 7/24."),
   box("Check: 31 is prime, so 31/24 will not simplify. Subtract back 31 " + MINUS + " 15 = ", 16,
       "Should give 16, the first fraction in 24ths.", done="16/24 = 2/3, so 31/24 is right."),
 ]})

# S2: 7/8 x 4/7 = 1/2   (removed duplicate no_simplify, keep no_cancel)
silver.append({
 "display": "\\(\\frac{7}{8} \\times \\frac{4}{7}\\)",
 "solutions": [1, 2], "calculator": False, "input_type": "fraction",
 "hint": "Cross-cancel the 7s before multiplying to keep it simple.",
 "misconceptions": [
   mis("no_cancel", [28, 56],
       "Cross-cancel the 7s before multiplying: (1/8) × (4/1) = 4/8 = 1/2. Multiplying straight across leaves 28/56, the same value but not simplified.",
       "Student multiplies straight across without cancelling: 7×4=28 over 8×7=56."),
 ],
 "guided_steps": [
   box("Multiply the tops: 7 × 4 = ", 28,
       "Multiply the two numerators."),
   box("Multiply the bottoms: 8 × 7 = ", 56,
       "Multiply the two denominators.", phase="substitute"),
   box("That gives 28/56. Simplify by dividing top and bottom by 28. Top: 28 ÷ 28 = ", 1,
       "28 divided by 28."),
   box("Bottom: 56 ÷ 28 = ", 2,
       "56 divided by 28.", done="So 7/8 × 4/7 = 1/2."),
   box("Check: turn 1/2 back up by 28. 1 × 28 = ", 28,
       "If it gives 28/56, the answer matches.", done="28/56 matches, so 1/2 is correct."),
 ]})

# S3: 1 1/2 + 3/4 = 9/4
silver.append({
 "display": "\\(1\\frac{1}{2} + \\frac{3}{4}\\)",
 "solutions": [9, 4], "calculator": False, "input_type": "fraction",
 "hint": "Turn 1 1/2 into 3/2 first, then find the common denominator.",
 "misconceptions": [
   mis("no_convert", [5, 4],
       "Convert the mixed number: 1 1/2 = 3/2. LCD of 2 and 4 is 4: 6/4 + 3/4 = 9/4 = 2 1/4.",
       "Student ignores the whole number 1 and only adds 1/2 + 3/4 = 5/4."),
   mis("wrong_improper", None,
       "1 1/2 as an improper fraction is 3/2 (1 × 2 + 1 = 3, over 2).",
       "Wrong improper conversions for 1 1/2 vary, no single determinate answer."),
 ],
 "guided_steps": [
   box("Convert the mixed number 1 1/2 to an improper fraction. Top: 1 × 2 + 1 = ", 3,
       "Whole times denominator, plus the top."),
   sy("So 1 1/2 = 3/2. The sum is now 3/2 + 3/4."),
   box("The common denominator of 2 and 4 is ", 4,
       "4 is already in the 2 times table."),
   box("Convert 3/2 into quarters: 2 goes into 4 twice, so 3 × 2 = ", 6,
       "Multiply the top of 3/2 by 2."),
   box("Add the tops: 6 + 3 = ", 9,
       "Add the numerators, keep the denominator 4.", phase="substitute"),
   box("The denominator stays ", 4,
       "Only the tops were added.", done="So 1 1/2 + 3/4 = 9/4 = 2 1/4."),
   box("Check: subtract back 9 " + MINUS + " 3 = ", 6,
       "Should give 6, which is 3/2 in quarters.", done="6/4 = 3/2 = 1 1/2, so 9/4 is right."),
 ]})

# S4: 2 1/3 x 3/7 = 1  (single_value)
silver.append({
 "display": "\\(2\\frac{1}{3} \\times \\frac{3}{7}\\)",
 "solutions": [1], "calculator": False, "input_type": "single_value",
 "hint": "Convert 2 1/3 to 7/3, then multiply across.",
 "misconceptions": [
   mis("no_convert", None,
       "Convert first: 2 1/3 = 7/3. Then 7/3 × 3/7 = 21/21 = 1.",
       "Using only the whole number 2 gives 6/7, but distributing gives 1; not determinate."),
   mis("wrong_improper", None,
       "2 1/3 = 7/3 (2 × 3 + 1 = 7, over 3).",
       "Wrong improper conversions vary, no single determinate answer."),
 ],
 "guided_steps": [
   box("Convert 2 1/3 to an improper fraction. Top: 2 × 3 + 1 = ", 7,
       "Whole times denominator, plus the top."),
   sy("So 2 1/3 = 7/3. The sum is 7/3 × 3/7."),
   box("Multiply the tops: 7 × 3 = ", 21,
       "Multiply the two numerators.", phase="substitute"),
   box("Multiply the bottoms: 3 × 7 = ", 21,
       "Multiply the two denominators."),
   box("That gives 21/21. A fraction with equal top and bottom equals ", 1,
       "Anything over itself is one whole.", done="So 2 1/3 × 3/7 = 1."),
   box("Check: 21 ÷ 21 = ", 1,
       "Top divided by bottom.", done="It equals 1, so the answer is right."),
 ]})

# S5: 5/6 / 5/12 = 2  (single_value)
silver.append({
 "display": "\\(\\frac{5}{6} \\div \\frac{5}{12}\\)",
 "solutions": [2], "calculator": False, "input_type": "single_value",
 "hint": "Keep, flip, multiply: 5/6 × 12/5.",
 "misconceptions": [
   mis("no_flip", None,
       "Flip and multiply: 5/6 × 12/5. Cancel the 5s: 1/6 × 12/1 = 12/6 = 2.",
       "Multiplying without flipping gives 25/72, not a whole number."),
   mis("arithmetic", None,
       "5/6 × 12/5: cancel the 5s and simplify 12/6 = 2.",
       "Generic arithmetic slip in the cancelling step."),
 ],
 "guided_steps": [
   box("To divide, flip the second fraction. The reciprocal of 5/12 is 12 over 5, so its new top is ", 12,
       "Swap the top and bottom of 5/12."),
   sy("Now the sum is 5/6 × 12/5."),
   box("Multiply the tops: 5 × 12 = ", 60,
       "Multiply the two numerators.", phase="substitute"),
   box("Multiply the bottoms: 6 × 5 = ", 30,
       "Multiply the two denominators."),
   box("That gives 60/30. Divide: 60 ÷ 30 = ", 2,
       "Top divided by bottom.", done="So 5/6 ÷ 5/12 = 2."),
   box("Check: multiply back. 2 × 5/12, tops: 2 × 5 = ", 10,
       "If it rebuilds 5/6, the answer is right.", done="10/12 = 5/6, so 2 is correct."),
 ]})

# S6: 7/10 - 2/5 = 3/10
silver.append({
 "display": "\\(\\frac{7}{10} - \\frac{2}{5}\\)",
 "solutions": [3, 10], "calculator": False, "input_type": "fraction",
 "hint": "Convert 2/5 to tenths, then subtract.",
 "misconceptions": [
   mis("no_common_denom", [5, 5],
       "Convert 2/5 to tenths: 2/5 = 4/10. Then 7/10 " + MINUS + " 4/10 = 3/10.",
       "Student subtracts tops and bottoms separately without converting: (7-2)/(10-5) = 5/5."),
 ],
 "guided_steps": [
   box("The common denominator of 10 and 5 is ", 10,
       "10 is already in the 5 times table."),
   box("Convert 2/5 into tenths: 5 goes into 10 twice, so 2 × 2 = ", 4,
       "Multiply the top of 2/5 by 2."),
   sy("The first fraction, 7/10, is already in tenths."),
   box("Subtract the tops: 7 " + MINUS + " 4 = ", 3,
       "Take 4 away from 7, keep the denominator 10.", phase="substitute"),
   box("The denominator stays ", 10,
       "Only the tops were subtracted.", done="So 7/10 " + MINUS + " 2/5 = 3/10."),
   box("Check: 3 and 10 share no factor, so 3/10 is simplest. Add back 3 + 4 = ", 7,
       "Should give 7, the first fraction in tenths.", done="7/10 was the first fraction, so 3/10 is right."),
 ]})

# ---------------------------------------------------------------- GOLD
gold = []

# G0: 3 1/4 - 1 2/3 = 19/12  (CHANGED from 2 3/4 - 1 2/3 so borrowing is genuinely needed)
gold.append({
 "display": "\\(3\\frac{1}{4} - 1\\frac{2}{3}\\)",
 "solutions": [19, 12], "calculator": False, "input_type": "fraction",
 "hint": "Convert both to improper fractions first, then find the LCD.",
 "misconceptions": [
   mis("wrong_improper", None,
       "3 1/4 = 13/4 and 1 2/3 = 5/3. LCD is 12: 39/12 " + MINUS + " 20/12 = 19/12 = 1 7/12.",
       "Wrong improper conversions vary, no single determinate answer."),
   mis("subtract_wholes_fracs", [29, 12],
       "You can't subtract the whole parts and fraction parts separately here, because 1/4 is smaller than 2/3. Convert to improper fractions: 3 1/4 = 13/4 and 1 2/3 = 5/3.",
       "Student does wholes 3-1=2 and flips the fraction gap to 2/3-1/4=5/12, giving 2 5/12 = 29/12."),
 ],
 "guided_steps": [
   box("Convert 3 1/4 to an improper fraction. Top: 3 × 4 + 1 = ", 13,
       "Whole times denominator, plus the top."),
   box("Convert 1 2/3 to an improper fraction. Top: 1 × 3 + 2 = ", 5,
       "Whole times denominator, plus the top."),
   box("The common denominator of 4 and 3 is ", 12,
       "4 × 3, since they share no factor."),
   box("Convert 13/4 into twelfths: 4 goes into 12 three times, so 13 × 3 = ", 39,
       "Multiply the top of 13/4 by 3."),
   box("Convert 5/3 into twelfths: 3 goes into 12 four times, so 5 × 4 = ", 20,
       "Multiply the top of 5/3 by 4."),
   box("Subtract the tops: 39 " + MINUS + " 20 = ", 19,
       "Take 20 away from 39, keep the denominator 12.", phase="substitute"),
   box("The denominator stays ", 12,
       "Only the tops were subtracted.", done="So 3 1/4 " + MINUS + " 1 2/3 = 19/12 = 1 7/12."),
   box("Check by adding back: 20 + 19 = ", 39,
       "Should give 39, the first fraction in twelfths.", done="39/12 = 3 1/4, so 19/12 is right."),
 ]})

# G1: 1 2/5 x 2 1/2 = 7/2
gold.append({
 "display": "\\(1\\frac{2}{5} \\times 2\\frac{1}{2}\\)",
 "solutions": [7, 2], "calculator": False, "input_type": "fraction",
 "hint": "Convert both to improper fractions, then multiply across.",
 "misconceptions": [
   mis("wrong_improper", None,
       "1 2/5 = 7/5 and 2 1/2 = 5/2. Then 7/5 × 5/2 = 35/10 = 7/2 = 3 1/2.",
       "Wrong improper conversions vary, no single determinate answer."),
   mis("multiply_wholes_fracs", [11, 5],
       "Don't multiply whole parts and fraction parts separately. Convert to improper fractions first.",
       "Student multiplies wholes 1x2=2 and fractions 2/5x1/2=1/5, then adds: 2 + 1/5 = 11/5."),
 ],
 "guided_steps": [
   box("Convert 1 2/5 to an improper fraction. Top: 1 × 5 + 2 = ", 7,
       "Whole times denominator, plus the top."),
   box("Convert 2 1/2 to an improper fraction. Top: 2 × 2 + 1 = ", 5,
       "Whole times denominator, plus the top."),
   box("Multiply the tops: 7 × 5 = ", 35,
       "Multiply the two numerators.", phase="substitute"),
   box("Multiply the bottoms: 5 × 2 = ", 10,
       "Multiply the two denominators."),
   box("That gives 35/10. Simplify by dividing top and bottom by 5. Top: 35 ÷ 5 = ", 7,
       "35 divided by 5."),
   box("Bottom: 10 ÷ 5 = ", 2,
       "10 divided by 5.", done="So 1 2/5 × 2 1/2 = 7/2 = 3 1/2."),
   box("Check: turn 7/2 back up by 5. 7 × 5 = ", 35,
       "If it gives 35/10, the answer matches.", done="35/10 matches, so 7/2 is correct."),
 ]})

# G2: 3 1/3 / 1 2/3 = 2  (single_value)
gold.append({
 "display": "\\(3\\frac{1}{3} \\div 1\\frac{2}{3}\\)",
 "solutions": [2], "calculator": False, "input_type": "single_value",
 "hint": "Convert to improper, then keep, flip, multiply.",
 "misconceptions": [
   mis("wrong_improper", None,
       "3 1/3 = 10/3 and 1 2/3 = 5/3. Then 10/3 ÷ 5/3 = 10/3 × 3/5 = 30/15 = 2.",
       "Wrong improper conversions vary, no single determinate answer."),
   mis("no_flip", None,
       "For dividing, flip the second fraction: 10/3 × 3/5.",
       "Multiplying without flipping gives 50/9, not a whole number."),
 ],
 "guided_steps": [
   box("Convert 3 1/3 to an improper fraction. Top: 3 × 3 + 1 = ", 10,
       "Whole times denominator, plus the top."),
   box("Convert 1 2/3 to an improper fraction. Top: 1 × 3 + 2 = ", 5,
       "Whole times denominator, plus the top."),
   box("To divide, flip the second fraction. The reciprocal of 5/3 is 3 over 5, so its new top is ", 3,
       "Swap the top and bottom of 5/3."),
   sy("Now the sum is 10/3 × 3/5."),
   box("Multiply the tops: 10 × 3 = ", 30,
       "Multiply the two numerators.", phase="substitute"),
   box("Multiply the bottoms: 3 × 5 = ", 15,
       "Multiply the two denominators."),
   box("That gives 30/15. Divide: 30 ÷ 15 = ", 2,
       "Top divided by bottom.", done="So 3 1/3 ÷ 1 2/3 = 2."),
   box("Check: multiply back. 2 × 5/3, tops: 2 × 5 = ", 10,
       "If it rebuilds 10/3, the answer is right.", done="10/3 = 3 1/3, so 2 is correct."),
 ]})

# G3: 2/3 + 5/6 - 1/4 = 5/4
gold.append({
 "display": "\\(\\frac{2}{3} + \\frac{5}{6} - \\frac{1}{4}\\)",
 "solutions": [5, 4], "calculator": False, "input_type": "fraction",
 "hint": "Find the common denominator of all three (3, 6 and 4).",
 "misconceptions": [
   mis("wrong_lcd", None,
       "The LCD of 3, 6 and 4 is 12. Convert: 8/12 + 10/12 " + MINUS + " 3/12 = 15/12 = 5/4 = 1 1/4.",
       "A wrong LCD gives unpredictable results; no single determinate answer."),
   mis("partial", [3, 2],
       "Add the first two, then subtract the third. All three need the same denominator.",
       "Student handles only the first two and ignores the subtraction: 2/3 + 5/6 = 9/6 = 3/2."),
 ],
 "guided_steps": [
   box("The common denominator of 3, 6 and 4 is ", 12,
       "The smallest number all three divide into."),
   box("Convert 2/3 into twelfths: 3 goes into 12 four times, so 2 × 4 = ", 8,
       "Multiply the top of 2/3 by 4."),
   box("Convert 5/6 into twelfths: 6 goes into 12 twice, so 5 × 2 = ", 10,
       "Multiply the top of 5/6 by 2."),
   box("Convert 1/4 into twelfths: 4 goes into 12 three times, so 1 × 3 = ", 3,
       "Multiply the top of 1/4 by 3."),
   box("Combine the tops in order: 8 + 10 " + MINUS + " 3 = ", 15,
       "Add the first two, then subtract the third.", phase="substitute"),
   box("That gives 15/12. Simplify by dividing top and bottom by 3. Top: 15 ÷ 3 = ", 5,
       "15 divided by 3."),
   box("Bottom: 12 ÷ 3 = ", 4,
       "12 divided by 3.", done="So 2/3 + 5/6 " + MINUS + " 1/4 = 5/4 = 1 1/4."),
   box("Check: turn 5/4 back up by 3. 5 × 3 = ", 15,
       "If it gives 15/12, the answer matches.", done="15/12 matches, so 5/4 is correct."),
 ]})

# G4: 3/8 / 3/4 + 1/2 = 1  (single_value) -- removed mislabelled left_to_right
gold.append({
 "display": "\\(\\frac{3}{8} \\div \\frac{3}{4} + \\frac{1}{2}\\)",
 "solutions": [1], "calculator": False, "input_type": "single_value",
 "hint": "BIDMAS: do the division before the addition.",
 "misconceptions": [
   mis("add_first", None,
       "Don't add 3/4 and 1/2 first. The division only links 3/8 and 3/4. Work out 3/8 ÷ 3/4, which is 1/2, then add 1/2 to get 1.",
       "Grouping wrongly as 3/8 ÷ (3/4 + 1/2) gives 3/8 ÷ 5/4 = 3/10, not a whole number."),
 ],
 "guided_steps": [
   sy("BIDMAS: do the division before the addition. Work out 3/8 ÷ 3/4 first."),
   box("Flip the second fraction. The reciprocal of 3/4 is 4 over 3, so its new top is ", 4,
       "Swap the top and bottom of 3/4."),
   box("Multiply the tops: 3 × 4 = ", 12,
       "Multiply 3/8 by 4/3, tops first."),
   box("Multiply the bottoms: 8 × 3 = ", 24,
       "Multiply the denominators."),
   box("Simplify 12/24 to a half. Its top is ", 1,
       "12 ÷ 12 = 1 and 24 ÷ 12 = 2, giving 1/2."),
   box("Now add 1/2 + 1/2. Add the tops: 1 + 1 = ", 2,
       "Two halves, add the numerators over 2.", phase="substitute"),
   box("That gives 2/2, which equals ", 1,
       "Anything over itself is one whole.", done="So 3/8 ÷ 3/4 + 1/2 = 1."),
   box("Check: 3/8 ÷ 3/4 = 0.5 and 0.5 + 0.5 = ", 1,
       "Two halves make a whole.", done="It equals 1, so the answer is right."),
 ]})

# ---------------------------------------------------------------- tier_guides
tier_guides = {
 "bronze": {
   "title": "Bronze: adding, subtracting and multiplying simple fractions",
   "steps": [
     "For <strong>+</strong> or <strong>−</strong>: give both fractions the same denominator, then combine the tops only.",
     "For <strong>×</strong>: no common denominator is needed. Multiply the tops together and the bottoms together.",
     "Always simplify the final fraction by dividing top and bottom by their highest common factor.",
   ],
   "example": {
     "question": "Calculate \\(\\frac{1}{6} + \\frac{1}{2}\\)",
     "steps": [
       {"label": "Common denominator", "content": "The LCD of 6 and 2 is 6, so 1/2 = 3/6."},
       {"label": "Add the tops", "content": "1/6 + 3/6 = 4/6."},
       {"label": "Simplify", "content": "Divide top and bottom by 2: 4/6 = 2/3."},
       {"label": "Check", "content": "2/3 turned back into sixths is 4/6, matching the sum."},
       {"label": "Answer", "content": "\\(\\frac{2}{3}\\)", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "silver": {
   "title": "Silver: dividing fractions and using mixed numbers",
   "steps": [
     "To divide, use <strong>keep, flip, multiply</strong>: keep the first fraction, flip the second, then multiply across.",
     "Turn any mixed number into an improper fraction before you calculate.",
     "Multiply or add as usual, then simplify the answer.",
   ],
   "example": {
     "question": "Calculate \\(\\frac{4}{5} \\div \\frac{2}{3}\\)",
     "steps": [
       {"label": "Keep, flip, multiply", "content": "4/5 ÷ 2/3 = 4/5 × 3/2."},
       {"label": "Multiply across", "content": "4 × 3 = 12 and 5 × 2 = 10, giving 12/10."},
       {"label": "Simplify", "content": "Divide top and bottom by 2: 12/10 = 6/5."},
       {"label": "Check", "content": "6/5 × 2/3 = 12/15 = 4/5, rebuilding the first fraction."},
       {"label": "Answer", "content": "\\(\\frac{6}{5}\\)", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "gold": {
   "title": "Gold: mixed numbers, three fractions and BIDMAS",
   "steps": [
     "Convert every mixed number to an improper fraction before you start.",
     "For a chain of fractions, give them all one common denominator, then combine the tops in order.",
     "With mixed operations, follow <strong>BIDMAS</strong>: do division and multiplication before addition and subtraction. Simplify at the end.",
   ],
   "example": {
     "question": "Calculate \\(1\\frac{1}{2} \\times \\frac{2}{3}\\)",
     "steps": [
       {"label": "Convert", "content": "1 1/2 = 3/2, so the sum is 3/2 × 2/3."},
       {"label": "Multiply across", "content": "3 × 2 = 6 and 2 × 3 = 6, giving 6/6."},
       {"label": "Simplify", "content": "6/6 = 1."},
       {"label": "Check", "content": "A number times a fraction just under a half of 3 lands on 1; 3/2 × 2/3 cancels to 1."},
       {"label": "Answer", "content": "\\(1\\)", "isAnswer": True, "is_answer": True},
     ],
   },
 },
}

# ---------------------------------------------------------------- guided (opener + teach)
guided = {
 "opener": {
   "steps": [
     sy("Forget the maths for a second. Picture a pizza cut into quarter-slices."),
     box("You eat one half of the pizza. How many quarter-slices is that? ", 2,
         "A half of the pizza is the same as two of the quarter-slices."),
     sy("Your friend then eats one more quarter-slice."),
     box("Altogether, how many quarter-slices have gone? ", 3,
         "Your 2 quarters plus your friend's 1 quarter."),
     sy("You just worked out \\(\\frac{1}{2} + \\frac{1}{4} = \\frac{3}{4}\\) without any rules. The trick was turning the half into quarters so both pieces were the same size. That is exactly what <strong>find a common denominator</strong> means: make the slices match, then count them."),
   ],
 },
 "teach": {
   "bronze": {
     "display": "Calculate \\(\\frac{1}{4} + \\frac{1}{12}\\)",
     "steps": [
       box("The common denominator of 4 and 12 is ", 12,
           "12 is already in the 4 times table."),
       box("Convert 1/4 into twelfths: 4 goes into 12 three times, so 1 × 3 = ", 3,
           "Multiply the top of 1/4 by 3."),
       sy("The second fraction, 1/12, is already in twelfths."),
       box("Add the tops: 3 + 1 = ", 4,
           "Add the numerators, keep the denominator 12."),
       box("That gives 4/12. Simplify by dividing top and bottom by 4. Top: 4 ÷ 4 = ", 1,
           "4 divided by 4."),
       box("Bottom: 12 ÷ 4 = ", 3,
           "12 divided by 4.",
           done="So 1/4 + 1/12 = 1/3. That is the whole bronze move: match the denominators, add, then simplify."),
     ],
   },
   "silver": {
     "display": "Calculate \\(\\frac{2}{3} \\div \\frac{4}{9}\\)",
     "steps": [
       box("To divide, flip the second fraction. The reciprocal of 4/9 is 9 over 4, so its new top is ", 9,
           "Swap the top and bottom of 4/9."),
       sy("Now the sum is 2/3 × 9/4."),
       box("Multiply the tops: 2 × 9 = ", 18,
           "Multiply the two numerators."),
       box("Multiply the bottoms: 3 × 4 = ", 12,
           "Multiply the two denominators."),
       box("That gives 18/12. Simplify by dividing top and bottom by 6. Top: 18 ÷ 6 = ", 3,
           "18 divided by 6."),
       box("Bottom: 12 ÷ 6 = ", 2,
           "12 divided by 6.",
           done="So 2/3 ÷ 4/9 = 3/2. Keep, flip, multiply: that is the whole silver move."),
     ],
   },
   "gold": {
     "display": "Calculate \\(2\\frac{1}{4} \\times 1\\frac{1}{3}\\)",
     "steps": [
       box("Convert 2 1/4 to an improper fraction. Top: 2 × 4 + 1 = ", 9,
           "Whole times denominator, plus the top."),
       box("Convert 1 1/3 to an improper fraction. Top: 1 × 3 + 1 = ", 4,
           "Whole times denominator, plus the top."),
       box("Multiply the tops: 9 × 4 = ", 36,
           "Multiply the two numerators."),
       box("Multiply the bottoms: 4 × 3 = ", 12,
           "Multiply the two denominators."),
       box("That gives 36/12. Divide: 36 ÷ 12 = ", 3,
           "Top divided by bottom.",
           done="So 2 1/4 × 1 1/3 = 3. Turning mixed numbers into improper fractions first is the whole gold move."),
     ],
   },
 },
}

# ---------------------------------------------------------------- method_card (slim)
method_card = {
 "title": "How to Add, Subtract, Multiply and Divide Fractions",
 "steps": [
   "Convert any mixed numbers to improper fractions first.",
   "To add or subtract: find a common denominator, then combine the tops only.",
   "To multiply: multiply tops and bottoms. To divide: keep, flip, multiply.",
   "Always simplify the final fraction by its highest common factor.",
 ],
 "content": "<p><strong>Adding and subtracting</strong> needs a common denominator: convert both fractions so the bottoms match, then combine the tops only.</p><p><strong>Multiplying</strong> needs no common denominator: multiply the numerators together and the denominators together. Cross-cancel first to keep numbers small.</p><p><strong>Dividing</strong> uses keep, flip, multiply: keep the first fraction, flip the second, then multiply.</p><p><strong>Mixed numbers</strong> must become improper fractions before you calculate. Simplify every answer at the end.</p>",
 "example": "<p><strong>Calculate</strong> \\(\\frac{2}{3} + \\frac{3}{4}\\)</p><p>LCD of 3 and 4 is 12: \\(\\frac{8}{12} + \\frac{9}{12} = \\frac{17}{12} = 1\\frac{5}{12}\\).</p>",
}

# ---------------------------------------------------------------- assemble
live = json.load(io.open("_live_number_L02.json", encoding="utf-8"))

out = {}
out["method_card"] = method_card
out["topic_links"] = live["topic_links"]          # preserved
out["problem_bank"] = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": "Add, subtract or multiply two simple fractions, then simplify the answer.",
  "silver_description": "Divide fractions with keep, flip, multiply, and handle a mixed number or an unlike denominator.",
  "gold_description": "Combine mixed numbers, three fractions or a BIDMAS chain, converting and simplifying throughout.",
}
out["tier_guides"] = tier_guides
out["guided"] = guided
out["related_videos"] = live["related_videos"]    # preserved byte-for-byte
# worked_examples preserved, except em dashes in step labels violate the hard
# style rule (dash reads as minus in maths); replace " — " with ": ".
we = live["worked_examples"]
for ex in we:
    for st in ex.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")
out["worked_examples"] = we

json.dump(out, io.open("lesson_number-L02.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written lesson_number-L02.json")

# ---------------------------------------------------------------- self-check
from fractions import Fraction as F
def last_two_answers(steps):
    ans = [s["answer"] for s in steps if s.get("answer") is not None]
    return ans
prob = {"bronze": bronze, "silver": silver, "gold": gold}
problems_all = [(t, i, p) for t in ("bronze","silver","gold") for i, p in enumerate(prob[t])]
for t, i, p in problems_all:
    sols = p["solutions"]
    ans = last_two_answers(p["guided_steps"])
    # final answer boxes: for fraction -> the numerator/denominator boxes; check the walk lands on solutions
    if p["input_type"] == "fraction":
        # the simplified numerator & denominator should both appear as box values
        need = set(sols)
        assert need.issubset(set(ans)), "%s[%d] solutions %s not all in boxes %s" % (t,i,sols,ans)
    else:
        assert sols[0] in ans, "%s[%d] single_value %s not in boxes %s" % (t,i,sols,ans)
    # boundary + >=2 live after
    idx = [k for k,s in enumerate(p["guided_steps"]) if s.get("phase")=="substitute"]
    assert idx and idx[0] >= 1, "%s[%d] bad boundary" % (t,i)
    live_after = sum(1 for s in p["guided_steps"][idx[0]:] if s.get("answer") is not None)
    assert live_after >= 2, "%s[%d] only %d live after boundary" % (t,i,live_after)
    # expects != correct
    for m in p["misconceptions"]:
        e = m["expect"]
        if e is not None:
            assert list(e) != list(sols), "%s[%d] expect==sol" % (t,i)
# duplicate solutions within tier
for t in ("bronze","silver","gold"):
    seen=[]
    for p in prob[t]:
        key=tuple(p["solutions"])
        assert key not in seen, "dup %s in %s" % (key,t)
        seen.append(key)
print("self-check OK: all walks land on solutions, boundaries valid, no dup solutions, expects clean")
