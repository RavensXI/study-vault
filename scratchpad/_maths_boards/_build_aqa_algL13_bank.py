# -*- coding: utf-8 -*-
import json, io

def mc(display, opts, correct, hint, miscs):
    idx = opts.index(correct)
    return {
        "display": display, "options": opts, "solutions": [idx],
        "calculator": False, "input_type": "multiple_choice", "hint": hint,
        "misconceptions": miscs
    }

def sv(display, sol, hint, miscs, steps):
    return {
        "display": display, "solutions": [sol], "calculator": False,
        "input_type": "single_value", "hint": hint,
        "misconceptions": miscs, "guided_steps": steps
    }

# ============ BRONZE ============
bronze = []

# B1 MC 5,9,13,17 -> 4n+1  (correct at idx 2)
bronze.append(mc(
    "Find the nth term of \\(5, 9, 13, 17, ...\\)",
    ["\\(4n + 5\\)", "\\(5n + 4\\)", "\\(4n + 1\\)", "\\(4n - 1\\)"],
    "\\(4n + 1\\)",
    "The number in front of n is the common difference; the constant is the zero term (first term minus the difference).",
    [{"pattern": "used_first_term",
      "expect": 0,
      "message": "The number in front of n is the difference (4), but the constant is the zero term: 5 − 4 = 1, not the first term. So the rule is 4n + 1, not 4n + 5."}]
))

# B2 MC 2,7,12,17 -> 5n-3  (correct at idx 3)
bronze.append(mc(
    "Find the nth term of \\(2, 7, 12, 17, ...\\)",
    ["\\(5n + 2\\)", "\\(2n + 5\\)", "\\(5n - 2\\)", "\\(5n - 3\\)"],
    "\\(5n - 3\\)",
    "The number in front of n is the common difference; the constant is the zero term (first term minus the difference).",
    [{"pattern": "used_first_term",
      "expect": 0,
      "message": "d = 5, but the constant is the zero term: 2 − 5 = −3, giving 5n − 3. Using the first term (2) gives 5n + 2, which fails at n = 1."}]
))

# B3 single 20th term of 3,8,13,18 -> 98
bronze.append(sv(
    "Find the 20th term of the sequence \\(3, 8, 13, 18, ...\\)",
    98,
    "Find the nth term first (dn plus the zero term), then substitute n = 20.",
    [{"pattern": "dropped_constant", "expect": 100,
      "message": "The nth term is 5n − 2, so the 20th term is 5 × 20 − 2 = 98. Getting 100 means the − 2 was dropped."},
     {"pattern": "n_not_n_minus_1", "expect": 103,
      "message": "From term 1 to term 20 is 19 steps of 5, so 3 + 19 × 5 = 98. Using 20 steps instead of 19 gives 103."}],
    [
        {"say": "First find the nth term. Common difference:", "pre": "8 − 3 = ", "post": "", "answer": 5, "hint": "Subtract one term from the next."},
        {"say": "The rule starts 5n. Zero term is one step before the first.", "pre": "3 − 5 = ", "post": "", "answer": -2, "hint": "First term minus the difference."},
        {"say": "So the nth term is 5n − 2. Substitute n = 20, starting with 5 × 20.", "phase": "substitute", "pre": "5 × 20 = ", "post": "", "answer": 100, "hint": "Multiply the difference by 20."},
        {"pre": "Now take off the 2: 100 − 2 = ", "post": "", "answer": 98, "hint": "Subtract the zero term's value."},
        {"say": "Check the rule gives the first term.", "pre": "5 × 1 − 2 = ", "post": "", "answer": 3, "done": "Term 1 is 3, so the 20th term 98 is right."}
    ]
))

