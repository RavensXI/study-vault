# -*- coding: utf-8 -*-
"""Build guided-learning practice_data for number-L03 (Decimals & Rounding)."""
import json, io

LIVE = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\_live_number_L03.json"
OUT  = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\lesson_number-L03.json"

pd = json.load(io.open(LIVE, encoding="utf-8"))


def box(pre, answer, hint, post=None, say=None, done=None, phase=None):
    d = {}
    if say is not None:
        d["say"] = say
    d["pre"] = pre
    if post is not None:
        d["post"] = post
    d["answer"] = answer
    d["hint"] = hint
    if done is not None:
        d["done"] = done
    if phase is not None:
        d["phase"] = phase
    return d


def sy(say):
    return {"say": say}


def mis(pattern, expect, message):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}


# ---------------- guided_steps per bank problem ----------------
GS = {}

# B0  4.673 -> 1 d.p. = 4.7
GS["B0"] = [
    sy("Rounding to 1 decimal place means keeping one digit after the point. Two digits decide it: the one you keep and the one right after."),
    box("The 1st decimal place of 4.673 is ", 6, "The first digit after the point."),
    box("The deciding digit, the next one along, is ", 7, "The digit straight after the 6."),
    box("6 rounds up to ", 7, "Add one to 6.", say="7 is 5 or more, so the digit you keep rounds up.", phase="substitute"),
    box("So 4.673 to 1 decimal place is ", 4.7, "One digit after the point: four point seven.", phase="substitute"),
    box("Check: 4.700 − 4.673 = ", 0.027, "Subtract 4.673 from 4.700.", done="The gap up to 4.7 is only 0.027, well under 0.05, so 4.7 is the nearest tenth. Correct.", phase="substitute"),
]

# B1  12.345 -> 2 d.p. = 12.35
GS["B1"] = [
    sy("Rounding to 2 decimal places keeps two digits after the point. Look at the second decimal place and the digit after it."),
    box("The 2nd decimal place of 12.345 is ", 4, "The second digit after the point."),
    box("The deciding digit after it is ", 5, "The next digit along."),
    box("So the 4 rounds up to ", 5, "Add one to 4.", say="The decider is exactly 5, and the rule is that 5 rounds up.", phase="substitute"),
    box("12.345 to 2 decimal places is ", 12.35, "Two digits after the point.", phase="substitute"),
    box("Check: 12.350 − 12.345 = ", 0.005, "Subtract 12.345 from 12.350.", done="12.345 sits exactly halfway between 12.34 and 12.35, and the convention is to round up, so 12.35 is right. Correct.", phase="substitute"),
]

# B2  8.049 -> 1 d.p. = 8
GS["B2"] = [
    sy("Rounding to 1 decimal place. Find the first decimal place and the digit right after it."),
    box("The 1st decimal place of 8.049 is ", 0, "The first digit after the point is 0."),
    box("The deciding digit after it is ", 4, "The next digit along."),
    box("So the 0 stays as ", 0, "It does not change, so 0.", say="4 is below 5, so the kept digit does not change. The 9 further along does not matter.", phase="substitute"),
    box("8.049 to 1 decimal place is ", 8, "Eight point zero, which we write as 8.", phase="substitute"),
    box("Check: 8.049 − 8.0 = ", 0.049, "Subtract 8.0 from 8.049.", done="The gap to 8.0 is 0.049, under 0.05, so 8.0 is the nearest tenth. The 9 was a trap. Correct.", phase="substitute"),
]

# B3  3647 -> nearest 100 = 3600
GS["B3"] = [
    sy("Rounding to the nearest 100. The hundreds digit is the one we keep, and the tens digit decides."),
    box("The hundreds digit of 3647 is ", 6, "3 thousands, 6 hundreds, 4 tens, 7 units."),
    box("The deciding tens digit is ", 4, "The digit in the tens column."),
    box("The hundreds digit stays as ", 6, "It does not change: 6.", say="4 is below 5, so the hundreds digit stays and the digits after it become 0.", phase="substitute"),
    box("So 3647 to the nearest 100 is ", 3600, "Keep 36 hundreds and fill the rest with zeros.", phase="substitute"),
    box("Check: 3647 − 3600 = ", 47, "Subtract 3600 from 3647.", done="3647 is 47 above 3600 and 53 below 3700, so 3600 is nearer. Correct.", phase="substitute"),
]

