# -*- coding: utf-8 -*-
"""Full guided + diagrams build for ratio-proportion-L03 (maths-ocr)."""
import json, io

LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_rpL03_live.json"
OUT  = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_ratio-proportion-L03.json"

live = json.load(io.open(LIVE, encoding="utf-8"))

DIV = "÷"   # ÷
MUL = "×"   # ×

# ---------- SVG helpers ----------
def tri(top, left, right, aria):
    return (
        '<svg viewBox="0 0 200 160" role="img" aria-label="%s" style="max-width:150px;display:block;margin:0 auto 8px">'
        '<polygon points="100,12 22,150 178,150" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="2"/>'
        '<line x1="53" y1="95" x2="147" y2="95" stroke="currentColor" stroke-width="1.5"/>'
        '<line x1="100" y1="95" x2="100" y2="150" stroke="currentColor" stroke-width="1.5"/>'
        '<text x="100" y="70" text-anchor="middle" fill="currentColor" font-family="Inter,sans-serif" font-size="26">%s</text>'
        '<text x="74" y="132" text-anchor="middle" fill="currentColor" font-family="Inter,sans-serif" font-size="22">%s</text>'
        '<text x="126" y="132" text-anchor="middle" fill="currentColor" font-family="Inter,sans-serif" font-size="22">%s</text>'
        '</svg>' % (aria, top, left, right))

SPEED_TRI = tri("D", "S", "T", "Formula triangle: distance on top, speed and time below")
PRESS_TRI = tri("F", "P", "A", "Formula triangle: force on top, pressure and area below")

CUBE_SVG = (
    '<svg viewBox="0 0 150 150" role="img" aria-label="A cube of side 4 cm" style="max-width:150px;display:block;margin:0 auto 6px">'
    '<polygon points="30,55 60,30 130,30 100,55" fill="#60a5fa" fill-opacity="0.20" stroke="currentColor" stroke-width="1.6"/>'
    '<polygon points="100,55 130,30 130,100 100,125" fill="#60a5fa" fill-opacity="0.12" stroke="currentColor" stroke-width="1.6"/>'
    '<rect x="30" y="55" width="70" height="70" fill="#60a5fa" fill-opacity="0.28" stroke="currentColor" stroke-width="1.6"/>'
    '<text x="65" y="146" text-anchor="middle" fill="currentColor" font-family="Inter,sans-serif" font-size="13">4 cm</text>'
    '</svg>')

CYL_SVG = (
    '<svg viewBox="0 0 150 165" role="img" aria-label="A cylinder of radius 3 cm and height 10 cm" style="max-width:140px;display:block;margin:0 auto 6px">'
    '<rect x="35" y="28" width="70" height="100" fill="#60a5fa" fill-opacity="0.18" stroke="none"/>'
    '<line x1="35" y1="28" x2="35" y2="128" stroke="currentColor" stroke-width="1.6"/>'
    '<line x1="105" y1="28" x2="105" y2="128" stroke="currentColor" stroke-width="1.6"/>'
    '<path d="M35 128 A35 12 0 0 0 105 128" fill="none" stroke="currentColor" stroke-width="1.6"/>'
    '<ellipse cx="70" cy="28" rx="35" ry="12" fill="#60a5fa" fill-opacity="0.28" stroke="currentColor" stroke-width="1.6"/>'
    '<line x1="70" y1="28" x2="105" y2="28" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 2"/>'
    '<text x="86" y="22" text-anchor="middle" fill="currentColor" font-family="Inter,sans-serif" font-size="12">3 cm</text>'
    '<line x1="120" y1="28" x2="120" y2="128" stroke="currentColor" stroke-width="1.2"/>'
    '<text x="132" y="82" text-anchor="middle" fill="currentColor" font-family="Inter,sans-serif" font-size="12">10 cm</text>'
    '</svg>')

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

# ---------- walk builders ----------
def divide_walk(formula_say, a, b, ans, unit, hint_div, check_hint):
    """ans = a / b. Setup: read divisor. Solve + check after boundary."""
    assert abs(a / b - ans) < 1e-9, (a, b, ans)
    return [
        {"say": formula_say},
        {"pre": "Set up the division: %s %s " % (a, DIV), "post": "", "answer": b,
         "hint": "This is the number you divide by."},
        {"phase": "substitute", "pre": "%s %s %s = " % (a, DIV, b), "post": " " + unit,
         "answer": ans, "hint": hint_div},
        {"phase": "substitute", "pre": "Check: %s %s %s = " % (fmt(ans), MUL, b), "post": "",
         "answer": a, "done": "Back to %s, so %s %s is right." % (fmt(a), fmt(ans), unit),
         "hint": check_hint},
    ]

