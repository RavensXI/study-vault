# -*- coding: utf-8 -*-
import json, io

OUT = "lesson_maths-aqa_ratio-proportion-L03.json"

# ---- SVG figures (theme-safe: currentColor text/strokes, soft opacity fills) ----
SVG_JOURNEY = ('<svg viewBox="0 0 240 92" role="img" aria-label="A journey from A to B of 120 miles taking 2 hours">'
 '<line x1="30" y1="58" x2="210" y2="58" stroke="currentColor" stroke-width="2"/>'
 '<circle cx="30" cy="58" r="4" fill="currentColor"/>'
 '<circle cx="210" cy="58" r="4" fill="currentColor"/>'
 '<text x="22" y="76" font-family="Inter, sans-serif" font-size="11" fill="currentColor">A</text>'
 '<text x="204" y="76" font-family="Inter, sans-serif" font-size="11" fill="currentColor">B</text>'
 '<rect x="105" y="44" width="30" height="14" rx="3" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
 '<text x="120" y="30" text-anchor="middle" font-family="Inter, sans-serif" font-size="12" fill="currentColor">120 miles</text>'
 '<text x="120" y="90" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="currentColor">2 hours</text>'
 '</svg>')

SVG_CUBE = ('<svg viewBox="0 0 160 130" role="img" aria-label="A cube of side 5 cm and mass 750 g">'
 '<rect x="30" y="42" width="70" height="70" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>'
 '<path d="M30 42 L55 22 L125 22 L100 42 Z" fill="#60a5fa" fill-opacity="0.2" stroke="currentColor" stroke-width="2"/>'
 '<path d="M100 42 L125 22 L125 92 L100 112 Z" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="2"/>'
 '<text x="65" y="126" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="currentColor">5 cm</text>'
 '<text x="130" y="62" font-family="Inter, sans-serif" font-size="11" fill="currentColor">5 cm</text>'
 '<text x="8" y="80" font-family="Inter, sans-serif" font-size="11" fill="currentColor">5 cm</text>'
 '</svg>')

SVG_CYL = ('<svg viewBox="0 0 150 150" role="img" aria-label="A cylinder of radius 3 cm, height 7 cm and mass 594 g">'
 '<ellipse cx="70" cy="30" rx="40" ry="13" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>'
 '<line x1="30" y1="30" x2="30" y2="115" stroke="currentColor" stroke-width="2"/>'
 '<line x1="110" y1="30" x2="110" y2="115" stroke="currentColor" stroke-width="2"/>'
 '<path d="M30 115 A40 13 0 0 0 110 115" fill="none" stroke="currentColor" stroke-width="2"/>'
 '<line x1="70" y1="30" x2="110" y2="30" stroke="currentColor" stroke-width="1.5"/>'
 '<text x="88" y="26" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" fill="currentColor">3 cm</text>'
 '<text x="118" y="78" font-family="Inter, sans-serif" font-size="11" fill="currentColor">7 cm</text>'
 '</svg>')

SVG_CUBOID = ('<svg viewBox="0 0 170 130" role="img" aria-label="A cuboid measuring 5 cm by 4 cm by 2 cm with mass 200 g">'
 '<rect x="30" y="50" width="90" height="55" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>'
 '<path d="M30 50 L55 30 L145 30 L120 50 Z" fill="#60a5fa" fill-opacity="0.2" stroke="currentColor" stroke-width="2"/>'
 '<path d="M120 50 L145 30 L145 85 L120 105 Z" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="2"/>'
 '<text x="75" y="121" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="currentColor">5 cm</text>'
 '<text x="150" y="72" font-family="Inter, sans-serif" font-size="11" fill="currentColor">4 cm</text>'
 '<text x="92" y="46" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" fill="currentColor">2 cm</text>'
 '</svg>')

CAP = '<span class="figure-caption">Not drawn accurately</span>'

def box(pre, answer, hint, post="", **kw):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    d.update(kw)
    return d

def say(s):
    return {"say": s}

