# -*- coding: utf-8 -*-
import json

LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_number-L05.json"
OUT  = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-aqa_number-L05.json"
live = json.load(open(LIVE, encoding="utf-8"))

def box(pre, answer, hint, done=None, say=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if done: d["done"] = done
    if say: d["say"] = say
    if phase: d["phase"] = phase
    return d
def say(s): return {"say": s}

# ---------------- BRONZE ----------------
bronze = [
 {  # 0
  "display": r"Find \(25\%\) of \(360\)",
  "solutions": [90], "calculator": False, "input_type": "single_value",
  "hint": "25% is a quarter. Find 10% of 360 first, then build up to 25%.",
  "misconceptions": [{"pattern": "divide_by_percent", "expect": 14.4,
    "message": "14.4 comes from dividing 360 by 25. 25% means a quarter, so divide by 4: 360 ÷ 4 = 90."}],
  "guided_steps": [
    say(r"We are finding \(25\%\) of \(360\)."),
    box("Find 10% of 360 by dividing by 10.", 36, "360 ÷ 10 = 36."),
    box("Find 5% by halving that 10%.", 18, "Half of 36 is 18.", phase="substitute"),
    box("25% is 10% + 10% + 5%. Add 36 + 36 + 18.", 90, "36 + 36 + 18 = 90.",
        done="Check: 90 × 4 = 360, so 90 is one quarter of 360.")]},
 {  # 1  (CHANGED: was 40% of 150 = 60, duplicate)
  "display": r"Find \(40\%\) of \(250\)",
  "solutions": [100], "calculator": False, "input_type": "single_value",
  "hint": "Find 10% of 250, then build up to 40%.",
  "misconceptions": [{"pattern": "stopped_at_ten", "expect": 25,
    "message": "25 is only 10% of 250. 40% is four lots of 10%, so 4 × 25 = 100."}],
  "guided_steps": [
    say(r"We are finding \(40\%\) of \(250\)."),
    box("Find 10% of 250 by dividing by 10.", 25, "250 ÷ 10 = 25."),
    box("Find 20% by doubling the 10%.", 50, "25 × 2 = 50.", phase="substitute"),
    box("40% is double 20%. Double 50.", 100, "50 × 2 = 100.",
        done="Check: 0.4 × 250 = 100. Correct.")]},
 {  # 2
  "display": r"Find \(15\%\) of \(80\)",
  "solutions": [12], "calculator": False, "input_type": "single_value",
  "hint": "Find 10% of 80, then add half of it for the extra 5%.",
  "misconceptions": [{"pattern": "stopped_at_ten", "expect": 8,
    "message": "8 is only 10% of 80. 15% is 10% plus 5%, so 8 + 4 = 12."}],
  "guided_steps": [
    say(r"We are finding \(15\%\) of \(80\)."),
    box("Find 10% of 80 by dividing by 10.", 8, "80 ÷ 10 = 8."),
    box("Find 5% by halving the 10%.", 4, "Half of 8 is 4.", phase="substitute"),
    box("15% is 10% + 5%. Add 8 + 4.", 12, "8 + 4 = 12.",
        done="Check: 0.15 × 80 = 12. Correct.")]},
 {  # 3
  "display": r"Increase \(200\) by \(10\%\)",
  "solutions": [220], "calculator": False, "input_type": "single_value",
  "hint": "Find 10% of 200, then add it on to the original.",
  "misconceptions": [{"pattern": "found_percent_only", "expect": 20,
    "message": "20 is just 10% of 200. The question says increase, so add it on: 200 + 20 = 220."}],
  "guided_steps": [
    say(r"We are increasing \(200\) by \(10\%\)."),
    box("Find 10% of 200 by dividing by 10.", 20, "200 ÷ 10 = 20."),
    box("The new amount is 100% + 10% of the original. Write that percentage.", 110,
        "100 + 10 = 110.", phase="substitute"),
    box("110% of 200 means add the 20 on: 200 + 20.", 220, "200 + 20 = 220.",
        done="Check: 200 × 1.1 = 220. Correct.")]},
 {  # 4  (CHANGED: was decrease 80 by 25% = 60, duplicate)
  "display": r"Decrease \(90\) by \(20\%\)",
  "solutions": [72], "calculator": False, "input_type": "single_value",
  "hint": "Find 20% of 90, then take it off the original.",
  "misconceptions": [{"pattern": "forgot_subtract", "expect": 18,
    "message": "18 is just 20% of 90. Decrease means take it away: 90 − 18 = 72."}],
  "guided_steps": [
    say(r"We are decreasing \(90\) by \(20\%\)."),
    box("Find 10% of 90 by dividing by 10.", 9, "90 ÷ 10 = 9."),
    box("Find 20% by doubling the 10%.", 18, "9 × 2 = 18.", phase="substitute"),
    box("Decrease means subtract: 90 − 18.", 72, "90 − 18 = 72.",
        done="Check: 90 × 0.8 = 72. Correct.")]},
 {  # 5
  "display": r"Write \(\frac{3}{5}\) as a percentage",
  "solutions": [60], "calculator": False, "input_type": "single_value",
  "hint": "Turn the fraction into a decimal, then multiply by 100.",
  "misconceptions": [{"pattern": "forgot_times_100", "expect": 0.6,
    "message": "0.6 is the decimal from 3 ÷ 5. To make a percentage, multiply by 100: 0.6 × 100 = 60%."}],
  "guided_steps": [
    say(r"We are writing \(\frac{3}{5}\) as a percentage."),
    box("Divide 3 by 5 to write the fraction as a decimal.", 0.6, "3 ÷ 5 = 0.6."),
    box("A percentage is out of 100, so multiply the decimal by 100.", 60,
        "0.6 × 100 = 60.", phase="substitute"),
    box("Write the final percentage as a whole number.", 60, "It is 60.",
        done="Check: 3/5 = 60/100 = 60%. Correct.")]},
 {  # 6
  "display": r"Write \(0.35\) as a percentage",
  "solutions": [35], "calculator": False, "input_type": "single_value",
  "hint": "A percentage is out of 100, so multiply the decimal by 100.",
  "misconceptions": [{"pattern": "one_place_only", "expect": 3.5,
    "message": "3.5 moves the point only one place. Per cent is out of 100, so move two places: 0.35 becomes 35%."}],
  "guided_steps": [
    say(r"We are writing \(0.35\) as a percentage."),
    box("Multiplying by 100 moves the point two places. First work out 0.35 × 10.", 3.5,
        "0.35 × 10 = 3.5."),
    box("Multiply by 10 again to complete the × 100.", 35, "3.5 × 10 = 35.", phase="substitute"),
    box("Write 0.35 as a percentage.", 35, "It is 35.",
        done="Check: 35 ÷ 100 = 0.35. Correct.")]},
 {  # 7
  "display": r"Write \(45\%\) as a decimal",
  "solutions": [0.45], "calculator": False, "input_type": "single_value",
  "hint": "A percentage is out of 100, so divide by 100.",
  "misconceptions": [{"pattern": "one_place_only", "expect": 4.5,
    "message": "4.5 divides by only 10. Per cent is out of 100, so divide by 100: 45 ÷ 100 = 0.45."}],
  "guided_steps": [
    say(r"We are writing \(45\%\) as a decimal."),
    box("Dividing by 100 moves the point two places. First work out 45 ÷ 10.", 4.5,
        "45 ÷ 10 = 4.5."),
    box("Divide by 10 again to complete the ÷ 100.", 0.45, "4.5 ÷ 10 = 0.45.", phase="substitute"),
    box("Write 45% as a decimal.", 0.45, "It is 0.45.",
        done="Check: 0.45 × 100 = 45%. Correct.")]},
]

# ---------------- SILVER ----------------
silver = [
 {  # 0
  "display": r"Increase \(\pounds350\) by \(12\%\)",
  "solutions": [392], "calculator": True, "input_type": "single_value",
  "hint": "The new amount is 112% of £350, so multiply by 1.12.",
  "misconceptions": [{"pattern": "found_percent_only", "expect": 42,
    "message": "42 is just 12% of 350. Increase means add it on: 350 + 42 = 392."}],
  "guided_steps": [
    say(r"We are increasing \(\pounds350\) by \(12\%\)."),
    box("A 12% increase means the total is 100% + 12%. Write that percentage.", 112,
        "100 + 12 = 112."),
    box("112% as a multiplier is 1.12. Work out 350 × 1.12.", 392, "350 × 1.12 = 392.",
        phase="substitute"),
    box("Write the increased price in pounds.", 392, "It is 392.",
        done="Check: 12% of 350 is 42, and 350 + 42 = 392. Correct.")]},
 {  # 1
  "display": r"Decrease \(\pounds240\) by \(35\%\)",
  "solutions": [156], "calculator": True, "input_type": "single_value",
  "hint": "You keep 65% of £240, so multiply by 0.65.",
  "misconceptions": [{"pattern": "found_percent_only", "expect": 84,
    "message": "84 is 35% of 240, the amount removed. Decrease means take it off: 240 − 84 = 156."}],
  "guided_steps": [
    say(r"We are decreasing \(\pounds240\) by \(35\%\)."),
    box("Decreasing by 35% leaves 100% − 35%. Write the percentage kept.", 65,
        "100 − 35 = 65."),
    box("65% as a multiplier is 0.65. Work out 240 × 0.65.", 156, "240 × 0.65 = 156.",
        phase="substitute"),
    box("Write the reduced price in pounds.", 156, "It is 156.",
        done="Check: 35% of 240 is 84, and 240 − 84 = 156. Correct.")]},
 {  # 2
  "display": r"A shirt was \(\pounds25\) and now costs \(\pounds30\). Find the percentage increase.",
  "solutions": [20], "calculator": False, "input_type": "single_value",
  "hint": "Find the money change, then divide by the original £25.",
  "misconceptions": [{"pattern": "gave_change", "expect": 5,
    "message": "5 is just the money increase, not a percentage. Divide the £5 rise by the original £25, then × 100: 20%."}],
  "guided_steps": [
    say(r"A shirt rose from \(\pounds25\) to \(\pounds30\). We want the percentage increase."),
    box("Find the money increase: 30 − 25.", 5, "30 − 25 = 5."),
    box("Divide the rise by the original price: 5 ÷ 25.", 0.2, "5 ÷ 25 = 0.2.",
        phase="substitute"),
    box("Multiply by 100 to get the percentage.", 20, "0.2 × 100 = 20.",
        done="Check: 20% of 25 is 5, and 25 + 5 = 30. Correct.")]},
 {  # 3  (CHANGED: was £9600 = 20%, duplicate with [2])
  "display": r"A car was \(\pounds12\,000\) and sold for \(\pounds9\,000\). Find the percentage decrease.",
  "solutions": [25], "calculator": True, "input_type": "single_value",
  "hint": "Find the money fall, then divide by the original £12000.",
  "misconceptions": [{"pattern": "gave_change", "expect": 3000,
    "message": "3000 is the amount the price fell, not a percentage. Divide 3000 by the original 12000, then × 100: 25%."}],
  "guided_steps": [
    say(r"A car fell from \(\pounds12\,000\) to \(\pounds9\,000\). We want the percentage decrease."),
    box("Find the money decrease: 12000 − 9000.", 3000, "12000 − 9000 = 3000."),
    box("Divide the fall by the original price: 3000 ÷ 12000.", 0.25, "3000 ÷ 12000 = 0.25.",
        phase="substitute"),
    box("Multiply by 100 to get the percentage.", 25, "0.25 × 100 = 25.",
        done="Check: 25% of 12000 is 3000, and 12000 − 3000 = 9000. Correct.")]},
 {  # 4
  "display": r"VAT is \(20\%\). An item costs \(\pounds45\) before VAT. What is the price including VAT?",
  "solutions": [54], "calculator": True, "input_type": "single_value",
  "hint": "Find 20% of £45 and add it on, or multiply by 1.2.",
  "misconceptions": [{"pattern": "found_percent_only", "expect": 9,
    "message": "9 is just the VAT (20% of 45). The price including VAT adds it on: 45 + 9 = 54."}],
  "guided_steps": [
    say(r"VAT is \(20\%\). An item is \(\pounds45\) before VAT."),
    box("Find 20% of 45 (the VAT).", 9, "0.2 × 45 = 9."),
    box("Add the VAT onto the price: 45 + 9.", 54, "45 + 9 = 54.", phase="substitute"),
    box("Write the price including VAT in pounds.", 54, "It is 54.",
        done="Check: 45 × 1.2 = 54. Correct.")]},
 {  # 5
  "display": r"Express \(18\) out of \(45\) as a percentage",
  "solutions": [40], "calculator": False, "input_type": "single_value",
  "hint": "Simplify 18/45, turn it into a decimal, then multiply by 100.",
  "misconceptions": [{"pattern": "forgot_times_100", "expect": 0.4,
    "message": "0.4 is the decimal from 18 ÷ 45. Multiply by 100 to make a percentage: 40%."}],
  "guided_steps": [
    say(r"We are writing \(18\) out of \(45\) as a percentage."),
    box("Simplify 18/45 by dividing both by 9. Write the new numerator.", 2,
        "18 ÷ 9 = 2 and 45 ÷ 9 = 5, giving 2/5."),
    box("2/5 as a decimal is 2 ÷ 5. Work it out.", 0.4, "2 ÷ 5 = 0.4.", phase="substitute"),
    box("Multiply by 100 to get the percentage.", 40, "0.4 × 100 = 40.",
        done="Check: 40% of 45 is 18. Correct.")]},
 {  # 6
  "display": r"Find \(17.5\%\) of \(\pounds640\)",
  "solutions": [112], "calculator": True, "input_type": "single_value",
  "hint": "Multiply 640 by 0.175, or add 10% + 5% + 2.5%.",
  "misconceptions": [{"pattern": "stopped_at_ten", "expect": 64,
    "message": "64 is only 10% of 640. 17.5% is 10% + 5% + 2.5% = 64 + 32 + 16 = 112."}],
  "guided_steps": [
    say(r"We are finding \(17.5\%\) of \(\pounds640\)."),
    box("Find 10% of 640 by dividing by 10.", 64, "640 ÷ 10 = 64."),
    box("Find 5% by halving the 10%.", 32, "Half of 64 is 32.", phase="substitute"),
    box("2.5% is half of 5% (16). Add 10% + 5% + 2.5%: 64 + 32 + 16.", 112,
        "64 + 32 + 16 = 112.",
        done="Check: 0.175 × 640 = 112. Correct.")]},
]

# ---------------- GOLD ----------------
gold = [
 {  # 0
  "display": r"After a \(15\%\) discount, a sofa costs \(\pounds510\). Find the original price.",
  "solutions": [600], "calculator": True, "input_type": "single_value",
  "hint": "The £510 is 85% of the original, so divide by 0.85.",
  "misconceptions": [{"pattern": "add_15", "expect": 586.5,
    "message": "586.5 adds 15% onto the sale price. The £510 is already 85% of the original, so divide by 0.85: 510 ÷ 0.85 = 600."}],
  "guided_steps": [
    say(r"After a \(15\%\) discount, a sofa costs \(\pounds510\). We want the original price."),
    box("A 15% discount means you pay 100% − 15%. Write that percentage.", 85,
        "100 − 15 = 85."),
    box("So £510 is 85% of the original. Find 1% by dividing 510 by 85.", 6,
        "510 ÷ 85 = 6.", phase="substitute"),
    box("The original is 100%. Multiply 1% by 100.", 600, "6 × 100 = 600."),
    box("Write the original price in pounds.", 600, "It is 600.",
        done="Check: 600 × 0.85 = 510. Correct.")]},
 {  # 1
  "display": r"After a \(20\%\) pay rise, Alex earns \(\pounds27\,000\). Find the original salary.",
  "solutions": [22500], "calculator": True, "input_type": "single_value",
  "hint": "The £27000 is 120% of the original, so divide by 1.2.",
  "misconceptions": [{"pattern": "subtract_20", "expect": 21600,
    "message": "21600 takes 20% off the new salary. The £27000 is 120% of the original, so divide by 1.2: 27000 ÷ 1.2 = 22500."}],
  "guided_steps": [
    say(r"After a \(20\%\) pay rise, Alex earns \(\pounds27\,000\). We want the original salary."),
    box("A 20% rise means the new pay is 100% + 20%. Write that percentage.", 120,
        "100 + 20 = 120."),
    box("So £27000 is 120% of the original. Find 1% by dividing 27000 by 120.", 225,
        "27000 ÷ 120 = 225.", phase="substitute"),
    box("The original is 100%. Multiply 1% by 100.", 22500, "225 × 100 = 22500."),
    box("Write the original salary in pounds.", 22500, "It is 22500.",
        done="Check: 22500 × 1.2 = 27000. Correct.")]},
 {  # 2
  "display": r"\(\pounds5000\) is invested at \(3\%\) compound interest per year. Find the value after \(2\) years.",
  "solutions": [5304.5], "calculator": True, "input_type": "single_value",
  "hint": "Multiply by 1.03 once for each year: 5000 × 1.03².",
  "misconceptions": [{"pattern": "simple_interest", "expect": 5300,
    "message": "5300 uses simple interest (2 × 3% = 6% of 5000 = 300). Compound interest multiplies by 1.03 each year: 5000 × 1.03² = 5304.50."}],
  "guided_steps": [
    say(r"\(\pounds5000\) grows at \(3\%\) compound interest for \(2\) years."),
    box("Each year multiplies by 1.03. After year 1, work out 5000 × 1.03.", 5150,
        "5000 × 1.03 = 5150."),
    box("Apply another year: multiply 5150 by 1.03.", 5304.5, "5150 × 1.03 = 5304.5.",
        phase="substitute"),
    box("Write the value after 2 years in pounds.", 5304.5, "It is 5304.50.",
        done="Check: 5000 × 1.03² = 5000 × 1.0609 = 5304.50. Correct.")]},
 {  # 3
  "display": r"A car depreciates by \(10\%\) each year. It costs \(\pounds20\,000\). Find its value after \(3\) years.",
  "solutions": [14580], "calculator": True, "input_type": "single_value",
  "hint": "Multiply by 0.9 once for each year: 20000 × 0.9³.",
  "misconceptions": [{"pattern": "linear", "expect": 14000,
    "message": "14000 takes 30% off once (3 × 10%). Depreciation multiplies by 0.9 each year: 20000 × 0.9³ = 14580."}],
  "guided_steps": [
    say(r"A car worth \(\pounds20\,000\) depreciates by \(10\%\) each year for \(3\) years."),
    box("Losing 10% leaves 90%, so multiply by 0.9. After year 1: 20000 × 0.9.", 18000,
        "20000 × 0.9 = 18000."),
    box("After year 2: multiply 18000 by 0.9.", 16200, "18000 × 0.9 = 16200.",
        phase="substitute"),
    box("After year 3: multiply 16200 by 0.9.", 14580, "16200 × 0.9 = 14580.",
        done="Check: 20000 × 0.9³ = 20000 × 0.729 = 14580. Correct.")]},
 {  # 4
  "display": r"After two successive discounts of \(10\%\) and \(20\%\), an item costs \(\pounds288\). Find the original price.",
  "solutions": [400], "calculator": True, "input_type": "single_value",
  "hint": "The two discounts multiply to 0.9 × 0.8 = 0.72, so divide 288 by 0.72.",
  "misconceptions": [{"pattern": "reversed_one_only", "expect": 360,
    "message": "360 reverses only the 20% discount. Both discounts apply, so divide by 0.9 × 0.8 = 0.72: 288 ÷ 0.72 = 400."}],
  "guided_steps": [
    say(r"After discounts of \(10\%\) then \(20\%\), an item costs \(\pounds288\). We want the original price."),
    box("A 10% discount is ×0.9 and a 20% discount is ×0.8. Multiply them: 0.9 × 0.8.", 0.72,
        "0.9 × 0.8 = 0.72."),
    box("So £288 is 72% of the original. Find 1% by dividing 288 by 72.", 4,
        "288 ÷ 72 = 4.", phase="substitute"),
    box("The original is 100%. Multiply 1% by 100.", 400, "4 × 100 = 400."),
    box("Write the original price in pounds.", 400, "It is 400.",
        done="Check: 400 × 0.9 × 0.8 = 400 × 0.72 = 288. Correct.")]},
]

# ---------------- OPENER (with bar-model SVG) ----------------
svg = ('<svg viewBox="0 0 240 96" role="img" aria-label="A bar showing 40 pounds '
 'split into four equal 10 pound blocks, with one block shaded as the 25 percent discount">'
 '<text x="120" y="15" font-family="Inter, sans-serif" font-size="12" fill="currentColor" text-anchor="middle">Jacket: £40</text>'
 '<rect x="20" y="28" width="200" height="34" fill="none" stroke="currentColor" stroke-width="1.5"/>'
 '<line x1="70" y1="28" x2="70" y2="62" stroke="currentColor" stroke-width="1"/>'
 '<line x1="120" y1="28" x2="120" y2="62" stroke="currentColor" stroke-width="1"/>'
 '<line x1="170" y1="28" x2="170" y2="62" stroke="currentColor" stroke-width="1"/>'
 '<rect x="170" y="28" width="50" height="34" fill="#f59e0b" fill-opacity="0.3"/>'
 '<text x="45" y="49" font-family="Inter, sans-serif" font-size="10" fill="currentColor" text-anchor="middle">£10</text>'
 '<text x="95" y="49" font-family="Inter, sans-serif" font-size="10" fill="currentColor" text-anchor="middle">£10</text>'
 '<text x="145" y="49" font-family="Inter, sans-serif" font-size="10" fill="currentColor" text-anchor="middle">£10</text>'
 '<text x="195" y="49" font-family="Inter, sans-serif" font-size="10" fill="currentColor" text-anchor="middle">£10</text>'
 '<text x="195" y="79" font-family="Inter, sans-serif" font-size="10" fill="currentColor" text-anchor="middle">25% off</text>'
 '</svg>')

opener = {
  "display": ('<div style="text-align:center">' + svg + '</div>'
    'A jacket costs <strong>£40</strong>. A sign says <strong>25% off</strong>.<br>'
    'The bar shows the £40 split into four equal £10 blocks.'),
  "steps": [
    box("Each block is a quarter of £40. How many pounds is one block?", 10,
        "£40 shared into 4 equal blocks: 40 ÷ 4 = 10."),
    box("The shaded block is the 25% off. After taking it off, what do you pay in pounds?", 30,
        "40 − 10 = 30."),
    say("You just found <strong>25% of £40</strong>. 25% means 25 out of 100, the same as one "
        "quarter, so a quarter of £40 is £10. Every percentage question is this move: turn "
        "the percent into a fraction or decimal, then multiply. Increases add it on, decreases take "
        "it off, and working backwards undoes the multiply.")]
}

# ---------------- TEACH ----------------
teach = {
 "bronze": {
   "display": r"Find \(30\%\) of \(80\).",
   "steps": [
     say(r"30% means 30 out of every 100. An easy route is to find 10% first."),
     box("Find 10% of 80 by dividing by 10.", 8, "80 ÷ 10 = 8."),
     box("30% is three lots of 10%. Multiply 8 by 3.", 24, "3 × 8 = 24."),
     box("Check with a decimal: 30% is 0.3. Work out 0.3 × 80.", 24, "0.3 × 80 = 24."),
     box("Write 30% of 80.", 24, "Both routes give 24.",
         done="30% of 80 is 24. That was the whole point.")]},
 "silver": {
   "display": r"Increase \(\pounds80\) by \(15\%\).",
   "steps": [
     say(r"Increasing by 15% means the new amount is 115% of the old."),
     box("Find 10% of 80 by dividing by 10.", 8, "80 ÷ 10 = 8."),
     box("Find 5% by halving the 10%.", 4, "Half of 8 is 4."),
     box("15% is 10% + 5%. Add 8 + 4.", 12, "8 + 4 = 12."),
     box("Increase means add the 15% on: 80 + 12.", 92, "80 + 12 = 92.",
         done="£80 increased by 15% is £92. Gone.")]},
 "gold": {
   "display": r"After a \(20\%\) discount, a coat costs \(\pounds64\). Find the original price.",
   "steps": [
     say(r"A 20% discount means you pay 80% of the original, so \(\pounds64\) is 80% of the price."),
     box("Start at 100% and take off the 20% discount. Write the percentage paid.", 80,
         "100 − 20 = 80."),
     box("£64 is 80%. Find 1% by dividing 64 by 80.", 0.8, "64 ÷ 80 = 0.8."),
     box("The original is 100%. Multiply 1% by 100.", 80, "0.8 × 100 = 80."),
     box("Write the original price in pounds.", 80, "It is 80.",
         done="Original £80. Check: 80 × 0.8 = 64. Gone.")]},
}

# ---------------- TIER GUIDES ----------------
tier_guides = {
 "bronze": {
   "title": "Bronze: Percentage of an amount",
   "steps": [
     "<strong>Per cent means out of 100.</strong> To find a percentage of an amount, turn the percentage into a decimal (25% = 0.25) and multiply.",
     "No calculator? Find <strong>10%</strong> by dividing by 10, and <strong>1%</strong> by dividing by 100, then build the percentage you need.",
     "To <strong>increase or decrease</strong>, find the percentage, then add it on or take it off the original."],
   "example": {
     "question": r"Find 20% of \(\pounds150\)",
     "steps": [
       {"label": "10%", "content": "10% of 150 is 15."},
       {"label": "20%", "content": "20% is double 10%, so 2 × 15 = 30."},
       {"label": "Check", "content": "0.2 × 150 = 30 as well."},
       {"label": "Answer", "content": r"\(\pounds30\)", "isAnswer": True, "is_answer": True}]}},
 "silver": {
   "title": "Silver: Percentage change and comparison",
   "steps": [
     "<strong>Increase or decrease by a percentage</strong> with a multiplier: increase by 12% is ×1.12, decrease by 12% is ×0.88.",
     "To write one amount <strong>as a percentage of another</strong>, divide the part by the whole, then multiply by 100.",
     "For a <strong>percentage change</strong>, divide the actual change by the <strong>original</strong> amount, then multiply by 100."],
   "example": {
     "question": r"A price rises from \(\pounds40\) to \(\pounds50\). Find the percentage increase.",
     "steps": [
       {"label": "Change", "content": "The rise is 50 − 40 = £10."},
       {"label": "Divide by original", "content": "10 ÷ 40 = 0.25."},
       {"label": "Check", "content": "0.25 × 100 = 25."},
       {"label": "Answer", "content": r"\(25\%\)", "isAnswer": True, "is_answer": True}]}},
 "gold": {
   "title": "Gold: Reverse and repeated percentages",
   "steps": [
     "<strong>Reverse percentage:</strong> the final amount equals the original times a multiplier. Divide the final amount by the multiplier to get the original.",
     "A 15% discount means you paid <strong>85%</strong>, so divide by 0.85. A 20% rise means 120%, so divide by 1.2.",
     "<strong>Repeated change</strong> (compound interest, depreciation): multiply by the multiplier once for each year."],
   "example": {
     "question": r"After a 20% rise, a wage is \(\pounds30\) per hour. Find the original.",
     "steps": [
       {"label": "Multiplier", "content": "A 20% rise means ×1.2."},
       {"label": "Reverse it", "content": "Original = 30 ÷ 1.2."},
       {"label": "Check", "content": "25 × 1.2 = 30."},
       {"label": "Answer", "content": r"\(\pounds25\)", "isAnswer": True, "is_answer": True}]}},
}

# ---------------- METHOD CARD (slim) ----------------
method_card = {
  "title": "How to Work with Percentages",
  "steps": [
    "To find a percentage of an amount, write the percentage as a decimal and multiply.",
    "To increase or decrease, use a multiplier: increase by 12% is ×1.12, decrease by 12% is ×0.88.",
    "To write one number as a percentage of another, divide the part by the whole, then multiply by 100.",
    "For a reverse percentage, divide the final amount by its multiplier to find the original."],
  "content": ("<p><strong>Per cent</strong> means 'out of 100'. To find a percentage of an amount, turn "
    "the percentage into a decimal and multiply. Without a calculator, find 10% by dividing by 10 and "
    "1% by dividing by 100, then build the percentage you need.</p><p>To <strong>increase or "
    "decrease</strong>, use a multiplier: increase by 12% is ×1.12, decrease by 12% is ×0.88.</p><p>To "
    "write one number <strong>as a percentage of another</strong>, divide the part by the whole and "
    "multiply by 100. For a <strong>reverse percentage</strong>, divide the final amount by its "
    "multiplier. <strong>Compound</strong> change multiplies once per year.</p>"),
  "example": ("<p><strong>A coat is reduced by 20% to £48. Find the original price.</strong></p>"
    "<p><strong>Step 1:</strong> A 20% discount means you pay 80%, so the multiplier is 0.8.</p>"
    "<p><strong>Step 2:</strong> Original = 48 ÷ 0.8.</p><p><strong>Answer:</strong> \\(\\pounds60\\)</p>"),
}

pb = {
  "bronze": bronze, "silver": silver, "gold": gold,
  "bronze_description": "Find a percentage of an amount, apply a simple increase or decrease, and convert between fractions, decimals and percentages.",
  "silver_description": "Increase or decrease by a percentage, and find one amount as a percentage of another.",
  "gold_description": "Work backwards to an original amount (reverse percentages) and apply repeated percentage change like compound interest and depreciation.",
}

out = {
  "method_card": method_card,
  "topic_links": live["topic_links"],
  "problem_bank": pb,
  "related_videos": live["related_videos"],
  "worked_examples": live["worked_examples"],
  "tier_guides": tier_guides,
  "guided": {"opener": opener, "teach": teach},
}

json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", OUT)
print("bronze sols:", [p["solutions"] for p in bronze])
print("silver sols:", [p["solutions"] for p in silver])
print("gold sols:", [p["solutions"] for p in gold])
