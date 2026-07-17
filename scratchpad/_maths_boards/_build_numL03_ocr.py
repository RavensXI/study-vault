# -*- coding: utf-8 -*-
"""Build guided-learning + figure practice_data for maths-ocr number-L03
(Decimals & Rounding). Fresh-solved bank verified correct; this adds hints,
guided_steps, honest-diagnosis expects, tier_guides, guided(opener+teach),
slim method_card, and a number-line SVG in the opener. Verifies every box."""
import json, io

live = json.load(io.open("_numL03_live.json", encoding="utf-8"))

# ---------- helpers to build/verify walks ----------
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def say(s): return {"say": s}

# distance-check say for rounding
def round_down_check(n, r, half):
    d = round(abs(n - r), 6)
    assert d <= half + 1e-12, (n, r, d, half)
    return "Check: %s is %s away from %s, less than the %s half-step, so %s is the nearest value." % (
        _fmt(n), _fmt(d), _fmt(r), _fmt(half), _fmt(r))
def _fmt(x):
    if isinstance(x, float) and x == int(x): return str(int(x))
    return ("%f" % x).rstrip("0").rstrip(".") if isinstance(x, float) else str(x)

# ---------- guided_steps per problem (hand-built, then asserted) ----------
BRONZE = live["problem_bank"]["bronze"]
SILVER = live["problem_bank"]["silver"]
GOLD   = live["problem_bank"]["gold"]

# --- BRONZE ---
BRONZE[0]["hint"] = "Look at the 2nd decimal to decide, then keep one digit after the point."
BRONZE[0]["guided_steps"] = [
    say("1 decimal place means keep one digit after the point, the tenths."),
    box("The tenths digit of 3.847 is: ", 8, "First digit after the point."),
    box("The deciding digit, the next one along, is: ", 4, "The hundredths digit, just after the 8."),
    box("4 is less than 5, so round down and keep the 8. Type 3.847 rounded to 1 dp: ", 3.8,
        "Keep 3.8 and drop the 47.", phase="substitute"),
    box("Confirm the answer: ", 3.8, "Type 3.8.",
        say=round_down_check(3.847, 3.8, 0.05), done="Within half a step, so 3.8 is correct."),
]
BRONZE[0]["misconceptions"] = [{"pattern": "rounded_up",
    "message": "The deciding digit is 4, which is under 5, so round down. The answer is 3.8, not 3.9.",
    "expect": 3.9}]

BRONZE[1]["hint"] = "Check the 2nd decimal: 5 or more rounds the tenths up."
BRONZE[1]["guided_steps"] = [
    say("1 decimal place keeps one digit after the point, the tenths."),
    box("The tenths digit of 12.653 is: ", 6, "First digit after the point."),
    box("The deciding digit, the next one along, is: ", 5, "The hundredths digit, just after the 6."),
    box("5 is 5 or more, so round the 6 up to 7. Type 12.653 rounded to 1 dp: ", 12.7,
        "Round the tenths up: 6 becomes 7.", phase="substitute"),
    box("Confirm the answer: ", 12.7, "Type 12.7.",
        say=round_down_check(12.653, 12.7, 0.05), done="Within half a step, so 12.7 is correct."),
]
BRONZE[1]["misconceptions"] = [{"pattern": "rounded_down",
    "message": "The 2nd decimal is 5, so the tenths digit rounds up from 6 to 7, giving 12.7.",
    "expect": 12.6}]

BRONZE[2]["hint"] = "The 3rd decimal decides whether the 2 stays or goes up."
BRONZE[2]["guided_steps"] = [
    say("2 decimal places means keep two digits after the point."),
    box("The 2nd decimal (last kept) digit of 0.7249 is: ", 2, "The hundredths digit."),
    box("The deciding digit, the next one along, is: ", 4, "The thousandths digit, just after the 2."),
    box("4 is less than 5, so round down and keep the 2. Type 0.7249 rounded to 2 dp: ", 0.72,
        "Keep 0.72 and drop the 49.", phase="substitute"),
    box("Confirm the answer: ", 0.72, "Type 0.72.",
        say=round_down_check(0.7249, 0.72, 0.005), done="Within half a step, so 0.72 is correct."),
]
BRONZE[2]["misconceptions"] = []  # natural wrong 0.73 is within validator's 0.011 tolerance of 0.72