# B4  0.562 -> 1 s.f. = 0.6
GS["B4"] = [
    sy("Rounding to 1 significant figure. The first significant figure is the first non-zero digit."),
    box("The 1st significant figure of 0.562 is ", 5, "The first non-zero digit."),
    box("The deciding digit after it is ", 6, "The next digit along."),
    box("5 rounds up to ", 6, "Add one to 5.", say="6 is 5 or more, so the 5 rounds up.", phase="substitute"),
    box("0.562 to 1 significant figure is ", 0.6, "Zero point six.", phase="substitute"),
    box("Check: 0.6 − 0.562 = ", 0.038, "Subtract 0.562 from 0.6.", done="The gap to 0.6 is 0.038, smaller than the 0.062 gap down to 0.5, so 0.6 is nearer. Correct.", phase="substitute"),
]

# B5  3.2 + 4.58 = 7.78
GS["B5"] = [
    sy("Adding decimals: line up the decimal points, then add column by column. Write 3.2 as 3.20 so both have two decimal places."),
    box("Hundredths: 0 + 8 = ", 8, "3.20 has 0 hundredths, 4.58 has 8."),
    box("Tenths: 2 + 5 = ", 7, "Add the tenths digits."),
    box("Units: 3 + 4 = ", 7, "Add the whole-number parts.", say="Now the units, then put it together.", phase="substitute"),
    box("So 3.20 + 4.58 = ", 7.78, "Units point tenths hundredths: 7.78.", phase="substitute"),
    box("Check by rounding: 3.2 is about 3, 4.58 is about 5, and 3 + 5 = ", 8, "Round each to the nearest whole number and add.", done="8 is close to 7.78, so the answer is the right size. Correct.", phase="substitute"),
]

# B6  5.7 - 2.35 = 3.35
GS["B6"] = [
    sy("Subtracting decimals: line up the points and write 5.7 as 5.70. Work right to left, borrowing when needed."),
    box("Hundredths: borrow to make 10 − 5 = ", 5, "You cannot do 0 − 5, so borrow one tenth: 10 − 5."),
    box("Tenths: after lending one, 6 − 3 = ", 3, "The 7 tenths became 6 after the borrow."),
    box("Units: 5 − 2 = ", 3, "Subtract the whole-number parts.", say="Now the units, then read off the answer.", phase="substitute"),
    box("So 5.70 − 2.35 = ", 3.35, "Units point tenths hundredths: 3.35.", phase="substitute"),
    box("Check by adding back: 3.35 + 2.35 = ", 5.7, "Add 2.35 to your answer; it should return 5.7.", done="Adding the answer to 2.35 gives back 5.7, so the subtraction is right. Correct.", phase="substitute"),
]

# B7  0.3 x 4 = 1.2
GS["B7"] = [
    sy("Multiplying a decimal: ignore the point first, multiply as whole numbers, then put the point back by counting decimal places."),
    box("Ignore the point: 3 × 4 = ", 12, "Three times four."),
    box("Decimal places in the question: 0.3 has ", 1, "One digit after the point.", post=" d.p."),
    box("12 with 1 decimal place is ", 1.2, "One digit after the point: 1.2.", say="So the answer needs 1 decimal place. Put the point back into 12.", phase="substitute"),
    box("Check by adding: 0.3 + 0.3 + 0.3 + 0.3 = ", 1.2, "Add 0.3 four times.", done="Four lots of 0.3 is 1.2, matching the multiplication. Correct.", phase="substitute"),
]

# S0  0.003482 -> 2 s.f. = 0.0035
GS["S0"] = [
    sy("Rounding to 2 significant figures. Leading zeros are not significant, so start counting at the first non-zero digit."),
    box("The 1st significant figure of 0.003482 is ", 3, "The first non-zero digit."),
    box("The 2nd significant figure is ", 4, "The next digit after the 3."),
    box("The deciding digit after the 4 is ", 8, "The next digit along."),
    box("4 rounds up to ", 5, "Add one to 4.", say="8 is 5 or more, so the 4 rounds up. The leading zeros stay to hold the place value.", phase="substitute"),
    box("0.003482 to 2 significant figures is ", 0.0035, "Keep the three leading zeros: 0.0035.", phase="substitute"),
    box("Check: how many significant figures does 0.0035 have? ", 2, "Count the digits from the first non-zero one: 3 and 5.", done="Two significant figures, 3 and 5, with the zeros only holding place value. Correct.", phase="substitute"),
]

