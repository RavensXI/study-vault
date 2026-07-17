# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_eduqas_L13_live.json", encoding="utf-8"))

MINUS = "−"  # unicode minus for prose

def C(msg, expect, pattern):
    return {"check": "common", "expect": expect, "message": msg, "pattern": pattern}

# ---------- SVG figures ----------
def opener_svg():
    # cinema rows: row1=5, row2=7, row3=9 seats (d=2). count shown = count drawn.
    rows = [(5, 22), (7, 52), (9, 82)]  # (seats, y)
    seatw, seath, pitch, cx = 15, 11, 22, 130
    parts = ['<svg viewBox="0 0 260 128" role="img" aria-label="A cinema seating plan: row 1 has 5 seats, row 2 has 7 seats, row 3 has 9 seats, growing by 2 each row." style="max-width:280px">']
    parts.append('<rect x="60" y="6" width="140" height="8" rx="3" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>')
    parts.append('<text x="130" y="13" font-family="Inter,sans-serif" font-size="8" text-anchor="middle" fill="currentColor">SCREEN</text>')
    for n, y in rows:
        width = n * seatw + (n - 1) * (pitch - seatw)
        x0 = cx - width / 2
        for i in range(n):
            x = x0 + i * pitch
            parts.append('<rect x="%.1f" y="%d" width="%d" height="%d" rx="2" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2"/>' % (x, y, seatw, seath))
        parts.append('<text x="%.1f" y="%d" font-family="Inter,sans-serif" font-size="10" text-anchor="end" fill="currentColor">%d</text>' % (x0 - 6, y + 9, n))
    parts.append('</svg>')
    return "".join(parts)

def bronze_teach_svg():
    # dot patterns: pattern1=3, pattern2=5, pattern3=7 dots (d=2). count drawn = count stated.
    groups = [(3, 44), (5, 142), (7, 240)]  # (dots, centre-x)
    r, pitch, y = 5, 16, 34
    parts = ['<svg viewBox="0 0 285 78" role="img" aria-label="Three dot patterns: pattern 1 has 3 dots, pattern 2 has 5 dots, pattern 3 has 7 dots, growing by 2 each time." style="max-width:280px">']
    for i, (n, cx) in enumerate(groups):
        width = (n - 1) * pitch
        x0 = cx - width / 2
        for k in range(n):
            parts.append('<circle cx="%.1f" cy="%d" r="%d" fill="#34d399" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2"/>' % (x0 + k * pitch, y, r))
        parts.append('<text x="%d" y="66" font-family="Inter,sans-serif" font-size="11" text-anchor="middle" fill="currentColor">Pattern %d: %d</text>' % (cx, i + 1, n))
    parts.append('</svg>')
    return "".join(parts)

OP_SVG = opener_svg()
BT_SVG = bronze_teach_svg()

# ---------- BRONZE ----------
bronze = []

# B0 (reordered to front): 10th term of 4,9,14,19 = 49 ; rule 5n-1
bronze.append({
 "display": "Find the 10th term of the sequence \\(4, 9, 14, 19, ...\\)",
 "solutions": [49], "calculator": False, "input_type": "single_value",
 "hint": "Build the nth term rule first, then put n = 10 into it.",
 "misconceptions": [
   C("5 × 10 = 50 is only the 5n part. The rule is 5n " + MINUS + " 1, so the 10th term is 50 " + MINUS + " 1 = 49.", 50, "forgot_constant"),
   C("The constant is first term minus d = 4 " + MINUS + " 5 = " + MINUS + "1, not +4. So 5 × 10 " + MINUS + " 1 = 49.", 54, "used_first_term"),
 ],
 "guided_steps": [
   {"say": "A straight-line sequence, so build its rule first."},
   {"pre": "Common difference: 9 " + MINUS + " 4 = ", "post": "", "answer": 5, "hint": "Subtract the first term from the second."},
   {"pre": "Zero term: 4 " + MINUS + " 5 = ", "post": "", "answer": -1, "hint": "Subtract d from the first term.", "done": "So the rule is \\(5n - 1\\)."},
   {"pre": "The 5n part of the 10th term: 5 × 10 = ", "post": "", "answer": 50, "hint": "Multiply the difference by 10.", "say": "Now use the rule for n = 10.", "phase": "substitute"},
   {"pre": "Add the zero term: 50 " + MINUS + " 1 = ", "post": "", "answer": 49, "hint": "Take 1 away from 50."},
   {"pre": "Check the rule rebuilds term 1: 5 × 1 " + MINUS + " 1 = ", "post": "", "answer": 4, "hint": "Put n = 1 in.", "done": "Gives the first term, so the 10th term is 49."},
 ],
})

