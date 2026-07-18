# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_canonical_raw.json", encoding="utf-8"))
pb = pd["problem_bank"]

# ---------------------------------------------------------------------------
# 1. BANK REPAIR + guided_steps + hints + expects, tier by tier
# ---------------------------------------------------------------------------

def gs_box(pre, ans, hint, post="", phase=False, done=None, say=None):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if phase: d["phase"] = "substitute"
    if done: d["done"] = done
    if say is not None: d["say"] = say
    return d

def gs_say(say):
    return {"say": say}

# --- BRONZE -----------------------------------------------------------------
bronze = pb["bronze"]

# B1 pool 2.0 m -> 19600 Pa
bronze[0]["hint"] = "Multiply depth, density and g: p = hρg."
bronze[0]["misconceptions"] = [{
    "pattern": "forgot_g", "check": "common", "expect": 2000,
    "message": "Remember the × g. p = hρg = 2.0 × 1000 × 9.8 = 19,600 Pa. Stopping at 2.0 × 1000 gives 2,000, which is only h × ρ."}]
bronze[0]["guided_steps"] = [
    gs_say("Fluid pressure is \\(p = h\\rho g\\). Multiply the three values in turn."),
    gs_box("Depth × density: 2.0 × 1000 = ", 2000, "Two times 1000."),
    gs_box("Now × g: 2000 × 9.8 = ", 19600, "2000 times 9.8.", phase=True),
    gs_box("Check by working back: 19600 ÷ (1000 × 9.8) = 19600 ÷ 9800 = ", 2, "Divide 19600 by 9800.", phase=True,
           done="That returns the 2.0 m depth, so the answer is 19,600 Pa."),
]

# B2 lake 5.0 m -> 49000 Pa
bronze[1]["hint"] = "Straight into p = hρg with the three values."
bronze[1]["misconceptions"] = [{
    "pattern": "forgot_g", "check": "common", "expect": 5000,
    "message": "p = hρg = 5.0 × 1000 × 9.8 = 49,000 Pa. Leaving off the g gives 5.0 × 1000 = 5,000, which is not a pressure."}]
bronze[1]["guided_steps"] = [
    gs_say("Fluid pressure is \\(p = h\\rho g\\)."),
    gs_box("Depth × density: 5.0 × 1000 = ", 5000, "Five times 1000."),
    gs_box("Now × g: 5000 × 9.8 = ", 49000, "5000 times 9.8.", phase=True),
    gs_box("Check: 49000 ÷ 9800 = ", 5, "Divide the pressure by ρg.", phase=True,
           done="Back to the 5.0 m depth, so the answer is 49,000 Pa."),
]

# B3 cube side 0.10 m -> upthrust 9.8 N
bronze[2]["hint"] = "Find the cube's volume (side cubed) first, then Upthrust = ρVg."
bronze[2]["misconceptions"] = [{
    "pattern": "wrong_volume", "check": "common", "expect": 980,
    "message": "Volume of the cube = side³ = 0.10³ = 0.001 m³, not 0.10. Upthrust = 1000 × 0.001 × 9.8 = 9.8 N. Using 0.10 as the volume gives 980 N."}]
bronze[2]["guided_steps"] = [
    gs_say("Upthrust \\(= \\rho V g\\). First find the cube's volume."),
    gs_box("Volume = side³ = 0.10 × 0.10 × 0.10 = ", 0.001, "0.1 cubed: 0.1×0.1 = 0.01, then ×0.1 = 0.001."),
    gs_box("Upthrust = 1000 × 0.001 × 9.8. First 1000 × 0.001 = ", 1, "A thousand times one thousandth.", phase=True),
    gs_box("Now × g: 1 × 9.8 = ", 9.8, "One times 9.8.", phase=True),
    gs_box("Check: 9.8 ÷ 9.8 ÷ 1000 = ", 0.001, "Divide back by g then by density.", phase=True,
           done="Returns the volume 0.001 m³, so the upthrust is 9.8 N."),
]