# S1  45982 -> 3 s.f. = 46000
GS["S1"] = [
    sy("Rounding 45982 to 3 significant figures: keep the first three digits, and the next digit decides. Zeros hold the place value."),
    box("The first three significant figures are 4, 5 and ", 9, "The first three digits: 4, 5, 9."),
    box("The deciding digit after the 9 is ", 8, "The 4th digit: 8."),
    box("459 rounded up is ", 460, "459 rounds up to 460.", say="8 is 5 or more, so the 9 rounds up. That makes 459 carry to 460.", phase="substitute"),
    box("Fill the last two places with zeros: 45982 to 3 s.f. is ", 46000, "460 then two zeros.", phase="substitute"),
    box("Check the size: 46000 − 45982 = ", 18, "Subtract 45982 from 46000.", done="Only 18 away from 46000, the nearest 3-figure value. Correct.", phase="substitute"),
]

# S2  Estimate 31.2 x 4.87 = 150
GS["S2"] = [
    sy("Estimating means rounding each number to 1 significant figure first, then multiplying the simple numbers."),
    box("31.2 to 1 significant figure is ", 30, "First figure 3, next digit 1 is below 5, so 30."),
    box("4.87 to 1 significant figure is ", 5, "First figure 4, next digit 8 is 5 or more, so 5."),
    box("30 × 5 = ", 150, "Three times five is fifteen, then add the zero.", say="Now multiply the rounded numbers.", phase="substitute"),
    box("Check with a tighter round: 31 × 5 = ", 155, "Thirty-one times five.", done="155 is close to 150, confirming the estimate is about right. Correct.", phase="substitute"),
]

# S3  Estimate 198 / 0.48 = 400
GS["S3"] = [
    sy("Estimating a division: round each number to 1 significant figure, then divide."),
    box("198 to 1 significant figure is ", 200, "First figure 1, next digit 9 rounds up, so 200."),
    box("0.48 to 1 significant figure is ", 0.5, "First figure 4, next digit 8 rounds up, so 0.5."),
    box("200 ÷ 0.5 = 200 × 2 = ", 400, "Double 200.", say="Dividing by 0.5 is the same as multiplying by 2.", phase="substitute"),
    box("Check by scaling: multiply both by 10, then 2000 ÷ 5 = ", 400, "Two thousand divided by five.", done="Both methods give 400, so the estimate is sound. Correct.", phase="substitute"),
]

# S4  2.4 x 0.3 = 0.72
GS["S4"] = [
    sy("Multiplying decimals: multiply as whole numbers first, then count the total decimal places and put the point back."),
    box("Ignore the points: 24 × 3 = ", 72, "Twenty-four times three."),
    box("Total decimal places: 2.4 has 1 and 0.3 has 1, giving ", 2, "One plus one.", post=" d.p."),
    box("72 with 2 decimal places is ", 0.72, "Two places from the right: 0.72.", say="So the answer has 2 decimal places. Put the point back into 72.", phase="substitute"),
    box("Check the size: 2.4 is about 2, and 2 × 0.3 = ", 0.6, "Two times nought point three.", done="0.6 is close to 0.72, so the size is right. Correct.", phase="substitute"),
]

# S5  6.5 / 0.5 = 13
GS["S5"] = [
    sy("Dividing by a decimal: make the divisor a whole number by multiplying BOTH numbers by the same amount."),
    box("Multiply both by 10. The divisor 0.5 becomes ", 5, "0.5 times 10."),
    box("And 6.5 becomes ", 65, "6.5 times 10."),
    box("65 ÷ 5 = ", 13, "Sixty-five divided by five.", say="Now it is a whole-number division.", phase="substitute"),
    box("Check by multiplying back: 13 × 0.5 = ", 6.5, "Half of 13.", done="13 halves back to 6.5, the original number, so the division is right. Correct.", phase="substitute"),
]