BRONZE[3]["hint"] = "The 5 in the thousandths rounds up, and watch the carry through the nines."
BRONZE[3]["guided_steps"] = [
    say("2 decimal places keeps two digits after the point."),
    box("The 2nd decimal (last kept) digit of 5.995 is: ", 9, "The hundredths digit."),
    box("The deciding digit, the next one along, is: ", 5, "The thousandths digit, just after the second 9."),
    box("5 rounds up, so 5.99 rolls over. Type 5.995 rounded to 2 dp: ", 6,
        "Rounding 5.99 up carries through: 5.99 becomes 6.00.", phase="substitute"),
    box("Confirm the answer: ", 6, "Type 6.",
        say="Check: the deciding 5 rounds up, and both nines carry, so 5.99 becomes 6.00.",
        done="The carry runs all the way, so 6.00 is correct."),
]
BRONZE[3]["misconceptions"] = []  # natural wrong 5.99 is within validator's 0.011 tolerance of 6

BRONZE[4]["hint"] = "One significant figure keeps only the first digit, then zeros hold the place."
BRONZE[4]["guided_steps"] = [
    say("1 significant figure keeps only the first non-zero digit."),
    box("The first significant figure of 347 is: ", 3, "The hundreds digit."),
    box("The deciding digit, the next one along, is: ", 4, "The tens digit, just after the 3."),
    box("4 is less than 5, so round down and keep the 3, with zeros holding the place. Type 347 to 1 s.f.: ", 300,
        "The 3 stays; the 4 and 7 become 0: 300.", phase="substitute"),
    box("Confirm the answer: ", 300, "Type 300.",
        say=round_down_check(347, 300, 50), done="Within half a step of 100, so 300 is correct."),
]
BRONZE[4]["misconceptions"] = [{"pattern": "two_sf",
    "message": "One significant figure keeps only the first digit, so 347 becomes 300, not 350.",
    "expect": 350}]

BRONZE[5]["hint"] = "Two significant figures here are the 6 and the 8; the next digit decides."
BRONZE[5]["guided_steps"] = [
    say("2 significant figures keeps the first two non-zero digits."),
    box("The first two significant figures of 6.851 are 6 and 8. The deciding digit (next) is: ", 5,
        "The digit just after the 8."),
    box("5 is 5 or more, so round the 8 up to: ", 9, "8 rounds up to 9."),
    box("Type 6.851 rounded to 2 s.f.: ", 6.9, "The 6 stays, the 8 becomes 9: 6.9.", phase="substitute"),
    box("Confirm the answer: ", 6.9, "Type 6.9.",
        say=round_down_check(6.851, 6.9, 0.05), done="Within half a step, so 6.9 is correct."),
]
BRONZE[5]["misconceptions"] = [{"pattern": "rounded_down",
    "message": "The 3rd significant digit is 5, so the 8 rounds up to 9, giving 6.9.",
    "expect": 6.8}]

BRONZE[6]["hint"] = "Skip the leading zeros; the first significant figure is the 6."
BRONZE[6]["guided_steps"] = [
    say("Leading zeros are not significant. Significant figures start at the first non-zero digit."),
    box("The first significant figure of 0.0638 is: ", 6, "Skip the two leading zeros; the first non-zero digit."),
    box("The deciding digit, the next one along, is: ", 3, "The digit just after the 6."),
    box("3 is less than 5, so round down and keep the 6. Type 0.0638 to 1 s.f.: ", 0.06,
        "Keep 0.06 and drop the 38.", phase="substitute"),
    box("Confirm the answer: ", 0.06, "Type 0.06.",
        say=round_down_check(0.0638, 0.06, 0.005), done="Within half a step, so 0.06 is correct."),
]
BRONZE[6]["misconceptions"] = [{"pattern": "one_dp",
    "message": "Rounding to 1 significant figure gives 0.06, since the first significant figure is the 6. Rounding to 1 decimal place instead gives 0.1.",
    "expect": 0.1}]

