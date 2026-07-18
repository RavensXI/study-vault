# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open('_live_canonical.json', encoding='utf-8'))
pb = pd['problem_bank']

# ---- 1. Fix em dashes in preserved fields (style rule is hard) ----
pd['exam_context']['frequency'] = "Common: pressure appears on most Paper 1 exams"
for we in pd['worked_examples']:
    for stp in we['steps']:
        stp['label'] = stp['label'].replace(' — ', ': ')

# ---- 2. method_card: slim, no em dash, add example ----
pd['method_card']['content'] = (
    "<p>Two pressure equations, so pick the right one for the situation.</p>"
    "<p><strong>Solid on a surface:</strong> \\(p = \\frac{F}{A}\\). The force is the object's weight; "
    "the area is the contact area. For MAXIMUM pressure, use the smallest face.</p>"
    "<p><strong>Liquid at a depth:</strong> \\(p = h\\rho g\\). Depth in metres, density in kg/m³.</p>"
    "<p><strong>Units:</strong> cm to m divide by 100; cm² to m² divide by 10,000. For total pressure "
    "in a liquid, add atmospheric pressure (about 101,000 Pa). 1 kPa = 1000 Pa.</p>"
)
pd['method_card']['example'] = (
    "<p><strong>Solve:</strong> a 300 N box rests on 0.06 m².</p>"
    "<p>\\(p = \\frac{F}{A} = \\frac{300}{0.06} = 5000\\) Pa.</p>"
)

# ---- 3. Fix duplicate bronze[2]: 50000 Pa -> 40000 Pa (answer 4000 N) ----
b2 = pb['bronze'][2]
b2['display'] = "A pressure of 40,000 Pa acts over an area of 0.1 m². Calculate the force."
b2['solutions'] = [4000]

# ---- helpers ----
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def say(s): return {"say": s}
def m(pattern, message, expect):
    return {"check": "common", "pattern": pattern, "message": message, "expect": expect}
def set_misc(prob, misc): prob['misconceptions'] = misc

# ===================== BRONZE =====================
B = pb['bronze']

B[0]['guided_steps'] = [
    say("A solid pushing on a surface uses \\(p = \\dfrac{F}{A}\\). Force \\(F = 200\\) N, area \\(A = 0.04\\) m²."),
    box("The area is already in m², so write A = ", 0.04, "It is given as 0.04 m², no conversion needed."),
    box("p = 200 ÷ 0.04 = ", 5000, "Dividing by 0.04 is the same as multiplying by 25: 200 × 25.", phase="substitute"),
    box("Check: 5000 × 0.04 = ", 200, "Answer × area should return the 200 N force.", done="That returns the 200 N force, so 5000 Pa is right."),
]
set_misc(B[0], [m("inverse_error", "Pressure = force ÷ area = 200 ÷ 0.04 = 5000 Pa. Multiplying gives 8, which is far too small.", 8)])

B[1]['guided_steps'] = [
    say("Pressure in a liquid uses \\(p = h\\rho g\\). Depth \\(h = 2\\) m, density \\(\\rho = 1000\\) kg/m³, \\(g = 9.8\\) N/kg."),
    box("Multiply depth × density: 2 × 1000 = ", 2000, "Just 2 × 1000."),
    box("Now × g: 2000 × 9.8 = ", 19600, "2000 × 9.8: think 2000 × 10 = 20000, then take off 400.", phase="substitute"),
    box("Check: 19600 ÷ 9.8 ÷ 1000 = ", 2, "Undo the two multiplications to get the depth back.", done="That returns the 2 m depth, so 19,600 Pa is right."),
]
set_misc(B[1], [m("forgot_step", "Use p = hρg. Do not stop at h × ρ = 2000; multiply by g too: 2 × 1000 × 9.8 = 19,600 Pa.", 2000)])

B[2]['guided_steps'] = [
    say("Rearranged, \\(F = p \\times A\\). Pressure \\(p = 40000\\) Pa, area \\(A = 0.1\\) m²."),
    box("Write the area in m²: A = ", 0.1, "Given as 0.1 m² already."),
    box("F = 40000 × 0.1 = ", 4000, "Multiplying by 0.1 is dividing by 10.", phase="substitute"),
    box("Check: 4000 ÷ 0.1 = ", 40000, "Force ÷ area should give the pressure back.", done="That returns the 40,000 Pa, so 4000 N is right."),
]
set_misc(B[2], [m("inverse_error", "F = p × A = 40,000 × 0.1 = 4000 N. Dividing gives 400,000, which is the slip.", 400000)])