# S6  Estimate sqrt(83) = 9
GS["S6"] = [
    sy("Estimating a square root: find the perfect squares either side, then see which one 83 is closest to."),
    box("The perfect square just below 83 is 81, which is ", 9, "9 × 9 = 81.", post=" squared"),
    box("The perfect square just above 83 is 100, which is ", 10, "10 × 10 = 100.", post=" squared"),
    box("Since 83 is very close to 81, √83 is about ", 9, "Round to the nearer whole root, 9.", say="83 is only just above 81, so the root is just above 9.", phase="substitute"),
    box("Check: 9 × 9 = ", 81, "Nine times nine.", done="9 squared is 81, right next to 83, so √83 is about 9. Correct.", phase="substitute"),
]

# G0  Estimate (6.12 x 48.7) / 0.236 = 1500
GS["G0"] = [
    sy("Estimating a bigger calculation: round every number to 1 significant figure, then work through it."),
    box("6.12 to 1 significant figure is ", 6, "First figure 6, next digit 1 below 5."),
    box("48.7 to 1 significant figure is ", 50, "First figure 4, next digit 8 rounds up, so 50."),
    box("0.236 to 1 significant figure is ", 0.2, "First figure 2, next digit 3 below 5, so 0.2."),
    box("The top: 6 × 50 = ", 300, "Six times fifty.", say="Now the numerator, then divide.", phase="substitute"),
    box("300 ÷ 0.2 = ", 1500, "Dividing by 0.2 multiplies by 5, so 300 × 5.", say="Dividing by 0.2 is the same as multiplying by 5.", phase="substitute"),
    box("Check by scaling: 3000 ÷ 2 = ", 1500, "Three thousand divided by two.", done="Multiplying top and bottom of 300 ÷ 0.2 by 10 gives 3000 ÷ 2 = 1500, the same answer. Correct.", phase="substitute"),
]

# G1  0.07 x 0.004 = 0.00028
GS["G1"] = [
    sy("Multiplying small decimals: multiply the non-zero digits, then count every decimal place and put the point back."),
    box("Ignore the points: 7 × 4 = ", 28, "Seven times four."),
    box("Decimal places: 0.07 has 2 and 0.004 has 3, giving a total of ", 5, "Two plus three.", post=" d.p."),
    box("Place the point 5 digits from the right of 28, giving ", 0.00028, "Zero point, then three zeros, then 28.", say="So the answer needs 5 decimal places. Write 28 and count 5 places from the right, filling with zeros.", phase="substitute"),
    box("Check: how many zeros sit after the point before the 28? ", 3, "0.000 then 28, so three zeros.", done="Three zeros then 28 gives 0.00028, five decimal places in all. Correct.", phase="substitute"),
]

# G2  4.56 / 0.08 = 57
GS["G2"] = [
    sy("Dividing by a decimal: multiply BOTH numbers by the same power of 10 to make the divisor a whole number."),
    box("To turn 0.08 into a whole number, multiply both by 100. 0.08 × 100 = ", 8, "Move the point two places: 8."),
    box("And 4.56 × 100 = ", 456, "Move the point two places: 456."),
    box("456 ÷ 8 = ", 57, "How many eights in 456.", say="Now divide the whole numbers.", phase="substitute"),
    box("Check by multiplying back: 57 × 0.08 = ", 4.56, "57 × 8 = 456, then two decimal places.", done="57 times 0.08 returns 4.56, the original number, so the division is right. Correct.", phase="substitute"),
]

# G3  0.009950 -> 3 s.f. = 0.00995
GS["G3"] = [
    sy("Rounding to 3 significant figures. Leading zeros are not significant, so start at the first non-zero digit."),
    box("The three significant figures of 0.009950 are 9, 9 and ", 5, "The first three non-zero-place digits: 9, 9, 5."),
    box("The deciding digit after the last 5 is ", 0, "The next digit along is 0."),
    box("The 5 stays as ", 5, "It does not change: 5.", say="0 is below 5, so nothing rounds up. The digits stay as they are.", phase="substitute"),
    box("So 0.009950 to 3 significant figures is ", 0.00995, "Keep the two leading zeros: 0.00995.", phase="substitute"),
    box("Check: how many significant figures does 0.00995 have? ", 3, "Count from the first 9: 9, 9, 5.", done="Three significant figures, 9, 9 and 5, with the zeros only holding place value. The trailing 0 rounds nothing up. Correct.", phase="substitute"),
]