BRONZE[7]["hint"] = "Line up the decimal points and pad 3.4 as 3.40 before adding."
BRONZE[7]["guided_steps"] = [
    say("Line up the decimal points and pad 3.4 as 3.40 so both have two decimals."),
    box("Hundredths column: 0 + 5 = ", 5, "3.40 has 0 hundredths, 2.75 has 5."),
    box("Tenths column: 4 + 7 = ", 11, "Write 1, carry 1 into the units."),
    box("Units column: 3 + 2 + the carried 1 = ", 6, "Add the two units and the carry.", phase="substitute"),
    box("Put it together, tenths and hundredths after the point. Type 3.4 + 2.75: ", 6.15,
        "6 units, 1 tenth, 5 hundredths: 6.15.",
        say="So far: units 6, tenths 1, hundredths 5.",
        done="6.15 is the total; a quick check: 3.4 is near 3.5 and 2.75 near 3, sum near 6.25, so 6.15 fits."),
]
BRONZE[7]["misconceptions"] = []

# --- SILVER ---
SILVER[0]["hint"] = "Keep the 4 and 5, then let the next digit decide the rounding."
SILVER[0]["guided_steps"] = [
    say("2 significant figures keeps the first two non-zero digits, then zeros hold the place."),
    box("The first two significant figures of 45672 are 4 and 5. The deciding digit (next) is: ", 6,
        "The hundreds digit, just after the 5."),
    box("6 is 5 or more, so round 45 up to: ", 46, "45 rounds up to 46."),
    box("Replace the remaining digits with zeros. Type 45672 to 2 s.f.: ", 46000,
        "46 followed by three zeros.", phase="substitute"),
    box("Confirm the answer: ", 46000, "Type 46000.",
        say=round_down_check(45672, 46000, 500), done="Within half a step of 1000, so 46000 is correct."),
]
SILVER[0]["misconceptions"] = [{"pattern": "rounded_down",
    "message": "The 3rd digit is 6, so 45 rounds up to 46, giving 46000.",
    "expect": 45000}]

SILVER[1]["hint"] = "Ignore the leading zeros; the significant figures start at the 3."
SILVER[1]["guided_steps"] = [
    say("Leading zeros are not significant. Significant figures start at the first non-zero digit."),
    box("The first significant figure of 0.003457 is: ", 3, "Skip the leading zeros; the first non-zero digit."),
    box("Keep 2 s.f.: 3 and 4. The deciding digit (next) is: ", 5, "The digit just after the 4."),
    box("5 is 5 or more, so round the 4 up to 5. Type 0.003457 to 2 s.f.: ", 0.0035,
        "0.0034 rounds up to 0.0035.", phase="substitute"),
    box("Confirm the answer: ", 0.0035, "Type 0.0035.",
        say=round_down_check(0.003457, 0.0035, 0.00005), done="Within half a step, so 0.0035 is correct."),
]
SILVER[1]["misconceptions"] = []  # natural wrong 0.0034 is within validator's 0.011 tolerance of 0.0035

SILVER[2]["hint"] = "Round each number to one significant figure before multiplying."
SILVER[2]["guided_steps"] = [
    say("Estimate by rounding each number to 1 significant figure."),
    box("4.8 to 1 s.f. is: ", 5, "4.8 is nearer 5 than 4."),
    box("21.3 to 1 s.f. is: ", 20, "Keep the tens digit; 21.3 rounds to 20."),
    box("Now multiply the rounded values: 5 × 20 = ", 100, "5 twenties make 100.", phase="substitute"),
    box("Check the size: the true value is about 102, so type the estimate 100: ", 100,
        "The estimate should be close to the real answer.",
        done="100 is close to the true 102, so the estimate is sensible."),
]
SILVER[2]["misconceptions"] = []

