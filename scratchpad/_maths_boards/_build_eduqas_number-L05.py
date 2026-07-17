# -*- coding: utf-8 -*-
"""Full guided-learning + diagram conversion of maths-eduqas number-L05 (Percentages)."""
import json, io

live = json.load(io.open("_live_L05.json", encoding="utf-8"))

def prob(display, sols, calc, hint, misc, steps):
    return {
        "display": display, "solutions": sols, "calculator": calc,
        "input_type": "single_value", "hint": hint,
        "misconceptions": misc, "guided_steps": steps,
    }

def m(pattern, expect, message, note=None):
    d = {"pattern": pattern, "expect": expect, "message": message}
    if note: d["note"] = note
    return d

# ---------------- BRONZE (non-calculator) ----------------
bronze = [
 prob("Find \\(25\\%\\) of \\(80\\).", [20], False,
   "25% is a quarter, so halve 80 and halve again.",
   [m("divide_by_percent", 3.2, "25% means a quarter (÷4), not 80 ÷ 25. A quarter of 80 is 80 ÷ 4 = 20.")],
   [
    {"say": "25% is one quarter. A quarter means halve, then halve again."},
    {"pre": "Half of 80 = 80 ÷ 2 = ", "post": "", "answer": 40, "hint": "Split 80 in two."},
    {"phase": "substitute", "pre": "Half again (that is a quarter): 40 ÷ 2 = ", "post": "", "answer": 20, "hint": "Halve the 40."},
    {"phase": "substitute", "pre": "Check: four quarters rebuild the whole, 4 × 20 = ", "post": "", "answer": 80,
     "done": "Four lots of 20 make 80, so 25% of 80 is 20.", "hint": "4 × 20."},
   ]),
 prob("Find \\(10\\%\\) of \\(350\\).", [35], False,
   "10% means one tenth, so divide by 10.",
   [m("divide_by_100", 3.5, "Dividing by 100 gives 1% (£3.50). 10% means divide by 10: 350 ÷ 10 = 35.")],
   [
    {"say": "1% is one hundredth. Find that first, then scale up to 10%."},
    {"pre": "1% of 350 = 350 ÷ 100 = ", "post": "", "answer": 3.5, "hint": "Move two places right."},
    {"phase": "substitute", "pre": "10% is ten times 1%: 3.5 × 10 = ", "post": "", "answer": 35, "hint": "Move one place left."},
    {"phase": "substitute", "pre": "Check: ten lots of 10% rebuild the whole, 35 × 10 = ", "post": "", "answer": 350,
     "done": "Ten tenths make 350, so 10% of 350 is 35.", "hint": "Scale back to 100%."},
   ]),
 prob("Find \\(15\\%\\) of \\(60\\).", [9], False,
   "Build 15% from 10% plus 5%.",
   [m("divide_by_percent", 4, "Dividing 60 by 15 gives 4, but that is not 15%. Build it: 10% + 5% = 6 + 3 = 9.")],
   [
    {"say": "15% is 10% plus 5%. Find each block, then add."},
    {"pre": "10% of 60 = 60 ÷ 10 = ", "post": "", "answer": 6, "hint": "Divide by 10."},
    {"phase": "substitute", "pre": "5% is half of 10%: 6 ÷ 2 = ", "post": "", "answer": 3, "hint": "Half of 6."},
    {"phase": "substitute", "pre": "15% = 10% + 5% = 6 + 3 = ", "post": "", "answer": 9,
     "done": "The two blocks add to 9, so 15% of 60 is 9.", "hint": "Add the two parts."},
   ]),
 prob("Find \\(50\\%\\) of \\(130\\).", [65], False,
   "50% is one half, so halve 130.",
   [m("divide_by_percent", 2.6, "50% is a half, not 130 ÷ 50. Half of 130 is 65.")],
   [
    {"say": "50% is one half. Halve, then double-check by rebuilding."},
    {"pre": "Half of 130 = 130 ÷ 2 = ", "post": "", "answer": 65, "hint": "Split 130 in two."},
    {"phase": "substitute", "pre": "Confirm with tenths: 10% of 130 = 13, and 50% = 5 × 13 = ", "post": "", "answer": 65, "hint": "Five lots of 10%."},
    {"phase": "substitute", "pre": "Check: the two halves rebuild the whole, 65 × 2 = ", "post": "", "answer": 130,
     "done": "Both routes give 65 and it doubles back to 130.", "hint": "Two halves make the whole."},
   ]),
 prob("What is \\(12\\) out of \\(48\\) as a percentage?", [25], False,
   "Write it as a fraction, simplify, then turn it into a percentage.",
   [m("forgot_times_100", 0.25, "12 ÷ 48 = 0.25 is the decimal. A percentage is out of 100, so × 100 gives 25%.")],
   [
    {"say": "Write it as a fraction, simplify, then change to a percentage."},
    {"pre": "12/48 simplifies (÷12 top and bottom) to 1/4. As a decimal, 1 ÷ 4 = ", "post": "", "answer": 0.25, "hint": "1 divided by 4."},
    {"phase": "substitute", "pre": "Decimal to percentage: 0.25 × 100 = ", "post": "", "answer": 25, "hint": "Multiply by 100."},
    {"phase": "substitute", "pre": "Check: 25% of 48 = a quarter of 48 = 48 ÷ 4 = ", "post": "", "answer": 12,
     "done": "A quarter of 48 is 12, so 12 out of 48 is 25%.", "hint": "48 ÷ 4."},
   ]),
 prob("What is \\(30\\) out of \\(200\\) as a percentage?", [15], False,
   "Scale the fraction so the bottom becomes 100.",
   [m("forgot_times_100", 0.15, "30 ÷ 200 = 0.15 is the decimal. Multiply by 100 for a percentage: 15%.")],
   [
    {"say": "Percentage means out of 100. Scale 200 down to 100 and do the same to 30."},
    {"pre": "To go from 200 to 100 you halve, so halve the top too: 30 ÷ 2 = ", "post": "", "answer": 15, "hint": "Whatever you do to 200, do to 30."},
    {"phase": "substitute", "pre": "So 30/200 = 15/100. Confirm as a decimal: 30 ÷ 200 = ", "post": "", "answer": 0.15, "hint": "30 divided by 200."},
    {"phase": "substitute", "pre": "Decimal to percentage: 0.15 × 100 = ", "post": "", "answer": 15,
     "done": "30 out of 200 is 15%.", "hint": "Multiply by 100."},
   ]),
 prob("Find \\(20\\%\\) of \\(£55\\).", [11], False,
   "20% is one fifth, so divide by 5.",
   [m("divide_by_percent", 2.75, "Dividing 55 by 20 gives 2.75, but that is not 20%. 20% is a fifth: 55 ÷ 5 = 11.")],
   [
    {"say": "20% is two lots of 10%, which is the same as a fifth."},
    {"pre": "10% of 55 = 55 ÷ 10 = ", "post": "", "answer": 5.5, "hint": "Divide by 10."},
    {"phase": "substitute", "pre": "20% = 2 × 10% = 2 × 5.5 = ", "post": "", "answer": 11, "hint": "Double the 10%."},
    {"phase": "substitute", "pre": "Check: five lots of 20% rebuild the whole, 5 × 11 = ", "post": "", "answer": 55,
     "done": "Five fifths make 55, so 20% of 55 is 11.", "hint": "5 × 20% = 100%."},
   ]),
 prob("What is \\(18\\) out of \\(60\\) as a percentage?", [30], False,
   "Simplify the fraction, then turn it into a percentage.",
   [m("forgot_times_100", 0.3, "18 ÷ 60 = 0.3 is the decimal. Multiply by 100 for a percentage: 30%.")],
   [
    {"say": "Simplify the fraction, then change it to a percentage."},
    {"pre": "18/60 simplifies (÷6 top and bottom) to 3/10. As a decimal, 3 ÷ 10 = ", "post": "", "answer": 0.3, "hint": "3 divided by 10."},
    {"phase": "substitute", "pre": "Decimal to percentage: 0.3 × 100 = ", "post": "", "answer": 30, "hint": "Multiply by 100."},
    {"phase": "substitute", "pre": "Check: 30% of 60 = 3 × 6 = ", "post": "", "answer": 18,
     "done": "30% of 60 is 18, so 18 out of 60 is 30%.", "hint": "10% of 60 is 6, times 3."},
   ]),
]

