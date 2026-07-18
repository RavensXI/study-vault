# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_live_1563a319.json", encoding="utf-8"))

# ---- method_card: strip em dashes, slim to <=140 words ----
pd["method_card"]["content"] = (
    "<p>Two calculations: <strong>rate</strong> from data and "
    "<strong>concentration</strong> of a solution.</p>"
    "<p><strong>Mean rate</strong> = quantity produced (or used) ÷ time. "
    "On a graph, the gradient at a point gives the instantaneous rate.</p>"
    "<p><strong>Concentration</strong>: g/dm³ = mass ÷ volume (dm³); "
    "mol/dm³ = moles ÷ volume (dm³). Remember 1 dm³ = 1,000 cm³.</p>"
    "<p><strong>Watch out:</strong> forgetting to convert cm³ to dm³ is the "
    "most common slip. Read mean rate as total quantity ÷ total time, not from a "
    "single point.</p>"
)

# ---- strip pre-existing em dashes in preserved fields ----
pd["exam_context"]["frequency"] = "Medium-High. Rate and concentration appear regularly"
for we in pd["worked_examples"]:
    for st in we["steps"]:
        if "label" in st:
            st["label"] = st["label"].replace(" — ", ": ")

pb = pd["problem_bank"]
pb["bronze_description"] =("One equation, values already in the right units (or a single "
    "cm³ to dm³ conversion), straight in.")
pb["silver_description"] = ("Rearrange the equation, or convert the volume to dm³ before "
    "you substitute.")
pb["gold_description"] = ("Two steps chained: find moles first, convert units, or read a "
    "graph before you calculate.")

def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase is not None: d["phase"] = phase
    if done is not None: d["done"] = done
    return d
def say(text): return {"say": text}

# ================= BRONZE =================
b = pb["bronze"]
b[0]["guided_steps"] = [
    say("The equation is <strong>mean rate = volume ÷ time</strong>. Read the two numbers straight from the question."),
    box("Volume of gas collected (cm³) = ", 48, "The gas collected is given directly."),
    box("Time taken (s) = ", 12, "The time is already in seconds, no conversion needed."),
    box("48 ÷ 12 = ", 4, "Share the 48 cm³ out over the 12 seconds.", say="Now divide volume by time.", phase="substitute"),
    box("4 × 12 = ", 48, "Rate × time should give back the volume.", say="State it with the unit: 4 cm³/s. Check by multiplying back:", done="That returns the 48 cm³ we started with, so 4 cm³/s is right."),
]
b[0]["misconceptions"][0]["expect"] = 0.25
b[0]["misconceptions"][0]["message"] = "Rate is volume ÷ time, not time ÷ volume. 48 ÷ 12 = 4 cm³/s. Dividing the other way (12 ÷ 48) gives 0.25, far too small for gas bubbling out."

b[1]["guided_steps"] = [
    say("The equation is <strong>mean rate = volume ÷ time</strong>. Read the two values."),
    box("Volume of gas (cm³) = ", 60, "Given directly in the question."),
    box("Time (s) = ", 30, "Already in seconds."),
    box("60 ÷ 30 = ", 2, "Share 60 cm³ over 30 seconds.", say="Now divide.", phase="substitute"),
    box("2 × 30 = ", 60, "Rate × time should return the volume.", say="Answer: 2 cm³/s. Check by multiplying back:", done="Returns 60 cm³, so 2 cm³/s is right."),
]
b[1]["misconceptions"][0]["expect"] = 0.5
b[1]["misconceptions"][0]["message"] = "Rate is volume ÷ time. 60 ÷ 30 = 2 cm³/s. Dividing time by volume (30 ÷ 60) gives 0.5, which is upside down."

b[2]["guided_steps"] = [
    say("1 dm³ = 1,000 cm³, so to change cm³ into dm³ you <strong>divide by 1,000</strong>."),
    box("How many cm³ are in 1 dm³? ", 1000, "One dm³ is a thousand cm³."),
    box("250 ÷ 1000 = ", 0.25, "Move the digits three places, or divide on the calculator.", say="Now do the conversion.", phase="substitute"),
    box("0.25 × 1000 = ", 250, "Multiplying back by 1,000 should return the original cm³.", say="Check by going back the other way:", done="Returns 250 cm³, so 0.25 dm³ is right."),
]
b[2]["misconceptions"][0]["expect"] = 250000
b[2]["misconceptions"][0]["message"] = "cm³ to dm³ means dividing by 1,000: 250 ÷ 1,000 = 0.25 dm³. Multiplying by 1,000 gives 250,000, far bigger than you started with."

