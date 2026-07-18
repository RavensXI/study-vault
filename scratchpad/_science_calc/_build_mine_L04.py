# -*- coding: utf-8 -*-
import json, io, copy

CANON = "_mine_L04_canonical.json"
KEY = "chemistry-calculations-L04@b7b54666b8"
OUT = "lesson_%s.json" % KEY

pd = json.load(io.open(CANON, encoding="utf-8"))

# ---------------------------------------------------------------------------
# 1. method_card: trim to <=140 words, <=4 steps, no em dashes
# ---------------------------------------------------------------------------
pd["method_card"]["steps"] = [
    "Identify the quantity that changes (gas volume, mass, or amount dissolved) and the time.",
    "Use rate = quantity ÷ time, or concentration = mass ÷ volume.",
    "Convert cm³ to dm³ (÷ 1000) before any concentration divide.",
    "State the answer with its unit: cm³/s, g/s or g/dm³.",
]
pd["method_card"]["content"] = (
    "<p><strong>Rate of reaction</strong> measures how fast a quantity changes: "
    "rate = change in quantity ÷ time. The quantity may be gas volume (cm³), "
    "mass lost (g), or product made.</p>"
    "<p>On a graph, a <strong>steeper</strong> curve means a <strong>faster</strong> "
    "reaction; a flat line means it has finished. Mean rate between two points is the "
    "change in height divided by the change in time.</p>"
    "<p><strong>Concentration</strong> = mass ÷ volume, with volume in dm³. "
    "1 dm³ = 1000 cm³, so divide a cm³ volume by 1000 first.</p>"
)

# ---------------------------------------------------------------------------
# 2. exam_context: strip em dash (validator enforces)
# ---------------------------------------------------------------------------
pd["exam_context"]["frequency"] = "Common: rate graphs appear frequently on Paper 2"

# ---------------------------------------------------------------------------
# 3. worked_examples: strip em dashes from labels (preserve otherwise)
# ---------------------------------------------------------------------------
for we in pd["worked_examples"]:
    for st in we["steps"]:
        if "label" in st and " — " in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ")

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def mc(pattern, message, expect):
    return {"pattern": pattern, "check": "common", "message": message, "expect": expect}

# ---------------------------------------------------------------------------
# 4. tier descriptions
# ---------------------------------------------------------------------------
pb = pd["problem_bank"]
pb["bronze_description"] = "One step: put the numbers straight into rate = quantity ÷ time, or concentration = mass ÷ volume."
pb["silver_description"] = "Read a change off a graph, or convert cm³ to dm³, before you divide."
pb["gold_description"] = "Two moves: rearrange the equation or read the right line, then convert units to finish."

# ---------------------------------------------------------------------------
# 5. per-problem: misconceptions (with expect) + hint + guided_steps
#    Problems are matched by (tier, index) into the canonical bank.
# ---------------------------------------------------------------------------

BRONZE = pb["bronze"]
SILVER = pb["silver"]
GOLD = pb["gold"]

# ---- BRONZE ----
# B0: 48 cm3 / 60 s = 0.8
BRONZE[0]["misconceptions"] = [
    mc("inverted", "Rate = quantity ÷ time = 48 ÷ 60 = 0.8 cm³/s. Dividing time by quantity (60 ÷ 48 = 1.25) is upside down.", 1.25),
]
BRONZE[0]["guided_steps"] = [
    {"say": "Rate of reaction = amount of gas produced ÷ time. State the equation, then read the two numbers.", "pre": "Amount of gas produced = ", "post": " cm³", "answer": 48, "hint": "Read it straight from the question."},
    {"pre": "Time taken = ", "post": " s", "answer": 60, "hint": "The question gives the time in seconds."},
    {"say": "Both are already in the right units, so substitute and divide.", "phase": "substitute", "pre": "rate = 48 ÷ 60 = ", "post": "", "answer": 0.8, "hint": "Divide the volume by the time."},
    {"pre": "Check: 0.8 × 60 = ", "post": " cm³", "answer": 48, "done": "That returns the 48 cm³ given, so the rate is 0.8 cm³/s.", "hint": "Multiply your rate back by the time."},
]

