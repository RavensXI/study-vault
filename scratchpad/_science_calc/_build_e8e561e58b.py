# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_d9384cf5.json", encoding="utf-8"))

MINUS = "−"  # −

# ---- preserve + em-dash-fix worked_examples ----
we = live["worked_examples"]
for ex in we:
    for st in ex["steps"]:
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ": ")

exam_context = {
    "marks": "2–4 per calculation",
    "paper": "Physics paper",
    "frequency": "Medium: typically 1–2 questions per paper",
}

topic_links = live.get("topic_links", {"prerequisites": []})
related_videos = live.get("related_videos", [])

# ---- method_card (slim, board-neutral, no em dash) ----
method_card = {
    "title": "Density, Specific Heat Capacity and Latent Heat",
    "content": ("<p>Three equations, three traps.</p>"
        "<p><strong>Density:</strong> \\(\\rho = m \\div V\\). Keep units consistent: g with cm³, or kg with m³.</p>"
        "<p><strong>Heating:</strong> \\(\\Delta E = mc\\Delta\\theta\\). Use the temperature <em>change</em> (final "
        + MINUS + " initial), never the final temperature.</p>"
        "<p><strong>Change of state:</strong> \\(E = mL\\). Temperature stays constant while melting or boiling, and the "
        "vaporisation latent heat is far larger than fusion.</p>"
        "<p>Check whether your board gives you these equations or expects them from memory.</p>"),
    "steps": [
        "Choose the equation: density \\(\\rho = m/V\\), heating \\(\\Delta E = mc\\Delta\\theta\\), or change of state \\(E = mL\\).",
        "Convert units if needed, and use the temperature change, not the final temperature.",
        "Substitute the values and calculate.",
        "State the answer with its unit.",
    ],
}

# ---- helper for steps ----
def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase is not None: d["phase"] = phase
    if done is not None: d["done"] = done
    return d
def sayonly(say):
    return {"say": say}