# ---------------- BRONZE ----------------
bronze = [
 {  # B0 240/4=60
  "display": "A car travels 240 km in 4 hours. What is the speed?",
  "solutions": [60], "calculator": False, "input_type": "single_value",
  "hint": "Speed is distance divided by time: 240 ÷ 4.",
  "misconceptions": [{"pattern": "multiplied", "expect": 960,
    "message": "Speed is Distance ÷ Time, not Distance × Time. 240 ÷ 4 = 60 km/h."}],
  "guided_steps": [
    say("Speed = Distance ÷ Time. The distance is 240 km, the time is 4 hours."),
    box("240 ÷ 4 = ", 60, "Share 240 km across 4 hours."),
    box("Check by rebuilding the distance: 60 × 4 = ", 240, "Speed × time should give the distance back.", phase="substitute"),
    box("So in 5 hours it goes 60 × 5 = ", 300, "Multiply the speed by 5.", done="60 km/h works forwards and backwards, so the speed is right."),
  ]},
 {  # B1 80*3=240
  "display": "A train travels at 80 km/h for 3 hours. How far does it go?",
  "solutions": [240], "calculator": False, "input_type": "single_value",
  "hint": "Distance is speed times time: 80 × 3.",
  "misconceptions": [],
  "guided_steps": [
    say("Distance = Speed × Time. Speed 80 km/h, time 3 hours."),
    box("80 × 3 = ", 240, "Multiply the speed by the time."),
    box("Check by dividing back: 240 ÷ 3 = ", 80, "Distance ÷ time returns the speed.", phase="substitute"),
    box("In 5 hours it would go 80 × 5 = ", 400, "Multiply the speed by 5.", done="Divides back to 80 km/h, so 240 km is right."),
  ]},
 {  # B2 30/15=2
  "display": "A cyclist covers 30 km at 15 km/h. How long does it take?",
  "solutions": [2], "calculator": False, "input_type": "single_value",
  "hint": "Time is distance divided by speed: 30 ÷ 15.",
  "misconceptions": [{"pattern": "reversed", "expect": 0.5,
    "message": "Time is Distance ÷ Speed: 30 ÷ 15 = 2 hours, not 15 ÷ 30."}],
  "guided_steps": [
    say("Time = Distance ÷ Speed. Distance 30 km, speed 15 km/h."),
    box("30 ÷ 15 = ", 2, "How many 15s fit into 30?"),
    box("Check: 15 × 2 = ", 30, "Speed × time rebuilds the distance.", phase="substitute"),
    box("At 15 km/h, 45 km would take 45 ÷ 15 = ", 3, "Divide 45 by 15.", done="Rebuilds 30 km, so 2 hours is right."),
  ]},
 {  # B3 200/25=8
  "display": "A block has mass 200 g and volume 25 cm³. Find the density.",
  "solutions": [8], "calculator": False, "input_type": "single_value",
  "hint": "Density is mass divided by volume: 200 ÷ 25.",
  "misconceptions": [{"pattern": "reversed", "expect": 0.125,
    "message": "Density is Mass ÷ Volume: 200 ÷ 25 = 8 g/cm³, not Volume ÷ Mass."}],
  "guided_steps": [
    say("Density = Mass ÷ Volume. Mass 200 g, volume 25 cm³."),
    box("200 ÷ 25 = ", 8, "Mass shared across the volume."),
    box("Check: 8 × 25 = ", 200, "Density × volume rebuilds the mass.", phase="substitute"),
    box("A 50 cm³ piece of the same metal has mass 8 × 50 = ", 400, "Density × new volume.", done="Rebuilds 200 g, so 8 g/cm³ is right."),
  ]},
 {  # B4 CHANGED 1.4*50=70
  "display": "A liquid has density 1.4 g/cm³ and volume 50 cm³. Find the mass.",
  "solutions": [70], "calculator": False, "input_type": "single_value",
  "hint": "Mass is density times volume: 1.4 × 50.",
  "misconceptions": [],
  "guided_steps": [
    say("Mass = Density × Volume. Density 1.4 g/cm³, volume 50 cm³."),
    box("1.4 × 50 = ", 70, "Multiply density by volume."),
    box("Check: 70 ÷ 50 = ", 1.4, "Mass ÷ volume returns the density.", phase="substitute"),
    box("A 100 cm³ amount would have mass 1.4 × 100 = ", 140, "Density × new volume.", done="Divides back to 1.4 g/cm³, so 70 g is right."),
  ]},
 {  # B5 120/4=30
  "display": "A force of 120 N acts on an area of 4 m². Find the pressure.",
  "solutions": [30], "calculator": False, "input_type": "single_value",
  "hint": "Pressure is force divided by area: 120 ÷ 4.",
  "misconceptions": [{"pattern": "multiplied", "expect": 480,
    "message": "Pressure is Force ÷ Area, not Force × Area. 120 ÷ 4 = 30 N/m²."}],
  "guided_steps": [
    say("Pressure = Force ÷ Area. Force 120 N, area 4 m²."),
    box("120 ÷ 4 = ", 30, "Force shared over the area."),
    box("Check: 30 × 4 = ", 120, "Pressure × area rebuilds the force.", phase="substitute"),
    box("The same force on 6 m² gives 120 ÷ 6 = ", 20, "Force ÷ larger area.", done="Rebuilds 120 N, so 30 N/m² is right."),
  ]},
 {  # B6 600/3=200
  "display": "An object has mass 600 g and density 3 g/cm³. Find the volume.",
  "solutions": [200], "calculator": False, "input_type": "single_value",
  "hint": "Volume is mass divided by density: 600 ÷ 3.",
  "misconceptions": [{"pattern": "multiplied", "expect": 1800,
    "message": "Volume is Mass ÷ Density: 600 ÷ 3 = 200 cm³, not Mass × Density."}],
  "guided_steps": [
    say("Volume = Mass ÷ Density. Mass 600 g, density 3 g/cm³."),
    box("600 ÷ 3 = ", 200, "Mass shared by the density."),
    box("Check: 3 × 200 = ", 600, "Density × volume rebuilds the mass.", phase="substitute"),
    box("900 g of it would fill 900 ÷ 3 = ", 300, "New mass ÷ density.", done="Rebuilds 600 g, so 200 cm³ is right."),
  ]},
 {  # B7 50*6=300
  "display": "A pressure of 50 N/m² acts on an area of 6 m². Find the force.",
  "solutions": [300], "calculator": False, "input_type": "single_value",
  "hint": "Force is pressure times area: 50 × 6.",
  "misconceptions": [],
  "guided_steps": [
    say("Force = Pressure × Area. Pressure 50 N/m², area 6 m²."),
    box("50 × 6 = ", 300, "Multiply pressure by area."),
    box("Check: 300 ÷ 6 = ", 50, "Force ÷ area returns the pressure.", phase="substitute"),
    box("The same pressure on 10 m² gives 50 × 10 = ", 500, "Pressure × new area.", done="Divides back to 50 N/m², so 300 N is right."),
  ]},
]

