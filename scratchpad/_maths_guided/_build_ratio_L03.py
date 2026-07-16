# -*- coding: utf-8 -*-
import json, io

SRC = "_live_ratio-proportion-L03.json"
OUT = "lesson_ratio-proportion-L03.json"

pd = json.load(io.open(SRC, encoding="utf-8"))

# ---- helpers ---------------------------------------------------------------
def say(t):
    return {"say": t}

def box(pre, answer, hint, post="", done=None, phase=False):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if done is not None:
        d["done"] = done
    if phase:
        d["phase"] = "substitute"
    return d

# ============================================================================
# method_card (slim)
# ============================================================================
pd["method_card"] = {
    "title": "Speed, Density & Pressure",
    "steps": [
        "Choose the formula: Speed = Distance ÷ Time, Density = Mass ÷ Volume, Pressure = Force ÷ Area.",
        "Check the units match, and convert if needed (km/h to m/s is ÷ 3.6).",
        "Rearrange with a formula triangle: cover the quantity you want to find.",
        "Substitute, calculate, and state the units."
    ],
    "content": "<p>Each measure is one quantity shared over another. Use a <strong>formula triangle</strong>: cover the quantity you want. If the other two sit side by side, multiply; if one is above the other, divide.</p><p>$$\\text{Speed}=\\frac{\\text{Distance}}{\\text{Time}} \\quad \\text{Density}=\\frac{\\text{Mass}}{\\text{Volume}} \\quad \\text{Pressure}=\\frac{\\text{Force}}{\\text{Area}}$$</p>",
    "example": "<p><strong>A block has mass 450 g and volume 50 cm³.</strong></p><p>Density = 450 ÷ 50 = 9 g/cm³.</p>"
}

# ============================================================================
# worked_examples: fix em-dash labels (required by style rule / validator)
# ============================================================================
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str):
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ============================================================================
# problem_bank
# ============================================================================
pb = pd["problem_bank"]
bronze = pb["bronze"]
silver = pb["silver"]
gold = pb["gold"]

# ---------- BRONZE ----------
bronze[0]["hint"] = "Speed is distance shared over time, so divide 30 by 2."
bronze[0]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 60,
    "message": "60 comes from multiplying, 30 × 2. To find speed you divide: Speed = Distance ÷ Time = 30 ÷ 2 = 15 km/h.",
    "note": "error: multiplied instead of divided"
}]
bronze[0]["guided_steps"] = [
    say("Speed = Distance ÷ Time. It shares the distance out over the hours. The distance is 30 km, the time is 2 hours."),
    box("First, the distance to share out is ", 30, "Read the distance straight from the question.", post=" km"),
    box("Now divide over the 2 hours: 30 ÷ 2 = ", 15, "How far is covered in one hour?", post=" km/h", phase=True),
    box("Check by going forward: 15 × 2 = ", 30, "Speed × time should rebuild the distance.", post=" km", done="Back to 30 km, so 15 km/h is right.", phase=True),
]

bronze[1]["hint"] = "Distance is speed times time, so multiply 80 by 3."
bronze[1]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 26.67,
    "message": "26.67 is 80 ÷ 3, dividing. To find distance you multiply: Distance = Speed × Time = 80 × 3 = 240 km.",
    "note": "error: divided instead of multiplied"
}]
bronze[1]["guided_steps"] = [
    say("Distance = Speed × Time. The speed is 80 km/h, the time is 3 hours."),
    box("First, the time travelled is ", 3, "Read the time from the question.", post=" hours"),
    box("Multiply: 80 × 3 = ", 240, "80 km each hour, for 3 hours.", post=" km", phase=True),
    box("Check the other way: 240 ÷ 3 = ", 80, "Distance ÷ time should rebuild the speed.", post=" km/h", done="Back to 80 km/h, so 240 km is right.", phase=True),
]

bronze[2]["hint"] = "Density is mass shared over volume, so divide 200 by 25."
bronze[2]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 0.125,
    "message": "0.125 is 25 ÷ 200, the formula upside down. Density = Mass ÷ Volume = 200 ÷ 25 = 8 g/cm³.",
    "note": "error: inverted the formula"
}]
bronze[2]["guided_steps"] = [
    say("Density = Mass ÷ Volume: the mass packed into each cm³. The mass is 200 g, the volume is 25 cm³."),
    box("First, the mass to share out is ", 200, "Read the mass from the question.", post=" g"),
    box("Now divide: 200 ÷ 25 = ", 8, "How many grams sit in each cm³?", post=" g/cm³", phase=True),
    box("Check: 8 × 25 = ", 200, "Density × volume should rebuild the mass.", post=" g", done="Back to 200 g, so 8 g/cm³ is right.", phase=True),
]

