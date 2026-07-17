# -*- coding: utf-8 -*-
"""Build guided-learning + figure conversion for maths-ocr number-L05 Percentages."""
import json, io

live = json.load(io.open("_L05_live.json", encoding="utf-8"))
pd = live  # mutate in place; preserve untouched fields

# ---- topic_links, related_videos preserved byte-for-byte ----
# worked_examples: preserved, except em dashes in step labels replaced with
# colons to satisfy the no-em-dash style law (minimal style repair).
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str) and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---- method_card: slim reference (<=4 steps, content <=140 words) ----
pd["method_card"] = {
    "title": "Working with Percentages",
    "steps": [
        "Percentage of an amount: turn the % into a decimal (÷ 100), then multiply.",
        "Increase or decrease: multiply by 1 + r/100 (up) or 1 − r/100 (down).",
        "Percentage change: (change ÷ original) × 100. Always divide by the original.",
        "Reverse: if you know the value after the change, divide by the multiplier.",
    ],
    "content": "<p>A <strong>percentage</strong> means 'out of 100'. Convert it to a decimal and multiply to find a percentage of an amount. For a change, use a <strong>multiplier</strong>: a 15% rise is × 1.15, a 20% fall is × 0.80. To measure a change, divide by the <em>original</em> value. To undo a change (reverse percentage), divide the new value by the multiplier.</p>",
    "example": "<p><strong>Find</strong> 15% of £240.</p><p>15% = 0.15, so 240 × 0.15 = £36.</p>",
}

pb = pd["problem_bank"]
pb["bronze_description"] = "Find a percentage of an amount, and convert between decimals, fractions and percentages."
pb["silver_description"] = "Increase or decrease by a percentage, find a percentage change, and reverse a single percentage."
pb["gold_description"] = "Reverse percentages, compound growth and decay, and repeated percentage change."

def M(pattern, expect, message, note):
    return {"pattern": pattern, "expect": expect, "message": message, "note": note}

