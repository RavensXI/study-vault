# -*- coding: utf-8 -*-
"""Full guided conversion of maths-ocr algebra-L05 (Solving Linear Equations)."""
import json, copy

SRC = "_live_ocr_algL05.json"
OUT = "../_maths_guided/lesson_algebra-L05.json"

live = json.load(open(SRC, encoding="utf-8"))
out = copy.deepcopy(live)  # preserves method_card, topic_links, related_videos, worked_examples

# Style-law repair: preserved worked_examples labels contain em dashes ("Step 1 — ..").
# Replace with a colon (no em dashes allowed student-facing).
def desmash(obj):
    if isinstance(obj, dict):
        return {k: desmash(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [desmash(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace(" — ", ": ").replace("—", ": ")
    return obj
if "worked_examples" in out:
    out["worked_examples"] = desmash(out["worked_examples"])

M = "−"   # unicode minus for student-facing maths text
X = "×"   # times
D = "÷"   # divide

# ---------- helpers ----------
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

# =====================================================================
# PROBLEM BANK
# =====================================================================
bronze = []
silver = []
gold = []

# ---- BRONZE ----
# [0] 2x+3=11 -> 4
bronze.append({
 "display": "Solve \\(2x + 3 = 11\\)", "solutions": [4],
 "input_type": "single_value", "calculator": False,
 "hint": "Undo the +3 first, then divide by the 2 in front of x.",
 "misconceptions": [
   {"pattern": "forgot_divide", "expect": 8,
    "message": "Subtracting the 3 gives \\(2x = 8\\). That is not the answer yet: \\(x\\) is multiplied by 2, so divide by 2. \\(x = 8 " + D + " 2 = 4\\).",
    "note": "stops at 2x=8, forgets to divide"},
   {"pattern": "added_constant", "expect": 7,
    "message": "The +3 must be taken OFF both sides, not added on. \\(2x = 11 " + M + " 3 = 8\\), so \\(x = 4\\). Adding it gives \\(2x = 14\\) and \\(x = 7\\).",
    "note": "2x=11+3=14, x=7"}],
 "guided_steps": [
   sayonly("Two things have happened to \\(x\\): multiplied by 2, then 3 added. Undo them in reverse, so take off the 3 first."),
   box("Take off the 3: 11 " + M + " 3 = ", 8, "Subtract 3 from both sides. This leaves 2x."),
   box("Now divide by the 2 in front of x: 8 " + D + " 2 = ", 4, "Divide both sides by 2.", phase="substitute"),
   box("Check: 2 " + X + " 4 + 3 = ", 11, "Put x = 4 back in.", done="It gives 11, the right-hand side, so x = 4 is right.")]
})
# [1] 3x-5=10 -> 5
bronze.append({
 "display": "Solve \\(3x - 5 = 10\\)", "solutions": [5],
 "input_type": "single_value", "calculator": False,
 "hint": "Add 5 to both sides, then divide by 3.",
 "misconceptions": [
   {"pattern": "forgot_divide", "expect": 15,
    "message": "Adding 5 gives \\(3x = 15\\). Now divide by 3 to finish: \\(x = 5\\). Stopping at 15 skips the last step.",
    "note": "3x=15, forgets divide"}],
 "guided_steps": [
   sayonly("The 5 is subtracted, so undo it by adding 5 to both sides first."),
   box("Add 5: 10 + 5 = ", 15, "Add 5 to both sides. This leaves 3x."),
   box("Now divide by 3: 15 " + D + " 3 = ", 5, "Divide both sides by 3.", phase="substitute"),
   box("Check: 3 " + X + " 5 " + M + " 5 = ", 10, "Put x = 5 back in.", done="It gives 10, so x = 5 is right.")]
})
# [2] x/4=3 -> 12
bronze.append({
 "display": "Solve \\(\\frac{x}{4} = 3\\)", "solutions": [12],
 "input_type": "single_value", "calculator": False,
 "hint": "x is divided by 4, so multiply both sides by 4.",
 "misconceptions": [
   {"pattern": "divide_instead", "expect": 0.75,
    "message": "Here \\(x\\) is divided by 4, so undo it by multiplying: \\(x = 3 " + X + " 4 = 12\\). Dividing 3 by 4 goes the wrong way and gives 0.75.",
    "note": "3/4=0.75"}],
 "guided_steps": [
   sayonly("\\(x\\) has been divided by 4. To undo a division, multiply both sides by 4."),
   box("The number under x is ", 4, "It is the 4 that x is divided by."),
   box("Multiply both sides by 4: 3 " + X + " 4 = ", 12, "3 times 4.", phase="substitute"),
   box("Check: 12 " + D + " 4 = ", 3, "Put x = 12 back in.", done="It gives 3, so x = 12 is right.")]
})
# [3] 5x=35 -> 7
bronze.append({
 "display": "Solve \\(5x = 35\\)", "solutions": [7],
 "input_type": "single_value", "calculator": False,
 "hint": "Divide both sides by 5, do not subtract.",
 "misconceptions": [
   {"pattern": "subtract_instead", "expect": 30,
    "message": "\\(5x\\) means 5 times \\(x\\), so undo it by dividing, not subtracting: \\(x = 35 " + D + " 5 = 7\\). Subtracting 5 gives 30, which is wrong.",
    "note": "35-5=30"}],
 "guided_steps": [
   sayonly("\\(5x\\) means 5 times \\(x\\). Undo the multiply by dividing both sides by 5."),
   box("The number in front of x is ", 5, "It is the 5 multiplying x."),
   box("Divide both sides by 5: 35 " + D + " 5 = ", 7, "35 divided by 5.", phase="substitute"),
   box("Check: 5 " + X + " 7 = ", 35, "Put x = 7 back in.", done="It gives 35, so x = 7 is right.")]
})
# [4] 4x+1=33 -> 8  (CHANGED from 4x+1=17 which duplicated bronze[0] answer 4)
bronze.append({
 "display": "Solve \\(4x + 1 = 33\\)", "solutions": [8],
 "input_type": "single_value", "calculator": False,
 "hint": "Take off the 1, then divide by 4.",
 "misconceptions": [
   {"pattern": "forgot_divide", "expect": 32,
    "message": "Taking off the 1 gives \\(4x = 32\\). You still need to divide by 4: \\(x = 8\\). Stopping at 32 forgets the last step.",
    "note": "4x=32, forgets divide"}],
 "guided_steps": [
   sayonly("Undo the +1 first, then the multiply by 4."),
   box("Take off the 1: 33 " + M + " 1 = ", 32, "Subtract 1 from both sides. This leaves 4x."),
   box("Now divide by 4: 32 " + D + " 4 = ", 8, "Divide both sides by 4.", phase="substitute"),
   box("Check: 4 " + X + " 8 + 1 = ", 33, "Put x = 8 back in.", done="It gives 33, so x = 8 is right.")]
})
# [5] 7x-2=19 -> 3
bronze.append({
 "display": "Solve \\(7x - 2 = 19\\)", "solutions": [3],
 "input_type": "single_value", "calculator": False,
 "hint": "Add 2 to both sides, then divide by 7.",
 "misconceptions": [
   {"pattern": "forgot_divide", "expect": 21,
    "message": "Adding 2 gives \\(7x = 21\\). Now divide by 7 to finish: \\(x = 3\\). Leaving it at 21 skips the last step.",
    "note": "7x=21, forgets divide"}],
 "guided_steps": [
   sayonly("The 2 is subtracted, so add 2 to both sides first."),
   box("Add 2: 19 + 2 = ", 21, "Add 2 to both sides. This leaves 7x."),
   box("Now divide by 7: 21 " + D + " 7 = ", 3, "Divide both sides by 7.", phase="substitute"),
   box("Check: 7 " + X + " 3 " + M + " 2 = ", 19, "Put x = 3 back in.", done="It gives 19, so x = 3 is right.")]
})
# [6] x/3+2=5 -> 9
bronze.append({
 "display": "Solve \\(\\frac{x}{3} + 2 = 5\\)", "solutions": [9],
 "input_type": "single_value", "calculator": False,
 "hint": "Take off the 2 first, then multiply both sides by 3.",
 "misconceptions": [
   {"pattern": "wrong_sign_on_constant", "expect": 21,
    "message": "The +2 comes off first: \\(\\frac{x}{3} = 5 " + M + " 2 = 3\\), then \\(x = 9\\). Adding the 2 instead gives \\(\\frac{x}{3} = 7\\) and \\(x = 21\\), which is too big.",
    "note": "x/3=5+2=7, x=21"},
   {"pattern": "forgot_multiply", "expect": 3,
    "message": "After \\(\\frac{x}{3} = 3\\), multiply by 3 to get \\(x = 9\\). Leaving the answer as 3 forgets to undo the division.",
    "note": "stops at x/3=3, says x=3"}],
 "guided_steps": [
   sayonly("\\(x\\) is divided by 3, then 2 is added. Undo the +2 first."),
   box("Take off the 2: 5 " + M + " 2 = ", 3, "Subtract 2 from both sides. This leaves x/3."),
   box("Now x is divided by 3, so multiply: 3 " + X + " 3 = ", 9, "Multiply both sides by 3.", phase="substitute"),
   box("Check: 9 " + D + " 3 + 2 = ", 5, "Put x = 9 back in.", done="It gives 5, so x = 9 is right.")]
})
# [7] 20-3x=2 -> 6  (CHANGED from 20-3x=5 which duplicated bronze[1] answer 5)
bronze.append({
 "display": "Solve \\(20 - 3x = 2\\)", "solutions": [6],
 "input_type": "single_value", "calculator": False,
 "hint": "Add 3x to both sides so the x term is positive, then solve.",
 "misconceptions": [
   {"pattern": "sign_error", "expect": -6,
    "message": "Watch the sign. \\(20 " + M + " 3x = 2\\) rearranges to \\(3x = 20 " + M + " 2 = 18\\), so \\(x = 6\\). Dropping the sign and writing \\(3x = 2 " + M + " 20 = " + M + "18\\) gives \\(x = " + M + "6\\).",
    "note": "3x=2-20=-18, x=-6"}],
 "guided_steps": [
   sayonly("The \\(x\\) term is negative. Add \\(3x\\) to both sides and move the 2 across so everything stays positive."),
   box("20 " + M + " 2 = ", 18, "This equals 3x."),
   box("So 3x = 18. Divide by 3: 18 " + D + " 3 = ", 6, "Divide both sides by 3.", phase="substitute"),
   box("Check: 20 " + M + " 3 " + X + " 6 = ", 2, "Put x = 6 back in.", done="It gives 2, so x = 6 is right.")]
})

# ---- SILVER ----
# [0] 5x+2=3x+10 -> 4
silver.append({
 "display": "Solve \\(5x + 2 = 3x + 10\\)", "solutions": [4],
 "input_type": "single_value", "calculator": False,
 "hint": "Take 3x off both sides, then take the 2 across.",
 "misconceptions": [
   {"pattern": "added_x_terms", "expect": 1,
    "message": "Move the \\(3x\\) by subtracting it: \\(5x " + M + " 3x = 2x\\). Adding it gives \\(8x = 8\\) and \\(x = 1\\), which does not fit.",
    "note": "5x+3x=10-2 -> 8x=8, x=1"},
   {"pattern": "wrong_sign_on_constant", "expect": 6,
    "message": "The +2 crosses the equals sign as \\(" + M + "2\\): \\(2x = 10 " + M + " 2 = 8\\), so \\(x = 4\\). Keeping it as +2 gives \\(2x = 12\\) and \\(x = 6\\).",
    "note": "2x=10+2=12, x=6"}],
 "guided_steps": [
   sayonly("Unknowns on both sides. Collect the \\(x\\) terms on the left and the numbers on the right."),
   box("Take 3x off both sides: 5x " + M + " 3x = ", 2, "5 minus 3.", post="x"),
   box("Take 2 off both sides: 10 " + M + " 2 = ", 8, "Move the +2 across as minus 2. This gives 2x = 8."),
   sayonly("So \\(2x = 8\\)."),
   box("Divide by 2: 8 " + D + " 2 = ", 4, "Divide both sides by 2.", phase="substitute"),
   box("Check the left side: 5 " + X + " 4 + 2 = ", 22, "Work out 5 times 4, add 2.", done="Right side 3 " + X + " 4 + 10 also = 22, so x = 4 is right.")]
})
# [1] 7x-3=4x+12 -> 5
silver.append({
 "display": "Solve \\(7x - 3 = 4x + 12\\)", "solutions": [5],
 "input_type": "single_value", "calculator": False,
 "hint": "Collect x on the left: 7x minus 4x, and move the numbers across.",
 "misconceptions": [
   {"pattern": "wrong_sign_on_constant", "expect": 3,
    "message": "The \\(" + M + "3\\) moves across as \\(+3\\): \\(3x = 12 + 3 = 15\\), so \\(x = 5\\). Subtracting it gives \\(3x = 9\\) and \\(x = 3\\).",
    "note": "3x=12-3=9, x=3"}],
 "guided_steps": [
   sayonly("Collect the \\(x\\) terms on the left and the numbers on the right."),
   box("Take 4x off both sides: 7x " + M + " 4x = ", 3, "7 minus 4.", post="x"),
   box("The " + M + "3 moves across as +3: 12 + 3 = ", 15, "Add 3 to the 12. This gives 3x = 15."),
   sayonly("So \\(3x = 15\\)."),
   box("Divide by 3: 15 " + D + " 3 = ", 5, "Divide both sides by 3.", phase="substitute"),
   box("Check the left side: 7 " + X + " 5 " + M + " 3 = ", 32, "Work out 7 times 5, take off 3.", done="Right side 4 " + X + " 5 + 12 also = 32, so x = 5 is right.")]
})
# [2] 3(x+4)=30 -> 6  (CHANGED from =21 which gave answer 3, a triple-duplicate)
silver.append({
 "display": "Solve \\(3(x + 4) = 30\\)", "solutions": [6],
 "input_type": "single_value", "calculator": False,
 "hint": "Expand the bracket first, then take the 12 across.",
 "misconceptions": [
   {"pattern": "wrong_sign_on_constant", "expect": 14,
    "message": "Expanding gives \\(3x + 12 = 30\\). The 12 comes OFF: \\(3x = 30 " + M + " 12 = 18\\), so \\(x = 6\\). Adding it gives \\(3x = 42\\) and \\(x = 14\\).",
    "note": "3x=30+12=42, x=14"},
   {"pattern": "divided_one_side", "expect": 26,
    "message": "Dividing only the left by 3 leaves \\(x + 4 = 30\\) and \\(x = 26\\). Divide BOTH sides: \\(x + 4 = 10\\), so \\(x = 6\\).",
    "note": "x+4=30, x=26"}],
 "guided_steps": [
   sayonly("Expand the bracket first: 3 times each term inside."),
   box("Multiply the 4: 3 " + X + " 4 = ", 12, "3 times 4. So 3x + 12 = 30."),
   box("Take the 12 across: 30 " + M + " 12 = ", 18, "Subtract 12 from both sides. This gives 3x = 18."),
   sayonly("So \\(3x = 18\\)."),
   box("Divide by 3: 18 " + D + " 3 = ", 6, "Divide both sides by 3.", phase="substitute"),
   box("Check: 3 " + X + " (6 + 4) = ", 30, "Work out 6 + 4, then times 3.", done="It gives 30, so x = 6 is right.")]
})
# [3] 3(x-1)=x+15 -> 9  (CHANGED from 2(3x-1)=x+13 which gave 3, a triple-duplicate)
silver.append({
 "display": "Solve \\(3(x - 1) = x + 15\\)", "solutions": [9],
 "input_type": "single_value", "calculator": False,
 "hint": "Expand 3(x minus 1), then collect the x terms on one side.",
 "misconceptions": [
   {"pattern": "expand_sign_error", "expect": 6,
    "message": "\\(3(x " + M + " 1) = 3x " + M + " 3\\), not \\(3x + 3\\). With the correct sign, \\(2x = 18\\) and \\(x = 9\\). A sign slip gives \\(3x + 3 = x + 15\\), so \\(x = 6\\).",
    "note": "3x+3=x+15 -> 2x=12, x=6"},
   {"pattern": "forgot_multiply_constant", "expect": 8,
    "message": "Multiply the 1 by 3 as well: \\(3(x " + M + " 1) = 3x " + M + " 3\\). Writing \\(3x " + M + " 1\\) instead gives \\(2x = 16\\) and \\(x = 8\\). The correct answer is \\(x = 9\\).",
    "note": "3x-1=x+15 -> 2x=16, x=8"}],
 "guided_steps": [
   sayonly("Expand the bracket: multiply both terms inside by 3."),
   box("Multiply the " + M + "1: 3 " + X + " (" + M + "1) = ", -3, "3 times minus 1. So 3x " + M + " 3 = x + 15."),
   box("Collect x on the left: 3x " + M + " x = ", 2, "3 minus 1.", post="x"),
   box("Move the numbers across: 15 + 3 = ", 18, "The " + M + "3 crosses as +3. This gives 2x = 18."),
   sayonly("So \\(2x = 18\\)."),
   box("Divide by 2: 18 " + D + " 2 = ", 9, "Divide both sides by 2.", phase="substitute"),
   box("Check the left side: 3 " + X + " (9 " + M + " 1) = ", 24, "Work out 9 minus 1, then times 3.", done="Right side 9 + 15 also = 24, so x = 9 is right.")]
})
# [4] (x+5)/3=4 -> 7
silver.append({
 "display": "Solve \\(\\frac{x+5}{3} = 4\\)", "solutions": [7],
 "input_type": "single_value", "calculator": False,
 "hint": "Multiply both sides by 3 to clear the fraction, then take off 5.",
 "misconceptions": [
   {"pattern": "did_not_clear_fraction", "expect": -1,
    "message": "Multiply both sides by 3 first: \\(x + 5 = 12\\), so \\(x = 7\\). Solving \\(x + 5 = 4\\) forgets to clear the \\(" + D + "3\\) and gives \\(x = " + M + "1\\).",
    "note": "x+5=4, x=-1"},
   {"pattern": "wrong_sign_on_constant", "expect": 17,
    "message": "After clearing, \\(x + 5 = 12\\) means \\(x = 12 " + M + " 5 = 7\\). Adding the 5 gives \\(x = 17\\).",
    "note": "x=12+5=17"}],
 "guided_steps": [
   sayonly("The whole left side is divided by 3. Multiply both sides by 3 to clear it."),
   box("Multiply both sides by 3: 4 " + X + " 3 = ", 12, "4 times 3. So x + 5 = 12."),
   box("Take off 5: 12 " + M + " 5 = ", 7, "Subtract 5 from both sides.", phase="substitute"),
   box("Check: (7 + 5) " + D + " 3 = ", 4, "Work out 7 + 5, then divide by 3.", done="It gives 4, so x = 7 is right.")]
})
# [5] 4(x-2)=3(x+1) -> 11
silver.append({
 "display": "Solve \\(4(x - 2) = 3(x + 1)\\)", "solutions": [11],
 "input_type": "single_value", "calculator": False,
 "hint": "Expand both brackets, then collect x on one side and numbers on the other.",
 "misconceptions": [
   {"pattern": "wrong_sign_on_constant", "expect": -5,
    "message": "Expanding gives \\(4x " + M + " 8 = 3x + 3\\), so \\(x = 3 + 8 = 11\\). Subtracting the 8 instead of adding it across gives \\(x = 3 " + M + " 8 = " + M + "5\\).",
    "note": "x=3-8=-5"},
   {"pattern": "forgot_multiply_constant", "expect": 9,
    "message": "\\(3(x + 1) = 3x + 3\\), not \\(3x + 1\\). With the correct expansion \\(x = 11\\). Writing \\(3x + 1\\) gives \\(4x " + M + " 8 = 3x + 1\\) and \\(x = 9\\).",
    "note": "4x-8=3x+1 -> x=9"}],
 "guided_steps": [
   sayonly("Expand both brackets first."),
   box("Left: 4 " + X + " (" + M + "2) = ", -8, "4 times minus 2. So the left is 4x " + M + " 8."),
   box("Right: 3 " + X + " 1 = ", 3, "3 times 1. So the right is 3x + 3. Now 4x " + M + " 8 = 3x + 3."),
   box("Collect x: 4x " + M + " 3x = ", 1, "4 minus 3.", post="x"),
   sayonly("So \\(x " + M + " 8 = 3\\)."),
   box("Add 8: 3 + 8 = ", 11, "Add 8 to both sides.", phase="substitute"),
   box("Check the left side: 4 " + X + " (11 " + M + " 2) = ", 36, "Work out 11 minus 2, then times 4.", done="Right side 3 " + X + " (11 + 1) also = 36, so x = 11 is right.")]
})
# [6] 8-2x=3x-7 -> 3
silver.append({
 "display": "Solve \\(8 - 2x = 3x - 7\\)", "solutions": [3],
 "input_type": "single_value", "calculator": False,
 "hint": "Add 2x to both sides, then add 7, then divide by 5.",
 "misconceptions": [
   {"pattern": "sign_error", "expect": -3,
    "message": "Collecting gives \\(8 + 7 = 3x + 2x\\), so \\(15 = 5x\\) and \\(x = 3\\). A dropped sign turns it into \\(5x = " + M + "7 " + M + " 8 = " + M + "15\\) and \\(x = " + M + "3\\).",
    "note": "5x=-15, x=-3"}],
 "guided_steps": [
   sayonly("The \\(x\\) terms are on opposite sides. Add \\(2x\\) to both sides so they combine and stay positive."),
   box("Collect the x terms: 3x + 2x = ", 5, "3 plus 2. This gives 8 = 5x " + M + " 7.", post="x"),
   box("Add 7 to both sides: 8 + 7 = ", 15, "Add 7. This gives 15 = 5x."),
   sayonly("So \\(5x = 15\\)."),
   box("Divide by 5: 15 " + D + " 5 = ", 3, "Divide both sides by 5.", phase="substitute"),
   box("Check: 8 " + M + " 2 " + X + " 3 = ", 2, "Work out 8 minus (2 times 3).", done="Right side 3 " + X + " 3 " + M + " 7 also = 2, so x = 3 is right.")]
})

# ---- GOLD ----
# [0] (2x+1)/3=(x+4)/2 -> 10
gold.append({
 "display": "Solve \\(\\frac{2x+1}{3} = \\frac{x+4}{2}\\)", "solutions": [10],
 "input_type": "single_value", "calculator": False,
 "hint": "Cross-multiply to clear the fractions, then collect like terms.",
 "misconceptions": [
   {"pattern": "did_not_cross_multiply", "expect": 3,
    "message": "Clear the fractions first: \\(2(2x+1) = 3(x+4)\\). Ignoring the denominators and solving \\(2x + 1 = x + 4\\) gives \\(x = 3\\), which is wrong.",
    "note": "2x+1=x+4 -> x=3"},
   {"pattern": "wrong_sign_on_constant", "expect": 14,
    "message": "After cross-multiplying, \\(4x + 2 = 3x + 12\\), so \\(x = 12 " + M + " 2 = 10\\). Adding the 2 across instead gives \\(x = 12 + 2 = 14\\).",
    "note": "x=12+2=14"}],
 "guided_steps": [
   sayonly("Cross-multiply to clear the fractions: \\(2(2x+1) = 3(x+4)\\)."),
   box("Expand the left: 2 " + X + " 2x = ", 4, "2 times 2x. So the left is 4x + 2.", post="x"),
   box("Expand the right: 3 " + X + " 4 = ", 12, "3 times 4. So the right is 3x + 12. Now 4x + 2 = 3x + 12."),
   box("Collect x: 4x " + M + " 3x = ", 1, "4 minus 3.", post="x"),
   sayonly("So \\(x + 2 = 12\\)."),
   box("Take off 2: 12 " + M + " 2 = ", 10, "Subtract 2 from both sides.", phase="substitute"),
   box("Check the left side: (2 " + X + " 10 + 1) " + D + " 3 = ", 7, "Work out 2 times 10 plus 1, then divide by 3.", done="Right side (10 + 4) " + D + " 2 also = 7, so x = 10 is right.")]
})
# [1] 3(2x+1)=5(x+2) -> 7
gold.append({
 "display": "Solve \\(3(2x + 1) = 5(x + 2)\\)", "solutions": [7],
 "input_type": "single_value", "calculator": False,
 "hint": "Expand both brackets, then collect x on one side.",
 "misconceptions": [
   {"pattern": "forgot_multiply_constant", "expect": 1,
    "message": "Multiply the constants too: \\(3(2x+1) = 6x + 3\\) and \\(5(x+2) = 5x + 10\\), giving \\(x = 7\\). Writing \\(6x + 1 = 5x + 2\\) gives \\(x = 1\\).",
    "note": "6x+1=5x+2 -> x=1"},
   {"pattern": "wrong_sign_on_constant", "expect": 13,
    "message": "From \\(6x + 3 = 5x + 10\\), \\(x = 10 " + M + " 3 = 7\\). Adding the 3 across instead gives \\(x = 10 + 3 = 13\\).",
    "note": "x=10+3=13"}],
 "guided_steps": [
   sayonly("Expand both brackets first."),
   box("Left: 3 " + X + " 2x = ", 6, "3 times 2x, and 3 times 1 is 3. So the left is 6x + 3.", post="x"),
   box("Right: 5 " + X + " 2 = ", 10, "5 times 2. So the right is 5x + 10. Now 6x + 3 = 5x + 10."),
   box("Collect x: 6x " + M + " 5x = ", 1, "6 minus 5.", post="x"),
   sayonly("So \\(x + 3 = 10\\)."),
   box("Take off 3: 10 " + M + " 3 = ", 7, "Subtract 3 from both sides.", phase="substitute"),
   box("Check the left side: 3 " + X + " (2 " + X + " 7 + 1) = ", 45, "Work out 2 times 7 plus 1, then times 3.", done="Right side 5 " + X + " (7 + 2) also = 45, so x = 7 is right.")]
})
# [2] x/2 + x/3 = 10 -> 12
gold.append({
 "display": "Solve \\(\\frac{x}{2} + \\frac{x}{3} = 10\\)", "solutions": [12],
 "input_type": "single_value", "calculator": False,
 "hint": "Multiply every term by 6 to clear both fractions.",
 "misconceptions": [
   {"pattern": "added_denominators", "expect": 50,
    "message": "You cannot add \\(\\frac{x}{2} + \\frac{x}{3}\\) as \\(\\frac{x}{5}\\). Using the LCD 6 gives \\(3x + 2x = 60\\), so \\(5x = 60\\) and \\(x = 12\\). The \\(\\frac{x}{5} = 10\\) route wrongly gives 50.",
    "note": "x/5=10, x=50"},
   {"pattern": "forgot_scale_rhs", "expect": 2,
    "message": "Multiply EVERY term by 6, including the 10: \\(3x + 2x = 60\\). Leaving the right side as 10 gives \\(5x = 10\\) and \\(x = 2\\).",
    "note": "5x=10, x=2"}],
 "guided_steps": [
   sayonly("The denominators are 2 and 3, so the lowest common denominator is 6. Multiply every term by 6."),
   box("First term: 6 " + X + " x/2 = ", 3, "6 divided by 2 is 3, so this becomes 3x.", post="x"),
   box("Second term: 6 " + X + " x/3 = ", 2, "6 divided by 3 is 2, so this becomes 2x.", post="x"),
   box("Right side: 6 " + X + " 10 = ", 60, "Do not forget to scale the 10. Now 3x + 2x = 60, i.e. 5x = 60."),
   box("Divide by 5: 60 " + D + " 5 = ", 12, "Divide both sides by 5.", phase="substitute"),
   box("Check: 12 " + D + " 2 + 12 " + D + " 3 = ", 10, "Work out 6 + 4.", done="It gives 10, so x = 12 is right.")]
})
# [3] 3(x-1)/4 = (2x+5)/3 -> 29
gold.append({
 "display": "Solve \\(\\frac{3(x-1)}{4} = \\frac{2x+5}{3}\\)", "solutions": [29],
 "input_type": "single_value", "calculator": False,
 "hint": "Cross-multiply, then expand and collect the x terms.",
 "misconceptions": [
   {"pattern": "wrong_sign_on_constant", "expect": 11,
    "message": "Cross-multiplying gives \\(9x " + M + " 9 = 8x + 20\\), so \\(x = 20 + 9 = 29\\). Subtracting the 9 instead of adding it across gives \\(x = 20 " + M + " 9 = 11\\).",
    "note": "x=20-9=11"},
   {"pattern": "did_not_cross_multiply", "expect": 8,
    "message": "Clear the fractions first: \\(3 " + X + " 3(x-1) = 4(2x+5)\\). Dropping the denominators and solving \\(3(x-1) = 2x+5\\) gives \\(x = 8\\), which is wrong.",
    "note": "3x-3=2x+5 -> x=8"}],
 "guided_steps": [
   sayonly("Cross-multiply: \\(3 " + X + " 3(x-1) = 4(2x+5)\\)."),
   box("Left coefficient: 3 " + X + " 3 = ", 9, "So the left is 9(x " + M + " 1) = 9x " + M + " 9."),
   box("Right: 4 " + X + " 2x = ", 8, "4 times 2x, and 4 times 5 is 20. So the right is 8x + 20. Now 9x " + M + " 9 = 8x + 20.", post="x"),
   box("Collect x: 9x " + M + " 8x = ", 1, "9 minus 8.", post="x"),
   sayonly("So \\(x " + M + " 9 = 20\\)."),
   box("Add 9: 20 + 9 = ", 29, "Add 9 to both sides.", phase="substitute"),
   box("Check the left side: 3 " + X + " (29 " + M + " 1) " + D + " 4 = ", 21, "Work out 29 minus 1, times 3, divide by 4.", done="Right side (2 " + X + " 29 + 5) " + D + " 3 also = 21, so x = 29 is right.")]
})
# [4] (x+3)/4 + (x-1)/2 = 4 -> 5
gold.append({
 "display": "Solve \\(\\frac{x+3}{4} + \\frac{x-1}{2} = 4\\)", "solutions": [5],
 "input_type": "single_value", "calculator": False,
 "hint": "Multiply every term by 4, remembering the second fraction becomes 2(x minus 1).",
 "misconceptions": [
   {"pattern": "forgot_scale_second_fraction", "expect": 7,
    "message": "The second fraction has denominator 2, so \\(" + X + "4\\) makes it \\(2(x " + M + " 1)\\), not \\(x " + M + " 1\\). Correctly: \\(3x + 1 = 16\\), \\(x = 5\\). The slip gives \\(2x + 2 = 16\\) and \\(x = 7\\).",
    "note": "(x+3)+(x-1)=16 -> 2x+2=16, x=7"},
   {"pattern": "forgot_scale_rhs", "expect": 1,
    "message": "Multiply the 4 on the right by 4 as well: \\(3x + 1 = 16\\), so \\(x = 5\\). Leaving it as 4 gives \\(3x + 1 = 4\\) and \\(x = 1\\).",
    "note": "3x+1=4, x=1"}],
 "guided_steps": [
   sayonly("The denominators are 4 and 2, so the lowest common denominator is 4. Multiply every term by 4."),
   box("The second fraction: 4 " + X + " (x" + M + "1)/2 becomes __(x " + M + " 1)", 2, "4 divided by 2 is 2, so it becomes 2(x " + M + " 1). The first becomes (x + 3)."),
   box("Right side: 4 " + X + " 4 = ", 16, "Scale the 4 too. So (x + 3) + 2(x " + M + " 1) = 16."),
   box("Expand and collect x: x + 2x = ", 3, "One x from the first bracket, 2x from 2(x " + M + " 1). And 3 " + M + " 2 = 1, so 3x + 1 = 16.", post="x"),
   box("Take off 1: 16 " + M + " 1 = ", 15, "Subtract 1 from both sides. This gives 3x = 15."),
   sayonly("So \\(3x = 15\\)."),
   box("Divide by 3: 15 " + D + " 3 = ", 5, "Divide both sides by 3.", phase="substitute"),
   box("Check: (5+3)" + D + "4 + (5" + M + "1)" + D + "2 = ", 4, "Work out 8/4 + 4/2 = 2 + 2.", done="It gives 4, so x = 5 is right.")]
})

# =====================================================================
# assemble problem_bank
# =====================================================================
out["problem_bank"] = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description": "One-step and two-step equations: undo the operations on x in reverse order.",
 "silver_description": "Unknowns on both sides, brackets, or a single fraction: tidy up first, then solve.",
 "gold_description": "Fractions and algebraic fractions: clear every denominator, then solve as normal.",
}

# =====================================================================
# tier_guides
# =====================================================================
out["tier_guides"] = {
 "bronze": {
  "title": "Bronze: undo in reverse",
  "steps": [
   "An equation is a balance. Whatever you do to one side, do to the other, so it stays level.",
   "Things were done to \\(x\\) in an order. Undo them in <strong>reverse</strong>: take off any added number first, then divide by the number in front of \\(x\\).",
   "Always check by putting your answer back into the original equation."
  ],
  "example": {"question": "Solve 5x " + M + " 4 = 16", "steps": [
   {"label": "Add 4", "content": "<p>\\(5x = 16 + 4 = 20\\)</p>"},
   {"label": "Divide by 5", "content": "<p>\\(x = 20 " + D + " 5 = 4\\)</p>"},
   {"label": "Check", "content": "<p>\\(5(4) " + M + " 4 = 16\\) ✓</p>"},
   {"label": "Answer", "content": "<p>\\(x = 4\\)</p>", "isAnswer": True, "is_answer": True}
  ]}
 },
 "silver": {
  "title": "Silver: tidy up, then solve",
  "steps": [
   "First clear anything in the way: expand any brackets, or multiply through to remove a single fraction.",
   "If \\(x\\) appears on both sides, collect the \\(x\\) terms on one side and the numbers on the other.",
   "You are left with a bronze-style equation. Solve it and check."
  ],
  "example": {"question": "Solve 2(x + 1) = x + 9", "steps": [
   {"label": "Expand", "content": "<p>\\(2x + 2 = x + 9\\)</p>"},
   {"label": "Collect", "content": "<p>\\(2x " + M + " x = 9 " + M + " 2\\) → \\(x = 7\\)</p>"},
   {"label": "Check", "content": "<p>\\(2(7 + 1) = 16\\) and \\(7 + 9 = 16\\) ✓</p>"},
   {"label": "Answer", "content": "<p>\\(x = 7\\)</p>", "isAnswer": True, "is_answer": True}
  ]}
 },
 "gold": {
  "title": "Gold: clear the fractions first",
  "steps": [
   "Find the lowest common denominator, then multiply <strong>every</strong> term by it, including any whole numbers.",
   "With one fraction equal to another, cross-multiply: each numerator times the other denominator.",
   "No fractions remain. Expand, collect, solve and check as before."
  ],
  "example": {"question": "Solve (x + 4)/3 = (x " + M + " 2)/2", "steps": [
   {"label": "Cross-multiply", "content": "<p>\\(2(x + 4) = 3(x " + M + " 2)\\)</p>"},
   {"label": "Expand", "content": "<p>\\(2x + 8 = 3x " + M + " 6\\)</p>"},
   {"label": "Solve", "content": "<p>\\(8 + 6 = 3x " + M + " 2x\\) → \\(x = 14\\)</p>"},
   {"label": "Check", "content": "<p>\\((14+4)" + D + "3 = 6\\) and \\((14" + M + "2)" + D + "2 = 6\\) ✓</p>"},
   {"label": "Answer", "content": "<p>\\(x = 14\\)</p>", "isAnswer": True, "is_answer": True}
  ]}
 }
}

# =====================================================================
# guided (opener + teach)
# =====================================================================
out["guided"] = {
 "opener": {
  "label": "Before any algebra",
  "display": "A taxi charges £3 to get in, then £2 for every mile.<br>Kim's ride cost £11 in total. How many miles was it?",
  "steps": [
   box("Take off the £3 start fee: 11 " + M + " 3 = £", 8,
       "Subtract the one-off £3 from the £11 total.",
       say="No algebra needed, just think it through. The £3 is charged once, at the start."),
   box("Each mile costs £2, so miles = 8 " + D + " 2 = ", 4,
       "How many lots of £2 fit into £8?",
       say="That £8 was all spent on the miles, at £2 each."),
   sayonly("You just solved \\(2x + 3 = 11\\). Taking off the £3 was subtracting 3 from both sides; dividing by £2 was dividing by the 2 in front of \\(x\\). Undo the +3 first, then the ×2: <strong>inverse operations, in reverse order</strong>. That is the whole method.")
  ]
 },
 "teach": {
  "bronze": {
   "display": "Solve \\(3x + 4 = 19\\)",
   "label": "Together: your first one",
   "steps": [
    box("The number added to 3x is ", 4, "It is the +4.",
        say="Two things have happened to \\(x\\): multiplied by 3, then 4 added. Undo the +4 first."),
    box("Undo it: 19 " + M + " 4 = ", 15, "Take the 4 off both sides. This leaves 3x."),
    box("Undo the " + X + "3: 15 " + D + " 3 = ", 5, "Divide both sides by 3.", say="So \\(3x = 15\\)."),
    box("Check: 3 " + X + " 5 + 4 = ", 19, "Put x = 5 back in.", done="It gives 19, the right-hand side, so x = 5 is right.")
   ]
  },
  "silver": {
   "display": "Solve \\(2(x + 1) = x + 9\\)",
   "label": "Together: the silver move",
   "steps": [
    box("Expand the bracket. 2 " + X + " x = 2x, and 2 " + X + " 1 = ", 2, "Multiply the 1 by 2 as well.",
        say="First clear the bracket: multiply each term inside by 2."),
    box("So 2x + 2 = x + 9. Collect x: 2x " + M + " x = ", 1, "2 minus 1.", post="x"),
    box("So x + 2 = 9. Take off 2: 9 " + M + " 2 = ", 7, "Subtract 2 from both sides."),
    box("Check the left side: 2 " + X + " (7 + 1) = ", 16, "Work out 7 + 1, then times 2.", done="Right side 7 + 9 also = 16, so x = 7 is right.")
   ]
  },
  "gold": {
   "display": "Solve \\(\\frac{x}{3} + \\frac{x}{6} = 3\\)",
   "label": "Together: the gold move",
   "steps": [
    box("First term: 6 " + X + " x/3 = ", 2, "6 divided by 3 is 2, so this becomes 2x.", post="x",
        say="The denominators are 3 and 6, so the lowest common denominator is 6. Multiply every term by 6."),
    box("Second term: 6 " + X + " x/6 = ", 1, "6 divided by 6 is 1, so this becomes x.", post="x"),
    box("Right side: 6 " + X + " 3 = ", 18, "Do not forget to scale the 3. So 2x + x = 18, i.e. 3x = 18."),
    box("Divide by 3: 18 " + D + " 3 = ", 6, "Divide both sides by 3."),
    box("Check: 6 " + D + " 3 + 6 " + D + " 6 = ", 3, "Work out 2 + 1.", done="It gives 3, the right-hand side, so x = 6 is right.")
   ]
  }
 }
}

# method_card: keep the existing slim reference (already within budget). Preserved.

# =====================================================================
# INDEPENDENT VERIFICATION
# =====================================================================
from fractions import Fraction as Fr
def solve_check(disp_id, x, checks):
    for lhs, rhs in checks:
        assert abs(lhs - rhs) < 1e-9, f"{disp_id}: {lhs} != {rhs}"

errors = []
# verify each stored solution independently from the equation structure
verif = {
 ("bronze",0): (4, lambda x: 2*x+3==11),
 ("bronze",1): (5, lambda x: 3*x-5==10),
 ("bronze",2): (12, lambda x: Fr(x,4)==3),
 ("bronze",3): (7, lambda x: 5*x==35),
 ("bronze",4): (8, lambda x: 4*x+1==33),
 ("bronze",5): (3, lambda x: 7*x-2==19),
 ("bronze",6): (9, lambda x: Fr(x,3)+2==5),
 ("bronze",7): (6, lambda x: 20-3*x==2),
 ("silver",0): (4, lambda x: 5*x+2==3*x+10),
 ("silver",1): (5, lambda x: 7*x-3==4*x+12),
 ("silver",2): (6, lambda x: 3*(x+4)==30),
 ("silver",3): (9, lambda x: 3*(x-1)==x+15),
 ("silver",4): (7, lambda x: Fr(x+5,3)==4),
 ("silver",5): (11, lambda x: 4*(x-2)==3*(x+1)),
 ("silver",6): (3, lambda x: 8-2*x==3*x-7),
 ("gold",0): (10, lambda x: Fr(2*x+1,3)==Fr(x+4,2)),
 ("gold",1): (7, lambda x: 3*(2*x+1)==5*(x+2)),
 ("gold",2): (12, lambda x: Fr(x,2)+Fr(x,3)==10),
 ("gold",3): (29, lambda x: Fr(3*(x-1),4)==Fr(2*x+5,3)),
 ("gold",4): (5, lambda x: Fr(x+3,4)+Fr(x-1,2)==4),
}
bankmap = {"bronze": bronze, "silver": silver, "gold": gold}
for (tier,i),(sol,fn) in verif.items():
    p = bankmap[tier][i]
    assert p["solutions"] == [sol], f"{tier}[{i}] solutions {p['solutions']} != [{sol}]"
    assert fn(sol), f"{tier}[{i}] value {sol} does NOT satisfy the equation"
    # verify a couple of nearby non-solutions fail
    assert not fn(sol+1), f"{tier}[{i}] {sol+1} unexpectedly satisfies too"

# verify last live guided box lands on solution & misconception expects != sol
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(bankmap[tier]):
        sol = p["solutions"][0]
        gs = p["guided_steps"]
        boxes = [s for s in gs if s.get("answer") is not None]
        assert len(boxes) >= 3, f"{tier}[{i}] only {len(boxes)} boxes"
        # find the solve box: the box whose answer == sol appearing at/after phase
        phase_idx = next((k for k,s in enumerate(gs) if s.get("phase")=="substitute"), None)
        assert phase_idx is not None, f"{tier}[{i}] no phase"
        live_after = [s for s in gs[phase_idx:] if s.get("answer") is not None]
        assert len(live_after) >= 2, f"{tier}[{i}] only {len(live_after)} live after phase"
        for m in p.get("misconceptions", []):
            e = m.get("expect")
            assert e is not None, f"{tier}[{i}] null expect"
            assert abs(float(e)-float(sol)) > 1e-9, f"{tier}[{i}] expect {e} == sol {sol}"

# teach boxes >= 4
for tier in ("bronze","silver","gold"):
    t = out["guided"]["teach"][tier]
    nb = sum(1 for s in t["steps"] if s.get("answer") is not None)
    assert nb >= 4, f"teach.{tier} has {nb} boxes"

# duplicate check within tiers
for tier in ("bronze","silver","gold"):
    sols = [tuple(p["solutions"]) for p in bankmap[tier]]
    assert len(sols) == len(set(sols)), f"{tier} duplicate solutions: {sols}"

print("ALL VERIFICATION ASSERTS PASSED")
json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT)
print("bronze sols:", [p["solutions"] for p in bronze])
print("silver sols:", [p["solutions"] for p in silver])
print("gold sols:", [p["solutions"] for p in gold])
