# -*- coding: utf-8 -*-
# physics-calculations-L05@c30ee7c879 : Density, SHC and Latent Heat
import json, io

pd = json.load(io.open('_mine_L05_c30e_canon.json', encoding='utf-8'))

# ---------- 1. Em-dash fixes (punctuation only, validator-fatal) ----------
def fix_dash(s):
    if not isinstance(s, str) or '—' not in s:
        return s
    for n in ('1','2','3','4','5'):
        s = s.replace('Step %s — ' % n, 'Step %s: ' % n)
    s = s.replace(' — ', ', ').replace('—', ', ')
    return s
def deep_fix(o):
    if isinstance(o, dict):
        return {k: deep_fix(v) for k, v in o.items()}
    if isinstance(o, list):
        return [deep_fix(v) for v in o]
    return fix_dash(o)
pd = deep_fix(pd)

# ---------- 2. Slim method_card (board-neutral, <=140 words, <=4 steps) ----------
pd['method_card'] = {
    "title": "Density, SHC and Latent Heat",
    "steps": [
        "Decide what is happening: density, a temperature change (SHC), or a state change (latent heat).",
        "Write the equation: \\(\\rho = m/V\\), \\(\\Delta E = mc\\Delta\\theta\\), or \\(E = mL\\).",
        "Convert units first: grams to kilograms, cm³ to m³, minutes to seconds, and use the temperature change, not the final temperature.",
        "Substitute, calculate, and state the unit. If it heats AND changes state, add two calculations."
    ],
    "content": ("<p>Three equations: <strong>density</strong> \\(\\rho = m/V\\), "
        "<strong>specific heat capacity</strong> \\(\\Delta E = mc\\Delta\\theta\\), and "
        "<strong>latent heat</strong> \\(E = mL\\). Check which of these your board gives you "
        "and which you need to recall.</p>"
        "<p>Use SHC when the temperature changes, latent heat when the state changes (melting "
        "or boiling), and both added together when a substance heats up and then changes state. "
        "During a state change the temperature stays constant.</p>"
        "<p>Convert grams to kilograms before substituting, and watch volume units: cm³ and "
        "m³ give different density units. Temperature change means final minus initial.</p>")
}

pb = pd['problem_bank']
pb['bronze_description'] = "One equation, all values already in kg, m³ and °C. Pick density, SHC or latent heat and substitute straight in."
pb['silver_description'] = "Convert grams to kilograms (or cm³ to m³) first, or rearrange the equation before you substitute."
pb['gold_description'] = "Chain two steps: heat and change state, or work back from a heater's power and time to find c or L."

# ---------- 4. hints ----------
hints = {
 'bronze': [
   "Density is mass divided by volume, both already in base units.",
   "Rearrange to mass = density × volume.",
   "Find the temperature change first, then multiply m × c × Δθ.",
   "Temperature change is 100 − 20, then m × c × Δθ.",
   "State change, so energy = mass × latent heat.",
   "Boiling is a state change: energy = mass × latent heat of vaporisation.",
   "A state change at constant temperature uses latent heat.",
   "Density is mass divided by volume.",
 ],
 'silver': [
   "Convert 400 g to kg, find Δθ, then convert the answer to kJ.",
   "Rearrange to Δθ = energy ÷ (m × c).",
   "Convert the density to g/cm³, then volume = mass ÷ density.",
   "Find the rise with Δθ = energy ÷ (m × c), then add the start temperature.",
   "Convert 250 g to kg, then energy = mass × latent heat.",
   "Keep grams and cm³: density = mass ÷ volume.",
 ],
 'gold': [
   "Melt the ice, warm the water, then add the two energies.",
   "Heat the water to 100°C, boil it, then add the two energies.",
   "Convert the time to seconds, find energy with P × t, then L = energy ÷ mass.",
   "The volume is the water rise; convert mass and volume to base units first.",
   "Convert time to seconds, find energy with P × t, then c = energy ÷ (m × Δθ).",
   "Energy lost by the water = melting energy + warming energy of the melted ice.",
 ],
}
for tier, hs in hints.items():
    for i, h in enumerate(hs):
        pb[tier][i]['hint'] = h