# B1: 35 / 50 = 0.7
BRONZE[1]["misconceptions"] = [
    mc("inverted", "Rate = 35 ÷ 50 = 0.7 cm³/s. Always put the quantity on top and the time underneath.", None),
]
BRONZE[1]["guided_steps"] = [
    {"say": "Rate = amount of gas ÷ time. Pull out the two values.", "pre": "Amount of gas produced = ", "post": " cm³", "answer": 35, "hint": "Straight from the question."},
    {"pre": "Time taken = ", "post": " s", "answer": 50, "hint": "In seconds already."},
    {"say": "Units are fine, so divide.", "phase": "substitute", "pre": "rate = 35 ÷ 50 = ", "post": "", "answer": 0.7, "hint": "Volume divided by time."},
    {"pre": "Check: 0.7 × 50 = ", "post": " cm³", "answer": 35, "done": "Back to 35 cm³, so the rate is 0.7 cm³/s.", "hint": "Multiply the rate by the time."},
]

# B2: 0.72 g / 120 s = 0.006
BRONZE[2]["misconceptions"] = [
    mc("inverted", "Rate = change in mass ÷ time = 0.72 ÷ 120 = 0.006 g/s. Keep the mass on top.", None),
]
BRONZE[2]["guided_steps"] = [
    {"say": "Here the quantity is mass lost, not gas volume, but the rule is the same: rate = change in mass ÷ time.", "pre": "Change in mass = ", "post": " g", "answer": 0.72, "hint": "The mass the flask loses."},
    {"pre": "Time taken = ", "post": " s", "answer": 120, "hint": "In seconds."},
    {"say": "Divide the mass by the time.", "phase": "substitute", "pre": "rate = 0.72 ÷ 120 = ", "post": "", "answer": 0.006, "hint": "A small number, three decimal places."},
    {"pre": "Check: 0.006 × 120 = ", "post": " g", "answer": 0.72, "done": "Back to 0.72 g, so the rate is 0.006 g/s.", "hint": "Multiply the rate by the time."},
]

# B3: 10 / 2 = 5
BRONZE[3]["misconceptions"] = [
    mc("inverted", "Concentration = mass ÷ volume = 10 ÷ 2 = 5 g/dm³. Dividing volume by mass (0.2) is the wrong way round.", 0.2),
]
BRONZE[3]["guided_steps"] = [
    {"say": "Concentration = mass ÷ volume, with the volume in dm³. Read the two values.", "pre": "Mass of solute = ", "post": " g", "answer": 10, "hint": "The mass dissolved."},
    {"pre": "Volume = ", "post": " dm³", "answer": 2, "hint": "Already in dm³, no conversion needed."},
    {"say": "Volume is already in dm³, so divide.", "phase": "substitute", "pre": "concentration = 10 ÷ 2 = ", "post": "", "answer": 5, "hint": "Mass divided by volume."},
    {"pre": "Check: 5 × 2 = ", "post": " g", "answer": 10, "done": "Back to 10 g, so the concentration is 5 g/dm³.", "hint": "Multiply concentration by volume."},
]

# B4: 4 / 0.5 = 8
BRONZE[4]["misconceptions"] = [
    mc("inverted", "Concentration = 4 ÷ 0.5 = 8 g/dm³. Mass goes on top, volume underneath (0.5 ÷ 4 = 0.125 is upside down).", 0.125),
]
BRONZE[4]["guided_steps"] = [
    {"say": "Concentration = mass ÷ volume in dm³.", "pre": "Mass of solute = ", "post": " g", "answer": 4, "hint": "The mass dissolved."},
    {"pre": "Volume = ", "post": " dm³", "answer": 0.5, "hint": "Already in dm³."},
    {"say": "Divide the mass by the volume.", "phase": "substitute", "pre": "concentration = 4 ÷ 0.5 = ", "post": "", "answer": 8, "hint": "Dividing by 0.5 is the same as doubling."},
    {"pre": "Check: 8 × 0.5 = ", "post": " g", "answer": 4, "done": "Back to 4 g, so the concentration is 8 g/dm³.", "hint": "Multiply concentration by volume."},
]