bronze[3]["hint"] = "Mass is density times volume, so multiply 3 by 40."
bronze[3]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 0.075,
    "message": "0.075 is 3 ÷ 40, dividing. To find mass you multiply: Mass = Density × Volume = 3 × 40 = 120 g.",
    "note": "error: divided instead of multiplied"
}]
bronze[3]["guided_steps"] = [
    say("Rearrange to Mass = Density × Volume. The density is 3 g/cm³, the volume is 40 cm³."),
    box("First, the volume is ", 40, "Read the volume from the question.", post=" cm³"),
    box("Multiply: 3 × 40 = ", 120, "3 g in each of the 40 cm³.", post=" g", phase=True),
    box("Check: 120 ÷ 40 = ", 3, "Mass ÷ volume should rebuild the density.", post=" g/cm³", done="Back to 3 g/cm³, so 120 g is right.", phase=True),
]

bronze[4]["hint"] = "Pressure is force shared over area, so divide 60 by 12."
bronze[4]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 0.2,
    "message": "0.2 is 12 ÷ 60, the formula flipped. Pressure = Force ÷ Area = 60 ÷ 12 = 5 N/m².",
    "note": "error: inverted the formula"
}]
bronze[4]["guided_steps"] = [
    say("Pressure = Force ÷ Area: the force on each square metre. The force is 60 N, the area is 12 m²."),
    box("First, the force to share out is ", 60, "Read the force from the question.", post=" N"),
    box("Now divide: 60 ÷ 12 = ", 5, "How much force presses on each of the 12 m²?", post=" N/m²", phase=True),
    box("Check: 5 × 12 = ", 60, "Pressure × area should rebuild the force.", post=" N", done="Back to 60 N, so 5 N/m² is right.", phase=True),
]

bronze[5]["hint"] = "Time is distance divided by speed, so divide 100 by 50."
bronze[5]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 5000,
    "message": "5000 is 100 × 50, multiplying. To find time you divide: Time = Distance ÷ Speed = 100 ÷ 50 = 2 hours.",
    "note": "error: multiplied instead of divided"
}]
bronze[5]["guided_steps"] = [
    say("Rearrange to Time = Distance ÷ Speed. The distance is 100 km, the speed is 50 km/h."),
    box("First, the distance is ", 100, "Read the distance from the question.", post=" km"),
    box("Now divide: 100 ÷ 50 = ", 2, "How many 50s fit into 100?", post=" hours", phase=True),
    box("Check: 50 × 2 = ", 100, "Speed × time should rebuild the distance.", post=" km", done="Back to 100 km, so 2 hours is right.", phase=True),
]

# B6 (CHANGED): 420 m / 60 s -> 7  (was 400/80 -> 5, duplicate value with B4)
bronze[6]["display"] = "A runner covers 420 m in 60 seconds. What is their speed in m/s?"
bronze[6]["solutions"] = [7]
bronze[6]["hint"] = "Speed is distance shared over time, so divide 420 by 60."
bronze[6]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 25200,
    "message": "25200 is 420 × 60, multiplying. Speed = Distance ÷ Time = 420 ÷ 60 = 7 m/s.",
    "note": "error: multiplied instead of divided"
}]
bronze[6]["guided_steps"] = [
    say("Speed = Distance ÷ Time. The distance is 420 m, the time is 60 s."),
    box("First, the distance run is ", 420, "Read the distance from the question.", post=" m"),
    box("Now divide: 420 ÷ 60 = ", 7, "How many metres each second?", post=" m/s", phase=True),
    box("Check: 7 × 60 = ", 420, "Speed × time should rebuild the distance.", post=" m", done="Back to 420 m, so 7 m/s is right.", phase=True),
]