def multiply_walk(formula_say, a, b, ans, unit, hint_mul, check_hint):
    assert abs(a * b - ans) < 1e-9, (a, b, ans)
    return [
        {"say": formula_say},
        {"pre": "Set up the product: %s %s " % (a, MUL), "post": "", "answer": b,
         "hint": "This is the number you multiply by."},
        {"phase": "substitute", "pre": "%s %s %s = " % (a, MUL, b), "post": " " + unit,
         "answer": ans, "hint": hint_mul},
        {"phase": "substitute", "pre": "Check: %s %s %s = " % (fmt(ans), DIV, b), "post": "",
         "answer": a, "done": "Back to %s, so %s %s is right." % (fmt(a), fmt(ans), unit),
         "hint": check_hint},
    ]

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return str(x)

# =========================================================
# BRONZE
# =========================================================
bronze = []

# b0: 180 km / 3 h = 60 km/h
bronze.append({
    "display": "A car travels 180 km in 3 hours. What is the speed in km/h?",
    "solutions": [60], "calculator": False, "input_type": "single_value",
    "hint": "Speed = distance divided by time.",
    "misconceptions": [{
        "pattern": "multiplied_not_divided", "expect": 540,
        "message": "Speed = distance %s time, so divide: 180 %s 3 = 60. Multiplying gives 540, far too fast for a car." % (DIV, DIV),
        "note": "180*3=540"}],
    "guided_steps": divide_walk(
        "Speed = distance %s time. The distance is 180 km and the time is 3 hours." % DIV,
        180, 3, 60, "km/h", "Share the distance equally over the 3 hours.",
        "If it does not give back 180 km, something slipped."),
})

# b1: 12 km/h * 3 h = 36 km
bronze.append({
    "display": "A cyclist travels at 12 km/h for 3 hours. How far do they go?",
    "solutions": [36], "calculator": False, "input_type": "single_value",
    "hint": "Distance = speed multiplied by time.",
    "misconceptions": [{
        "pattern": "divided_not_multiplied", "expect": 4,
        "message": "To find distance, multiply: 12 %s 3 = 36 km. Dividing gives 4, which is smaller than one hour's travel." % MUL,
        "note": "12/3=4"}],
    "guided_steps": multiply_walk(
        "Distance = speed %s time. The speed is 12 km/h and the time is 3 hours." % MUL,
        12, 3, 36, "km", "Three hours at 12 km each hour.",
        "If it does not give back 12 km/h, something slipped."),
})

# b2: 400 m / 80 s = 5 m/s
bronze.append({
    "display": "A runner covers 400 m in 80 seconds. What is their speed in m/s?",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "Speed = distance divided by time.",
    "misconceptions": [{
        "pattern": "divided_wrong_way", "expect": 0.2,
        "message": "Divide distance by time, not time by distance: 400 %s 80 = 5 m/s. 80 %s 400 gives 0.2, the wrong way round." % (DIV, DIV),
        "note": "80/400=0.2"}],
    "guided_steps": divide_walk(
        "Speed = distance %s time. The distance is 400 m and the time is 80 s." % DIV,
        400, 80, 5, "m/s", "How many metres in one second?",
        "If it does not give back 400 m, something slipped."),
})

# b3: 60 g / 20 cm3 = 3
bronze.append({
    "display": "An object has mass 60 g and volume 20 cm³. Find the density.",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Density = mass divided by volume.",
    "misconceptions": [{
        "pattern": "multiplied_not_divided", "expect": 1200,
        "message": "Density = mass %s volume, so divide: 60 %s 20 = 3 g/cm³. Multiplying gives 1200, which is not a density." % (DIV, DIV),
        "note": "60*20=1200"}],
    "guided_steps": divide_walk(
        "Density = mass %s volume. The mass is 60 g and the volume is 20 cm³." % DIV,
        60, 20, 3, "g/cm³", "How much mass sits in each cm³?",
        "If it does not give back 60 g, something slipped."),
})

# b4: D=5, V=8 -> M=40
bronze.append({
    "display": "Density = 5 g/cm³, Volume = 8 cm³. Find the mass.",
    "solutions": [40], "calculator": False, "input_type": "single_value",
    "hint": "Mass = density multiplied by volume.",
    "misconceptions": [{
        "pattern": "divided_not_multiplied", "expect": 1.6,
        "message": "Mass = density %s volume, so multiply: 5 %s 8 = 40 g. Dividing gives 1.6, too light for 8 cm³." % (MUL, MUL),
        "note": "8/5=1.6"}],
    "guided_steps": multiply_walk(
        "Mass = density %s volume. The density is 5 g/cm³ and the volume is 8 cm³." % MUL,
        5, 8, 40, "g", "Eight lots of 5 g.",
        "If it does not give back 5 g/cm³, something slipped."),
})