# B4 submarine 50 m fresh -> total 591000 Pa
bronze[3]["hint"] = "Work out the fluid pressure hρg, then add atmospheric pressure on top."
bronze[3]["misconceptions"] = [{
    "pattern": "forgot_atm", "check": "common", "expect": 490000,
    "message": "That is only the fluid pressure. Total pressure adds atmospheric: 490,000 + 101,000 = 591,000 Pa."}]
bronze[3]["guided_steps"] = [
    gs_say("Total pressure = atmospheric + fluid: \\(p_{total} = p_{atm} + h\\rho g\\)."),
    gs_box("Fluid pressure first: 50 × 1000 = ", 50000, "Fifty times 1000."),
    gs_box("Now × g: 50000 × 9.8 = ", 490000, "50000 times 9.8."),
    gs_box("Add atmospheric: 490000 + 101000 = ", 591000, "Add on the 101,000.", phase=True),
    gs_box("Check the fluid part: 591000 − 101000 = ", 490000, "Take the atmospheric part back off.", phase=True,
           done="That is the fluid pressure we found, so the total is 591,000 Pa."),
]

# B5 depth from pressure -> 19.9 m
bronze[4]["hint"] = "Rearrange to h = p ÷ (ρg)."
bronze[4]["misconceptions"] = [{
    "pattern": "forgot_g", "check": "common", "expect": 195.12,
    "message": "Divide by ρg, not just ρ. h = 200000 ÷ (1025 × 9.8) = 200000 ÷ 10045 = 19.9 m. Dividing by 1025 alone gives about 195 m."}]
bronze[4]["guided_steps"] = [
    gs_say("Rearrange \\(p = h\\rho g\\) to find depth: \\(h = \\dfrac{p}{\\rho g}\\)."),
    gs_box("Work out ρg first: 1025 × 9.8 = ", 10045, "Density times g."),
    gs_box("Divide (to 2 d.p.): 200000 ÷ 10045 = ", 19.91, "Pressure divided by ρg.", phase=True),
    gs_box("Sense check: at roughly 100,000 Pa per 10 m, 200,000 Pa is about 200000 ÷ 100000 = 2 lots of 10 m, so ≈ ",
           20, "Roughly double 10 m.", phase=True,
           done="About 20 m, matching our 19.9 m. Answer: 19.9 m."),
]

# --- SILVER -----------------------------------------------------------------
silver = pb["silver"]

# S1 diver 40 m sea -> total 502800 Pa
silver[0]["hint"] = "Fluid pressure hρg first, then add atmospheric pressure."
silver[0]["misconceptions"] = [{
    "pattern": "forgot_atm", "check": "common", "expect": 401800,
    "message": "That is the fluid pressure only. Total = 401,800 + 101,000 = 502,800 Pa."}]
silver[0]["guided_steps"] = [
    gs_say("Total pressure = atmospheric + fluid: \\(p_{total} = p_{atm} + h\\rho g\\)."),
    gs_box("Fluid pressure: 40 × 1025 = ", 41000, "Forty times 1025."),
    gs_box("Now × g: 41000 × 9.8 = ", 401800, "41000 times 9.8."),
    gs_box("Add atmospheric: 401800 + 101000 = ", 502800, "Add on the 101,000.", phase=True),
    gs_box("Check: 502800 − 101000 = ", 401800, "Take the atmospheric part back off.", phase=True,
           done="Matches the fluid pressure, so the total is 502,800 Pa."),
]

# S2 ball -> net 1.96 N (FIX 1.97 -> 1.96)
silver[1]["solutions"] = [1.96]
silver[1]["hint"] = "Find upthrust and weight separately, then subtract."
silver[1]["misconceptions"] = [{
    "pattern": "forgot_step", "check": "common", "expect": 4.9,
    "message": "That is the upthrust. The net force also needs the weight subtracted: 4.9 − 2.94 = 1.96 N upward."}]
silver[1]["guided_steps"] = [
    gs_say("Net force = upthrust − weight. Work out each one."),
    gs_box("Upthrust = ρVg = 1000 × 0.0005 × 9.8. First 1000 × 0.0005 = ", 0.5, "A thousand times five ten-thousandths."),
    gs_box("Now × g: 0.5 × 9.8 = ", 4.9, "Half of 9.8.", phase=True),
    gs_box("Weight = 0.30 × 9.8 = ", 2.94, "Mass times g.", phase=True),
    gs_box("Net upward force = 4.9 − 2.94 = ", 1.96, "Subtract weight from upthrust.", phase=True,
           done="Upthrust beats weight by 1.96 N, so the ball is pushed up. Answer: 1.96 N upward."),
]