# ============================ BRONZE ============================
bronze = [
    # B1 25% of 60 = 15
    {"hint": "25% is a quarter. Turn it into a decimal (0.25) and multiply.",
     "misc": [M("divide_by_number", 2.4, "25% does not mean ÷ 25. It means × 0.25 (or ÷ 4): 60 × 0.25 = 15.", "60/25=2.4")],
     "steps": [
        {"say": "25% means 25 out of 100. Write it as a decimal.", "pre": "25 ÷ 100 = ", "post": "", "answer": 0.25, "hint": "Move the digits two places, so 25 becomes 0.25."},
        {"say": "Now find that fraction of 60.", "phase": "substitute", "pre": "60 × 0.25 = ", "post": "", "answer": 15, "hint": "A quarter of 60."},
        {"phase": "substitute", "pre": "Check it really is 25%: 15 ÷ 60 × 100 = ", "post": "", "answer": 25, "done": "15 is exactly 25% of 60, so it is right.", "hint": "Divide the part by the whole, then × 100."},
     ]},
    # B2 10% of 350 = 35
    {"hint": "10% means divide by 10.",
     "misc": [M("divide_by_100", 3.5, "10% is ÷ 10, not ÷ 100. 350 ÷ 10 = 35.", "350/100=3.5")],
     "steps": [
        {"say": "10% means 10 out of 100. As a decimal that is 0.1.", "pre": "10 ÷ 100 = ", "post": "", "answer": 0.1, "hint": "Ten hundredths is 0.1."},
        {"say": "Now take that much of 350.", "phase": "substitute", "pre": "350 × 0.1 = ", "post": "", "answer": 35, "hint": "Multiplying by 0.1 is the same as dividing by 10."},
        {"phase": "substitute", "pre": "Check: 35 ÷ 350 × 100 = ", "post": "", "answer": 10, "done": "35 is 10% of 350, correct.", "hint": "Part over whole, times 100."},
     ]},
    # B3 50% of 84 = 42
    {"hint": "50% is a half, so divide by 2.",
     "misc": [M("divide_by_number", 1.68, "50% does not mean ÷ 50. It means half: 84 ÷ 2 = 42.", "84/50=1.68")],
     "steps": [
        {"say": "50% means half. As a decimal that is 0.5.", "pre": "50 ÷ 100 = ", "post": "", "answer": 0.5, "hint": "Fifty hundredths is 0.5."},
        {"say": "Now halve 84.", "phase": "substitute", "pre": "84 × 0.5 = ", "post": "", "answer": 42, "hint": "Half of 84."},
        {"phase": "substitute", "pre": "Check: 42 ÷ 84 × 100 = ", "post": "", "answer": 50, "done": "42 is half of 84, so it is 50%. Correct.", "hint": "Part over whole, times 100."},
     ]},
    # B4 20% of 45 = 9
    {"hint": "20% means × 0.2, which is the same as ÷ 5.",
     "misc": [
        M("multiply_by_number", 900, "20% means × 0.2, not × 20. 45 × 0.2 = 9.", "45*20=900"),
        M("wrong_fraction", 2.25, "20% is ÷ 5 (not ÷ 20): 45 ÷ 5 = 9. Dividing by 20 gives 5%.", "45/20=2.25"),
     ],
     "steps": [
        {"say": "20% means 20 out of 100, which is 0.2 as a decimal.", "pre": "20 ÷ 100 = ", "post": "", "answer": 0.2, "hint": "Twenty hundredths is 0.2."},
        {"say": "Now find that much of 45.", "phase": "substitute", "pre": "45 × 0.2 = ", "post": "", "answer": 9, "hint": "One fifth of 45."},
        {"phase": "substitute", "pre": "Check: 9 ÷ 45 × 100 = ", "post": "", "answer": 20, "done": "9 is 20% of 45, correct.", "hint": "Part over whole, times 100."},
     ]},
    # B5 15% of 200 = 30
    {"hint": "Find 10%, then 5% (half of 10%), then add them.",
     "misc": [M("stopped_at_10", 20, "20 is only 10% of 200. Add another 5% (=10) to reach 15%: 20 + 10 = 30.", "found 10% only")],
     "steps": [
        {"say": "Build 15% from parts you can do in your head. Start with 10%.", "pre": "10% of 200 = 200 × 0.1 = ", "post": "", "answer": 20, "hint": "Divide 200 by 10."},
        {"say": "5% is half of 10%.", "pre": "5% of 200 = 20 ÷ 2 = ", "post": "", "answer": 10, "hint": "Half of the 10% you just found."},
        {"say": "15% is 10% plus 5%.", "phase": "substitute", "pre": "20 + 10 = ", "post": "", "answer": 30, "hint": "Add the two parts together."},
        {"phase": "substitute", "pre": "Check with a decimal: 200 × 0.15 = ", "post": "", "answer": 30, "done": "Both methods give 30, so it is right.", "hint": "15% as a decimal is 0.15."},
     ]},
    # B6 0.45 as % = 45
    {"hint": "To turn a decimal into a percentage, multiply by 100.",
     "misc": [M("wrong_direction", 0.0045, "To go from a decimal to a percentage you multiply by 100, not divide. 0.45 × 100 = 45.", "0.45/100=0.0045")],
     "steps": [
        {"say": "A decimal is already a fraction out of 100. Write 0.45 as hundredths.", "pre": "0.45 = 45 over ", "post": "", "answer": 100, "hint": "0.45 means 45 hundredths."},
        {"say": "Per cent means 'per 100', so 45 over 100 is 45%.", "phase": "substitute", "pre": "0.45 × 100 = ", "post": "", "answer": 45, "hint": "Multiply the decimal by 100."},
        {"phase": "substitute", "pre": "Check it reverses: 45 ÷ 100 = ", "post": "", "answer": 0.45, "done": "45% turns back into 0.45, so it is right.", "hint": "Dividing a percentage by 100 gives the decimal back."},
     ]},
    # B7 3/5 as % = 60
    {"hint": "Divide the top by the bottom, then multiply by 100.",
     "misc": [M("read_as_digits", 35, "Do not just read off the digits. 3 ÷ 5 = 0.6, and 0.6 × 100 = 60%.", "reads 3/5 as 35")],
     "steps": [
        {"say": "First turn the fraction into a decimal by dividing.", "pre": "3 ÷ 5 = ", "post": "", "answer": 0.6, "hint": "Three fifths is 0.6."},
        {"say": "Now turn the decimal into a percentage.", "phase": "substitute", "pre": "0.6 × 100 = ", "post": "", "answer": 60, "hint": "Multiply by 100."},
        {"phase": "substitute", "pre": "Check: 60% of 5 is 0.6 × 5 = ", "post": "", "answer": 3, "done": "60% of 5 gives back 3, so 3/5 = 60%. Correct.", "hint": "0.6 × 5 should return the numerator."},
     ]},
    # B8 5% of 160 = 8
    {"hint": "Find 10% first, then halve it to get 5%.",
     "misc": [M("divide_by_5", 32, "5% is not ÷ 5 (that gives 20%). 5% is × 0.05: 160 × 0.05 = 8.", "160/5=32")],
     "steps": [
        {"say": "5% is easiest as half of 10%. Start with 10% of 160.", "pre": "160 × 0.1 = ", "post": "", "answer": 16, "hint": "Divide 160 by 10."},
        {"say": "5% is half of 10%.", "phase": "substitute", "pre": "16 ÷ 2 = ", "post": "", "answer": 8, "hint": "Halve the 10% you found."},
        {"phase": "substitute", "pre": "Check: 8 ÷ 160 × 100 = ", "post": "", "answer": 5, "done": "8 is 5% of 160, correct.", "hint": "Part over whole, times 100."},
     ]},
]