# B7 (CHANGED): rearrangement force = pressure x area = 8 x 6 -> 48
bronze[7]["display"] = "A pressure of 8 N/m² acts over an area of 6 m². Find the force in N."
bronze[7]["solutions"] = [48]
bronze[7]["hint"] = "Force is pressure times area, so multiply 8 by 6."
bronze[7]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 1.33,
    "message": "1.33 is 8 ÷ 6, still using the pressure formula. To find force you multiply: Force = Pressure × Area = 8 × 6 = 48 N.",
    "note": "error: divided instead of multiplied (8/6 = 1.333)"
}]
bronze[7]["guided_steps"] = [
    say("Rearrange Pressure = Force ÷ Area to Force = Pressure × Area. The pressure is 8 N/m², the area is 6 m²."),
    box("First, the area is ", 6, "Read the area from the question.", post=" m²"),
    box("Multiply: 8 × 6 = ", 48, "8 N presses on each of the 6 m².", post=" N", phase=True),
    box("Check: 48 ÷ 6 = ", 8, "Force ÷ area should rebuild the pressure.", post=" N/m²", done="Back to 8 N/m², so 48 N is right.", phase=True),
]

# ---------- SILVER ----------
silver[0]["hint"] = "To go from km/h to m/s, divide by 3.6."
silver[0]["misconceptions"] = [{
    "pattern": "unit_error", "check": "common", "expect": 259.2,
    "message": "259.2 comes from multiplying by 3.6. Going from km/h to m/s you DIVIDE: 72 ÷ 3.6 = 20 m/s.",
    "note": "error: multiplied by 3.6 instead of dividing"
}]
silver[0]["guided_steps"] = [
    say("km/h to m/s: divide by 3.6. There are 3600 s in an hour and 1000 m in a km, and 3600 ÷ 1000 = 3.6."),
    box("First, the speed to convert is ", 72, "Read the speed from the question.", post=" km/h"),
    box("Now divide: 72 ÷ 3.6 = ", 20, "Divide the km/h figure by 3.6.", post=" m/s", phase=True),
    box("Check by converting back: 20 × 3.6 = ", 72, "Multiply by 3.6 to undo the conversion.", post=" km/h", done="Back to 72 km/h, so 20 m/s is right.", phase=True),
]

silver[1]["hint"] = "Work out each leg's time with distance divided by speed, then add them."
silver[1]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 0.75,
    "message": "0.75 is only ONE leg's time. The total time needs both legs added: 0.75 + 0.75 = 1.5 h.",
    "note": "error: stopped after one leg"
}]
silver[1]["guided_steps"] = [
    say("Total time means each leg's time added together. For each part, Time = Distance ÷ Speed."),
    box("Leg 1: 45 ÷ 60 = ", 0.75, "Distance ÷ speed for the first part.", post=" h"),
    box("Leg 2: 30 ÷ 40 = ", 0.75, "Distance ÷ speed for the second part.", post=" h", phase=True),
    box("Total time: 0.75 + 0.75 = ", 1.5, "Add the two leg times.", post=" h", phase=True),
    box("Check leg 1: 60 × 0.75 = ", 45, "Speed × time should rebuild each distance.", post=" km", done="Back to 45 km, so the leg times are right.", phase=True),
]

silver[2]["hint"] = "Mass is density times volume, so multiply 19.3 by 52."
silver[2]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 2.7,
    "message": "2.7 is 52 ÷ 19.3, dividing. To find mass you multiply: Mass = Density × Volume = 19.3 × 52 = 1003.6 g.",
    "note": "error: divided instead of multiplied"
}]
silver[2]["guided_steps"] = [
    say("Rearrange to Mass = Density × Volume. The density is 19.3 g/cm³, the volume is 52 cm³."),
    box("First, the volume is ", 52, "Read the volume from the question.", post=" cm³"),
    box("Multiply: 19.3 × 52 = ", 1003.6, "Density times volume.", post=" g", done="1003.6 g to 1 d.p.", phase=True),
    box("Check: 1003.6 ÷ 52 = ", 19.3, "Mass ÷ volume should rebuild the density.", post=" g/cm³", done="Back to 19.3 g/cm³, so 1003.6 g is right.", phase=True),
]