# ---------------- SILVER ----------------
silver = [
 {  # S0 90/1.5=60
  "display": "A car travels 90 km in 1 hour 30 minutes. Find the speed in km/h.",
  "solutions": [60], "calculator": False, "input_type": "single_value",
  "hint": "Change 1 hour 30 minutes to 1.5 hours, then divide 90 by it.",
  "misconceptions": [{"pattern": "dropped_minutes", "expect": 90,
    "message": "1 hour 30 minutes is 1.5 hours, not 1 hour. 90 ÷ 1.5 = 60 km/h."}],
  "guided_steps": [
    say("Speed = Distance ÷ Time, but the time must be in hours first."),
    box("Change the time: 1 h 30 min = ", 1.5, "30 minutes is 30 ÷ 60 = 0.5 hours."),
    box("Now divide: 90 ÷ 1.5 = ", 60, "Distance ÷ time in hours.", phase="substitute"),
    box("Check: 60 × 1.5 = ", 90, "Speed × time rebuilds the distance.", done="Rebuilds 90 km, so 60 km/h is right."),
  ]},
 {  # S1 400/50=8
  "display": "A runner covers 400 m in 50 seconds. Find the speed in m/s.",
  "solutions": [8], "calculator": False, "input_type": "single_value",
  "hint": "Speed is distance divided by time: 400 ÷ 50.",
  "misconceptions": [{"pattern": "reversed", "expect": 0.125,
    "message": "Speed is Distance ÷ Time: 400 ÷ 50 = 8 m/s, not Time ÷ Distance."}],
  "guided_steps": [
    say("Speed = Distance ÷ Time. Metres and seconds give m/s directly."),
    box("400 ÷ 50 = ", 8, "Metres shared across the seconds."),
    box("Check: 8 × 50 = ", 400, "Speed × time rebuilds the distance.", phase="substitute"),
    box("In 75 seconds it covers 8 × 75 = ", 600, "Speed × new time.", done="Rebuilds 400 m, so 8 m/s is right."),
  ]},
 {  # S2 cube side5 mass750 -> 6 (SVG)
  "display": SVG_CUBE + CAP + "<br>A metal cube has sides 5 cm and mass 750 g. Find the density.",
  "solutions": [6], "calculator": True, "input_type": "single_value",
  "hint": "Cube the side for the volume, then divide the mass by it.",
  "misconceptions": [
    {"pattern": "side_not_cubed", "expect": 150,
     "message": "The volume is 5³ = 125 cm³, not 5. Density = 750 ÷ 125 = 6 g/cm³."},
    {"pattern": "used_area", "expect": 30,
     "message": "5² = 25 is an area, not a volume. The cube's volume is 5³ = 125, so 750 ÷ 125 = 6 g/cm³."}],
  "guided_steps": [
    say("Density = Mass ÷ Volume. First find the cube's volume."),
    box("Volume = 5³ = 5 × 5 × 5 = ", 125, "Cube the side length."),
    box("Density: 750 ÷ 125 = ", 6, "Mass ÷ volume.", phase="substitute"),
    box("Check: 6 × 125 = ", 750, "Density × volume rebuilds the mass.", done="Rebuilds 750 g, so 6 g/cm³ is right."),
  ]},
 {  # S3 72/3.6=20
  "display": "Convert 72 km/h to m/s.",
  "solutions": [20], "calculator": False, "input_type": "single_value",
  "hint": "To go from km/h to m/s, divide by 3.6.",
  "misconceptions": [{"pattern": "multiplied_by_3point6", "expect": 259.2,
    "message": "To change km/h to m/s, divide by 3.6, not multiply. 72 ÷ 3.6 = 20 m/s."}],
  "guided_steps": [
    say("To change km/h to m/s, divide by 3.6 (that is 1000 m ÷ 3600 s)."),
    box("72 ÷ 3.6 = ", 20, "Divide the km/h value by 3.6."),
    box("Check by going back: 20 × 3.6 = ", 72, "m/s to km/h is × 3.6.", phase="substitute"),
    box("At 20 m/s, one minute covers 20 × 60 = ", 1200, "Metres per second × 60.", done="Returns to 72 km/h, so 20 m/s is right."),
  ]},
 {  # S4 600/0.02=30000
  "display": "A woman weighing 600 N stands on one foot with area 0.02 m². Find the pressure.",
  "solutions": [30000], "calculator": True, "input_type": "single_value",
  "hint": "Pressure is force divided by area: 600 ÷ 0.02.",
  "misconceptions": [
    {"pattern": "multiplied", "expect": 12,
     "message": "Pressure is Force ÷ Area: 600 ÷ 0.02 = 30000 Pa, not Force × Area."},
    {"pattern": "divided_by_2", "expect": 300,
     "message": "Divide by 0.02, not 2. 600 ÷ 0.02 = 30000 Pa."}],
  "guided_steps": [
    say("Pressure = Force ÷ Area. Force 600 N, area 0.02 m²."),
    box("600 ÷ 0.02 = ", 30000, "Dividing by 0.02 is the same as × 50."),
    box("Check: 30000 × 0.02 = ", 600, "Pressure × area rebuilds the force.", phase="substitute"),
    box("On double the area, 0.04 m², the pressure is 600 ÷ 0.04 = ", 15000, "Force ÷ larger area.", done="Rebuilds 600 N, so 30000 Pa is right."),
  ]},
 {  # S5 50*2.4=120
  "display": "A car travels at 50 mph for 2 hours 24 minutes. How far does it go?",
  "solutions": [120], "calculator": True, "input_type": "single_value",
  "hint": "Change 2 hours 24 minutes to 2.4 hours, then multiply by 50.",
  "misconceptions": [
    {"pattern": "decimal_minutes", "expect": 112,
     "message": "2 hours 24 minutes is 2.4 hours (24 ÷ 60 = 0.4), not 2.24. 50 × 2.4 = 120 miles."},
    {"pattern": "dropped_minutes", "expect": 100,
     "message": "Do not drop the 24 minutes: 2 h 24 min = 2.4 h, so 50 × 2.4 = 120 miles."}],
  "guided_steps": [
    say("Distance = Speed × Time. Put the time into hours first."),
    box("Change the time: 2 h 24 min = ", 2.4, "24 minutes is 24 ÷ 60 = 0.4 hours."),
    box("Distance: 50 × 2.4 = ", 120, "Speed × time in hours.", phase="substitute"),
    box("Check: 120 ÷ 2.4 = ", 50, "Distance ÷ time returns the speed.", done="Divides back to 50 mph, so 120 miles is right."),
  ]},
 {  # S6 alloy total volume 80
  "display": "An alloy is made by mixing 300 g of metal A (density 10 g/cm³) with 400 g of metal B (density 8 g/cm³). Find the total volume.",
  "solutions": [80], "calculator": True, "input_type": "single_value",
  "hint": "Find each metal's volume with mass ÷ density, then add them.",
  "misconceptions": [{"pattern": "add_densities", "expect": None,
    "message": "Find each volume separately (Mass ÷ Density), then add: 30 + 50 = 80 cm³. You cannot add the densities."}],
  "guided_steps": [
    say("Find each metal's volume with Volume = Mass ÷ Density, then add."),
    box("Volume of A: 300 ÷ 10 = ", 30, "Mass of A ÷ density of A."),
    box("Volume of B: 400 ÷ 8 = ", 50, "Mass of B ÷ density of B."),
    box("Total volume: 30 + 50 = ", 80, "Add the two volumes.", phase="substitute"),
    box("Check B's mass: 50 × 8 = ", 400, "Volume × density gives the mass back.", done="A gives 300 g, B gives 400 g, back to the start. 80 cm³ is right."),
  ]},
]