# B1: nth term 5,9,13,17 (MC) -> 4n+1 idx0
bronze.append({
 "display": "Find the nth term of \\(5, 9, 13, 17, ...\\)",
 "options": ["\\(4n + 1\\)", "\\(4n + 5\\)", "\\(5n + 4\\)", "\\(4n - 1\\)"],
 "solutions": [0], "calculator": False, "input_type": "multiple_choice",
 "hint": "Common difference 4; the constant is first term minus d.",
 "misconceptions": [
   C("The constant is first term minus d = 5 " + MINUS + " 4 = 1, not the first term 5. Check n = 1: 4 + 1 = 5. The rule is 4n + 1.", 1, "used_first_term"),
   C("The number in front of n is the common difference 4, not the first term 5. The rule is 4n + 1.", 2, "swapped_d"),
 ],
})

# B2: 3,7,11,15 (MC) -> 4n-1 idx0
bronze.append({
 "display": "Find the nth term of \\(3, 7, 11, 15, ...\\)",
 "options": ["\\(4n - 1\\)", "\\(4n + 3\\)", "\\(3n + 4\\)", "\\(4n + 1\\)"],
 "solutions": [0], "calculator": False, "input_type": "multiple_choice",
 "hint": "Common difference 4; the constant is first term minus d.",
 "misconceptions": [
   C("The constant is first term minus d = 3 " + MINUS + " 4 = " + MINUS + "1, not +3. Check n = 1: 4 " + MINUS + " 1 = 3. The rule is 4n " + MINUS + " 1.", 1, "used_first_term"),
   C("The number in front of n is the common difference 4, not the first term 3. The rule is 4n " + MINUS + " 1.", 2, "swapped_d"),
 ],
})

# B3: 2,5,8,11 (MC) -> 3n-1 idx0
bronze.append({
 "display": "Find the nth term of \\(2, 5, 8, 11, ...\\)",
 "options": ["\\(3n - 1\\)", "\\(3n + 2\\)", "\\(2n + 3\\)", "\\(3n + 1\\)"],
 "solutions": [0], "calculator": False, "input_type": "multiple_choice",
 "hint": "Common difference 3; the constant is first term minus d.",
 "misconceptions": [
   C("The constant is first term minus d = 2 " + MINUS + " 3 = " + MINUS + "1, not +2. The rule is 3n " + MINUS + " 1.", 1, "used_first_term"),
   C("The number in front of n is the common difference 3, not the first term 2. The rule is 3n " + MINUS + " 1.", 2, "swapped_d"),
 ],
})

# B4: common difference of 8,5,2,-1 = -3
bronze.append({
 "display": "Find the common difference of \\(8, 5, 2, -1, ...\\)",
 "solutions": [-3], "calculator": False, "input_type": "single_value",
 "hint": "Subtract in order: the second term minus the first.",
 "misconceptions": [
   C("Subtract in order: second term minus first, 5 " + MINUS + " 8 = " + MINUS + "3. The sequence falls, so the difference is negative.", 3, "positive_only"),
 ],
 "guided_steps": [
   {"say": "The common difference is how much you add each step. Subtract in order: the later term minus the earlier one."},
   {"pre": "First gap: 5 " + MINUS + " 8 = ", "post": "", "answer": -3, "hint": "Take 8 from 5; it goes negative."},
   {"pre": "Next gap: 2 " + MINUS + " 5 = ", "post": "", "answer": -3, "hint": "Take 5 from 2.", "say": "Check the gap stays the same all the way along.", "phase": "substitute"},
   {"pre": "And the next: " + MINUS + "1 " + MINUS + " 2 = ", "post": "", "answer": -3, "hint": "Take 2 from minus 1.", "done": "Every gap is " + MINUS + "3, so the common difference is " + MINUS + "3."},
 ],
})

# B5: 10,15,20,25 (MC) -> 5n+5 idx0
bronze.append({
 "display": "Find the nth term of \\(10, 15, 20, 25, ...\\)",
 "options": ["\\(5n + 5\\)", "\\(5n + 10\\)", "\\(10n + 5\\)", "\\(5n\\)"],
 "solutions": [0], "calculator": False, "input_type": "multiple_choice",
 "hint": "Common difference 5; the constant is first term minus d.",
 "misconceptions": [
   C("The constant is first term minus d = 10 " + MINUS + " 5 = 5, not +10. The rule is 5n + 5.", 1, "used_first_term"),
   C("The number in front of n is the common difference 5, not the first term 10. The rule is 5n + 5.", 2, "swapped_d"),
   C("5n alone gives 5, 10, 15, which is 5 too small each time. Add 5: 5n + 5.", 3, "no_constant"),
 ],
})