# b5: 80 mph * 2.5 h = 200
bronze.append({
    "display": "A train travels at 80 mph for 2.5 hours. How far does it go?",
    "solutions": [200], "calculator": False, "input_type": "single_value",
    "hint": "Distance = speed multiplied by time.",
    "misconceptions": [{
        "pattern": "divided_not_multiplied", "expect": 32,
        "message": "Distance = speed %s time, so multiply: 80 %s 2.5 = 200 miles. Dividing gives 32, less than one hour's travel." % (MUL, MUL),
        "note": "80/2.5=32"}],
    "guided_steps": multiply_walk(
        "Distance = speed %s time. The speed is 80 mph and the time is 2.5 hours." % MUL,
        80, 2.5, 200, "miles", "Eighty miles for each of the 2.5 hours.",
        "If it does not give back 80 mph, something slipped."),
})

# b6: M=150, D=6 -> V=25
bronze.append({
    "display": "Mass = 150 g, Density = 6 g/cm³. Find the volume.",
    "solutions": [25], "calculator": False, "input_type": "single_value",
    "hint": "Volume = mass divided by density.",
    "misconceptions": [{
        "pattern": "multiplied_not_divided", "expect": 900,
        "message": "Volume = mass %s density, so divide: 150 %s 6 = 25 cm³. Multiplying gives 900, far too large." % (DIV, DIV),
        "note": "150*6=900"}],
    "guided_steps": divide_walk(
        "Volume = mass %s density. The mass is 150 g and the density is 6 g/cm³." % DIV,
        150, 6, 25, "cm³", "How many cm³ does 150 g fill at 6 g each?",
        "If it does not give back 150 g, something slipped."),
})

# b7 (REPAIRED from 90 miles/1.5h=60 duplicate -> 84 miles/1.5h=56)
bronze.append({
    "display": "A journey of 84 miles takes 1.5 hours. What is the speed?",
    "solutions": [56], "calculator": False, "input_type": "single_value",
    "hint": "Speed = distance divided by time.",
    "misconceptions": [{
        "pattern": "multiplied_not_divided", "expect": 126,
        "message": "Speed = distance %s time, so divide: 84 %s 1.5 = 56 mph. Multiplying gives 126, faster than any leg of the trip." % (DIV, DIV),
        "note": "84*1.5=126"}],
    "guided_steps": divide_walk(
        "Speed = distance %s time. The distance is 84 miles and the time is 1.5 hours." % DIV,
        84, 1.5, 56, "mph", "Double both to make it easy: 168 %s 3." % DIV,
        "If it does not give back 84 miles, something slipped."),
})

# =========================================================
# SILVER
# =========================================================
silver = []

# s0: F=200, A=4 -> P=50
silver.append({
    "display": "A force of 200 N acts on an area of 4 m². Find the pressure in N/m².",
    "solutions": [50], "calculator": False, "input_type": "single_value",
    "hint": "Pressure = force divided by area.",
    "misconceptions": [{
        "pattern": "multiplied_not_divided", "expect": 800,
        "message": "Pressure = force %s area, so divide: 200 %s 4 = 50 N/m². Multiplying gives 800." % (DIV, DIV),
        "note": "200*4=800"}],
    "guided_steps": divide_walk(
        "Pressure = force %s area. Cover P in the triangle to see the divide. Force is 200 N, area is 4 m²." % DIV,
        200, 4, 50, "N/m²", "Spread the 200 N over the 4 m².",
        "If it does not give back 200 N, something slipped."),
})

# s1: P=500, A=0.3 -> F=150 (multiply)
silver.append({
    "display": "Pressure = 500 Pa, Area = 0.3 m². Find the force.",
    "solutions": [150], "calculator": True, "input_type": "single_value",
    "hint": "Force = pressure multiplied by area.",
    "misconceptions": [{
        "pattern": "decimal_place_slip", "expect": 1500,
        "message": "The area is 0.3 m², not 3. Force = 500 %s 0.3 = 150 N. Using 3 gives 1500 N, ten times too big." % MUL,
        "note": "500*3=1500"}],
    "guided_steps": [
        {"say": "Force is the top of the pressure triangle: F = pressure %s area." % MUL},
        {"pre": "Read the area as a decimal: 0.3 m², so multiply 500 %s " % MUL, "post": "",
         "answer": 0.3, "hint": "It is 0.3, not 3."},
        {"phase": "substitute", "pre": "500 %s 0.3 = " % MUL, "post": " N", "answer": 150,
         "hint": "Half of 300 is 150."},
        {"phase": "substitute", "pre": "Check: 150 %s 0.3 = " % DIV, "post": "", "answer": 500,
         "done": "Back to 500 Pa, so 150 N is right.", "hint": "Dividing undoes the multiply."},
    ],
})