B[3]['guided_steps'] = [
    say("Solid on a surface: \\(p = \\dfrac{F}{A}\\). Weight \\(F = 500\\) N, area \\(A = 0.05\\) m²."),
    box("Area in m²: A = ", 0.05, "Given as 0.05 m²."),
    box("p = 500 ÷ 0.05 = ", 10000, "Dividing by 0.05 is multiplying by 20.", phase="substitute"),
    box("Check: 10000 × 0.05 = ", 500, "Answer × area should give the 500 N force.", done="Returns the 500 N weight, so 10,000 Pa is right."),
]
set_misc(B[3], [m("inverse_error", "p = F ÷ A = 500 ÷ 0.05 = 10,000 Pa. Multiplying gives 25, far too small.", 25)])

B[4]['guided_steps'] = [
    say("Liquid pressure: \\(p = h\\rho g\\). \\(h = 5\\) m, \\(\\rho = 1000\\) kg/m³, \\(g = 9.8\\)."),
    box("Multiply depth × density: 5 × 1000 = ", 5000, "5 × 1000."),
    box("Now × g: 5000 × 9.8 = ", 49000, "5000 × 9.8 = 5000 × 10 − 5000 × 0.2.", phase="substitute"),
    box("Check: 49000 ÷ 1000 ÷ 9.8 = ", 5, "Undo the multiplications to recover the depth.", done="Returns the 5 m depth, so 49,000 Pa is right."),
]
set_misc(B[4], [m("forgot_step", "Use p = hρg. Do not stop at 5 × 1000 = 5000; multiply by g: 5 × 1000 × 9.8 = 49,000 Pa.", 5000)])

B[5]['guided_steps'] = [
    say("Rearranged for area, \\(A = \\dfrac{F}{p}\\). Force \\(F = 600\\) N, pressure \\(p = 3000\\) Pa."),
    box("Write the pressure in Pa: p = ", 3000, "Given as 3000 Pa."),
    box("A = 600 ÷ 3000 = ", 0.2, "600 ÷ 3000 = 6 ÷ 30 = 0.2.", phase="substitute"),
    box("Check: 600 ÷ 0.2 = ", 3000, "Force ÷ area should give the pressure back.", done="Returns the 3000 Pa, so 0.2 m² is right."),
]
set_misc(B[5], [m("inverse_error", "A = F ÷ p = 600 ÷ 3000 = 0.2 m². Multiplying gives 1,800,000, which is impossible for an area.", 1800000)])

B[6]['guided_steps'] = [
    say("Rearranged for depth, \\(h = \\dfrac{p}{\\rho g}\\). \\(p = 29400\\) Pa, \\(\\rho = 1000\\), \\(g = 9.8\\)."),
    box("First work out ρ × g: 1000 × 9.8 = ", 9800, "1000 × 9.8."),
    box("h = 29400 ÷ 9800 = ", 3, "29400 ÷ 9800 = 294 ÷ 98 = 3.", phase="substitute"),
    box("Check: 3 × 9800 = ", 29400, "Depth × ρg should give the pressure back.", done="Returns the 29,400 Pa, so 3 m is right."),
]
set_misc(B[6], [m("wrong_rearrange", "h = p ÷ (ρg). Divide by both ρ AND g: 29,400 ÷ (1000 × 9.8) = 3 m. Dividing by 1000 only gives 29.4 m.", 29.4)])

B[7]['guided_steps'] = [
    say("\\(F = p \\times A\\). Pressure \\(p = 800\\) Pa, area \\(A = 0.5\\) m²."),
    box("Area in m²: A = ", 0.5, "Given as 0.5 m²."),
    box("F = 800 × 0.5 = ", 400, "Multiplying by 0.5 is halving.", phase="substitute"),
    box("Check: 400 ÷ 0.5 = ", 800, "Force ÷ area gives the pressure back.", done="Returns the 800 Pa, so 400 N is right."),
]
set_misc(B[7], [m("inverse_error", "F = p × A = 800 × 0.5 = 400 N. Dividing gives 1600, which is the slip.", 1600)])

