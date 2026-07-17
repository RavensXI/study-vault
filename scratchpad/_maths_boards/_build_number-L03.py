# -*- coding: utf-8 -*-
"""Full guided conversion for number-L03 (Decimals & Rounding), maths-aqa."""
import json, io

SRC = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_number-L03.json"
OUT = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-aqa_number-L03.json"

pd = json.load(io.open(SRC, encoding="utf-8"))


def box(pre, answer, hint, post=None, say=None, done=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post is not None: d["post"] = post
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d


def say(s):
    return {"say": s}


# -------- misconceptions {pattern, message, expect} --------
MIS = {
    "bronze": [
        [{"pattern": "round_down", "expect": 4.3,
          "message": "4.3 ignores the 7. The digit after the first decimal place is 7, which is 5 or more, so the 3 rounds up to 4.4."}],
        [{"pattern": "round_down", "expect": None,
          "message": "Dropping the 5 gives 6.84, but a 5 rounds up, so the answer is 6.85."}],
        [{"pattern": "round_down", "expect": 2500,
          "message": "2500 rounds down, but the tens digit is 6, which is 5 or more, so round up to 2600."}],
        [{"pattern": "round_up", "expect": 0.8,
          "message": "0.8 rounds up wrongly. The digit after the tenths is 3, which is less than 5, so it stays 0.7."}],
        [{"pattern": "round_down", "expect": 34.9,
          "message": "34.9 ignores the 5. The digit after the tenths is 5, so the 9 rounds up and carries to 35.0."}],
        [{"pattern": "round_down", "expect": None,
          "message": "Dropping the 6 gives 7.99, but the 6 rounds the 9 up, which carries all the way to 8.00."}],
        [{"pattern": "no_simplify", "expect": 4,
          "message": "4 comes from 4/10 before simplifying. 4/10 cancels to 2/5, so the numerator is 2."}],
        [{"pattern": "dp_error", "expect": 2.1,
          "message": "2.1 has the point in the wrong place. 3 times 7 is 21, and there are 2 decimal places in total, so the answer is 0.21."}],
    ],
    "silver": [
        [{"pattern": "count_zeros", "expect": None,
          "message": "Counting a leading zero as significant gives 0.06. Significant figures start at the first non-zero digit 6, so the 2nd is 4 and the next digit 7 rounds it up to 0.065."}],
        [{"pattern": "wrong_sf", "expect": 3400,
          "message": "3400 rounds down, but the digit after the second significant figure is 5, so it rounds up to 3500."}],
        [{"pattern": "round_down", "expect": None,
          "message": "Keeping the 9 gives 0.809, but the next digit is 7, so the 9 rounds up and carries to 0.810."}],
        [{"pattern": "round_instead", "expect": 3.9,
          "message": "3.9 rounds the number. Truncating just chops off the extra digits, so 3.876 becomes 3.8."}],
        [{"pattern": "dp_error", "expect": 3.6,
          "message": "3.6 has the point one place out. 24 times 15 is 360, and there are 3 decimal places altogether, so the answer is 0.36."}],
        [{"pattern": "dp_error", "expect": 0.08,
          "message": "0.08 keeps the decimals. Multiply both numbers by 100 first, then 48 divided by 6 is 8."}],
        [{"pattern": "wrong_sf", "expect": 49000,
          "message": "49000 rounds down, but the digit after the second significant figure is 7, so the 9 rounds up and carries to 50000."}],
    ],
    "gold": [
        [{"pattern": "div_by_decimal", "expect": 50,
          "message": "50 comes from multiplying by 0.5 instead of dividing. Dividing 100 by 0.5 asks how many halves fit in 100, which is 200."}],
        [{"pattern": "div_by_decimal", "expect": 5,
          "message": "5 comes from multiplying by 0.05 instead of dividing. 100 divided by 0.05 is 2000."}],
        [{"pattern": "dp_error", "expect": 1.44,
          "message": "1.44 counts only 2 decimal places. Squaring 0.12 doubles the 2 decimal places to 4, so 12 times 12 is 144 becomes 0.0144."}],
        [{"pattern": "root_is_half", "expect": 31,
          "message": "31 halves 62. A square root is not a half. Since 7.9 squared is about 62.4, the root of 62 is about 7.9."}],
        [{"pattern": "round_instead", "expect": None,
          "message": "Treating it as rounding suggests 3.475, but truncation keeps 3.47 for any third digit from 0 to 9, so the greatest value to 3 decimal places is 3.479."}],
    ],
}

# -------- hints --------
HINT = {
    "bronze": [
        "Look at the digit after the first decimal place to decide whether to round up.",
        "The digit after the second decimal place is 5, so round up.",
        "Check the tens digit to decide whether the hundreds round up.",
        "The digit after the first decimal place is less than 5, so round down.",
        "The 5 makes the 9 round up, so it carries into the whole number.",
        "The 6 rounds the 9 up, which carries all the way to 8.",
        "Write it over 10, then cancel the fraction down.",
        "Multiply 3 by 7, then place 2 decimal places.",
    ],
    "silver": [
        "Start counting from the first non-zero digit, then check the next digit.",
        "Keep place value with zeros after rounding the second significant figure.",
        "The next digit rounds the 9 up, so it carries.",
        "Truncating means chop off the extra digits, never round.",
        "Work out 24 times 15, then count three decimal places.",
        "Multiply both numbers by 100 first, then divide.",
        "Round the second significant figure and hold the place value with zeros.",
    ],
    "gold": [
        "Round each number to 1 significant figure, then dividing by 0.5 doubles the top.",
        "Round to 1 significant figure, then dividing by 0.05 multiplies by 20.",
        "Squaring 0.12 gives four decimal places.",
        "It lies between 7 and 8, closer to 8.",
        "Truncation keeps 3.47 for any third digit up to 9.",
    ],
}

# -------- guided_steps (full walks, phase:substitute boundary) --------
GS = {"bronze": [], "silver": [], "gold": []}

# bronze rounding-place template: target digit, decider (substitute), answer
GS["bronze"].append([
    say("We are rounding \\(4.372\\) to 1 decimal place."),
    box("Write the digit sitting in the first decimal place.", 3, "It is the first digit after the point."),
    box("Write the very next digit to the right, the one that decides.", 7, "It is the digit in the second decimal place.", phase="substitute"),
    box("7 is 5 or more, so the 3 rounds up. Write the number to 1 decimal place.", 4.4, "The 3 becomes 4 and everything after is dropped.",
        done="4.4 has one decimal place and rounds correctly."),
])
GS["bronze"].append([
    say("We are rounding \\(6.845\\) to 2 decimal places."),
    box("Write the digit in the second decimal place.", 4, "It is the second digit after the point."),
    box("Write the next digit to the right, the decider.", 5, "It is the third decimal digit.", phase="substitute"),
    box("5 rounds up, so the 4 becomes 5. Write the number to 2 decimal places.", 6.85, "Only the last kept digit changes.",
        done="6.85 has two decimal places. Correct."),
])
GS["bronze"].append([
    say("We are rounding \\(2563\\) to the nearest 100."),
    box("Write the digit in the hundreds place.", 5, "In 2563 the hundreds digit is the 5."),
    box("Write the digit in the tens place, the decider.", 6, "The tens digit decides whether the hundreds round up.", phase="substitute"),
    box("6 is 5 or more, so round up. Write the number to the nearest 100.", 2600, "The tens and units become zeros.",
        done="2600 is the nearest multiple of 100."),
])
GS["bronze"].append([
    say("We are rounding \\(0.739\\) to 1 decimal place."),
    box("Write the digit in the first decimal place.", 7, "It is the first digit after the point."),
    box("Write the next digit to the right, the decider.", 3, "It is the second decimal digit.", phase="substitute"),
    box("3 is less than 5, so the 7 stays. Write the number to 1 decimal place.", 0.7, "Rounding down means the digit does not change.",
        done="0.7 has one decimal place. Correct."),
])
GS["bronze"].append([
    say("We are rounding \\(34.95\\) to 1 decimal place."),
    box("Write the digit in the first decimal place.", 9, "It is the tenths digit."),
    box("Write the next digit to the right, the decider.", 5, "It is the hundredths digit.", phase="substitute",
        say="The 9 rounds up, so it becomes 10 and carries into the whole number."),
    box("The 9 rounds up and carries. Write the number to 1 decimal place.", 35, "34.9 rounds up to 35.0.",
        done="35.0 is 34.95 rounded to 1 decimal place."),
])
GS["bronze"].append([
    say("We are rounding \\(7.996\\) to 2 decimal places."),
    box("Write the digit in the second decimal place.", 9, "It is the hundredths digit."),
    box("Write the next digit to the right, the decider.", 6, "It is the thousandths digit.", phase="substitute",
        say="6 rounds the 9 up, so it carries all the way to a whole number."),
    box("The carry reaches the units. Write the number to 2 decimal places.", 8, "7.99 rounds up to 8.00.",
        done="8.00 is 7.996 rounded to 2 decimal places."),
])
GS["bronze"].append([
    say("We are writing \\(0.4\\) as a fraction in its simplest form."),
    box("0.4 is 4 tenths, so write it as a fraction over 10. Write the top number.", 4, "The numerator sits over 10."),
    box("Divide the denominator 10 by the common factor 2.", 5, "10 divided by 2 is 5.", phase="substitute"),
    box("Divide the numerator 4 by the same factor 2. Write the simplest numerator.", 2, "4 divided by 2 is 2.",
        done="2/5 is 0.4 in its simplest form, numerator 2."),
])
GS["bronze"].append([
    say("We are working out \\(0.3 \\times 0.7\\)."),
    box("Ignore the points and multiply the digits: 3 times 7.", 21, "3 times 7 is 21."),
    box("Count the decimal places in the question: 0.3 has 1 and 0.7 has 1. Write the total.", 2, "1 plus 1 is 2.", phase="substitute"),
    box("Put 2 decimal places into 21. Write the answer.", 0.21, "21 with 2 decimal places is 0.21.",
        done="0.3 times 0.7 is 0.21."),
])

# silver
GS["silver"].append([
    say("We are rounding \\(0.06472\\) to 2 significant figures."),
    box("Significant figures start at the first non-zero digit. Write the 2nd significant figure.", 4, "The 1st is 6, the 2nd is 4."),
    box("Write the next digit, the one that decides the rounding.", 7, "It is the digit after the 4.", phase="substitute"),
    box("7 rounds the 4 up. Write the number to 2 significant figures.", 0.065, "4 becomes 5, leading zeros stay.",
        done="0.065 has two significant figures."),
])
GS["silver"].append([
    say("We are rounding \\(3452\\) to 2 significant figures."),
    box("Write the 2nd significant figure of 3452.", 4, "The 1st is 3, the 2nd is 4."),
    box("Write the next digit, the decider.", 5, "It is the 5 in the tens place.", phase="substitute"),
    box("5 rounds up, and zeros hold the place value. Write the number to 2 significant figures.", 3500, "34 becomes 35, then two zeros.",
        done="3500 has two significant figures."),
])
GS["silver"].append([
    say("We are rounding \\(0.8097\\) to 3 significant figures."),
    box("Write the 3rd significant figure of 0.8097.", 9, "The figures are 8, 0, 9."),
    box("Write the next digit, the decider.", 7, "It is the final 7.", phase="substitute",
        say="7 rounds the 9 up, which carries into the 0 before it."),
    box("The 9 rounds up and carries. Write the value to 3 significant figures.", 0.81, "0.809 rounds up to 0.810, which is 0.81.",
        done="0.810 to 3 significant figures equals 0.81."),
])
GS["silver"].append([
    say("We are truncating \\(3.876\\) to 1 decimal place."),
    box("Truncating keeps digits without rounding. Write the digit in the first decimal place.", 8, "It is the first digit after the point."),
    box("Write the next digit. In truncation we ignore it, we never round up.", 7, "It is the second decimal digit.", phase="substitute"),
    box("Chop everything after the first decimal place. Write the result.", 3.8, "Keep 3.8 exactly, no rounding.",
        done="3.876 truncated to 1 decimal place is 3.8."),
])
GS["silver"].append([
    say("We are working out \\(2.4 \\times 0.15\\)."),
    box("Ignore the points and multiply: 24 times 15.", 360, "24 times 15 is 360."),
    box("Count the decimal places: 2.4 has 1 and 0.15 has 2. Write the total.", 3, "1 plus 2 is 3.", phase="substitute"),
    box("Put 3 decimal places into 360, then write it simplified.", 0.36, "0.360 is the same as 0.36.",
        done="2.4 times 0.15 is 0.36."),
])
GS["silver"].append([
    say("We are working out \\(0.48 \\div 0.06\\)."),
    box("Multiply both numbers by 100 to clear the decimals. Write 0.48 times 100.", 48, "0.48 times 100 is 48."),
    box("Write 0.06 times 100.", 6, "0.06 times 100 is 6.", phase="substitute"),
    box("Now divide the whole numbers: 48 divided by 6.", 8, "48 divided by 6 is 8.",
        done="0.48 divided by 0.06 is 8."),
])
GS["silver"].append([
    say("We are rounding \\(49\\,750\\) to 2 significant figures."),
    box("Write the 2nd significant figure of 49750.", 9, "The 1st is 4, the 2nd is 9."),
    box("Write the next digit, the decider.", 7, "It is the 7 in the hundreds place.", phase="substitute",
        say="7 rounds the 9 up, which carries into the 4 in front."),
    box("The 9 rounds up and carries. Keep place value with zeros. Write the number.", 50000, "49 becomes 50, then three zeros.",
        done="49750 to 2 significant figures is 50000."),
])

# gold
GS["gold"].append([
    say("We are estimating \\(\\dfrac{5.1 \\times 19.7}{0.48}\\) by rounding to 1 significant figure."),
    box("Round 5.1 to 1 significant figure.", 5, "5.1 is close to 5."),
    box("Round 19.7 to 1 significant figure.", 20, "19.7 is close to 20."),
    box("Round 0.48 to 1 significant figure. Type it as a decimal.", 0.5, "0.48 is close to 0.5.", phase="substitute"),
    box("Work out the top: 5 times 20.", 100, "5 times 20 is 100."),
    box("Divide by 0.5. Write the estimate.", 200, "Dividing by 0.5 doubles, so 100 becomes 200.",
        done="The estimate is about 200."),
])
GS["gold"].append([
    say("We are estimating \\(\\dfrac{61.3 + 38.9}{0.052}\\) by rounding to 1 significant figure."),
    box("Round 61.3 to 1 significant figure.", 60, "61.3 is close to 60."),
    box("Round 38.9 to 1 significant figure.", 40, "38.9 is close to 40."),
    box("Round 0.052 to 1 significant figure. Type it as a decimal.", 0.05, "0.052 is close to 0.05.", phase="substitute"),
    box("Work out the top: 60 plus 40.", 100, "60 plus 40 is 100."),
    box("Divide by 0.05. Write the estimate.", 2000, "Dividing by 0.05 multiplies by 20, so 100 becomes 2000.",
        done="The estimate is about 2000."),
])
GS["gold"].append([
    say("We are working out \\(0.12^2\\)."),
    box("Ignore the point and multiply: 12 times 12.", 144, "12 times 12 is 144."),
    box("0.12 has 2 decimal places. Squaring adds them: 2 plus 2. Write the number of decimal places.", 4, "Two lots of 2 places make 4.", phase="substitute"),
    box("Put 4 decimal places into 144. Write the answer.", 0.0144, "144 with 4 decimal places is 0.0144.",
        done="0.12 squared is 0.0144."),
])
GS["gold"].append([
    say("We are estimating \\(\\sqrt{62}\\) to 1 decimal place."),
    box("Which whole number squared is just below 62? Try 7: work out 7 times 7.", 49, "7 times 7 is 49."),
    box("Now work out 8 times 8.", 64, "8 times 8 is 64.", phase="substitute"),
    box("62 sits between 49 and 64, close to 64. Using a calculator, write the root of 62 to 1 decimal place.", 7.9, "The root of 62 is 7.874..., which rounds to 7.9.",
        done="The root of 62 is about 7.9."),
])
GS["gold"].append([
    say("A number \\(x\\) truncates to 2 decimal places to give \\(3.47\\). We want the greatest \\(x\\) to 3 decimal places."),
    box("Truncating keeps 3.47 as long as x begins 3.47. Write the smallest such x to 2 decimal places.", 3.47, "The smallest value is 3.47 itself."),
    box("x must stay below the next value up. Write that upper limit to 2 decimal places.", 3.48, "Anything from 3.48 would truncate to 3.48.", phase="substitute"),
    box("The greatest 3 decimal place value below 3.48 is?", 3.479, "3.479 is just under 3.48.",
        done="Any third digit from 0 to 9 keeps 3.47, so 3.479 is greatest."),
])

# -------- attach to bank --------
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        p["hint"] = HINT[tier][i]
        p["misconceptions"] = MIS[tier][i]
        p["guided_steps"] = GS[tier][i]

pd["problem_bank"]["bronze_description"] = "Round to a given number of decimal places or place value, and handle simple decimal calculations."
pd["problem_bank"]["silver_description"] = "Round to significant figures, truncate, and multiply or divide with decimals."
pd["problem_bank"]["gold_description"] = "Estimate calculations by rounding to 1 significant figure, and reason about truncation bounds."

# -------- tier_guides --------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: Rounding to decimal places",
        "steps": [
            "<strong>Find the place</strong> you are keeping and note that digit.",
            "<strong>Look at the next digit</strong> to its right. If it is 5 or more, add 1 to your digit. If it is 4 or less, leave it.",
            "Drop everything after the place you kept, keeping the right number of decimal places even if it ends in a zero.",
        ],
        "example": {
            "question": "Round \\(12.68\\) to 1 decimal place",
            "steps": [
                {"label": "Place to keep", "content": "1 decimal place is the 6 in 12.68."},
                {"label": "Next digit", "content": "The next digit is 8, which is 5 or more, so round up."},
                {"label": "Check", "content": "The 6 becomes 7 and nothing follows."},
                {"label": "Answer", "content": "\\(12.7\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: Significant figures and truncating",
        "steps": [
            "<strong>Significant figures</strong> start at the first non-zero digit. Count that many, then use the next digit to round.",
            "Leading zeros never count, but keep place value: 3452 to 2 s.f. is 3500, not 35.",
            "<strong>Truncating</strong> is different: you just chop off the extra digits and never round up.",
        ],
        "example": {
            "question": "Round \\(0.04617\\) to 2 significant figures",
            "steps": [
                {"label": "First s.f.", "content": "Skip the zeros. The 1st is 4, the 2nd is 6."},
                {"label": "Next digit", "content": "The next digit is 1, which is 4 or less."},
                {"label": "Check", "content": "The 6 stays as 6 and the zeros hold the place."},
                {"label": "Answer", "content": "\\(0.046\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: Estimating with 1 significant figure",
        "steps": [
            "<strong>Round every number to 1 significant figure</strong>, then do the easy calculation.",
            "Dividing by a decimal below 1 makes the answer bigger, so \\(100 \\div 0.5 = 200\\) is meant to look large.",
            "An estimate is a check, not the exact value. Use the \\(\\approx\\) sign.",
        ],
        "example": {
            "question": "Estimate \\(\\dfrac{7.8 \\times 4.1}{0.21}\\)",
            "steps": [
                {"label": "Round to 1 s.f.", "content": "\\(7.8 \\approx 8\\), \\(4.1 \\approx 4\\), \\(0.21 \\approx 0.2\\)."},
                {"label": "Top", "content": "\\(8 \\times 4 = 32\\)."},
                {"label": "Check", "content": "\\(32 \\div 0.2 = 160\\)."},
                {"label": "Answer", "content": "\\(\\approx 160\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# -------- guided (opener + teach) --------
pd["guided"] = {
    "opener": {
        "display": "You are at the till. Your shopping comes to <strong>£6.85</strong>, but the card machine only charges whole pounds.<br>Roughly how many pounds is that?",
        "steps": [
            box("£6.85 is between £6 and £7. Type the nearest whole number of pounds.", 7,
                "0.85 is past halfway, so it is closer to 7."),
            box("Now a bill of £6.40 rounds to which whole pound?", 6,
                "0.40 is below halfway, so it stays at 6."),
            say("You just <strong>rounded to the nearest whole number</strong>. You looked at the part after the point, checked whether it passed halfway (0.5), and bumped up or stayed. Rounding to a decimal place or a significant figure is the same move, aimed at a different column."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "Round \\(5.762\\) to 1 decimal place.",
            "steps": [
                say("Rounding to 1 decimal place means we keep one digit after the point."),
                box("Write the digit in the first decimal place.", 7, "It is the first digit after the point."),
                box("Write the next digit to the right, the decider.", 6, "It is the second decimal digit."),
                box("6 is 5 or more, so the 7 rounds up to?", 8, "7 plus 1 is 8."),
                box("Write the number to 1 decimal place.", 5.8, "The 7 became 8 and the rest is dropped.",
                    done="5.8 is 5.762 rounded to 1 decimal place. Gone."),
            ],
        },
        "silver": {
            "display": "Round \\(0.02384\\) to 2 significant figures.",
            "steps": [
                say("Significant figures start at the first non-zero digit."),
                box("Write the 1st significant figure of 0.02384.", 2, "Skip the leading zeros; the first non-zero digit is 2."),
                box("Write the 2nd significant figure.", 3, "The digit after the 2 is 3."),
                box("Write the next digit, the decider.", 8, "It is the 8 after the 3."),
                box("8 rounds the 3 up. Write the number to 2 significant figures.", 0.024, "3 becomes 4, and the zeros hold the place.",
                    done="0.024 has two significant figures. That was the whole point."),
            ],
        },
        "gold": {
            "display": "Estimate \\(\\dfrac{3.9 \\times 48.2}{0.19}\\) by rounding to 1 significant figure.",
            "steps": [
                say("Round every number to 1 significant figure first."),
                box("Round 3.9 to 1 significant figure.", 4, "3.9 is close to 4."),
                box("Round 48.2 to 1 significant figure.", 50, "48.2 is close to 50."),
                box("Round 0.19 to 1 significant figure. Type it as a decimal.", 0.2, "0.19 is close to 0.2."),
                box("Work out the top: 4 times 50.", 200, "4 times 50 is 200."),
                box("Divide by 0.2. Write the estimate.", 1000, "Dividing by 0.2 multiplies by 5, so 200 becomes 1000.",
                    done="The estimate is about 1000. That is the whole move."),
            ],
        },
    },
}

# -------- method_card (slim) --------
pd["method_card"] = {
    "title": "How to Work with Decimals and Rounding",
    "steps": [
        "Identify the place you are rounding to (decimal places or significant figures).",
        "Look at the next digit to the right.",
        "If it is 5 or more, round the kept digit up by 1; if less than 5, keep it.",
        "Drop the rest, holding place value with zeros before the decimal point.",
    ],
    "content": "<p><strong>Rounding</strong> makes a number simpler to a stated accuracy. Look at the digit just after the place you are keeping: if it is 5 or more, round up; if it is 4 or less, round down.</p><p><strong>Decimal places</strong> count digits after the point. <strong>Significant figures</strong> count from the first non-zero digit; leading zeros never count, but hold place value with zeros (3452 to 2 s.f. is 3500).</p><p><strong>Truncation</strong> chops off digits without rounding. <strong>Estimation</strong> rounds every number to 1 significant figure, then does the easy calculation.</p>",
    "example": "<p><strong>Round 0.04673 to 2 significant figures</strong></p><p><strong>Step 1:</strong> The first significant figure is 4 (ignore leading zeros). The second significant figure is 6.</p><p><strong>Step 2:</strong> Look at the next digit: 7 (5 or more, so round up).</p><p><strong>Step 3:</strong> 6 rounds up to 7.</p><p><strong>Answer:</strong> \\(0.047\\)</p>",
}

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", OUT)