# s2: 30km@60 + 40km@80 -> total time 1 h (multi-step)
silver.append({
    "display": "A car travels 30 km at 60 km/h then 40 km at 80 km/h. Find the total time in hours. Give as a decimal.",
    "solutions": [1], "calculator": True, "input_type": "single_value",
    "hint": "Find each leg's time separately, then add them.",
    "misconceptions": [{
        "pattern": "totals_divided", "expect": 0.5,
        "message": "Add the two times, do not divide total distance by total speed. 30 %s 60 = 0.5 h and 40 %s 80 = 0.5 h, total 1 hour. (30+40) %s (60+80) gives 0.5, which is wrong." % (DIV, DIV, DIV),
        "note": "70/140=0.5"}],
    "guided_steps": [
        {"say": "Total time = time for leg 1 + time for leg 2. Each time = distance %s speed." % DIV},
        {"pre": "Leg 1 time = 30 %s 60 = " % DIV, "post": " h", "answer": 0.5,
         "hint": "Thirty km at 60 km/h is half an hour."},
        {"pre": "Leg 2 time = 40 %s 80 = " % DIV, "post": " h", "answer": 0.5,
         "hint": "Forty km at 80 km/h is half an hour."},
        {"phase": "substitute", "pre": "Total time = 0.5 + 0.5 = ", "post": " hours", "answer": 1,
         "hint": "Add the two half hours."},
        {"phase": "substitute", "pre": "Check leg 1 distance: 60 %s 0.5 = " % MUL, "post": "", "answer": 30,
         "done": "Back to 30 km, so the times are right.", "hint": "Speed times time gives the distance."},
    ],
})

# s3: 72 km/h -> m/s = 20 (div by 3.6)
silver.append({
    "display": "Convert 72 km/h to m/s.",
    "solutions": [20], "calculator": False, "input_type": "single_value",
    "hint": "To go from km/h to m/s, divide by 3.6.",
    "misconceptions": [{
        "pattern": "multiplied_by_36", "expect": 259.2,
        "message": "km/h to m/s divides by 3.6: 72 %s 3.6 = 20 m/s. Multiplying by 3.6 gives 259.2, which is faster than sound." % DIV,
        "note": "72*3.6=259.2"}],
    "guided_steps": [
        {"say": "km/h to m/s: divide by 3.6 (there are 3.6 km/h in each 1 m/s)."},
        {"pre": "Write the speed to convert: ", "post": " km/h", "answer": 72,
         "hint": "It is the number given in the question."},
        {"phase": "substitute", "pre": "72 %s 3.6 = " % DIV, "post": " m/s", "answer": 20,
         "hint": "72 %s 3.6 is 20." % DIV},
        {"phase": "substitute", "pre": "Check back: 20 %s 3.6 = " % MUL, "post": "", "answer": 72,
         "done": "Back to 72 km/h, so 20 m/s is right.", "hint": "Multiplying by 3.6 undoes the divide."},
    ],
})

# s4: D=7.5, M=225 -> V=30 (divide)
silver.append({
    "display": "An alloy has density 7.5 g/cm³ and mass 225 g. Find the volume.",
    "solutions": [30], "calculator": True, "input_type": "single_value",
    "hint": "Volume = mass divided by density.",
    "misconceptions": [{
        "pattern": "multiplied_not_divided", "expect": 1687.5,
        "message": "Volume = mass %s density, so divide: 225 %s 7.5 = 30 cm³. Multiplying gives 1687.5." % (DIV, DIV),
        "note": "225*7.5=1687.5"}],
    "guided_steps": divide_walk(
        "Volume = mass %s density. Cover V in the triangle. Mass is 225 g, density is 7.5 g/cm³." % DIV,
        225, 7.5, 30, "cm³", "How many cm³ at 7.5 g each make 225 g?",
        "If it does not give back 225 g, something slipped."),
})

# s5: F=800, P=400 -> A=2 (divide)
silver.append({
    "display": "Force = 800 N, Pressure = 400 Pa. Find the area.",
    "solutions": [2], "calculator": False, "input_type": "single_value",
    "hint": "Area = force divided by pressure.",
    "misconceptions": [{
        "pattern": "multiplied_not_divided", "expect": 320000,
        "message": "Area = force %s pressure, so divide: 800 %s 400 = 2 m². Multiplying gives 320000." % (DIV, DIV),
        "note": "800*400=320000"}],
    "guided_steps": divide_walk(
        "Area = force %s pressure. Cover A in the triangle. Force is 800 N, pressure is 400 Pa." % DIV,
        800, 400, 2, "m²", "How many m² at 400 Pa each carry 800 N?",
        "If it does not give back 800 N, something slipped."),
})

