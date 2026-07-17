# -*- coding: utf-8 -*-
import json

SRC = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_eduqas_L02.json"
OUT = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_ratio-proportion-L02.json"

pd = json.load(open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]

# ---- 1. Fix the two wrong answers (option[0] is always the correct one) ----
pb["silver"][5]["options"][0] = r"\(\pounds 6749.18\)"   # 6000*1.04^3 = 6749.184
pb["gold"][4]["options"][0] = "68 699"                    # 80000*0.97^5 = 68698.72

# ---- 2/3. Per-problem hint + honest, distractor-mapped misconceptions ----
# expect = INDEX of the distractor option the error lands on (board MC convention).
BRONZE_MC = [
    # 0: 25% of £60 -> [15,20,12,25]
    ("A quarter of £60. Split £60 into four equal parts.", [
        ("used_20pct", 2, r"£12 is 20% of £60 (dividing by 5). 25% is a quarter, so £60 ÷ 4 = £15."),
        ("copied_number", 3, r"£25 just copies the 25 from 25%. It means a quarter of £60, which is £15."),
    ]),
    # 1: 10% of 340 -> [34,3.4,340,3400]
    ("To find 10%, divide by 10.", [
        ("found_1pct", 1, r"3.4 is 1% of 340 (dividing by 100). For 10%, divide by 10: 340 ÷ 10 = 34."),
        ("no_change", 2, r"340 is the whole amount unchanged. 10% means one tenth: 340 ÷ 10 = 34."),
    ]),
    # 2: Increase £200 by 15% -> [230,215,170,30]
    ("Find 15% of £200, then add it on. Or multiply by 1.15.", [
        ("found_change_only", 3, r"£30 is 15% of £200, the increase on its own. Add it back: 200 + 30 = £230."),
        ("decreased", 2, r"£170 has 15% taken off. The question says increase, so add: £230."),
        ("added_flat_15", 1, r"£215 adds a flat £15. 15% of £200 is £30, so 200 + 30 = £230."),
    ]),
    # 3: Decrease 80 by 20% -> [64,60,16,96]
    ("Find 20% of 80, then subtract. Or multiply by 0.8.", [
        ("found_change_only", 2, r"16 is 20% of 80, the amount removed. Take it off: 80 − 16 = 64."),
        ("increased", 3, r"96 adds 20% instead. Decrease means subtract: 80 − 16 = 64."),
        ("subtracted_flat", 1, r"60 takes off a flat 20. 20% of 80 is 16, so 80 − 16 = 64."),
    ]),
    # 4: Shirt £35 reduced 10% -> [31.50,38.50,25,3.50]
    ("Reduced by 10% means multiply by 0.9 (or take 10% off).", [
        ("increased", 1, r"£38.50 adds 10%. Reduced means subtract: 35 − 3.50 = £31.50."),
        ("found_discount_only", 3, r"£3.50 is the 10% discount, not the price. Take it off £35: £31.50."),
        ("subtracted_flat", 2, r"£25 takes off a flat £10. 10% of £35 is £3.50, so £31.50."),
    ]),
    # 5: 0.35 as % -> [35%,3.5%,0.35%,350%]
    ("Multiply a decimal by 100 to make it a percentage.", [
        ("times_10", 1, r"3.5% only multiplies by 10. A decimal becomes a percentage by ×100: 0.35 × 100 = 35%."),
        ("just_added_sign", 2, r"0.35% just adds a % sign. Multiply by 100 first: 0.35 × 100 = 35%."),
        ("times_1000", 3, r"350% multiplies by 1000. It is only ×100: 35%."),
    ]),
    # 6: 18 out of 60 -> [30%,18%,33.3%,42%]
    ("Divide the part by the whole, then multiply by 100.", [
        ("copied_part", 1, r"18% just copies the 18. Divide part by whole: 18 ÷ 60 = 0.3 = 30%."),
        ("used_other_part", 3, r"42 is 60 − 18, the part left over. The question wants 18 as a percentage: 30%."),
    ]),
    # 7: 40% of 250 -> [100,150,40,90]
    ("40% = 0.4. Multiply 250 by 0.4.", [
        ("copied_number", 2, r"40 just repeats the 40 from 40%. 40% of 250 is 0.4 × 250 = 100."),
        ("used_complement", 1, r"150 is 60% of 250, what is left after 40%. The question wants 40%: 100."),
    ]),
]