# ============================ SILVER ============================
silver = [
    # S1 Increase 80 by 15% = 92
    {"hint": "Find 15% of 80, then add it on (or multiply by 1.15).",
     "misc": [M("percentage_only", 12, "12 is the increase, not the answer. Add it on: 80 + 12 = 92 (or 80 × 1.15).", "found 15% only")],
     "steps": [
        {"say": "First find 15% of 80. Do 10% then 5%.", "pre": "10% of 80 = ", "post": "", "answer": 8, "hint": "Divide 80 by 10."},
        {"say": "5% is half of that.", "pre": "5% of 80 = 8 ÷ 2 = ", "post": "", "answer": 4, "hint": "Half of the 10%."},
        {"say": "'Increase' means add the rise on top.", "phase": "substitute", "pre": "80 + 8 + 4 = ", "post": "", "answer": 92, "hint": "Original plus the two parts of the increase."},
        {"phase": "substitute", "pre": "Check with the multiplier: 92 ÷ 80 = ", "post": "", "answer": 1.15, "done": "1.15 means a 15% rise, so 92 is right.", "hint": "The multiplier for a 15% increase is 1.15."},
     ]},
    # S2 Decrease 250 by 20% = 200
    {"hint": "Find 20% of 250, then subtract it (or multiply by 0.8).",
     "misc": [M("percentage_only", 50, "50 is the amount taken off, not the answer. 250 − 50 = 200 (or 250 × 0.8).", "found 20% only")],
     "steps": [
        {"say": "First find 20% of 250. Start with 10%.", "pre": "10% of 250 = ", "post": "", "answer": 25, "hint": "Divide 250 by 10."},
        {"say": "20% is double 10%.", "pre": "20% of 250 = 25 × 2 = ", "post": "", "answer": 50, "hint": "Two lots of the 10%."},
        {"say": "'Decrease' means take the fall away.", "phase": "substitute", "pre": "250 − 50 = ", "post": "", "answer": 200, "hint": "Original minus the amount off."},
        {"phase": "substitute", "pre": "Check with the multiplier: 200 ÷ 250 = ", "post": "", "answer": 0.8, "done": "0.8 means a 20% drop, so 200 is right.", "hint": "The multiplier for a 20% decrease is 0.8."},
     ]},
    # S3 400 -> 340, % decrease = 15
    {"hint": "Find the change, then divide by the ORIGINAL and multiply by 100.",
     "misc": [
        M("gave_change", 60, "60 is the £ change, not the percentage. Divide by the original: 60 ÷ 400 × 100 = 15%.", "gives change in pounds"),
        M("forgot_times_100", 0.15, "After dividing you get 0.15. Multiply by 100 to make it a percentage: 15%.", "60/400=0.15 not scaled"),
     ],
     "steps": [
        {"say": "First work out how much the price fell.", "pre": "Change = 400 − 340 = ", "post": "", "answer": 60, "hint": "The drop in price."},
        {"say": "Percentage change divides by the ORIGINAL value.", "phase": "substitute", "pre": "60 ÷ 400 = ", "post": "", "answer": 0.15, "hint": "Change over the starting price."},
        {"phase": "substitute", "pre": "Turn it into a percentage: 0.15 × 100 = ", "post": "", "answer": 15, "done": "A £60 fall on £400 is a 15% decrease.", "hint": "Multiply the decimal by 100."},
     ]},
    # S4 shirt £24 after 20% off, original = 30
    {"hint": "£24 is 80% of the original. Divide by 0.8.",
     "misc": [M("add_percent", 28.8, "Do not add 20% back onto £24. £24 is 80% of the original, so divide: 24 ÷ 0.8 = 30.", "24*1.2=28.8")],
     "steps": [
        {"say": "20% off means you pay 80% of the original price.", "pre": "As a decimal, the multiplier is 0.", "post": "", "answer": 0.8, "hint": "100% − 20% = 80%, which is 0.8."},
        {"say": "The £24 is the price AFTER the discount, so reverse it by dividing.", "phase": "substitute", "pre": "24 ÷ 0.8 = ", "post": "", "answer": 30, "hint": "Divide the sale price by the multiplier."},
        {"phase": "substitute", "pre": "Check forwards: 20% off £30 is 30 × 0.8 = ", "post": "", "answer": 24, "done": "£30 with 20% off gives £24, so the original was £30.", "hint": "Take 20% off your answer and you should reach £24."},
     ]},
    # S5 36 as % of 90 = 40
    {"hint": "Divide the part (36) by the whole (90), then multiply by 100.",
     "misc": [
        M("upside_down", 250, "Divide the part by the whole, not the other way up: 36 ÷ 90 × 100 = 40, not 90 ÷ 36.", "90/36*100=250"),
        M("forgot_times_100", 0.4, "36 ÷ 90 = 0.4. Multiply by 100 to make it a percentage: 40%.", "0.4 not scaled"),
     ],
     "steps": [
        {"say": "Write 36 out of 90 as a fraction and divide.", "pre": "36 ÷ 90 = ", "post": "", "answer": 0.4, "hint": "Part over whole."},
        {"say": "Now turn the decimal into a percentage.", "phase": "substitute", "pre": "0.4 × 100 = ", "post": "", "answer": 40, "hint": "Multiply by 100."},
        {"phase": "substitute", "pre": "Check: 40% of 90 is 90 × 0.4 = ", "post": "", "answer": 36, "done": "40% of 90 is 36, so it is right.", "hint": "0.4 × 90 should return 36."},
     ]},
    # S6 pop 5000 grows 8% = 5400
    {"hint": "Find 8% of 5000, then add it on (or multiply by 1.08).",
     "misc": [M("percentage_only", 400, "400 is the growth, not the new population. Add it: 5000 + 400 = 5400 (or 5000 × 1.08).", "found 8% only")],
     "steps": [
        {"say": "First find 8% of 5000.", "pre": "5000 × 0.08 = ", "post": "", "answer": 400, "hint": "8% as a decimal is 0.08."},
        {"say": "Growth means add the increase on.", "phase": "substitute", "pre": "5000 + 400 = ", "post": "", "answer": 5400, "hint": "Original plus the growth."},
        {"phase": "substitute", "pre": "Check with the multiplier: 5400 ÷ 5000 = ", "post": "", "answer": 1.08, "done": "1.08 means an 8% rise, so 5400 is right.", "hint": "The multiplier for an 8% increase is 1.08."},
     ]},
    # S7 VAT 20% on £85 = 102
    {"hint": "Find 20% of 85, then add it to the bill (or multiply by 1.2).",
     "misc": [M("vat_separate", 17, "17 is just the VAT. The total is the bill plus the VAT: 85 + 17 = 102 (or 85 × 1.2).", "found VAT only")],
     "steps": [
        {"say": "First work out the VAT: 20% of 85.", "pre": "85 × 0.2 = ", "post": "", "answer": 17, "hint": "20% as a decimal is 0.2."},
        {"say": "The total adds the VAT to the bill.", "phase": "substitute", "pre": "85 + 17 = ", "post": "", "answer": 102, "hint": "Bill plus VAT."},
        {"phase": "substitute", "pre": "Check with the multiplier: 85 × 1.2 = ", "post": "", "answer": 102, "done": "Adding 20% VAT to £85 gives £102.", "hint": "1.2 adds the 20% in one step."},
     ]},
]