# G4  Estimate (sqrt(99) + 4.1^2) / 1.97 = 13
GS["G4"] = [
    sy("Estimating a calculation with a root and a square: round each part to something easy, then work through it in order."),
    box("√99 is very close to √100, which is ", 10, "10 × 10 = 100."),
    box("4.1 squared is about 4 squared, which is ", 16, "4 × 4 = 16."),
    box("1.97 to 1 significant figure is ", 2, "Almost 2."),
    box("The top first: 10 + 16 = ", 26, "Add the two parts of the numerator.", say="Work out the numerator first, then divide.", phase="substitute"),
    box("Now divide by 2: 26 ÷ 2 = ", 13, "Half of 26.", phase="substitute"),
    box("Check by multiplying back: 13 × 2 = ", 26, "Thirteen times two.", done="13 times 2 returns 26, the numerator, so the estimate is right. Correct.", phase="substitute"),
]

# ---------------- misconceptions per problem ----------------
MIS = {
    "B0": [mis("round_down", 4.6, "The 2nd decimal place is 7, which is 5 or more, so the digit you keep rounds up. 4.673 to 1 d.p. is 4.7, not 4.6.")],
    "B1": [mis("wrong_places", 12.3, "2 decimal places means two digits after the point. 12.345 to 2 d.p. is 12.35. 12.3 has only one decimal place.")],
    "B2": [mis("round_up", 8.1, "The 2nd decimal place is 4, which is below 5, so the kept digit stays. 8.049 to 1 d.p. is 8.0, not 8.1. The 9 further along does not matter.")],
    "B3": [mis("round_up", 3700, "For the nearest 100, the tens digit decides. Here it is 4, below 5, so round down to 3600, not 3700."),
           mis("wrong_place", 3650, "3650 is the nearest 50, not the nearest 100. The answer must end in 00, and since the tens digit 4 is below 5, it is 3600.")],
    "B4": [mis("round_down", 0.5, "The first significant figure is 5, and the next digit is 6, which is 5 or more, so round up to 0.6, not 0.5.")],
    "B5": [mis("misalign", 7.6, "Line up the decimal points, not the last digits: 3.20 + 4.58 = 7.78. Slipping the 2 into the hundredths column gives 7.60 by mistake.")],
    "B6": [mis("no_borrow", 3.45, "In the hundredths column you cannot take 5 from 0, so borrow: 5.70 − 2.35 = 3.35. Taking 0 from 5 to get 5 gives 3.45 by mistake.")],
    "B7": [mis("decimal_error", 12, "3 × 4 = 12, but 0.3 has one decimal place, so the answer has one too: 1.2, not 12.")],
    "S0": [mis("place_shift", 0.035, "Keep the place value. 0.003482 to 2 s.f. is 0.0035. Writing 0.035 shifts the decimal and makes the number ten times too big.")],
    "S1": [mis("no_zeros", 460, "Keep the place value by filling with zeros: 45982 to 3 s.f. is 46000, not 460."),
           mis("no_carry", 45900, "The 4th digit is 8, so the 9 rounds up and carries to make 46000. Leaving it as 459 gives 45900, which is too small.")],
    "S2": [mis("round_wrong", 120, "1 s.f.: 4.87 rounds to 5, because the next digit 8 is 5 or more, not to 4. So 30 × 5 = 150, not 120."),
           mis("no_round", 155, "Round every number to 1 s.f. first: 31.2 becomes 30, not 31. Then 30 × 5 = 150.")],
    "S3": [mis("divide_wrong", 100, "Dividing by 0.5 doubles the number: 200 ÷ 0.5 = 400. Multiplying by 0.5 instead gives 100."),
           mis("round_wrong", 500, "1 s.f.: 0.48 rounds to 0.5, because the next digit 8 is 5 or more, not to 0.4. Then 200 ÷ 0.5 = 400.")],
    "S4": [mis("decimal_places", 7.2, "24 × 3 = 72, and 2.4 × 0.3 has two decimal places in total (one from each number), so the answer is 0.72, not 7.2.")],
    "S5": [mis("scale_one", 1.3, "Multiply BOTH numbers by 10: 65 ÷ 5 = 13. Scaling only the 0.5 gives 6.5 ÷ 5 = 1.3, ten times too small.")],
    "S6": [mis("halve", 41.5, "A square root is not a half. \\(9^2 = 81\\), so \\(\\sqrt{83}\\) is about 9, not 41.5.")],
    "G0": [mis("divide_by_decimal", 60, "Dividing by 0.2 multiplies by 5: 300 ÷ 0.2 = 1500. Multiplying by 0.2 instead gives 60.")],
    "G1": [mis("too_few_places", 0.028, "7 × 4 = 28. Count every decimal place: 0.07 has 2 and 0.004 has 3, which is 5 in total, giving 0.00028. Stopping at 3 places gives 0.028.")],
    "G2": [mis("scale_one", 0.57, "Multiply BOTH numbers by 100: 456 ÷ 8 = 57. Scaling only the 0.08 gives 4.56 ÷ 8 = 0.57, a hundred times too small.")],
    "G3": [mis("place_shift", 0.0995, "Keep the place value. 0.009950 to 3 s.f. is 0.00995. Writing 0.0995 shifts the decimal and makes it ten times too big.")],
    "G4": [mis("order_error", 18, "Work out the whole top first: \\(10 + 16 = 26\\), then divide by 2 to get 13. Dividing only the 16 gives \\(10 + 8 = 18\\)."),
           mis("square_as_double", 9, "Squaring means \\(4.1 \\times 4.1 \\approx 16\\), not \\(4.1 \\times 2 = 8\\). So \\((10 + 16) \\div 2 = 13\\), not 9.")],
}

