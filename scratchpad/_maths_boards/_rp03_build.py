# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_rp03_live.json", encoding="utf-8"))
pb = pd["problem_bank"]

# ---- hints per tier (index-aligned) ----
hints = {
    "bronze": [
        "Speed = distance ÷ time, so divide 120 by 2.",
        "Speed = distance ÷ time: divide 400 by 50.",
        "Distance = speed × time, so multiply 90 by 3.",
        "Time = distance ÷ speed: divide 200 by 50.",
        "Density = mass ÷ volume, so divide 600 by 200.",
        "Mass = density × volume: multiply 8 by 25.",
        "Pressure = force ÷ area, so divide 300 by 6.",
        "Distance = speed × time: multiply 12 by 30.",
    ],
    "silver": [
        "Turn 30 minutes into 0.5 hours first, then divide 45 by 0.5.",
        "Volume = mass ÷ density: divide 936 by 7.8.",
        "Write 2 h 15 min as 2.25 hours, then multiply by 80.",
        "Change 2.5 litres to 2500 cm³, then multiply by 1.2.",
        "Area = force ÷ pressure: divide 500 by 200.",
        "Use metres and seconds: 60000 m ÷ 2700 s.",
        "Find the mass in grams (2.4 × 150), then divide by 1000 for kg.",
    ],
    "gold": [
        "Find each leg's time first, then total distance ÷ total time.",
        "Work out each mass with M = D × V, then add them.",
        "Find the volume (mass ÷ density), then take the cube root.",
        "To change km/h to m/s, divide by 3.6.",
        "Divide the force by the area in m², then change Pa to kPa by dividing by 1000.",
    ],
}

# ---- expect + message overrides per misconception (index by tier, problem, misc) ----
# value: (expect, new_message_or_None)
ov = {
    ("bronze", 0, 0): (1, None),
    ("bronze", 0, 1): (None, None),
    ("bronze", 1, 0): (1, None),
    ("bronze", 1, 1): (2, None),
    ("bronze", 2, 0): (1, None),
    ("bronze", 2, 1): (None, None),
    ("bronze", 3, 0): (1, None),
    ("bronze", 3, 1): (None, None),
    ("bronze", 4, 0): (1, None),
    ("bronze", 4, 1): (2, None),
    ("bronze", 5, 0): (2, "Mass = density × volume, so multiply. Dividing 8 ÷ 25 gives 0.32 g, which is wrong. 8 × 25 = 200 g."),
    ("bronze", 5, 1): (None, None),
    ("bronze", 6, 0): (1, None),
    ("bronze", 6, 1): (None, None),
    ("bronze", 7, 0): (1, "Distance = speed × time, so multiply. Dividing 30 ÷ 12 gives 2.5 m, which is wrong. 12 × 30 = 360 m."),
    ("bronze", 7, 1): (None, None),

    ("silver", 0, 0): (1, "You divided by 30 minutes instead of 0.5 hours, giving 1.5. Convert first: 30 min = 0.5 h, then 45 ÷ 0.5 = 90 km/h."),
    ("silver", 0, 1): (None, None),
    ("silver", 1, 0): (1, "Volume = mass ÷ density, so divide. Multiplying 936 × 7.8 gives 7300.8, which is wrong. 936 ÷ 7.8 = 120 cm³."),
    ("silver", 1, 1): (None, None),
    ("silver", 2, 0): (1, "Using just 2 hours gives 80 × 2 = 160 km. 15 minutes is 0.25 hours, so use 2.25 hours: 80 × 2.25 = 180 km."),
    ("silver", 2, 1): (None, None),
    ("silver", 3, 0): (2, "Using 2.5 without converting gives 1.2 × 2.5 = 3 g. First change 2.5 litres to 2500 cm³: 1.2 × 2500 = 3000 g."),
    ("silver", 3, 1): (None, None),
    ("silver", 4, 0): (1, "Area = force ÷ pressure, so divide. Multiplying 500 × 200 gives 100000, which is wrong. 500 ÷ 200 = 2.5 m²."),
    ("silver", 4, 1): (None, None),
    ("silver", 5, 0): (1, "That is the speed in km/h: 60 ÷ 0.75 = 80. The question wants m/s: 60000 m ÷ 2700 s = 22.2 m/s."),
    ("silver", 5, 1): (3, "You used metres but left the time in minutes, giving 60000 ÷ 45 = 1333.3. Convert 45 min to 2700 s: 60000 ÷ 2700 = 22.2 m/s."),
    ("silver", 6, 0): (1, "Mass = 2.4 × 150 = 360 g. That is grams, not kilograms. Divide by 1000: 360 ÷ 1000 = 0.36 kg."),
    ("silver", 6, 1): (None, None),

    ("gold", 0, 0): (None, "Do not average the two speeds. Find each time: 30 ÷ 60 = 0.5 h and 45 ÷ 90 = 0.5 h. Total distance 75 km ÷ total time 1 h = 75 km/h."),
    ("gold", 0, 1): (None, None),
    ("gold", 1, 0): (3, "Adding the densities (3 + 5 = 8) and multiplying by the total volume (160) gives 1280 g, which is wrong. Find each mass: 3 × 100 = 300 and 5 × 60 = 300, total 600 g."),
    ("gold", 1, 1): (None, None),
    ("gold", 2, 0): (2, "You found the volume but stopped there. Volume = 729 ÷ 2.7 = 270 cm³, then the side is the cube root: ∛270 = 6.46 cm."),
    ("gold", 2, 1): (3, "You took the cube root of the mass: ∛729 = 9. Divide by the density first: 729 ÷ 2.7 = 270, then ∛270 = 6.46 cm."),
    ("gold", 3, 0): (1, "km/h to m/s means divide by 3.6, not multiply by 3600. 108 ÷ 3.6 = 30 m/s."),
    ("gold", 3, 1): (None, None),
    ("gold", 4, 0): (None, "Pressure = force ÷ area = 600 ÷ 0.0001 = 6 000 000 Pa. Then 6 000 000 ÷ 1000 = 6000 kPa."),
    ("gold", 4, 1): (None, None),
}