# =====================================================================
# BRONZE
# =====================================================================
bronze = [
 {  # B1 density direct 2.7
  "unit": "g/cm³",
  "display": "A block of material has a mass of 540 g and a volume of 200 cm³. Calculate its density in g/cm³.",
  "solutions": [2.7], "accept": 0.05, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "equation_hint": "\\(\\rho = m \\div V\\)",
  "hint": "Density is mass divided by volume; the units already match.",
  "misconceptions": [
   {"pattern": "inverse_error", "check": "common", "expect": 0.37,
    "message": "Density is mass ÷ volume: 540 ÷ 200 = 2.7 g/cm³. Dividing the other way (200 ÷ 540) gives 0.37, which is upside down."}],
  "guided_steps": [
   sayonly("Density is mass ÷ volume: \\(\\rho = m \\div V\\). Mass is in grams and volume in cm³, a matching pair, so nothing to convert."),
   box("Read off the volume you will divide by. V = ", 200, "It is given directly as 200 cm³."),
   box("Now divide: 540 ÷ 200 = ", 2.7, "A calculator gives 2.7.", phase="substitute"),
   box("Check by multiplying back: 2.7 × 200 = ", 540, "Density × volume should return the mass.", phase="substitute",
       done="That returns the original 540 g, so the density is 2.7 g/cm³.")]},
 {  # B2 rearrange volume 200
  "unit": "cm³",
  "display": "A material has a mass of 600 g and a density of 3 g/cm³. Calculate its volume in cm³.",
  "solutions": [200], "accept": 1, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "equation_hint": "\\(V = m \\div \\rho\\)",
  "hint": "Rearrange to volume = mass ÷ density.",
  "misconceptions": [
   {"pattern": "wrong_rearrange", "check": "common", "expect": 1800,
    "message": "Volume = mass ÷ density: 600 ÷ 3 = 200 cm³. Multiplying instead (600 × 3) gives 1800, which is far too big."}],
  "guided_steps": [
   sayonly("You want volume, so rearrange \\(\\rho = m \\div V\\) into \\(V = m \\div \\rho\\)."),
   box("Read off the density you will divide by. ρ = ", 3, "It is given as 3 g/cm³."),
   box("Now divide: 600 ÷ 3 = ", 200, "600 shared into 3.", phase="substitute"),
   box("Check: density × volume should give the mass, 3 × 200 = ", 600, "3 × 200 should return the mass.", phase="substitute",
       done="That returns 600 g, so the volume is 200 cm³.")]},
 {  # B3 temperature change 45
  "unit": "°C",
  "display": "A 2 kg aluminium block (c = 900 J/kg/°C) is heated from 20 °C to 65 °C. What is the temperature change?",
  "solutions": [45], "accept": 0.5, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "equation_hint": "Δθ = final temperature " + MINUS + " initial temperature",
  "hint": "Temperature change is final minus initial.",
  "misconceptions": [
   {"pattern": "final_temp", "check": "common", "expect": 65,
    "message": "The temperature change is final " + MINUS + " initial = 65 " + MINUS + " 20 = 45 °C. Writing 65 uses the final temperature instead of the change."}],
  "guided_steps": [
   sayonly("Temperature change means final − initial: \\(\\Delta\\theta = \\theta_{final} - \\theta_{initial}\\)."),
   box("Write the final temperature. final = ", 65, "The block ends at 65 °C."),
   box("Subtract the start: 65 " + MINUS + " 20 = ", 45, "Take the initial 20 away.", phase="substitute"),
   box("Check it is a rise: 45 + 20 = ", 65, "The change plus the start should give the final temperature.", phase="substitute",
       done="45 + 20 returns the final 65 °C, so the change is 45 °C, not 65 °C.")]},
 {  # B4 SHC energy 81000
  "unit": "J",
  "display": "Calculate the energy needed to heat the 2 kg aluminium block (c = 900 J/kg/°C) by 45 °C.",
  "solutions": [81000], "accept": 100, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "equation_hint": "\\(\\Delta E = mc\\Delta\\theta\\)",
  "hint": "Multiply mass, SHC and the temperature change together.",
  "misconceptions": [
   {"pattern": "final_temp", "check": "common", "expect": 117000,
    "message": "Use the temperature change (45 °C), not a final temperature: \\(\\Delta E\\) = 2 × 900 × 45 = 81,000 J. Using 65 °C gives 117,000 J."}],
  "guided_steps": [
   sayonly("Thermal energy uses \\(\\Delta E = mc\\Delta\\theta\\), with mass in kg (it is already 2 kg)."),
   box("Multiply mass by SHC first: 2 × 900 = ", 1800, "kg times J/kg/°C."),
   box("Now multiply by the temperature change: 1800 × 45 = ", 81000, "1800 lots of 45.", phase="substitute"),
   box("Check by dividing back: 81000 ÷ 45 = ", 1800, "Energy ÷ Δθ should give mc.", phase="substitute",
       done="That returns 2 × 900 = 1800, so the energy is 81,000 J.")]},
 {  # B5 latent fusion 66800
  "unit": "J",
  "display": "How much energy is needed to melt 0.2 kg of ice? (Specific latent heat of fusion of water = 334,000 J/kg)",
  "solutions": [66800], "accept": 100, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "equation_hint": "\\(E = m \\times L\\)",
  "hint": "Energy to melt = mass × latent heat of fusion.",
  "misconceptions": [
   {"pattern": "wrong_L", "check": "common", "expect": 452000,
    "message": "Melting uses the latent heat of fusion (334,000 J/kg): E = 0.2 × 334,000 = 66,800 J. Using the vaporisation value (2,260,000) gives 452,000 J."}],
  "guided_steps": [
   sayonly("Melting is a change of state, so use latent heat: \\(E = m \\times L\\), mass in kg (0.2 kg)."),
   box("Write the latent heat of fusion. L = ", 334000, "334,000 J/kg, given in the question."),
   box("Multiply: 0.2 × 334000 = ", 66800, "A fifth of 334,000.", phase="substitute"),
   box("Check: 66800 ÷ 334000 = ", 0.2, "Energy ÷ L should return the mass.", phase="substitute",
       done="That returns the 0.2 kg mass, so the energy is 66,800 J.")]},
 {  # B6 unit conversion 2700
  "unit": "kg/m³",
  "display": "Convert a density of 2.7 g/cm³ to kg/m³.",
  "solutions": [2700], "accept": 10, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "equation_hint": "Multiply by 1,000 to convert g/cm³ to kg/m³",
  "hint": "Multiply by 1,000 to turn g/cm³ into kg/m³.",
  "misconceptions": [
   {"pattern": "unit_error", "check": "common", "expect": 0.0027,
    "message": "To go from g/cm³ to kg/m³ you multiply by 1,000: 2.7 × 1,000 = 2,700 kg/m³. Dividing by 1,000 (0.0027) goes the wrong way."}],
  "guided_steps": [
   sayonly("1 g/cm³ = 1,000 kg/m³, so to convert g/cm³ to kg/m³ you multiply by 1,000."),
   box("Write the factor you multiply by. factor = ", 1000, "1 g/cm³ = 1,000 kg/m³."),
   box("Multiply: 2.7 × 1000 = ", 2700, "Move the decimal three places right.", phase="substitute"),
   box("Check by dividing back: 2700 ÷ 1000 = ", 2.7, "Dividing by 1,000 undoes the conversion.", phase="substitute",
       done="That returns 2.7 g/cm³, so the density is 2,700 kg/m³.")]},
]