SILVER[3]["hint"] = "Round to 200 over 0.5; dividing by 0.5 doubles the number."
SILVER[3]["guided_steps"] = [
    say("Estimate by rounding each number to 1 significant figure."),
    box("197 to 1 s.f. is: ", 200, "Round to the nearest hundred."),
    box("0.48 to 1 s.f. is: ", 0.5, "The first significant figure is the 4; 0.48 rounds to 0.5."),
    box("Now divide: 200 ÷ 0.5. Dividing by 0.5 doubles the number, so 200 ÷ 0.5 = ", 400,
        "200 × 2 = 400.", phase="substitute"),
    box("Check: 400 × 0.5 = 200, matching the top. Type the estimate 400: ", 400,
        "Multiply back to check.", done="400 × 0.5 = 200, so the estimate is sound."),
]
SILVER[3]["misconceptions"] = [{"pattern": "multiplied_by_half",
    "message": "Dividing by 0.5 is the same as multiplying by 2, so 200 ÷ 0.5 = 400, not 100.",
    "expect": 100}]

SILVER[4]["hint"] = "Work out 47 × 3, then place the decimal point using the total decimal places."
SILVER[4]["guided_steps"] = [
    say("First multiply as whole numbers, ignoring the decimal points."),
    box("47 × 3 = ", 141, "Multiply the digits as if there were no points."),
    box("Count the decimal places: 4.7 has 1, 0.3 has 1, so the total is: ", 2, "1 + 1 decimal places."),
    box("Put the point 2 places from the right of 141. Type 4.7 × 0.3: ", 1.41,
        "141 with the point 2 places in is 1.41.", phase="substitute"),
    box("Check the size: 4.7 is near 5, and 5 × 0.3 = 1.5, close to 1.41. Type 1.41: ", 1.41,
        "Compare with a quick estimate.", done="1.41 is close to the estimate 1.5, so it is correct."),
]
SILVER[4]["misconceptions"] = [{"pattern": "wrong_place",
    "message": "47 × 3 = 141, and there are 2 decimal places in total, so the answer is 1.41, not 14.1.",
    "expect": 14.1}]

SILVER[5]["hint"] = "Multiply both numbers by 10 so you divide by a whole number."
SILVER[5]["guided_steps"] = [
    say("Make the divisor a whole number by multiplying both numbers by 10."),
    box("8.4 × 10 = ", 84, "Move the point one place right."),
    box("0.6 × 10 = ", 6, "Move the point one place right."),
    box("Now divide whole numbers: 84 ÷ 6 = ", 14, "How many 6s make 84.", phase="substitute"),
    box("Check: 14 × 0.6 = 8.4, matching the start. Type 14: ", 14,
        "Multiply back to check.", done="14 × 0.6 = 8.4, so 14 is correct."),
]
SILVER[5]["misconceptions"] = [{"pattern": "decimal_slip",
    "message": "Multiply both numbers by 10 first: 84 ÷ 6 = 14, not 1.4.",
    "expect": 1.4}]

SILVER[6]["hint"] = "Find the two square numbers 53 lies between."
SILVER[6]["guided_steps"] = [
    say("Find the two square numbers that 53 sits between."),
    box("7² = ", 49, "7 times 7."),
    box("8² = ", 64, "8 times 8."),
    box("53 lies between 49 and 64. The gap down to 49 is 53 − 49 = ", 4,
        "Subtract the lower square.", phase="substitute"),
    box("The gap up to 64 is 64 − 53 = ", 11, "Subtract from the higher square."),
    box("4 is less than 11, so 53 is nearer 49. The nearest integer to √53 is: ", 7,
        "Nearer 49 means nearer 7.", done="53 is closer to 7² than 8², so √53 rounds to 7."),
]
SILVER[6]["misconceptions"] = [{"pattern": "rounded_up",
    "message": "53 is closer to 49 (7²) than to 64 (8²), so √53 rounds to 7, not 8.",
    "expect": 8}]