# B5: 56 / 40 = 1.4
BRONZE[5]["misconceptions"] = [
    mc("inverted", "Rate = 56 ÷ 40 = 1.4 cm³/s. Quantity on top, time underneath.", None),
]
BRONZE[5]["guided_steps"] = [
    {"say": "Rate = amount of gas ÷ time.", "pre": "Amount of gas produced = ", "post": " cm³", "answer": 56, "hint": "From the question."},
    {"pre": "Time taken = ", "post": " s", "answer": 40, "hint": "In seconds."},
    {"say": "Divide.", "phase": "substitute", "pre": "rate = 56 ÷ 40 = ", "post": "", "answer": 1.4, "hint": "Volume divided by time."},
    {"pre": "Check: 1.4 × 40 = ", "post": " cm³", "answer": 56, "done": "Back to 56 cm³, so the rate is 1.4 cm³/s.", "hint": "Multiply the rate by the time."},
]

# B6: graph, total volume = 42 (calculator false)
BRONZE[6]["misconceptions"] = [
    mc("wrong_reading", "The curve levels off at 42 cm³ from 60 s onwards. That flat height is the total gas produced.", None),
]
BRONZE[6]["guided_steps"] = [
    {"say": "The reaction is over when the curve stops climbing and goes flat. Read the height there.", "pre": "Height of the curve at 50 s = ", "post": " cm³", "answer": 40, "hint": "Read the y-value above 50 s."},
    {"pre": "Height at 60 s = ", "post": " cm³", "answer": 42, "hint": "Read the y-value above 60 s."},
    {"say": "If the next reading is the same, the curve has levelled off.", "phase": "substitute", "pre": "Height at 70 s = ", "post": " cm³", "answer": 42, "hint": "Read the y-value above 70 s."},
    {"pre": "Total gas produced = ", "post": " cm³", "answer": 42, "done": "60 s and 70 s both read 42 cm³, so the flat height, 42 cm³, is the total gas made.", "hint": "The flat height is the total."},
]

# B7: 20 / 0.4 = 50
BRONZE[7]["misconceptions"] = [
    mc("inverted", "Concentration = 20 ÷ 0.4 = 50 g/dm³. Mass on top, volume underneath (0.4 ÷ 20 = 0.02 is upside down).", 0.02),
]
BRONZE[7]["guided_steps"] = [
    {"say": "Concentration = mass ÷ volume in dm³.", "pre": "Mass of solute = ", "post": " g", "answer": 20, "hint": "The mass dissolved."},
    {"pre": "Volume = ", "post": " dm³", "answer": 0.4, "hint": "Already in dm³."},
    {"say": "Divide.", "phase": "substitute", "pre": "concentration = 20 ÷ 0.4 = ", "post": "", "answer": 50, "hint": "20 divided by 0.4."},
    {"pre": "Check: 50 × 0.4 = ", "post": " g", "answer": 20, "done": "Back to 20 g, so the concentration is 50 g/dm³.", "hint": "Multiply concentration by volume."},
]

# ---- SILVER ----
# S0: graph first 20 s = 1.1 (at 20 s = 22)
SILVER[0]["misconceptions"] = [
    mc("wrong_reading", "At 20 s the volume is 22 cm³. Mean rate = 22 ÷ 20 = 1.1 cm³/s.", None),
    mc("used_total_time", "Divide by the 20 seconds asked for, not the whole run time. Rate = 22 ÷ 20 = 1.1 cm³/s.", None),
]
SILVER[0]["guided_steps"] = [
    {"say": "Mean rate from a graph = change in volume ÷ change in time. Over the first 20 seconds the change starts from zero.", "pre": "Volume at 20 s = ", "post": " cm³", "answer": 22, "hint": "Read the height above 20 s."},
    {"pre": "Time = ", "post": " s", "answer": 20, "hint": "The first 20 seconds."},
    {"say": "Divide the volume by the time.", "phase": "substitute", "pre": "rate = 22 ÷ 20 = ", "post": "", "answer": 1.1, "hint": "22 divided by 20."},
    {"pre": "Check: 1.1 × 20 = ", "post": " cm³", "answer": 22, "done": "Back to 22 cm³, so the mean rate is 1.1 cm³/s.", "hint": "Multiply the rate by the time."},
]