# ---------- 5. expects ----------
expects = {
 ('bronze',2,0): 135000, ('bronze',3,0): 1260000,
 ('silver',3,1): 79.6, ('silver',4,0): 83500000, ('silver',5,0): 2700,
 ('gold',3,1): 1500, ('gold',4,0): 10, ('gold',5,0): 100800,
}
for tier in ('bronze','silver','gold'):
    for pi, prob in enumerate(pb[tier]):
        for mi, m in enumerate(prob.get('misconceptions', [])):
            m['expect'] = expects.get((tier, pi, mi), None)

# ---------- 6. guided_steps ----------
DEG = "°"; MU = "Δθ"; TIMES = "×"; DIV = "÷"; MINUS = "−"
def b(pre, answer, hint, post="", say=None, done=None, phase=False):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase: d["phase"] = "substitute"
    return d
def s(say): return {"say": say}
RHO = "\\(\\rho = \\frac{m}{V}\\)"
SHC = "\\(\\Delta E = mc\\Delta\\theta\\)"
MDL = "\\(E = mL\\)"

walks = {
 ('bronze',0): [
   s("Density is mass shared over volume: %s. Both values are already in kg and m³, so go straight in." % RHO),
   b("Mass in kg, m = ", 3.9, "It is given in kg already: 3.9."),
   b("Volume in m³, V = ", 0.0005, "Given in m³ already: 0.0005."),
   b("Now divide: 3.9 ÷ 0.0005 = ", 7800, "Dividing by 0.0005 is the same as × 2000.", phase=True),
   b("Check by multiplying back: 7800 × 0.0005 = ", 3.9, "7800 × 0.0005 should return the original mass.", done="Back to the mass we started with, so the density is 7800 kg/m³."),
   s("So \\(\\rho = 7800\\) kg/m³."),
 ],
 ('bronze',1): [
   s("Density and volume are given, and we want the mass. Rearrange %s to \\(m = \\rho V\\)." % RHO),
   b("Density in kg/m³, ρ = ", 800, "Given: 800."),
   b("Volume in m³, V = ", 0.002, "Given: 0.002."),
   b("Multiply: 800 × 0.002 = ", 1.6, "800 × 0.002 = 800 ÷ 500.", phase=True),
   b("Check with the original equation: 1.6 ÷ 0.002 = ", 800, "Mass ÷ volume should give back 800.", done="That returns the density, so the mass is 1.6 kg."),
   s("So \\(m = 1.6\\) kg."),
 ],
 ('bronze',2): [
   s("Heating with no state change means specific heat capacity: %s. First find the temperature change." % SHC),
   b("Temperature change Δθ = 75 − 25 = ", 50, "Final minus start: 75 − 25."),
   b("Mass in kg, m = ", 2, "Given in kg: 2."),
   b("Substitute and multiply: 2 × 900 × 50 = ", 90000, "2 × 900 = 1800, then × 50.", phase=True),
   b("Check: 90000 ÷ (2 × 900) = 90000 ÷ 1800 = ", 50, "Energy ÷ (m × c) returns the temperature change.", done="Back to the 50°C change, so the energy is 90,000 J."),
   s("So \\(\\Delta E = 90{,}000\\) J."),
 ],
 ('bronze',3): [
   s("Temperature is changing, so use SHC: %s. Find the change first." % SHC),
   b("Δθ = 100 − 20 = ", 80, "Final minus start: 100 − 20."),
   b("Mass in kg, m = ", 3, "Given in kg: 3."),
   b("Multiply: 3 × 4200 × 80 = ", 1008000, "3 × 4200 = 12600, then × 80.", phase=True),
   b("Check: 1008000 ÷ (3 × 4200) = 1008000 ÷ 12600 = ", 80, "Energy ÷ (m × c) returns the temperature change.", done="Back to the 80°C change, so the energy is 1,008,000 J."),
   s("So \\(\\Delta E = 1{,}008{,}000\\) J."),
 ],
 ('bronze',4): [
   s("Melting is a state change, so use latent heat: %s. No temperature change here." % MDL),
   b("Mass in kg, m = ", 0.5, "Given in kg: 0.5."),
   b("Latent heat of fusion, L = ", 334000, "The value given: 334,000."),
   b("Multiply: 0.5 × 334000 = ", 167000, "Half of 334,000.", phase=True),
   b("Check: 167000 ÷ 0.5 = ", 334000, "Energy ÷ mass returns the latent heat.", done="Back to L, so the energy is 167,000 J."),
   s("So \\(E = 167{,}000\\) J."),
 ],
 ('bronze',5): [
   s("Boiling is a state change, so use latent heat: %s. Use the vaporisation value." % MDL),
   b("Mass in kg, m = ", 0.1, "Given in kg: 0.1."),
   b("Latent heat of vaporisation, L = ", 2260000, "Given: 2,260,000."),
   b("Multiply: 0.1 × 2260000 = ", 226000, "One tenth of 2,260,000.", phase=True),
   b("Check: 226000 ÷ 0.1 = ", 2260000, "Energy ÷ mass returns the latent heat.", done="Back to L, so the energy is 226,000 J."),
   s("So \\(E = 226{,}000\\) J."),
 ],
 ('bronze',7): [
   s("Density is mass over volume: %s. Both units are already base units." % RHO),
   b("Mass in kg, m = ", 0.15, "Given in kg: 0.15."),
   b("Volume in m³, V = ", 0.00005, "Given in m³: 0.00005."),
   b("Divide: 0.15 ÷ 0.00005 = ", 3000, "0.15 ÷ 0.00005 = 0.15 × 20000.", phase=True),
   b("Check: 3000 × 0.00005 = ", 0.15, "Density × volume returns the mass.", done="Back to the mass, so the density is 3000 kg/m³."),
   s("So \\(\\rho = 3000\\) kg/m³."),
 ],
 ('silver',0): [
   s("Temperature is changing, so SHC: %s. The mass is in grams and the answer is wanted in kJ, so convert carefully." % SHC),
   b("Convert mass to kg: 400 ÷ 1000 = ", 0.4, "Grams to kilograms: divide by 1000."),
   b("Temperature change Δθ = 118 − 18 = ", 100, "Final minus start: 118 − 18."),
   b("Energy in joules: 0.4 × 385 × 100 = ", 15400, "0.4 × 385 = 154, then × 100.", phase=True),
   b("Convert to kJ: 15400 ÷ 1000 = ", 15.4, "Joules to kilojoules: divide by 1000.", done="15.4 kJ, matching the answer wanted in kilojoules."),
   s("So \\(\\Delta E = 15.4\\) kJ."),
 ],
 ('silver',1): [
   s("Energy and mass are given, and we want the temperature rise. Rearrange %s to \\(\\Delta\\theta = \\frac{\\Delta E}{mc}\\)." % SHC),
   b("First work out m × c: 2 × 4200 = ", 8400, "Multiply mass by specific heat capacity."),
   b("Energy supplied, ΔE = ", 50400, "Given in joules: 50,400."),
   b("Divide: 50400 ÷ 8400 = ", 6, "50400 ÷ 8400.", phase=True),
   b("Check: 2 × 4200 × 6 = ", 50400, "m × c × Δθ should return the energy.", done="Back to the 50,400 J supplied, so the rise is 6°C."),
   s("So \\(\\Delta\\theta = 6\\)°C."),
 ],
 ('silver',2): [
   s("We want the volume, so rearrange %s to \\(V = \\frac{m}{\\rho}\\). The mass is in grams, so convert the density to grams per cm³ to match." % RHO),
   b("Convert density to g/cm³: 19300 ÷ 1000 = ", 19.3, "1000 kg/m³ = 1 g/cm³, so divide by 1000."),
   b("Mass in grams, m = ", 9.65, "Given in grams: 9.65."),
   b("Volume: 9.65 ÷ 19.3 = ", 0.5, "9.65 ÷ 19.3 = 0.5.", phase=True),
   b("Check: 19.3 × 0.5 = ", 9.65, "Density × volume returns the mass.", done="Back to the 9.65 g mass, so the volume is 0.5 cm³."),
   s("So \\(V = 0.5\\) cm³."),
 ],
 ('silver',3): [
   s("Find the temperature rise first, then add the starting temperature. Rearrange to \\(\\Delta\\theta = \\frac{\\Delta E}{mc}\\)."),
   b("Work out m × c: 2.5 × 4200 = ", 10500, "Mass × specific heat capacity."),
   b("Energy, ΔE = ", 836000, "Given: 836,000 J."),
   b("Temperature rise (to 1 d.p.): 836000 ÷ 10500 = ", 79.6, "836000 ÷ 10500 = 79.6 to 1 d.p.", phase=True),
   b("Add the start temperature: 15 + 79.6 = ", 94.6, "Final temperature = start + rise.", done="94.6°C, the final temperature, not just the rise."),
   s("So the final temperature is \\(94.6\\)°C."),
 ],
 ('silver',4): [
   s("Melting is a state change: %s. The mass is in grams, so convert first." % MDL),
   b("Convert mass to kg: 250 ÷ 1000 = ", 0.25, "Grams to kilograms: divide by 1000."),
   b("Latent heat of fusion, L = ", 334000, "Given: 334,000 J/kg."),
   b("Multiply: 0.25 × 334000 = ", 83500, "A quarter of 334,000.", phase=True),
   b("Check: 83500 ÷ 0.25 = ", 334000, "Energy ÷ mass returns the latent heat.", done="Back to L, so the energy is 83,500 J."),
   s("So \\(E = 83{,}500\\) J."),
 ],
 ('silver',5): [
   s("The question asks for g/cm³, so keep grams and cm³ as they are: %s." % RHO),
   b("Mass in grams, m = ", 162, "Given in grams: 162."),
   b("Volume in cm³, V = ", 60, "Given in cm³: 60."),
   b("Divide: 162 ÷ 60 = ", 2.7, "162 ÷ 60 = 2.7.", phase=True),
   b("Check: 2.7 × 60 = ", 162, "Density × volume returns the mass.", done="Back to the 162 g mass, so the density is 2.7 g/cm³."),
   s("So \\(\\rho = 2.7\\) g/cm³."),
 ],
 ('gold',0): [
   s("Two things happen: the ice melts, then the water warms up. Do each and add. Melting uses %s; warming uses %s." % (MDL, SHC)),
   b("Step 1, melt the ice: 0.3 × 334000 = ", 100200, "m × L = 0.3 × 334,000."),
   b("Step 2, temperature change of the water: 40 − 0 = ", 40, "Final minus start: 40 − 0."),
   b("Step 2, warm the water: 0.3 × 4200 × 40 = ", 50400, "0.3 × 4200 = 1260, then × 40."),
   b("Add the two energies: 100200 + 50400 = ", 150600, "Melting energy plus warming energy.", phase=True),
   b("Check the melting share: 150600 − 50400 = ", 100200, "Total minus the warming part returns the melting part.", done="Back to the melting energy, so the total is 150,600 J."),
   s("So the total energy is \\(150{,}600\\) J."),
 ],
 ('gold',1): [
   s("Two steps: heat the water to boiling, then boil it. Warming uses %s; boiling uses %s." % (SHC, MDL)),
   b("Temperature change: 100 − 20 = ", 80, "Final minus start: 100 − 20."),
   b("Step 1, heat the water: 0.5 × 4200 × 80 = ", 168000, "0.5 × 4200 = 2100, then × 80."),
   b("Step 2, boil the water: 0.5 × 2260000 = ", 1130000, "m × L = 0.5 × 2,260,000."),
   b("Add the two energies: 168000 + 1130000 = ", 1298000, "Heating energy plus boiling energy.", phase=True),
   b("Check the boiling share: 1298000 − 168000 = ", 1130000, "Total minus the heating part returns the boiling part.", done="Back to the boiling energy, so the total is 1,298,000 J."),
   s("So the total energy is \\(1{,}298{,}000\\) J."),
 ],
 ('gold',2): [
   s("First find the energy the heater supplied with \\(E = Pt\\), then use %s to get the latent heat. Convert the time to seconds first." % MDL),
   b("Convert time to seconds: 8 × 60 + 20 = ", 500, "8 minutes is 480 s, plus 20 s."),
   b("Energy supplied: 50 × 500 = ", 25000, "Power × time = 50 × 500."),
   b("Rearrange \\(E = mL\\) to \\(L = E/m\\): 25000 ÷ 0.5 = ", 50000, "Energy ÷ mass = 25,000 ÷ 0.5.", phase=True),
   b("Check: 0.5 × 50000 = ", 25000, "m × L should return the energy.", done="Back to the 25,000 J supplied, so L = 50,000 J/kg."),
   s("So the specific latent heat of fusion is \\(50{,}000\\) J/kg."),
 ],
 ('gold',3): [
   s("The volume of the object is how much the water rose. Then convert to base units and use %s." % RHO),
   b("Volume from the water rise: 80 − 50 = ", 30, "The object pushes the level up: 80 − 50."),
   b("Convert mass to kg: 120 ÷ 1000 = ", 0.12, "Grams to kilograms: divide by 1000."),
   b("Convert volume to m³: 30 ÷ 1000000 = ", 0.00003, "1 cm³ = 1 × 10⁻⁶ m³, so divide by a million."),
   b("Divide: 0.12 ÷ 0.00003 = ", 4000, "0.12 ÷ 0.00003.", phase=True),
   b("Check: 4000 × 0.00003 = ", 0.12, "Density × volume returns the mass.", done="Back to the 0.12 kg mass, so the density is 4000 kg/m³."),
   s("So \\(\\rho = 4000\\) kg/m³."),
 ],
 ('gold',4): [
   s("Find the energy with \\(E = Pt\\), then use %s rearranged to \\(c = \\frac{\\Delta E}{m\\Delta\\theta}\\). Convert the time first." % SHC),
   b("Convert time to seconds: 2 × 60 = ", 120, "2 minutes × 60."),
   b("Energy supplied: 40 × 120 = ", 4800, "Power × time = 40 × 120."),
   b("Temperature change: 30 − 20 = ", 10, "Final minus start: 30 − 20."),
   b("Divide: 4800 ÷ (0.8 × 10) = 4800 ÷ 8 = ", 600, "m × Δθ = 8, then 4800 ÷ 8.", phase=True),
   b("Check: 0.8 × 600 × 10 = ", 4800, "m × c × Δθ should return the energy.", done="Back to the 4800 J supplied, so c = 600 J/(kg°C)."),
   s("So the specific heat capacity is \\(600\\) J/(kg°C)."),
 ],
 ('gold',5): [
   s("Energy lost by the warm water equals energy gained by the ice as it melts and then warms. Set them equal and solve for L."),
   b("Water cools by: 25 − 21 = ", 4, "The warm water drops from 25 to 21."),
   b("Energy lost by the water: 0.3 × 4200 × 4 = ", 5040, "m × c × Δθ = 0.3 × 4200 × 4."),
   b("Energy to warm the melted ice from 0 to 21: 0.05 × 4200 × 21 = ", 4410, "The melted ice warms up: 0.05 × 4200 × 21."),
   b("Energy left for melting: 5040 − 4410 = ", 630, "Total gained minus the warming part.", phase=True),
   b("Latent heat: 630 ÷ 0.05 = ", 12600, "Melting energy ÷ mass of ice = 630 ÷ 0.05.", done="L = 12,600 J/kg, the estimate for the ice."),
   s("So the specific latent heat of fusion is about \\(12{,}600\\) J/kg."),
 ],
}
for (tier, idx), gs in walks.items():
    pb[tier][idx]['guided_steps'] = gs