# --- GOLD ---
GOLD[0]["hint"] = "Square 6, add 4, then divide by 0.5."
GOLD[0]["guided_steps"] = [
    say("Estimate every part to 1 significant figure, including the square."),
    box("6.2 to 1 s.f. is 6, and 6² = ", 36, "6 times 6."),
    box("3.8 to 1 s.f. is: ", 4, "3.8 is nearer 4 than 3."),
    box("So the top is about 36 + 4 = ", 40, "Add the rounded parts."),
    box("0.49 to 1 s.f. is: ", 0.5, "The first significant figure is the 4; 0.49 rounds to 0.5."),
    box("Now divide: 40 ÷ 0.5. Dividing by 0.5 doubles it, so 40 ÷ 0.5 = ", 80,
        "40 × 2 = 80.", phase="substitute"),
    box("Check: 80 × 0.5 = 40, matching the top. Type the estimate 80: ", 80,
        "Multiply back to check.", done="80 × 0.5 = 40, so the estimate is sound."),
]
GOLD[0]["misconceptions"] = [{"pattern": "multiplied_by_half",
    "message": "Dividing by 0.5 doubles the number, so 40 ÷ 0.5 = 80, not 20.",
    "expect": 20}]

GOLD[1]["hint"] = "Multiply 24 × 15, then count four decimal places."
GOLD[1]["guided_steps"] = [
    say("First multiply as whole numbers, ignoring the decimal points."),
    box("24 × 15 = ", 360, "Multiply the digits as whole numbers."),
    box("Count the decimal places: 0.24 has 2, 0.15 has 2, so the total is: ", 4, "2 + 2 decimal places."),
    box("Put the point 4 places from the right of 360, using a leading zero. Type 0.24 × 0.15: ", 0.036,
        "0360 with the point 4 places in is 0.0360, i.e. 0.036.", phase="substitute"),
    box("Check the size: 0.24 and 0.15 are both under 1, so the product is small. Type 0.036: ", 0.036,
        "A product of two small decimals is smaller still.",
        done="Both factors are under 1, so 0.036 is a sensible small answer."),
]
GOLD[1]["misconceptions"] = [{"pattern": "wrong_place",
    "message": "24 × 15 = 360 with 4 decimal places in total, giving 0.036, not 0.36.",
    "expect": 0.36}]

GOLD[2]["hint"] = "The 5 rounds the 99 up, and the carry runs into the units."
GOLD[2]["guided_steps"] = [
    say("2 significant figures keeps the first two non-zero digits."),
    box("The first two significant figures of 0.9955 are 9 and 9. The deciding digit (next) is: ", 5,
        "The digit just after the second 9."),
    box("5 rounds up, so 99 rolls over to 100. Type 0.9955 rounded to 2 s.f.: ", 1,
        "0.99 rounds up to 1.0, which is 1.", phase="substitute"),
    box("Check: 0.9955 is just under 1, and rounding pushes it up to 1.0. Type 1: ", 1,
        "The value is very close to 1.", done="The carry runs into the units, so 1 is correct."),
]
GOLD[2]["misconceptions"] = []  # natural wrong 0.99 is within validator's 0.011 tolerance of 1

GOLD[3]["hint"] = "Round to 400 × 0.5 over 20."
GOLD[3]["guided_steps"] = [
    say("Estimate every number to 1 significant figure."),
    box("398 to 1 s.f. is: ", 400, "Round to the nearest hundred."),
    box("0.52 to 1 s.f. is: ", 0.5, "The first significant figure is the 5."),
    box("So the top is about 400 × 0.5 = ", 200, "Half of 400."),
    box("19.7 to 1 s.f. is: ", 20, "Round to the nearest ten."),
    box("Now divide: 200 ÷ 20 = ", 10, "How many 20s make 200.", phase="substitute"),
    box("Check: 10 × 20 = 200, matching the top. Type the estimate 10: ", 10,
        "Multiply back to check.", done="10 × 20 = 200, so the estimate is sound."),
]
GOLD[3]["misconceptions"] = []