# B4 MC 10,7,4,1 -> -3n+13 (correct idx 1). Replaced duplicate distractor "10 - 3n"
bronze.append(mc(
    "Find the nth term of \\(10, 7, 4, 1, ...\\)",
    ["\\(3n + 7\\)", "\\(-3n + 13\\)", "\\(-3n + 10\\)", "\\(-3n + 7\\)"],
    "\\(-3n + 13\\)",
    "The difference is negative here; the zero term is the first term minus that negative difference.",
    [{"pattern": "zero_term_is_first_term", "expect": 2,
      "message": "The zero term goes one step BEFORE the first term: 10 − (−3) = 13. Using the first term (10) gives −3n + 10, which gives 7 at n = 1, not 10."}]
))

# B5 single nth term 2n+5, 10th term -> 25
bronze.append(sv(
    "The nth term of a sequence is \\(2n + 5\\). Find the 10th term.",
    25,
    "Substitute n = 10 into the rule and keep the + 5.",
    [{"pattern": "dropped_constant", "expect": 20,
      "message": "Substitute the whole rule: 2 × 10 + 5 = 25. Getting 20 drops the + 5."}],
    [
        {"say": "The rule is 2n + 5. What number multiplies n?", "pre": "The number in front of n is ", "post": "", "answer": 2, "hint": "It is written in front of the n."},
        {"say": "Now substitute n = 10. Work the 2n part first.", "phase": "substitute", "pre": "2 × 10 = ", "post": "", "answer": 20, "hint": "Multiply 2 by 10."},
        {"pre": "Now add the 5: 20 + 5 = ", "post": "", "answer": 25, "hint": "Add the constant term."},
        {"say": "Check the start: term 1 is 2 × 1 + 5.", "pre": "2 + 5 = ", "post": "", "answer": 7, "done": "Term 1 is 7, giving 7, 9, 11, ..., so the 10th term 25 is right."}
    ]
))

# B6 single nth term 3n-1, which term = 50 -> 17
bronze.append(sv(
    "The nth term is \\(3n - 1\\). Which term has value 50?",
    17,
    "This asks which term equals 50, so set the rule equal to 50 and solve for n.",
    [{"pattern": "substituted_50", "expect": 149,
      "message": "This asks WHICH term equals 50, so solve 3n − 1 = 50, giving n = 17. Substituting n = 50 gives 149, which is the value of the 50th term, not what was asked."}],
    [
        {"say": "This asks which term equals 50, so set the rule equal to 50: 3n − 1 = 50. Undo the − 1 by adding 1 to both sides.", "pre": "50 + 1 = ", "post": "", "answer": 51, "hint": "Add 1 to both sides."},
        {"say": "Now 3n = 51. Divide by 3.", "phase": "substitute", "pre": "51 ÷ 3 = ", "post": "", "answer": 17, "hint": "Divide both sides by 3."},
        {"say": "So n = 17: the 17th term is 50. Check it.", "pre": "3 × 17 − 1 = ", "post": "", "answer": 50, "done": "Gives 50, so the 17th term is correct."}
    ]
))

# B7 MC 1,4,7,10 -> 3n-2 (correct idx 3)
bronze.append(mc(
    "Find the nth term of \\(1, 4, 7, 10, ...\\)",
    ["\\(3n + 1\\)", "\\(n + 3\\)", "\\(3n\\)", "\\(3n - 2\\)"],
    "\\(3n - 2\\)",
    "The difference times n, then add the zero term (first term minus the difference).",
    [{"pattern": "used_first_term", "expect": 0,
      "message": "d = 3, but the constant is the zero term: 1 − 3 = −2, so the rule is 3n − 2. Using the first term (1) gives 3n + 1, wrong at n = 1."}]
))