SILVER_MC = [
    # 0: £8000 5% simple 3yr, total interest -> [1200,400,1261.00,9200]
    ("Simple interest: find one year, then multiply by 3.", [
        ("one_year_only", 1, r"£400 is one year's interest. Simple interest repeats it: 400 × 3 = £1200."),
        ("used_compound", 2, r"£1261 is the compound interest. This is simple interest: 8000 × 0.05 × 3 = £1200."),
        ("gave_total", 3, r"£9200 is the final balance (8000 + 1200). The question asks for the interest: £1200."),
    ]),
    # 1: pop 50000 +2% after 1yr -> [51000,50200,52000,50020]
    ("Find 2% of 50 000, then add it on.", [
        ("tenth_of_change", 1, r"50 200 adds only 200. 2% of 50 000 is 1000, so the total is 51 000."),
        ("doubled_change", 2, r"52 000 adds 2000. 2% of 50 000 is 1000, not 2000, giving 51 000."),
    ]),
    # 2: car £16000 -10% after 2yr -> [12960,12800,14400,11520]
    ("Multiply by 0.9 each year, so use 0.9 squared.", [
        ("took_20pct_once", 1, r"£12 800 takes 20% off in one go. Depreciation compounds: 16000 × 0.9² = £12 960."),
        ("one_year_only", 2, r"£14 400 is after 1 year. Apply 0.9 again for year 2: 14400 × 0.9 = £12 960."),
    ]),
    # 3: £45 as % of £180 -> [25%,45%,4%,75%]
    ("Divide 45 by 180, then multiply by 100.", [
        ("copied_part", 1, r"45% just repeats the 45. Divide part by whole: 45 ÷ 180 = 0.25 = 25%."),
        ("divided_backwards", 2, r"4 comes from 180 ÷ 45, the wrong way round. It is 45 ÷ 180 = 25%."),
    ]),
    # 4: house 150000->180000 % profit -> [20%,30%,16.7%,£30000]
    ("Divide the profit by the ORIGINAL price, then ×100.", [
        ("used_selling_price", 2, r"16.7% divides by the selling price. Percentage change uses the original: 30000 ÷ 150000 = 20%."),
        ("gave_amount", 3, r"£30 000 is the cash profit, not a percentage. As a percentage of 150 000 it is 20%."),
    ]),
    # 5: £6000 4% compound 3yr -> [6749.18,6720,7200,6240]
    ("Multiply by 1.04 cubed.", [
        ("simple_interest", 1, r"£6720 uses simple interest (6000 + 3 × 240). Compound needs 6000 × 1.04³ = £6749.18."),
        ("one_year_only", 3, r"£6240 is after 1 year. Apply 1.04 three times: 6000 × 1.04³ = £6749.18."),
    ]),
    # 6: VAT 20% on £85 -> [102,105,68,17]
    ("Adding 20% VAT means multiply by 1.2.", [
        ("found_vat_only", 3, r"£17 is the VAT (20% of 85). Add it on: 85 + 17 = £102."),
        ("subtracted", 2, r"£68 takes the VAT off. VAT is added: 85 × 1.2 = £102."),
        ("added_flat", 1, r"£105 adds a flat £20. 20% of £85 is £17, so £102."),
    ]),
]

GOLD_MC = [
    # 0: after 25% inc price £60, original -> [48,45,75,80]
    ("Reverse percentage: divide £60 by 1.25.", [
        ("took_pct_off", 1, r"£45 takes 25% off £60. The £60 is already after the rise, so divide: 60 ÷ 1.25 = £48."),
        ("multiplied", 2, r"£75 multiplies 60 × 1.25. To undo an increase, divide: 60 ÷ 1.25 = £48."),
        ("wrong_multiplier", 3, r"£80 divides by 0.75. A 25% increase uses 1.25: 60 ÷ 1.25 = £48."),
    ]),
    # 1: after 30% red sofa £350, original -> [500,455,1166.67,245]
    ("Reverse percentage: divide £350 by 0.70.", [
        ("added_pct", 1, r"£455 adds 30% to £350. To undo a reduction, divide by 0.70: 350 ÷ 0.70 = £500."),
        ("divided_by_rate", 2, r"£1166.67 divides by 0.30. A 30% reduction leaves 0.70: 350 ÷ 0.70 = £500."),
        ("multiplied", 3, r"£245 takes another 30% off. The £350 is already reduced, so divide: £500."),
    ]),
    # 2: £2000 6% compound, years to exceed £2500 -> [4,3,5,2]
    ("Multiply by 1.06 year by year until you pass £2500.", [
        ("stopped_early", 1, r"After 3 years it is £2382.03, still under £2500. Year 4 reaches £2524.95, so 4 years."),
        ("stopped_too_early", 3, r"After 2 years it is £2247.20, well under £2500. It first passes £2500 after 4 years."),
    ]),
    # 3: painting +5%/yr now £12000, 2 years ago -> [10884.35,10800,11400,13230]
    ("Two years AGO: divide by 1.05 squared.", [
        ("went_forward", 3, r"£13 230 goes forward in time (12000 × 1.05²). Two years ago means divide: 12000 ÷ 1.05² = £10 884.35."),
        ("one_step_back", 2, r"£11 400 only takes 5% off once. Divide by 1.05 twice: 12000 ÷ 1.05² = £10 884.35."),
    ]),
    # 4: town pop -3%/yr from 80000 after 5yr -> [68699,68000,72000,65000]
    ("Compound decrease: 80 000 × 0.97 to the power 5.", [
        ("simple_decrease", 1, r"68 000 takes off 15% in one go (3% × 5). Compound: 80 000 × 0.97⁵ = 68 699."),
        ("one_year_rate", 2, r"72 000 is only 80 000 × 0.9, too big a single cut. Use 0.97 five times: 68 699."),
    ]),
]