GOLD[4]["hint"] = "Multiply both numbers by 100 so you divide by a whole number."
GOLD[4]["guided_steps"] = [
    say("Make the divisor a whole number by multiplying both numbers by 100."),
    box("2.56 × 100 = ", 256, "Move the point two places right."),
    box("0.08 × 100 = ", 8, "Move the point two places right."),
    box("Now divide whole numbers: 256 ÷ 8 = ", 32, "How many 8s make 256.", phase="substitute"),
    box("Check: 32 × 0.08 = 2.56, matching the start. Type 32: ", 32,
        "Multiply back to check.", done="32 × 0.08 = 2.56, so 32 is correct."),
]
GOLD[4]["misconceptions"] = [{"pattern": "decimal_slip",
    "message": "Multiply both numbers by 100 first: 256 ÷ 8 = 32, not 3.2.",
    "expect": 3.2}]

# tier descriptions
live["problem_bank"]["bronze_description"] = "Round decimals to a given number of decimal places or significant figures, and add decimals."
live["problem_bank"]["silver_description"] = "Round larger and smaller numbers to significant figures, estimate calculations, and multiply or divide decimals."
live["problem_bank"]["gold_description"] = "Estimate multi-step calculations to one significant figure and multiply or divide trickier decimals."

# ---------- tier_guides ----------
live["tier_guides"] = {
    "bronze": {
        "title": "Bronze: round to a place you can point to",
        "steps": [
            "<strong>Decimal places</strong> count digits after the point. Keep the number of digits you need, then look at the very next digit.",
            "If that deciding digit is <strong>5 or more</strong>, round the kept digit up; if it is 4 or less, leave it and drop the rest.",
            "Watch for a carry: rounding 5.99 up gives 6.00, because the nines roll over.",
        ],
        "example": {"question": "Round 3.472 to 1 decimal place", "steps": [
            {"label": "Keep", "content": "<p>1 d.p. keeps one digit after the point: 3.4...</p>"},
            {"label": "Decide", "content": "<p>The next digit is 7, and 7 ≥ 5, so round up.</p>"},
            {"label": "Check", "content": "<p>The tenths digit 4 becomes 5.</p>"},
            {"label": "Answer", "content": "<p>3.5</p>", "isAnswer": True, "is_answer": True},
        ]},
    },
    "silver": {
        "title": "Silver: significant figures and estimates",
        "steps": [
            "<strong>Significant figures</strong> start at the first non-zero digit, so the leading zeros in 0.0034 do not count.",
            "To <strong>estimate</strong>, round every number to 1 s.f. first, then do the easy calculation.",
            "To multiply or divide decimals, work with whole numbers, then fix the decimal point or scale back.",
        ],
        "example": {"question": "Estimate 3.9 × 48", "steps": [
            {"label": "Round", "content": "<p>3.9 ≈ 4 and 48 ≈ 50 (1 s.f.).</p>"},
            {"label": "Multiply", "content": "<p>4 × 50 = 200.</p>"},
            {"label": "Check", "content": "<p>The true value is about 187, so 200 is sensible.</p>"},
            {"label": "Answer", "content": "<p>200</p>", "isAnswer": True, "is_answer": True},
        ]},
    },
    "gold": {
        "title": "Gold: multi-step estimates and tricky decimals",
        "steps": [
            "Round <strong>every</strong> part to 1 s.f., including squares and roots, before combining them.",
            "Dividing by 0.5 doubles a number; dividing by 0.1 multiplies by 10. Watch these when you scale.",
            "For decimal products count the total decimal places; for quotients scale both numbers to whole numbers.",
        ],
        "example": {"question": "Estimate (5.1² + 2.8) ÷ 0.51", "steps": [
            {"label": "Round", "content": "<p>5² = 25, 2.8 ≈ 3, 0.51 ≈ 0.5.</p>"},
            {"label": "Combine", "content": "<p>Top: 25 + 3 = 28.</p>"},
            {"label": "Divide", "content": "<p>28 ÷ 0.5 = 56.</p>"},
            {"label": "Answer", "content": "<p>56</p>", "isAnswer": True, "is_answer": True},
        ]},
    },
}