# S3 density from upthrust -> 1000 kg/m3
silver[2]["hint"] = "Rearrange to ρ = upthrust ÷ (Vg). The mass is not needed."
silver[2]["misconceptions"] = [{
    "pattern": "forgot_step", "check": "common", "expect": 9800,
    "message": "Divide by Vg, not V alone. ρ = 3.92 ÷ (4.0×10⁻⁴ × 9.8) = 1000 kg/m³. Dividing by V only gives 9,800."}]
silver[2]["guided_steps"] = [
    gs_say("Rearrange Upthrust \\(= \\rho V g\\) for density: \\(\\rho = \\dfrac{\\text{upthrust}}{V g}\\). The mass is a distractor."),
    gs_box("Work out Vg: 0.0004 × 9.8 = ", 0.00392, "Volume times g."),
    gs_box("Divide: 3.92 ÷ 0.00392 = ", 1000, "Upthrust divided by Vg.", phase=True),
    gs_box("Check: 1000 × 0.00392 = ", 3.92, "Multiply density by Vg to get the upthrust back.", phase=True,
           done="Returns the 3.92 N upthrust, so the density is 1000 kg/m³ (fresh water)."),
]

# S4 hydraulic press -> 25000 Pa
silver[3]["hint"] = "Pressure uses the piston the force acts on: p = F ÷ A, the small piston area."
silver[3]["misconceptions"] = [{
    "pattern": "wrong_area", "check": "common", "expect": 500,
    "message": "Use the piston the force acts on (the small one). p = 50 ÷ 0.002 = 25,000 Pa. Using the large area 0.10 gives 500 Pa."}]
silver[3]["guided_steps"] = [
    gs_say("Pressure transmitted uses the piston the force acts on: \\(p = \\dfrac{F}{A}\\). The large piston area is a distractor."),
    gs_box("Area the 50 N pushes on is the small piston: A = ", 0.002, "The force is applied to the small piston."),
    gs_box("Pressure = 50 ÷ 0.002 = ", 25000, "Fifty divided by 0.002.", phase=True),
    gs_box("Check: 25000 × 0.002 = ", 50, "Multiply pressure by the small area to get the force back.", phase=True,
           done="Returns the 50 N force, so the pressure is 25,000 Pa."),
]

# S5 fish -> net 0.245 N (FIX 0.6 -> 0.245)
silver[4]["solutions"] = [0.245]
silver[4]["hint"] = "Upthrust minus weight gives the net force; state the direction."
silver[4]["misconceptions"] = [{
    "pattern": "forgot_step", "check": "common", "expect": 2.009,
    "message": "That is the upthrust. Subtract the weight too: 2.009 − 1.764 = 0.245 N upward."}]
silver[4]["guided_steps"] = [
    gs_say("Net force = upthrust − weight. Work out both."),
    gs_box("Upthrust = ρVg = 1025 × 0.0002 × 9.8. First 1025 × 0.0002 = ", 0.205, "1025 times two ten-thousandths."),
    gs_box("Now × g: 0.205 × 9.8 = ", 2.009, "0.205 times 9.8.", phase=True),
    gs_box("Weight = 0.18 × 9.8 = ", 1.764, "Mass times g.", phase=True),
    gs_box("Net force = 2.009 − 1.764 = ", 0.245, "Subtract weight from upthrust.", phase=True,
           done="Upthrust is a little larger, so the net force is 0.245 N upward: the fish tends to rise. Answer: 0.245 N upward."),
]

# --- GOLD -------------------------------------------------------------------
gold = pb["gold"]

# G1 Mariana Trench -> total 110596000 Pa (FIX 110456000 -> 110596000)
gold[0]["solutions"] = [110596000]
gold[0]["hint"] = "Fluid pressure hρg is huge here; add the small atmospheric pressure at the end."
gold[0]["misconceptions"] = [{
    "pattern": "forgot_atm", "check": "common", "expect": 110495000,
    "message": "Fluid pressure = 11000 × 1025 × 9.8 = 110,495,000 Pa. Total = 110,495,000 + 101,000 = 110,596,000 Pa. At this depth atmospheric pressure barely matters."}]
