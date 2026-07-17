# -*- coding: utf-8 -*-
# Full guided-learning conversion of AQA algebra-L11 (Inequalities).
import json, io

pd = json.load(io.open("_live_aqa_algL11.json", encoding="utf-8"))
pb = pd["problem_bank"]

# ---- helper to set common MC fields ----
def mc(display, options, correct_idx, hint, misc):
    return {
        "display": display,
        "options": options,
        "solutions": [correct_idx],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": hint,
        "misconceptions": misc,
    }

def M(pattern, expect, message, note):
    return {"pattern": pattern, "expect": expect, "message": message, "note": note}

# =================== BRONZE ===================
bronze = [
    mc("Solve \\(x + 4 > 9\\). Which is the solution?",
       ["\\(x > 5\\)", "\\(x > 13\\)", "\\(x < 5\\)", "\\(x > 4\\)"], 0,
       "Subtract 4 from both sides.",
       [M("arithmetic", 1, "Take 4 off both sides, do not add it: x > 9 − 4 = 5.", "Adds 4: x>13."),
        M("wrong_direction", 2, "The boundary 5 is right but the arrow is reversed. No negative was used, so keep >.", "Flips to x<5.")]),
    mc("Solve \\(3x \\le 15\\). Which is the solution?",
       ["\\(x \\le 5\\)", "\\(x < 5\\)", "\\(x \\ge 5\\)", "\\(x \\le 45\\)"], 0,
       "Divide both sides by 3.",
       [M("strict_vs_nonstrict", 1, "The question uses ≤, so the answer must use ≤, not the strict <.", "Uses < instead of ≤."),
        M("wrong_direction", 2, "Dividing by a positive keeps the arrow the same way, so it stays ≤.", "Flips to ≥."),
        M("arithmetic", 3, "To undo 3 times x, divide by 3, do not multiply: x ≤ 5.", "Multiplies: 3×15=45.")]),
    mc("Solve \\(2x - 1 < 9\\). Which is the solution?",
       ["\\(x < 5\\)", "\\(x < 4\\)", "\\(x > 5\\)", "\\(x \\le 5\\)"], 0,
       "Add 1 to both sides, then divide by 2.",
       [M("arithmetic", 1, "Add the 1 to both sides: 2x < 9 + 1 = 10, then divide by 2 to get x < 5.", "Subtracts 1: 2x<8, x<4."),
        M("wrong_direction", 2, "The boundary 5 is right but the arrow is reversed. Keep < as no negative was used.", "Flips to x>5."),
        M("strict_vs_nonstrict", 3, "The question uses <, so 5 is not included; use <, not ≤.", "Uses ≤.")]),
    mc("Solve \\(5x + 2 \\ge 17\\). Which is the solution?",
       ["\\(x \\ge 3\\)", "\\(x > 3\\)", "\\(x \\ge 15\\)", "\\(x \\le 3\\)"], 0,
       "Subtract 2 from both sides, then divide by 5.",
       [M("strict_vs_nonstrict", 1, "The question uses ≥, so 3 is included; use ≥, not the strict >.", "Uses > instead of ≥."),
        M("arithmetic", 2, "After 5x ≥ 15 you still divide by 5: x ≥ 3.", "Forgets to divide by 5, keeps x≥15."),
        M("wrong_direction", 3, "The boundary 3 is right but the arrow is reversed; keep ≥.", "Flips to ≤.")]),
    mc("List the integer values of \\(n\\) where \\(-2 < n \\le 3\\). Which list is correct?",
       ["\\(-1, 0, 1, 2, 3\\)", "\\(-2, -1, 0, 1, 2, 3\\)", "\\(-1, 0, 1, 2\\)", "\\(0, 1, 2, 3\\)"], 0,
       "The left symbol is strict, the right one includes its value.",
       [M("include_endpoint", 1, "The left symbol is strict (<), so −2 is NOT included. Start at −1.", "Includes -2."),
        M("wrong_integers", 2, "The right symbol is ≤, so 3 IS included: the list ends at 3.", "Drops the 3."),
        M("wrong_integers", 3, "Do not skip the negatives: −1 is greater than −2, so it counts.", "Ignores negatives.")]),
    mc("Solve \\(4x > 2x + 6\\). Which is the solution?",
       ["\\(x > 3\\)", "\\(x > 1\\)", "\\(x < 3\\)", "\\(x > 6\\)"], 0,
       "Take 2x from both sides, then divide by 2.",
       [M("wrong_direction", 2, "The boundary 3 is right but the arrow is reversed; keep >.", "Flips to x<3."),
        M("arithmetic", 3, "After 2x > 6 you still divide by 2: x > 3.", "Forgets to divide by 2, keeps x>6.")]),
    mc("Solve \\(10 - x < 4\\). Which is the solution?",
       ["\\(x > 6\\)", "\\(x < 6\\)", "\\(x > 14\\)", "\\(x < -6\\)"], 0,
       "Get −x on its own, then divide by minus 1 and flip the sign.",
       [M("didnt_flip", 1, "You reach −x < −6. Dividing by a negative flips the sign, so x > 6, not x < 6.", "Divides by -1 without flipping: x<6."),
        M("wrong_direction", 3, "−x < −6 becomes x > 6 after flipping; x < −6 keeps the wrong direction.", "Keeps x<-6 sign.")]),
    mc("Solve \\(\\frac{x}{2} + 1 > 5\\). Which is the solution?",
       ["\\(x > 8\\)", "\\(x > 4\\)", "\\(x > 12\\)", "\\(x > 10\\)"], 0,
       "Subtract 1, then multiply both sides by 2.",
       [M("arithmetic", 1, "After x/2 > 4, multiply by 2 to undo the divide: x > 8.", "Forgets to multiply by 2: keeps x>4."),
        M("arithmetic", 2, "Take the 1 off first: x/2 > 5 − 1 = 4, then times 2 gives x > 8.", "Adds 1: x/2>6, x>12.")]),
]