silver[3]["hint"] = "Force is pressure times area, so multiply 400 by 0.15."
silver[3]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 2666.67,
    "message": "2666.67 is 400 ÷ 0.15, dividing. To find force you multiply: Force = Pressure × Area = 400 × 0.15 = 60 N.",
    "note": "error: divided instead of multiplied"
}]
silver[3]["guided_steps"] = [
    say("Rearrange to Force = Pressure × Area. The pressure is 400 N/m², the area is 0.15 m²."),
    box("First, the area is ", 0.15, "Read the area from the question.", post=" m²"),
    box("Multiply: 400 × 0.15 = ", 60, "Pressure times area.", post=" N", phase=True),
    box("Check: 60 ÷ 0.15 = ", 400, "Force ÷ area should rebuild the pressure.", post=" N/m²", done="Back to 400 N/m², so 60 N is right.", phase=True),
]

silver[4]["hint"] = "Change 1.2 kg into grams first, then divide by the density."
silver[4]["misconceptions"] = [{
    "pattern": "unit_error", "check": "common", "expect": 0.5,
    "message": "0.5 is 1.2 ÷ 2.4 without converting. The density is per gram, so change 1.2 kg to 1200 g first: 1200 ÷ 2.4 = 500 cm³.",
    "note": "error: did not convert kg to g"
}]
silver[4]["guided_steps"] = [
    say("Rearrange to Volume = Mass ÷ Density. But the units clash: mass is in kg, the density uses grams, so convert first."),
    box("Convert the mass to grams: 1.2 × 1000 = ", 1200, "There are 1000 g in 1 kg.", post=" g"),
    box("Now divide: 1200 ÷ 2.4 = ", 500, "Mass ÷ density.", post=" cm³", phase=True),
    box("Check: 2.4 × 500 = ", 1200, "Density × volume should rebuild the mass.", post=" g", done="Back to 1200 g (1.2 kg), so 500 cm³ is right.", phase=True),
]

silver[5]["hint"] = "To go from m/s to km/h, multiply by 3.6."
silver[5]["misconceptions"] = [{
    "pattern": "unit_error", "check": "common", "expect": 8.33,
    "message": "8.33 comes from dividing by 3.6. Going from m/s to km/h you MULTIPLY: 30 × 3.6 = 108 km/h.",
    "note": "error: divided instead of multiplying by 3.6"
}]
silver[5]["guided_steps"] = [
    say("m/s to km/h: multiply by 3.6, the reverse of dividing by 3.6."),
    box("First, the speed to convert is ", 30, "Read the speed from the question.", post=" m/s"),
    box("Now multiply: 30 × 3.6 = ", 108, "Multiply the m/s figure by 3.6.", post=" km/h", phase=True),
    box("Check by converting back: 108 ÷ 3.6 = ", 30, "Divide by 3.6 to undo the conversion.", post=" m/s", done="Back to 30 m/s, so 108 km/h is right.", phase=True),
]

silver[6]["hint"] = "Speed is distance divided by time, so divide 195 by 3."
silver[6]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 585,
    "message": "585 is 195 × 3, multiplying. Speed = Distance ÷ Time = 195 ÷ 3 = 65 mph.",
    "note": "error: multiplied instead of divided"
}]
silver[6]["guided_steps"] = [
    say("Speed = Distance ÷ Time. The distance is 195 miles, the time is 3 hours."),
    box("First, the distance is ", 195, "Read the distance from the question.", post=" miles"),
    box("Now divide: 195 ÷ 3 = ", 65, "Share 195 miles over 3 hours.", post=" mph", phase=True),
    box("Check: 65 × 3 = ", 195, "Speed × time should rebuild the distance.", post=" miles", done="Back to 195 miles, so 65 mph is right.", phase=True),
]

# ---------- GOLD ----------
gold[0]["hint"] = "Find each leg's time, then divide total distance by total time."
gold[0]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 70,
    "message": "70 is (60 + 80) ÷ 2, averaging the two speeds. That is wrong because more time is spent on the slow leg. Use total distance ÷ total time: 200 ÷ 3 ≈ 66.7 km/h.",
    "note": "error: averaged the speeds"
}]
gold[0]["guided_steps"] = [
    say("Average speed = total distance ÷ total time. You cannot just average 60 and 80, so find each leg's time first."),
    box("Leg 1 time = 120 ÷ 60 = ", 2, "Distance ÷ speed for the first leg.", post=" h"),
    box("Leg 2 time = 80 ÷ 80 = ", 1, "Distance ÷ speed for the second leg.", post=" h"),
    box("Total distance = 120 + 80 = ", 200, "Add the two distances.", post=" km", phase=True),
    box("Total time = 2 + 1 = ", 3, "Add the two leg times.", post=" h", phase=True),
    box("Average speed = 200 ÷ 3 = ", 66.7, "Total distance ÷ total time, to 1 d.p.", post=" km/h", done="Not 70: the slow first leg drags the average down. Sanity check: 66.7 × 3 ≈ 200 km.", phase=True),
]

