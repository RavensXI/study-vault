# -*- coding: utf-8 -*-
"""Build guided-learning practice_data for ratio-proportion-L02 (Percentages & Compound Change)."""
import json, io

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def say(text):
    return {"say": text}

# ---------------------------------------------------------------------------
# PROBLEM BANK
# ---------------------------------------------------------------------------

bronze = [
    {  # B0
        "display": "Increase £80 by 25%",
        "solutions": [100], "calculator": False, "input_type": "single_value",
        "hint": "Increase means multiply by 1.25.",
        "misconceptions": [{"check": "common", "expect": 20, "pattern": "wrong_formula",
            "message": "20 is only 25% of 80, the increase on its own. Add it back on: 80 + 20 = £100. Or multiply by 1.25 in one step."}],
        "guided_steps": [
            box("Multiplier = 1 + 0.25 = ", 1.25, "An increase adds the rate to 1: 1 + 0.25.",
                say="First the multiplier. An increase of 25% keeps the whole amount and adds a quarter, so add 0.25 to 1."),
            box("80 × 1.25 = £", 100, "80 plus a quarter of 80.",
                say="Now multiply the original by the multiplier.", phase="substitute"),
            box("100 − 80 = £", 20, "Subtract the original from your new price.",
                say="Check: the increase on its own should be 25% of 80.",
                done="20 is a quarter of 80, exactly 25%. So £100 is right."),
        ],
    },
    {  # B1
        "display": "Decrease 600 by 10%",
        "solutions": [540], "calculator": False, "input_type": "single_value",
        "hint": "Decrease means multiply by 0.9.",
        "misconceptions": [{"check": "common", "expect": 60, "pattern": "wrong_formula",
            "message": "60 is only 10% of 600, the amount taken off. Subtract it: 600 − 60 = 540. Or multiply by 0.9 in one step."}],
        "guided_steps": [
            box("Multiplier = 1 − 0.10 = ", 0.9, "A decrease takes the rate off 1: 1 − 0.1.",
                say="First the multiplier. A decrease of 10% keeps 90% of the amount, so take 0.1 off 1."),
            box("600 × 0.9 = ", 540, "600 minus 10% of 600.",
                say="Now multiply the original by the multiplier.", phase="substitute"),
            box("600 − 540 = ", 60, "Subtract your answer from the original.",
                say="Check: the amount lost should be 10% of 600.",
                done="60 is 10% of 600. So 540 is right."),
        ],
    },
    {  # B2 (REPLACED: was off-topic 'Find 15% of £320')
        "display": "Increase £320 by 15%",
        "solutions": [368], "calculator": False, "input_type": "single_value",
        "hint": "Increase means multiply by 1.15 (or find 15% and add it on).",
        "misconceptions": [{"check": "common", "expect": 48, "pattern": "wrong_formula",
            "message": "48 is only the increase (15% of 320), not the new total. Add it back on: 320 + 48 = £368. Or multiply by 1.15 in one step."}],
        "guided_steps": [
            box("Multiplier = 1 + 0.15 = ", 1.15, "An increase adds the rate to 1: 1 + 0.15.",
                say="First the multiplier. An increase of 15% adds 0.15 to 1."),
            box("320 × 1.15 = £", 368, "15% of 320 is 48, so 320 + 48.",
                say="Now multiply the original by the multiplier.", phase="substitute"),
            box("368 − 320 = £", 48, "Subtract the original from your new price.",
                say="Check: the increase on its own should be 15% of 320.",
                done="48 is 15% of 320. So £368 is right."),
        ],
    },
    {  # B3
        "display": "A shirt costs £40 and is reduced by 30%. What is the sale price?",
        "solutions": [28], "calculator": False, "input_type": "single_value",
        "hint": "Reduced by 30% means multiply by 0.7.",
        "misconceptions": [{"check": "common", "expect": 12, "pattern": "wrong_formula",
            "message": "12 is the reduction (30% of 40), not the sale price. Take it off: 40 − 12 = £28. Or multiply by 0.7 in one step."}],
        "guided_steps": [
            box("Multiplier = 1 − 0.30 = ", 0.7, "A decrease takes the rate off 1: 1 − 0.3.",
                say="First the multiplier. Reduced by 30% leaves 70% of the price, so take 0.3 off 1."),
            box("40 × 0.7 = £", 28, "40 minus 30% of 40.",
                say="Now multiply the original price by the multiplier.", phase="substitute"),
            box("40 − 28 = £", 12, "Subtract the sale price from the original.",
                say="Check: the reduction should be 30% of 40.",
                done="12 is 30% of 40. So £28 is right."),
        ],
    },
    {  # B4 (REPLACED: was off-topic 'Express 45 out of 180 as a percentage')
        "display": "A jacket costs £180. It is reduced by 45%. What is the sale price?",
        "solutions": [99], "calculator": False, "input_type": "single_value",
        "hint": "Reduced by 45% means multiply by 0.55.",
        "misconceptions": [{"check": "common", "expect": 81, "pattern": "wrong_formula",
            "message": "81 is the reduction (45% of 180), not the sale price. Take it off: 180 − 81 = £99. Or multiply by 0.55 in one step."}],
        "guided_steps": [
            box("Multiplier = 1 − 0.45 = ", 0.55, "A decrease takes the rate off 1: 1 − 0.45.",
                say="First the multiplier. Reduced by 45% leaves 55% of the price, so take 0.45 off 1."),
            box("180 × 0.55 = £", 99, "45% of 180 is 81, so 180 − 81.",
                say="Now multiply the original price by the multiplier.", phase="substitute"),
            box("180 − 99 = £", 81, "Subtract the sale price from the original.",
                say="Check: the reduction should be 45% of 180.",
                done="81 is 45% of 180. So £99 is right."),
        ],
    },
    {  # B5
        "display": "Increase 350 by 40%",
        "solutions": [490], "calculator": False, "input_type": "single_value",
        "hint": "Increase means multiply by 1.4.",
        "misconceptions": [{"check": "common", "expect": 140, "pattern": "wrong_formula",
            "message": "140 is only the increase (40% of 350), not the new total. Add it back on: 350 + 140 = 490. Or multiply by 1.4 in one step."}],
        "guided_steps": [
            box("Multiplier = 1 + 0.40 = ", 1.4, "An increase adds the rate to 1: 1 + 0.4.",
                say="First the multiplier. An increase of 40% adds 0.4 to 1."),
            box("350 × 1.4 = ", 490, "40% of 350 is 140, so 350 + 140.",
                say="Now multiply the original by the multiplier.", phase="substitute"),
            box("490 − 350 = ", 140, "Subtract the original from your new value.",
                say="Check: the increase should be 40% of 350.",
                done="140 is 40% of 350. So 490 is right."),
        ],
    },
    {  # B6
        "display": "A bike costs £200 plus 20% VAT. What is the total price?",
        "solutions": [240], "calculator": False, "input_type": "single_value",
        "hint": "Adding 20% VAT means multiply by 1.2.",
        "misconceptions": [{"check": "common", "expect": 40, "pattern": "wrong_formula",
            "message": "40 is only the VAT (20% of 200), not the total. Add it back on: 200 + 40 = £240. Or multiply by 1.2 in one step."}],
        "guided_steps": [
            box("Multiplier = 1 + 0.20 = ", 1.2, "Adding VAT is an increase: 1 + 0.2.",
                say="First the multiplier. Adding 20% VAT adds 0.2 to 1."),
            box("200 × 1.2 = £", 240, "200 plus 20% of 200.",
                say="Now multiply the price before VAT by the multiplier.", phase="substitute"),
            box("240 − 200 = £", 40, "Subtract the price before VAT from the total.",
                say="Check: the VAT added should be 20% of 200.",
                done="40 is 20% of 200. So £240 is right."),
        ],
    },
    {  # B7
        "display": "Decrease 480 by 25%",
        "solutions": [360], "calculator": False, "input_type": "single_value",
        "hint": "Decrease means multiply by 0.75.",
        "misconceptions": [{"check": "common", "expect": 120, "pattern": "wrong_formula",
            "message": "120 is only 25% of 480, the amount taken off. Subtract it: 480 − 120 = 360. Or multiply by 0.75 in one step."}],
        "guided_steps": [
            box("Multiplier = 1 − 0.25 = ", 0.75, "A decrease takes the rate off 1: 1 − 0.25.",
                say="First the multiplier. A decrease of 25% keeps 75% of the amount, so take 0.25 off 1."),
            box("480 × 0.75 = ", 360, "480 minus a quarter of 480.",
                say="Now multiply the original by the multiplier.", phase="substitute"),
            box("480 − 360 = ", 120, "Subtract your answer from the original.",
                say="Check: the amount lost should be 25% of 480.",
                done="120 is a quarter of 480, exactly 25%. So 360 is right."),
        ],
    },
]