# =====================================================================
# SILVER
# =====================================================================
silver = [
 {  # S1 cooling copper 173250
  "unit": "J",
  "display": "A 3 kg copper block (c = 385 J/kg/°C) is cooled from 200 °C to 50 °C. Calculate the energy released.",
  "solutions": [173250], "accept": 100, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "equation_hint": "\\(\\Delta E = mc\\Delta\\theta\\). Δθ = 200 " + MINUS + " 50",
  "hint": "Find the temperature change first, then use mcΔθ.",
  "misconceptions": [
   {"pattern": "final_temp", "check": "common", "expect": 231000,
    "message": "Use the temperature change 200 " + MINUS + " 50 = 150 °C, not a single temperature: \\(\\Delta E\\) = 3 × 385 × 150 = 173,250 J. Using 200 °C gives 231,000 J."}],
  "guided_steps": [
   sayonly("Cooling still uses \\(\\Delta E = mc\\Delta\\theta\\). First find the temperature change."),
   box("Temperature change: 200 " + MINUS + " 50 = ", 150, "Final take away initial; ignore the direction."),
   box("Multiply mass by SHC: 3 × 385 = ", 1155, "3 lots of 385.", phase="substitute"),
   box("Now multiply by the change: 1155 × 150 = ", 173250, "1155 times 150.", phase="substitute"),
   box("Check: 173250 ÷ 150 = ", 1155, "Energy ÷ Δθ should give mc.", phase="substitute",
       done="That returns 3 × 385 = 1155, so the energy released is 173,250 J.")]},
 {  # S2 heat water 504000
  "unit": "J",
  "display": "How much energy is needed to heat 1.5 kg of water from 20 °C to 100 °C? (c of water = 4,200 J/kg/°C)",
  "solutions": [504000], "accept": 500, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "equation_hint": "\\(\\Delta E = mc\\Delta\\theta\\). Δθ = 100 " + MINUS + " 20",
  "hint": "Work out the 80 °C change before substituting.",
  "misconceptions": [
   {"pattern": "final_temp", "check": "common", "expect": 630000,
    "message": "Use the change 100 " + MINUS + " 20 = 80 °C: \\(\\Delta E\\) = 1.5 × 4200 × 80 = 504,000 J. Using 100 °C gives 630,000 J."}],
  "guided_steps": [
   sayonly("Heating water uses \\(\\Delta E = mc\\Delta\\theta\\). First the temperature change."),
   box("Temperature change: 100 " + MINUS + " 20 = ", 80, "Final minus initial."),
   box("Multiply mass by SHC: 1.5 × 4200 = ", 6300, "1.5 lots of 4200.", phase="substitute"),
   box("Now multiply by the change: 6300 × 80 = ", 504000, "6300 times 80.", phase="substitute"),
   box("Check: 504000 ÷ 80 = ", 6300, "Energy ÷ Δθ should give mc.", phase="substitute",
       done="That returns 1.5 × 4200 = 6300, so the energy is 504,000 J.")]},
 {  # S3 boil water vaporisation 1130000
  "unit": "J",
  "display": "Calculate the energy needed to boil away 0.5 kg of water at 100 °C. (Specific latent heat of vaporisation = 2,260,000 J/kg)",
  "solutions": [1130000], "accept": 1000, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "equation_hint": "\\(E = m \\times L\\)",
  "hint": "Use the vaporisation latent heat, then multiply by the mass.",
  "misconceptions": [
   {"pattern": "wrong_L", "check": "common", "expect": 167000,
    "message": "Boiling uses the latent heat of vaporisation (2,260,000 J/kg): E = 0.5 × 2,260,000 = 1,130,000 J. Using fusion (334,000) gives 167,000 J."}],
  "guided_steps": [
   sayonly("Boiling is a change of state, so \\(E = m \\times L\\). Use the vaporisation latent heat, not fusion."),
   box("Write the latent heat of vaporisation. L = ", 2260000, "2,260,000 J/kg for boiling."),
   box("Multiply: 0.5 × 2260000 = ", 1130000, "Half of 2,260,000.", phase="substitute"),
   box("Check: 1130000 ÷ 2260000 = ", 0.5, "Energy ÷ L should return the mass.", phase="substitute",
       done="That returns the 0.5 kg mass, so the energy is 1,130,000 J.")]},
 {  # S4 rearrange for c 1000
  "unit": "J/kg/°C",
  "display": "A 0.5 kg material heated by 3,500 J rises in temperature by 7 °C. Calculate its specific heat capacity.",
  "solutions": [1000], "accept": 5, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "equation_hint": "Rearrange \\(\\Delta E = mc\\Delta\\theta\\) for c",
  "hint": "Rearrange to c = energy ÷ (mass × temperature change).",
  "misconceptions": [
   {"pattern": "forgot_rearrange", "check": "common", "expect": 7000,
    "message": "Divide by mass AND temperature change: c = 3500 ÷ (0.5 × 7) = 3500 ÷ 3.5 = 1,000 J/kg/°C. Dividing by mass only (3500 ÷ 0.5) gives 7,000."}],
  "guided_steps": [
   sayonly("You want c, so rearrange \\(\\Delta E = mc\\Delta\\theta\\) into \\(c = \\Delta E \\div (m \\times \\Delta\\theta)\\)."),
   box("Work out the bottom first: m × Δθ = 0.5 × 7 = ", 3.5, "Mass times temperature change."),
   box("Now divide the energy by it: 3500 ÷ 3.5 = ", 1000, "3500 shared into 3.5.", phase="substitute"),
   box("Check: 0.5 × 1000 × 7 = ", 3500, "Put c back into mcΔθ; it should give 3,500 J.", phase="substitute",
       done="That returns the 3,500 J supplied, so c = 1,000 J/kg/°C.")]},
]