gold[1]["hint"] = "Find each metal's mass, add masses and volumes, then divide."
gold[1]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 9.25,
    "message": "9.25 is (7.2 + 11.3) ÷ 2, averaging the densities. Metal A fills more volume, so it should weigh more heavily. Use total mass ÷ total volume: 4420 ÷ 500 = 8.84 g/cm³.",
    "note": "error: averaged the densities"
}]
gold[1]["guided_steps"] = [
    say("You cannot average the densities. Find each metal's mass, add the masses, add the volumes, then divide."),
    box("Mass of A = 300 × 7.2 = ", 2160, "Density × volume for metal A.", post=" g"),
    box("Mass of B = 200 × 11.3 = ", 2260, "Density × volume for metal B.", post=" g"),
    box("Total mass = 2160 + 2260 = ", 4420, "Add the two masses.", post=" g", phase=True),
    box("Total volume = 300 + 200 = ", 500, "Add the two volumes.", post=" cm³", phase=True),
    box("Density = 4420 ÷ 500 = ", 8.84, "Total mass ÷ total volume.", post=" g/cm³", done="8.84 g/cm³, or 8.8 to 1 d.p. It sits between 7.2 and 11.3, nearer A's value because A fills more volume.", phase=True),
]

gold[2]["hint"] = "Add the distances and the times, then convert to km/h."
gold[2]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 8.4,
    "message": "8.4 is the average of the two leg speeds (4.8 km/h walking and 12 km/h running). Averaging speeds ignores the time on each part. Use total distance ÷ total time: 240 ÷ 38 ≈ 6.3 km/h.",
    "note": "error: averaged the two leg speeds"
}]
gold[2]["guided_steps"] = [
    say("Average speed = total distance ÷ total time, worked in km and hours. Add the distances, add the minutes, then convert."),
    box("Total distance = 2.4 + 1.6 = ", 4, "Add the two distances.", post=" km"),
    box("Total time = 30 + 8 = ", 38, "Add the two times, in minutes.", post=" min"),
    box("There are 60 minutes in an hour, so scale the distance up: 4 × 60 = ", 240, "Distance in km times 60.", post="", phase=True),
    box("Now divide by the total minutes: 240 ÷ 38 = ", 6.3, "Divide by the 38 minutes, to 1 d.p.", post=" km/h", done="6.3 km/h to 1 d.p., a gentle walk-then-run pace, which is sensible.", phase=True),
]

gold[3]["hint"] = "Area is force divided by pressure, so divide 500 by 250."
gold[3]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 0.5,
    "message": "0.5 is 250 ÷ 500, the formula upside down. Area = Force ÷ Pressure = 500 ÷ 250 = 2 m².",
    "note": "error: inverted the formula"
}]
gold[3]["guided_steps"] = [
    say("Rearrange Pressure = Force ÷ Area to Area = Force ÷ Pressure. The weight is the force (500 N), the pressure is 250 N/m²."),
    box("First, the force (the weight) is ", 500, "The weight pressing down is the force.", post=" N"),
    box("Now divide: 500 ÷ 250 = ", 2, "Force ÷ pressure.", post=" m²", phase=True),
    box("Check: 500 ÷ 2 = ", 250, "Force ÷ area should rebuild the pressure.", post=" N/m²", done="Back to 250 N/m², so 2 m² is right.", phase=True),
]