silver = [
    {  # S0
        "display": "£3,000 is invested at 5% compound interest for 2 years. What is the final amount?",
        "solutions": [3307.5], "calculator": True, "input_type": "single_value",
        "hint": "Compound: multiply by 1.05 raised to the power 2.",
        "misconceptions": [{"check": "common", "expect": 3300, "pattern": "wrong_formula",
            "message": "3000 × 1.05² = 3000 × 1.1025 = £3307.50. Adding 5% twice would give simple interest of £3300, not compound."}],
        "guided_steps": [
            box("Multiplier = 1 + 0.05 = ", 1.05, "Add the rate as a decimal to 1.",
                say="Compound interest is a repeated increase. First the yearly multiplier for 5%."),
            box("1.05² = ", 1.1025, "1.05 × 1.05.",
                say="It runs for 2 years, so raise the multiplier to the power 2."),
            box("3000 × 1.1025 = £", 3307.5, "Multiply 3000 by 1.1025.",
                say="Now multiply the starting amount by this single factor.", phase="substitute"),
            box("3307.50 − 3000 = £", 307.5, "Subtract the starting amount.",
                say="Check the interest earned.",
                done="£307.50 interest on £3000 over 2 years at 5% compound. So £3307.50 is right."),
        ],
    },
    {  # S1
        "display": "A car depreciates by 20% each year. It is worth £10,000 now. What will it be worth in 2 years?",
        "solutions": [6400], "calculator": True, "input_type": "single_value",
        "hint": "Depreciation of 20% means multiply by 0.8 each year, so use 0.8 squared.",
        "misconceptions": [{"check": "common", "expect": 6000, "pattern": "wrong_formula",
            "message": "10000 × 0.8² = 10000 × 0.64 = £6400. Taking off 40% in one go (£6000) ignores that the second year's 20% is smaller."}],
        "guided_steps": [
            box("Multiplier = 1 − 0.20 = ", 0.8, "A decrease takes the rate off 1: 1 − 0.2.",
                say="Depreciation is a repeated decrease. First the yearly multiplier for 20%."),
            box("0.8² = ", 0.64, "0.8 × 0.8.",
                say="Over 2 years, raise the multiplier to the power 2."),
            box("10000 × 0.64 = £", 6400, "Multiply 10000 by 0.64.",
                say="Now multiply the current value by this factor.", phase="substitute"),
            box("10000 − 6400 = £", 3600, "Subtract your answer from 10000.",
                say="Check the value lost over the 2 years.",
                done="The car lost £3600 of its £10000 value. So £6400 is right."),
        ],
    },
    {  # S2
        "display": "A population of 50,000 grows by 2% per year. What is the population after 3 years? Round to the nearest whole number.",
        "solutions": [53060], "calculator": True, "input_type": "single_value",
        "hint": "Multiply by 1.02 cubed, then round.",
        "misconceptions": [{"check": "common", "expect": 53000, "pattern": "wrong_formula",
            "message": "50000 × 1.02³ = 50000 × 1.061208 = 53060. Adding 6% in one go (53000) ignores that each year grows the new, larger population."}],
        "guided_steps": [
            box("Multiplier = 1 + 0.02 = ", 1.02, "Add the rate as a decimal to 1.",
                say="Growth is a repeated increase. First the yearly multiplier for 2%."),
            box("1.02³ = ", 1.061208, "1.02 × 1.02 × 1.02.",
                say="Over 3 years, raise the multiplier to the power 3."),
            box("50000 × 1.061208 = ", 53060.4, "Multiply 50000 by 1.061208.",
                say="Now multiply the starting population by this factor.", phase="substitute"),
            box("Round to the nearest whole person: ", 53060, "53060.4 rounds down to 53060.",
                say="The question asks for a whole number of people.",
                done="53060 people after 3 years of 2% growth. That matches."),
        ],
    },
    {  # S3
        "display": "What multiplier represents a 7.5% increase?",
        "solutions": [1.075], "calculator": False, "input_type": "single_value",
        "hint": "An increase adds to 1: 1 plus 0.075.",
        "misconceptions": [{"check": "common", "expect": 0.075, "pattern": "wrong_formula",
            "message": "1 + 0.075 = 1.075. Writing 0.075 gives only the extra bit, not the whole amount plus the extra."}],
        "guided_steps": [
            box("7.5 ÷ 100 = ", 0.075, "Divide by 100: move the point two places.",
                say="An increase keeps the whole original (100%) and adds the extra. First write 7.5% as a decimal."),
            box("1 + 0.075 = ", 1.075, "Add 0.075 to 1.",
                say="An increase adds this to 1, the 100% you keep.", phase="substitute"),
            box("As a percentage, (1.075 − 1) × 100 = ", 7.5, "Multiply the decimal part by 100.",
                say="Check by reading it back: a multiplier of 1.075 keeps 100% and adds how much?",
                done="7.5% extra, exactly the increase asked for. So 1.075 is right."),
        ],
    },
    {  # S4
        "display": "What multiplier represents a 35% decrease?",
        "solutions": [0.65], "calculator": False, "input_type": "single_value",
        "hint": "A decrease takes away from 1: 1 minus 0.35.",
        "misconceptions": [{"check": "common", "expect": 0.35, "pattern": "wrong_formula",
            "message": "1 − 0.35 = 0.65. Writing 0.35 gives only the part removed, not the part that is left."}],
        "guided_steps": [
            box("35 ÷ 100 = ", 0.35, "Divide by 100: move the point two places.",
                say="A decrease keeps what is left after taking the percentage away. First write 35% as a decimal."),
            box("1 − 0.35 = ", 0.65, "Subtract 0.35 from 1.",
                say="A decrease takes this off 1, the 100% you started with.", phase="substitute"),
            box("Read it back: 1 − 0.65 = ", 0.35, "Subtract the multiplier from 1.",
                say="Check: how much has been taken off?",
                done="0.35 taken off, exactly the 35% decrease. So 0.65 is right."),
        ],
    },
    {  # S5
        "display": "A house increases in value by 4% per year. It is currently worth £180,000. What will it be worth in 5 years? Give your answer to the nearest pound.",
        "solutions": [218998], "calculator": True, "input_type": "single_value",
        "hint": "Multiply by 1.04 to the power 5, then round to the nearest pound.",
        "misconceptions": [{"check": "common", "expect": 216000, "pattern": "wrong_formula",
            "message": "180000 × 1.04⁵ = 180000 × 1.2166529 ≈ £218,998. £216,000 comes from adding 4% five times (a 20% rise), which is simple interest, not compound."}],
        "guided_steps": [
            box("Multiplier = 1 + 0.04 = ", 1.04, "Add the rate as a decimal to 1.",
                say="Growth is a repeated increase. First the yearly multiplier for 4%."),
            box("1.04⁵ = ", 1.2166529, "1.04 to the power 5.",
                say="Over 5 years, raise the multiplier to the power 5."),
            box("180000 × 1.2166529 = £", 218997.52, "Multiply 180000 by the multiplier.",
                say="Now multiply the current value by this factor.", phase="substitute"),
            box("Round to the nearest pound: £", 218998, "218997.52 rounds up to 218998.",
                say="The question asks for the nearest pound.",
                done="£218,998 after 5 years of 4% growth. That matches."),
        ],
    },
    {  # S6
        "display": "£8,000 depreciates at 12% per year for 3 years. Find the final value to the nearest penny.",
        "solutions": [5451.78], "calculator": True, "input_type": "single_value",
        "hint": "Multiply by 0.88 cubed, then round to the nearest penny.",
        "misconceptions": [{"check": "common", "expect": 5120, "pattern": "wrong_formula",
            "message": "8000 × 0.88³ = 8000 × 0.681472 = £5451.78. £5120 comes from taking off 36% (12% × 3) in one go, which ignores compounding."}],
        "guided_steps": [
            box("Multiplier = 1 − 0.12 = ", 0.88, "A decrease takes the rate off 1: 1 − 0.12.",
                say="Depreciation is a repeated decrease. First the yearly multiplier for 12%."),
            box("0.88³ = ", 0.681472, "0.88 × 0.88 × 0.88.",
                say="Over 3 years, raise the multiplier to the power 3."),
            box("8000 × 0.681472 = £", 5451.776, "Multiply 8000 by 0.681472.",
                say="Now multiply the starting value by this factor.", phase="substitute"),
            box("Round to the nearest penny: £", 5451.78, "5451.776 rounds to 5451.78.",
                say="The question asks for the nearest penny.",
                done="£5451.78 left after 3 years of 12% depreciation. That matches."),
        ],
    },
]