# ===================== SILVER =====================
S = pb['silver']

S[0]['guided_steps'] = [
    say("Solid on a surface: \\(p = \\dfrac{F}{A}\\). The dimensions are in cm, so convert to metres first."),
    box("Convert 20 cm to metres (÷100): 20 ÷ 100 = ", 0.2, "Divide by 100."),
    box("Convert 50 cm to metres: 50 ÷ 100 = ", 0.5, "Divide by 100."),
    box("Area = 0.2 × 0.5 = ", 0.1, "Multiply the two sides in metres."),
    box("p = 300 ÷ 0.1 = ", 3000, "Dividing by 0.1 is × 10.", phase="substitute"),
    box("Check: 3000 × 0.1 = ", 300, "Answer × area gives the 300 N force.", done="Returns the 300 N, so 3000 Pa is right."),
]
set_misc(S[0], [m("unit_error", "Convert to metres first: 0.20 × 0.50 = 0.1 m², so p = 300 ÷ 0.1 = 3000 Pa. Using 20 × 50 = 1000 (cm²) gives 0.3, which is wrong.", 0.3)])

S[1]['guided_steps'] = [
    say("Liquid pressure: \\(p = h\\rho g\\). Use mercury's density, 13,600 kg/m³, not water. \\(h = 0.8\\) m."),
    box("Multiply depth × density: 0.8 × 13600 = ", 10880, "0.8 × 13600 = 8 × 1360."),
    box("Now × g: 10880 × 9.8 = ", 106624, "10880 × 9.8 = 10880 × 10 − 10880 × 0.2.", phase="substitute"),
    box("Check: 106624 ÷ 13600 ÷ 9.8 = ", 0.8, "Undo the multiplications to recover the height.", done="Returns the 0.8 m, so 106,624 Pa is right."),
]
set_misc(S[1], [m("wrong_density", "Use mercury's density 13,600 kg/m³, not water's 1000. p = 0.8 × 13,600 × 9.8 = 106,624 Pa. Using 1000 gives 7840.", 7840)])

S[2]['guided_steps'] = [
    say("Total pressure = atmospheric + liquid: \\(p = p_{atm} + h\\rho g\\). \\(h = 10\\) m, \\(\\rho = 1000\\), \\(g = 9.8\\)."),
    box("Liquid pressure, step 1: 10 × 1000 = ", 10000, "10 × 1000."),
    box("× g: 10000 × 9.8 = ", 98000, "10000 × 9.8."),
    box("Add atmospheric: 101000 + 98000 = ", 199000, "Add the 101,000 Pa of air pressure on top.", phase="substitute"),
    box("Check: 199000 − 101000 = ", 98000, "Subtract atmospheric to recover the liquid pressure.", done="That is the liquid pressure back, so 199,000 Pa total is right."),
]
set_misc(S[2], [m("forgot_atmospheric", "Liquid pressure = 10 × 1000 × 9.8 = 98,000 Pa. Add atmospheric: 101,000 + 98,000 = 199,000 Pa. Forgetting it leaves 98,000.", 98000)])

S[3]['guided_steps'] = [
    say("Solid on a surface: \\(p = \\dfrac{F}{A}\\). The area is in cm², so convert to m² first."),
    box("Convert 2 cm² to m² (÷10000): 2 ÷ 10000 = ", 0.0002, "1 m² = 10,000 cm², so divide by 10,000."),
    box("p = 50 ÷ 0.0002 = ", 250000, "50 ÷ 0.0002 = 50 × 5000.", phase="substitute"),
    box("Check: 250000 × 0.0002 = ", 50, "Answer × area gives the 50 N force.", done="Returns the 50 N force, so 250,000 Pa is right."),
]
set_misc(S[3], [m("wrong_conversion", "Convert cm² to m² by ÷10,000: 2 cm² = 0.0002 m². p = 50 ÷ 0.0002 = 250,000 Pa. Dividing by 100 instead gives 2500.", 2500)])