# B8 single n^2+2, 4th term -> 18  (CHANGED from n^2+1 to remove duplicate answer 17)
bronze.append(sv(
    "Write down the first 4 terms of the sequence with nth term \\(n^2 + 2\\). What is the 4th term?",
    18,
    "n squared means multiply n by itself, then add 2.",
    [{"pattern": "read_as_2n", "expect": 10,
      "message": "n squared means 4 × 4 = 16, not 4 × 2. So 16 + 2 = 18. Reading n² as 2n gives 10."},
     {"pattern": "forgot_constant", "expect": 16,
      "message": "4² = 16, then add the 2: 16 + 2 = 18. Stopping at 16 forgets the + 2."}],
    [
        {"say": "The rule is n² + 2. Substitute n = 4. First work n squared.", "pre": "4 × 4 = ", "post": "", "answer": 16, "hint": "n squared means 4 times 4."},
        {"say": "Now add the 2.", "phase": "substitute", "pre": "16 + 2 = ", "post": "", "answer": 18, "hint": "Add the constant term."},
        {"say": "Check the start: term 1 is 1² + 2.", "pre": "1 + 2 = ", "post": "", "answer": 3, "done": "Term 1 is 3, so the sequence is 3, 6, 11, 18 and the 4th term 18 is right."}
    ]
))

# ============ SILVER ============
silver = []

# S1 is 100 in 7,13,19,25? -> 0 (No)
silver.append(sv(
    "Is \\(100\\) a term in the sequence \\(7, 13, 19, 25, ...\\)?  Enter 1 for Yes, 0 for No.",
    0,
    "Find the nth term, set it equal to 100, and check whether n comes out as a whole number.",
    [{"pattern": "rounded_to_yes", "expect": 1,
      "message": "6n + 1 = 100 gives n = 16.5, which is not a whole number, so 100 is NOT in the sequence. The answer is 0 (No). Rounding 16.5 to a term is the trap."}],
    [
        {"say": "Find the nth term. Common difference first.", "pre": "13 − 7 = ", "post": "", "answer": 6, "hint": "Subtract one term from the next."},
        {"say": "Zero term is one step before the first.", "pre": "7 − 6 = ", "post": "", "answer": 1, "hint": "First term minus the difference."},
        {"say": "So the rule is 6n + 1. Set it equal to 100: 6n + 1 = 100, so 6n = 99. Solve for n.", "phase": "substitute", "pre": "99 ÷ 6 = ", "post": "", "answer": 16.5, "hint": "Divide both sides by 6."},
        {"say": "n = 16.5 is not a whole number, so 100 is NOT a term. Answer 0 for No.", "pre": "Enter 0 for No: ", "post": "", "answer": 0, "done": "Since n is not whole, 100 cannot be in the sequence."}
    ]
))

# S2 MC -1,3,7,11 -> 4n-5 (correct idx 2)
silver.append(mc(
    "Find the nth term of \\(-1, 3, 7, 11, ...\\)",
    ["\\(4n - 1\\)", "\\(-n + 4\\)", "\\(4n - 5\\)", "\\(4n + 1\\)"],
    "\\(4n - 5\\)",
    "The constant is the zero term: the first term minus the common difference.",
    [{"pattern": "used_first_term", "expect": 0,
      "message": "d = 4, but the constant is the zero term: −1 − 4 = −5, so 4n − 5. Using the first term (−1) as the constant gives 4n − 1, wrong at n = 1."}]
))

# S3 smallest shared value of 3n+1 and 5n-9 -> 16
silver.append(sv(
    "Two sequences have nth terms \\(3n + 1\\) and \\(5n - 9\\). Find the smallest value they share.",
    16,
    "List a few terms of each sequence and find the first value that appears in both.",
    [{"pattern": "gave_n_not_value", "expect": 5,
      "message": "n = 5 is the term number, not the value. Put it back into the rule: 3 × 5 + 1 = 16. The shared value is 16."}],
    [
        {"say": "List the first few terms of 3n + 1 by putting n = 1, 2, 3, ...", "pre": "n = 1: 3 × 1 + 1 = ", "post": "", "answer": 4, "hint": "Substitute n = 1 into 3n + 1."},
        {"say": "The first sequence is 4, 7, 10, 13, 16, ... Now list 5n − 9.", "pre": "n = 1: 5 × 1 − 9 = ", "post": "", "answer": -4, "hint": "Substitute n = 1 into 5n − 9."},
        {"say": "The second sequence is −4, 1, 6, 11, 16, ... Scan both lists for the first value in common.", "phase": "substitute", "pre": "The smallest shared value is ", "post": "", "answer": 16, "hint": "Compare 4, 7, 10, 13, 16 with −4, 1, 6, 11, 16."},
        {"say": "Check 16 is in the first sequence: 3n + 1 = 16 gives n = 5.", "pre": "3 × 5 + 1 = ", "post": "", "answer": 16, "done": "16 is in both sequences (n = 5 in each), and nothing smaller is shared."}
    ]
))