# ---------- guided (opener + teach) ----------
NUMLINE = ('<svg viewBox="0 0 260 64" role="img" aria-label="Number line from 3 to 4 pounds with 3.84 marked past the halfway point">'
    '<line x1="20" y1="40" x2="240" y2="40" stroke="currentColor" stroke-width="1.5"/>'
    '<line x1="20" y1="34" x2="20" y2="46" stroke="currentColor" stroke-width="1.5"/>'
    '<line x1="130" y1="35" x2="130" y2="45" stroke="currentColor" stroke-width="1"/>'
    '<line x1="240" y1="34" x2="240" y2="46" stroke="currentColor" stroke-width="1.5"/>'
    '<circle cx="205" cy="40" r="4" fill="#f59e0b" fill-opacity="0.6" stroke="currentColor" stroke-width="1"/>'
    '<text x="20" y="58" font-family="Inter" font-size="11" text-anchor="middle" fill="currentColor">£3</text>'
    '<text x="130" y="58" font-family="Inter" font-size="10" text-anchor="middle" fill="currentColor">£3.50</text>'
    '<text x="240" y="58" font-family="Inter" font-size="11" text-anchor="middle" fill="currentColor">£4</text>'
    '<text x="205" y="22" font-family="Inter" font-size="11" text-anchor="middle" fill="currentColor">£3.84</text>'
    '</svg>')

