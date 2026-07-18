# -*- coding: utf-8 -*-
import json, io

src = json.load(io.open("_fetched_canonical.json", encoding="utf-8"))
pd = src["practice_data"]

# ---------- helpers ----------
def sub(say, pre, ans, hint, post="", phase=False, done=None):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if say is not None: d["say"] = say
    if phase: d["phase"] = "substitute"
    if done: d["done"] = done
    return d

def say(s):
    return {"say": s}

# =========================================================
# METHOD CARD (slim; no em dashes; <=140 words; <=4 steps)
# =========================================================
pd["method_card"] = {
    "title": "Pressure in Fluids",
    "steps": [
        "Identify which equation: p = F/A (solid on a surface) or p = hρg (liquid at depth)",
        "Convert units first: cm to m (÷100), cm² to m² (÷10,000)",
        "Substitute the values and calculate",
        "State the answer with its unit; for total pressure at depth, add atmospheric pressure",
    ],
    "content": ("<p>Two pressure equations, and you must choose the right one.</p>"
        "<p><strong>Solid on a surface:</strong> \\(p = \\frac{F}{A}\\). The force is the object's weight; "
        "the area is the contact face. For maximum pressure, use the smallest face.</p>"
        "<p><strong>Liquid at depth:</strong> \\(p = h\\rho g\\). Depth in metres, density in kg/m³.</p>"
        "<p><strong>Watch the units:</strong> cm to m divide by 100; cm² to m² divide by 10,000. "
        "For total pressure in a liquid, add atmospheric pressure (about 101,000 Pa) to the liquid pressure. "
        "Remember 1 kPa = 1000 Pa.</p>"),
}

# exam_context: strip the em dash
pd["exam_context"]["frequency"] = "Common, pressure appears on most Paper 1 exams"

# =========================================================
# PROBLEM BANK  (keep displays/units/equation_hint; add hint,
# guided_steps, expect-bearing misconceptions)
# =========================================================
pb = pd["problem_bank"]

# ---- fix duplicate bronze answer: B3 50000 -> 60000 (F 5000 -> 6000)
b = pb["bronze"]
b[2]["display"] = "A pressure of 60,000 Pa acts over an area of 0.1 m². Calculate the force."
b[2]["solutions"] = [6000]

# ---------- BRONZE ----------
b[0]["hint"] = "Pressure is force divided by area."
b[0]["misconceptions"] = [{"pattern": "inverse_error", "check": "common", "expect": 8,
    "message": "Pressure = force ÷ area, not force × area. 200 ÷ 0.04 = 5000 Pa."}]
b[0]["guided_steps"] = [
    say("Pressure is how hard a force presses on each bit of area: \\(p = \\frac{F}{A}\\)."),
    sub(None, "Force in N: F = ", 200, "Read the box's weight straight from the question."),
    sub(None, "Contact area in m²: A = ", 0.04, "It is already in m², no conversion needed."),
    sub("Now divide force by area.", "p = 200 ÷ 0.04 = ", 5000, "Dividing by 0.04 is the same as ×25.", phase=True),
    sub(None, "Check: 5000 × 0.04 = ", 200, "Multiply your pressure by the area.", done="Back to 200 N, so p = 5000 Pa."),
]

b[1]["hint"] = "Liquid pressure is depth × density × g."
b[1]["misconceptions"] = [{"pattern": "forgot_step", "check": "common", "expect": 2000,
    "message": "Do not forget g. p = hρg = 2 × 1000 × 9.8 = 19,600 Pa. Leaving out g gives 2000."}]
b[1]["guided_steps"] = [
    say("Liquid pressure grows with depth: \\(p = h\\rho g\\)."),
    sub(None, "Depth in m: h = ", 2, "Straight from the question."),
    sub(None, "Density in kg/m³: ρ = ", 1000, "Given as water."),
    sub("Multiply depth × density × g, with g = 9.8.", "p = 2 × 1000 × 9.8 = ", 19600, "2 × 1000 = 2000, then × 9.8.", phase=True),
    sub(None, "Check: 19,600 ÷ 9800 = ", 2, "Divide the pressure by ρg.", done="Back to 2 m, so p = 19,600 Pa."),
]