# B6: 20th term of 1,4,7,10 = 58 ; rule 3n-2
bronze.append({
 "display": "Find the 20th term of \\(1, 4, 7, 10, ...\\)",
 "solutions": [58], "calculator": False, "input_type": "single_value",
 "hint": "Build the nth term rule first, then put n = 20 into it.",
 "misconceptions": [
   C("3 × 20 = 60 is only the 3n part. The rule is 3n " + MINUS + " 2, so the 20th term is 60 " + MINUS + " 2 = 58.", 60, "forgot_constant"),
   C("The constant is first term minus d = 1 " + MINUS + " 3 = " + MINUS + "2, not +1. So 3 × 20 " + MINUS + " 2 = 58.", 61, "used_first_term"),
 ],
 "guided_steps": [
   {"say": "Straight-line sequence: build the rule, then jump to n = 20."},
   {"pre": "Common difference: 4 " + MINUS + " 1 = ", "post": "", "answer": 3, "hint": "Subtract the first term from the second."},
   {"pre": "Zero term: 1 " + MINUS + " 3 = ", "post": "", "answer": -2, "hint": "Subtract d from the first term.", "done": "So the rule is \\(3n - 2\\)."},
   {"pre": "The 3n part of the 20th term: 3 × 20 = ", "post": "", "answer": 60, "hint": "Multiply 3 by 20.", "say": "Now use the rule for n = 20.", "phase": "substitute"},
   {"pre": "Add the zero term: 60 " + MINUS + " 2 = ", "post": "", "answer": 58, "hint": "Take 2 off 60."},
   {"pre": "Check term 1: 3 × 1 " + MINUS + " 2 = ", "post": "", "answer": 1, "hint": "Put n = 1 in.", "done": "Gives the first term, so the 20th term is 58."},
 ],
})

# B7: 6,10,14,18 (MC) -> 4n+2 idx0
bronze.append({
 "display": "Find the nth term of \\(6, 10, 14, 18, ...\\)",
 "options": ["\\(4n + 2\\)", "\\(4n + 6\\)", "\\(6n + 4\\)", "\\(4n\\)"],
 "solutions": [0], "calculator": False, "input_type": "multiple_choice",
 "hint": "Common difference 4; the constant is first term minus d.",
 "misconceptions": [
   C("The constant is first term minus d = 6 " + MINUS + " 4 = 2, not +6. The rule is 4n + 2.", 1, "used_first_term"),
   C("The number in front of n is the common difference 4, not the first term 6. The rule is 4n + 2.", 2, "swapped_d"),
 ],
})

# ---------- SILVER ----------
silver = []

# S0 (reordered to front): nth term 5n-2, which term = 73 -> 15
silver.append({
 "display": "The nth term is \\(5n - 2\\). Which term has value \\(73\\)?",
 "solutions": [15], "calculator": False, "input_type": "single_value",
 "hint": "Set 5n minus 2 equal to 73 and solve for n.",
 "misconceptions": [
   C("Putting n = 73 in finds the 73rd term, not which term equals 73. Solve 5n " + MINUS + " 2 = 73 instead: n = 15.", 363, "substituted_value"),
 ],
 "guided_steps": [
   {"say": "We know the value (73) and want the position n, so solve an equation."},
   {"pre": "Set \\(5n - 2 = 73\\). Add 2 to both sides: 5n = ", "post": "", "answer": 75, "hint": "Add 2 to 73."},
   {"pre": "Divide by 5: n = 75 ÷ 5 = ", "post": "", "answer": 15, "hint": "Divide 75 by 5.", "say": "Now undo the multiply.", "phase": "substitute"},
   {"pre": "Check term 15: 5 × 15 " + MINUS + " 2 = ", "post": "", "answer": 73, "hint": "Put n = 15 back in.", "done": "It gives 73, so the 15th term is 73."},
 ],
})

# S1: Is 83 in 5,8,11,14 (MC) -> Yes n=27 idx0
silver.append({
 "display": "Is \\(83\\) in the sequence \\(5, 8, 11, 14, ...\\)?",
 "options": ["Yes (n = 27)", "No", "Yes (n = 26)", "Yes (n = 28)"],
 "solutions": [0], "calculator": False, "input_type": "multiple_choice",
 "hint": "Find the rule, set it equal to 83, and check n is a whole number.",
 "misconceptions": [
   C("The rule is 3n + 2 (zero term 5 " + MINUS + " 3 = 2), not 3n + 5. With the correct rule, 3n + 2 = 83 gives n = 27, so yes.", 2, "wrong_zero_term"),
 ],
})

# S2: 20,17,14,11 (MC) -> 23-3n idx0
silver.append({
 "display": "Find the nth term of \\(20, 17, 14, 11, ...\\)",
 "options": ["\\(23 - 3n\\)", "\\(20 - 3n\\)", "\\(-3n + 20\\)", "\\(3n + 20\\)"],
 "solutions": [0], "calculator": False, "input_type": "multiple_choice",
 "hint": "The difference is negative; the constant is first term minus d.",
 "misconceptions": [
   C("The constant is first term minus d = 20 " + MINUS + " (" + MINUS + "3) = 23, not 20. Check n = 1: 23 " + MINUS + " 3 = 20. The rule is 23 " + MINUS + " 3n.", 1, "used_first_term"),
   C("The sequence falls, so d = " + MINUS + "3, giving " + MINUS + "3n. 3n + 20 would rise. The rule is 23 " + MINUS + " 3n.", 3, "dropped_minus"),
 ],
})