# ---------- 7. tier_guides ----------
pd['tier_guides'] = {
 "bronze": {
   "title": "Bronze: one equation, straight in",
   "steps": [
     "Decide which equation fits: density \\(\\rho = m/V\\), specific heat \\(\\Delta E = mc\\Delta\\theta\\), or latent heat \\(E = mL\\).",
     "The values are already in kg, m³ and °C, so substitute straight in. For a temperature change, use final minus start.",
     "Calculate and state the unit."
   ],
   "example": {
     "question": "A copper block has mass 8.9 kg and volume 0.001 m³. Find its density.",
     "steps": [
       {"label": "Equation", "content": "<p>\\(\\rho = \\frac{m}{V}\\)</p>"},
       {"label": "Substitute", "content": "<p>\\(\\rho = \\frac{8.9}{0.001}\\)</p>"},
       {"label": "Check", "content": "<p>\\(8900 \\times 0.001 = 8.9\\) ✓</p>"},
       {"label": "Answer", "content": "<p>\\(\\rho = 8900\\) <strong>kg/m³</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 },
 "silver": {
   "title": "Silver: convert or rearrange first",
   "steps": [
     "The values are not in base units, or the unknown is not on its own. Convert grams to kg (÷ 1000) and cm³ to m³ before substituting.",
     "If you need mass, volume, c or a temperature, rearrange the equation first, then substitute.",
     "Calculate and state the unit."
   ],
   "example": {
     "question": "A 200 g iron block is heated from 15°C to 65°C. SHC of iron = 450 J/(kg°C). Find the energy.",
     "steps": [
       {"label": "Convert", "content": "<p>200 g ÷ 1000 = 0.2 kg</p>"},
       {"label": "Substitute", "content": "<p>\\(\\Delta E = 0.2 \\times 450 \\times 50 = 4500\\) J</p>"},
       {"label": "Check", "content": "<p>\\(4500 \\div (0.2 \\times 450) = 50\\)°C ✓</p>"},
       {"label": "Answer", "content": "<p>\\(\\Delta E = 4500\\) <strong>J</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 },
 "gold": {
   "title": "Gold: chain two steps",
   "steps": [
     "Some questions need two calculations: heat a substance (\\(\\Delta E = mc\\Delta\\theta\\)) and change its state (\\(E = mL\\)), then add the energies.",
     "Others give power and time: find the energy with \\(E = Pt\\), then rearrange to get c or L.",
     "Work each part in full, keep the units, and add or divide only at the end."
   ],
   "example": {
     "question": "Total energy to melt 0.4 kg of ice at 0°C then heat the water to 50°C. \\(L_f\\) = 334,000 J/kg, c = 4200 J/(kg°C).",
     "steps": [
       {"label": "Melt", "content": "<p>\\(E_1 = mL = 0.4 \\times 334000 = 133600\\) J</p>"},
       {"label": "Heat", "content": "<p>\\(E_2 = mc\\Delta\\theta = 0.4 \\times 4200 \\times 50 = 84000\\) J</p>"},
       {"label": "Check", "content": "<p>\\(217600 - 84000 = 133600\\) ✓</p>"},
       {"label": "Answer", "content": "<p>Total = 133600 + 84000 = <strong>217600 J</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 }
}

# ---------- 8. guided (opener + teach) ----------
pd['guided'] = {
 "opener": {
   "label": "Before any equations",
   "display": "A 4 cm³ lump of metal has a mass of 12 g.<br>A smaller 1 cm³ piece of the SAME metal...",
   "steps": [
     b("The same metal, just a quarter of the size. So 1 cm³ has a mass of ", 3,
       "A quarter of the size means a quarter of the mass: 12 ÷ 4.", post=" g",
       say="No equations yet, just common sense. Four cm³ weighs 12 g."),
     b("That 3 grams per cm³ is the metal's density. A 10 cm³ block of it would weigh ", 30,
       "10 lots of 3 grams.", post=" g",
       say="Each cm³ carries the same 3 g. Density just means mass per unit of volume."),
     s("You just found density: mass shared out per cm³. Written as an equation that is \\(\\rho = \\frac{m}{V}\\); you divided 12 by 4 to get 3 g/cm³. Specific heat capacity and latent heat work the same way, using an equation your board may give you."),
   ]
 },
 "teach": {
   "bronze": {
     "display": "A copper block has a mass of 8.9 kg and a volume of 0.001 m³. Calculate its density.",
     "label": "Together: your first one",
     "steps": [
       s("Density is mass over volume: %s. Both values are already in base units." % RHO),
       b("Mass in kg, m = ", 8.9, "Given in kg: 8.9."),
       b("Volume in m³, V = ", 0.001, "Given in m³: 0.001."),
       b("Divide: 8.9 ÷ 0.001 = ", 8900, "Dividing by 0.001 is the same as × 1000.", phase=True),
       b("Check: 8900 × 0.001 = ", 8.9, "Density × volume returns the mass.", done="Back to the mass, so the density is right."),
       s("So \\(\\rho = 8900\\) kg/m³."),
     ]
   },
   "silver": {
     "display": "A 200 g block of iron is heated from 15°C to 65°C. The SHC of iron is 450 J/(kg°C). Calculate the energy transferred.",
     "label": "Together: convert first",
     "steps": [
       s("Temperature is changing, so SHC: %s. The mass is in grams, so convert before substituting." % SHC),
       b("Convert mass to kg: 200 ÷ 1000 = ", 0.2, "Grams to kilograms: divide by 1000."),
       b("Temperature change Δθ = 65 − 15 = ", 50, "Final minus start: 65 − 15."),
       b("Substitute: 0.2 × 450 × 50 = ", 4500, "0.2 × 450 = 90, then × 50.", phase=True),
       b("Check: 4500 ÷ (0.2 × 450) = 4500 ÷ 90 = ", 50, "Energy ÷ (m × c) returns the temperature change.", done="Back to the 50°C change, so the energy is right."),
       s("So \\(\\Delta E = 4500\\) J."),
     ]
   },
   "gold": {
     "display": "Calculate the total energy needed to melt 0.4 kg of ice at 0°C and then heat the water to 50°C. SHC of water = 4200 J/(kg°C), \\(L_f\\) = 334,000 J/kg.",
     "label": "Together: two steps",
     "steps": [
       s("Two steps: melt the ice, then warm the water. Melting uses %s; warming uses %s. Add them." % (MDL, SHC)),
       b("Step 1, melt the ice: 0.4 × 334000 = ", 133600, "m × L = 0.4 × 334,000."),
       b("Step 2, temperature change: 50 − 0 = ", 50, "Final minus start: 50 − 0."),
       b("Step 2, warm the water: 0.4 × 4200 × 50 = ", 84000, "0.4 × 4200 = 1680, then × 50."),
       b("Add the two energies: 133600 + 84000 = ", 217600, "Melting energy plus warming energy.", phase=True),
       b("Check the melting share: 217600 − 84000 = ", 133600, "Total minus the warming part returns the melting part.", done="Back to the melting energy, so the total is 217,600 J."),
       s("So the total energy is \\(217{,}600\\) J."),
     ]
   }
 }
}

io.open('lesson_physics-calculations-L05@c30ee7c879.json', 'w', encoding='utf-8').write(
    json.dumps(pd, ensure_ascii=False, indent=1))
print("built OK")
