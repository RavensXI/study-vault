# -*- coding: utf-8 -*-
import json, io

KEY = "ratio-proportion-L02"
BOARD = "maths-aqa"
DIR = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"

live = json.load(io.open(DIR + "_live_l02.json", encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

def mc(pattern, expect, message):
    return {"pattern": pattern, "expect": expect, "message": message}

# ---------------- BRONZE ----------------
bronze = [
 {  # 0
  "display": "Find 25% of £80.",
  "solutions": [20], "calculator": False, "input_type": "single_value",
  "hint": "Turn 25% into 0.25, then multiply by 80.",
  "misconceptions": [
    mc("decimal_place", 2, "25% is 0.25, not 0.025. 0.25 × 80 = 20, not 2."),
  ],
  "guided_steps": [
    sayonly("'Percent' means out of 100, so first write 25% as a decimal."),
    box("25 ÷ 100 = ", 0.25, "Two places: 25% becomes 0.25."),
    box("'Of' means multiply. 0.25 × 80 = ", 20, "A quarter of 80.", phase="substitute"),
    box("Check: a quarter of 80, so 4 × 20 = ", 80, "Multiply your answer by 4.", done="Back to 80, so 20 is right."),
  ],
 },
 {  # 1
  "display": "Find 10% of 350.",
  "solutions": [35], "calculator": False, "input_type": "single_value",
  "hint": "10% means divide by 10.",
  "misconceptions": [
    mc("div_100", 3.5, "10% means divide by 10, not 100. 350 ÷ 10 = 35."),
  ],
  "guided_steps": [
    sayonly("10% is one tenth. Write it as a decimal first."),
    box("10 ÷ 100 = ", 0.1, "10% becomes 0.1."),
    box("0.1 × 350 = ", 35, "One tenth of 350.", phase="substitute"),
    box("Check: ten lots of 35 is 10 × 35 = ", 350, "Multiply your answer by 10.", done="That rebuilds 350, so 35 is a tenth."),
  ],
 },
 {  # 2
  "display": "Increase £60 by 20%.",
  "solutions": [72], "calculator": False, "input_type": "single_value",
  "hint": "Find 20% of 60 and add it on, or multiply by 1.2.",
  "misconceptions": [
    mc("increase_only", 12, "12 is the increase, not the new amount. Add it on: 60 + 12 = 72."),
  ],
  "guided_steps": [
    sayonly("Increasing keeps the whole £60 and adds 20% on top."),
    box("20% of 60: 0.2 × 60 = ", 12, "0.2 × 60."),
    box("Add it on: 60 + 12 = ", 72, "New amount is the old plus the extra.", phase="substitute"),
    box("Faster check: 60 × 1.2 = ", 72, "Paying 120% is the multiplier 1.2.", done="The multiplier 1.2 gives the same £72."),
  ],
 },
 {  # 3
  "display": "Decrease 200 by 15%.",
  "solutions": [170], "calculator": False, "input_type": "single_value",
  "hint": "Find 15% of 200 and take it off, or multiply by 0.85.",
  "misconceptions": [
    mc("decrease_only", 30, "30 is the amount taken off, not the new value. 200 − 30 = 170."),
  ],
  "guided_steps": [
    sayonly("Decreasing takes 15% away from the whole 200."),
    box("15% of 200: 0.15 × 200 = ", 30, "0.15 × 200."),
    box("Take it off: 200 − 30 = ", 170, "New value is the old minus the slice.", phase="substitute"),
    box("Faster check: 200 × 0.85 = ", 170, "Keeping 85% is the multiplier 0.85.", done="The multiplier 0.85 gives the same 170."),
  ],
 },
 {  # 4
  "display": "What is the decimal multiplier for a 30% increase?",
  "solutions": [1.3], "calculator": False, "input_type": "single_value",
  "hint": "An increase adds to 1: think 1 plus the decimal.",
  "misconceptions": [
    mc("forgot_the_one", 0.3, "0.3 finds 30% OF an amount. To INCREASE you keep the whole (1) and add: 1 + 0.3 = 1.3."),
  ],
  "guided_steps": [
    sayonly("An increase keeps all of the original (that is 1 whole) and adds more."),
    box("Write 30% as a decimal: 30 ÷ 100 = ", 0.3, "30% becomes 0.3."),
    box("Increase means add to 1: 1 + 0.3 = ", 1.3, "Start from 1 whole, then add the extra.", phase="substitute"),
    box("Check on £10: 10 × 1.3 = ", 13, "Multiply a test amount.", done="£13 is £10 plus 30% (£3). The multiplier works."),
  ],
 },
 {  # 5
  "display": "What is the decimal multiplier for a 5% decrease?",
  "solutions": [0.95], "calculator": False, "input_type": "single_value",
  "hint": "A decrease takes the decimal off 1.",
  "misconceptions": [
    mc("five_as_half", 0.5, "5% is 0.05, not 0.5. 1 − 0.05 = 0.95."),
  ],
  "guided_steps": [
    sayonly("A decrease keeps most of the original and takes a slice off the 1 whole."),
    box("Write 5% as a decimal: 5 ÷ 100 = ", 0.05, "5% becomes 0.05."),
    box("Decrease means take it off 1: 1 − 0.05 = ", 0.95, "Start from 1 whole, then subtract.", phase="substitute"),
    box("Check on £200: 200 × 0.95 = ", 190, "Multiply a test amount.", done="£190 is £200 minus 5% (£10). Correct."),
  ],
 },
 {  # 6
  "display": "A shirt costs £40. It is reduced by 10%. What is the sale price?",
  "solutions": [36], "calculator": False, "input_type": "single_value",
  "hint": "Multiply by 0.9 to pay 90% of the price.",
  "misconceptions": [
    mc("discount_only", 4, "£4 is the discount, not the price you pay. Sale price = 40 − 4 = 36."),
  ],
  "guided_steps": [
    sayonly("A 10% reduction takes one tenth off the £40."),
    box("10% of 40: 0.1 × 40 = ", 4, "One tenth of 40."),
    box("Sale price: 40 − 4 = ", 36, "Take the discount off.", phase="substitute"),
    box("Faster check: 40 × 0.9 = ", 36, "Paying 90% is the multiplier 0.9.", done="Paying 90% gives the same £36."),
  ],
 },
 {  # 7
  "display": "Find 50% of 84.",
  "solutions": [42], "calculator": False, "input_type": "single_value",
  "hint": "50% is just half.",
  "misconceptions": [],
  "guided_steps": [
    sayonly("50% is one half."),
    box("Write 50% as a decimal: 50 ÷ 100 = ", 0.5, "50% becomes 0.5."),
    box("0.5 × 84 = ", 42, "Half of 84.", phase="substitute"),
    box("Check: two halves rebuild it, 42 + 42 = ", 84, "Add your answer to itself.", done="Two halves make 84, so 42 is half."),
  ],
 },
]

# ---------------- SILVER ----------------
silver = [
 {  # 0
  "display": "£2000 earns 5% simple interest per year. How much interest after 3 years?",
  "solutions": [300], "calculator": False, "input_type": "single_value",
  "hint": "Simple interest is the same each year: find one year, then times by 3.",
  "misconceptions": [
    mc("gave_total", 2300, "£2300 is the total in the account. The question asks for the interest only: £300."),
    mc("one_year", 100, "£100 is one year's interest. Over 3 years: 3 × 100 = 300."),
  ],
  "guided_steps": [
    sayonly("Simple interest pays the same amount every year, worked out on the starting £2000."),
    box("One year: 5% of 2000 = 0.05 × 2000 = ", 100, "5% is 0.05."),
    box("Three years, same each time: 3 × 100 = ", 300, "Multiply one year by the number of years.", phase="substitute"),
    box("Check the total: 2000 + 300 = ", 2300, "Add the interest to the start.", done="The £300 is the interest earned, which is what was asked."),
  ],
 },
 {  # 1
  "display": "A house bought for £200000 increases in value by 10% per year (compound). What is it worth after 2 years?",
  "solutions": [242000], "calculator": True, "input_type": "single_value",
  "hint": "Multiply by 1.1 twice, once for each year.",
  "misconceptions": [
    mc("added_20pc", 240000, "Two years of 10% compound is not the same as 20% once. 200000 × 1.1² = 242000, not 240000."),
    mc("one_year", 220000, "£220000 is the value after 1 year. Apply the 1.1 again: 220000 × 1.1 = 242000."),
  ],
  "guided_steps": [
    sayonly("Compound means each year grows on the NEW value, not the start."),
    box("Multiplier for a 10% rise: 1 + 0.1 = ", 1.1, "1 whole plus 0.1."),
    box("After year 1: 200000 × 1.1 = ", 220000, "Apply the multiplier once."),
    box("After year 2: 220000 × 1.1 = ", 242000, "Apply it again to the new value.", phase="substitute"),
    box("Check with a power: 200000 × 1.1² = 200000 × 1.21 = ", 242000, "1.1 squared is 1.21.", done="Both routes agree: £242000."),
  ],
 },
 {  # 2
  "display": "After a 20% increase, a price is £96. What was the original price?",
  "solutions": [80], "calculator": False, "input_type": "single_value",
  "hint": "The £96 is 120% of the original, so divide by 1.2.",
  "misconceptions": [
    mc("subtract_from_new", 76.8, "You cannot just take 20% off the new price. The £96 is 120% of the original, so divide by 1.2: 96 ÷ 1.2 = 80."),
  ],
  "guided_steps": [
    sayonly("The £96 already INCLUDES the 20% rise, so it is 120% of the original."),
    box("Multiplier that was used: 1 + 0.2 = ", 1.2, "1 whole plus 0.2."),
    box("Reverse it by dividing: 96 ÷ 1.2 = ", 80, "To undo a multiply, divide.", phase="substitute"),
    box("Check forwards: 80 × 1.2 = ", 96, "Multiply back up.", done="Back to £96, so £80 is right."),
  ],
 },
 {  # 3
  "display": "A car was £15000 new. It is now worth £9600. What percentage has it decreased by?",
  "solutions": [36], "calculator": True, "input_type": "single_value",
  "hint": "Divide the amount lost by the original price, then times 100.",
  "misconceptions": [
    mc("base_is_new", 56.25, "Percentage change is always out of the ORIGINAL: 5400 ÷ 15000 × 100 = 36, not out of 9600."),
    mc("remaining_pc", 64, "64% is what it is still worth. The DECREASE is 100 − 64 = 36."),
  ],
  "guided_steps": [
    sayonly("Percentage change is always measured against the ORIGINAL price."),
    box("Amount lost: 15000 − 9600 = ", 5400, "The drop in value."),
    box("As a percentage of the start: (5400 ÷ 15000) × 100 = ", 36, "Divide by the original, then × 100.", phase="substitute"),
    box("Check: 36% of 15000 = 0.36 × 15000 = ", 5400, "Multiply the original by 0.36.", done="That matches the £5400 lost, so 36% is right."),
  ],
 },
 {  # 4
  "display": "A population of 5000 grows by 2% each year (compound). Find the population after 3 years. Give to the nearest whole number.",
  "solutions": [5306], "calculator": True, "input_type": "single_value",
  "hint": "Multiply by 1.02 three times, or use 1.02 to the power 3.",
  "misconceptions": [
    mc("added_6pc", 5300, "Adding 2% three times to the start gives 5000 × 1.06 = 5300. Compound grows on the new total: 5000 × 1.02³ = 5306."),
  ],
  "guided_steps": [
    sayonly("Each year the population grows on the previous year's total."),
    box("Multiplier for a 2% rise: 1 + 0.02 = ", 1.02, "1 whole plus 0.02."),
    box("Year 1: 5000 × 1.02 = ", 5100, "Apply the multiplier once."),
    box("Year 2: 5100 × 1.02 = ", 5202, "Apply it to the new total."),
    box("Year 3: 5202 × 1.02 = ", 5306.04, "Apply it once more.", phase="substitute"),
    box("To the nearest whole number: ", 5306, "Round 5306.04.", done="5306 people."),
    box("Check with a power: 5000 × 1.02³ = ", 5306.04, "1.02 to the power 3, then × 5000.", done="Same value, so 5306 is right."),
  ],
 },
 {  # 5
  "display": "VAT is 20%. An item costs £84 including VAT. What was the price before VAT?",
  "solutions": [70], "calculator": False, "input_type": "single_value",
  "hint": "The £84 is 120% including VAT, so divide by 1.2.",
  "misconceptions": [
    mc("subtract_from_new", 67.2, "You cannot take 20% off the VAT-inclusive price. £84 is 120% of the pre-VAT price, so divide by 1.2: 84 ÷ 1.2 = 70."),
  ],
  "guided_steps": [
    sayonly("The £84 already includes 20% VAT, so it is 120% of the price before VAT."),
    box("Multiplier: 1 + 0.2 = ", 1.2, "1 whole plus 0.2."),
    box("Reverse by dividing: 84 ÷ 1.2 = ", 70, "Undo the multiply.", phase="substitute"),
    box("Check forwards: 70 × 1.2 = ", 84, "Add the VAT back on.", done="Back to £84, so £70 before VAT is right."),
  ],
 },
 {  # 6
  "display": "A laptop depreciates by 25% each year. It cost £800 new. Find its value after 2 years.",
  "solutions": [450], "calculator": True, "input_type": "single_value",
  "hint": "Multiply by 0.75 twice, once per year.",
  "misconceptions": [
    mc("halved", 400, "Losing 25% twice is not losing 50%. Depreciation compounds: 800 × 0.75² = 450, not 800 × 0.5."),
    mc("one_year", 600, "£600 is the value after 1 year. Apply 0.75 again: 600 × 0.75 = 450."),
  ],
  "guided_steps": [
    sayonly("Losing 25% each year means keeping 75% each year."),
    box("Multiplier for a 25% fall: 1 − 0.25 = ", 0.75, "1 whole minus 0.25."),
    box("After year 1: 800 × 0.75 = ", 600, "Apply the multiplier once."),
    box("After year 2: 600 × 0.75 = ", 450, "Apply it to the new value.", phase="substitute"),
    box("Check with a power: 800 × 0.75² = 800 × 0.5625 = ", 450, "0.75 squared is 0.5625.", done="The power route agrees: £450."),
  ],
 },
]

# ---------------- GOLD ----------------
gold = [
 {  # 0
  "display": "After a 15% decrease, a price is £340. What was the original price?",
  "solutions": [400], "calculator": True, "input_type": "single_value",
  "hint": "The £340 is 85% of the original, so divide by 0.85.",
  "misconceptions": [
    mc("added_back", 391, "Adding 15% of 340 back on does not reverse a percentage. £340 is 85% of the original, so divide by 0.85: 340 ÷ 0.85 = 400."),
  ],
  "guided_steps": [
    sayonly("The £340 is what is left AFTER 15% came off, so it is 85% of the original."),
    box("Multiplier: 1 − 0.15 = ", 0.85, "1 whole minus 0.15."),
    box("Reverse by dividing: 340 ÷ 0.85 = ", 400, "Undo the multiply.", phase="substitute"),
    box("Check forwards: 400 × 0.85 = ", 340, "Take 15% off the original.", done="Back to £340, so £400 is right."),
  ],
 },
 {  # 1  FIXED solution 3 -> 4
  "display": "£8000 is invested at 4% compound interest. After how many complete years will it first exceed £9000?",
  "solutions": [4], "calculator": True, "input_type": "single_value",
  "hint": "Add 4% year by year and count the first total over £9000.",
  "misconceptions": [
    mc("stopped_at_3", 3, "After 3 years the total is £8998.91, still just under £9000. It first passes £9000 in year 4."),
  ],
  "guided_steps": [
    sayonly("Add 4% each year and watch for the first total over £9000."),
    box("Multiplier: 1 + 0.04 = ", 1.04, "1 whole plus 0.04."),
    box("Year 1: 8000 × 1.04 = ", 8320, "Apply the multiplier once."),
    box("Year 2: 8320 × 1.04 = ", 8652.8, "Apply it to the new total."),
    box("Year 3: 8652.80 × 1.04 = ", 8998.91, "Still under £9000.", phase="substitute"),
    box("Year 4: 8998.91 × 1.04 = ", 9358.87, "Now over £9000."),
    box("First complete year over £9000: ", 4, "Count the first year the total beats £9000.", done="Year 3 was £8998.91, just short. Year 4 is the first over £9000."),
  ],
 },
 {  # 2  FIXED solution 7903 -> 7909
  "display": "A population decreases by 8% each year from 12000. Find the population after 5 years to the nearest whole number.",
  "solutions": [7909], "calculator": True, "input_type": "single_value",
  "hint": "Multiply 12000 by 0.92 to the power 5.",
  "misconceptions": [
    mc("subtracted_40pc", 7200, "Multiplying the 8% by 5 gives 12000 × 0.6 = 7200. Compound decay keeps 92% each year: 12000 × 0.92⁵ = 7909."),
  ],
  "guided_steps": [
    sayonly("A fall of 8% each year means keeping 92% each year for five years."),
    box("Multiplier: 1 − 0.08 = ", 0.92, "1 whole minus 0.08."),
    box("Apply for 5 years: 12000 × 0.92⁵ = ", 7908.98, "0.92 to the power 5, then × 12000.", phase="substitute"),
    box("To the nearest whole number: ", 7909, "Round 7908.98.", done="7909 people."),
    box("Check by reversing one year: 7908.98 ÷ 0.92 = ", 8596.72, "Dividing by 0.92 steps back a year.", done="That is the year-4 total, and one more × 0.92 returns to 7909."),
  ],
 },
 {  # 3  FIXED final 396 -> 495, solution 400 -> 500 (removes duplicate with gold[0])
  "display": "An item is increased by 10% then decreased by 10%. The final price is £495. What was the original price?",
  "solutions": [500], "calculator": True, "input_type": "single_value",
  "hint": "Combine 1.1 and 0.9 into one multiplier, then divide the final price by it.",
  "misconceptions": [
    mc("net_zero", 495, "A 10% rise then a 10% fall is not zero: 1.1 × 0.9 = 0.99, so the price ends slightly below the start. Divide 495 by 0.99 = 500."),
  ],
  "guided_steps": [
    sayonly("A 10% rise then a 10% fall do NOT cancel. Combine the two multipliers first."),
    box("Rise multiplier: 1 + 0.1 = ", 1.1, "1 whole plus 0.1."),
    box("Fall multiplier: 1 − 0.1 = ", 0.9, "1 whole minus 0.1."),
    box("Combined: 1.1 × 0.9 = ", 0.99, "Multiply the two multipliers."),
    box("Reverse: 495 ÷ 0.99 = ", 500, "Divide the final price by the combined multiplier.", phase="substitute"),
    box("Check forwards: 500 × 0.99 = ", 495, "Apply the combined multiplier.", done="Back to £495, so the original was £500."),
  ],
 },
 {  # 4  FIXED solution 885.55 -> 885.14
  "display": "A savings account pays 3.5% compound interest. £6000 is invested. What is the interest earned (not total) after 4 years? Give to the nearest penny.",
  "solutions": [885.14], "calculator": True, "input_type": "single_value",
  "hint": "Find the total with 1.035 to the power 4, then subtract the £6000.",
  "misconceptions": [
    mc("gave_total", 6885.14, "£6885.14 is the total in the account. Interest earned = 6885.14 − 6000 = 885.14."),
    mc("simple_interest", 840, "That is simple interest (6000 × 0.035 × 4). Compound gives 6000 × 1.035⁴ − 6000 = 885.14."),
  ],
  "guided_steps": [
    sayonly("Grow the money by compounding, then take the £6000 back off to leave just the interest."),
    box("Multiplier: 1 + 0.035 = ", 1.035, "1 whole plus 0.035."),
    box("Total after 4 years: 6000 × 1.035⁴ = ", 6885.14, "1.035 to the power 4, then × 6000, to the penny."),
    box("Interest only: 6885.14 − 6000 = ", 885.14, "Subtract the original investment.", phase="substitute"),
    box("Check: 6000 + 885.14 = ", 6885.14, "Add the interest back on.", done="Adds back to the total, so £885.14 interest is right."),
  ],
 },
]

# ---------------- TIER GUIDES ----------------
tier_guides = {
 "bronze": {
   "title": "Bronze: single percentage of an amount",
   "steps": [
     "<strong>Percent to decimal:</strong> divide by 100. So 30% becomes 0.3.",
     "<strong>Of</strong> means multiply. 30% of £50 = 0.3 × 50 = £15.",
     "To increase, add the part on; to decrease, take it off.",
   ],
   "example": {
     "question": "Find 30% of £50.",
     "steps": [
       {"label": "Decimalise", "content": "30 ÷ 100 = 0.3"},
       {"label": "Multiply", "content": "0.3 × 50 = 15"},
       {"label": "Check", "content": "10% of 50 is 5, so 30% is 3 × 5 = 15 ✓"},
       {"label": "Answer", "content": "£15", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "silver": {
   "title": "Silver: compound change and reverse percentages",
   "steps": [
     "<strong>Multiplier:</strong> increase is 1 + p/100, decrease is 1 − p/100. A 4% rise is × 1.04; a 25% fall is × 0.75.",
     "<strong>Compound</strong> over n years: multiply by the multiplier n times, so × multiplier to the power n.",
     "<strong>Reverse:</strong> given the amount AFTER a change, divide by the multiplier to get the original.",
   ],
   "example": {
     "question": "A £6000 car loses 15% of its value each year. Its value after 2 years?",
     "steps": [
       {"label": "Multiplier", "content": "1 − 0.15 = 0.85"},
       {"label": "Compound", "content": "6000 × 0.85² = 6000 × 0.7225 = 4335"},
       {"label": "Check", "content": "Year 1: 6000 × 0.85 = 5100; Year 2: 5100 × 0.85 = 4335 ✓"},
       {"label": "Answer", "content": "£4335", "isAnswer": True, "is_answer": True},
     ],
   },
 },
 "gold": {
   "title": "Gold: multi-step and problem-solving percentages",
   "steps": [
     "<strong>Combine changes</strong> by multiplying the multipliers: a 10% rise then a 10% fall is 1.1 × 0.9 = 0.99, not back to the start.",
     "<strong>Reverse a compound change</strong> by dividing by the combined multiplier.",
     "For 'how many years until', apply the multiplier year by year and count when the total passes the target.",
   ],
   "example": {
     "question": "£1000 at 5% compound interest. In which year does the total first pass £1150?",
     "steps": [
       {"label": "Year 1", "content": "1000 × 1.05 = 1050"},
       {"label": "Year 2", "content": "1050 × 1.05 = 1102.50"},
       {"label": "Year 3", "content": "1102.50 × 1.05 = 1157.63, over 1150"},
       {"label": "Check", "content": "Year 2 was £1102.50, still under £1150, so year 3 is the first over ✓"},
       {"label": "Answer", "content": "3 years", "isAnswer": True, "is_answer": True},
     ],
   },
 },
}

# ---------------- GUIDED (opener + teach) ----------------
opener_svg = ('<svg viewBox="0 0 240 130" role="img" aria-label="A price tag showing twenty pounds with twenty percent off">'
  '<path d="M30 25 L150 25 L150 95 L30 95 Z" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>'
  '<circle cx="45" cy="40" r="4" fill="none" stroke="currentColor" stroke-width="2"/>'
  '<text x="90" y="58" text-anchor="middle" font-family="Inter, sans-serif" font-size="20" fill="currentColor">£20</text>'
  '<text x="90" y="82" text-anchor="middle" font-family="Inter, sans-serif" font-size="13" fill="currentColor">20% OFF</text>'
  '</svg>')

guided = {
 "opener": {
   "display": opener_svg + "<br>A £20 hoodie is in a '20% off' sale. Work out what you actually pay.",
   "steps": [
     box("20% of £20 is £", 4, "10% of £20 is £2, so 20% is £4."),
     box("So you pay 20 − 4 = £", 16, "Take the discount off the price."),
     sayonly("You just did a <strong>percentage decrease</strong>. There is a one-step shortcut: paying 80% of the price means × 0.8, and 20 × 0.8 = 16. That multiplier, <strong>0.8</strong>, is the whole method. Every question in this lesson is really 'find the multiplier, then multiply'."),
   ],
 },
 "teach": {
   "bronze": {
     "display": "Increase £50 by 40%.",
     "steps": [
       sayonly("Turn the 40% into a decimal."),
       box("40 ÷ 100 = ", 0.4, "Two places: 40% becomes 0.4."),
       box("Increase, so add to 1: 1 + 0.4 = ", 1.4, "1 whole plus 0.4."),
       box("Multiply the amount: 50 × 1.4 = ", 70, "50 times the multiplier.", done="Gone in one multiply. That is the shortcut."),
       box("Check the long way: 40% of 50 = 0.4 × 50 = ", 20, "0.4 × 50."),
       box("50 + 20 = ", 70, "Add the increase on.", done="Both ways give £70."),
     ],
   },
   "silver": {
     "display": "A £1200 bike loses 20% of its value each year. Find its value after 2 years.",
     "steps": [
       sayonly("Losing 20% means keeping 80% each year."),
       box("Multiplier: 1 − 0.2 = ", 0.8, "1 whole minus 0.2."),
       box("After year 1: 1200 × 0.8 = ", 960, "Apply the multiplier once."),
       box("After year 2: 960 × 0.8 = ", 768, "Apply it to the new value.", done="Each year works on the latest value."),
       box("Check with a power: 1200 × 0.8² = 1200 × 0.64 = ", 768, "0.8 squared is 0.64.", done="The power route agrees: £768."),
     ],
   },
   "gold": {
     "display": "£2500 is invested at 4% compound interest per year. Find the interest earned after 3 years, to the nearest penny.",
     "steps": [
       sayonly("Grow the money first, then strip out the original to leave just the interest."),
       box("Multiplier: 1 + 0.04 = ", 1.04, "1 whole plus 0.04."),
       box("Total after 3 years: 2500 × 1.04³ = ", 2812.16, "1.04 to the power 3, then × 2500, to the penny."),
       box("Interest only: 2812.16 − 2500 = ", 312.16, "Subtract the money you started with.", done="Interest is the growth on top of the original."),
       box("Check: 2500 + 312.16 = ", 2812.16, "Add the interest back on.", done="Adds back to the total, so £312.16 is the interest."),
     ],
   },
 },
}

# ---------------- METHOD CARD (slim) ----------------
method_card = {
 "title": "Percentages & Compound Change",
 "steps": [
   "Multiplier: increase is 1 + p/100, decrease is 1 − p/100.",
   "One change: multiply once. Compound: multiply by the multiplier to the power n.",
   "Reverse percentage: divide by the multiplier.",
   "Percentage change = (new − old) ÷ old × 100.",
 ],
 "content": ("<p>Every percentage change uses a <strong>multiplier</strong>: a 20% rise is × 1.2, a 15% fall is × 0.85.</p>"
   "<p><strong>Compound</strong> change applies the multiplier once per year, so after \\(n\\) years amount = start \\(\\times\\) multiplier\\(^n\\). This covers interest, depreciation and population change.</p>"
   "<p>To find the <strong>original</strong> before a change (reverse percentage), divide by the multiplier instead of multiplying.</p>"),
 "example": ("<p><strong>£5000 at 3% compound interest for 4 years.</strong></p>"
   "<p>Multiplier = 1.03. Value = 5000 × 1.03⁴ = 5000 × 1.12550881 = £5627.54 (2 d.p.)</p>"),
}

# ---------------- ASSEMBLE ----------------
pd = dict(live)  # shallow copy, preserve related_videos, worked_examples, topic_links
pd["method_card"] = method_card
pd["problem_bank"] = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": "Find a percentage of an amount, or a single increase or decrease.",
  "silver_description": "Compound growth and depreciation, reverse percentages, and percentage change.",
  "gold_description": "Combined changes, reverse compound problems, and 'how many years' questions.",
}
pd["tier_guides"] = tier_guides
pd["guided"] = guided
# preserve topic_links, related_videos, worked_examples untouched (already in `live`)

out = DIR + "lesson_%s_%s.json" % (BOARD, KEY)
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
print("preserved keys:", [k for k in ("related_videos","worked_examples","topic_links") if k in pd])