# ---------------- SILVER (calculator) ----------------
silver = [
 prob("Increase \\(£350\\) by \\(12\\%\\).", [392], True,
   "Multiplier for a 12% increase is 1.12, then multiply.",
   [m("percent_only", 42, "0.12 × 350 = 42 is just the increase, not the new amount. Multiply by 1.12 to keep the original and add the 42: £392.")],
   [
    {"say": "An increase keeps the original 100% and adds 12% on top, so the multiplier is 1 + 0.12."},
    {"pre": "Write the multiplier: 1 + 0.12 = ", "post": "", "answer": 1.12, "hint": "112% as a decimal."},
    {"phase": "substitute", "pre": "Multiply: 350 × 1.12 = £", "post": "", "answer": 392, "hint": "Straight into the calculator."},
    {"phase": "substitute", "pre": "Check: 12% of 350 = 42, and 350 + 42 = £", "post": "", "answer": 392,
     "done": "The original plus the 12% is £392.", "hint": "Add the increase to the original."},
   ]),
 prob("Decrease \\(£480\\) by \\(15\\%\\).", [408], True,
   "A 15% decrease leaves 85%, so multiply by 0.85.",
   [m("percent_only", 72, "0.15 × 480 = 72 is the amount taken off, not the new price. Multiply by 0.85 to keep the 85% that remains: £408.")],
   [
    {"say": "A 15% decrease leaves 100% − 15% = 85%, so the multiplier is 0.85."},
    {"pre": "Write the multiplier: 1 − 0.15 = ", "post": "", "answer": 0.85, "hint": "85% as a decimal."},
    {"phase": "substitute", "pre": "Multiply: 480 × 0.85 = £", "post": "", "answer": 408, "hint": "Into the calculator."},
    {"phase": "substitute", "pre": "Check: 15% of 480 = 72, and 480 − 72 = £", "post": "", "answer": 408,
     "done": "The original minus the 15% is £408.", "hint": "Subtract the discount."},
   ]),
 prob("A laptop was \\(£600\\) and is reduced by \\(30\\%\\). Find the sale price.", [420], True,
   "Reduced by 30% leaves 70%, so multiply by 0.7.",
   [m("percent_only", 180, "£180 is the discount (30% of 600), not the sale price. The sale price keeps 70%: 600 × 0.7 = £420.")],
   [
    {"say": "Taking 30% off leaves 70% to pay, so the multiplier is 0.7."},
    {"pre": "100% − 30% = 70%, as a decimal: ", "post": "", "answer": 0.7, "hint": "70 ÷ 100."},
    {"phase": "substitute", "pre": "Sale price = 600 × 0.7 = £", "post": "", "answer": 420, "hint": "Into the calculator."},
    {"phase": "substitute", "pre": "Check: 30% of 600 = 180, and 600 − 180 = £", "post": "", "answer": 420,
     "done": "The original minus the discount is £420.", "hint": "Take the discount off."},
   ]),
 prob("A population of \\(2500\\) increases by \\(8\\%\\). Find the new population.", [2700], True,
   "Multiplier for an 8% increase is 1.08.",
   [m("percent_only", 200, "200 is the increase (8% of 2500), not the new population. Multiply by 1.08 to include the original: 2700.")],
   [
    {"say": "Growth of 8% means 108% of the start, so the multiplier is 1.08."},
    {"pre": "1 + 0.08 = ", "post": "", "answer": 1.08, "hint": "108% as a decimal."},
    {"phase": "substitute", "pre": "2500 × 1.08 = ", "post": "", "answer": 2700, "hint": "Into the calculator."},
    {"phase": "substitute", "pre": "Check: 8% of 2500 = 200, and 2500 + 200 = ", "post": "", "answer": 2700,
     "done": "The original plus the 8% is 2700.", "hint": "Add the growth."},
   ]),
 prob("Find \\(17.5\\%\\) of \\(£240\\).", [42], True,
   "Multiply 240 by 0.175.",
   [m("no_divide_100", 4200, "17.5% as a decimal is 0.175, not 17.5. 240 × 0.175 = £42, not £4200.")],
   [
    {"say": "17.5% as a decimal is 0.175. Multiply."},
    {"pre": "17.5 ÷ 100 = ", "post": "", "answer": 0.175, "hint": "Move two places right."},
    {"phase": "substitute", "pre": "240 × 0.175 = £", "post": "", "answer": 42, "hint": "Into the calculator."},
    {"phase": "substitute", "pre": "Check by blocks: 10% is 24, 5% is 12, 2.5% is 6, and 24 + 12 + 6 = £", "post": "", "answer": 42,
     "done": "10% + 5% + 2.5% = 17.5%, giving £42.", "hint": "Add 10%, 5% and 2.5%."},
   ]),
 prob("A jacket is \\(£54\\) after a \\(10\\%\\) discount. What was the original price?", [60], True,
   "The £54 is 90% of the original, so divide by 0.9.",
   [m("reverse_wrong_way", 59.4, "Adding 10% to £54 gives £59.40, but 10% of the smaller price is not 10% of the original. The £54 is 90% of the original, so divide: 54 ÷ 0.9 = £60.")],
   [
    {"say": "A 10% discount means £54 is only 90% of the original, so the multiplier used was 0.9."},
    {"pre": "90% as a decimal: 1 − 0.1 = ", "post": "", "answer": 0.9, "hint": "100% − 10%."},
    {"phase": "substitute", "pre": "Reverse by dividing: 54 ÷ 0.9 = £", "post": "", "answer": 60, "hint": "Divide, do not multiply."},
    {"phase": "substitute", "pre": "Check forwards: 10% of 60 = 6, and 60 − 6 = £", "post": "", "answer": 54,
     "done": "Taking 10% off £60 gives £54, so £60 is right.", "hint": "Take 10% off your answer."},
   ]),
 prob("Increase \\(£75\\) by \\(4\\%\\).", [78], True,
   "Multiplier for a 4% increase is 1.04.",
   [m("percent_only", 3, "3 is just the increase (4% of 75), not the new amount. Multiply by 1.04: 75 × 1.04 = £78.")],
   [
    {"say": "Add 4%: the multiplier is 1 + 0.04 = 1.04."},
    {"pre": "1 + 0.04 = ", "post": "", "answer": 1.04, "hint": "104% as a decimal."},
    {"phase": "substitute", "pre": "75 × 1.04 = £", "post": "", "answer": 78, "hint": "Into the calculator."},
    {"phase": "substitute", "pre": "Check: 4% of 75 = 3, and 75 + 3 = £", "post": "", "answer": 78,
     "done": "The original plus the 4% is £78.", "hint": "Add the increase."},
   ]),
]