b[2]["hint"] = "Force is pressure × area."
b[2]["misconceptions"] = [{"pattern": "inverse_error", "check": "common", "expect": 600000,
    "message": "Force = pressure × area = 60,000 × 0.1 = 6000 N. Dividing (60,000 ÷ 0.1 = 600,000) is the slip."}]
b[2]["guided_steps"] = [
    say("To get force from pressure: \\(F = p \\times A\\)."),
    sub(None, "Pressure in Pa: p = ", 60000, "From the question."),
    sub(None, "Area in m²: A = ", 0.1, "Already in m²."),
    sub("Multiply pressure by area.", "F = 60,000 × 0.1 = ", 6000, "× 0.1 moves the decimal one place.", phase=True),
    sub(None, "Check: 6000 ÷ 0.1 = ", 60000, "Divide force by area.", done="Back to 60,000 Pa, so F = 6000 N."),
]

b[3]["hint"] = "Pressure is force divided by area."
b[3]["misconceptions"] = [{"pattern": "inverse_error", "check": "common", "expect": 25,
    "message": "Pressure = force ÷ area = 500 ÷ 0.05 = 10,000 Pa. Multiplying (500 × 0.05 = 25) is the slip."}]
b[3]["guided_steps"] = [
    say("Use \\(p = \\frac{F}{A}\\)."),
    sub(None, "Force in N: F = ", 500, "The crate's weight."),
    sub(None, "Area in m²: A = ", 0.05, "Given in m²."),
    sub("Divide force by area.", "p = 500 ÷ 0.05 = ", 10000, "÷ 0.05 is the same as ×20.", phase=True),
    sub(None, "Check: 10,000 × 0.05 = ", 500, "Multiply pressure by area.", done="Back to 500 N, so p = 10,000 Pa."),
]

b[4]["hint"] = "Use p = hρg for liquid depth."
b[4]["misconceptions"] = [{"pattern": "forgot_step", "check": "common", "expect": 5000,
    "message": "Multiply by g as well: p = 5 × 1000 × 9.8 = 49,000 Pa. Leaving out g gives 5000."}]
b[4]["guided_steps"] = [
    say("\\(p = h\\rho g\\) for a liquid."),
    sub(None, "Depth in m: h = ", 5, "From the question."),
    sub(None, "Density in kg/m³: ρ = ", 1000, "Water."),
    sub("Multiply depth × density × g.", "p = 5 × 1000 × 9.8 = ", 49000, "5 × 1000 = 5000, then × 9.8.", phase=True),
    sub(None, "Check: 49,000 ÷ 9800 = ", 5, "Divide by ρg = 9800.", done="Back to 5 m, so p = 49,000 Pa."),
]

b[5]["hint"] = "Area is force divided by pressure."
b[5]["misconceptions"] = [{"pattern": "inverse_error", "check": "common", "expect": 5,
    "message": "Area = force ÷ pressure = 600 ÷ 3000 = 0.2 m². Dividing the other way (3000 ÷ 600 = 5) is the slip."}]
b[5]["guided_steps"] = [
    say("Rearrange \\(p = \\frac{F}{A}\\) to \\(A = \\frac{F}{p}\\)."),
    sub(None, "Force in N: F = ", 600, "From the question."),
    sub(None, "Pressure in Pa: p = ", 3000, "From the question."),
    sub("Divide force by pressure.", "A = 600 ÷ 3000 = ", 0.2, "600 ÷ 3000 = 6 ÷ 30.", phase=True),
    sub(None, "Check: 600 ÷ 0.2 = ", 3000, "Force ÷ area should give the pressure.", done="Back to 3000 Pa, so A = 0.2 m²."),
]