gold[0]["guided_steps"] = [
    gs_say("Total pressure = atmospheric + fluid: \\(p_{total} = p_{atm} + h\\rho g\\). The fluid term is enormous here."),
    gs_box("Fluid: 11000 × 1025 = ", 11275000, "Eleven thousand times 1025."),
    gs_box("Now × g: 11275000 × 9.8 = ", 110495000, "Multiply by 9.8."),
    gs_box("Add atmospheric: 110495000 + 101000 = ", 110596000, "Add on the 101,000.", phase=True),
    gs_box("See how small the atmospheric part is: 110596000 − 110495000 = ", 101000, "Subtract the fluid part.", phase=True,
           done="Just 101,000 Pa out of 110 million, so atmospheric barely matters. Answer: 110,596,000 Pa (about 1.11 × 10⁸ Pa)."),
]

# G2 hollow sphere -> net 20.8 N upward (FIX 20.3 -> 20.8)
gold[1]["solutions"] = [20.8]
gold[1]["hint"] = "Upthrust minus weight; a positive result means the net force is upward."
gold[1]["misconceptions"] = [{
    "pattern": "forgot_step", "check": "common", "expect": 50.2,
    "message": "That is the upthrust alone. Net force = upthrust − weight = 50.2 − 29.4 = 20.8 N upward."}]
gold[1]["guided_steps"] = [
    gs_say("Net force = upthrust − weight, then say which way it acts."),
    gs_box("Upthrust = ρVg = 1025 × 0.005 × 9.8. First 1025 × 0.005 = ", 5.125, "1025 times five thousandths."),
    gs_box("Now × g: 5.125 × 9.8 = ", 50.225, "5.125 times 9.8.", phase=True),
    gs_box("Weight = 3.0 × 9.8 = ", 29.4, "Mass times g.", phase=True),
    gs_box("Net = 50.225 − 29.4 = ", 20.825, "Subtract weight from upthrust.", phase=True,
           done="Upthrust wins, so the net force is about 20.8 N upward: the sphere rises. Answer: 20.8 N upward."),
]

# G3 barge draught -> 3.0 m (FIX 0.306 -> 3.0)
gold[2]["solutions"] = [3.0]
gold[2]["hint"] = "Floating means upthrust = weight, so V = m ÷ ρ, then draught = V ÷ area."
gold[2]["misconceptions"] = [{
    "pattern": "forgot_step", "check": "common", "expect": 60,
    "message": "60 m³ is the submerged volume, not the depth. Divide by the base area: draught = 60 ÷ 20 = 3.0 m."}]
gold[2]["guided_steps"] = [
    gs_say("Floating means upthrust = weight. The g cancels, leaving \\(\\rho V_{sub} = m\\). Find the submerged volume, then the depth."),
    gs_box("Submerged volume V = m ÷ ρ = 60000 ÷ 1000 = ", 60, "Mass divided by water density."),
    gs_box("Draught = volume ÷ base area = 60 ÷ 20 = ", 3, "Spread that volume over 20 m².", phase=True),
    gs_box("Check the weight: 60000 × 9.8 = ", 588000, "Mass times g.", phase=True),
    gs_box("Check the upthrust: 1000 × 60 × 9.8 = ", 588000, "Density × submerged volume × g.", phase=True,
           done="Upthrust 588,000 N equals the weight 588,000 N, so it floats at a draught of 3.0 m."),
]

# G4 block in mercury -> upthrust 79.97 N, floats
gold[3]["hint"] = "Upthrust = ρVg using mercury's density; compare with the block's weight."
gold[3]["misconceptions"] = [{
    "pattern": "wrong_density", "check": "common", "expect": 49,
    "message": "Upthrust uses the fluid's density (mercury), not the block. Upthrust = 13600 × 0.0006 × 9.8 = 79.97 N. Using the block's mass gives its weight, 49 N, which is a different quantity."}]