# S1: graph 10 s to 30 s = 0.9 (12 -> 30)
SILVER[1]["misconceptions"] = [
    mc("wrong_reading", "At 10 s volume = 12 cm³, at 30 s volume = 30 cm³.", None),
    mc("forgot_subtract", "Use the CHANGE in volume, 30 − 12 = 18 cm³, not the 30 at the end. With the 20 s interval that gives 18 ÷ 20 = 0.9 cm³/s. Using 30 ÷ 20 gives 1.5, which is too fast.", 1.5),
]
SILVER[1]["guided_steps"] = [
    {"say": "Between two times you need the change in volume AND the change in time. Read both heights first.", "pre": "Volume at 30 s = ", "post": " cm³", "answer": 30, "hint": "Height above 30 s."},
    {"pre": "Volume at 10 s = ", "post": " cm³", "answer": 12, "hint": "Height above 10 s."},
    {"pre": "Change in volume = 30 − 12 = ", "post": " cm³", "answer": 18, "hint": "Subtract the earlier height from the later one."},
    {"say": "The time interval is 30 − 10 = 20 s. Now divide.", "phase": "substitute", "pre": "rate = 18 ÷ 20 = ", "post": "", "answer": 0.9, "hint": "Change in volume divided by change in time."},
    {"pre": "Check: 0.9 × 20 = ", "post": " cm³", "answer": 18, "done": "Back to the 18 cm³ change, so the mean rate is 0.9 cm³/s.", "hint": "Multiply the rate by the time interval."},
]

# S2: 7.3 g / 250 cm3 = 29.2
SILVER[2]["misconceptions"] = [
    mc("unit_error", "Convert 250 cm³ to 0.25 dm³ first. Dividing by 250 straight away gives 0.0292, far too small. Correct: 7.3 ÷ 0.25 = 29.2 g/dm³.", 0.0292),
    mc("forgot_convert", "250 cm³ is 0.25 dm³, not 250 dm³. Divide the cm³ by 1000 before dividing the mass.", None),
]
SILVER[2]["guided_steps"] = [
    {"say": "Concentration = mass ÷ volume, and the volume must be in dm³. This one is in cm³, so convert first.", "pre": "Mass of solute = ", "post": " g", "answer": 7.3, "hint": "The mass dissolved."},
    {"say": "Convert the volume: 1000 cm³ = 1 dm³, so divide by 1000.", "pre": "Volume in dm³ = 250 ÷ 1000 = ", "post": "", "answer": 0.25, "hint": "Move the decimal point three places."},
    {"say": "Now divide the mass by the volume in dm³.", "phase": "substitute", "pre": "concentration = 7.3 ÷ 0.25 = ", "post": "", "answer": 29.2, "hint": "7.3 divided by 0.25."},
    {"pre": "Check: 29.2 × 0.25 = ", "post": " g", "answer": 7.3, "done": "Back to 7.3 g, so the concentration is 29.2 g/dm³.", "hint": "Multiply concentration by volume in dm³."},
]

# S3: 5.85 g / 500 cm3 = 11.7
SILVER[3]["misconceptions"] = [
    mc("unit_error", "Convert 500 cm³ to 0.5 dm³ first. Dividing by 500 gives 0.0117, far too small. Correct: 5.85 ÷ 0.5 = 11.7 g/dm³.", 0.0117),
    mc("forgot_convert", "500 cm³ = 0.5 dm³. Convert before dividing.", None),
]
SILVER[3]["guided_steps"] = [
    {"say": "Concentration = mass ÷ volume in dm³. The volume is in cm³, so convert.", "pre": "Mass of solute = ", "post": " g", "answer": 5.85, "hint": "The mass dissolved."},
    {"say": "Convert: divide the cm³ by 1000.", "pre": "Volume in dm³ = 500 ÷ 1000 = ", "post": "", "answer": 0.5, "hint": "500 ÷ 1000."},
    {"say": "Now divide.", "phase": "substitute", "pre": "concentration = 5.85 ÷ 0.5 = ", "post": "", "answer": 11.7, "hint": "Dividing by 0.5 doubles the number."},
    {"pre": "Check: 11.7 × 0.5 = ", "post": " g", "answer": 5.85, "done": "Back to 5.85 g, so the concentration is 11.7 g/dm³.", "hint": "Multiply concentration by volume in dm³."},
]