# =====================================================================
# GOLD
# =====================================================================
gold = [
 {  # G1 heat then vaporise 3894000
  "unit": "J",
  "display": "A 1.5 kg sample of water is heated from 20 °C to 100 °C, then completely vaporised. Calculate the total energy required. (c water = 4,200 J/kg/°C; L vaporisation = 2,260,000 J/kg)",
  "solutions": [3894000], "accept": 1000, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "hint": "Heat the water first, then boil it, then add the two energies.",
  "misconceptions": [
   {"pattern": "forgot_step", "check": "common", "expect": 3390000,
    "message": "Add both stages: heating 504,000 J plus boiling 3,390,000 J = 3,894,000 J. Giving only 3,390,000 J forgets the energy to heat the water to 100 °C first."},
   {"pattern": "wrong_L", "check": "common", "expect": 1005000,
    "message": "Boiling uses the vaporisation latent heat (2,260,000 J/kg), giving 3,390,000 J for the boil and 3,894,000 J total. Using fusion (334,000) gives 1,005,000 J."}],
  "guided_steps": [
   sayonly("Two stages: heat the water to boiling with \\(\\Delta E = mc\\Delta\\theta\\), then boil it away with \\(E = mL\\). Add the two."),
   box("Stage 1 temperature change: 100 " + MINUS + " 20 = ", 80, "Final minus initial."),
   box("Stage 1 energy, heating: 1.5 × 4200 × 80 = ", 504000, "mcΔθ for the heating.", phase="substitute"),
   box("Stage 2 energy, boiling: 1.5 × 2260000 = ", 3390000, "mL for the change of state.", phase="substitute"),
   box("Add the two stages: 504000 + 3390000 = ", 3894000, "Heating energy plus boiling energy.", phase="substitute"),
   box("Check: take the boiling energy off the total, 3894000 " + MINUS + " 3390000 = ", 504000, "Total minus boiling should give the heating energy.", phase="substitute",
       done="That returns the stage-1 heating energy, so the total is 3,894,000 J.")]},
 {  # G2 cube volume then density 18
  "unit": "g/cm³",
  "display": "A metal cube has a mass of 486 g and sides 3 cm long. Calculate the density of the metal in g/cm³.",
  "solutions": [18], "accept": 0.1, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "hint": "Find the cube's volume (side cubed), then divide mass by it.",
  "misconceptions": [
   {"pattern": "volume_error", "check": "common", "expect": 54,
    "message": "A cube's volume is side³ = 3 × 3 × 3 = 27 cm³, so ρ = 486 ÷ 27 = 18 g/cm³. Using 3² = 9 by mistake gives 54."}],
  "guided_steps": [
   sayonly("A cube's volume is side³. Find the volume, then use \\(\\rho = m \\div V\\). The units already match (g and cm)."),
   box("Volume of the cube: 3 × 3 × 3 = ", 27, "Side cubed."),
   box("Now the density: 486 ÷ 27 = ", 18, "486 shared into 27.", phase="substitute"),
   box("Check: 18 × 27 = ", 486, "Density × volume should return the mass.", phase="substitute",
       done="That returns the 486 g mass, so the density is 18 g/cm³.")]},
 {  # G3 rearrange for c 1200
  "unit": "J/kg/°C",
  "display": "A heater supplies 120,000 J to 4 kg of a liquid and raises its temperature by 25 °C. Calculate the specific heat capacity of the liquid.",
  "solutions": [1200], "accept": 5, "calculator": True, "input_type": "single_value",
  "higher_only": False,
  "hint": "Rearrange to c = energy ÷ (mass × temperature change).",
  "misconceptions": [
   {"pattern": "forgot_rearrange", "check": "common", "expect": 30000,
    "message": "Divide by mass AND temperature change: c = 120,000 ÷ (4 × 25) = 120,000 ÷ 100 = 1,200 J/kg/°C. Dividing by mass only (120,000 ÷ 4) gives 30,000."}],
  "guided_steps": [
   sayonly("You want c, so rearrange \\(\\Delta E = mc\\Delta\\theta\\) into \\(c = \\Delta E \\div (m \\times \\Delta\\theta)\\)."),
   box("Bottom line first: m × Δθ = 4 × 25 = ", 100, "Mass times temperature rise."),
   box("Divide the energy by it: 120000 ÷ 100 = ", 1200, "120,000 shared into 100.", phase="substitute"),
   box("Check: 4 × 1200 × 25 = ", 120000, "Put c back into mcΔθ; it should give 120,000 J.", phase="substitute",
       done="That returns the 120,000 J supplied, so c = 1,200 J/kg/°C.")]},
]