b[3]["guided_steps"] = [
    say("The equation is <strong>concentration (g/dm³) = mass ÷ volume in dm³</strong>. The volume is in cm³, so convert it first."),
    box("Convert the volume: 200 ÷ 1000 = ", 0.2, "Divide cm³ by 1,000 to get dm³.", post=" dm³"),
    box("Mass (g) = ", 3.6, "Given directly in the question."),
    box("3.6 ÷ 0.2 = ", 18, "Divide the mass by the volume in dm³.", say="Now divide mass by volume.", phase="substitute"),
    box("18 × 0.2 = ", 3.6, "Concentration × volume should return the mass.", say="Answer: 18 g/dm³. Check by multiplying back:", done="Returns 3.6 g, so 18 g/dm³ is right."),
]
b[3]["misconceptions"][0]["expect"] = 0.018
b[3]["misconceptions"][0]["message"] = "Convert 200 cm³ to 0.2 dm³ first, then c = 3.6 ÷ 0.2 = 18 g/dm³. Dividing by 200 gives 0.018, a thousand times too small."

# edit numbers to remove duplicate solution [2] clash with bronze[1]:
# 0.25 dm3 -> 0.2 dm3, so 0.5 / 0.2 = 2.5 mol/dm3
b[4]["display"] = "0.5 mol of solute is dissolved in 0.2 dm³ of water. Calculate the concentration in mol/dm³."
b[4]["solutions"] = [2.5]
b[4]["guided_steps"] = [
    say("The equation is <strong>concentration = moles ÷ volume in dm³</strong>. The volume is already in dm³."),
    box("Moles of solute = ", 0.5, "Given directly."),
    box("Volume (dm³) = ", 0.2, "Already in dm³, no conversion needed."),
    box("0.5 ÷ 0.2 = ", 2.5, "Divide moles by volume.", say="Now divide.", phase="substitute"),
    box("2.5 × 0.2 = ", 0.5, "Concentration × volume should return the moles.", say="Answer: 2.5 mol/dm³. Check by multiplying back:", done="Returns 0.5 mol, so 2.5 mol/dm³ is right."),
]
b[4]["misconceptions"][0]["expect"] = 0.4
b[4]["misconceptions"][0]["message"] = "Concentration is moles ÷ volume. 0.5 ÷ 0.2 = 2.5 mol/dm³. Dividing the other way (0.2 ÷ 0.5) gives 0.4, which is upside down."

b[5]["guided_steps"] = [
    say("Rearranged, <strong>moles = concentration × volume in dm³</strong>. Convert the volume first."),
    box("Convert the volume: 500 ÷ 1000 = ", 0.5, "Divide cm³ by 1,000 to get dm³.", post=" dm³"),
    box("Concentration (mol/dm³) = ", 0.4, "Given directly."),
    box("0.4 × 0.5 = ", 0.2, "Multiply concentration by volume in dm³.", say="Now multiply.", phase="substitute"),
    box("0.2 ÷ 0.5 = ", 0.4, "Moles ÷ volume should return the concentration.", say="Answer: 0.2 mol. Check by dividing back:", done="Returns 0.4 mol/dm³, so 0.2 mol is right."),
]
b[5]["misconceptions"][0]["expect"] = 200
b[5]["misconceptions"][0]["message"] = "Convert 500 cm³ to 0.5 dm³ first. moles = 0.4 × 0.5 = 0.2 mol. Using 500 gives 200 mol, which is impossibly large."

# ================= SILVER =================
s = pb["silver"]
s[0]["guided_steps"] = [
    say("Rearrange <strong>rate = volume ÷ time</strong> to <strong>volume = rate × time</strong>."),
    box("Mean rate (cm³/s) = ", 1.5, "Given directly."),
    box("Time (s) = ", 40, "Already in seconds."),
    box("1.5 × 40 = ", 60, "Multiply rate by time.", say="Now multiply.", phase="substitute"),
    box("60 ÷ 40 = ", 1.5, "Volume ÷ time should return the rate.", say="Answer: 60 cm³. Check by dividing back:", done="Returns 1.5 cm³/s, so 60 cm³ is right."),
]
s[0]["misconceptions"][0]["expect"] = 0.0375
s[0]["misconceptions"][0]["message"] = "Rearrange to volume = rate × time = 1.5 × 40 = 60 cm³. Dividing instead (1.5 ÷ 40) gives 0.0375, far too small."