# S4: mass-loss graph first 40 s = 0.007 (at 40 s = 0.28)
SILVER[4]["misconceptions"] = [
    mc("wrong_reading", "At 40 s the mass lost is 0.28 g. Rate = 0.28 ÷ 40 = 0.007 g/s.", None),
]
SILVER[4]["guided_steps"] = [
    {"say": "Mean rate of mass loss = change in mass ÷ time. Read the blue line at 40 s.", "pre": "Mass lost by 40 s = ", "post": " g", "answer": 0.28, "hint": "Height of the line above 40 s."},
    {"pre": "Time = ", "post": " s", "answer": 40, "hint": "The first 40 seconds."},
    {"say": "Divide the mass by the time.", "phase": "substitute", "pre": "rate = 0.28 ÷ 40 = ", "post": "", "answer": 0.007, "hint": "A small number, three decimal places."},
    {"pre": "Check: 0.007 × 40 = ", "post": " g", "answer": 0.28, "done": "Back to 0.28 g, so the mean rate is 0.007 g/s.", "hint": "Multiply the rate by the time."},
]

# S5: finish time = 100 (calculator false)
SILVER[5]["misconceptions"] = [
    mc("wrong_reading", "The mass loss stops changing at 0.48 g. Both 100 s and 120 s read 0.48 g, so the reaction finishes at 100 s.", None),
]
SILVER[5]["guided_steps"] = [
    {"say": "The reaction has finished when the mass loss stops changing, where the curve goes flat. Read the last few points.", "pre": "Mass lost at 80 s = ", "post": " g", "answer": 0.45, "hint": "Height above 80 s."},
    {"pre": "Mass lost at 100 s = ", "post": " g", "answer": 0.48, "hint": "Height above 100 s."},
    {"say": "If the next point is the same, nothing more is being lost.", "phase": "substitute", "pre": "Mass lost at 120 s = ", "post": " g", "answer": 0.48, "hint": "Height above 120 s."},
    {"pre": "Time the reaction finishes = ", "post": " s", "answer": 100, "done": "100 s and 120 s both read 0.48 g, so no gas escapes after 100 s. The reaction finishes at 100 s.", "hint": "The first time the value stops rising."},
]

# ---- GOLD ----
# G0: graph A first 10 s = 2.4 (A at 10 s = 24)
GOLD[0]["hint"] = "Read Reaction A (red) at 10 s, then divide by 10."
GOLD[0]["misconceptions"] = [
    mc("wrong_reaction", "Read Reaction A, the red line. At 10 s it reads 24 cm³, giving 24 ÷ 10 = 2.4 cm³/s. The blue line (Reaction B) reads 15 and gives 1.5.", 1.5),
    mc("used_total", "Use only the first 10 seconds, not the whole run. Rate = 24 ÷ 10 = 2.4 cm³/s.", None),
]
GOLD[0]["guided_steps"] = [
    {"say": "Mean rate = change in volume ÷ time. Read Reaction A, the red line, over the first 10 seconds.", "pre": "Volume of A at 10 s = ", "post": " cm³", "answer": 24, "hint": "Height of the red line above 10 s."},
    {"pre": "Time = ", "post": " s", "answer": 10, "hint": "The first 10 seconds."},
    {"say": "Divide.", "phase": "substitute", "pre": "rate = 24 ÷ 10 = ", "post": "", "answer": 2.4, "hint": "24 divided by 10."},
    {"pre": "Check: 2.4 × 10 = ", "post": " cm³", "answer": 24, "done": "Back to 24 cm³, so Reaction A's mean rate is 2.4 cm³/s.", "hint": "Multiply the rate by the time."},
]

# G1: graph B first 10 s = 1.5 (B at 10 s = 15)
GOLD[1]["hint"] = "Read Reaction B (blue) at 10 s, then divide by 10."
GOLD[1]["misconceptions"] = [
    mc("wrong_reaction", "Read Reaction B, the blue line. At 10 s it reads 15 cm³, giving 15 ÷ 10 = 1.5 cm³/s. The red line (Reaction A) reads 24 and gives 2.4.", 2.4),
]
GOLD[1]["guided_steps"] = [
    {"say": "Same method, but read Reaction B, the blue line, at 10 seconds.", "pre": "Volume of B at 10 s = ", "post": " cm³", "answer": 15, "hint": "Height of the blue line above 10 s."},
    {"pre": "Time = ", "post": " s", "answer": 10, "hint": "The first 10 seconds."},
    {"say": "Divide.", "phase": "substitute", "pre": "rate = 15 ÷ 10 = ", "post": "", "answer": 1.5, "hint": "15 divided by 10."},
    {"pre": "Check: 1.5 × 10 = ", "post": " cm³", "answer": 15, "done": "Back to 15 cm³, so Reaction B's mean rate is 1.5 cm³/s.", "hint": "Multiply the rate by the time."},
]