HINT = {
    "B0": "Look at the digit after the first decimal place to decide.",
    "B1": "The third decimal place decides, and an exact 5 rounds up.",
    "B2": "The digit after the first decimal place is 4, so it rounds down.",
    "B3": "For the nearest 100, the tens digit decides.",
    "B4": "Round to the first significant figure using the next digit.",
    "B5": "Line up the decimal points and add.",
    "B6": "Line up the decimal points and subtract, borrowing if needed.",
    "B7": "Multiply 3 by 4, then place one decimal point.",
    "S0": "Start counting significant figures at the first non-zero digit.",
    "S1": "Keep three significant figures and fill the rest with zeros.",
    "S2": "Round each number to 1 significant figure, then multiply.",
    "S3": "Round each number to 1 significant figure, then divide.",
    "S4": "Multiply 24 by 3, then count two decimal places.",
    "S5": "Multiply both numbers by 10, then divide.",
    "S6": "Find the perfect squares either side of 83.",
    "G0": "Round each number to 1 significant figure, then work top then bottom.",
    "G1": "Multiply 7 by 4, then count five decimal places.",
    "G2": "Multiply both numbers by 100, then divide.",
    "G3": "Keep three significant figures; the next digit is 0, so nothing rounds up.",
    "G4": "Round the root and the square, add the top, then divide.",
}

# order of keys per tier matches the live bank order
ORDER = {
    "gold":   ["G0", "G1", "G2", "G3", "G4"],
    "bronze": ["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"],
    "silver": ["S0", "S1", "S2", "S3", "S4", "S5", "S6"],
}

pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    keys = ORDER[tier]
    probs = pb[tier]
    assert len(keys) == len(probs), (tier, len(keys), len(probs))
    for k, p in zip(keys, probs):
        p["hint"] = HINT[k]
        p["misconceptions"] = MIS[k]
        p["guided_steps"] = GS[k]

# tier descriptions
pb["bronze_description"] = "Round to a given number of decimal places, significant figures or the nearest 10 or 100, and add, subtract or multiply simple decimals."
pb["silver_description"] = "Round to significant figures with leading zeros, estimate calculations by rounding to 1 s.f., and divide with decimals."
pb["gold_description"] = "Estimate multi-step calculations with roots and squares, and handle very small or awkward decimals accurately."