# ---------------- GOLD (calculator) ----------------
gold = [
 prob("A house is worth \\(£225\\,000\\) after a \\(12.5\\%\\) increase. Find the original value.", [200000], True,
   "£225,000 is 112.5% of the original, so divide by 1.125.",
   [m("reverse_wrong_way", 196875, "Taking 12.5% off £225,000 gives £196,875, but that is not the reverse. The £225,000 is 112.5% of the original, so divide: 225000 ÷ 1.125 = £200,000.")],
   [
    {"say": "A 12.5% increase means £225,000 is 112.5% of the original value."},
    {"pre": "Write that as a multiplier: 1 + 0.125 = ", "post": "", "answer": 1.125, "hint": "112.5% as a decimal."},
    {"phase": "substitute", "pre": "Reverse by dividing: 225000 ÷ 1.125 = £", "post": "", "answer": 200000, "hint": "Divide the new value by the multiplier."},
    {"phase": "substitute", "pre": "Check forwards: 12.5% of 200000 = 25000, and 200000 + 25000 = £", "post": "", "answer": 225000,
     "done": "Adding 12.5% to £200,000 rebuilds £225,000, so the original was £200,000.", "hint": "Add 12.5% to your answer."},
   ]),
 prob("\\(£4000\\) is invested at \\(3\\%\\) compound interest. Find the value after 2 years.", [4243.6], True,
   "Multiply by 1.03 each year, or by 1.03 squared.",
   [m("simple_interest", 4240, "Simple interest adds £120 twice for £4240. Compound interest earns interest on interest: 4000 × 1.03² = £4243.60.")],
   [
    {"say": "Compound means multiply by 1.03 each year. Two years is 1.03 twice, or 1.03²."},
    {"pre": "After year 1: 4000 × 1.03 = £", "post": "", "answer": 4120, "hint": "One year's growth."},
    {"phase": "substitute", "pre": "After year 2: 4120 × 1.03 = £", "post": "", "answer": 4243.6, "hint": "Grow the year-1 amount again."},
    {"phase": "substitute", "pre": "Check with the power: 1.03² = 1.0609, and 4000 × 1.0609 = £", "post": "", "answer": 4243.6,
     "done": "Both routes give £4243.60.", "hint": "4000 × 1.0609."},
   ]),
 prob("A car depreciates by \\(20\\%\\) per year. It is now worth \\(£12\\,800\\). Find its value 3 years ago.", [25000], True,
   "Each year multiplies by 0.8, so three years is × 0.8 cubed. Reverse by dividing.",
   [m("one_year_only", 16000, "12800 ÷ 0.8 undoes only one year, giving £16,000. Three years means dividing by 0.8 three times (÷0.512): £25,000.")],
   [
    {"say": "Losing 20% each year multiplies by 0.8. Over 3 years that is 0.8 × 0.8 × 0.8."},
    {"pre": "0.8 × 0.8 × 0.8 = ", "post": "", "answer": 0.512, "hint": "Cube 0.8."},
    {"phase": "substitute", "pre": "The £12,800 is the old value × 0.512. Reverse by dividing: 12800 ÷ 0.512 = £", "post": "", "answer": 25000, "hint": "Divide by 0.512."},
    {"phase": "substitute", "pre": "Check forwards: 25000 × 0.512 = £", "post": "", "answer": 12800,
     "done": "Depreciating £25,000 by 20% for 3 years gives £12,800.", "hint": "Multiply your answer by 0.512."},
   ]),
 prob("After a \\(5\\%\\) pay rise, Sam earns \\(£27\\,300\\). What was his original salary?", [26000], True,
   "£27,300 is 105% of the original, so divide by 1.05.",
   [m("reverse_wrong_way", 25935, "Taking 5% off £27,300 gives £25,935, but that is not the reverse. The £27,300 is 105% of the old salary, so divide: 27300 ÷ 1.05 = £26,000.")],
   [
    {"say": "A 5% rise means £27,300 is 105% of the old salary."},
    {"pre": "Write the multiplier: 1 + 0.05 = ", "post": "", "answer": 1.05, "hint": "105% as a decimal."},
    {"phase": "substitute", "pre": "Reverse by dividing: 27300 ÷ 1.05 = £", "post": "", "answer": 26000, "hint": "Divide the new salary by 1.05."},
    {"phase": "substitute", "pre": "Check: 5% of 26000 = 1300, and 26000 + 1300 = £", "post": "", "answer": 27300,
     "done": "Adding 5% to £26,000 gives £27,300, so the original was £26,000.", "hint": "Add 5% to your answer."},
   ]),
 prob("\\(£5000\\) earns \\(2.5\\%\\) compound interest. After how many years does it first exceed \\(£5500\\)? Give the number of years.", [4], True,
   "Multiply by 1.025 repeatedly until you pass £5500, then count the years.",
   [m("off_by_one", 3, "After 3 years it is £5384.45, still under £5500. It first passes £5500 in year 4 (£5519.06), so the answer is 4 years.")],
   [
    {"say": "Multiply by 1.025 each year and watch for the first time you pass £5500."},
    {"pre": "After year 1: 5000 × 1.025 = £", "post": "", "answer": 5125, "hint": "One year."},
    {"pre": "After year 2: 5125 × 1.025 = £", "post": "", "answer": 5253.125, "hint": "Grow again."},
    {"phase": "substitute", "pre": "Year 3 gives £5384.45 (still under 5500). After year 4: 5384.45 × 1.025 = £", "post": "", "answer": 5519.06, "hint": "One more year."},
    {"phase": "substitute", "pre": "5519.06 is the first value above 5500, so the number of years is ", "post": "", "answer": 4,
     "done": "Year 3 was £5384.45 (under), year 4 is £5519.06 (over), so 4 years.", "hint": "Count the first year over 5500."},
   ]),
]