# G2: multiple choice, keep as is (no guided_steps), add hint + expect
GOLD[2]["hint"] = "Same total gas means the same amount of reactant. What speeds up the start without changing the total?"
GOLD[2]["misconceptions"] = [
    mc("wrong_factor", "Same total volume means the same amount of reactant. A higher starting rate with the same final volume points to a higher concentration: more frequent collisions at the start, but the same total moles of reactant.", None),
]

# G3: 8 g needed, 40 g/dm3 -> 0.2 dm3 -> 200 cm3
GOLD[3]["hint"] = "Rearrange to volume = mass ÷ concentration, then convert dm³ to cm³ (× 1000)."
GOLD[3]["misconceptions"] = [
    mc("forgot_convert", "Volume = mass ÷ concentration = 8 ÷ 40 = 0.2 dm³. The answer is wanted in cm³, so multiply by 1000: 200 cm³. Leaving it as 0.2 forgets the conversion.", 0.2),
    mc("wrong_rearrange", "Rearrange concentration = mass ÷ volume to volume = mass ÷ concentration. Divide the mass by the concentration, not the other way round.", None),
]
GOLD[3]["guided_steps"] = [
    {"say": "You are given the concentration and the mass, and asked for the volume. Rearrange concentration = mass ÷ volume to volume = mass ÷ concentration.", "pre": "Mass needed = ", "post": " g", "answer": 8, "hint": "The mass of solute wanted."},
    {"pre": "Concentration = ", "post": " g/dm³", "answer": 40, "hint": "Given in the question."},
    {"say": "Divide the mass by the concentration to get the volume in dm³.", "phase": "substitute", "pre": "volume in dm³ = 8 ÷ 40 = ", "post": "", "answer": 0.2, "hint": "8 divided by 40."},
    {"say": "The answer is wanted in cm³, so convert: 1 dm³ = 1000 cm³.", "pre": "volume in cm³ = 0.2 × 1000 = ", "post": "", "answer": 200, "hint": "Multiply the dm³ value by 1000."},
    {"pre": "Check: 8 ÷ 0.2 = ", "post": " g/dm³", "answer": 40, "done": "That returns the 40 g/dm³ concentration, so the volume is 200 cm³.", "hint": "Mass divided by the volume in dm³ should give the concentration."},
]

# G4: overall mean rate 0 to 60 s = 0.7 (at 60 s = 42)
GOLD[4]["hint"] = "The reaction finishes at 60 s; divide the final volume by 60."
GOLD[4]["misconceptions"] = [
    mc("wrong_time", "The reaction finishes at 60 s, where the curve goes flat. Rate = 42 ÷ 60 = 0.7 cm³/s. Dividing by 70 gives 0.6, but no gas is made after 60 s.", 0.6),
    mc("used_70", "The line is flat from 60 s to 70 s, so the reaction ended at 60 s. Use 60 s, not 70 s.", None),
]
GOLD[4]["guided_steps"] = [
    {"say": "Overall mean rate = total volume ÷ total time. The reaction finishes at 60 s, where the curve goes flat.", "pre": "Final volume at 60 s = ", "post": " cm³", "answer": 42, "hint": "Height where the curve levels off."},
    {"pre": "Total time = ", "post": " s", "answer": 60, "hint": "The reaction ends at 60 s, not 70 s."},
    {"say": "Divide the total volume by the total time.", "phase": "substitute", "pre": "rate = 42 ÷ 60 = ", "post": "", "answer": 0.7, "hint": "42 divided by 60."},
    {"pre": "Check: 0.7 × 60 = ", "post": " cm³", "answer": 42, "done": "Back to 42 cm³, so the overall mean rate is 0.7 cm³/s.", "hint": "Multiply the rate by the total time."},
]