gold[4]["hint"] = "Find the cylinder's volume first, then multiply by the density."
gold[4]["misconceptions"] = [{
    "pattern": "wrong_formula", "check": "common", "expect": 3768,
    "message": "3768 uses the diameter (10 cm) instead of the radius: 3.14 × 10² × 20 × 0.6. Use the radius 5 cm: volume = 3.14 × 5² × 20 = 1570 cm³, then mass = 0.6 × 1570 = 942 g.",
    "note": "error: used diameter 10 instead of radius 5 (4x too big)"
}]
gold[4]["guided_steps"] = [
    say("Two stages: find the cylinder's volume, then Mass = Density × Volume. Volume of a cylinder = π × r² × h, with r = 5 cm."),
    box("First r²: 5 × 5 = ", 25, "The radius squared. Use the radius, not the diameter.", post=""),
    box("Volume = 3.14 × 25 × 20 = ", 1570, "π × r² × h.", post=" cm³"),
    box("Mass = 0.6 × 1570 = ", 942, "Density × volume.", post=" g", done="942 g.", phase=True),
    box("Check: 942 ÷ 1570 = ", 0.6, "Mass ÷ volume should rebuild the density.", post=" g/cm³", done="Back to 0.6 g/cm³, so 942 g is right.", phase=True),
]

# ---------- tier descriptions ----------
pb["bronze_description"] = "One formula, one step: divide or multiply once with whole numbers, no unit changes."
pb["silver_description"] = "Rearrange the formula or convert the units first, then apply it once."
pb["gold_description"] = "Several stages: combine parts or work through a shape or journey, then round."