# =================== SILVER ===================
silver = [
    mc("Solve \\(-2x + 5 > 11\\). Which is the solution?",
       ["\\(x < -3\\)", "\\(x > -3\\)", "\\(x < 3\\)", "\\(x > 3\\)"], 0,
       "Subtract 5, then divide by minus 2 and flip the sign.",
       [M("didnt_flip", 1, "You reach −2x > 6. Dividing by minus 2 flips the sign: x < −3.", "Divides by -2 without flipping: x>-3."),
        M("arithmetic", 3, "The coefficient is minus 2, not 2. Divide by minus 2 and flip: x < −3.", "Treats -2 as 2: 2x>6, x>3.")]),
    mc("Solve \\(3(x - 2) \\le 12\\). Which is the solution?",
       ["\\(x \\le 6\\)", "\\(x < 6\\)", "\\(x \\le 2\\)", "\\(x \\le 14\\)"], 0,
       "Expand the bracket first, then solve.",
       [M("strict_vs_nonstrict", 1, "The question uses ≤, so 6 is included; use ≤, not <.", "Uses < instead of ≤."),
        M("no_expand", 3, "Expand first: 3(x − 2) is 3x − 6, giving 3x ≤ 18 and x ≤ 6.", "Divides by 3 only on left: x-2≤12, x≤14.")]),
    mc("Solve \\(7 - 3x \\ge 1\\). Which is the solution?",
       ["\\(x \\le 2\\)", "\\(x \\ge 2\\)", "\\(x \\le -2\\)", "\\(x \\ge -2\\)"], 0,
       "Subtract 7, then divide by minus 3 and flip the sign.",
       [M("didnt_flip", 1, "You reach −3x ≥ −6. Dividing by minus 3 flips the sign: x ≤ 2.", "Divides by -3 without flipping: x≥2."),
        M("arithmetic", 2, "A negative divided by a negative is positive: −6 ÷ −3 = 2, so x ≤ 2.", "Computes -6/-3 as -2: x≤-2.")]),
    mc("Solve \\(1 < 2x - 3 \\le 9\\). Which list of integer values of \\(x\\) is correct?",
       ["\\(3, 4, 5, 6\\)", "\\(2, 3, 4, 5, 6\\)", "\\(3, 4, 5\\)", "\\(2, 3, 4, 5\\)"], 0,
       "Add 3 to all three parts, then divide all three by 2.",
       [M("include_endpoint", 1, "The left symbol is strict (<), giving 2 < x, so 2 is NOT included. Start at 3.", "Includes 2."),
        M("wrong_integers", 2, "The right symbol is ≤, so x ≤ 6 includes 6: the list ends at 6.", "Drops the 6.")]),
    mc("Solve \\(5x + 3 > 2x + 15\\). Which is the solution?",
       ["\\(x > 4\\)", "\\(x > 6\\)", "\\(x < 4\\)", "\\(x > 2\\)"], 0,
       "Take 2x from both sides and 3 from both sides.",
       [M("arithmetic", 1, "Take 3 off both sides: 3x > 15 − 3 = 12, then divide by 3 to get x > 4.", "Adds 3: 3x>18, x>6."),
        M("wrong_direction", 2, "The boundary 4 is right but the arrow is reversed; keep >.", "Flips to x<4.")]),
    mc("Solve \\(-4 \\le 3x + 2 < 11\\). Which list of integer values of \\(x\\) is correct?",
       ["\\(-2, -1, 0, 1, 2\\)", "\\(-2, -1, 0, 1, 2, 3\\)", "\\(-1, 0, 1, 2\\)", "\\(-2, -1, 0, 1\\)"], 0,
       "Subtract 2 from all three parts, then divide all three by 3.",
       [M("wrong_integers", 1, "The right symbol is strict (<), giving x < 3, so 3 is NOT included.", "Includes 3."),
        M("include_endpoint", 2, "The left symbol is ≤, giving −2 ≤ x, so −2 IS included. Start at −2.", "Drops -2.")]),
    {
        "display": "Find the largest integer \\(n\\) such that \\(4n - 7 < 20\\).",
        "solutions": [6],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Add 7, then find the largest whole number that keeps 4n below the bound.",
        "misconceptions": [
            M("wrong_integers", 7, "4n < 27 gives n < 6.75, and the symbol is strict, so 7 is too big. The largest integer is 6.", "Rounds 6.75 up to 7."),
            M("arithmetic", 3, "Add the 7, do not subtract it: 4n < 20 + 7 = 27, then divide by 4.", "Subtracts 7: 4n<13, largest 3."),
        ],
        "guided_steps": [
            {"say": "Solve \\(4n - 7 < 20\\) like an equation. Add 7 to both sides."},
            {"pre": "20 + 7 = ", "post": "", "answer": 27, "hint": "Add 7 to 20."},
            {"say": "So \\(4n < 27\\). We need the largest whole number n with \\(4n < 27\\). Try n = 6."},
            {"pre": "4 × 6 = ", "post": "", "answer": 24, "hint": "Multiply 4 by 6."},
            {"say": "24 is less than 27, so n = 6 works. Now test n = 7."},
            {"pre": "4 × 7 = ", "post": "", "answer": 28, "hint": "Multiply 4 by 7.", "phase": "substitute"},
            {"pre": "28 is more than 27, so 7 is too big. The largest integer n is ", "post": "", "answer": 6,
             "hint": "n = 6 gives 24, which is under 27.",
             "done": "4 × 6 = 24 is less than 27, but 4 × 7 = 28 is not. The largest integer is 6.", "phase": "substitute"},
        ],
    },
]