# ---------------- GOLD ----------------
gold = [
 {  # G0 CHANGED avg speed 60
  "display": "A train travels 180 km at 90 km/h, then 120 km at 40 km/h. Find the average speed for the whole journey.",
  "solutions": [60], "calculator": True, "input_type": "single_value",
  "hint": "Find the time for each leg, add the distances and times, then divide.",
  "misconceptions": [{"pattern": "averaged_speeds", "expect": 65,
    "message": "Do not average the two speeds. Each leg takes a different time. Total distance ÷ total time = 300 ÷ 5 = 60 km/h."}],
  "guided_steps": [
    say("Average speed = total distance ÷ total time. Find each leg's time."),
    box("Leg 1 time: 180 ÷ 90 = ", 2, "Distance ÷ speed for leg 1."),
    box("Leg 2 time: 120 ÷ 40 = ", 3, "Distance ÷ speed for leg 2."),
    box("Total distance ÷ total time: 300 ÷ 5 = ", 60, "Add the distances (300 km) and times (5 h), then divide.", phase="substitute"),
    box("Check: 60 × 5 = ", 300, "Average speed × total time rebuilds the distance.", done="Rebuilds 300 km over 5 h. Averaging 90 and 40 would wrongly give 65."),
  ]},
 {  # G1 cylinder density 3.0 (SVG)
  "display": SVG_CYL + CAP + "<br>A cylinder has radius 3 cm, height 7 cm, and mass 594 g. Find the density to 1 d.p.",
  "solutions": [3], "calculator": True, "input_type": "single_value",
  "hint": "Volume of a cylinder is πr²h; square the radius first.",
  "misconceptions": [{"pattern": "radius_not_squared", "expect": 9,
    "message": "Volume of a cylinder is πr²h, so square the radius: π × 3² × 7 ≈ 197.9. Density = 594 ÷ 197.9 ≈ 3.0 g/cm³."}],
  "guided_steps": [
    say("Density = Mass ÷ Volume. Volume of a cylinder is πr²h."),
    box("Square the radius: 3² = ", 9, "3 × 3."),
    box("Volume = π × 9 × 7 = 63π = ", 197.92, "63 × π, to 2 d.p."),
    box("Density: 594 ÷ 197.92 = ", 3, "Mass ÷ volume, then round to 1 d.p.", phase="substitute"),
    box("Check: 3 × 197.92 ≈ ", 594, "Density × volume gives back roughly the mass.", done="≈ 594 g, so 3.0 g/cm³ is right."),
  ]},
 {  # G2 car 12:15->13:00 60km -> 80
  "display": "A car passes point A at 12:15 and point B (60 km away) at 13:00. Find the average speed.",
  "solutions": [80], "calculator": False, "input_type": "single_value",
  "hint": "The time is 45 minutes, which is 0.75 hours.",
  "misconceptions": [{"pattern": "minutes_not_converted", "expect": None,
    "message": "The time is 45 minutes = 0.75 hours (45 ÷ 60). Speed = 60 ÷ 0.75 = 80 km/h."}],
  "guided_steps": [
    say("Speed = Distance ÷ Time. Work out the time as a fraction of an hour."),
    box("From 12:15 to 13:00 is 45 minutes. In hours: 45 ÷ 60 = ", 0.75, "45 minutes is three quarters of an hour."),
    box("Speed: 60 ÷ 0.75 = ", 80, "Distance ÷ time in hours.", phase="substitute"),
    box("Check: 80 × 0.75 = ", 60, "Speed × time rebuilds the distance.", done="Rebuilds 60 km, so 80 km/h is right."),
  ]},
 {  # G3 pressure factor 1/2, fraction
  "display": "An object exerts 500 N on the ground. Doubling the contact area would change the pressure by what factor?",
  "solutions": [1, 2], "calculator": False, "input_type": "fraction",
  "hint": "Pressure and area are inversely linked: double one, halve the other.",
  "misconceptions": [{"pattern": "direct_proportion", "expect": [2, 1],
    "message": "Pressure is inversely proportional to area: if the area doubles, the pressure halves. Factor = ½."}],
  "guided_steps": [
    say("Pressure = Force ÷ Area. The force 500 N stays the same; only the area changes."),
    box("Double the area, so the bottom of Force ÷ Area is multiplied by ", 2, "The area is doubled, so the denominator × 2."),
    box("Dividing by twice as much halves the result. New pressure = old pressure × ", 0.5, "Half of the original.", phase="substitute"),
    box("Check with numbers: area 1 m² gives 500 ÷ 1 = 500; area 2 m² gives 500 ÷ 2 = ", 250, "Force ÷ doubled area.", done="250 is half of 500, so the factor is ½."),
  ]},
 {  # G4 cuboid 5x4x2 -> density 5 (SVG)
  "display": SVG_CUBOID + CAP + "<br>A 200 g block of metal measures 5 cm × 4 cm × 2 cm. What is its density?",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Multiply all three sides for the volume, then divide the mass.",
  "misconceptions": [{"pattern": "one_face", "expect": 10,
    "message": "Volume is length × width × height = 5 × 4 × 2 = 40 cm³, not one face. Density = 200 ÷ 40 = 5 g/cm³."}],
  "guided_steps": [
    say("Density = Mass ÷ Volume. First multiply the three sides for the volume."),
    box("Volume = 5 × 4 × 2 = ", 40, "Length × width × height."),
    box("Density: 200 ÷ 40 = ", 5, "Mass ÷ volume.", phase="substitute"),
    box("Check: 5 × 40 = ", 200, "Density × volume rebuilds the mass.", done="Rebuilds 200 g, so 5 g/cm³ is right."),
  ]},
]