# S3: -1,3,7,11 (MC) -> 4n-5 idx0
silver.append({
 "display": "Find the nth term of \\(-1, 3, 7, 11, ...\\)",
 "options": ["\\(4n - 5\\)", "\\(4n - 1\\)", "\\(-n + 3\\)", "\\(4n + 1\\)"],
 "solutions": [0], "calculator": False, "input_type": "multiple_choice",
 "hint": "Common difference 4; the constant is minus 1 minus 4.",
 "misconceptions": [
   C("The constant is first term minus d = " + MINUS + "1 " + MINUS + " 4 = " + MINUS + "5, not " + MINUS + "1. Check n = 1: 4 " + MINUS + " 5 = " + MINUS + "1. The rule is 4n " + MINUS + " 5.", 1, "used_first_term"),
   C("Subtracting gives " + MINUS + "1 " + MINUS + " 4 = " + MINUS + "5, a negative constant. 4n + 1 would start at 5. The rule is 4n " + MINUS + " 5.", 3, "sign_slip"),
 ],
})

# S4: 5th term 19, d=4, first term -> 3
silver.append({
 "display": "The 5th term is \\(19\\) and the common difference is \\(4\\). Find the first term.",
 "solutions": [3], "calculator": False, "input_type": "single_value",
 "hint": "From the 1st to the 5th term is 4 steps of d; step back from 19.",
 "misconceptions": [
   C("From the 1st to the 5th term is 4 steps, not 5. First term = 19 " + MINUS + " 4 × 4 = 3.", -1, "used_n_not_n_minus_1"),
   C("The terms rise by 4, so step back (subtract) from the 5th term: 19 " + MINUS + " 4 × 4 = 3, not 19 + 16.", 35, "added_instead"),
 ],
 "guided_steps": [
   {"say": "From the 1st term to the 5th term there are 4 steps of d."},
   {"pre": "Number of steps: 5 " + MINUS + " 1 = ", "post": "", "answer": 4, "hint": "Subtract 1 from 5."},
   {"pre": "Total rise over those steps: 4 × 4 = ", "post": "", "answer": 16, "hint": "Multiply the steps by d.", "done": "The 5th term is 16 above the first."},
   {"pre": "Step back from the 5th term: 19 " + MINUS + " 16 = ", "post": "", "answer": 3, "hint": "Subtract 16 from 19.", "say": "Undo the rise to reach the first term.", "phase": "substitute"},
   {"pre": "Check: from 3, the 5th term is 3 + 4 × 4 = ", "post": "", "answer": 19, "hint": "Add 4 steps of 4 to 3.", "done": "Rebuilds 19, so the first term is 3."},
 ],
})

# S5: Is 50 in 3,7,11,15 (MC) -> No idx0
silver.append({
 "display": "Is \\(50\\) a term in the sequence \\(3, 7, 11, 15, ...\\)?",
 "options": ["No", "Yes (n = 12)", "Yes (n = 13)", "Yes (n = 11)"],
 "solutions": [0], "calculator": False, "input_type": "multiple_choice",
 "hint": "Set the nth term equal to 50; a fraction for n means no.",
 "misconceptions": [
   C("4n " + MINUS + " 1 = 50 gives n = 12.75, not a whole number, so 50 is not a term. You cannot round up to n = 13: the 13th term is 51.", 2, "rounded_up"),
 ],
})

# S6: sum of first 5 of 2,5,8,11 -> 40
silver.append({
 "display": "Find the sum of the first 5 terms of \\(2, 5, 8, 11, ...\\)",
 "solutions": [40], "calculator": False, "input_type": "single_value",
 "hint": "Write out all 5 terms first, then add them up.",
 "misconceptions": [
   C("That adds only the four terms shown. The 5th term is 14: 2 + 5 + 8 + 11 + 14 = 40.", 26, "missed_last_term"),
 ],
 "guided_steps": [
   {"say": "Write out all 5 terms first, then add."},
   {"pre": "The terms are 2, 5, 8, 11, then the 5th is 11 + 3 = ", "post": "", "answer": 14, "hint": "Add the common difference 3 to 11."},
   {"pre": "Add the first pair: 2 + 5 = ", "post": "", "answer": 7, "hint": "Add 2 and 5."},
   {"pre": "Running total with 8: 7 + 8 = ", "post": "", "answer": 15, "hint": "Add 8 to 7.", "say": "Add the terms one at a time.", "phase": "substitute"},
   {"pre": "Add 11: 15 + 11 = ", "post": "", "answer": 26, "hint": "Add 11 to 15."},
   {"pre": "Add the last term 14: 26 + 14 = ", "post": "", "answer": 40, "hint": "Add 14 to 26.", "done": "All five terms total 40."},
 ],
})