# ---------------- tier_guides ----------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: rounding and simple decimal sums",
        "steps": [
            "<strong>Rounding:</strong> find the digit you are keeping, then look at the very next digit. If it is 5 or more, round up; if it is 4 or less, it stays the same.",
            "<strong>Nearest 10 or 100:</strong> the digit in that column is the one you keep, and the digit to its right decides.",
            "<strong>Adding and subtracting decimals:</strong> line up the decimal points, fill gaps with zeros, then work column by column.",
        ],
        "example": {
            "question": "Round 5.28 to 1 decimal place",
            "steps": [
                {"label": "Find the digit to keep", "content": "The 1st decimal place is 2 (5.<strong>2</strong>8)."},
                {"label": "Look at the next digit", "content": "The next digit is 8. Since 8 is 5 or more, round up."},
                {"label": "Check", "content": "2 rounds up to 3, and 5.3 is the nearer tenth to 5.28."},
                {"label": "Answer", "content": "<strong>5.3</strong>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: significant figures and estimating",
        "steps": [
            "<strong>Significant figures:</strong> start counting at the first non-zero digit. Leading zeros are not significant, they only hold the place value.",
            "<strong>Estimating:</strong> round every number in the calculation to 1 significant figure, then work out the simpler version.",
            "<strong>Dividing by a decimal:</strong> multiply both numbers by 10, 100 and so on until the divisor is a whole number.",
        ],
        "example": {
            "question": "Estimate 62 × 0.38",
            "steps": [
                {"label": "Round to 1 s.f.", "content": "62 becomes 60 and 0.38 becomes 0.4."},
                {"label": "Multiply", "content": "60 × 0.4 = 24."},
                {"label": "Check", "content": "A tighter estimate, 60 × 0.38 = 22.8, is close to 24."},
                {"label": "Answer", "content": "<strong>≈ 24</strong>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: multi-step estimates and awkward decimals",
        "steps": [
            "<strong>Round first:</strong> change every number to 1 significant figure, including roots and squares (√99 becomes 10, 4.1² becomes 16).",
            "<strong>Work in order:</strong> finish the top of a fraction before dividing, and treat dividing by 0.5 as doubling and by 0.2 as multiplying by 5.",
            "<strong>Small decimals:</strong> when multiplying, count every decimal place; when rounding, keep the leading zeros so the place value stays right.",
        ],
        "example": {
            "question": "Estimate (√101 + 5.2²) ÷ 2.1",
            "steps": [
                {"label": "Round each part", "content": "√101 ≈ 10, 5.2² ≈ 25, 2.1 ≈ 2."},
                {"label": "Top first", "content": "10 + 25 = 35."},
                {"label": "Divide", "content": "35 ÷ 2 = 17.5."},
                {"label": "Check", "content": "17.5 × 2 = 35, the numerator, so the estimate holds."},
                {"label": "Answer", "content": "<strong>≈ 17.5</strong> (about 18)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------- guided (opener + teach) ----------------
pd["guided"] = {
    "opener": {
        "label": "Start here: a shopping puzzle",
        "display": "Your basket: a book <strong>£3.89</strong>, a pen <strong>£2.10</strong>, a mug <strong>£6.95</strong>.<br>Roughly, in your head, about how much altogether?",
        "steps": [
            sy("No exact sums yet. Round each price to the nearest pound and add them up."),
            box("£4 + £2 + £7 = £", 13, "£3.89 is about £4, £2.10 about £2, £6.95 about £7."),
            sy("That rough total, £13, is an <strong>estimate</strong>. You made it by <strong>rounding</strong> each price to the nearest pound before adding. The real total is £12.94, so £13 was spot on for a quick check."),
            box("Now round just the book, £3.89, to the nearest 10 pence: £", 3.9, "3.89 is between 3.80 and 3.90, and nearer 3.90."),
            sy("Rounding to the nearest 10p is the same idea as rounding to 1 decimal place: £3.89 becomes £3.90. <strong>Rounding</strong> and <strong>estimating</strong> are today's whole topic, and you already do them every time you shop. Now we make the rules exact."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "Round \\(6.37\\) to 1 decimal place",
            "steps": [
                sy("Rounding to 1 decimal place: keep one digit after the point, and the next digit decides."),
                box("The 1st decimal place of 6.37 is ", 3, "The first digit after the point."),
                box("The deciding digit after it is ", 7, "The next digit along."),
                box("7 is 5 or more, so the 3 rounds up to ", 4, "Add one to 3."),
                box("So 6.37 to 1 decimal place is ", 6.4, "Six point four."),
                box("Check: 6.4 − 6.37 = ", 0.03, "Subtract 6.37 from 6.4.", done="The gap is 0.03, under 0.05, so 6.4 is the nearest tenth. That is the whole method."),
            ],
        },
        "silver": {
            "display": "Round \\(0.02617\\) to 2 significant figures",
            "steps": [
                sy("Significant figures start at the first non-zero digit. Leading zeros only hold the place."),
                box("The 1st significant figure of 0.02617 is ", 2, "The first non-zero digit."),
                box("The 2nd significant figure is ", 6, "The next digit after the 2."),
                box("The deciding digit after the 6 is ", 1, "The next digit along."),
                box("1 is below 5, so the 6 stays. Keeping the place value, 0.02617 to 2 s.f. is ", 0.026, "Zero point zero two six."),
                box("Check: how many significant figures does 0.026 have? ", 2, "Count from the first non-zero digit: 2 and 6.", done="Two, the 2 and the 6, with the leading zero only holding place value. That is the new move: count from the first non-zero digit."),
            ],
        },
        "gold": {
            "display": "Estimate \\(\\frac{7.8 \\times 31}{0.51}\\)",
            "steps": [
                sy("A bigger estimate: round every number to 1 significant figure, do the top, then divide."),
                box("7.8 to 1 significant figure is ", 8, "First figure 7, next digit 8 rounds up: 8."),
                box("31 to 1 significant figure is ", 30, "First figure 3, next digit 1 below 5: 30."),
                box("0.51 to 1 significant figure is ", 0.5, "First figure 5, next digit 1 below 5: 0.5."),
                box("The top: 8 × 30 = ", 240, "Eight times thirty."),
                box("Divide by 0.5, which doubles: 240 ÷ 0.5 = ", 480, "240 × 2."),
                box("Check by scaling: 2400 ÷ 5 = ", 480, "Two thousand four hundred divided by five.", done="Both routes give 480, so the estimate holds. That is the new move: round everything, then work top then bottom."),
            ],
        },
    },
}

# ---------------- slim method_card ----------------
pd["method_card"] = {
    "title": "Rounding and Estimation",
    "steps": [
        "Rounding: keep the required digit, then round up if the next digit is 5 or more.",
        "Significant figures: count from the first non-zero digit and keep zeros that hold the place value.",
        "Estimate: round every number to 1 s.f., then calculate.",
        "Decimals: line up points for + and −, count decimal places for ×, and scale the divisor to a whole number for ÷.",
    ],
    "content": "<p><strong>Rounding</strong> to decimal places or significant figures: locate the digit you are keeping, then look at the next digit. 5 or more rounds up; 4 or less stays. For significant figures, start at the first non-zero digit and keep any zeros that hold the place value.</p><p><strong>Estimating:</strong> round every number to 1 significant figure, then work out the simpler calculation. Dividing by 0.5 doubles a number; dividing by 0.2 multiplies it by 5.</p><p><strong>Decimal arithmetic:</strong> line up the points to add or subtract, count the total decimal places when multiplying, and scale both numbers so the divisor is whole when dividing.</p>",
    "example": "<p><strong>Estimate</strong> \\(68.4 \\times 0.52\\): round to 1 s.f., \\(70 \\times 0.5 = 35\\).</p>",
}

# ---------------- de-dash preserved worked_examples (hard style rule) ----------------
def dedash(s):
    if not isinstance(s, str):
        return s
    return s.replace(" — ", ": ").replace("—", ": ")

for we in pd.get("worked_examples", []):
    if isinstance(we.get("question"), str):
        we["question"] = dedash(we["question"])
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str):
            st["label"] = dedash(st["label"])
        if isinstance(st.get("content"), str):
            st["content"] = dedash(st["content"])

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written", OUT)