# =================== GOLD ===================
gold = [
    mc("Solve \\(x^2 < 16\\). Which is the solution?",
       ["\\(-4 < x < 4\\)", "\\(x < 4\\)", "\\(x < 16\\)", "\\(x > -4\\)"], 0,
       "Take the square root both ways: x lies between the two roots.",
       [M("positive_only", 1, "x² < 16 allows negatives too. The full range is −4 < x < 4, not just x < 4.", "Keeps positive root only."),
        M("wrong_root", 2, "Square root both sides: √16 = 4, so the bound is 4, not 16.", "Forgets to square root.")]),
    mc("Solve \\(x^2 \\ge 9\\). Which is the solution?",
       ["\\(x \\le -3\\) or \\(x \\ge 3\\)", "\\(x \\ge 3\\)", "\\(-3 \\le x \\le 3\\)", "\\(x \\ge 9\\)"], 0,
       "For x² ≥ a number, the answer splits into two separate regions.",
       [M("positive_only", 1, "x² ≥ 9 has two parts: x ≤ −3 as well as x ≥ 3. A big negative like −4 also works.", "Keeps x≥3 only."),
        M("wrong_region", 2, "−3 ≤ x ≤ 3 is the solution to x² ≤ 9, the opposite inequality. Here x² ≥ 9 gives the outside.", "Uses the inside region."),
        M("wrong_root", 3, "Square root both sides: √9 = 3, so the bound is 3, not 9.", "Forgets to square root.")]),
    mc("Solve \\(2x + 1 > 5\\) and \\(3x - 4 < 14\\) simultaneously. Which is the solution?",
       ["\\(2 < x < 6\\)", "\\(x > 2\\)", "\\(x < 6\\)", "\\(2 < x \\le 6\\)"], 0,
       "Solve each inequality, then keep the overlap.",
       [M("one_only", 1, "That is only the first inequality. 3x − 4 < 14 also gives x < 6, so combine to 2 < x < 6.", "First only."),
        M("one_only", 2, "That is only the second inequality. 2x + 1 > 5 also gives x > 2, so combine to 2 < x < 6.", "Second only."),
        M("strict_vs_nonstrict", 3, "Both inequalities are strict, so both ends stay strict: 2 < x < 6.", "Uses ≤ on upper end.")]),
    {
        "display": "If \\(n\\) is a positive integer and \\(n^2 < 50\\), find the largest possible value of \\(n\\).",
        "solutions": [7],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Try squaring whole numbers until you pass 50.",
        "misconceptions": [
            M("wrong_root", 8, "√50 is about 7.07, so n must be 7 or less. 8² = 64 is above 50, so 8 is too big.", "Rounds 7.07 up to 8."),
            M("arithmetic", 25, "n² means n × n, not 2 × n. Square the number: 7² = 49, which is under 50.", "Treats n² as 2n: 2n<50, n<25."),
        ],
        "guided_steps": [
            {"say": "We need the largest whole number n with \\(n^2 < 50\\). Try n = 7."},
            {"pre": "7 × 7 = ", "post": "", "answer": 49, "hint": "Square 7."},
            {"say": "49 is less than 50, so n = 7 works. Now test n = 8."},
            {"pre": "8 × 8 = ", "post": "", "answer": 64, "hint": "Square 8.", "phase": "substitute"},
            {"pre": "64 is more than 50, so 8 is too big. The largest possible n is ", "post": "", "answer": 7,
             "hint": "n = 7 gives 49, which is under 50.",
             "done": "7² = 49 is less than 50, but 8² = 64 is not. The largest positive integer is 7.", "phase": "substitute"},
        ],
    },
    mc("Solve \\(-3 < \\frac{2x-1}{3} \\le 5\\). Which list of integer values of \\(x\\) is correct?",
       ["\\(-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8\\)",
        "\\(-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8\\)",
        "\\(-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7\\)",
        "\\(-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7\\)"], 0,
       "Multiply all three parts by 3, add 1, then divide by 2.",
       [M("include_endpoint", 1, "After solving, −4 < x, and the symbol is strict, so −4 is NOT included. Start at −3.", "Includes -4."),
        M("wrong_integers", 2, "The right symbol is ≤, giving x ≤ 8, so 8 IS included: the list ends at 8.", "Drops the 8.")]),
]