b[6]["hint"] = "Rearrange p = hρg to h = p ÷ (ρg)."
b[6]["misconceptions"] = [{"pattern": "wrong_rearrange", "check": "common", "expect": 29.4,
    "message": "Divide by ρg, not just ρ: h = 29,400 ÷ (1000 × 9.8) = 29,400 ÷ 9800 = 3 m. Dividing by 1000 alone gives 29.4."}]
b[6]["guided_steps"] = [
    say("Rearrange \\(p = h\\rho g\\) to \\(h = \\frac{p}{\\rho g}\\)."),
    sub(None, "Pressure in Pa: p = ", 29400, "From the question."),
    sub(None, "Work out ρg first: 1000 × 9.8 = ", 9800, "Density times g."),
    sub("Divide pressure by ρg.", "h = 29,400 ÷ 9800 = ", 3, "29,400 ÷ 9800.", phase=True),
    sub(None, "Check: 3 × 9800 = ", 29400, "Depth × ρg gives the pressure.", done="Back to 29,400 Pa, so h = 3 m."),
]

b[7]["hint"] = "Force is pressure × area."
b[7]["misconceptions"] = [{"pattern": "inverse_error", "check": "common", "expect": 1600,
    "message": "Force = pressure × area = 800 × 0.5 = 400 N. Dividing (800 ÷ 0.5 = 1600) is the slip."}]
b[7]["guided_steps"] = [
    say("\\(F = p \\times A\\)."),
    sub(None, "Pressure in Pa: p = ", 800, "From the question."),
    sub(None, "Area in m²: A = ", 0.5, "Given in m²."),
    sub("Multiply pressure by area.", "F = 800 × 0.5 = ", 400, "× 0.5 means halve it.", phase=True),
    sub(None, "Check: 400 ÷ 0.5 = ", 800, "Force ÷ area gives pressure.", done="Back to 800 Pa, so F = 400 N."),
]

# ---------- SILVER ----------
s = pb["silver"]
s[0]["hint"] = "Convert both sides to metres before finding the area."
s[0]["misconceptions"] = [{"pattern": "forgot_convert", "check": "common", "expect": 0.3,
    "message": "Convert cm to m first: 0.2 m × 0.5 m = 0.1 m². Pressure = 300 ÷ 0.1 = 3000 Pa. Using cm (area 1000) gives 0.3."}]
s[0]["guided_steps"] = [
    say("\\(p = \\frac{F}{A}\\), but the sides are in centimetres, so convert first."),
    sub(None, "Width in m: 20 cm ÷ 100 = ", 0.2, "Divide cm by 100."),
    sub(None, "Length in m: 50 cm ÷ 100 = ", 0.5, "Divide cm by 100."),
    sub(None, "Area in m²: 0.2 × 0.5 = ", 0.1, "Multiply the two sides."),
    sub("Now use p = F/A.", "p = 300 ÷ 0.1 = ", 3000, "÷ 0.1 is × 10.", phase=True),
    sub(None, "Check: 3000 × 0.1 = ", 300, "Pressure × area gives force.", done="Back to 300 N, so p = 3000 Pa."),
]

s[1]["hint"] = "Use the density of mercury, then p = hρg."
s[1]["misconceptions"] = [{"pattern": "wrong_density", "check": "common", "expect": 7840,
    "message": "Use the density of mercury (13,600 kg/m³), not water. p = 0.8 × 13,600 × 9.8 = 106,624 Pa. Water gives 7840."}]
s[1]["guided_steps"] = [
    say("\\(p = h\\rho g\\). The twist is the density: use mercury, not water."),
    sub(None, "Depth in m: h = ", 0.8, "From the question."),
    sub(None, "Density of mercury in kg/m³: ρ = ", 13600, "Given in the question, not 1000."),
    sub("Multiply depth × density × g.", "p = 0.8 × 13,600 × 9.8 = ", 106624, "0.8 × 13,600 = 10,880, then × 9.8.", phase=True),
    sub(None, "Check: 106,624 ÷ (13,600 × 9.8) = ", 0.8, "Divide by ρg.", done="Back to 0.8 m, so p = 106,624 Pa."),
]