# s6: 45 min @ 80 km/h -> 60 km (convert then multiply)
silver.append({
    "display": "A journey takes 45 minutes at 80 km/h. How far in km?",
    "solutions": [60], "calculator": False, "input_type": "single_value",
    "hint": "Turn 45 minutes into hours first, then multiply by the speed.",
    "misconceptions": [{
        "pattern": "forgot_minutes_to_hours", "expect": 3600,
        "message": "45 minutes = 0.75 hours, not 45. Distance = 80 %s 0.75 = 60 km. Using 45 gives 3600 km." % MUL,
        "note": "80*45=3600"}],
    "guided_steps": [
        {"say": "Distance = speed %s time, but time must be in hours. 45 minutes = 45 %s 60 hours." % (MUL, DIV)},
        {"pre": "Time in hours = 45 %s 60 = " % DIV, "post": " h", "answer": 0.75,
         "hint": "45 out of 60 minutes is three quarters."},
        {"phase": "substitute", "pre": "Distance = 80 %s 0.75 = " % MUL, "post": " km", "answer": 60,
         "hint": "Three quarters of 80."},
        {"phase": "substitute", "pre": "Check: 60 %s 80 = " % DIV, "post": "", "answer": 0.75,
         "done": "Back to 0.75 hours, so 60 km is right.", "hint": "Distance %s speed gives the time." % DIV},
    ],
})

# =========================================================
# GOLD
# =========================================================
gold = []

# g0: average speed 60@40 + 60@60 -> 48
gold.append({
    "display": "A car travels 60 km at 40 km/h, then 60 km at 60 km/h. Find the average speed for the whole journey in km/h. Give to 1 d.p.",
    "solutions": [48], "calculator": True, "input_type": "single_value",
    "hint": "Average speed = total distance divided by total time. Find each time first.",
    "misconceptions": [{
        "pattern": "averaged_the_speeds", "expect": 50,
        "message": "The average of 40 and 60 is 50, but more time is spent at the slower speed. Use total distance %s total time = 120 %s 2.5 = 48 km/h." % (DIV, DIV),
        "note": "(40+60)/2=50"}],
    "guided_steps": [
        {"say": "Average speed = total distance %s total time. Find each leg's time first." % DIV},
        {"pre": "Leg 1 time = 60 %s 40 = " % DIV, "post": " h", "answer": 1.5,
         "hint": "Distance %s speed." % DIV},
        {"pre": "Leg 2 time = 60 %s 60 = " % DIV, "post": " h", "answer": 1,
         "hint": "Distance %s speed." % DIV},
        {"pre": "Total distance = 60 + 60 = ", "post": " km", "answer": 120,
         "hint": "Add the two distances."},
        {"phase": "substitute", "pre": "Total time = 1.5 + 1 = ", "post": " h", "answer": 2.5,
         "hint": "Add the two times."},
        {"phase": "substitute", "pre": "Average speed = 120 %s 2.5 = " % DIV, "post": " km/h", "answer": 48,
         "hint": "Total distance %s total time." % DIV},
        {"phase": "substitute", "pre": "Check: 48 %s 2.5 = " % MUL, "post": "", "answer": 120,
         "done": "Back to the total distance, so 48 km/h is right.", "hint": "Average speed times total time gives total distance."},
    ],
})

# g1: cube side 4, mass 384 -> D=6  (SVG)
gold.append({
    "display": CUBE_SVG + "A cube has side 4 cm and mass 384 g. Find the density." + CAP,
    "solutions": [6], "calculator": False, "input_type": "single_value",
    "hint": "Find the volume of the cube first, then divide the mass by it.",
    "misconceptions": [{
        "pattern": "used_area_not_volume", "expect": 24,
        "message": "The volume of a cube is side³ = 4³ = 64, not 4² = 16. Density = 384 %s 64 = 6 g/cm³. Using 16 gives 24." % DIV,
        "note": "384/16=24"}],
    "guided_steps": [
        {"say": "Density = mass %s volume. First the volume of the cube: side %s side %s side." % (DIV, MUL, MUL)},
        {"pre": "Volume = 4 %s 4 %s 4 = " % (MUL, MUL), "post": " cm³", "answer": 64,
         "hint": "Cube the side: 4³."},
        {"phase": "substitute", "pre": "Density = 384 %s 64 = " % DIV, "post": " g/cm³", "answer": 6,
         "hint": "Mass %s volume." % DIV},
        {"phase": "substitute", "pre": "Check: 6 %s 64 = " % MUL, "post": "", "answer": 384,
         "done": "Back to the mass, so 6 g/cm³ is right.", "hint": "Density times volume gives the mass."},
    ],
})