gold = [
    {  # G0
        "display": "After a 15% increase, a TV costs £460. What was the original price?",
        "solutions": [400], "calculator": True, "input_type": "single_value",
        "hint": "Reverse percentage: divide 460 by 1.15.",
        "misconceptions": [{"check": "common", "expect": 391, "pattern": "wrong_formula",
            "message": "Divide by the multiplier: 460 ÷ 1.15 = £400. Do NOT find 15% of £460 and subtract."}],
        "guided_steps": [
            box("Multiplier = 1 + 0.15 = ", 1.15, "An increase adds the rate to 1.",
                say="A reverse percentage. £460 is the price AFTER a 15% increase, so it is the original times the multiplier. Find that multiplier first."),
            box("460 ÷ 1.15 = £", 400, "Divide, do not multiply: 460 ÷ 1.15.",
                say="To undo the increase, divide the final price by the multiplier.", phase="substitute"),
            box("400 × 1.15 = £", 460, "Multiply your answer by 1.15.",
                say="Check by going forwards: the original plus 15% should give £460.",
                done="It lands back on £460, so the original was £400."),
        ],
    },
    {  # G1
        "display": "A painting decreased in value by 8% and is now worth £1,380. What was it worth before the decrease?",
        "solutions": [1500], "calculator": True, "input_type": "single_value",
        "hint": "Reverse percentage: divide 1380 by 0.92.",
        "misconceptions": [{"check": "common", "expect": 1490.4, "pattern": "wrong_formula",
            "message": "Divide by the multiplier: 1380 ÷ 0.92 = £1500. Adding 8% to £1,380 (giving £1,490.40) applies the 8% to the new price, but it applied to the original."}],
        "guided_steps": [
            box("Multiplier = 1 − 0.08 = ", 0.92, "A decrease takes the rate off 1.",
                say="A reverse percentage. £1,380 is the value AFTER an 8% decrease, so it is the original times the multiplier. Find that multiplier first."),
            box("1380 ÷ 0.92 = £", 1500, "Divide, do not multiply: 1380 ÷ 0.92.",
                say="To undo the decrease, divide the final value by the multiplier.", phase="substitute"),
            box("1500 × 0.92 = £", 1380, "Multiply your answer by 0.92.",
                say="Check by going forwards: the original minus 8% should give £1,380.",
                done="It lands back on £1,380, so the original was £1,500."),
        ],
    },
    {  # G2
        "display": "After 2 years of 5% compound interest, an investment is worth £5,512.50. What was the original investment?",
        "solutions": [5000], "calculator": True, "input_type": "single_value",
        "hint": "Reverse compound: divide by 1.05 squared.",
        "misconceptions": [{"check": "common", "expect": 5250, "pattern": "wrong_formula",
            "message": "Divide by 1.05² = 1.1025: 5512.50 ÷ 1.1025 = £5000. Dividing by 1.05 only undoes one year, not two."}],
        "guided_steps": [
            box("Multiplier = 1 + 0.05 = ", 1.05, "An increase adds the rate to 1.",
                say="A reverse compound problem. The final amount is the original times 1.05, twice over. First the yearly multiplier."),
            box("1.05² = ", 1.1025, "1.05 × 1.05.",
                say="Two years means the total factor is 1.05 squared."),
            box("5512.50 ÷ 1.1025 = £", 5000, "Divide: 5512.5 ÷ 1.1025.",
                say="Undo it by dividing the final amount by this factor.", phase="substitute"),
            box("5000 × 1.1025 = £", 5512.5, "Multiply 5000 by 1.1025.",
                say="Check by going forwards.",
                done="It lands back on £5,512.50, so the original was £5,000."),
        ],
    },
    {  # G3
        "display": "A car was worth \\(£16{,}000\\). After 3 years at \\(x\\%\\) depreciation it is worth \\(£11{,}664\\). Find the annual rate of depreciation.",
        "solutions": [10], "calculator": True, "input_type": "single_value",
        "hint": "Divide final by original, take the cube root, then subtract from 1.",
        "misconceptions": [
            {"check": "equals_27.1", "expect": 27.1, "pattern": "simple_percentage_drop",
             "message": "You have found the overall percentage drop over all three years. To find the annual rate, take the cube root of the total factor (11664 ÷ 16000), then subtract from 1 and multiply by 100."},
            {"check": "equals_9.03", "expect": 9.03, "pattern": "divides_total_loss_by_years",
             "message": "Dividing the total loss by 3 gives the average money lost per year, not the compound rate. Depreciation multiplies each year, so take the cube root of 11664 ÷ 16000 to find the annual multiplier."},
            {"check": "equals_90", "expect": 90.0, "pattern": "omits_subtraction_from_1",
             "message": "You have correctly found the annual multiplier (0.9), but the rate of depreciation is 1 minus that multiplier: 1 − 0.9 = 0.1, so the answer is 10%, not 90%."},
            {"check": "equals_11.11", "expect": 11.11, "pattern": "inverts_the_ratio",
             "message": "You have divided the larger value by the smaller. Write the fraction as final ÷ original, that is 11664 ÷ 16000, then take the cube root and subtract from 1."},
        ],
        "guided_steps": [
            box("11664 ÷ 16000 = ", 0.729, "Divide the final value by the starting value.",
                say="First find the total factor over the 3 years: divide the final value by the original."),
            box("Cube root of 0.729 = ", 0.9, "What number cubed gives 0.729? Try 0.9 × 0.9 × 0.9.",
                say="That factor is the yearly multiplier applied 3 times, so it is (multiplier) cubed. Undo the power with a cube root."),
            box("1 − 0.9 = ", 0.1, "Subtract the multiplier from 1.",
                say="The yearly multiplier is 0.9. The rate is what was taken off each year: 1 minus the multiplier.", phase="substitute"),
            box("As a percentage: 0.1 × 100 = ", 10, "Multiply by 100.",
                say="Turn the decimal into a percentage."),
            box("16000 × 0.9 × 0.9 × 0.9 = £", 11664, "Work out 16000 × 0.729.",
                say="Check by going forwards: does £16,000 fall to £11,664 at 10% a year?",
                done="16000 × 0.9 three times gives 11664. So 10% a year is right."),
        ],
    },
    {  # G4
        "display": "A sale offers 20% off, then a further 10% off the sale price. What is the overall percentage decrease?",
        "solutions": [28], "calculator": False, "input_type": "single_value",
        "hint": "Multiply the two multipliers 0.8 and 0.9, then subtract from 1.",
        "misconceptions": [{"check": "common", "expect": 30, "pattern": "wrong_formula",
            "message": "Overall multiplier = 0.80 × 0.90 = 0.72. Decrease = 1 − 0.72 = 0.28 = 28%. NOT 30%: the second 10% comes off a smaller price."}],
        "guided_steps": [
            box("Multiplier = 1 − 0.20 = ", 0.8, "A decrease takes the rate off 1: 1 − 0.2.",
                say="Two decreases one after the other. Turn each into a multiplier. First, 20% off:"),
            box("Multiplier = 1 − 0.10 = ", 0.9, "A decrease takes the rate off 1: 1 − 0.1.",
                say="Then a further 10% off the reduced price:"),
            box("0.8 × 0.9 = ", 0.72, "Multiply the two multipliers together.",
                say="Apply both changes by multiplying the two multipliers into one overall factor."),
            box("1 − 0.72 = ", 0.28, "Subtract the overall multiplier from 1.",
                say="The overall multiplier is 0.72, so 72% of the price remains. The decrease is what is missing from 1.", phase="substitute"),
            box("As a percentage: 0.28 × 100 = ", 28, "Multiply by 100.",
                say="Turn the decimal into a percentage."),
            box("On £100: after 20% off £80, then 10% off £80 leaves £72, so 100 − 72 = ", 28, "The drop from £100 down to £72.",
                say="Check with a real price of £100.",
                done="£100 falls to £72, a £28 drop, which is 28%. Not 30%."),
        ],
    },
]