S[4]['guided_steps'] = [
    say("Rearranged for density, \\(\\rho = \\dfrac{p}{hg}\\). \\(p = 34300\\) Pa, \\(h = 3.5\\) m, \\(g = 9.8\\)."),
    box("First work out h × g: 3.5 × 9.8 = ", 34.3, "3.5 × 9.8."),
    box("ρ = 34300 ÷ 34.3 = ", 1000, "34300 ÷ 34.3 = 1000.", phase="substitute"),
    box("Check: 1000 × 34.3 = ", 34300, "Density × hg should give the pressure back.", done="Returns the 34,300 Pa, so 1000 kg/m³ is right."),
]
set_misc(S[4], [m("wrong_rearrange", "ρ = p ÷ (hg) = 34,300 ÷ (3.5 × 9.8) = 34,300 ÷ 34.3 = 1000 kg/m³. Dividing by h only (forgetting g) gives 9800.", 9800)])

S[5]['guided_steps'] = [
    say("Pressure difference uses the depth difference in \\(p = h\\rho g\\). \\(\\Delta h = 8 − 3\\)."),
    box("Depth difference: 8 − 3 = ", 5, "The extra depth between the two points."),
    box("× density: 5 × 1000 = ", 5000, "5 × 1000."),
    box("× g: 5000 × 9.8 = ", 49000, "5000 × 9.8.", phase="substitute"),
    box("Check: 49000 ÷ 9.8 ÷ 1000 = ", 5, "Undo the multiplications to recover the depth difference.", done="Returns the 5 m difference, so 49,000 Pa is right."),
]
set_misc(S[5], [m("forgot_step", "Use the depth difference: Δh = 8 − 3 = 5 m. Δp = 5 × 1000 × 9.8 = 49,000 Pa. Using 8 m instead of the difference gives 78,400.", 78400)])

# ===================== GOLD =====================
G = pb['gold']

G[0]['hint'] = "Find the liquid pressure with hρg (seawater density 1025), then add atmospheric pressure."
G[1]['hint'] = "Work out the weight first, then divide by the smallest face for maximum pressure."
G[2]['hint'] = "Find the pressure at 40 m with hρg, then multiply by the gate area."
G[3]['hint'] = "Find the fluid pressure from the small piston, then multiply by the large piston's area."
G[4]['hint'] = "Rearrange to h = p over ρg, using oil's density 800."
G[5]['hint'] = "Add atmospheric to the liquid pressure, then divide by 1000 for kPa."

G[0]['guided_steps'] = [
    say("Total pressure = atmospheric + liquid. Use seawater density 1025 kg/m³. \\(h = 25\\) m, \\(g = 9.8\\)."),
    box("Liquid pressure, step 1: 25 × 1025 = ", 25625, "25 × 1025."),
    box("× g: 25625 × 9.8 = ", 251125, "25625 × 9.8."),
    box("Add atmospheric: 101000 + 251125 = ", 352125, "Add the 101,000 Pa of air on the surface.", phase="substitute"),
    box("Check: 352125 − 101000 = ", 251125, "Subtract atmospheric to recover the liquid pressure.", done="That is the liquid pressure back, so 352,125 Pa is right."),
]
set_misc(G[0], [
    m("forgot_atmospheric", "Liquid pressure = 25 × 1025 × 9.8 = 251,125 Pa. Total = 101,000 + 251,125 = 352,125 Pa. Forgetting atmospheric leaves 251,125.", 251125),
    m("wrong_density", "Use seawater 1025 kg/m³, not fresh water 1000. Total = 101,000 + (25 × 1025 × 9.8) = 352,125 Pa. Using 1000 gives 346,000.", 346000),
])

G[1]['guided_steps'] = [
    say("Two steps: weight first, then pressure on the SMALLEST face for maximum pressure. \\(W = mg\\), then \\(p = \\dfrac{F}{A}\\)."),
    box("Weight: 20 × 9.8 = ", 196, "Mass × g."),
    box("Smallest face area (0.2 × 0.1): = ", 0.02, "The smallest face uses the two smallest sides: 0.2 × 0.1."),
    box("p = 196 ÷ 0.02 = ", 9800, "196 ÷ 0.02 = 196 × 50.", phase="substitute"),
    box("Check: 9800 × 0.02 = ", 196, "Answer × area gives the weight back.", done="Returns the 196 N weight, so 9800 Pa is right."),
]
set_misc(G[1], [
    m("wrong_area", "For MAXIMUM pressure use the SMALLEST face (0.2 × 0.1 = 0.02 m²): p = 196 ÷ 0.02 = 9800 Pa. Using the largest face (0.1 m²) gives 1960.", 1960),
    m("forgot_step", "The force is the weight, not the mass. Weight = 20 × 9.8 = 196 N, then p = 196 ÷ 0.02 = 9800 Pa. Using 20 N gives 1000 Pa.", 1000),
])