gold[3]["guided_steps"] = [
    gs_say("Upthrust \\(= \\rho V g\\) with the mercury density, then compare with the block's weight."),
    gs_box("Upthrust = 13600 × 0.0006 × 9.8. First 13600 × 0.0006 = ", 8.16, "13600 times six ten-thousandths."),
    gs_box("Now × g: 8.16 × 9.8 = ", 79.968, "8.16 times 9.8.", phase=True),
    gs_box("Weight of block = 5.0 × 9.8 = ", 49, "Mass times g.", phase=True),
    gs_box("Compare: 79.968 ÷ 49 = ", 1.632, "Divide upthrust by weight.", phase=True,
           done="Upthrust is over 1.6× the weight, so the block floats high on the dense mercury. Answer: upthrust ≈ 79.97 N, floats."),
]

# ---------------------------------------------------------------------------
# 2. FIGURE LABEL FIXES (question SVG typos)
# ---------------------------------------------------------------------------
def fix_q(prob, old, new):
    assert old in prob["question"], "missing: " + old
    prob["question"] = prob["question"].replace(old, new)

fix_q(gold[1], ">3.0 kg kg<", ">3.0 kg<")
fix_q(gold[3], ">5.0 kg kg<", ">5.0 kg<")
fix_q(silver[2], ">W = 0.50 kg N<", ">m = 0.50 kg<")
fix_q(bronze[2], ">W = W N<", ">Weight<")
fix_q(bronze[2], "V = 0.001 m³\n(0.1×0.1×0.1) m³", "V = 0.001 m³")

# ---------------------------------------------------------------------------
# 3. tier descriptions
# ---------------------------------------------------------------------------
pb["bronze_description"] = "One equation, values already in the right units. Substitute straight into p = hρg or Upthrust = ρVg."
pb["silver_description"] = "Rearrange the equation first, add atmospheric pressure, or find upthrust and weight then combine them."
pb["gold_description"] = "Multi-step problems: chain upthrust with a floating condition, or work through very large or awkward numbers."