# G5: 36 g/dm3, 500 cm3 -> 18 g
GOLD[5]["hint"] = "Convert 500 cm³ to 0.5 dm³, then mass = concentration × volume."
GOLD[5]["misconceptions"] = [
    mc("forgot_convert", "Convert 500 cm³ to 0.5 dm³ first. Mass = 36 × 0.5 = 18 g. Multiplying by 500 gives 18000, far too large.", 18000),
    mc("wrong_rearrange", "Mass = concentration × volume = 36 × 0.5 = 18 g. Dividing (36 ÷ 0.5 = 72) is the wrong operation.", 72),
]
GOLD[5]["guided_steps"] = [
    {"say": "You are given the concentration and the volume, and asked for the mass. Rearrange to mass = concentration × volume, with the volume in dm³.", "pre": "Concentration = ", "post": " g/dm³", "answer": 36, "hint": "Given in the question."},
    {"say": "Convert the volume: 500 cm³ ÷ 1000.", "pre": "Volume in dm³ = 500 ÷ 1000 = ", "post": "", "answer": 0.5, "hint": "500 divided by 1000."},
    {"say": "Multiply the concentration by the volume.", "phase": "substitute", "pre": "mass = 36 × 0.5 = ", "post": " g", "answer": 18, "hint": "36 times 0.5."},
    {"pre": "Check: 18 ÷ 0.5 = ", "post": " g/dm³", "answer": 36, "done": "That returns the 36 g/dm³ concentration, so the mass is 18 g.", "hint": "Mass divided by volume in dm³ gives concentration."},
]