s[1]["guided_steps"] = [
    say("The equation is <strong>concentration = moles ÷ volume in dm³</strong>. Convert the volume first."),
    box("Convert the volume: 500 ÷ 1000 = ", 0.5, "Divide cm³ by 1,000.", post=" dm³"),
    box("Moles of HCl = ", 0.4, "Given directly."),
    box("0.4 ÷ 0.5 = ", 0.8, "Divide moles by volume in dm³.", say="Now divide.", phase="substitute"),
    box("0.8 × 0.5 = ", 0.4, "Concentration × volume should return the moles.", say="Answer: 0.8 mol/dm³. Check by multiplying back:", done="Returns 0.4 mol, so 0.8 mol/dm³ is right."),
]
s[1]["misconceptions"][0]["expect"] = 0.0008
s[1]["misconceptions"][0]["message"] = "Convert 500 cm³ to 0.5 dm³. c = 0.4 ÷ 0.5 = 0.8 mol/dm³. Dividing by 500 gives 0.0008."

s[2]["guided_steps"] = [
    say("Rearrange <strong>concentration = moles ÷ volume</strong> to <strong>volume = moles ÷ concentration</strong>."),
    box("Moles needed = ", 0.1, "Given directly."),
    box("Concentration (mol/dm³) = ", 2, "Given directly."),
    box("0.1 ÷ 2 = ", 0.05, "Divide moles by concentration.", say="Now divide.", phase="substitute"),
    box("0.05 × 2 = ", 0.1, "Volume × concentration should return the moles.", say="Answer: 0.05 dm³. Check by multiplying back:", done="Returns 0.1 mol, so 0.05 dm³ is right."),
]
s[2]["misconceptions"][0]["expect"] = 20
s[2]["misconceptions"][0]["message"] = "Volume = moles ÷ concentration = 0.1 ÷ 2 = 0.05 dm³. Dividing the other way (2 ÷ 0.1) gives 20, far too big for so little solute."

s[3]["chart"] = {
    "type": "line",
    "data": {
        "labels": [0, 10, 20, 30, 40, 50],
        "datasets": [{
            "label": "Volume of gas (cm³)",
            "data": [0, 30, 42, 48, 50, 50],
            "borderColor": "#2563eb",
            "backgroundColor": "rgba(37,99,235,0.1)",
            "fill": True,
            "tension": 0.35,
            "pointRadius": 4
        }]
    },
    "options": {
        "scales": {
            "x": {"title": {"display": True, "text": "Time (s)"}},
            "y": {"title": {"display": True, "text": "Volume of gas (cm³)"}, "beginAtZero": True}
        }
    }
}
s[3]["guided_steps"] = [
    say("Mean rate over a period = <strong>volume produced in that period ÷ time of that period</strong>. Read the values for the first 10 s off the graph."),
    box("Volume produced in the first 10 s (cm³) = ", 30, "Read the curve at t = 10 s."),
    box("Length of that period (s) = ", 10, "The first 10 seconds."),
    box("30 ÷ 10 = ", 3, "Divide the volume by the time.", say="Now divide.", phase="substitute"),
    box("3 × 10 = ", 30, "Rate × time should return the 30 cm³.", say="Answer: 3 cm³/s. Check by multiplying back:", done="Returns 30 cm³, so 3 cm³/s is right."),
]
s[3]["misconceptions"][0]["expect"] = 1.25
s[3]["misconceptions"][0]["message"] = "For the first 10 s, use the volume produced in that period: 30 ÷ 10 = 3 cm³/s. Using the totals (50 ÷ 40) gives 1.25, the mean over the whole reaction."

# ================= GOLD =================
g = pb["gold"]
g[0]["hint"] = "Two steps: moles = mass ÷ Mr, then concentration = moles ÷ volume in dm³."
g[0]["guided_steps"] = [
    say("Two steps. First <strong>moles = mass ÷ Mr</strong>, then <strong>concentration = moles ÷ volume in dm³</strong>."),
    box("Moles: 5.85 ÷ 58.5 = ", 0.1, "Divide the mass by the relative formula mass."),
    box("Convert the volume: 250 ÷ 1000 = ", 0.25, "Divide cm³ by 1,000.", post=" dm³"),
    box("0.1 ÷ 0.25 = ", 0.4, "Divide moles by volume in dm³.", say="Now find the concentration.", phase="substitute"),
    box("0.4 × 0.25 = ", 0.1, "Concentration × volume should return the moles.", say="Answer: 0.4 mol/dm³. Check by multiplying back:", done="Returns 0.1 mol, so 0.4 mol/dm³ is right."),
]
g[0]["misconceptions"][0]["expect"] = 23.4
g[0]["misconceptions"][0]["message"] = "First turn the mass into moles: 5.85 ÷ 58.5 = 0.1 mol. Then c = 0.1 ÷ 0.25 = 0.4 mol/dm³. Using the mass 5.85 straight in gives 23.4, which would be g/dm³."
g[0]["misconceptions"][1]["expect"] = 0.0004
g[0]["misconceptions"][1]["message"] = "Convert 250 cm³ to 0.25 dm³ first. c = 0.1 ÷ 0.25 = 0.4 mol/dm³. Dividing by 250 gives 0.0004."