problem_bank = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "One equation, values already in matching units: substitute and solve.",
    "silver_description": "Convert a unit, find the temperature change, or rearrange before you substitute.",
    "gold_description": "Two calculations chained: two equations, or a volume then a density.",
}

# =====================================================================
# TIER GUIDES
# =====================================================================
tier_guides = {
 "bronze": {
  "title": "Bronze: one equation, units already right",
  "steps": [
   "Pick the equation: density \\(\\rho = m \\div V\\), heating \\(\\Delta E = mc\\Delta\\theta\\), or change of state \\(E = mL\\).",
   "Put the numbers straight in and calculate. Check your board's data sheet for any values you are not given.",
   "Always write the unit with your answer: g/cm³, J or °C.",
  ],
  "example": {
   "question": "A block has a mass of 480 g and a volume of 160 cm³. Find its density.",
   "steps": [
    {"label": "Equation", "content": "<p>\\(\\rho = m \\div V\\)</p>"},
    {"label": "Substitute", "content": "<p>\\(\\rho = 480 \\div 160\\)</p>"},
    {"label": "Check", "content": "<p>\\(3 \\times 160 = 480\\) ✓</p>"},
    {"label": "Answer", "content": "<p>\\(\\rho = 3\\) g/cm³</p>", "isAnswer": True, "is_answer": True},
   ]}},
 "silver": {
  "title": "Silver: convert or rearrange first",
  "steps": [
   "One thing needs doing before you substitute: find the temperature change (Δθ = final − initial), convert a unit, or rearrange the equation for the value you want.",
   "Then it becomes a bronze question: substitute and calculate.",
   "For a change of state, pick fusion (melting) or vaporisation (boiling); they are very different sizes.",
  ],
  "example": {
   "question": "A 2 kg block (c = 500 J/kg/°C) cools from 90 °C to 40 °C. Energy released?",
   "steps": [
    {"label": "Change", "content": "<p>Δθ = 90 − 40 = 50 °C</p>"},
    {"label": "Equation", "content": "<p>\\(\\Delta E = mc\\Delta\\theta\\)</p>"},
    {"label": "Substitute", "content": "<p>ΔE = 2 × 500 × 50</p>"},
    {"label": "Check", "content": "<p>50000 ÷ 50 = 1000 = 2 × 500 ✓</p>"},
    {"label": "Answer", "content": "<p>ΔE = 50,000 J</p>", "isAnswer": True, "is_answer": True},
   ]}},
 "gold": {
  "title": "Gold: two steps chained",
  "steps": [
   "Gold questions need two calculations. Spot both: often heat to a temperature (\\(\\Delta E = mc\\Delta\\theta\\)) then change state (\\(E = mL\\)), or find a volume then a density.",
   "Do each stage fully, keep the numbers, then combine them (usually add the energies).",
   "Watch the units the whole way through and state the final unit.",
  ],
  "example": {
   "question": "Melt 0.2 kg of ice then heat the water to 20 °C. (L = 334,000 J/kg; c = 4,200 J/kg/°C)",
   "steps": [
    {"label": "Stage 1 melt", "content": "<p>E = 0.2 × 334,000 = 66,800 J</p>"},
    {"label": "Stage 2 heat", "content": "<p>ΔE = 0.2 × 4200 × 20 = 16,800 J</p>"},
    {"label": "Add", "content": "<p>66,800 + 16,800</p>"},
    {"label": "Check", "content": "<p>83,600 − 66,800 = 16,800 ✓</p>"},
    {"label": "Answer", "content": "<p>83,600 J</p>", "isAnswer": True, "is_answer": True},
   ]}},
}