s[2]["hint"] = "Work out the liquid pressure, then add atmospheric pressure."
s[2]["misconceptions"] = [{"pattern": "forgot_atmospheric", "check": "common", "expect": 98000,
    "message": "Add atmospheric pressure too: total = 98,000 + 101,000 = 199,000 Pa. The liquid pressure alone is 98,000."}]
s[2]["guided_steps"] = [
    say("Total pressure is the water's pressure PLUS the air pushing down: \\(p_{\\text{total}} = h\\rho g + p_{\\text{atm}}\\)."),
    sub(None, "Liquid pressure: 10 × 1000 × 9.8 = ", 98000, "hρg for the water."),
    sub("Add atmospheric pressure.", "Total = 98,000 + 101,000 = ", 199000, "Add the air's pressure on top.", phase=True),
    sub(None, "Check: 199,000 − 101,000 = ", 98000, "Subtract atmospheric to get the liquid pressure back.", done="That is the water's share, so total = 199,000 Pa."),
]

s[3]["hint"] = "Convert cm² to m² by dividing by 10,000."
s[3]["misconceptions"] = [
    {"pattern": "wrong_conversion", "check": "common", "expect": 2500,
     "message": "Convert cm² to m² by dividing by 10,000: 2 cm² = 0.0002 m². p = 50 ÷ 0.0002 = 250,000 Pa. Dividing by 100 gives 2500."},
    {"pattern": "forgot_convert", "check": "common", "expect": 25,
     "message": "The area must be in m². Leaving it as 2 gives 50 ÷ 2 = 25, far too small. 2 cm² = 0.0002 m²."},
]
s[3]["guided_steps"] = [
    say("\\(p = \\frac{F}{A}\\), but the area is in cm², so convert to m² first."),
    sub(None, "1 m² = 10,000 cm², so 2 cm² in m² = 2 ÷ 10,000 = ", 0.0002, "Divide by 10,000, not 100."),
    sub(None, "Force in N: F = ", 50, "From the question."),
    sub("Now divide force by area.", "p = 50 ÷ 0.0002 = ", 250000, "50 ÷ 0.0002 = 50 × 5000.", phase=True),
    sub(None, "Check: 250,000 × 0.0002 = ", 50, "Pressure × area gives force.", done="Back to 50 N, so p = 250,000 Pa."),
]

s[4]["hint"] = "Rearrange p = hρg to ρ = p ÷ (hg)."
s[4]["misconceptions"] = [{"pattern": "wrong_rearrange", "check": "common", "expect": 9800,
    "message": "Divide by hg, not just h: ρ = 34,300 ÷ (3.5 × 9.8) = 34,300 ÷ 34.3 = 1000 kg/m³. Dividing by 3.5 alone gives 9800."}]
s[4]["guided_steps"] = [
    say("Rearrange \\(p = h\\rho g\\) to \\(\\rho = \\frac{p}{hg}\\)."),
    sub(None, "Pressure in Pa: p = ", 34300, "From the question."),
    sub(None, "Work out hg first: 3.5 × 9.8 = ", 34.3, "Depth times g."),
    sub("Divide pressure by hg.", "ρ = 34,300 ÷ 34.3 = ", 1000, "34,300 ÷ 34.3.", phase=True),
    sub(None, "Check: 1000 × 34.3 = ", 34300, "Density × hg gives pressure.", done="Back to 34,300 Pa, so ρ = 1000 kg/m³."),
]

s[5]["hint"] = "Use the difference in depth, 8 − 3 metres."
s[5]["misconceptions"] = [{"pattern": "forgot_step", "check": "common", "expect": 78400,
    "message": "Use the difference in depth: Δh = 8 − 3 = 5 m. Δp = 5 × 1000 × 9.8 = 49,000 Pa. Using 8 m gives 78,400."}]