# ---------- GOLD ----------
gold = []

# G0: smallest common of 4n-1 and 3n+2 -> 11
gold.append({
 "display": "Two sequences: \\(3, 7, 11, 15, ...\\) and \\(5, 8, 11, 14, ...\\). Find the smallest number that appears in both.",
 "solutions": [11], "calculator": False, "input_type": "single_value",
 "hint": "List a few terms of each and find the first number in both lists.",
 "misconceptions": [
   C("3 is the smallest term of the first sequence, but it is not in the second. A shared value must appear in BOTH lists. The smallest that does is 11.", 3, "smallest_term"),
 ],
 "guided_steps": [
   {"say": "A shared value must appear in BOTH lists. First list: 3, 7, 11, 15, ... Second list: 5, 8, 11, 14, ..."},
   {"pre": "The 3rd term of the first list: 4 × 3 " + MINUS + " 1 = ", "post": "", "answer": 11, "hint": "Put n = 3 into 4n " + MINUS + " 1."},
   {"pre": "Is 11 in the second list? Solve \\(3m + 2 = 11\\), so 3m = 11 " + MINUS + " 2 = ", "post": "", "answer": 9, "hint": "Subtract 2 from 11.", "say": "Test whether 11 also belongs to the second sequence.", "phase": "substitute"},
   {"pre": "m = 9 ÷ 3 = ", "post": "", "answer": 3, "hint": "Divide 9 by 3.", "done": "m = 3 is a whole position, so 11 is in both."},
   {"pre": "Check nothing smaller is shared: is 7 in the second list? 3m + 2 = 7 gives 3m = ", "post": "", "answer": 5, "hint": "Subtract 2 from 7.", "done": "5 ÷ 3 is not whole, so 7 is not shared. The smallest shared value is 11."},
 ],
})

# G1: an+b, 3rd=11, 7th=23, find a -> 3
gold.append({
 "display": "The nth term is \\(an + b\\). The 3rd term is \\(11\\) and the 7th is \\(23\\). Find \\(a\\).",
 "solutions": [3], "calculator": False, "input_type": "single_value",
 "hint": "Write both terms as equations and subtract to remove b.",
 "misconceptions": [
   C("23 " + MINUS + " 11 = 12 is the total rise over the 4 steps between the 3rd and 7th terms, not a itself. Divide by 4: a = 3.", 12, "forgot_divide"),
   C("The rise is over 7 " + MINUS + " 3 = 4 steps, not 3. So a = 12 ÷ 4 = 3.", 4, "wrong_step_count"),
 ],
 "guided_steps": [
   {"say": "Two equations: 3rd term \\(3a + b = 11\\), and 7th term \\(7a + b = 23\\). Subtract to remove b."},
   {"pre": "Subtract the equations: (7a + b) " + MINUS + " (3a + b) leaves 4a. The right side: 23 " + MINUS + " 11 = ", "post": "", "answer": 12, "hint": "Subtract 11 from 23."},
   {"pre": "So 4a = 12. Divide by 4: a = 12 ÷ 4 = ", "post": "", "answer": 3, "hint": "Divide 12 by 4.", "say": "The b cancels, leaving 4a. Solve for a.", "phase": "substitute"},
   {"pre": "Check the step count: from the 3rd to the 7th term is 7 " + MINUS + " 3 = ", "post": "", "answer": 4, "hint": "Subtract 3 from 7.", "done": "4 steps of a make the rise 12, so a = 3."},
 ],
})

# G2: find b (a=3) -> 2
gold.append({
 "display": "Find the value of \\(b\\) (from the previous question).",
 "solutions": [2], "calculator": False, "input_type": "single_value",
 "hint": "Put a = 3 into the 3rd-term equation 3a + b = 11.",
 "misconceptions": [
   C("Substitute the whole term: 3a + b with a = 3 is 3 × 3 + b = 9 + b = 11, so b = 2, not 3 + b.", 8, "forgot_multiply"),
 ],
 "guided_steps": [
   {"say": "Use a = 3 in the 3rd-term equation \\(3a + b = 11\\)."},
   {"pre": "Work out 3a: 3 × 3 = ", "post": "", "answer": 9, "hint": "Multiply a by 3."},
   {"pre": "So 9 + b = 11. Then b = 11 " + MINUS + " 9 = ", "post": "", "answer": 2, "hint": "Subtract 9 from 11.", "say": "Substitute and solve for b.", "phase": "substitute"},
   {"pre": "Check the 7th term: 7 × 3 + 2 = ", "post": "", "answer": 23, "hint": "Work out 7a + b with a = 3, b = 2.", "done": "Gives 23, matching the 7th term, so b = 2."},
 ],
})