# ---- fix pre-existing em dashes in worked_examples labels (style rule) ----
for we in pd.get("worked_examples") or []:
    for st in we.get("steps") or []:
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---- apply hints ----
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        p["hint"] = hints[tier][i]

# ---- fix G3 option (index 0) 6.43 -> 6.46 ----
g3 = pb["gold"][2]
assert g3["options"][0] == "6.43 cm", g3["options"][0]
g3["options"][0] = "6.46 cm"

# ---- apply expects + message overrides ----
for (tier, pi, mi), (expect, msg) in ov.items():
    m = pb[tier][pi]["misconceptions"][mi]
    m["expect"] = expect
    if msg is not None:
        m["message"] = msg

# sanity: every misconception has expect key
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        for j, m in enumerate(p.get("misconceptions") or []):
            assert "expect" in m, (tier, i, j)

# ---- tier_guides ----
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: pick the formula and do one step",
        "steps": [
            "Three formulas share one shape: <strong>Speed = Distance ÷ Time</strong>, <strong>Density = Mass ÷ Volume</strong>, <strong>Pressure = Force ÷ Area</strong>.",
            "Cover the letter you want in the triangle. If it sits on top you divide the other two; if it sits on the bottom you multiply them.",
            "Read the two numbers from the question, put them in, do one calculation, and keep the unit (km/h, g/cm³, Pa) with your answer.",
        ],
        "example": {
            "question": "A car travels 150 km in 3 hours. Find its speed.",
            "steps": [
                {"label": "Formula", "content": "<p>Speed = Distance ÷ Time</p>"},
                {"label": "Substitute", "content": "<p>\\(150 \\div 3 = 50\\)</p>"},
                {"label": "Check", "content": "<p>\\(50 \\times 3 = 150\\) km ✓</p>"},
                {"label": "Answer", "content": "<p><strong>50 km/h</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: rearrange and convert units",
        "steps": [
            "You may be given the answer letter and asked to work backwards. From <strong>D = M ÷ V</strong> you get <strong>M = D × V</strong> and <strong>V = M ÷ D</strong>.",
            "Check units before calculating: minutes to hours divide by 60, litres to cm³ multiply by 1000, km to m multiply by 1000.",
            "Convert first, calculate second, then change the answer into the unit the question asks for, such as grams into kilograms.",
        ],
        "example": {
            "question": "A block has density 3 g/cm³ and volume 250 cm³. Find its mass in kg.",
            "steps": [
                {"label": "Rearrange", "content": "<p>Mass = Density × Volume</p>"},
                {"label": "Substitute", "content": "<p>\\(3 \\times 250 = 750\\) g</p>"},
                {"label": "Convert", "content": "<p>\\(750 \\div 1000 = 0.75\\) kg</p>"},
                {"label": "Check", "content": "<p>\\(0.75 \\times 1000 = 750\\) g ✓</p>"},
                {"label": "Answer", "content": "<p><strong>0.75 kg</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: multi-step and compound units",
        "steps": [
            "Gold problems chain two ideas: find one quantity, then use it. For a cube, density gives volume, and the cube root of the volume gives the side.",
            "Compound units need care. To change km/h to m/s divide by 3.6; to change m/s to km/h multiply by 3.6.",
            "For an average speed over several legs, never average the speeds. Add the distances, add the times, then divide total distance by total time.",
        ],
        "example": {
            "question": "Travel 120 km at 40 km/h, then 120 km at 120 km/h. Find the average speed.",
            "steps": [
                {"label": "Times", "content": "<p>\\(120 \\div 40 = 3\\) h and \\(120 \\div 120 = 1\\) h</p>"},
                {"label": "Totals", "content": "<p>Distance 240 km, time 4 h</p>"},
                {"label": "Divide", "content": "<p>\\(240 \\div 4 = 60\\) km/h</p>"},
                {"label": "Check", "content": "<p>Not \\((40 + 120) \\div 2 = 80\\). The average is 60 km/h.</p>"},
                {"label": "Answer", "content": "<p><strong>60 km/h</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---- guided.opener + guided.teach ----
pd["guided"] = {
    "opener": {
        "label": "Before any formulas",
        "display": "A coach leaves at 1 pm and arrives at 4 pm.<br>In that time it covers 120 miles.",
        "steps": [
            {
                "say": "No formulas yet, just share it out. The trip lasts 3 hours, from 1 pm to 4 pm.",
                "pre": "Miles covered each hour: ",
                "post": "",
                "answer": 40,
                "hint": "Split 120 miles evenly across 3 hours: 120 ÷ 3.",
            },
            {
                "say": "Now a runner: she covers 100 metres every 10 seconds at a steady pace.",
                "pre": "Metres each second: ",
                "post": "",
                "answer": 10,
                "hint": "Split 100 m across 10 s: 100 ÷ 10.",
            },
            {
                "say": "Both times you shared a distance over a time. That IS speed: <strong>Speed = Distance ÷ Time</strong>. The same share-it-out idea gives <strong>Density = Mass ÷ Volume</strong> and <strong>Pressure = Force ÷ Area</strong>.",
            },
        ],
    },
    "teach": {
        "bronze": {
            "display": "A train covers 300 km in 5 hours at a steady speed.",
            "label": "Together: your first one",
            "steps": [
                {"say": "Start with the formula. Speed = Distance ÷ Time.", "pre": "300 ÷ 5 = ", "post": " km/h", "answer": 60, "hint": "Divide the distance by the time."},
                {"say": "The same three numbers make a triangle, so you can go backwards. In 2 hours at 60 km/h:", "pre": "60 × 2 = ", "post": " km", "answer": 120, "hint": "Distance = speed × time."},
                {"say": "To find a time instead, divide. How long for 180 km at 60 km/h?", "pre": "180 ÷ 60 = ", "post": " hours", "answer": 3, "hint": "Time = distance ÷ speed."},
                {"say": "Check the speed against the start.", "pre": "60 × 5 = ", "post": " km", "answer": 300, "done": "Back to the 300 km we began with, so 60 km/h is right.", "hint": "Speed × time should rebuild the distance."},
            ],
        },
        "silver": {
            "display": "A journey of 30 km takes 24 minutes. Find the speed in km/h, then use it.",
            "label": "Together: convert, then calculate",
            "steps": [
                {"say": "Speed in km/h needs the time in hours. Convert 24 minutes.", "pre": "24 ÷ 60 = ", "post": " hours", "answer": 0.4, "hint": "Divide minutes by 60."},
                {"say": "Now divide distance by time.", "pre": "30 ÷ 0.4 = ", "post": " km/h", "answer": 75, "hint": "Speed = distance ÷ time."},
                {"say": "Rearrange to find a time. How long for 45 km at this speed?", "pre": "45 ÷ 75 = ", "post": " hours", "answer": 0.6, "hint": "Time = distance ÷ speed."},
                {"say": "Turn that back into minutes.", "pre": "0.6 × 60 = ", "post": " minutes", "answer": 36, "done": "Convert in, calculate, convert out.", "hint": "Multiply hours by 60."},
            ],
        },
        "gold": {
            "display": "A car covers 90 km in 50 minutes. Find its speed in m/s.",
            "label": "Together: compound units",
            "steps": [
                {"say": "For m/s, work in metres and seconds. Distance first.", "pre": "90 × 1000 = ", "post": " m", "answer": 90000, "hint": "1 km = 1000 m."},
                {"say": "Now the time in seconds.", "pre": "50 × 60 = ", "post": " s", "answer": 3000, "hint": "1 minute = 60 seconds."},
                {"say": "Divide to get metres per second.", "pre": "90000 ÷ 3000 = ", "post": " m/s", "answer": 30, "hint": "Speed = distance ÷ time."},
                {"say": "Check by the km/h route: 90 km in 50 min is \\(90 \\div (50 \\div 60) = 108\\) km/h. Divide by 3.6.", "pre": "108 ÷ 3.6 = ", "post": " m/s", "answer": 30, "done": "Both routes give 30 m/s, so it is right.", "hint": "km/h ÷ 3.6 = m/s."},
            ],
        },
    },
}

json.dump(pd, io.open("lesson_maths-eduqas_ratio-proportion-L03.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("written. gold[2] options:", pb["gold"][2]["options"])
print("total problems:", sum(len(pb[t]) for t in ("bronze","silver","gold")))