# ============================ GOLD ============================
gold = [
    # G1 12% increase -> 168000, original = 150000
    {"hint": "£168 000 is 112% of the original. Divide by 1.12.",
     "misc": [M("subtract_percent", 147840, "Do not take 12% off the new price. £168 000 is 112% of the original, so divide: 168000 ÷ 1.12 = 150000.", "168000*0.88=147840")],
     "steps": [
        {"say": "A 12% increase multiplies the original by 1.12.", "pre": "The multiplier is 1.", "post": "", "answer": 1.12, "hint": "100% + 12% = 112%, which is 1.12."},
        {"say": "£168 000 is the value AFTER the rise, so reverse it by dividing.", "phase": "substitute", "pre": "168000 ÷ 1.12 = ", "post": "", "answer": 150000, "hint": "Divide the new value by the multiplier."},
        {"phase": "substitute", "pre": "Check forwards: 150000 × 1.12 = ", "post": "", "answer": 168000, "done": "A 12% rise on £150 000 gives £168 000, so the original was £150 000.", "hint": "Add 12% to your answer and you should reach 168 000."},
     ]},
    # G2 £2000 at 3% compound, 3 yrs = 2185
    {"hint": "Multiply by 1.03 for each of the three years.",
     "misc": [M("simple_interest", 2180, "That is simple interest (3% × 3 = 9%). Compound multiplies by 1.03 each year: 2000 × 1.03³ = 2185, not 2000 × 1.09.", "2000*1.09=2180")],
     "steps": [
        {"say": "Compound interest multiplies by the same figure each year. A 3% rise is × 1.03.", "pre": "The yearly multiplier is 1.", "post": "", "answer": 1.03, "hint": "100% + 3% = 103%, which is 1.03."},
        {"say": "Apply it year by year. After 1 year:", "pre": "2000 × 1.03 = ", "post": "", "answer": 2060, "hint": "Add 3% to £2000."},
        {"say": "After the second year:", "phase": "substitute", "pre": "2060 × 1.03 = ", "post": "", "answer": 2121.8, "hint": "Multiply last year's total by 1.03 again."},
        {"phase": "substitute", "pre": "After the third year, to the nearest £: 2121.8 × 1.03 = ", "post": "", "answer": 2185, "done": "Three years of × 1.03 turns £2000 into £2185.", "hint": "2121.8 × 1.03 = 2185.45, which rounds to 2185."},
     ]},
    # G3 car 15% dep, £12000, 2 yrs = 8670
    {"hint": "Multiply by 0.85 for each of the two years.",
     "misc": [M("linear", 8400, "Depreciation is compound, not a flat 30% off. Apply 0.85 twice: 12000 × 0.85² = 8670, not 12000 × 0.70.", "12000*0.7=8400")],
     "steps": [
        {"say": "Losing 15% each year multiplies the value by 0.85.", "pre": "The yearly multiplier is 0.", "post": "", "answer": 0.85, "hint": "100% − 15% = 85%, which is 0.85."},
        {"say": "After the first year:", "pre": "12000 × 0.85 = ", "post": "", "answer": 10200, "hint": "Take 15% off £12 000."},
        {"say": "After the second year:", "phase": "substitute", "pre": "10200 × 0.85 = ", "post": "", "answer": 8670, "hint": "Take 15% off last year's value."},
        {"phase": "substitute", "pre": "Check with the power: 0.85 × 0.85 = ", "post": "", "answer": 0.7225, "done": "12000 × 0.7225 = 8670, the same answer.", "hint": "0.85 squared, then × 12 000 should match."},
     ]},
    # G4 two discounts 10% then 20%, TV £360, original = 500
    {"hint": "Combined multiplier = 0.9 × 0.8 = 0.72. Divide £360 by 0.72.",
     "misc": [
        M("multiply_forward", 259.2, "£360 is already after the discounts, so divide, not multiply: 360 ÷ 0.72 = 500.", "360*0.72=259.2"),
        M("add_discounts", 514.29, "Do not add the discounts to 30%. Multiply the multipliers: 0.9 × 0.8 = 0.72 (not 0.7), so 360 ÷ 0.72 = 500.", "360/0.7=514.29"),
     ],
     "steps": [
        {"say": "Each discount is a multiplier: 10% off is 0.9, 20% off is 0.8. Combine them.", "pre": "0.9 × 0.8 = ", "post": "", "answer": 0.72, "hint": "Multiply the two multipliers together."},
        {"say": "£360 is the price after BOTH discounts, so reverse by dividing.", "phase": "substitute", "pre": "360 ÷ 0.72 = ", "post": "", "answer": 500, "hint": "Divide the final price by 0.72."},
        {"phase": "substitute", "pre": "Check: 500 × 0.9 = 450, then 450 × 0.8 = ", "post": "", "answer": 360, "done": "£500 with 10% then 20% off gives £360, so the original was £500.", "hint": "Apply both discounts to your answer and you should reach £360."},
     ]},
    # G5 pop grows 5%/yr, first exceeds double = 15
    {"hint": "Keep multiplying by 1.05 until the total passes 2. Count the years.",
     "misc": [M("divide", 20, "Growth is compound, not linear. 100 ÷ 5 = 20 is wrong: 1.05 raised to a power grows faster, passing 2 at 15 years.", "100/5=20")],
     "steps": [
        {"say": "Doubling means the multiplier 1.05 must build up past 2. Try 14 years first.", "pre": "1.05 to the power 14 = (2 d.p.) ", "post": "", "answer": 1.98, "hint": "1.05^14 is just under 2."},
        {"say": "1.98 has not yet passed 2, so try one more year.", "phase": "substitute", "pre": "1.05 to the power 15 = (2 d.p.) ", "post": "", "answer": 2.08, "hint": "1.05^15 tips just over 2."},
        {"phase": "substitute", "pre": "The first whole year over double is year ", "post": "", "answer": 15, "done": "1.05^15 ≈ 2.08 is the first value above 2, so it takes 15 years.", "hint": "The year where the total first exceeds 2."},
     ]},
]