# G3: sum of first n of 4,7,10 is 175 -> n=10 (FIXED from 115)
gold.append({
 "display": "The sum of the first \\(n\\) terms of \\(4, 7, 10, ...\\) is 175. Find \\(n\\).",
 "solutions": [10], "calculator": False, "input_type": "single_value",
 "hint": "Use the sum formula, form a quadratic in n, and solve it.",
 "misconceptions": [
   C("3n + 1 = 175 finds which term equals 175, not how many terms sum to 175. Use the sum formula: n = 10.", 58, "used_nth_term"),
 ],
 "guided_steps": [
   {"say": "Use the sum formula \\(S_n = \\frac{n}{2}(2a + (n-1)d)\\) with \\(a = 4\\), \\(d = 3\\)."},
   {"pre": "The bracket 2a + (n " + MINUS + " 1)d = 8 + 3(n " + MINUS + " 1) = 3n + 5, so \\(\\frac{n}{2}(3n + 5) = 175\\). Times both sides by 2: n(3n + 5) = ", "post": "", "answer": 350, "hint": "Double 175."},
   {"pre": "Expand to \\(3n^2 + 5n - 350 = 0\\), which factorises to (n " + MINUS + " 10)(3n + 35) = 0. The positive whole solution is n = ", "post": "", "answer": 10, "hint": "n " + MINUS + " 10 = 0 gives n = 10.", "say": "Solve the quadratic; only a positive whole n makes sense.", "phase": "substitute"},
   {"pre": "Check: the 10th term is 3 × 10 + 1 = 31, so \\(S_{10} = \\frac{10}{2}(4 + 31)\\) = 5 × 35 = ", "post": "", "answer": 175, "hint": "Half of 10 is 5, times (4 + 31).", "done": "Gives 175, so n = 10."},
 ],
})

# G4: a=7, d=-2, how many positive terms -> 4 ; nth = 9-2n
gold.append({
 "display": "An arithmetic sequence has first term \\(a = 7\\) and common difference \\(d = -2\\). How many positive terms are in the sequence?",
 "solutions": [4], "calculator": False, "input_type": "single_value",
 "hint": "Find the nth term rule, then solve nth term > 0.",
 "misconceptions": [
   C("The 5th term is 9 " + MINUS + " 10 = " + MINUS + "1, which is negative. Count only the positive terms 7, 5, 3, 1: there are 4.", 5, "counted_negative"),
 ],
 "guided_steps": [
   {"say": "Find the nth term rule, then see where it stops being positive."},
   {"pre": "Zero term: first term minus d = 7 " + MINUS + " (" + MINUS + "2) = ", "post": "", "answer": 9, "hint": "Subtract minus 2 from 7.", "done": "So the nth term is \\(-2n + 9\\), that is 9 " + MINUS + " 2n."},
   {"pre": "Positive means 9 " + MINUS + " 2n > 0, so 2n < 9, giving n < 4.5. The largest whole n is ", "post": "", "answer": 4, "hint": "The biggest whole number below 4.5.", "say": "Solve the inequality for n.", "phase": "substitute"},
   {"pre": "Check term 4: 9 " + MINUS + " 2 × 4 = ", "post": "", "answer": 1, "hint": "Put n = 4 into 9 " + MINUS + " 2n."},
   {"pre": "Check term 5: 9 " + MINUS + " 2 × 5 = ", "post": "", "answer": -1, "hint": "Put n = 5 in.", "done": "Term 4 is 1 (positive), term 5 is " + MINUS + "1 (negative), so there are 4 positive terms."},
 ],
})

# ---------- assemble ----------
pd = {}
pd["method_card"] = {
 "title": "How to Work with Arithmetic Sequences",
 "steps": [
   "Find the common difference d: subtract each term from the next.",
   "Zero term = first term minus d. The rule is dn + zero term.",
   "To test if a number N is in the sequence, solve nth term = N. A whole n means yes.",
   "For a sum, add the listed terms, or use Sₙ = n/2 (2a + (n − 1)d).",
 ],
 "content": "<p>An <strong>arithmetic sequence</strong> goes up or down by a constant <strong>common difference</strong> \\(d\\).</p><p>The <strong>nth term</strong> is \\(dn + (a - d)\\), where \\(a\\) is the first term. Find \\(d\\), then the zero term \\(a - d\\), and check \\(n = 1\\) rebuilds the start.</p><p><strong>Membership:</strong> set the nth term equal to the number and solve; a whole-number position means it is in the sequence.</p><p><strong>Sum:</strong> \\(S_n = \\frac{n}{2}(2a + (n-1)d)\\).</p>",
 "example": "<p><strong>Find the nth term of</strong> 5, 9, 13, 17, ...</p><p>\\(d = 4\\); zero term \\(= 5 - 4 = 1\\); nth term \\(= 4n + 1\\). Check \\(n = 1\\): \\(4 + 1 = 5\\) \\(\\checkmark\\)</p>",
}