# g2: cylinder r3 h10 mass848 -> ~3.0 (SVG, calc)
gold.append({
    "display": CYL_SVG + "A cylinder has radius 3 cm and height 10 cm and mass 848 g. Find the density to 1 d.p." + CAP,
    "solutions": [3], "calculator": True, "input_type": "single_value",
    "hint": "Volume of a cylinder is pi times radius squared times height.",
    "misconceptions": [{
        "pattern": "forgot_to_square_radius", "expect": 9,
        "message": "Volume = πr²h and r² = 9, so V ≈ 282.7 cm³ and density ≈ 848 %s 282.7 ≈ 3.0. Using r instead of r² gives about 9." % DIV,
        "note": "848/(pi*3*10)=8.997~9"}],
    "guided_steps": [
        {"say": "Density = mass %s volume. Volume of a cylinder = π %s r² %s h. Use π ≈ 3.142." % (DIV, MUL, MUL)},
        {"pre": "Square the radius: 3 %s 3 = " % MUL, "post": "", "answer": 9,
         "hint": "r² comes before multiplying by π."},
        {"pre": "Volume = π %s 9 %s 10 = (to 1 d.p.) " % (MUL, MUL), "post": " cm³", "answer": 282.7,
         "hint": "3.142 %s 90." % MUL},
        {"phase": "substitute", "pre": "Density = 848 %s 282.7 = (to 1 d.p.) " % DIV, "post": " g/cm³", "answer": 3,
         "hint": "Mass %s volume, rounded to 1 d.p." % DIV},
        {"phase": "substitute", "pre": "Check: 848 %s 3 = (to 1 d.p.) " % DIV, "post": "", "answer": 282.7,
         "done": "Back to the volume, so 3.0 g/cm³ is right.", "hint": "Mass %s density returns the volume." % DIV},
    ],
})

# g3: woman 55kg on 0.0002 m2, g=10 -> 2 750 000 Pa (SVG none)
gold.append({
    "display": "A woman of mass 55 kg stands on one heel of area 2 cm² = 0.0002 m². Find the pressure in Pa. (Use g = 10.)",
    "solutions": [2750000], "calculator": True, "input_type": "single_value",
    "hint": "Turn her mass into a force (weight = mass times g) before dividing by the area.",
    "misconceptions": [{
        "pattern": "used_mass_as_force", "expect": 275000,
        "message": "The force is her weight = mass %s g = 55 %s 10 = 550 N, not 55. Pressure = 550 %s 0.0002 = 2 750 000 Pa. Using 55 gives 275 000." % (MUL, MUL, DIV),
        "note": "55/0.0002=275000"}],
    "guided_steps": [
        {"say": "Pressure = force %s area. The force is her weight = mass %s g." % (DIV, MUL)},
        {"pre": "Weight = 55 %s 10 = " % MUL, "post": " N", "answer": 550,
         "hint": "Mass times gravity."},
        {"phase": "substitute", "pre": "Pressure = 550 %s 0.0002 = " % DIV, "post": " Pa", "answer": 2750000,
         "hint": "Dividing by 0.0002 is the same as multiplying by 5000."},
        {"phase": "substitute", "pre": "Check: 2750000 %s 0.0002 = " % MUL, "post": "", "answer": 550,
         "done": "Back to the 550 N force, so 2 750 000 Pa is right.", "hint": "Pressure times area returns the force."},
    ],
})

# g4: 15 m/s -> km/h = 54 (mul by 3.6)
gold.append({
    "display": "Convert 15 m/s to km/h.",
    "solutions": [54], "calculator": False, "input_type": "single_value",
    "hint": "To go from m/s to km/h, multiply by 3.6.",
    "misconceptions": [{
        "pattern": "divided_not_multiplied", "expect": 4.17,
        "message": "m/s to km/h multiplies by 3.6: 15 %s 3.6 = 54 km/h. Dividing by 3.6 gives about 4.17, which is slower, the wrong way round." % MUL,
        "note": "15/3.6=4.166..~4.17"}],
    "guided_steps": [
        {"say": "m/s to km/h: multiply by 3.6 (each 1 m/s is 3.6 km/h)."},
        {"pre": "Write the speed to convert: ", "post": " m/s", "answer": 15,
         "hint": "It is the number given in the question."},
        {"phase": "substitute", "pre": "15 %s 3.6 = " % MUL, "post": " km/h", "answer": 54,
         "hint": "15 %s 3.6 is 54." % MUL},
        {"phase": "substitute", "pre": "Check back: 54 %s 3.6 = " % DIV, "post": "", "answer": 15,
         "done": "Back to 15 m/s, so 54 km/h is right.", "hint": "Dividing by 3.6 undoes the multiply."},
    ],
})