G[2]['guided_steps'] = [
    say("Two steps: pressure at 40 m, then force on the gate. \\(p = h\\rho g\\), then \\(F = pA\\). \\(\\rho = 1000\\)."),
    box("Pressure, step 1: 40 × 1000 = ", 40000, "40 × 1000."),
    box("× g: 40000 × 9.8 = ", 392000, "40000 × 9.8."),
    box("Gate area: 2 × 1.5 = ", 3, "Width × height."),
    box("Force: 392000 × 3 = ", 1176000, "Pressure × area.", phase="substitute"),
    box("Check: 1176000 ÷ 3 = ", 392000, "Force ÷ area gives the pressure at 40 m back.", done="Returns the pressure at 40 m, so 1,176,000 N is right."),
]
set_misc(G[2], [m("forgot_step", "Pressure at 40 m = 40 × 1000 × 9.8 = 392,000 Pa. Force = pressure × area = 392,000 × 3 = 1,176,000 N. Stopping at the pressure gives 392,000.", 392000)])

G[3]['guided_steps'] = [
    say("Pressure is the same throughout the fluid. Find it from the small piston, then apply it to the large one. \\(p = \\dfrac{F}{A}\\), then \\(F = pA\\)."),
    box("Pressure from small piston: 50 ÷ 0.002 = ", 25000, "50 ÷ 0.002 = 50 × 500."),
    box("Force on large piston: 25000 × 0.04 = ", 1000, "Same pressure × the larger area.", phase="substitute"),
    box("Check: 1000 ÷ 0.04 = ", 25000, "Large force ÷ large area gives the fluid pressure back.", done="Returns the fluid pressure, so 1000 N is right."),
]
set_misc(G[3], [
    m("forgot_step", "Pressure = 50 ÷ 0.002 = 25,000 Pa. Force on large piston = 25,000 × 0.04 = 1000 N. Stopping at the pressure leaves 25,000.", 25000),
    m("inverse_error", "The large piston has the LARGER area, so the force is MULTIPLIED: F = 50 × (0.04 ÷ 0.002) = 1000 N. Inverting the ratio gives 50 × 0.05 = 2.5.", 2.5),
])

G[4]['guided_steps'] = [
    say("Rearranged for depth, \\(h = \\dfrac{p}{\\rho g}\\). Use oil's density 800 kg/m³. \\(p = 101000\\) Pa, to 1 d.p."),
    box("First ρ × g: 800 × 9.8 = ", 7840, "800 × 9.8."),
    box("h = 101000 ÷ 7840 = ", 12.9, "101000 ÷ 7840 = 12.88, which rounds to 12.9.", post=" m (to 1 d.p.)", phase="substitute"),
    box("Check: 12.9 × 7840 = ", 101136, "Depth × ρg returns about the atmospheric pressure.", done="That is about 101,000 Pa (the small gap is rounding), so 12.9 m is right."),
]
set_misc(G[4], [
    m("wrong_rearrange", "h = p ÷ (ρg) = 101,000 ÷ (800 × 9.8) = 101,000 ÷ 7840 = 12.9 m. Dividing by ρ only (forgetting g) gives 126.3.", 126.3),
    m("wrong_density", "Use oil's density 800 kg/m³. h = 101,000 ÷ (800 × 9.8) = 12.9 m. Using water (1000) gives 10.3 m.", 10.3),
])

G[5]['guided_steps'] = [
    say("Total pressure, then convert to kPa. \\(p = p_{atm} + h\\rho g\\), then ÷1000. \\(h = 200\\) m, \\(\\rho = 1025\\), \\(g = 9.8\\)."),
    box("Liquid pressure, step 1: 200 × 1025 = ", 205000, "200 × 1025."),
    box("× g: 205000 × 9.8 = ", 2009000, "205000 × 9.8."),
    box("Add atmospheric: 101000 + 2009000 = ", 2110000, "Add the surface air pressure."),
    box("Convert to kPa (÷1000): 2110000 ÷ 1000 = ", 2110, "1 kPa = 1000 Pa, so divide by 1000.", phase="substitute"),
    box("Check: 2110 × 1000 = ", 2110000, "kPa × 1000 gives the total in Pa back.", done="That is the total in Pa, so 2110 kPa is right."),
]
set_misc(G[5], [
    m("forgot_atmospheric", "Liquid pressure = 200 × 1025 × 9.8 = 2,009,000 Pa. Total = 101,000 + 2,009,000 = 2,110,000 Pa = 2110 kPa. Forgetting atmospheric gives 2009 kPa.", 2009),
    m("unit_error", "Convert Pa to kPa by ÷1000: 2,110,000 Pa = 2110 kPa. Leaving it in Pa gives 2,110,000.", 2110000),
])