g[1]["hint"] = "Ratio = rate at 30 s ÷ rate in the first 10 s."
g[1]["guided_steps"] = [
    say("The ratio of the later rate to the earlier rate = <strong>rate at 30 s ÷ rate in the first 10 s</strong>."),
    box("Rate at 30 s (cm³/s) = ", 1.5, "Given from the tangent."),
    box("Rate in the first 10 s (cm³/s) = ", 5, "The mean rate given for the first 10 s."),
    box("1.5 ÷ 5 = ", 0.3, "Divide the later rate by the earlier rate.", say="Now divide.", phase="substitute"),
    box("0.3 × 5 = ", 1.5, "The ratio × the earlier rate should return the 30 s rate.", say="Answer: 0.3 (the rate has fallen to 30% of its start). Check by multiplying back:", done="Returns 1.5 cm³/s, so 0.3 is right."),
]
g[1]["misconceptions"][0]["expect"] = None
g[1]["misconceptions"][0]["message"] = "Divide the later rate by the earlier one: 1.5 ÷ 5 = 0.3. Dividing the other way (5 ÷ 1.5) turns it upside down and suggests the reaction sped up, which it did not."

g[2]["hint"] = "Volume = moles ÷ concentration gives dm³; multiply by 1,000 for cm³."
g[2]["guided_steps"] = [
    say("Rearrange to <strong>volume = moles ÷ concentration</strong> (this gives dm³), then convert dm³ to cm³."),
    box("Moles of solute = ", 0.05, "Given directly."),
    box("Concentration (mol/dm³) = ", 0.1, "Given directly."),
    box("0.05 ÷ 0.1 = ", 0.5, "Divide moles by concentration to get dm³.", say="Now find the volume in dm³.", post=" dm³", phase="substitute"),
    box("0.5 × 1000 = ", 500, "Multiply dm³ by 1,000 to get cm³.", say="The question wants cm³, so convert:"),
    box("0.1 × 0.5 = ", 0.05, "Concentration × volume in dm³ should return the moles.", say="Answer: 500 cm³. Check the dm³ volume back:", done="Returns 0.05 mol, so 500 cm³ is right."),
]
g[2]["misconceptions"][0]["expect"] = 0.5
g[2]["misconceptions"][0]["message"] = "Volume = 0.05 ÷ 0.1 = 0.5 dm³. Convert to cm³ by × 1,000: 500 cm³. Stopping at 0.5 forgets the final conversion the question asks for."