s[5]["guided_steps"] = [
    say("Pressure difference depends on the CHANGE in depth: \\(\\Delta p = \\Delta h \\times \\rho g\\)."),
    sub(None, "Change in depth: 8 − 3 = ", 5, "Deeper minus shallower."),
    sub(None, "Density in kg/m³: ρ = ", 1000, "Water."),
    sub("Multiply the depth change × density × g.", "Δp = 5 × 1000 × 9.8 = ", 49000, "5 × 1000 = 5000, then × 9.8.", phase=True),
    sub(None, "Check: 49,000 ÷ 9800 = ", 5, "Divide by ρg.", done="Back to 5 m of extra depth, so Δp = 49,000 Pa."),
]

# ---------- GOLD ----------
g = pb["gold"]
g[0]["hint"] = "Find the liquid pressure with hρg, then add atmospheric pressure."
g[0]["misconceptions"] = [
    {"pattern": "forgot_atmospheric", "check": "common", "expect": 251125,
     "message": "Add atmospheric pressure: total = 251,125 + 101,000 = 352,125 Pa. The liquid pressure alone is 251,125."},
    {"pattern": "wrong_density", "check": "common", "expect": 346000,
     "message": "Use seawater density 1025 kg/m³, not 1000. Liquid pressure = 25 × 1025 × 9.8 = 251,125 Pa, total 352,125 Pa. Fresh water gives 346,000."},
]
g[0]["guided_steps"] = [
    say("Two steps: liquid pressure with \\(h\\rho g\\), then add atmospheric pressure."),
    sub(None, "Density of seawater in kg/m³: ρ = ", 1025, "Given as seawater, not 1000."),
    sub(None, "Liquid pressure: 25 × 1025 × 9.8 = ", 251125, "25 × 1025 = 25,625, then × 9.8."),
    sub("Add atmospheric pressure.", "Total = 251,125 + 101,000 = ", 352125, "Add the air's pressure on top.", phase=True),
    sub(None, "Check: 352,125 − 101,000 = ", 251125, "Subtract atmospheric to get the liquid pressure back.", done="That is the water's share, so total = 352,125 Pa."),
]

g[1]["hint"] = "Weight first, then divide by the smallest face for maximum pressure."
g[1]["misconceptions"] = [
    {"pattern": "wrong_face", "check": "common", "expect": 1960,
     "message": "For MAXIMUM pressure use the SMALLEST face (0.2 × 0.1 = 0.02 m²): p = 196 ÷ 0.02 = 9800 Pa. The largest face (0.1 m²) gives 1960."},
    {"pattern": "forgot_step", "check": "common", "expect": 1000,
     "message": "Use the weight, not the mass: weight = 20 × 9.8 = 196 N, then p = 196 ÷ 0.02 = 9800 Pa. Using 20 N gives 1000."},
]
g[1]["guided_steps"] = [
    say("Maximum pressure needs the smallest face. First find the weight, then divide by the smallest area."),
    sub(None, "Weight in N: 20 × 9.8 = ", 196, "Weight = mass × g."),
    sub(None, "Smallest face area in m²: 0.2 × 0.1 = ", 0.02, "Multiply the two smallest sides."),
    sub("Divide weight by the smallest face.", "p = 196 ÷ 0.02 = ", 9800, "196 ÷ 0.02 = 196 × 50.", phase=True),
    sub(None, "Check: 9800 × 0.02 = ", 196, "Pressure × area gives the weight.", done="Back to 196 N, so p = 9800 Pa."),
]

g[2]["hint"] = "Find the pressure at 40 m, then multiply by the gate area."
g[2]["misconceptions"] = [{"pattern": "forgot_step", "check": "common", "expect": 392000,
    "message": "Multiply the pressure by the gate area: F = 392,000 × 3 = 1,176,000 N. Stopping at the pressure gives 392,000."}]
g[2]["guided_steps"] = [
    say("Two steps: pressure at 40 m with \\(h\\rho g\\), then force with \\(F = p \\times A\\)."),
    sub(None, "Pressure at 40 m: 40 × 1000 × 9.8 = ", 392000, "hρg at the full depth."),
    sub(None, "Gate area in m²: 2 × 1.5 = ", 3, "Width times height."),
    sub("Multiply pressure by the gate area.", "F = 392,000 × 3 = ", 1176000, "392,000 × 3.", phase=True),
    sub(None, "Check: 1,176,000 ÷ 3 = ", 392000, "Force ÷ area gives the pressure.", done="Back to 392,000 Pa, so F = 1,176,000 N."),
]