# S4 a=3, d=-2, 15th term -> -25
silver.append(sv(
    "The first term of an arithmetic sequence is \\(a = 3\\) and the common difference is \\(d = -2\\). Find the 15th term.",
    -25,
    "Use first term plus (n minus 1) times the difference, keeping the difference negative.",
    [{"pattern": "used_n_steps", "expect": -27,
      "message": "From term 1 to term 15 is 14 steps, so 3 + 14 × (−2) = −25. Using 15 steps instead of 14 gives −27."},
     {"pattern": "ignored_sign", "expect": 31,
      "message": "d is −2, so 3 + 14 × (−2) = 3 − 28 = −25. Treating d as +2 gives 31."}],
    [
        {"say": "Use first term + (n − 1) × d. From term 1 to term 15, how many steps?", "pre": "15 − 1 = ", "post": "", "answer": 14, "hint": "It is n minus 1."},
        {"say": "Each step changes by d = −2. Total change over 14 steps:", "phase": "substitute", "pre": "14 × (−2) = ", "post": "", "answer": -28, "hint": "Multiply 14 by −2, keeping the minus."},
        {"say": "Add this to the first term, 3.", "pre": "3 + (−28) = ", "post": "", "answer": -25, "hint": "3 minus 28."},
        {"say": "Check by stepping: term 2 is 3 + (−2) = 1, and it falls by 2 each time.", "pre": "3 + (−2) = ", "post": "", "answer": 1, "done": "The sequence 3, 1, −1, ... falls by 2, reaching −25 at term 15."}
    ]
))

# S5 next term 2,6,18,54 -> 162
silver.append(sv(
    "Find the next term in \\(2, 6, 18, 54, ...\\)",
    162,
    "Each term is multiplied by a fixed ratio; find the ratio, then multiply the last term.",
    [{"pattern": "treated_as_arithmetic", "expect": 90,
      "message": "The terms multiply by 3 each time (geometric), they do not add a fixed amount. 54 × 3 = 162. Adding the last gap (36) gives 90, treating it as arithmetic."}],
    [
        {"say": "Check whether it is geometric: divide a term by the one before.", "pre": "6 ÷ 2 = ", "post": "", "answer": 3, "hint": "Divide the second term by the first."},
        {"say": "Confirm the ratio stays the same.", "pre": "18 ÷ 6 = ", "post": "", "answer": 3, "done": "Constant ratio 3, so it is geometric."},
        {"say": "Multiply the last term by the ratio 3 to get the next term.", "phase": "substitute", "pre": "54 × 3 = ", "post": "", "answer": 162, "hint": "Multiply 54 by 3."},
        {"say": "Check the ratio once more.", "pre": "54 ÷ 18 = ", "post": "", "answer": 3, "done": "The ratio is 3 throughout, so 162 is the next term."}
    ]
))

# S6 nth term 5*2^(n-1), 6th term -> 160
silver.append(sv(
    "The nth term of a geometric sequence is \\(5 \\times 2^{n-1}\\). Find the 6th term.",
    160,
    "The power is n minus 1, so for the 6th term use the power 5.",
    [{"pattern": "used_n_power", "expect": 320,
      "message": "The power is n − 1 = 5, so 5 × 2⁵ = 5 × 32 = 160. Using 2⁶ gives 320."}],
    [
        {"say": "The rule is 5 × 2 to the power (n − 1). For the 6th term, n = 6, so find the power.", "pre": "6 − 1 = ", "post": "", "answer": 5, "hint": "The power is n minus 1."},
        {"say": "Work out 2 to the power 5.", "phase": "substitute", "pre": "2 × 2 × 2 × 2 × 2 = ", "post": "", "answer": 32, "hint": "Multiply 2 by itself five times."},
        {"say": "Now multiply by the 5 in front.", "pre": "5 × 32 = ", "post": "", "answer": 160, "hint": "Multiply the front number by 32."},
        {"say": "Check term 1: power is 1 − 1 = 0, and 2 to the power 0 is 1, so 5 × 1 = 5.", "pre": "5 × 1 = ", "post": "", "answer": 5, "done": "Term 1 is 5, matching the rule, so the 6th term 160 is right."}
    ]
))