# ---------------------------------------------------------------------------
# 6. tier_guides
# ---------------------------------------------------------------------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one equation, straight in",
        "steps": [
            "<strong>Rate</strong> = quantity ÷ time. The quantity can be gas volume (cm³), mass lost (g), or product formed.",
            "<strong>Concentration</strong> = mass ÷ volume, with the volume in dm³.",
            "Read both numbers from the question, divide, and add the unit (cm³/s, g/s or g/dm³).",
        ],
        "example": {
            "question": "A reaction makes 45 cm³ of gas in 90 s. Find the mean rate.",
            "steps": [
                {"label": "Write the equation", "content": "<p>rate = quantity ÷ time</p>"},
                {"label": "Substitute", "content": "<p>rate = 45 ÷ 90</p>"},
                {"label": "Check", "content": "<p>0.5 × 90 = 45 cm³, matches the question</p>"},
                {"label": "Answer", "content": "<p><strong>0.5 cm³/s</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: convert or read a change first",
        "steps": [
            "From a graph, mean rate = <strong>change in quantity ÷ change in time</strong>. Read both points, subtract, then divide.",
            "For concentration, convert the volume: <strong>cm³ ÷ 1000 = dm³</strong> before dividing.",
            "One extra step before the divide, that is all silver adds.",
        ],
        "example": {
            "question": "8.5 g of solute is dissolved in 500 cm³. Find the concentration in g/dm³.",
            "steps": [
                {"label": "Convert", "content": "<p>500 ÷ 1000 = 0.5 dm³</p>"},
                {"label": "Substitute", "content": "<p>concentration = 8.5 ÷ 0.5</p>"},
                {"label": "Check", "content": "<p>17 × 0.5 = 8.5 g, matches</p>"},
                {"label": "Answer", "content": "<p><strong>17 g/dm³</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: rearrange and convert",
        "steps": [
            "Rearrange for what is asked: <strong>volume = mass ÷ concentration</strong>, or <strong>mass = concentration × volume</strong>.",
            "Convert between cm³ and dm³ as the final step (× 1000 or ÷ 1000).",
            "For two-curve graphs, read the right line, then divide by the time interval.",
        ],
        "example": {
            "question": "A solution is 50 g/dm³. How many cm³ hold 5 g?",
            "steps": [
                {"label": "Rearrange", "content": "<p>volume = mass ÷ concentration = 5 ÷ 50</p>"},
                {"label": "Convert", "content": "<p>0.1 dm³ × 1000 = 100 cm³</p>"},
                {"label": "Check", "content": "<p>50 × 0.1 = 5 g, matches</p>"},
                {"label": "Answer", "content": "<p><strong>100 cm³</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# 7. guided (opener + teach walks)
# ---------------------------------------------------------------------------
pd["guided"] = {
    "opener": {
        "label": "Before any equations",
        "display": "A fizzy tablet in water:<br>30 cm³ of gas bubbles up in 10 seconds.",
        "steps": [
            {
                "say": "Drop a fizzy vitamin tablet in water and watch the bubbles. No chemistry needed yet.",
                "pre": "It makes 30 cm³ of gas in 10 seconds. Each second it makes about ",
                "post": " cm³",
                "answer": 3,
                "hint": "Share the 30 cm³ out over the 10 seconds: 30 ÷ 10.",
            },
            {
                "say": "That number, gas made each second, is the <strong>rate of reaction</strong>. You just did rate = amount ÷ time.",
                "pre": "A stronger tablet makes the same 30 cm³ in only 6 seconds. Its rate is ",
                "post": " cm³ each second",
                "answer": 5,
                "hint": "30 ÷ 6.",
            },
            {
                "say": "Faster reaction, bigger rate. On a graph the gas climbs more steeply, and reading a value off the graph then dividing by the time is the whole skill.",
            },
        ],
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "A reaction produces 60 cm³ of gas in 30 seconds. Calculate the mean rate of reaction.",
            "steps": [
                {"say": "Rate of reaction = amount of gas produced ÷ time. Write it down, then read the numbers.", "pre": "Amount of gas produced = ", "post": " cm³", "answer": 60, "hint": "Straight from the question."},
                {"pre": "Time taken = ", "post": " s", "answer": 30, "hint": "In seconds already."},
                {"say": "Both units are fine, so divide.", "pre": "rate = 60 ÷ 30 = ", "post": "", "answer": 2, "hint": "60 divided by 30."},
                {"pre": "Check: 2 × 30 = ", "post": " cm³", "answer": 60, "done": "Back to 60 cm³. The mean rate is 2 cm³/s, gas over time. That is the whole bronze move.", "hint": "Multiply the rate by the time."},
            ],
        },
        "silver": {
            "label": "Together: the silver move",
            "display": "9.2 g of solute is dissolved in 400 cm³ of solution. Calculate the concentration in g/dm³.",
            "steps": [
                {"say": "Concentration = mass ÷ volume, but the volume must be in dm³ and this one is in cm³. The conversion is the new silver step.", "pre": "Mass of solute = ", "post": " g", "answer": 9.2, "hint": "The mass dissolved."},
                {"say": "Convert the volume: 1000 cm³ = 1 dm³, so divide by 1000.", "pre": "Volume in dm³ = 400 ÷ 1000 = ", "post": "", "answer": 0.4, "hint": "400 ÷ 1000."},
                {"say": "Now divide the mass by the volume in dm³.", "pre": "concentration = 9.2 ÷ 0.4 = ", "post": "", "answer": 23, "hint": "9.2 divided by 0.4."},
                {"pre": "Check: 23 × 0.4 = ", "post": " g", "answer": 9.2, "done": "Back to 9.2 g. The concentration is 23 g/dm³. Converting the volume first was the whole point.", "hint": "Multiply concentration by volume in dm³."},
            ],
        },
        "gold": {
            "label": "Together: the gold move",
            "display": "A solution has a concentration of 25 g/dm³. A student needs 5 g of solute. Calculate the volume of solution needed in cm³.",
            "steps": [
                {"say": "Here you rearrange AND convert, the gold combination. Concentration = mass ÷ volume rearranges to volume = mass ÷ concentration.", "pre": "Mass needed = ", "post": " g", "answer": 5, "hint": "The mass of solute wanted."},
                {"pre": "Concentration = ", "post": " g/dm³", "answer": 25, "hint": "Given in the question."},
                {"say": "Divide the mass by the concentration for the volume in dm³.", "pre": "volume in dm³ = 5 ÷ 25 = ", "post": "", "answer": 0.2, "hint": "5 divided by 25."},
                {"say": "Convert to cm³: multiply by 1000.", "pre": "volume in cm³ = 0.2 × 1000 = ", "post": "", "answer": 200, "hint": "0.2 × 1000."},
                {"pre": "Check: 5 ÷ 0.2 = ", "post": " g/dm³", "answer": 25, "done": "That returns the 25 g/dm³ concentration. The volume is 200 cm³. Rearrange, then convert.", "hint": "Mass ÷ volume in dm³ should give the concentration."},
            ],
        },
    },
}

# ---------------------------------------------------------------------------
# guard: no em dashes anywhere except note/guided_skip_reason
# ---------------------------------------------------------------------------
def scan_em(obj, path):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("note", "guided_skip_reason"):
                continue
            hits += scan_em(v, path + "." + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += scan_em(v, path + "[%d]" % i)
    elif isinstance(obj, str) and "—" in obj:
        hits.append(path)
    return hits

em = scan_em(pd, "pd")
if em:
    print("EM DASH FOUND:", em)
else:
    print("no em dashes")

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written", OUT)