def apply(tier_list, tier_probs):
    for prob, spec in zip(tier_probs, tier_list):
        prob["hint"] = spec["hint"]
        prob["misconceptions"] = spec["misc"]
        prob["guided_steps"] = spec["steps"]

apply(bronze, pb["bronze"])
apply(silver, pb["silver"])
apply(gold, pb["gold"])

# ============================ tier_guides ============================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: a percentage of an amount",
        "steps": [
            "A percentage means 'out of 100'. Turn it into a decimal by dividing by 100 (25% becomes 0.25), then multiply the amount.",
            "Easy ones you can build in your head: 10% is ÷ 10, 50% is a half, 25% is a quarter, and 5% is half of 10%.",
            "To convert: a decimal becomes a percentage by <strong>× 100</strong>, and a fraction becomes a percentage by dividing top by bottom, then × 100.",
        ],
        "example": {
            "question": "Find 30% of 80",
            "steps": [
                {"label": "Convert", "content": "<p>30% = 0.3</p>"},
                {"label": "Multiply", "content": "<p>80 × 0.3 = 24</p>"},
                {"label": "Check", "content": "<p>24 ÷ 80 × 100 = 30% ✓</p>"},
                {"label": "Answer", "content": "<p><strong>24</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: increase, decrease and percentage change",
        "steps": [
            "Use a <strong>multiplier</strong>. A rise of r% is × (1 + r/100); a fall of r% is × (1 − r/100). So +15% is × 1.15 and −20% is × 0.8.",
            "To find a percentage change: (change ÷ <strong>original</strong>) × 100. Always divide by the value you started with.",
            "To reverse one change: the amount you know is a percentage of the original, so divide by the multiplier to get back.",
        ],
        "example": {
            "question": "Increase £40 by 15%",
            "steps": [
                {"label": "Multiplier", "content": "<p>+15% → × 1.15</p>"},
                {"label": "Multiply", "content": "<p>40 × 1.15 = 46</p>"},
                {"label": "Check", "content": "<p>15% of 40 = 6, and 40 + 6 = 46 ✓</p>"},
                {"label": "Answer", "content": "<p><strong>£46</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: reverse percentages and compound change",
        "steps": [
            "<strong>Reverse:</strong> if a value is already after a change, divide by the multiplier to find the original (after a 12% rise, ÷ 1.12).",
            "<strong>Compound:</strong> apply the multiplier once for every year. Three years of 3% growth is × 1.03 × 1.03 × 1.03, which is × 1.03³.",
            "Two changes in a row multiply their multipliers: 10% then 20% off is × 0.9 × 0.8 = × 0.72, not 30% off.",
        ],
        "example": {
            "question": "After a 20% rise, a price is £60. Find the original.",
            "steps": [
                {"label": "Multiplier", "content": "<p>+20% → × 1.2</p>"},
                {"label": "Reverse", "content": "<p>60 ÷ 1.2 = 50</p>"},
                {"label": "Check", "content": "<p>50 × 1.2 = 60 ✓</p>"},
                {"label": "Answer", "content": "<p><strong>£50</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ============================ guided (opener + teach) ============================
tag_svg = (
    '<svg viewBox="0 0 260 140" role="img" aria-label="A sale price tag showing 25 percent off a coat that costs 40 pounds">'
    '<path d="M34 34 L150 34 A20 20 0 0 1 170 54 L170 100 A20 20 0 0 1 150 120 L34 120 Z" '
    'fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    '<circle cx="52" cy="77" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/>'
    '<text x="108" y="72" font-family="Inter, sans-serif" font-size="17" font-weight="700" text-anchor="middle" fill="currentColor">25% OFF</text>'
    '<text x="108" y="98" font-family="Inter, sans-serif" font-size="13" text-anchor="middle" fill="currentColor">£40 coat</text>'
    '</svg>'
)

pd["guided"] = {
    "opener": {
        "label": "Before any formulas",
        "display": tag_svg,
        "steps": [
            {"say": "This coat is in a sale, look at the tag. No formulas, just common sense.",
             "pre": "25% is a quarter. A quarter of £40 is £", "post": "", "answer": 10,
             "hint": "Split £40 into four equal parts and take one part."},
            {"say": "That £10 is the saving.",
             "pre": "So at the till you pay £", "post": "", "answer": 30,
             "hint": "Take the £10 saving off the £40."},
            {"say": "You just found 25% of £40 (the saving) and took it off to get the new price. That is a <strong>percentage decrease</strong>. The whole topic is this: find a percentage of an amount, then add it on or take it off. A shortcut writes '25% off' as × 0.75, so £40 × 0.75 = £30 in one step."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Find 40% of 150",
            "label": "Together: your first one",
            "steps": [
                {"say": "Build 40% from 10%. First find 10% of 150.", "pre": "150 ÷ 10 = ", "post": "", "answer": 15, "hint": "10% means divide by 10."},
                {"say": "40% is four lots of 10%.", "pre": "15 × 4 = ", "post": "", "answer": 60, "hint": "Four times the 10% you found."},
                {"say": "Check it with the decimal method. 40% = 0.4.", "pre": "150 × 0.4 = ", "post": "", "answer": 60, "hint": "Multiplying by 0.4 should give the same answer."},
                {"say": "And prove it really is 40%.", "pre": "60 ÷ 150 × 100 = ", "post": "", "answer": 40, "done": "Both routes give 60, and it is 40% of 150. That is the whole method.", "hint": "Part over whole, times 100."},
            ],
        },
        "silver": {
            "display": "A coat costs £60. In a sale it is reduced by 25%. Find the sale price.",
            "label": "Together: the silver move",
            "steps": [
                {"say": "Find 25% of £60. Start with 10%.", "pre": "10% of 60 = ", "post": "", "answer": 6, "hint": "Divide 60 by 10."},
                {"say": "25% is 10% + 10% + 5%, and 5% is half of 10%.", "pre": "6 + 6 + 3 = ", "post": "", "answer": 15, "hint": "Two lots of 10% plus one 5%."},
                {"say": "'Reduced by' means take the discount off.", "pre": "60 − 15 = ", "post": "", "answer": 45, "hint": "Original minus the discount."},
                {"say": "Check with the multiplier. 25% off is × 0.75.", "pre": "60 × 0.75 = ", "post": "", "answer": 45, "done": "The multiplier gives 45 in one step, matching the build-up. Gone.", "hint": "0.75 does the whole discount at once."},
            ],
        },
        "gold": {
            "display": "A £5000 car loses 10% of its value each year. What is it worth after 2 years?",
            "label": "Together: the gold move",
            "steps": [
                {"say": "Losing 10% each year multiplies the value by 0.9.", "pre": "The yearly multiplier is 0.", "post": "", "answer": 0.9, "hint": "100% − 10% = 90%, which is 0.9."},
                {"say": "Apply it for the first year.", "pre": "5000 × 0.9 = ", "post": "", "answer": 4500, "hint": "Take 10% off £5000."},
                {"say": "Now the second year, on the new value.", "pre": "4500 × 0.9 = ", "post": "", "answer": 4050, "hint": "Take 10% off £4500, not off £5000."},
                {"say": "Check with the power. Two years is × 0.9².", "pre": "0.9 × 0.9 = ", "post": "", "answer": 0.81, "done": "5000 × 0.81 = 4050, the same answer. Applying the multiplier each year is the whole point.", "hint": "0.9 squared, then × 5000 should match."},
            ],
        },
    },
}

json.dump(pd, io.open("../_maths_guided/lesson_number-L05.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written lesson_number-L05.json")