# ---------------- tier_guides ----------------
tier_guides = {
 "bronze": {
  "title": "Bronze: one formula, matching units",
  "steps": [
   "<strong>Speed</strong> = Distance ÷ Time. <strong>Density</strong> = Mass ÷ Volume. <strong>Pressure</strong> = Force ÷ Area.",
   "All three share one shape: a top quantity divided by a bottom one. To find a top quantity instead, multiply the other two.",
   "Write the formula, put the numbers in, divide (or multiply), then add the units.",
  ],
  "example": {
   "question": "A car travels 150 km in 3 hours. Find the speed.",
   "steps": [
    {"label": "Formula", "content": "Speed = Distance ÷ Time"},
    {"label": "Substitute", "content": "150 ÷ 3 = 50"},
    {"label": "Check", "content": "50 × 3 = 150 ✓"},
    {"label": "Answer", "content": "50 km/h", "isAnswer": True, "is_answer": True},
   ]}},
 "silver": {
  "title": "Silver: convert units, then use the formula",
  "steps": [
   "<strong>Time:</strong> change minutes to hours by dividing by 60. So 1 h 30 min = 1.5 h and 2 h 24 min = 2.4 h.",
   "<strong>Speed units:</strong> km/h to m/s divide by 3.6; m/s to km/h multiply by 3.6.",
   "<strong>Solids:</strong> find the volume first (cube = side³), then Density = Mass ÷ Volume.",
  ],
  "example": {
   "question": "Convert 90 km/h to m/s.",
   "steps": [
    {"label": "Rule", "content": "km/h to m/s: divide by 3.6"},
    {"label": "Calculate", "content": "90 ÷ 3.6 = 25"},
    {"label": "Check", "content": "25 × 3.6 = 90 ✓"},
    {"label": "Answer", "content": "25 m/s", "isAnswer": True, "is_answer": True},
   ]}},
 "gold": {
  "title": "Gold: multi-step compound measures",
  "steps": [
   "<strong>Average speed</strong> = total distance ÷ total time. Never just average the speeds unless each leg takes equal time.",
   "<strong>Cylinder volume</strong> = πr²h: square the radius, not the diameter.",
   "Work in stages: find each part (time, volume), keep them, then combine at the very end.",
  ],
  "example": {
   "question": "A cyclist rides 12 km at 12 km/h, then 12 km at 6 km/h. Find the average speed.",
   "steps": [
    {"label": "Times", "content": "12 ÷ 12 = 1 h; 12 ÷ 6 = 2 h"},
    {"label": "Combine", "content": "24 km ÷ 3 h"},
    {"label": "Check", "content": "Averaging 12 and 6 gives 9, which is wrong ✓"},
    {"label": "Answer", "content": "8 km/h", "isAnswer": True, "is_answer": True},
   ]}},
}