# ---------------------------------------------------------------------------
# 4. tier_guides
# ---------------------------------------------------------------------------
pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one equation, straight in",
   "steps": [
     "Pick the equation: fluid pressure uses \\(p = h\\rho g\\); upthrust uses Upthrust \\(= \\rho V g\\).",
     "Check the units are base ones: depth in m, density in kg/m³, volume in m³.",
     "Substitute and multiply. State the answer with its unit: Pa for pressure, N for upthrust."
   ],
   "example": {
     "question": "A tank of water is 3.0 m deep. Density = 1000 kg/m³, g = 9.8 N/kg. Find the pressure at the bottom.",
     "steps": [
       {"label": "Write the equation", "content": "<p>\\(p = h\\rho g\\)</p>"},
       {"label": "Substitute", "content": "<p>\\(p = 3.0 \\times 1000 \\times 9.8\\)</p>"},
       {"label": "Check the units", "content": "<p>Depth in m, density in kg/m³, g in N/kg: all base units.</p>"},
       {"label": "Answer", "content": "<p><strong>29,400 Pa</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 },
 "silver": {
   "title": "Silver: rearrange or add a step",
   "steps": [
     "Rearrange when needed: depth \\(h = \\dfrac{p}{\\rho g}\\); density \\(\\rho = \\dfrac{\\text{upthrust}}{V g}\\).",
     "For total pressure at depth, add atmospheric: \\(p_{total} = p_{atm} + h\\rho g\\).",
     "For floating or sinking, find upthrust and weight separately, then take the difference."
   ],
   "example": {
     "question": "A point is 10 m down in sea water (density 1025 kg/m³, g = 9.8 N/kg). Atmospheric pressure = 101,000 Pa. Find the total pressure.",
     "steps": [
       {"label": "Write the equation", "content": "<p>\\(p_{total} = p_{atm} + h\\rho g\\)</p>"},
       {"label": "Substitute", "content": "<p>\\(p_{total} = 101{,}000 + 10 \\times 1025 \\times 9.8\\)</p>"},
       {"label": "Check", "content": "<p>Fluid part = 100,450 Pa, then add the atmospheric 101,000 Pa.</p>"},
       {"label": "Answer", "content": "<p><strong>201,450 Pa</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 },
 "gold": {
   "title": "Gold: chain the steps",
   "steps": [
     "Break the problem into stages: an upthrust often feeds into a floating condition or a net force.",
     "When an object floats, upthrust equals weight; use \\(\\rho V_{sub} = m\\) to find a volume or depth.",
     "Keep large numbers tidy, and always finish with the unit and, for forces, the direction."
   ],
   "example": {
     "question": "A raft of mass 800 kg floats in fresh water (density 1000 kg/m³). Find the submerged volume.",
     "steps": [
       {"label": "Floating condition", "content": "<p>Upthrust = weight, so \\(\\rho V_{sub} g = mg\\), giving \\(\\rho V_{sub} = m\\).</p>"},
       {"label": "Rearrange", "content": "<p>\\(V_{sub} = \\dfrac{m}{\\rho} = \\dfrac{800}{1000}\\)</p>"},
       {"label": "Check", "content": "<p>Upthrust = 1000 × 0.80 × 9.8 = 7,840 N = weight 800 × 9.8.</p>"},
       {"label": "Answer", "content": "<p><strong>0.80 m³</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 }
}

# ---------------------------------------------------------------------------
# 5. guided (opener + teach walks)
# ---------------------------------------------------------------------------
pd["guided"] = {
 "opener": {
   "display": "Picture a stack of identical books on a table. Each book weighs 15 N.",
   "steps": [
     gs_say("The table holds the whole pile, but each book only feels the weight of the ones stacked above it."),
     gs_box("Put 3 books in the pile. The bottom book has all three pressing down: 3 × 15 = ", 45, "Three books, 15 N each.", post="N"),
     gs_box("Now make it 6 books. The bottom feels 6 × 15 = ", 90, "Six books this time.", post="N"),
     gs_say("Deeper in the pile means more weight pressing down. Water is the same: the deeper you go, the more fluid is stacked above, so the pressure climbs. That is exactly \\(p = h\\rho g\\): pressure grows with depth h, with the fluid's density ρ, and with g.")
   ]
 },
 "teach": {
   "bronze": {
     "display": "A storage tank holds oil 4.0 m deep. Oil density = 900 kg/m³, g = 9.8 N/kg. Find the pressure at the base, then at twice the depth.",
     "steps": [
       gs_say("Fluid pressure is \\(p = h\\rho g\\). Multiply depth, density and g."),
       gs_box("Depth × density: 4.0 × 900 = ", 3600, "Four times 900."),
       gs_box("Now × g: 3600 × 9.8 = ", 35280, "3600 times 9.8. That is the pressure at 4.0 m."),
       gs_box("At 8.0 m (twice as deep): 8.0 × 900 × 9.8 = ", 70560, "Same sum with 8.0 instead of 4.0."),
       gs_box("Compare the two: 70560 ÷ 35280 = ", 2, "Divide the deeper pressure by the shallower one.",
              done="Double the depth, double the pressure. That is p = hρg in action.")
     ]
   },
   "silver": {
     "display": "A submersible sits at 25 m in sea water (density 1025 kg/m³, g = 9.8 N/kg). Atmospheric pressure = 101,000 Pa. Find the total pressure.",
     "steps": [
       gs_say("Total pressure has two parts: the fluid above, plus the air pressing down on the surface. \\(p_{total} = p_{atm} + h\\rho g\\)."),
       gs_box("Fluid pressure: 25 × 1025 = ", 25625, "Twenty-five times 1025."),
       gs_box("Now × g: 25625 × 9.8 = ", 251125, "25625 times 9.8. That is the fluid pressure."),
       gs_box("Add atmospheric: 251125 + 101000 = ", 352125, "Add on the 101,000."),
       gs_box("How much did the air add? 352125 − 251125 = ", 101000, "Subtract the fluid part.",
              done="Exactly atmospheric pressure, the part people forget for total pressure.")
     ]
   },
   "gold": {
     "display": "A sealed drum of volume 0.20 m³ and mass 150 kg is held fully under fresh water (density 1000 kg/m³, g = 9.8 N/kg). Find the net force when it is released, and its direction.",
     "steps": [
       gs_say("Two forces act: upthrust up, weight down. Work out each, then subtract."),
       gs_box("Upthrust = ρVg = 1000 × 0.20 × 9.8. First 1000 × 0.20 = ", 200, "A thousand times 0.20."),
       gs_box("Now × g: 200 × 9.8 = ", 1960, "200 times 9.8. That is the upthrust in N."),
       gs_box("Weight = 150 × 9.8 = ", 1470, "Mass times g."),
       gs_box("Net force = 1960 − 1470 = ", 490, "Subtract weight from upthrust.",
              done="Upthrust wins by 490 N, so the drum accelerates upward and bobs to the surface.")
     ]
   }
 }
}

# ---------------------------------------------------------------------------
# 6. slim method_card
# ---------------------------------------------------------------------------
pd["method_card"] = {
 "title": "Fluid Pressure and Upthrust",
 "steps": [
   "Choose the equation: fluid pressure p = hρg, or upthrust = ρVg.",
   "Check units are base: depth in m, density in kg/m³, volume in m³.",
   "Substitute and calculate. For total pressure, add atmospheric pressure.",
   "State the answer with its unit (Pa or N) and, for forces, the direction."
 ],
 "content": "<p>Two calculations in this lesson.</p><p><strong>Fluid pressure:</strong> \\(p = h\\rho g\\), with depth h in m, density ρ in kg/m³ and g in N/kg. For the total pressure at depth, add atmospheric pressure: \\(p_{total} = p_{atm} + h\\rho g\\).</p><p><strong>Upthrust:</strong> \\(\\text{Upthrust} = \\rho_{fluid} V g\\), where V is the submerged volume and ρ is the fluid's density, not the object's. If upthrust exceeds the weight the object rises; if it is less, it sinks; equal means it floats in balance.</p>"
}

# ---------------------------------------------------------------------------
# 7. Fix pre-existing em dashes (worked_examples labels, exam_context)
# ---------------------------------------------------------------------------
pd["exam_context"]["frequency"] = "Moderate. Fluid pressure and upthrust appear regularly in higher-tier physics."
for we in pd["worked_examples"]:
    for st in we["steps"]:
        st["label"] = st["label"].replace(" — ", ": ")
        st["content"] = st["content"].replace(" — ", ", ")

# ---------------------------------------------------------------------------
# 8. Make question SVGs validator-compliant (role, aria-label; drop xmlns http)
# ---------------------------------------------------------------------------
ARIA = {
 ("bronze", 0): "Water tank 2.0 m deep with pressure at the base",
 ("bronze", 1): "Lake 5.0 m deep showing fluid pressure at depth",
 ("bronze", 2): "Cube submerged in fresh water showing upthrust",
 ("bronze", 3): "Submarine at 50 m depth, total pressure",
 ("bronze", 4): "Water column of unknown depth with a pressure gauge",
 ("silver", 0): "Diver at 40 m depth in sea water, total pressure",
 ("silver", 1): "Ball submerged in water with upthrust and weight arrows",
 ("silver", 2): "Object in an unknown liquid with upthrust and weight arrows",
 ("silver", 3): "Hydraulic press with small and large pistons",
 ("silver", 4): "Fish submerged in sea water with upthrust and weight arrows",
 ("gold", 0): "Deep-sea sensor at 11,000 m in the Mariana Trench",
 ("gold", 1): "Hollow sphere in sea water with upthrust and weight arrows",
 ("gold", 2): "Barge floating in water showing its draught",
 ("gold", 3): "Block in mercury with upthrust and weight arrows",
}
for tier in ("bronze", "silver", "gold"):
    for i, prob in enumerate(pb[tier]):
        q = prob.get("question")
        if not q or "<svg" not in q:
            continue
        q = q.replace(' xmlns="http://www.w3.org/2000/svg"', '')
        label = ARIA[(tier, i)]
        q = q.replace('<svg viewBox=', '<svg role="img" aria-label="%s" viewBox=' % label, 1)
        assert 'http://' not in q and 'https://' not in q, "residual http in %s[%d]" % (tier, i)
        prob["question"] = q

# ---------------------------------------------------------------------------
json.dump(pd, io.open("lesson_higher-calculations-L02@b3c8bb1c4f.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written")