g[3]["hint"] = "Pressure is the same in the fluid: find it from the small piston, then F = p × A."
g[3]["misconceptions"] = [{"pattern": "inverse_error", "check": "common", "expect": 2.5,
    "message": "The large piston has the larger area, so the force is multiplied: F = 50 × (0.04 ÷ 0.002) = 1000 N. Inverting the ratio gives 2.5."}]
g[3]["guided_steps"] = [
    say("Pressure is the same everywhere in the fluid. Find it from the small piston, then use \\(F = p \\times A\\) on the large one."),
    sub(None, "Pressure in the fluid: 50 ÷ 0.002 = ", 25000, "F ÷ A on the small piston."),
    sub(None, "Large piston area in m²: A = ", 0.04, "From the question."),
    sub("Multiply that pressure by the large area.", "F = 25,000 × 0.04 = ", 1000, "25,000 × 0.04.", phase=True),
    sub(None, "Check: 1000 ÷ 0.04 = ", 25000, "Force ÷ area gives the pressure back.", done="Same fluid pressure, so F = 1000 N."),
]

g[4]["hint"] = "Rearrange p = hρg to h = p ÷ (ρg)."
g[4]["misconceptions"] = [
    {"pattern": "wrong_density", "check": "common", "expect": 10.3,
     "message": "Use the density of oil (800 kg/m³): h = 101,000 ÷ (800 × 9.8) = 12.9 m. Using water (1000) gives 10.3."},
    {"pattern": "wrong_rearrange", "check": "common", "expect": 126.25,
     "message": "Divide by ρg, not just ρ: h = 101,000 ÷ 7840 = 12.9 m. Dividing by 800 alone gives 126.25."},
]
g[4]["guided_steps"] = [
    say("Rearrange \\(p = h\\rho g\\) to \\(h = \\frac{p}{\\rho g}\\). The answer is to 1 decimal place."),
    sub(None, "Work out ρg first: 800 × 9.8 = ", 7840, "Density of oil times g."),
    sub(None, "Pressure to match, in Pa: ", 101000, "Atmospheric pressure, from the question."),
    sub("Divide the pressure by ρg and round to 1 d.p.", "h = 101,000 ÷ 7840 = ", 12.9, "101,000 ÷ 7840 = 12.88, which rounds to 12.9.", phase=True),
    sub(None, "Check: 12.9 × 7840 = ", 101136, "Depth × ρg should return the pressure.", done="About 101,000 Pa, so h = 12.9 m to 1 d.p."),
]

g[5]["hint"] = "Find total pressure in Pa, then divide by 1000 for kPa."
g[5]["misconceptions"] = [
    {"pattern": "forgot_atmospheric", "check": "common", "expect": 2009,
     "message": "Add atmospheric pressure before converting: 2,009,000 + 101,000 = 2,110,000 Pa = 2110 kPa. The liquid pressure alone is 2009 kPa."},
    {"pattern": "unit_error", "check": "common", "expect": 2110000,
     "message": "Convert Pa to kPa by dividing by 1000: 2,110,000 Pa = 2110 kPa. Leaving it in Pa gives 2,110,000."},
]
g[5]["guided_steps"] = [
    say("Total pressure in Pa first, then convert to kPa by dividing by 1000."),
    sub(None, "Liquid pressure: 200 × 1025 × 9.8 = ", 2009000, "hρg: 200 × 1025 = 205,000, then × 9.8."),
    sub("Add atmospheric pressure.", "2,009,000 + 101,000 = ", 2110000, "Add the air's pressure.", phase=True),
    sub(None, "Convert to kPa: 2,110,000 ÷ 1000 = ", 2110, "Move the decimal three places."),
    sub(None, "Check: 2110 × 1000 = ", 2110000, "kPa × 1000 gives Pa.", done="Back to 2,110,000 Pa, so total = 2110 kPa."),
]