# ---------------- tier_guides ----------------
tier_guides = {
 "bronze": {
   "title": "Bronze: a percentage of an amount",
   "steps": [
     "<strong>Percent means out of 100.</strong> To find 10%, divide by 10; to find 1%, divide by 100.",
     "Build any percentage from 10%, 5% and 1% blocks. For 35%: three 10% blocks plus a 5% (half of 10%).",
     "To write one number as a percentage of another, divide them, then multiply by 100.",
   ],
   "example": {
     "question": "Find 15% of 80",
     "steps": [
       {"label": "10%", "content": "80 ÷ 10 = 8"},
       {"label": "5%", "content": "half of 8 = 4"},
       {"label": "Add", "content": "15% = 8 + 4"},
       {"label": "Check", "content": "12 out of 80 is 3 out of 20, which is 15%"},
       {"label": "Answer", "content": "12", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "silver": {
   "title": "Silver: change by a multiplier",
   "steps": [
     "An <strong>increase</strong> of r% multiplies by \\(1 + \\frac{r}{100}\\); a <strong>decrease</strong> multiplies by \\(1 - \\frac{r}{100}\\).",
     "So +12% means ×1.12 and −15% means ×0.85. One multiply does the whole job.",
     "To find the original from a known result, <strong>divide</strong> by that multiplier instead of multiplying.",
   ],
   "example": {
     "question": "Decrease £560 by 15%",
     "steps": [
       {"label": "Multiplier", "content": "1 − 0.15 = 0.85"},
       {"label": "Multiply", "content": "560 × 0.85"},
       {"label": "Check", "content": "15% of 560 = 84, and 560 − 84 = 476"},
       {"label": "Answer", "content": "476", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "gold": {
   "title": "Gold: reverse and compound",
   "steps": [
     "<strong>Reverse:</strong> the result is the original × multiplier, so divide the result by the multiplier to get back.",
     "<strong>Compound:</strong> apply the multiplier once per year. For n years, raise it to the power n.",
     "Growth uses a multiplier above 1; decay (depreciation) uses one below 1, such as 0.8 for losing 20%.",
   ],
   "example": {
     "question": "£84 is a price after a 20% increase. Find the original.",
     "steps": [
       {"label": "Multiplier", "content": "1 + 0.2 = 1.2"},
       {"label": "Reverse", "content": "84 ÷ 1.2 = 70"},
       {"label": "Check", "content": "20% of 70 = 14, and 70 + 14 = 84"},
       {"label": "Answer", "content": "70", "isAnswer": True, "is_answer": True},
     ],
   },
 },
}

# ---------------- guided (opener + teach) ----------------
PRICE_SVG = ('<svg viewBox="0 0 200 110" role="img" aria-label="A sale price tag reading 25% off a £20 T-shirt">'
 '<path d="M20 20 L118 20 L168 55 L118 90 L20 90 Z" fill="#f59e0b" fill-opacity="0.25" stroke="currentColor" stroke-width="1.5"/>'
 '<circle cx="42" cy="55" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/>'
 '<text x="72" y="50" font-family="Inter, sans-serif" font-size="17" fill="currentColor">£20</text>'
 '<text x="66" y="72" font-family="Inter, sans-serif" font-size="12" fill="currentColor">25% OFF</text>'
 '</svg>')

guided = {
 "opener": {
   "steps": [
     {"say": "A £20 T-shirt has 25% off in the sale.<br>" + PRICE_SVG},
     {"pre": "25% is a quarter. A quarter of £20 is 20 ÷ 4 = £", "post": "", "answer": 5,
      "hint": "Split £20 into four equal parts."},
     {"pre": "So you save £5. The price you pay is 20 − 5 = £", "post": "", "answer": 15,
      "hint": "Take the saving off the £20."},
     {"say": "You just found 25% of £20 by taking a quarter, then took it off the price. A percentage is only ever a slice of 100: today you will find that slice, add it on, take it off, and later undo it."},
   ],
 },
 "teach": {
   "bronze": {
     "display": "Find \\(35\\%\\) of \\(60\\)",
     "steps": [
       {"say": "Build 35% from 10% and 5% blocks, then add."},
       {"pre": "10% of 60 = 60 ÷ 10 = ", "post": "", "answer": 6, "hint": "Divide by 10."},
       {"pre": "30% = three 10% blocks = 3 × 6 = ", "post": "", "answer": 18, "hint": "Three lots of 10%."},
       {"pre": "5% is half of 10%: 6 ÷ 2 = ", "post": "", "answer": 3, "hint": "Half of 6."},
       {"pre": "35% = 30% + 5% = 18 + 3 = ", "post": "", "answer": 21,
        "done": "Blocks of 10% and 5% build any percentage. That was the whole point.", "hint": "Add the two blocks."},
     ],
   },
   "silver": {
     "display": "Increase \\(£250\\) by \\(8\\%\\)",
     "steps": [
       {"say": "An increase keeps the original 100% and adds 8% on top."},
       {"pre": "8% as a decimal: 8 ÷ 100 = ", "post": "", "answer": 0.08, "hint": "Two places right."},
       {"pre": "Multiplier for an increase: 1 + 0.08 = ", "post": "", "answer": 1.08, "hint": "100% + 8%."},
       {"pre": "New amount: 250 × 1.08 = £", "post": "", "answer": 270, "hint": "Into the calculator."},
       {"pre": "Check: 8% of 250 = 0.08 × 250 = £", "post": "", "answer": 20,
        "done": "250 + 20 = 270. The single multiplier does both jobs at once.", "hint": "Find the 8% on its own."},
     ],
   },
   "gold": {
     "display": "A price is \\(£84\\) after a \\(20\\%\\) increase. Find the original.",
     "steps": [
       {"say": "The £84 already includes the 20%, so it is 120% of the original."},
       {"pre": "Multiplier for a 20% increase: 1 + 0.2 = ", "post": "", "answer": 1.2, "hint": "120% as a decimal."},
       {"pre": "Reverse by dividing: 84 ÷ 1.2 = £", "post": "", "answer": 70, "hint": "Divide, do not multiply."},
       {"pre": "Check: 20% of 70 = 0.2 × 70 = £", "post": "", "answer": 14, "hint": "Find 20% of your answer."},
       {"pre": "And 70 + 14 = £", "post": "", "answer": 84,
        "done": "Adding 20% to £70 rebuilds £84. Reverse means divide by the multiplier: that is the gold move.", "hint": "Add the increase back."},
     ],
   },
 },
}

# ---------------- method_card (slim) ----------------
method_card = {
  "title": "How to Work with Percentages",
  "steps": [
    "Decide the job: find a %, increase, decrease, reverse, or compound.",
    "Write the multiplier: +15% → ×1.15, −20% → ×0.8.",
    "To reverse, divide by the multiplier instead of multiplying.",
    "For compound, raise the multiplier to the power n.",
  ],
  "content": ("<p><strong>Percentage of an amount:</strong> use a multiplier, or build from 10%, 5% and 1% blocks.</p>"
    "<p><strong>Increase or decrease:</strong> multiplier = \\(1 + \\frac{\\%}{100}\\) or \\(1 - \\frac{\\%}{100}\\).</p>"
    "<p><strong>Reverse:</strong> the result is 100% ± change, so divide by that multiplier.</p>"
    "<p><strong>Compound:</strong> \\(\\text{Final} = \\text{Original} \\times \\text{multiplier}^n\\).</p>"),
  "example": "<p><strong>Increase £350 by 12%</strong></p><p>Multiplier = 1.12</p><p>350 × 1.12 = £392</p>",
}

# ---------------- assemble ----------------
pd = dict(live)  # preserve everything else (topic_links, related_videos, worked_examples)
pd["problem_bank"] = {
  "bronze": bronze,
  "bronze_description": "Find a percentage of an amount, or write one number as a percentage of another, without a calculator.",
  "silver": silver,
  "silver_description": "Increase or decrease an amount by a percentage using a multiplier, and find an original amount from a known result.",
  "gold": gold,
  "gold_description": "Reverse a percentage change to find the original, and use repeated multipliers for compound growth or decay.",
}
pd["tier_guides"] = tier_guides
pd["guided"] = guided
pd["method_card"] = method_card

with io.open("../_maths_guided/lesson_maths-eduqas_number-L05.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
# also mirror into _maths_boards for the board ship-gate naming
with io.open("lesson_maths-eduqas_number-L05.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written. top keys:", list(pd.keys()))