# =====================================================================
# GUIDED: opener + teach
# =====================================================================
opener_svg = ('<svg viewBox="0 0 240 112" role="img" aria-label="Two blocks of equal size, '
 'block A labelled 20 grams and block B labelled 60 grams">'
 '<rect x="34" y="24" width="58" height="58" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>'
 '<rect x="148" y="24" width="58" height="58" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="2"/>'
 '<text x="120" y="16" text-anchor="middle" fill="currentColor" font-family="Inter, sans-serif" font-size="11">same size</text>'
 '<text x="63" y="100" text-anchor="middle" fill="currentColor" font-family="Inter, sans-serif" font-size="12">A: 20 g</text>'
 '<text x="177" y="100" text-anchor="middle" fill="currentColor" font-family="Inter, sans-serif" font-size="12">B: 60 g</text>'
 '</svg>')

guided = {
 "opener": {
  "label": "Before any equations",
  "display": opener_svg + "<br>Two blocks take up exactly the same space.",
  "steps": [
   {"say": "Both blocks fill the same space, but block B has three times the mass of block A packed inside it.",
    "pre": "How many times more mass is packed into B? ", "post": "", "answer": 3,
    "hint": "60 g is how many times 20 g?"},
   {"say": "That 'mass packed into a space' is exactly what <strong>density</strong> measures. Same space, more mass, more dense.",
    "pre": "If block A's density is 2 g/cm³, what is block B's, in g/cm³? ", "post": "", "answer": 6,
    "hint": "Three times as dense as 2."},
   {"say": "You just found density by comparing mass for the same volume. The equation writes it as \\(\\rho = m \\div V\\): mass divided by the space it fills. This lesson also heats things (\\(\\Delta E = mc\\Delta\\theta\\)) and melts or boils them (\\(E = mL\\)), but each one is the same move: put the numbers in, mind the units."}
  ]},
 "teach": {
  "bronze": {
   "display": "A block of plastic has a mass of 750 g and a volume of 300 cm³. Calculate its density in g/cm³.",
   "label": "Together: your first one",
   "steps": [
    sayonly("Density is mass ÷ volume: \\(\\rho = m \\div V\\). The units match (g with cm³), so no conversion."),
    box("Write the mass. m = ", 750, "Given as 750 g."),
    box("Write the volume. V = ", 300, "Given as 300 cm³."),
    box("Divide: 750 ÷ 300 = ", 2.5, "A calculator gives 2.5.", phase="substitute"),
    box("Check: 2.5 × 300 = ", 750, "Density × volume should give the mass.", phase="substitute",
        done="That returns 750 g, so the density is 2.5 g/cm³.")]},
  "silver": {
   "display": "A 2 kg block of iron (c = 450 J/kg/°C) is heated from 15 °C to 55 °C. Calculate the energy needed.",
   "label": "Together: the silver move",
   "steps": [
    sayonly("Heating uses \\(\\Delta E = mc\\Delta\\theta\\). The silver move is finding the temperature change first."),
    box("Temperature change: 55 " + MINUS + " 15 = ", 40, "Final minus initial."),
    box("Mass × SHC: 2 × 450 = ", 900, "2 lots of 450."),
    box("Now multiply by the change: 900 × 40 = ", 36000, "900 times 40.", phase="substitute"),
    box("Check: 36000 ÷ 40 = ", 900, "Energy ÷ Δθ should give mc.", phase="substitute",
        done="That returns 2 × 450 = 900, so the energy is 36,000 J.")]},
  "gold": {
   "display": "0.5 kg of ice at 0 °C is melted, then the water is heated to 30 °C. Calculate the total energy. (L fusion = 334,000 J/kg; c water = 4,200 J/kg/°C)",
   "label": "Together: the gold move",
   "steps": [
    sayonly("Two stages: melt the ice with \\(E = mL\\), then heat the water with \\(\\Delta E = mc\\Delta\\theta\\). Add them."),
    box("Stage 1, melting: 0.5 × 334000 = ", 167000, "mL for the change of state."),
    box("Stage 2 temperature change: 30 " + MINUS + " 0 = ", 30, "Final minus initial."),
    box("Stage 2 energy, heating: 0.5 × 4200 × 30 = ", 63000, "mcΔθ for the heating.", phase="substitute"),
    box("Add the stages: 167000 + 63000 = ", 230000, "Melting energy plus heating energy.", phase="substitute",
        done="Total energy = 230,000 J.")]},
 }
}

# =====================================================================
pd = {
    "method_card": method_card,
    "topic_links": topic_links,
    "exam_context": exam_context,
    "problem_bank": problem_bank,
    "related_videos": related_videos,
    "worked_examples": we,
    "tier_guides": tier_guides,
    "guided": guided,
}

with io.open("lesson_physics-calculations-L05@e8e561e58b.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written")