# tier descriptions
pb["bronze_description"] = "One equation, values already in the right units: substitute straight in."
pb["silver_description"] = "Convert a unit first (cm to m, cm² to m²), or rearrange the equation before substituting."
pb["gold_description"] = "More than one step: total pressure at depth, a force from a pressure, or a hydraulic ratio."

# =========================================================
# TIER GUIDES
# =========================================================
def ex(q, steps):
    return {"question": q, "steps": steps}
def st(label, content, ans=False):
    d = {"label": label, "content": content}
    if ans:
        d["isAnswer"] = True; d["is_answer"] = True
    return d

pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one equation, straight in",
        "steps": [
            "Pick the right equation. Solid pressing on a surface: \\(p = \\frac{F}{A}\\). Liquid at depth: \\(p = h\\rho g\\).",
            "The values are already in the right units (N, m², m, kg/m³). Substitute and calculate in one go.",
            "State the answer with its unit, usually pascals (Pa).",
        ],
        "example": ex("A crate weighs 240 N and its base covers 0.06 m². Find the pressure.", [
            st("Equation", "<p>Solid on a surface: \\(p = \\frac{F}{A}\\).</p>"),
            st("Substitute", "<p>\\(p = \\frac{240}{0.06}\\)</p>"),
            st("Check", "<p>\\(4000 \\times 0.06 = 240\\) N ✓</p>"),
            st("Answer", "<p><strong>4000 Pa</strong></p>", ans=True),
        ]),
    },
    "silver": {
        "title": "Silver: convert units, or rearrange first",
        "steps": [
            "Same equations, but a value is in the wrong unit. Convert before you substitute: cm to m (÷100), cm² to m² (÷10,000).",
            "Or the unknown is not the subject: rearrange first, for example \\(h = \\frac{p}{\\rho g}\\).",
            "Then it is a bronze question: substitute and state the unit.",
        ],
        "example": ex("A pin is pushed with 60 N through a point of area 3 cm². Find the pressure in Pa.", [
            st("Convert", "<p>\\(3\\) cm² = \\(3 \\div 10{,}000 = 0.0003\\) m².</p>"),
            st("Substitute", "<p>\\(p = \\frac{60}{0.0003}\\)</p>"),
            st("Check", "<p>\\(200{,}000 \\times 0.0003 = 60\\) N ✓</p>"),
            st("Answer", "<p><strong>200,000 Pa</strong></p>", ans=True),
        ]),
    },
    "gold": {
        "title": "Gold: more than one step",
        "steps": [
            "Two moves chained. Total pressure at depth: work out the liquid pressure \\(h\\rho g\\), then ADD atmospheric pressure (about 101,000 Pa).",
            "Or find a force from a pressure: \\(p = h\\rho g\\) first, then \\(F = p \\times A\\).",
            "Keep units consistent all the way through and state the final unit.",
        ],
        "example": ex("A submarine is 30 m deep in seawater (1025 kg/m³). Atmospheric pressure is 101,000 Pa, g = 9.8. Find the total pressure.", [
            st("Liquid pressure", "<p>\\(p = h\\rho g = 30 \\times 1025 \\times 9.8 = 301{,}350\\) Pa.</p>"),
            st("Add atmospheric", "<p>\\(301{,}350 + 101{,}000\\)</p>"),
            st("Check", "<p>\\(402{,}350 - 101{,}000 = 301{,}350\\) Pa ✓</p>"),
            st("Answer", "<p><strong>402,350 Pa</strong></p>", ans=True),
        ]),
    },
}