problem_bank = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "One percentage increase or decrease, done in your head with a multiplier.",
    "silver_description": "Compound change: the same percentage applied over several years using a power.",
    "gold_description": "Work backwards from a final amount, or find an unknown rate.",
}

# ---------------------------------------------------------------------------
# TIER GUIDES
# ---------------------------------------------------------------------------

tier_guides = {
    "bronze": {
        "title": "Bronze: one percentage change",
        "steps": [
            "A single increase or decrease. Turn the percentage into a <strong>multiplier</strong>: an increase of \\(r\\%\\) is \\(1 + \\frac{r}{100}\\), a decrease is \\(1 - \\frac{r}{100}\\).",
            "Multiply the original amount by the multiplier. A 25% rise uses 1.25, a 30% fall uses 0.70.",
            "Check by finding the change on its own: it should equal that percentage of the original.",
        ],
        "example": {
            "question": "Increase £60 by 20%",
            "steps": [
                {"label": "Multiplier", "content": "<p>Increase of 20%: \\(1 + 0.20 = 1.20\\)</p>"},
                {"label": "Multiply", "content": "<p>\\(60 \\times 1.20 = £72\\)</p>"},
                {"label": "Check", "content": "<p>Increase \\(= 72 - 60 = 12\\), and \\(20\\%\\) of \\(60 = 12\\) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>£72</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: compound change",
        "steps": [
            "The same percentage is applied again and again. Find the yearly multiplier once, exactly as in bronze.",
            "Then raise it to the power of the number of years: \\(\\text{Final} = \\text{Original} \\times (\\text{multiplier})^n\\).",
            "Two 10% rises are NOT one 20% rise: each change acts on the new amount, so always use the power, never repeated addition.",
        ],
        "example": {
            "question": "£2,000 at 10% compound interest for 3 years",
            "steps": [
                {"label": "Multiplier", "content": "<p>Increase of 10%: \\(1 + 0.10 = 1.10\\)</p>"},
                {"label": "Power", "content": "<p>3 years: \\(1.10^3 = 1.331\\)</p>"},
                {"label": "Multiply", "content": "<p>\\(2000 \\times 1.331 = £2662\\)</p>"},
                {"label": "Check", "content": "<p>Interest \\(= 2662 - 2000 = £662\\) over 3 years ✓</p>"},
                {"label": "Answer", "content": "<p><strong>£2,662</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: reverse percentages and hidden rates",
        "steps": [
            "You are given the amount AFTER a change and must work backwards. The final amount is original × multiplier, so <strong>divide</strong> by the multiplier to undo it.",
            "For compound, divide by \\((\\text{multiplier})^n\\). To find an unknown rate, divide final by original, take the \\(n\\)th root, then subtract from 1.",
            "Never just take the percentage off the final amount: the percentage applied to the original, not the new value.",
        ],
        "example": {
            "question": "After a 25% increase, a coat costs £75. Find the original price.",
            "steps": [
                {"label": "Multiplier", "content": "<p>Increase of 25%: \\(1 + 0.25 = 1.25\\)</p>"},
                {"label": "Divide back", "content": "<p>Original \\(= 75 \\div 1.25 = £60\\)</p>"},
                {"label": "Check", "content": "<p>Forwards: \\(60 \\times 1.25 = £75\\) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>£60</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# GUIDED (opener + teach walks)
# ---------------------------------------------------------------------------

guided = {
    "opener": {
        "label": "Before any formulas",
        "display": "SALE: everything 10% off<br>Jacket: £50",
        "steps": [
            box("So you pay £50 − £5 = £", 45, "Take the £5 off the £50.",
                say="No formulas yet. A £50 jacket has 10% off. 10% of £50 is £5."),
            {"say": "That is the whole method. Taking 10% off is the same as keeping 90%, and 90% as a decimal is 0.90, so £50 × 0.90 = £45 in one step. That 0.90 is called the <strong>multiplier</strong>."},
            box("So you finally pay £45 − £4.50 = £", 40.5, "Take £4.50 off £45.",
                say="Now the twist. At the till you get a loyalty 10% off the £45 as well. 10% of £45 is £4.50."),
            {"say": "Two 10%-offs did NOT make 20% off (that would be £40). Each cut comes off a smaller price, so they stack up: \\(£50 \\times 0.90 \\times 0.90 = £40.50\\). Raising the multiplier to a power is all <strong>compound change</strong> is."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Increase £60 by 20%",
            "label": "Together: your first one",
            "steps": [
                box("Multiplier = 1 + 0.20 = ", 1.2, "Add the rate as a decimal to 1.",
                    say="Bronze is one percentage change, done with a multiplier. This is an increase of 20%, so add 0.20 to 1."),
                box("60 × 1.2 = £", 72, "60 plus 20% of 60.",
                    say="Now multiply the original amount by it."),
                box("The increase alone: 72 − 60 = £", 12, "Subtract the original from the new price.",
                    say="Read the answer back to be sure."),
                box("20% of 60 = 0.2 × 60 = £", 12, "Multiply 60 by 0.2.",
                    say="And that increase should be 20% of 60.",
                    done="12 matches, so £72 is right. That is the whole bronze move."),
            ],
        },
        "silver": {
            "display": "£2,000 at 10% compound interest for 3 years",
            "label": "Together: the silver move",
            "steps": [
                box("Multiplier = 1 + 0.10 = ", 1.1, "Add the rate as a decimal to 1.",
                    say="Silver adds compounding: the same percentage applied several times. First the yearly multiplier for a 10% increase."),
                box("1.1³ = ", 1.331, "1.1 × 1.1 × 1.1.",
                    say="It runs for 3 years, so raise the multiplier to the power 3."),
                box("2000 × 1.331 = £", 2662, "Multiply 2000 by 1.331.",
                    say="Multiply the starting amount by this single factor."),
                box("2662 − 2000 = £", 662, "Subtract the starting amount.",
                    say="Check the interest earned looks right for 3 years.",
                    done="£662 interest on £2000 over 3 years at 10% compound. The power did the work: that is the silver move."),
            ],
        },
        "gold": {
            "display": "After a 25% increase, a coat costs £75. Find the original price.",
            "label": "Together: the gold move",
            "steps": [
                box("Multiplier = 1 + 0.25 = ", 1.25, "An increase adds the rate to 1.",
                    say="Gold works backwards. £75 is the price AFTER a 25% increase, so it equals the original times the multiplier. Find that multiplier."),
                box("75 ÷ 1.25 = £", 60, "Divide the final price by the multiplier.",
                    say="The final price is original × 1.25. To get back to the original, divide instead of multiply."),
                box("60 × 1.25 = £", 75, "Multiply your answer by 1.25.",
                    say="Check by going forwards: the original plus 25% should return £75.",
                    done="It lands back on £75, so the original was £60. Dividing by the multiplier is the gold move."),
                box("25% of 75 = 0.25 × 75 = £", 18.75, "Multiply 75 by 0.25.",
                    say="One trap to avoid: taking 25% off the £75 gives a different, wrong number. See it.",
                    done="£75 − £18.75 = £56.25, which is NOT the original. Always divide by the multiplier instead."),
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# METHOD CARD (slim)
# ---------------------------------------------------------------------------

method_card = {
    "title": "Percentages & Compound Change",
    "steps": [
        "Increase of \\(r\\%\\): multiply by \\(1 + \\frac{r}{100}\\). Decrease: multiply by \\(1 - \\frac{r}{100}\\).",
        "Compound change over \\(n\\) years: \\(\\text{Final} = \\text{Original} \\times (\\text{multiplier})^n\\).",
        "Reverse percentage: divide the final amount by the multiplier to find the original.",
        "Unknown rate: divide final by original, take the \\(n\\)th root, subtract from 1.",
    ],
    "content": "<p>A <strong>multiplier</strong> turns a percentage change into one multiplication. Increase by 20% means \\(\\times 1.20\\); decrease by 15% means \\(\\times 0.85\\).</p><p><strong>Compound change</strong> applies the same percentage repeatedly, so raise the multiplier to a power: \\(\\text{Final} = \\text{Original} \\times (1 \\pm \\frac{r}{100})^n\\).</p><p>For a <strong>reverse percentage</strong>, the amount you are given is the original already multiplied, so divide by the multiplier to get back. Do not take the percentage off the final amount: it was applied to the original.</p>",
    "example": "<p><strong>A car worth £12,000 depreciates by 15% per year. Value after 3 years?</strong></p><p>Multiplier \\(= 0.85\\). Value \\(= 12000 \\times 0.85^3 = 12000 \\times 0.614125 = £7369.50\\)</p>",
}

# ---------------------------------------------------------------------------
# Assemble: preserve related_videos & topic_links; fix worked_examples labels.
# ---------------------------------------------------------------------------

live = json.load(io.open("_live_ratio_L02.json", encoding="utf-8"))

worked_examples = live["worked_examples"]
for we in worked_examples:
    for st in we["steps"]:
        if "—" in st.get("label", ""):
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "problem_bank": problem_bank,
    "related_videos": live["related_videos"],
    "worked_examples": worked_examples,
    "tier_guides": tier_guides,
    "guided": guided,
}

json.dump(out, io.open("lesson_ratio-proportion-L02.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written lesson_ratio-proportion-L02.json")

# quick self-scan for em dashes
import re
def scan(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note", "guided_skip_reason"): continue
            scan(v, path + "." + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): scan(v, path + "[%d]" % i)
    elif isinstance(o, str) and "—" in o:
        print("EM DASH at", path, ":", o[:60])
scan(out, "pd")
print("em-dash scan done")