# ============================================================================
# tier_guides
# ============================================================================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one formula, one step",
        "steps": [
            "Pick the right formula: Speed = Distance ÷ Time, Density = Mass ÷ Volume, Pressure = Force ÷ Area. Each is a total shared over how many units.",
            "To find the <strong>top</strong> quantity, multiply the other two. To find a <strong>bottom</strong> quantity, divide the top by the one you know. A formula triangle helps: cover what you want.",
            "Do one calculation, then write the units straight from the formula (km ÷ h = km/h)."
        ],
        "example": {
            "question": "A car travels 90 km in 3 hours. Find its speed.",
            "steps": [
                {"label": "Formula", "content": "<p>Speed = Distance ÷ Time.</p>"},
                {"label": "Substitute", "content": "<p>\\(90 \\div 3 = 30\\) km/h.</p>"},
                {"label": "Check", "content": "<p>\\(30 \\times 3 = 90\\) km ✓</p>"},
                {"label": "Answer", "content": "<p><strong>30 km/h</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: convert or rearrange first",
        "steps": [
            "The formula is the same, but first make the pieces fit. You may need to <strong>rearrange</strong> (Force = Pressure × Area) or <strong>convert units</strong> before substituting.",
            "km/h to m/s: divide by 3.6. m/s to km/h: multiply by 3.6. kg to g: multiply by 1000. Get the units right, then apply the formula once.",
            "Answers may be decimals. Keep them exact unless the question asks you to round."
        ],
        "example": {
            "question": "Convert 90 km/h to m/s.",
            "steps": [
                {"label": "Rule", "content": "<p>km/h to m/s: divide by 3.6.</p>"},
                {"label": "Substitute", "content": "<p>\\(90 \\div 3.6 = 25\\) m/s.</p>"},
                {"label": "Check", "content": "<p>\\(25 \\times 3.6 = 90\\) km/h ✓</p>"},
                {"label": "Answer", "content": "<p><strong>25 m/s</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: several steps, then round",
        "steps": [
            "Break the problem into stages. For average speed over two legs, find each leg's time, then use total distance ÷ total time (never just average the speeds).",
            "For a mixture, add the masses and add the volumes before dividing. For a solid, work out its volume from the shape first, then use the density.",
            "Finish with the rounding the question asks for, and sanity-check the size of your answer."
        ],
        "example": {
            "question": "A trip: 100 km at 50 km/h, then 60 km at 60 km/h. Find the average speed (1 d.p.).",
            "steps": [
                {"label": "Leg times", "content": "<p>\\(100 \\div 50 = 2\\) h and \\(60 \\div 60 = 1\\) h.</p>"},
                {"label": "Totals", "content": "<p>Distance \\(= 160\\) km, time \\(= 3\\) h.</p>"},
                {"label": "Divide", "content": "<p>\\(160 \\div 3 = 53.3\\) km/h (1 d.p.).</p>"},
                {"label": "Check", "content": "<p>Between 50 and 60, nearer 50 (more time on the slow leg) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>53.3 km/h</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ============================================================================
# guided (opener + teach)
# ============================================================================
pd["guided"] = {
    "opener": {
        "label": "Before any formula",
        "display": "A car: 60 miles in 2 hours.<br>A shelf: 12 kg spread evenly over 3 tiles.",
        "steps": [
            {
                "say": "No formulas yet, just common sense. A car drives 60 miles in 2 hours at a steady pace.",
                "pre": "In 1 hour it goes ", "post": " miles", "answer": 30,
                "hint": "Split 60 miles evenly across the 2 hours."
            },
            {
                "say": "That is all a <strong>speed</strong> is: distance for each hour. You just did 60 ÷ 2 = 30 miles per hour. Now a heavy shelf rests evenly on 3 tiles, weighing 12 kg in total.",
                "pre": "Each tile carries ", "post": " kg", "answer": 4,
                "hint": "Share 12 kg equally between the 3 tiles."
            },
            {
                "say": "Same move: 12 ÷ 3 = 4 kg on each tile. That is what <strong>pressure</strong> measures, the force on each unit of area. <strong>Speed</strong>, <strong>density</strong> and <strong>pressure</strong> are all one total divided by how many units: distance ÷ time, mass ÷ volume, force ÷ area."
            }
        ]
    },
    "teach": {
        "bronze": {
            "display": "A metal block has mass 84 g and volume 12 cm³. Find its density in g/cm³, then find the mass of a 5 cm³ piece of the same metal.",
            "label": "Together: your first one",
            "steps": [
                say("Density = Mass ÷ Volume: the mass packed into each cm³. The mass is 84 g, the volume is 12 cm³."),
                box("84 ÷ 12 = ", 7, "Share 84 g over the 12 cm³.", post=" g/cm³"),
                say("So every cm³ of this metal weighs 7 g."),
                box("Check by rebuilding the mass: 7 × 12 = ", 84, "Density × volume returns the mass.", post=" g", done="Back to 84 g, so 7 g/cm³ is right."),
                say("The density belongs to the material, so a smaller piece has the SAME density. Find the mass of a 5 cm³ piece."),
                box("7 × 5 = ", 35, "7 g for each of the 5 cm³.", post=" g"),
                box("And that piece's density is still 35 ÷ 5 = ", 7, "Mass ÷ volume returns the density.", post=" g/cm³", done="Still 7 g/cm³. The number never changes for the same metal."),
            ]
        },
        "silver": {
            "display": "A car travels at 90 km/h. Convert this to m/s, then find how far it goes in 5 seconds.",
            "label": "Together: convert first",
            "steps": [
                say("The units do not match: the speed is in km/h but the time is in seconds. Convert the speed first. km/h to m/s: divide by 3.6."),
                box("90 ÷ 3.6 = ", 25, "Divide the km/h figure by 3.6.", post=" m/s"),
                say("Check it converts back."),
                box("25 × 3.6 = ", 90, "Multiply by 3.6 to undo the conversion.", post=" km/h", done="Back to 90 km/h, so 25 m/s is right."),
                say("Now the units match, metres and seconds. Distance = Speed × Time, for 5 seconds:"),
                box("25 × 5 = ", 125, "25 m every second, for 5 seconds.", post=" m"),
                box("Check: 125 ÷ 5 = ", 25, "Distance ÷ time returns the speed.", post=" m/s", done="The conversion and the distance both check out."),
            ]
        },
        "gold": {
            "display": "Two liquids are mixed: 200 cm³ of density 1.2 g/cm³ and 300 cm³ of density 0.8 g/cm³. Find the density of the mixture in g/cm³.",
            "label": "Together: combine, then divide",
            "steps": [
                say("You cannot average the two densities. Find each liquid's mass, add the masses, add the volumes, then divide."),
                box("Mass of liquid 1 = 200 × 1.2 = ", 240, "Density × volume gives the mass.", post=" g"),
                box("Mass of liquid 2 = 300 × 0.8 = ", 240, "Density × volume gives the mass.", post=" g"),
                box("Total mass = 240 + 240 = ", 480, "Add the two masses.", post=" g"),
                box("Total volume = 200 + 300 = ", 500, "Add the two volumes.", post=" cm³"),
                box("Density of mixture = 480 ÷ 500 = ", 0.96, "Total mass ÷ total volume.", post=" g/cm³", done="0.96 g/cm³: between 0.8 and 1.2, and nearer 0.8 because that liquid fills more volume. Sensible."),
            ]
        }
    }
}

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT)