# ================= TIER GUIDES =================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one step, right units",
        "steps": [
            "Pick the equation: mean rate = quantity ÷ time, or concentration = amount ÷ volume in dm³.",
            "Read the two numbers straight from the question, put them in, and divide.",
            "Write the answer with its unit (cm³/s, g/dm³ or mol/dm³) and check by multiplying back."
        ],
        "example": {
            "question": "A reaction gives 36 cm³ of gas in 9 s. Find the mean rate.",
            "steps": [
                {"label": "Equation", "content": "<p>mean rate = volume ÷ time</p>"},
                {"label": "Substitute", "content": "<p>36 ÷ 9</p>"},
                {"label": "Check", "content": "<p>4 × 9 = 36 ✓</p>"},
                {"label": "Answer", "content": "<p><strong>4 cm³/s</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: convert or rearrange first",
        "steps": [
            "The numbers are not ready. Convert the volume from cm³ to dm³ (÷ 1,000), or rearrange the equation to make your unknown the subject.",
            "Then substitute and calculate as normal.",
            "State the unit and check the answer fits the numbers."
        ],
        "example": {
            "question": "0.2 mol of solute is dissolved in 400 cm³. Find the concentration in mol/dm³.",
            "steps": [
                {"label": "Convert", "content": "<p>400 ÷ 1000 = 0.4 dm³</p>"},
                {"label": "Substitute", "content": "<p>0.2 ÷ 0.4</p>"},
                {"label": "Check", "content": "<p>0.5 × 0.4 = 0.2 ✓</p>"},
                {"label": "Answer", "content": "<p><strong>0.5 mol/dm³</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: chain two steps",
        "steps": [
            "Gold problems need a first step before the main one: find moles from mass (÷ Mr), read a value off a graph, or convert dm³ to cm³ at the end.",
            "Do that step, then use the result in the concentration or rate equation.",
            "Keep units straight the whole way and check the final answer."
        ],
        "example": {
            "question": "2.0 g of NaOH (Mr = 40) is dissolved in 250 cm³. Find the concentration in mol/dm³.",
            "steps": [
                {"label": "Moles", "content": "<p>2.0 ÷ 40 = 0.05 mol</p>"},
                {"label": "Convert", "content": "<p>250 ÷ 1000 = 0.25 dm³</p>"},
                {"label": "Concentration", "content": "<p>0.05 ÷ 0.25</p>"},
                {"label": "Answer", "content": "<p><strong>0.2 mol/dm³</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ================= GUIDED (opener + teach) =================
pd["guided"] = {
    "opener": {
        "label": "Before any chemistry",
        "display": "A tap fills a bucket: 12 litres of water in 4 seconds.",
        "steps": [
            box("Litres each second = ", 3,
                "Share the 12 litres out over the 4 seconds: 12 ÷ 4.",
                say="No chemistry yet, just the tap. Twelve litres pour out over four seconds, spread evenly."),
            box("Now dissolve 6 g of sugar in 2 litres of water. Grams per litre = ", 3,
                "Share the 6 g out over the 2 litres: 6 ÷ 2.",
                say="That was a <strong>rate</strong>: amount ÷ time. In a reaction the amount is gas made or mass lost, so mean rate = quantity ÷ time. Same move, new words."),
            say("That second one is <strong>concentration</strong>: amount ÷ volume. Chemists measure volume in dm³ (1 dm³ = 1 litre = 1,000 cm³), so watch the units, but the idea is exactly what you just did.")
        ]
    },
    "teach": {
        "bronze": {
            "display": "A reaction produces 45 cm³ of gas in 15 s. Calculate the mean rate.",
            "label": "Together: your first one",
            "steps": [
                say("The equation is <strong>mean rate = volume ÷ time</strong>. Read the two numbers."),
                box("Volume of gas (cm³) = ", 45, "Given directly."),
                box("Time (s) = ", 15, "Already in seconds."),
                box("45 ÷ 15 = ", 3, "Share 45 cm³ over 15 seconds.", say="Now divide.", phase="substitute"),
                box("3 × 15 = ", 45, "Rate × time should return the volume.", say="Answer: 3 cm³/s. Check by multiplying back:", done="Returns 45 cm³, so 3 cm³/s is right.")
            ]
        },
        "silver": {
            "display": "6 g of salt is dissolved in 300 cm³ of water. Calculate the concentration in g/dm³.",
            "label": "Together: the silver move",
            "steps": [
                say("The equation is <strong>concentration = mass ÷ volume in dm³</strong>. The volume is in cm³, so convert it first."),
                box("Convert the volume: 300 ÷ 1000 = ", 0.3, "Divide cm³ by 1,000.", post=" dm³"),
                box("Mass (g) = ", 6, "Given directly."),
                box("6 ÷ 0.3 = ", 20, "Divide mass by volume in dm³.", say="Now divide.", phase="substitute"),
                box("20 × 0.3 = ", 6, "Concentration × volume should return the mass.", say="Answer: 20 g/dm³. Check by multiplying back:", done="Returns 6 g, so 20 g/dm³ is right.")
            ]
        },
        "gold": {
            "display": "1.17 g of NaCl (Mr = 58.5) is dissolved in 100 cm³. Calculate the concentration in mol/dm³.",
            "label": "Together: the gold move",
            "steps": [
                say("Two steps: <strong>moles = mass ÷ Mr</strong>, then <strong>concentration = moles ÷ volume in dm³</strong>."),
                box("Moles: 1.17 ÷ 58.5 = ", 0.02, "Divide the mass by the relative formula mass."),
                box("Convert the volume: 100 ÷ 1000 = ", 0.1, "Divide cm³ by 1,000.", post=" dm³"),
                box("0.02 ÷ 0.1 = ", 0.2, "Divide moles by volume in dm³.", say="Now find the concentration.", phase="substitute"),
                box("0.2 × 0.1 = ", 0.02, "Concentration × volume should return the moles.", say="Answer: 0.2 mol/dm³. Check by multiplying back:", done="Returns 0.02 mol, so 0.2 mol/dm³ is right.")
            ]
        }
    }
}

json.dump(pd, io.open("lesson_chemistry-calculations-L04@6f3d09988e.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written")