# =========================================================
# tier_guides
# =========================================================
tier_guides = {
    "bronze": {
        "title": "Bronze: one formula, one step",
        "steps": [
            "Pick the formula: speed = distance %s time, density = mass %s volume, pressure = force %s area." % (DIV, DIV, DIV),
            "Put the two numbers you are given into it.",
            "Divide for the bottom of the triangle, multiply for the top, then write the units.",
        ],
        "example": {
            "question": "A car travels 240 km in 4 hours. Find the speed.",
            "steps": [
                {"label": "Formula", "content": "Speed = distance %s time" % DIV},
                {"label": "Substitute", "content": "Speed = 240 %s 4" % DIV},
                {"label": "Check", "content": "60 %s 4 = 240" % MUL},
                {"label": "Answer", "content": "60 km/h", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: rearrange or convert first",
        "steps": [
            "Cover the quantity you want in the triangle to see whether to multiply or divide.",
            "Convert units first if they do not match: km/h to m/s divide by 3.6, minutes to hours divide by 60.",
            "Then apply the formula in one step and add the units.",
        ],
        "example": {
            "question": "Convert 72 km/h to m/s.",
            "steps": [
                {"label": "Rule", "content": "km/h to m/s: divide by 3.6"},
                {"label": "Substitute", "content": "72 %s 3.6" % DIV},
                {"label": "Check", "content": "20 %s 3.6 = 72" % MUL},
                {"label": "Answer", "content": "20 m/s", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: two steps before the measure",
        "steps": [
            "Find the hidden quantity first: a volume from the solid, a total distance and total time, or a force from weight = mass %s g." % MUL,
            "For average speed use total distance %s total time, never the average of the two speeds." % DIV,
            "Then apply the compound-measure formula and keep the units.",
        ],
        "example": {
            "question": "A cube of side 4 cm has mass 384 g. Find the density.",
            "steps": [
                {"label": "Volume", "content": "4³ = 64 cm³"},
                {"label": "Substitute", "content": "Density = 384 %s 64" % DIV},
                {"label": "Check", "content": "6 %s 64 = 384" % MUL},
                {"label": "Answer", "content": "6 g/cm³", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# =========================================================
# guided.opener + guided.teach
# =========================================================
opener = {
    "label": "Before any formula",
    "display": SPEED_TRI + "A car drives <strong>120 miles</strong> in <strong>2 hours</strong>, going the same speed the whole way.",
    "steps": [
        {"say": "No formula needed, just common sense. Same speed each hour.",
         "pre": "Miles it covers in 1 hour = ", "post": "",
         "answer": 60, "hint": "Split 120 miles fairly across the 2 hours."},
        {"say": "That number per hour IS the speed. You just did speed = distance %s time." % DIV,
         "pre": "So in 3 hours it would go 60 %s 3 = " % MUL, "post": "",
         "answer": 180, "hint": "Three lots of 60 miles."},
        {"say": "Those two moves are the whole lesson. Every quantity lives in a triangle: <strong>speed</strong> (distance, speed, time), <strong>density</strong> (mass, density, volume) and <strong>pressure</strong> (force, pressure, area). Cover the one you want: it tells you to multiply or divide."},
    ],
}

teach = {
    "bronze": {
        "label": "One formula, one step",
        "display": SPEED_TRI + "A motorbike travels 240 km in 4 hours. Find the speed, then how far it goes in 7 hours at that speed.",
        "steps": [
            {"say": "Speed = distance %s time." % DIV,
             "pre": "Speed = 240 %s 4 = " % DIV, "post": " km/h", "answer": 60,
             "hint": "Share 240 km over 4 hours."},
            {"say": "Now distance = speed %s time, the top of the triangle." % MUL,
             "pre": "In 2 hours: 60 %s 2 = " % MUL, "post": " km", "answer": 120,
             "hint": "Two lots of 60 km."},
            {"pre": "In 7 hours: 60 %s 7 = " % MUL, "post": " km", "answer": 420,
             "hint": "Seven lots of 60 km."},
            {"pre": "Check: 420 %s 7 = " % DIV, "post": " km/h", "answer": 60,
             "done": "Back to the 60 km/h speed. It fits.", "hint": "Distance %s time returns the speed." % DIV},
        ],
    },
    "silver": {
        "label": "Rearrange the triangle",
        "display": PRESS_TRI + "A press pushes with 250 Pa on an area of 0.4 m². Find the force. Then find the area that 500 N would cover at the same pressure.",
        "steps": [
            {"say": "Force is the top: F = pressure %s area." % MUL,
             "pre": "F = 250 %s 0.4 = " % MUL, "post": " N", "answer": 100,
             "hint": "250 %s 0.4." % MUL},
            {"pre": "Check: 100 %s 0.4 = " % DIV, "post": " Pa", "answer": 250,
             "hint": "Force %s area returns the pressure." % DIV},
            {"say": "For area, cover A: A = force %s pressure." % DIV,
             "pre": "A = 500 %s 250 = " % DIV, "post": " m²", "answer": 2,
             "hint": "500 %s 250." % DIV},
            {"pre": "Check: 250 %s 2 = " % MUL, "post": " N", "answer": 500,
             "done": "Back to the 500 N force. It fits.", "hint": "Pressure %s area returns the force." % MUL},
        ],
    },
    "gold": {
        "label": "Two steps before the measure",
        "display": "A van drives 120 km at 40 km/h, then 120 km at 60 km/h. Find the average speed for the whole trip.",
        "steps": [
            {"say": "Average speed = total distance %s total time. Find each time first." % DIV,
             "pre": "Time 1 = 120 %s 40 = " % DIV, "post": " h", "answer": 3,
             "hint": "Distance %s speed." % DIV},
            {"pre": "Time 2 = 120 %s 60 = " % DIV, "post": " h", "answer": 2,
             "hint": "Distance %s speed." % DIV},
            {"pre": "Total distance = 120 + 120 = ", "post": " km", "answer": 240,
             "hint": "Add the two legs."},
            {"pre": "Total time = 3 + 2 = ", "post": " h", "answer": 5,
             "hint": "Add the two times."},
            {"pre": "Average speed = 240 %s 5 = " % DIV, "post": " km/h", "answer": 48,
             "done": "Not 50. The slow leg takes longer, so the average is pulled down.",
             "hint": "Total distance %s total time." % DIV},
        ],
    },
}

# =========================================================
# method_card (trim steps to <=4; preserve title/content/example)
# =========================================================
mc = dict(live["method_card"])
mc["steps"] = [
    "Choose the triangle: speed (D, S, T), density (M, D, V) or pressure (F, P, A).",
    "Cover the quantity you want: it shows you whether to multiply or divide.",
    "Match the units first (convert if needed), then calculate and add the units.",
]

# =========================================================
# assemble
# =========================================================
pd = {
    "method_card": mc,
    "topic_links": live["topic_links"],
    "problem_bank": {
        "bronze": bronze,
        "bronze_description": "One formula used once: divide (or multiply) the two numbers given and write the units.",
        "silver": silver,
        "silver_description": "Rearrange the triangle or convert a unit first, then apply the formula in one step.",
        "gold": gold,
        "gold_description": "Two steps: find a hidden volume, total, or force before the compound measure.",
    },
    "tier_guides": tier_guides,
    "guided": {"opener": opener, "teach": teach},
    "related_videos": live["related_videos"],
    "worked_examples": live["worked_examples"],
}

# ---- self-verification of every box value ----
def verify_walk(steps, name):
    boxes = [s for s in steps if s.get("answer") is not None]
    assert len(boxes) >= 3 or name.startswith("opener") or name.startswith("teach"), (name, len(boxes))
    for s in boxes:
        assert isinstance(s["answer"], (int, float)), (name, s)

for t, arr in (("bronze", bronze), ("silver", silver), ("gold", gold)):
    seen = {}
    for i, p in enumerate(arr):
        sol = tuple(p["solutions"])
        assert sol not in seen, ("DUP", t, i, seen.get(sol), sol)
        seen[sol] = i
        for m in p.get("misconceptions", []):
            assert m["expect"] != p["solutions"][0], ("expect==sol", t, i)
        verify_walk(p["guided_steps"], "%s[%d]" % (t, i))
        # final live box must equal solution
        live_boxes = [s for s in p["guided_steps"] if s.get("answer") is not None]
        # the "solve" box (first phase substitute box) should hit the solution
        sub_boxes = [s for s in p["guided_steps"] if s.get("phase") == "substitute" and s.get("answer") is not None]
        assert any(abs(float(b["answer"]) - float(p["solutions"][0])) < 0.011 for b in sub_boxes), ("no solve box hits sol", t, i, p["solutions"])

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("WROTE", OUT)
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
print("all self-checks passed")