pd["topic_links"] = live["topic_links"]

pd["problem_bank"] = {
 "bronze": bronze,
 "silver": silver,
 "gold": gold,
 "bronze_description": "Find the nth term rule of an arithmetic sequence, and use a rule to find any term or the common difference.",
 "silver_description": "Test whether a number belongs in a sequence, handle falling sequences, sum terms, and work back from a known term.",
 "gold_description": "Sequences that need reasoning: an unknown rule from two terms, a sum that fixes the number of terms, and counting positive terms.",
}

pd["related_videos"] = live["related_videos"]
pd["worked_examples"] = live["worked_examples"]

pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: the nth term of an arithmetic sequence",
   "steps": [
     "Find the <strong>common difference</strong> d: subtract each term from the next. If it is the same every time, the sequence is arithmetic.",
     "The rule starts <strong>dn</strong>. Find the constant from the <strong>zero term</strong>: first term minus d.",
     "So nth term = dn + (first term minus d). Always check n = 1 rebuilds the start.",
   ],
   "example": {
     "question": "Find the nth term of 6, 10, 14, 18, ...",
     "steps": [
       {"label": "Common difference", "content": "<p>\\(10 - 6 = 4\\), and it stays 4, so \\(d = 4\\).</p>"},
       {"label": "Zero term", "content": "<p>First term minus d: \\(6 - 4 = 2\\).</p>"},
       {"label": "Check", "content": "<p>Rule \\(4n + 2\\) at \\(n = 1\\) gives \\(4 + 2 = 6\\). ✓</p>"},
       {"label": "nth term", "content": "<p>\\(4n + 2\\)</p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "silver": {
   "title": "Silver: membership, falling sequences, and working back",
   "steps": [
     "To test if a number N is in a sequence, find the nth term, set it equal to N and solve for n. A whole number means yes; a fraction means no.",
     "Falling sequences have a negative d, but the rule is still dn + (first term minus d).",
     "Given a later term, step back in whole steps of d to reach any earlier term or the first term.",
   ],
   "example": {
     "question": "The 4th term is 20 and d = 3. Find the first term.",
     "steps": [
       {"label": "Steps back", "content": "<p>From the 1st to the 4th term is 3 steps of d.</p>"},
       {"label": "Step back", "content": "<p>\\(20 - 3 \\times 3 = 20 - 9 = 11\\).</p>"},
       {"label": "Check", "content": "<p>From 11: 11, 14, 17, 20. The 4th term is 20. ✓</p>"},
       {"label": "First term", "content": "<p>\\(11\\)</p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "gold": {
   "title": "Gold: unknown rules, sums, and counting terms",
   "steps": [
     "For a rule \\(an + b\\) from two terms, write both as equations and subtract to find a, then substitute back for b.",
     "For a sum, use \\(S_n = \\frac{n}{2}(2a + (n-1)d)\\); setting it equal to a total gives a quadratic in n.",
     "To count positive terms, solve nth term > 0 and take the whole values of n.",
   ],
   "example": {
     "question": "How many positive terms has the sequence with a = 10, d = -3?",
     "steps": [
       {"label": "nth term", "content": "<p>Zero term \\(= 10 - (-3) = 13\\), so nth term \\(= 13 - 3n\\).</p>"},
       {"label": "Solve > 0", "content": "<p>\\(13 - 3n > 0\\), so \\(n < 4.33\\).</p>"},
       {"label": "Check", "content": "<p>Terms: 10, 7, 4, 1, then \\(-2\\). Four are positive.</p>"},
       {"label": "Answer", "content": "<p>\\(4\\)</p>", "isAnswer": True, "is_answer": True},
     ],
   },
 },
}

pd["guided"] = {
 "opener": {
   "label": "Warm-up",
   "display": OP_SVG + "<p>A cinema fills up row by row. The front row has 5 seats, and each row back fits 2 more. Watch how the seats grow, no algebra needed.</p>",
   "steps": [
     {"say": "The front row has 5 seats. Each row further back fits 2 more seats than the row in front."},
     {"pre": "Row 2 has 5 + 2 = ", "post": "", "answer": 7, "hint": "Add 2 to 5."},
     {"pre": "Row 3 has 7 + 2 = ", "post": "", "answer": 9, "hint": "Add 2 more.", "say": "Every row back adds the same 2 seats.", "done": "Up by 2 every row. That fixed jump is the whole idea."},
     {"say": "That fixed jump of 2 is the <strong>common difference</strong>. To find any row \\(n\\) without drawing it, the rule is \\(2n + 3\\). Check row 1: \\(2(1) + 3 = 5\\). ✓ That rule is the <strong>nth term</strong>. Every arithmetic sequence works this way: a fixed step \\(d\\), then the rule \\(dn + (\\text{first} - d)\\)."},
   ],
 },
 "teach": {
   "bronze": {
     "label": "Bronze walk",
     "display": BT_SVG + "<p>Each pattern is made of dots: pattern 1 has 3 dots, pattern 2 has 5, pattern 3 has 7. Find the rule for the number of dots in pattern \\(n\\).</p>",
     "steps": [
       {"say": "The counts are 3, 5, 7. First find how many dots are added each time."},
       {"pre": "5 " + MINUS + " 3 = ", "post": "", "answer": 2, "hint": "Subtract pattern 1 from pattern 2.", "done": "It adds 2 every pattern (7 " + MINUS + " 5 = 2 too), so d = 2."},
       {"pre": "Now the zero term: 3 " + MINUS + " 2 = ", "post": "", "answer": 1, "hint": "Subtract d from the first count.", "say": "The rule starts \\(2n\\). The constant is the zero term:", "done": "So the rule is \\(2n + 1\\)."},
       {"pre": "Use it for pattern 10: 2 × 10 + 1 = ", "post": "", "answer": 21, "hint": "Multiply 2 by 10, then add 1.", "say": "Now the rule works for any pattern, even ones you have not drawn."},
       {"pre": "Check it rebuilds pattern 1: 2 × 1 + 1 = ", "post": "", "answer": 3, "hint": "Put n = 1 into 2n + 1.", "say": "Last, make sure the rule gives back the start:", "done": "Gives 3 dots, so \\(2n + 1\\) is right."},
     ],
   },
   "silver": {
     "label": "Silver walk",
     "display": "<p>Is 100 a term in the sequence \\(4, 9, 14, 19, ...\\)?</p>",
     "steps": [
       {"say": "First find the rule for the sequence."},
       {"pre": "Common difference: 9 " + MINUS + " 4 = ", "post": "", "answer": 5, "hint": "Subtract 4 from 9."},
       {"pre": "Zero term: 4 " + MINUS + " 5 = ", "post": "", "answer": -1, "hint": "Subtract d from the first term.", "done": "So the rule is \\(5n - 1\\)."},
       {"pre": "Now test 100. Set \\(5n - 1 = 100\\), so \\(5n = 101\\). Then n = 101 ÷ 5 = ", "post": "", "answer": 20.2, "hint": "Divide 101 by 5; type the decimal.", "say": "The new move: to test if a number is in the list, set the rule equal to it and solve for the position n.", "done": "n is not a whole number, so 100 lands between terms. It is NOT in the sequence."},
       {"pre": "Contrast with 104: \\(5n - 1 = 104\\) gives \\(5n = 105\\), so n = 105 ÷ 5 = ", "post": "", "answer": 21, "hint": "Divide 105 by 5.", "say": "Compare with a number that does fit:", "done": "A whole number, so 104 is the 21st term. Whole n means yes, a fraction means no."},
     ],
   },
   "gold": {
     "label": "Gold walk",
     "display": "<p>The sum of the first \\(n\\) terms of a sequence is \\(S_n = n^2 + 4n\\). Find the 6th term.</p>",
     "steps": [
       {"say": "A term is the jump in the running total. The 6th term is \\(S_6 - S_5\\)."},
       {"pre": "S₆ = 6² + 4 × 6 = 36 + 24 = ", "post": "", "answer": 60, "hint": "Square 6, then add 4 lots of 6."},
       {"pre": "S₅ = 5² + 4 × 5 = 25 + 20 = ", "post": "", "answer": 45, "hint": "Square 5, then add 4 lots of 5.", "done": "Two running totals ready."},
       {"pre": "The 6th term = S₆ " + MINUS + " S₅ = 60 " + MINUS + " 45 = ", "post": "", "answer": 15, "hint": "Subtract the two totals.", "say": "Now subtract the totals to peel off just the 6th term:", "done": "That gap between the totals is exactly the 6th term."},
       {"pre": "Check the method on term 1: S₁ = 1² + 4 × 1 = ", "post": "", "answer": 5, "hint": "Put n = 1 in; S₁ is the first term itself.", "say": "Confirm with the first term, which is just \\(S_1\\):", "done": "S₁ = 5 is the first term, so each term is the jump in the total. The 6th term is 15."},
     ],
   },
 },
}

json.dump(pd, io.open("lesson_maths-eduqas_algebra-L13.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote lesson_maths-eduqas_algebra-L13.json")
print("opener svg chars:", len(OP_SVG))
print("bronze teach svg chars:", len(BT_SVG))