# ---- 5. tier descriptions ----
pb['bronze_description'] = "One pressure equation, values already in the right units (m, m², N, Pa). Pick p = F/A or p = hρg and substitute straight in."
pb['silver_description'] = "Convert units first (cm to m, cm² to m²) or rearrange the equation for the unknown before you substitute."
pb['gold_description'] = "Two steps chained: a weight or liquid pressure first, then add atmospheric pressure, work a hydraulic system, or convert the result."

# ---- 6. tier_guides ----
def stp(label, content, ans=False):
    d = {"label": label, "content": content}
    if ans: d["isAnswer"] = True; d["is_answer"] = True
    return d

pd['tier_guides'] = {
    "bronze": {
        "title": "Bronze: one equation, straight in",
        "steps": [
            "Pick the equation from the situation: a solid on a surface uses \\(p = \\frac{F}{A}\\); a liquid at a depth uses \\(p = h\\rho g\\).",
            "The values are already in the right units (m, m², N, Pa), so substitute straight in and calculate.",
            "State the answer with its unit (Pa, N, or m), then check by working backwards.",
        ],
        "example": {"question": "A 240 N box rests on the floor on an area of 0.6 m². Find the pressure.", "steps": [
            stp("Equation", "<p>Solid on a surface: \\(p = \\frac{F}{A}\\).</p>"),
            stp("Substitute", "<p>\\(p = \\frac{240}{0.6}\\)</p>"),
            stp("Check", "<p>\\(400 \\times 0.6 = 240\\) N ✓</p>"),
            stp("Answer", "<p><strong>400 Pa</strong></p>", ans=True),
        ]},
    },
    "silver": {
        "title": "Silver: convert or rearrange first",
        "steps": [
            "If lengths are in cm, convert before substituting: cm to m divide by 100, cm² to m² divide by 10,000.",
            "If the unknown is not the subject, rearrange first: \\(A = \\frac{F}{p}\\), \\(h = \\frac{p}{\\rho g}\\), \\(\\rho = \\frac{p}{hg}\\).",
            "Then substitute and calculate as in Bronze, and check backwards.",
        ],
        "example": {"question": "A force of 8 N acts on a 25 cm × 20 cm face. Find the pressure in Pa.", "steps": [
            stp("Convert", "<p>25 cm = 0.25 m, 20 cm = 0.20 m, so area = \\(0.25 \\times 0.20 = 0.05\\) m².</p>"),
            stp("Substitute", "<p>\\(p = \\frac{8}{0.05}\\)</p>"),
            stp("Check", "<p>\\(160 \\times 0.05 = 8\\) N ✓</p>"),
            stp("Answer", "<p><strong>160 Pa</strong></p>", ans=True),
        ]},
    },
    "gold": {
        "title": "Gold: two steps chained",
        "steps": [
            "Break the problem into two calculations. Common chains: weight then pressure, liquid pressure then force, or pressure then unit convert.",
            "For total pressure in a liquid, add atmospheric pressure (about 101,000 Pa) to \\(h\\rho g\\).",
            "Work the first step, feed its result into the second, then check backwards.",
        ],
        "example": {"question": "A diver is 15 m deep in fresh water (density 1000 kg/m³). Atmospheric pressure = 101,000 Pa. Find the total pressure. (g = 9.8 N/kg)", "steps": [
            stp("Liquid pressure", "<p>\\(h\\rho g = 15 \\times 1000 \\times 9.8 = 147{,}000\\) Pa</p>"),
            stp("Add atmospheric", "<p>\\(101{,}000 + 147{,}000\\)</p>"),
            stp("Check", "<p>\\(248{,}000 - 101{,}000 = 147{,}000\\) Pa ✓</p>"),
            stp("Answer", "<p><strong>248,000 Pa</strong></p>", ans=True),
        ]},
    },
}