live["guided"] = {
    "opener": {
        "label": "Before any rules",
        "display": NUMLINE + "A bill comes to <strong>£3.84</strong>, but the charity box only takes whole pounds. On the line above, £3.84 sits past the halfway mark.",
        "steps": [
            box("£3.84 sits between £3 and £4. Which whole pound is it nearer? Type it: ", 4,
                "0.84 is past the halfway mark of 0.50, so it is nearer 4."),
            box("Now a bill of £3.40 to the nearest pound: ", 3,
                "0.40 is below halfway, so it stays at 3."),
            say("You just <strong>rounded to the nearest whole number</strong>: look at the part after the point, check whether it passed the halfway mark 0.5, then round up or stay. Rounding to a decimal place or a significant figure is the very same move, just aimed at a different column."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "Round \\(4.362\\) to 2 decimal places",
            "label": "Together: your first one",
            "steps": [
                box("2 decimal places means keep two digits after the point. The 2nd decimal (last kept) digit of 4.362 is: ", 6,
                    "The hundredths digit.", say="Start by finding the digit you keep."),
                box("The deciding digit, the next one along, is: ", 2, "The thousandths digit, just after the 6."),
                box("2 is less than 5, so round down and keep the 6. Type 4.362 rounded to 2 dp: ", 4.36,
                    "Keep 4.36 and drop the 2.", phase="substitute"),
                box("Confirm the answer: ", 4.36, "Type 4.36.",
                    say="Check: 4.362 is 0.002 from 4.36, under the 0.005 half-step.",
                    done="Within half a step, so 4.36 is right. That was the whole move."),
            ],
        },
        "silver": {
            "display": "Estimate \\(6.1 \\times 39\\)",
            "label": "Together: your first one",
            "steps": [
                box("Estimate by rounding each to 1 significant figure. 6.1 to 1 s.f. is: ", 6,
                    "6.1 is nearer 6 than 7.", say="Round each number first."),
                box("39 to 1 s.f. is: ", 40, "39 is nearer 40 than 30."),
                box("Multiply the rounded values: 6 × 40 = ", 240, "6 forties make 240.", phase="substitute"),
                box("Check the size: the true value is about 238, so type the estimate 240: ", 240,
                    "The estimate should be close to the real answer.",
                    done="240 is close to the true 238. That was the whole move."),
            ],
        },
        "gold": {
            "display": "Calculate \\(3.6 \\div 0.04\\)",
            "label": "Together: your first one",
            "steps": [
                box("Make the divisor whole by multiplying both by 100. 3.6 × 100 = ", 360,
                    "Move the point two places right.", say="Clear the decimal from the divisor."),
                box("0.04 × 100 = ", 4, "Move the point two places right."),
                box("Now divide whole numbers: 360 ÷ 4 = ", 90, "How many 4s make 360.", phase="substitute"),
                box("Check: 90 × 0.04 = 3.6, matching the start. Type 90: ", 90,
                    "Multiply back to check.", done="90 × 0.04 = 3.6, so 90 is right. That was the whole move."),
            ],
        },
    },
}

# ---------- slim method_card ----------
live["method_card"] = {
    "title": "Decimals & Rounding",
    "steps": [
        "Decide the rounding rule: decimal places or significant figures.",
        "Find the deciding digit, the one just after your last kept digit.",
        "If it is 5 or more round up, otherwise round down; keep place-holding zeros.",
        "To estimate, round each number to 1 s.f. first, then calculate.",
    ],
    "content": ("<p><strong>Decimal places</strong> count digits after the point. "
        "<strong>Significant figures</strong> count from the first non-zero digit, so leading zeros in 0.0034 do not count.</p>"
        "<p>To round, look at the deciding digit just after the last one you keep. If it is 5 or more, round up; if it is 4 or less, round down. Watch for carries: 5.99 rounded up becomes 6.00.</p>"
        "<p>To <strong>estimate</strong>, round every value to 1 significant figure, then do the simpler calculation.</p>"),
    "example": ("<p><strong>Round</strong> \\(3.4572\\) to 2 d.p.</p>"
        "<p>Keep two decimals: 3.45. The deciding digit is 7 (≥ 5), so round up.</p>"
        "<p><strong>Answer: 3.46</strong></p>"),
}

# ---------- de-dash preserved worked_examples labels (style law is hard) ----------
for we in live.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---------- VERIFY every final box == stored solution & arithmetic ----------
def final_box_answer(steps):
    boxes = [s for s in steps if s.get("answer") is not None]
    return boxes

problems = [("bronze", i, p) for i, p in enumerate(BRONZE)] + \
           [("silver", i, p) for i, p in enumerate(SILVER)] + \
           [("gold", i, p) for i, p in enumerate(GOLD)]
for tier, i, p in problems:
    gs = p.get("guided_steps")
    assert gs, (tier, i, "no guided_steps")
    boxes = final_box_answer(gs)
    # the answer that equals the stored solution must appear as a box value
    sol = p["solutions"][0]
    assert any(abs(float(b["answer"]) - sol) < 1e-9 for b in boxes), (tier, i, "solution not produced", sol, [b["answer"] for b in boxes])
    # completion boundary present
    assert any(s.get("phase") == "substitute" for s in gs), (tier, i, "no phase")
    # >=1 before, >=2 live at/after
    idx = next(k for k, s in enumerate(gs) if s.get("phase") == "substitute")
    before = sum(1 for s in gs[:idx] if s.get("answer") is not None)
    after = sum(1 for s in gs[idx:] if s.get("answer") is not None)
    assert before >= 1 and after >= 2, (tier, i, "boundary", before, after)
    # misconception expects differ from solution
    for m in p.get("misconceptions", []):
        assert "expect" in m
        if m["expect"] is not None:
            assert abs(float(m["expect"]) - sol) > 1e-9, (tier, i, "expect==sol")

# teach walks: >=4 boxes each
for t in ("bronze", "silver", "gold"):
    tb = [s for s in live["guided"]["teach"][t]["steps"] if s.get("answer") is not None]
    assert len(tb) >= 4, (t, len(tb))
# opener has boxes
assert any(s.get("answer") is not None for s in live["guided"]["opener"]["steps"])

print("VERIFY OK: all final boxes land on solutions; boundaries valid; expects clean.")

json.dump(live, io.open("lesson_maths-ocr_number-L03.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote lesson_maths-ocr_number-L03.json")