# S7 5th=17, 8th=26, first term -> 5
silver.append(sv(
    "The 5th term of an arithmetic sequence is 17 and the 8th term is 26. Find the first term.",
    5,
    "Find the common difference from the gap between the two given terms, then step back to the first term.",
    [{"pattern": "back_wrong_steps", "expect": 2,
      "message": "The 5th term is 4 steps after the first, so go back 4: 17 − 4 × 3 = 5. Going back 5 steps instead gives 2."}],
    [
        {"say": "From the 5th term to the 8th is how many steps?", "pre": "8 − 5 = ", "post": "", "answer": 3, "hint": "Subtract the term numbers."},
        {"say": "The value rose from 17 to 26 over those 3 steps. Total rise:", "pre": "26 − 17 = ", "post": "", "answer": 9, "hint": "Subtract the two term values."},
        {"say": "Common difference is the rise per step.", "phase": "substitute", "pre": "9 ÷ 3 = ", "post": "", "answer": 3, "hint": "Divide the total rise by the number of steps."},
        {"say": "The 5th term is 4 steps after the first. Go back 4 steps of 3 from 17.", "pre": "17 − 4 × 3 = ", "post": "", "answer": 5, "hint": "17 minus 12."},
        {"say": "Check: first term 5, add 3 four times.", "pre": "5 + 3 + 3 + 3 + 3 = ", "post": "", "answer": 17, "done": "The 5th term is 17, so the first term 5 is right."}
    ]
))

# ============ GOLD ============
gold = []

# G1 S_n = n^2+3n, 10th term -> 22
gold.append(sv(
    "The sum of the first \\(n\\) terms of a sequence is \\(S_n = n^2 + 3n\\). Find the 10th term of the sequence.",
    22,
    "The nth term is the total up to n minus the total up to (n minus 1).",
    [{"pattern": "gave_sum", "expect": 130,
      "message": "S₁₀ = 130 is the SUM of the first 10 terms, not the 10th term. The 10th term is S₁₀ − S₉ = 130 − 108 = 22."}],
    [
        {"say": "The 10th term is the total of the first 10 terms minus the total of the first 9. Work S₁₀ = 10² + 3 × 10.", "pre": "100 + 30 = ", "post": "", "answer": 130, "hint": "Square 10, then add 3 times 10."},
        {"say": "Now S₉ = 9² + 3 × 9.", "pre": "81 + 27 = ", "post": "", "answer": 108, "hint": "Square 9, then add 3 times 9."},
        {"say": "The 10th term is S₁₀ − S₉.", "phase": "substitute", "pre": "130 − 108 = ", "post": "", "answer": 22, "hint": "Subtract the two totals."},
        {"say": "Check with the first terms: S₁ = 4 and S₂ = 10, so term 2 = 6.", "pre": "10 − 4 = ", "post": "", "answer": 6, "done": "Terms go 4, 6, 8, ..., rising by 2, so the 10th term 22 fits."}
    ]
))