# ---------------- guided (opener + teach) ----------------
guided = {
 "opener": {
  "display": SVG_JOURNEY + CAP + "<br>On a road trip you cover 120 miles in 2 hours. Work out your average speed in mph.",
  "steps": [
   box("Split the distance evenly across the time: 120 ÷ 2 = ", 60, "How many miles in each single hour?"),
   say("You just found <strong>speed = distance ÷ time</strong>. That is the whole idea. Density and pressure work the same way: one quantity shared by another (mass ÷ volume, force ÷ area). Every question here is really 'pick the formula, then divide or multiply'."),
  ]},
 "teach": {
  "bronze": {
   "display": "A van travels 180 km in 4 hours. Find its speed, then how far it goes in 7 hours at that speed.",
   "steps": [
    say("Speed = Distance ÷ Time. Find the speed first."),
    box("180 ÷ 4 = ", 45, "Share 180 km across 4 hours."),
    box("Check: 45 × 4 = ", 180, "Speed × time rebuilds the distance.", done="Back to 180 km, so 45 km/h."),
    box("Now distance in 7 hours: Distance = Speed × Time = 45 × 7 = ", 315, "Multiply the speed by 7."),
    box("Check: 315 ÷ 7 = ", 45, "Distance ÷ time returns the speed.", done="Divides back to 45 km/h. The formula works both ways."),
   ]},
  "silver": {
   "display": "A sprinter runs 200 m in 25 seconds. Find the speed in m/s, then convert it to km/h.",
   "steps": [
    say("First the basic speed in m/s, then convert the units."),
    box("200 ÷ 25 = ", 8, "Distance ÷ time in m/s."),
    box("m/s to km/h: multiply by 3.6. 8 × 3.6 = ", 28.8, "m/s to km/h is × 3.6."),
    box("Check back: 28.8 ÷ 3.6 = ", 8, "Divide by 3.6 to return to m/s.", done="Returns to 8 m/s."),
    box("In one minute, 60 s, they cover 8 × 60 = ", 480, "Metres per second × 60.", done="480 m per minute, all from the one speed."),
   ]},
  "gold": {
   "display": "A coach drives 60 km at 60 km/h, then 90 km at 45 km/h. Find the average speed for the whole trip.",
   "steps": [
    say("Average speed is total distance ÷ total time. Find each leg's time first."),
    box("Leg 1 time: 60 ÷ 60 = ", 1, "Distance ÷ speed for leg 1."),
    box("Leg 2 time: 90 ÷ 45 = ", 2, "Distance ÷ speed for leg 2."),
    box("Total distance: 60 + 90 = ", 150, "Add the two distances."),
    box("Average speed: 150 ÷ 3 = ", 50, "Total distance ÷ total time (1 + 2 = 3 h).", done="Not (60 + 45) ÷ 2 = 52.5. Total ÷ total gives 50 km/h."),
   ]},
 }}