pb["bronze"] = bronze
pb["silver"] = silver
pb["gold"] = gold
pb["bronze_description"] = "One and two step inequalities, including listing integers in a range."
pb["silver_description"] = "Negatives that flip the sign, brackets, and double inequalities."
pb["gold_description"] = "Quadratic inequalities, combined inequalities, and integer solutions."

# =================== tier_guides ===================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one and two step inequalities",
        "steps": [
            "Solve like an equation: undo the <strong>+</strong> or <strong>−</strong> first, then the <strong>×</strong> or <strong>÷</strong>.",
            "Do the same thing to both sides, and keep the same symbol all the way through.",
            "The answer is a range, like \\(x > 5\\): every number bigger than 5, not one value.",
        ],
        "example": {
            "question": "Solve \\(x + 4 > 9\\)",
            "steps": [
                {"label": "Subtract 4", "content": "\\(x > 5\\)"},
                {"label": "Check", "content": "Try \\(x = 6\\): \\(6 + 4 = 10 > 9\\), so 6 fits."},
                {"label": "Answer", "content": "\\(x > 5\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: sign flips and double inequalities",
        "steps": [
            "If you multiply or divide by a <strong>negative</strong>, flip the sign: \\(>\\) becomes \\(<\\).",
            "For a double inequality like \\(1 < 2x \\le 8\\), do the same step to all three parts.",
            "Expand any brackets first, then solve as normal.",
        ],
        "example": {
            "question": "Solve \\(7 - 3x \\ge 1\\)",
            "steps": [
                {"label": "Subtract 7", "content": "\\(-3x \\ge -6\\)"},
                {"label": "Divide by −3 and flip", "content": "\\(x \\le 2\\)"},
                {"label": "Check", "content": "Try \\(x = 2\\): \\(7 - 6 = 1 \\ge 1\\), so 2 fits."},
                {"label": "Answer", "content": "\\(x \\le 2\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: quadratic and combined inequalities",
        "steps": [
            "For \\(x^2 < k\\), square root both ways: \\(-\\sqrt{k} < x < \\sqrt{k}\\). For \\(x^2 \\ge k\\) it splits: \\(x \\le -\\sqrt{k}\\) or \\(x \\ge \\sqrt{k}\\).",
            "For two inequalities at once, solve each and keep only the overlap, like \\(2 < x < 6\\).",
            "Listing integers, include negatives and check each end: a strict symbol leaves the boundary out.",
        ],
        "example": {
            "question": "Solve \\(x^2 < 25\\)",
            "steps": [
                {"label": "Square root both ways", "content": "\\(-5 < x < 5\\)"},
                {"label": "Check", "content": "Try \\(x = 4\\): \\(16 < 25\\); \\(x = 6\\) gives \\(36\\), not \\(< 25\\)."},
                {"label": "Answer", "content": "\\(-5 < x < 5\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# =================== guided (opener + teach) ===================
pd["guided"] = {
    "opener": {
        "steps": [
            {"say": "A puzzle first, no algebra needed. New trainers cost £20. You already have £8 and you save £4 every week."},
            {"pre": "Fewest whole weeks until you can afford them? ", "post": "weeks", "answer": 3,
             "hint": "You need £12 more, saving £4 each week."},
            {"say": "3 weeks works, and so do 4, or 5. The answer is a whole <strong>range</strong>, 3 or more, not a single number. Writing your money as \\(8 + 4w\\), you found where \\(8 + 4w \\ge 20\\). That is an <strong>inequality</strong>: solve it just like an equation, but the answer is a range."},
            {"pre": "Check the boundary: after exactly 3 weeks, how much have you saved, in £? ", "post": "", "answer": 20,
             "hint": "Start with £8 and add £4 three times."},
            {"say": "£20, exactly enough. That boundary comes from solving \\(8 + 4w = 20\\), and the inequality then says 3 weeks or more. One warning for later: if you ever divide by a negative, the inequality sign flips over."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Solve \\(3x + 4 < 19\\)",
            "steps": [
                {"say": "Solve \\(3x + 4 < 19\\) the same way you solve an equation. First take 4 off both sides."},
                {"pre": "19 − 4 = ", "post": "", "answer": 15, "hint": "Subtract 4 from the right-hand side."},
                {"say": "So \\(3x < 15\\). Now divide both sides by 3."},
                {"pre": "15 ÷ 3 = ", "post": "", "answer": 5, "hint": "Divide the right-hand side by 3."},
                {"say": "So \\(x < 5\\): every number less than 5. Keep the same symbol \\(<\\), because we did not divide by a negative."},
                {"pre": "Test x = 4: 3 × 4 + 4 = ", "post": "", "answer": 16, "hint": "Work out 3 × 4 + 4.",
                 "done": "16 is less than 19, so x = 4 fits. The range x < 5 is right."},
                {"pre": "Test the boundary x = 5: 3 × 5 + 4 = ", "post": "", "answer": 19, "hint": "Work out 3 × 5 + 4.",
                 "done": "19 is not less than 19, so 5 is NOT included. That is why its circle is open."},
            ],
        },
        "silver": {
            "display": "Solve \\(5 - 2x \\le 13\\)",
            "steps": [
                {"say": "Solve \\(5 - 2x \\le 13\\). Take 5 off both sides first."},
                {"pre": "13 − 5 = ", "post": "", "answer": 8, "hint": "Subtract 5 from the right."},
                {"say": "So \\(-2x \\le 8\\). Now divide by −2. Because we divide by a NEGATIVE, the sign flips: \\(\\le\\) becomes \\(\\ge\\)."},
                {"pre": "8 ÷ (−2) = ", "post": "", "answer": -4, "hint": "A positive divided by a negative is negative."},
                {"say": "So \\(x \\ge -4\\). The flip is the whole point: dividing by a negative reverses the arrow."},
                {"pre": "Test x = 0 (more than −4): 5 − 2 × 0 = ", "post": "", "answer": 5, "hint": "2 × 0 is 0.",
                 "done": "5 is less than 13, so x = 0 fits, confirming x ≥ −4."},
                {"pre": "Test x = −5 (less than −4): 5 − 2 × (−5) = ", "post": "", "answer": 15, "hint": "−2 × −5 = +10, then add 5.",
                 "done": "15 is NOT less than 13, so −5 fails. The arrow really does point the other way."},
            ],
        },
        "gold": {
            "display": "List the integers satisfying \\(x^2 < 30\\)",
            "steps": [
                {"say": "\\(x^2 < 30\\) means x lies between \\(-\\sqrt{30}\\) and \\(\\sqrt{30}\\). Find the biggest whole number whose square is still under 30. Try 5."},
                {"pre": "5 × 5 = ", "post": "", "answer": 25, "hint": "Square 5."},
                {"say": "25 is under 30, so 5 is allowed. Now try 6."},
                {"pre": "6 × 6 = ", "post": "", "answer": 36, "hint": "Square 6."},
                {"say": "36 is over 30, so 6 is too big. The integers run from −5 up to 5."},
                {"pre": "The largest integer with \\(x^2 < 30\\) is ", "post": "", "answer": 5, "hint": "5² = 25 is under 30, 6² = 36 is too big."},
                {"pre": "How many integers from −5 to 5 inclusive? ", "post": "", "answer": 11, "hint": "Count −5, −4, ..., 4, 5.",
                 "done": "Eleven integers, −5 to 5. Don't forget the negatives and zero."},
            ],
        },
    },
}

# =================== method_card (slim) ===================
pd["method_card"] = {
    "title": "Solving Inequalities",
    "steps": [
        "Solve like an equation: the same operation to both sides until the letter is alone.",
        "Multiplying or dividing by a negative flips the inequality sign.",
        "For \\(x^2 < k\\), the answer is \\(-\\sqrt{k} < x < \\sqrt{k}\\).",
        "To list integers, take the range and write every whole number in it, negatives included.",
    ],
    "content": "<p>An <strong>inequality</strong> uses \\(<\\), \\(>\\), \\(\\le\\), \\(\\ge\\) instead of \\(=\\). Solve it exactly like an equation, with one extra rule: dividing or multiplying by a <strong>negative</strong> flips the sign, so \\(<\\) becomes \\(>\\).</p><p>Strict symbols (\\(<\\), \\(>\\)) leave the boundary out; \\(\\le\\) and \\(\\ge\\) include it. Do the same step to all three parts of a double inequality.</p>",
    "example": "<p><strong>Solve</strong> \\(3x + 5 > 14\\)</p><p>Subtract 5: \\(3x > 9\\). Divide by 3: \\(x > 3\\).</p>",
}

# topic_links, related_videos, worked_examples preserved as-is from live.

out = "lesson_maths-aqa_algebra-L11.json"
json.dump(pd, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out)
print("word count method content:", len(pd["method_card"]["content"].replace("\\("," ").replace("\\)"," ").split()))
for t in ("bronze","silver","gold"):
    tot=sum(len(s.replace("\\(", " ").replace("\\)", " ").split()) for s in pd["tier_guides"][t]["steps"])
    print("tier_guide", t, "words:", tot)