# G2 geometric a=4, r=1/2, sum first 5 as numerator/4 -> 31
gold.append(sv(
    "A geometric sequence has first term 4 and common ratio \\(\\frac{1}{2}\\). Find the sum of the first 5 terms as a fraction. Give the numerator (denominator is 4).",
    31,
    "Write out all five terms as fractions over 4 and add the numerators.",
    [{"pattern": "stopped_early", "expect": 30,
      "message": "Sum ALL five terms: 4, 2, 1, ½, ¼. As quarters that is 31/4. Stopping after four terms gives 30/4."}],
    [
        {"say": "Write the first five terms. Start at 4 and halve each time.", "pre": "4 ÷ 2 = ", "post": "", "answer": 2, "hint": "Halve the first term."},
        {"say": "The terms are 4, 2, 1, ½, ¼. As quarters: 16/4, 8/4, 4/4, 2/4, 1/4. Add the numerators.", "phase": "substitute", "pre": "16 + 8 + 4 + 2 + 1 = ", "post": "", "answer": 31, "hint": "Add the five numerators over 4."},
        {"say": "So the sum is 31/4. Check as a decimal: 4 + 2 + 1 + 0.5 + 0.25 = 7.75.", "pre": "31 ÷ 4 = ", "post": "", "answer": 7.75, "done": "31/4 = 7.75, matching the decimal sum, so the numerator is 31."}
    ]
))

# G3 prove nth term 5,8,11,14 is 3n+2, 100th term -> 302
gold.append(sv(
    "Prove the nth term of \\(5, 8, 11, 14, ...\\) is \\(3n + 2\\). What is the 100th term?",
    302,
    "Substitute n = 100 into 3n + 2 and keep the + 2.",
    [{"pattern": "dropped_constant", "expect": 300,
      "message": "The 100th term is 3 × 100 + 2 = 302. Getting 300 drops the + 2."}],
    [
        {"say": "First confirm the rule. Common difference:", "pre": "8 − 5 = ", "post": "", "answer": 3, "hint": "Subtract one term from the next."},
        {"say": "Zero term is one step before the first: 5 − 3 = 2, so the rule is 3n + 2, as claimed. Now the 100th term: work 3 × 100.", "phase": "substitute", "pre": "3 × 100 = ", "post": "", "answer": 300, "hint": "Multiply 3 by 100."},
        {"say": "Add the 2.", "pre": "300 + 2 = ", "post": "", "answer": 302, "hint": "Add the + 2 from the rule."},
        {"say": "Check the rule at n = 1: 3 × 1 + 2.", "pre": "3 + 2 = ", "post": "", "answer": 5, "done": "Term 1 is 5, so 3n + 2 is proved and the 100th term is 302."}
    ]
))

# G4 k, 8, 2k+1 arithmetic, find k -> 5
gold.append(sv(
    "A sequence starts \\(k, 8, 2k+1, ...\\) and is arithmetic. Find \\(k\\).",
    5,
    "For an arithmetic sequence the gap from term 1 to 2 equals the gap from term 2 to 3; set them equal.",
    [{"pattern": "sign_slip", "expect": -1,
      "message": "Both gaps must be equal: 8 − k = (2k + 1) − 8. Solving gives k = 5. Flipping the second gap to 8 − (2k + 1) gives k = −1."}],
    [
        {"say": "In an arithmetic sequence the gaps are equal. First gap: 8 − k. Second gap: (2k + 1) − 8 = 2k − 7. Set them equal: 8 − k = 2k − 7. Add k to both sides to get 8 = 3k − 7, then add 7.", "pre": "8 + 7 = ", "post": "", "answer": 15, "hint": "Add 7 to both sides to isolate the 3k."},
        {"say": "So 3k = 15. Divide by 3.", "phase": "substitute", "pre": "15 ÷ 3 = ", "post": "", "answer": 5, "hint": "Divide both sides by 3."},
        {"say": "So k = 5. The sequence becomes 5, 8, 11. Check the gaps are equal.", "pre": "8 − 5 = ", "post": "", "answer": 3, "done": "The gaps 8 − 5 and 11 − 8 both equal 3, so k = 5 is right."}
    ]
))

bank = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "Find the nth term of a simple increasing sequence, or use a given rule to find a term.",
    "silver_description": "Work backwards from terms, test membership, and handle geometric sequences and negative differences.",
    "gold_description": "Reason algebraically about sequences: sum formulas, proofs, and finding unknowns."
}

json.dump(bank, io.open("_L13_bank.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
print("bank written")