# ---------------- method_card (slim) ----------------
method_card = {
 "title": "Speed, Density & Pressure",
 "steps": [
  "Speed = Distance ÷ Time. Rearrange: D = S × T, T = D ÷ S.",
  "Density = Mass ÷ Volume. Pressure = Force ÷ Area. Same triangle pattern.",
  "Match units first: minutes to hours, and length units before a volume.",
  "To find the top of a triangle, multiply; to find a bottom, divide.",
 ],
 "content": ("<p>Three compound measures share one pattern: a top quantity equals the two below it, combined.</p>"
  "<p><strong>Speed</strong> = Distance ÷ Time. <strong>Density</strong> = Mass ÷ Volume. <strong>Pressure</strong> = Force ÷ Area.</p>"
  "<p>Use a <strong>formula triangle</strong>: cover the quantity you want and what is left is the calculation. Covering a bottom corner leaves a division; covering the top leaves a multiplication.</p>"
  "<p>Always make <strong>units</strong> agree first: change minutes to hours for km/h, and match length units before finding a volume.</p>"),
 "example": ("<p><strong>A block has mass 450 g and volume 50 cm³. Find its density.</strong></p>"
  "<p>Density = Mass ÷ Volume = 450 ÷ 50 = 9 g/cm³.</p>"),
}

# ---------------- assemble (preserve topic_links, related_videos, worked_examples) ----------------
live = json.load(io.open("_live_rp03.json", encoding="utf-8"))

pd = {
 "method_card": method_card,
 "topic_links": live["topic_links"],
 "problem_bank": {
   "bronze": bronze, "silver": silver, "gold": gold,
   "bronze_description": "Use one formula (speed, density or pressure) when the units already match.",
   "silver_description": "Convert units first (minutes to hours, km/h to m/s) or find a volume before dividing.",
   "gold_description": "Multi-step problems: average speed, cylinder volumes, and reasoning about the formula.",
 },
 "related_videos": live["related_videos"],
 "worked_examples": live["worked_examples"],
 "tier_guides": tier_guides,
 "guided": guided,
}

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT)