# =========================================================
# GUIDED: opener + teach walks
# =========================================================
pd["guided"] = {
    "opener": {
        "label": "Before any equation",
        "display": ("Same 60 N of weight, two different shoes:<br>"
                    "snowshoe touching 2 m² of snow, or a stiletto heel touching just 0.01 m²."),
        "steps": [
            sub("No equation yet, just share the weight out over the area it presses on.",
                "Force per square metre under the snowshoe: 60 ÷ 2 = ", 30,
                "Divide the weight by the area it spreads over."),
            sub("Now the heel, same weight but a tiny area:",
                "Force per square metre under the heel: 60 ÷ 0.01 = ", 6000,
                "Divide 60 by 0.01, the same as × 100."),
            say("Same person, same weight, but the heel presses 6000 on each square metre against the snowshoe's 30. "
                "That force-per-area is exactly <strong>pressure</strong>, \\(p = \\frac{F}{A}\\). Small area, big pressure, "
                "which is why a heel dents a floor a boot never would. Liquids do the same with depth: \\(p = h\\rho g\\)."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "Solve: a lake is 3 m deep. The water density is 1000 kg/m³ and g = 9.8 N/kg. Find the water pressure at the bottom.",
            "label": "Together: your first one",
            "steps": [
                say("This is a liquid, so use \\(p = h\\rho g\\)."),
                sub(None, "Depth in m: h = ", 3, "From the question."),
                sub(None, "Density in kg/m³: ρ = ", 1000, "Given as water."),
                sub("Multiply depth × density × g.", "p = 3 × 1000 × 9.8 = ", 29400, "3 × 1000 = 3000, then × 9.8."),
                sub(None, "Check: 29,400 ÷ 9800 = ", 3, "Divide by ρg.", done="Back to 3 m, so p = 29,400 Pa."),
            ],
        },
        "silver": {
            "display": "Solve: a brick presses down with a force of 40 N through a face of area 200 cm². Find the pressure in Pa.",
            "label": "Together: the silver move",
            "steps": [
                say("Use \\(p = \\frac{F}{A}\\), but the area is in cm², so convert to m² first."),
                sub(None, "200 cm² in m² = 200 ÷ 10,000 = ", 0.02, "Divide by 10,000."),
                sub(None, "Force in N: F = ", 40, "From the question."),
                sub("Now divide force by area.", "p = 40 ÷ 0.02 = ", 2000, "40 ÷ 0.02 = 40 × 50."),
                sub(None, "Check: 2000 × 0.02 = ", 40, "Pressure × area gives force.", done="Back to 40 N, so p = 2000 Pa."),
            ],
        },
        "gold": {
            "display": "Solve: a diver is 15 m below the surface of the sea. The density of seawater is 1030 kg/m³, g = 9.8 N/kg, and atmospheric pressure is 101,000 Pa. Find the TOTAL pressure on the diver.",
            "label": "Together: the gold move",
            "steps": [
                say("Two steps: liquid pressure with \\(h\\rho g\\), then add atmospheric pressure."),
                sub(None, "Depth in m: h = ", 15, "From the question."),
                sub(None, "Liquid pressure: 15 × 1030 × 9.8 = ", 151410, "15 × 1030 = 15,450, then × 9.8."),
                sub("Add atmospheric pressure.", "Total = 151,410 + 101,000 = ", 252410, "Add the air's pressure on top."),
                sub(None, "Check: 252,410 − 101,000 = ", 151410, "Subtract atmospheric to get the liquid pressure back.", done="That is the water's share, so total = 252,410 Pa."),
            ],
        },
    },
}

# worked_examples: replace em dash in step labels with colon (validator bans em dash)
for we in pd.get("worked_examples", []):
    for stp in we.get("steps", []):
        if "label" in stp and "—" in stp["label"]:
            stp["label"] = stp["label"].replace(" — ", ": ").replace("—", ": ")

out = "lesson_higher-calculations-L04@b4b6d1f722.json"
with io.open(out, "w", encoding="utf-8") as f:
    f.write(json.dumps(pd, indent=1, ensure_ascii=False))
print("written", out)

# quick em-dash scan
def scan(o, p=""):
    hits = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("note", "guided_skip_reason"): continue
            hits += scan(v, p + "." + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o): hits += scan(v, p + "[%d]" % i)
    elif isinstance(o, str) and "—" in o:
        hits.append(p)
    return hits
print("em-dash hits:", scan(pd))