# ---- 7. guided (opener + teach) ----
pd['guided'] = {
    "opener": {
        "label": "Before any equation",
        "display": ("An elephant weighs 40,000 N, spread over 0.4 m² of feet.<br>"
                    "A woman weighs 500 N, balanced on 0.0002 m² of heel tips.<br>"
                    "Who presses harder on each square metre of floor?"),
        "steps": [
            box("Elephant: 40000 ÷ 0.4 = ", 100000,
                "Share 40,000 N over 0.4 m²: 40000 ÷ 0.4.",
                say="No equation yet, just share each weight over its area. Elephant first:"),
            box("Woman: 500 ÷ 0.0002 = ", 2500000,
                "Share 500 N over a tiny 0.0002 m²: 500 ÷ 0.0002.",
                say="Now the stiletto, same idea:"),
            say("The woman, at 2,500,000 Pa against the elephant's 100,000 Pa. A slim heel can dent a wooden floor an elephant would not mark, because the same force squeezed through a tiny area makes huge pressure. That is exactly \\(p = \\dfrac{F}{A}\\): pressure is force ÷ area."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "Find the pressure at the bottom of a 3 m deep freshwater lake. Density of water = 1000 kg/m³. (g = 9.8 N/kg)",
            "label": "Together: your first one",
            "steps": [
                say("A liquid at a depth, so use \\(p = h\\rho g\\). Depth 3 m, density 1000, g = 9.8. Take it one multiply at a time."),
                box("Depth in metres: h = ", 3, "Given as 3 m."),
                box("Depth × density: 3 × 1000 = ", 3000, "3 × 1000."),
                box("Now × g: 3000 × 9.8 = ", 29400, "3000 × 9.8 = 3000 × 10 − 3000 × 0.2."),
                box("Check: 29400 ÷ 1000 ÷ 9.8 = ", 3, "Undo the multiplies to get the depth back.", done="Returns the 3 m depth, so 29,400 Pa is right."),
            ],
        },
        "silver": {
            "display": "A tile weighing 8 N rests flat on a 25 cm × 20 cm face. Find the pressure on the floor in Pa.",
            "label": "Together: the silver move",
            "steps": [
                say("Solid on a surface: \\(p = \\dfrac{F}{A}\\). The sides are in cm, so convert to metres before finding the area."),
                box("25 cm to m (÷100): 25 ÷ 100 = ", 0.25, "Divide by 100."),
                box("20 cm to m: 20 ÷ 100 = ", 0.2, "Divide by 100."),
                box("Area = 0.25 × 0.2 = ", 0.05, "Multiply the two sides."),
                box("p = 8 ÷ 0.05 = ", 160, "Dividing by 0.05 is × 20."),
                box("Check: 160 × 0.05 = ", 8, "Answer × area gives the 8 N force.", done="Returns the 8 N, so 160 Pa is right."),
            ],
        },
        "gold": {
            "display": "A diver is 15 m below the surface of a freshwater lake (density 1000 kg/m³). Atmospheric pressure = 101,000 Pa. Calculate the total pressure on the diver. (g = 9.8 N/kg)",
            "label": "Together: the gold move",
            "steps": [
                say("Two steps: liquid pressure with \\(p = h\\rho g\\), then add atmospheric. Build the liquid pressure one multiply at a time."),
                box("Depth × density: 15 × 1000 = ", 15000, "15 × 1000."),
                box("× g: 15000 × 9.8 = ", 147000, "15000 × 9.8."),
                box("Add atmospheric: 101000 + 147000 = ", 248000, "Add the surface air pressure."),
                box("Check: 248000 − 101000 = ", 147000, "Subtract atmospheric to recover the liquid pressure.", done="That is the liquid pressure back, so 248,000 Pa total is right."),
            ],
        },
    },
}

# ---- write ----
OUT = 'lesson_higher-calculations-L04@57e3210892.json'
io.open(OUT, 'w', encoding='utf-8').write(json.dumps(pd, ensure_ascii=False, indent=2))
print("written", OUT)

def words(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
print("method_card content words:", words(pd['method_card']['content']))
for t in ('bronze','silver','gold'):
    print(t, "tier_guide steps words:", sum(words(x) for x in pd['tier_guides'][t]['steps']))