def apply(tier, specs):
    for p, (hint, miscs) in zip(pb[tier], specs):
        p["hint"] = hint
        p["misconceptions"] = [
            {"pattern": pat, "expect": idx, "message": msg} for (pat, idx, msg) in miscs
        ]

apply("bronze", BRONZE_MC)
apply("silver", SILVER_MC)
apply("gold", GOLD_MC)

# ---- 4. tier_guides ----
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one percentage change",
        "steps": [
            r"A single increase or decrease. Turn the percentage into a <strong>multiplier</strong>: an increase of \(r\%\) is \(1 + \frac{r}{100}\), a decrease is \(1 - \frac{r}{100}\).",
            r"Multiply the original amount by the multiplier. A 25% rise uses 1.25, a 20% fall uses 0.80. To find a percentage OF an amount, just multiply by the decimal.",
            r"Check by finding the change on its own: it should equal that percentage of the original.",
        ],
        "example": {
            "question": "Increase £60 by 20%",
            "steps": [
                {"label": "Multiplier", "content": r"<p>Increase of 20%: \(1 + 0.20 = 1.20\)</p>"},
                {"label": "Multiply", "content": r"<p>\(60 \times 1.20 = £72\)</p>"},
                {"label": "Check", "content": r"<p>Increase \(= 72 - 60 = 12\), and \(20\%\) of \(60 = 12\) ✓</p>"},
                {"label": "Answer", "content": r"<p><strong>£72</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: compound change and percentage change",
        "steps": [
            r"Compound change applies the same percentage again and again. Find the yearly multiplier once, then raise it to the power of the number of years: \(\text{Final} = \text{Original} \times (\text{multiplier})^n\).",
            r"Simple interest is different: it adds the same amount every year, so find one year's interest and multiply by the number of years.",
            r"To write one amount as a percentage of another, divide the part by the whole and multiply by 100.",
        ],
        "example": {
            "question": "£2,000 at 10% compound interest for 3 years",
            "steps": [
                {"label": "Multiplier", "content": r"<p>Increase of 10%: \(1 + 0.10 = 1.10\)</p>"},
                {"label": "Power", "content": r"<p>3 years: \(1.10^3 = 1.331\)</p>"},
                {"label": "Multiply", "content": r"<p>\(2000 \times 1.331 = £2662\)</p>"},
                {"label": "Check", "content": r"<p>Interest \(= 2662 - 2000 = £662\) over 3 years ✓</p>"},
                {"label": "Answer", "content": r"<p><strong>£2,662</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: reverse percentages and hidden rates",
        "steps": [
            r"You are given the amount AFTER a change and must work backwards. The final amount is original × multiplier, so <strong>divide</strong> by the multiplier to undo it.",
            r"For compound change, divide by \((\text{multiplier})^n\), or step back one year at a time. Never just take the percentage off the final amount: it applied to the original.",
        ],
        "example": {
            "question": "After a 25% increase, a coat costs £75. Find the original price.",
            "steps": [
                {"label": "Multiplier", "content": r"<p>Increase of 25%: \(1 + 0.25 = 1.25\)</p>"},
                {"label": "Divide back", "content": r"<p>Original \(= 75 \div 1.25 = £60\)</p>"},
                {"label": "Check", "content": r"<p>Forwards: \(60 \times 1.25 = £75\) ✓</p>"},
                {"label": "Answer", "content": r"<p><strong>£60</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---- 5. guided.opener + guided.teach ----
pd["guided"] = {
    "opener": {
        "label": "Before any formulas",
        "display": "SALE: 25% off everything<br>Hoodie: £40",
        "steps": [
            {
                "say": "No formulas yet. A £40 hoodie has 25% off. 25% of £40 is a quarter, which is £10.",
                "pre": "So you pay 40 − 10 = £",
                "post": "",
                "answer": 30,
                "hint": "Take the £10 off the £40.",
            },
            {
                "say": r"That is the whole idea. Taking 25% off is the same as keeping 75%, and 75% as a decimal is 0.75, so \(£40 \times 0.75 = £30\) in one step. That 0.75 is called the <strong>multiplier</strong>."
            },
            {
                "say": "Now the twist. At the till you get a loyalty 10% off the £30 as well. 10% of £30 is £3.",
                "pre": "So you finally pay 30 − 3 = £",
                "post": "",
                "answer": 27,
                "hint": "Take £3 off £30.",
            },
            {
                "say": r"Two cuts did NOT make 35% off (that would be £26). Each cut comes off a smaller price, so they stack up: \(£40 \times 0.75 \times 0.90 = £27\). Multiplying multipliers together is all <strong>compound change</strong> is."
            },
        ],
    },
    "teach": {
        "bronze": {
            "display": "Increase £60 by 30%",
            "label": "Together: your first one",
            "steps": [
                {"pre": "Multiplier = 1 + 0.30 = ", "post": "", "answer": 1.3,
                 "hint": "Add the rate as a decimal to 1.",
                 "say": "Bronze is one percentage change, done with a multiplier. This is an increase of 30%, so add 0.30 to 1."},
                {"pre": "60 × 1.3 = £", "post": "", "answer": 78,
                 "hint": "60 plus 30% of 60.",
                 "say": "Now multiply the original amount by it."},
                {"pre": "The increase alone: 78 − 60 = £", "post": "", "answer": 18,
                 "hint": "Subtract the original from the new price.",
                 "say": "Read the answer back to be sure."},
                {"pre": "30% of 60 = 0.3 × 60 = £", "post": "", "answer": 18,
                 "hint": "Multiply 60 by 0.3.",
                 "say": "And that increase should be 30% of 60.",
                 "done": "18 matches, so £78 is right. That is the whole bronze move."},
            ],
        },
        "silver": {
            "display": "£4,000 at 5% compound interest for 3 years",
            "label": "Together: the silver move",
            "steps": [
                {"pre": "Multiplier = 1 + 0.05 = ", "post": "", "answer": 1.05,
                 "hint": "Add the rate as a decimal to 1.",
                 "say": "Silver adds compounding: the same percentage applied several times. First the yearly multiplier for a 5% increase."},
                {"pre": "1.05³ = ", "post": "", "answer": 1.157625,
                 "hint": "1.05 × 1.05 × 1.05.",
                 "say": "It runs for 3 years, so raise the multiplier to the power 3."},
                {"pre": "4000 × 1.157625 = £", "post": "", "answer": 4630.5,
                 "hint": "Multiply 4000 by 1.157625.",
                 "say": "Multiply the starting amount by this single factor."},
                {"pre": "4630.50 − 4000 = £", "post": "", "answer": 630.5,
                 "hint": "Subtract the starting amount.",
                 "say": "Check the interest earned looks right for 3 years.",
                 "done": "£630.50 interest on £4000 over 3 years at 5% compound. The power did the work: that is the silver move."},
            ],
        },
        "gold": {
            "display": "After a 20% increase, a coat costs £96. Find the original price.",
            "label": "Together: the gold move",
            "steps": [
                {"pre": "Multiplier = 1 + 0.20 = ", "post": "", "answer": 1.2,
                 "hint": "An increase adds the rate to 1.",
                 "say": "Gold works backwards. £96 is the price AFTER a 20% increase, so it equals the original times the multiplier. Find that multiplier."},
                {"pre": "96 ÷ 1.2 = £", "post": "", "answer": 80,
                 "hint": "Divide the final price by the multiplier.",
                 "say": "The final price is original × 1.2. To get back to the original, divide instead of multiply."},
                {"pre": "80 × 1.2 = £", "post": "", "answer": 96,
                 "hint": "Multiply your answer by 1.2.",
                 "say": "Check by going forwards: the original plus 20% should return £96.",
                 "done": "It lands back on £96, so the original was £80. Dividing by the multiplier is the gold move."},
                {"pre": "20% of 96 = 0.2 × 96 = £", "post": "", "answer": 19.2,
                 "hint": "Multiply 96 by 0.2.",
                 "say": "One trap to avoid: taking 20% off the £96 gives a different, wrong number. See it.",
                 "done": "£96 − £19.20 = £76.80, which is NOT the original. Always divide by the multiplier instead."},
            ],
        },
    },
}

# ---- Repair preexisting em dashes in preserved worked_examples labels ----
for we in pd.get("worked_examples") or []:
    for st in we.get("steps") or []:
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# Safety sweep: no em dash anywhere
import re
def has_em(o):
    if isinstance(o, dict): return any(has_em(v) for k, v in o.items() if k not in ("note", "guided_skip_reason"))
    if isinstance(o, list): return any(has_em(v) for v in o)
    return isinstance(o, str) and "—" in o
assert not has_em(pd), "em dash still present"

json.dump(pd, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT)
print("top keys:", list(pd.keys()))
