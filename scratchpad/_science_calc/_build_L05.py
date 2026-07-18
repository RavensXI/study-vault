# -*- coding: utf-8 -*-
import json, io, copy

SRC = "_live_L05.json"
OUT = "lesson_higher-calculations-L05@f4fdd10261.json"

live = json.load(io.open(SRC, encoding="utf-8"))
live = live["practice_data"] if "practice_data" in live else live
pd = copy.deepcopy(live)

def B(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def S(say):
    return {"say": say}

# ---------------- method_card (slim, board-neutral, no em dash) ----------
pd["method_card"] = {
    "title": "Energy, Power and Efficiency",
    "steps": [
        "Pick the equation from the quantities the question gives you.",
        "Check units: mass in kg, speed in m/s, height in m, time in s, energy in J, power in W.",
        "Substitute and calculate. For kinetic energy, square the speed before anything else.",
        "State the answer with its unit."
    ],
    "content": "<p>The core equations: \\(E_k = \\tfrac{1}{2}mv^2\\) (kinetic energy), \\(E_p = mgh\\) (gravitational PE), \\(P = E \\div t\\) (power), \\(P = IV\\) and \\(P = I^2R\\) (electrical power), and efficiency = useful output ÷ total input.</p><p>Check whether your board gives you any of these; either way, knowing them cold saves time. Use \\(g = 9.8\\) N/kg unless told otherwise.</p><p>Two errors cost the most marks: forgetting to square the speed, and getting efficiency upside down (it must land between 0 and 1, or 0% and 100%).</p>"
}

# ---------------- exam_context (sanitise em dashes) ----------------------
pd["exam_context"] = {
    "marks": "2 to 5 marks per calculation; efficiency may add a follow-up on energy wasted as heat",
    "paper": "Physics: Breadth and Depth papers",
    "frequency": "Very high: energy and power calculations appear in virtually every Physics paper"
}

# ---------------- tier descriptions -------------------------------------
pb = pd["problem_bank"]
pb["bronze_description"] = "One equation, values already in the right units. Substitute and calculate."
pb["silver_description"] = "Convert a unit or rearrange the equation before you substitute."
pb["gold_description"]   = "Two steps chained, or efficiency, or a before-and-after energy comparison."

# ---------------- misconception expects ---------------------------------
# ordered list per problem; None keeps a misconception non-firing
EXPECTS = {
    ("bronze",0): [18000, 1080000],
    ("bronze",1): [250, 5000],
    ("bronze",2): [15],
    ("bronze",3): [3000],
    ("bronze",4): [4.8],
    ("bronze",5): [1.43, None],
    ("bronze",6): [22.22],
    ("bronze",7): [48],
    ("silver",0): [5],
    ("silver",1): [98, 7],
    ("silver",2): [1066.67],
    ("silver",3): [60, None],
    ("silver",4): [125],
    ("silver",5): [5, 300],
    ("gold",0): [2.5, None],
    ("gold",1): [200, None],
    ("gold",2): [2.4, None],
    ("gold",3): [3430, None],
    ("gold",4): [78.4, None],
    ("gold",5): [0.2, 5],
}

# revised misconception messages (avoid em dash, name the slip, board-neutral)
MSG = {
    ("bronze",0): [
        "Square the speed first: v² = 30² = 900. Eₖ = 0.5 × 1200 × 900 = 540 000 J. Multiplying by 30 without squaring gives 18 000 J.",
        "Keep the ½ in Eₖ = ½mv². Leaving it out gives 1 200 × 900 = 1 080 000 J, double the real answer."
    ],
    ("bronze",1): [
        "Square the speed first: v² = 10² = 100. Eₖ = 0.5 × 50 × 100 = 2500 J. Using 10 without squaring gives 250 J.",
        "Eₖ = ½ × 50 × 100 = 2500 J. Forgetting the ½ gives 5000 J."
    ],
    ("bronze",2): [
        "Multiply all three: Eₚ = 5.0 × 9.8 × 3.0 = 147 J. Leaving g out gives 5.0 × 3.0 = 15 J."
    ],
    ("bronze",3): [
        "Convert time to seconds first: 3 minutes = 180 s. P = 9000 ÷ 180 = 50 W. Dividing by 3 gives 3000 W."
    ],
    ("bronze",4): [
        "P = IV = 2.5 × 12 = 30 W. Multiply current by voltage. Dividing (12 ÷ 2.5) gives 4.8, which is not a power."
    ],
    ("bronze",5): [
        "Efficiency = useful ÷ total = 3500 ÷ 5000 = 0.7. Dividing the wrong way (5000 ÷ 3500) gives about 1.43.",
        "Efficiency is always useful ÷ total, so the answer sits between 0 and 1."
    ],
    ("bronze",6): [
        "Rearrange to E = P × t = 2000 × 90 = 180 000 J. Dividing (2000 ÷ 90) gives about 22.2, which is not an energy."
    ],
    ("bronze",7): [
        "P = IV = 5 × 240 = 1200 W. Multiply, do not divide: 240 ÷ 5 = 48 is the slip."
    ],
    ("silver",0): [
        "Eₚ = mgh = 0.5 × 9.8 × 10 = 49 J. Leaving g out gives 0.5 × 10 = 5 J."
    ],
    ("silver",1): [
        "v² = 2gh = 2 × 9.8 × 5 = 98, then v = √98 = 9.9 m/s. Forgetting the square root leaves 98.",
        "Use v² = 2gh; the 2 comes from the ½ in ½mv². Dropping it gives v² = gh = 49 and v = 7 m/s."
    ],
    ("silver",2): [
        "Useful output = efficiency × input = 0.75 × 800 = 600 W. Dividing (800 ÷ 0.75) gives about 1067 W, more than the input."
    ],
    ("silver",3): [
        "Square the current first: P = I²R = 3.0² × 20 = 9 × 20 = 180 W. Using 3.0 without squaring gives 60 W.",
        "Use P = I²R when you are given current and resistance."
    ],
    ("silver",4): [
        "Efficiency = (useful ÷ total) × 100 = (36 000 ÷ 45 000) × 100 = 80%. Dividing the wrong way gives 125%, which is impossible."
    ],
    ("silver",5): [
        "P = IV = 2.5 W. Convert time: 2 hours = 7200 s. E = 2.5 × 7200 = 18 000 J. Using t = 2 gives 5 J.",
        "2 hours is 7200 seconds, not 120. Converting only to minutes gives 2.5 × 120 = 300 J."
    ],
    ("gold",0): [
        "KE = ½ × 1500 × 25² = ½ × 1500 × 625 = 468 750 J. Then Δθ = 468 750 ÷ (15 × 500) = 62.5 °C. Forgetting to square the speed gives Δθ = 2.5 °C.",
        "All the kinetic energy becomes heat, so use ΔE = mcΔθ rearranged to Δθ = ΔE ÷ (mc)."
    ],
    ("gold",1): [
        "Output power P = IV = 10 × 230 = 2300 W. The internal waste I²R = 10² × 2.0 = 200 W is a separate answer, not the output.",
        "This has two parts: output power P = IV, then wasted power P = I²R."
    ],
    ("gold",2): [
        "Efficiency = useful ÷ total = 5.0 ÷ 12 = 0.417. Dividing the wrong way (12 ÷ 5.0) gives 2.4, above 1.",
        "Efficiency can never exceed 1 (100%)."
    ],
    ("gold",3): [
        "GPE gained = mgh = 70 × 9.8 × 5.0 = 3430 J. Power P = 3430 ÷ 4.0 = 857.5 W. Stopping at 3430 forgets to divide by time.",
        "Find the GPE first, then divide by the time to turn energy into power."
    ],
    ("gold",4): [
        "Initial GPE = 0.4 × 9.8 × 20 = 78.4 J. Final GPE = 0.4 × 9.8 × 12 = 47.04 J. Energy lost = 78.4 − 47.04 = 31.36 J. Giving 78.4 forgets to subtract the final GPE.",
        "Work out the GPE at 20 m and at 12 m, then subtract."
    ],
    ("gold",5): [
        "I = P ÷ V = 1150 ÷ 230 = 5.0 A, then R = V ÷ I = 230 ÷ 5.0 = 46.0 Ω. Using R = V ÷ P gives 0.2 Ω, far too small.",
        "The question asks for resistance, not current: after I = 5.0 A you still need R = V ÷ I."
    ],
}
# clean the accidental key duplication
if ("bronze",2) in EXPECTS:
    pass

def apply_misconceptions(tier):
    for i, prob in enumerate(pb[tier]):
        exps = EXPECTS[(tier, i)]
        msgs = MSG[(tier, i)]
        mc = prob.get("misconceptions") or []
        assert len(mc) == len(exps) == len(msgs), (tier, i, len(mc), len(exps), len(msgs))
        for j, m in enumerate(mc):
            m["message"] = msgs[j]
            m["expect"] = exps[j]

for t in ("bronze","silver","gold"):
    apply_misconceptions(t)

# ---------------- fix B1 equation_hint em dash --------------------------
pb["bronze"][0]["equation_hint"] = "\\(E_k = \\tfrac{1}{2}mv^2\\): square the speed first."

# ---------------- gold problem hints (gold lacks equation_hint) ---------
GOLD_HINTS = [
    "All the kinetic energy becomes heat: find KE with ½mv², then use ΔE = mcΔθ rearranged for the temperature rise.",
    "Output power uses P = IV; keep the internal resistance for the separate wasted-power part.",
    "Efficiency is useful power out divided by total power in; both are in MW so the units cancel.",
    "Find the GPE gained (mgh), then divide by the time to get the power.",
    "Work out the GPE at 20 m and at 12 m, then subtract to get the energy lost.",
    "Find the current with I = P ÷ V, then the resistance with R = V ÷ I."
]
for i, prob in enumerate(pb["gold"]):
    prob["hint"] = GOLD_HINTS[i]

# ---------------- S4 circuit figure -------------------------------------
S4_SVG = ('<svg viewBox="0 0 240 165" role="img" aria-label="A simple series circuit: a cell drives a current of 3.0 amps through a 20 ohm resistor, measured by an ammeter">'
 '<g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">'
 '<line x1="40" y1="30" x2="95" y2="30"/><line x1="145" y1="30" x2="200" y2="30"/>'
 '<rect x="95" y="22" width="50" height="16"/>'
 '<line x1="200" y1="30" x2="200" y2="120"/>'
 '<line x1="200" y1="120" x2="134" y2="120"/><line x1="106" y1="120" x2="40" y2="120"/>'
 '<circle cx="120" cy="120" r="14"/>'
 '<line x1="40" y1="120" x2="40" y2="82"/><line x1="40" y1="68" x2="40" y2="30"/>'
 '<line x1="24" y1="68" x2="56" y2="68"/><line x1="32" y1="82" x2="48" y2="82"/>'
 '</g>'
 '<text x="120" y="14" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="currentColor">20 Ω</text>'
 '<text x="120" y="124" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="currentColor">A</text>'
 '<text x="120" y="152" text-anchor="middle" font-family="Inter, sans-serif" font-size="11" fill="currentColor">3.0 A</text>'
 '</svg>')
_s4 = pb["silver"][3]
if not _s4["display"].startswith("<svg"):
    _s4["display"] = S4_SVG + _s4["display"]

# ---------------- guided_steps for every bank problem -------------------
GS = {}

GS[("bronze",0)] = [
    S("Kinetic energy uses \\(E_k = \\tfrac{1}{2}mv^2\\). Mass is in kg and speed in m/s already, so no conversion."),
    B("Square the speed: 30² = ", 900, "30 × 30."),
    B("Multiply by the mass: 1200 × 900 = ", 1080000, "Mass times the squared speed.", phase="substitute"),
    B("Halve it: 1080000 ÷ 2 = ", 540000, "Divide the last line by 2.", phase="substitute",
      done="540 000 J (540 kJ). Energy is measured in joules."),
]
GS[("bronze",1)] = [
    S("Kinetic energy uses \\(E_k = \\tfrac{1}{2}mv^2\\). Units are already kg and m/s."),
    B("Square the speed: 10² = ", 100, "10 × 10."),
    B("Multiply by the mass: 50 × 100 = ", 5000, "Mass times the squared speed.", phase="substitute"),
    B("Halve it: 5000 ÷ 2 = ", 2500, "Divide the last line by 2.", phase="substitute",
      done="2500 J."),
]
GS[("bronze",2)] = [
    S("Gravitational PE uses \\(E_p = mgh\\). Mass in kg, g in N/kg, height in m, all as given."),
    B("Weight per metre risen: 9.8 × 5.0 = ", 49, "g times the mass."),
    B("Multiply by the height: 49 × 3.0 = ", 147, "Times the 3.0 m.", phase="substitute",
      done="147 J."),
    B("Check by dividing back: 147 ÷ 49 = ", 3, "This should return the height.", phase="substitute",
      done="It returns the 3.0 m height, so 147 J is right."),
]
GS[("bronze",3)] = [
    S("Power uses \\(P = E \\div t\\). Time must be in seconds first."),
    B("Convert the time: 3 × 60 = ", 180, "60 seconds in a minute."),
    B("Divide energy by time: 9000 ÷ 180 = ", 50, "Energy over time.", phase="substitute",
      done="50 W."),
    B("Check: 50 × 180 = ", 9000, "Power times time returns the energy.", phase="substitute",
      done="Returns 9000 J, so 50 W is right."),
]
GS[("bronze",4)] = [
    S("Electrical power uses \\(P = IV\\). Both the current and the voltage are given."),
    B("Multiply the whole part: 2 × 12 = ", 24, "Two lots of 12."),
    B("Now the 0.5 part: 0.5 × 12 = ", 6, "Half of 12.", phase="substitute"),
    B("Add the parts: 24 + 6 = ", 30, "Combine the two lines.", phase="substitute",
      done="30 W."),
]
GS[("bronze",5)] = [
    S("Efficiency = useful output ÷ total input. It has no unit."),
    B("Simplify the top: 3500 ÷ 100 = ", 35, "Drop two zeros."),
    B("Simplify the bottom: 5000 ÷ 100 = ", 50, "Drop two zeros.", phase="substitute"),
    B("Divide them: 35 ÷ 50 = ", 0.7, "Thirty-five fiftieths.", phase="substitute",
      done="0.70. Efficiency sits between 0 and 1, with no unit."),
]
GS[("bronze",6)] = [
    S("Rearrange \\(P = E \\div t\\) to \\(E = P \\times t\\). The time is already in seconds."),
    B("First part: 2000 × 9 = ", 18000, "Multiply by 9."),
    B("Scale up for the 90: 18000 × 10 = ", 180000, "Now times 10.", phase="substitute"),
    B("Check: 180000 ÷ 90 = ", 2000, "Energy over time returns the power.", phase="substitute",
      done="Returns the 2000 W, so 180 000 J (180 kJ) is right."),
]
GS[("bronze",7)] = [
    S("Electrical power uses \\(P = IV\\). Multiply the current by the voltage."),
    B("First part: 5 × 200 = ", 1000, "Multiply by 200."),
    B("Now the 40: 5 × 40 = ", 200, "Multiply by 40.", phase="substitute"),
    B("Add the parts: 1000 + 200 = ", 1200, "Combine the two lines.", phase="substitute",
      done="1200 W."),
]

GS[("silver",0)] = [
    S("Gravitational PE uses \\(E_p = mgh\\). Units are already kg, N/kg and m."),
    B("Weight per metre risen: 0.5 × 9.8 = ", 4.9, "Half of 9.8."),
    B("Multiply by the height: 4.9 × 10 = ", 49, "Times the 10 m.", phase="substitute",
      done="49 J."),
    B("Check: 49 ÷ 10 = ", 4.9, "Divide back by the height.", phase="substitute",
      done="Returns 4.9, so 49 J is right."),
]
GS[("silver",1)] = [
    S("GPE lost becomes KE gained: \\(mgh = \\tfrac{1}{2}mv^2\\). The mass cancels, leaving \\(v^2 = 2gh\\)."),
    B("Twice g: 2 × 9.8 = ", 19.6, "Double 9.8."),
    B("Times the height: 19.6 × 5.0 = ", 98, "This is v² in m²/s²."),
    B("Square root, to 1 d.p.: √98 = ", 9.9, "The root turns v² into v.", phase="substitute",
      done="9.9 m/s."),
    B("Check: 9.9 × 9.9 = ", 98.01, "Squaring should return about 98.", phase="substitute",
      done="Squaring returns about 98, so 9.9 m/s is right."),
]
GS[("silver",2)] = [
    S("Rearrange efficiency: useful output = efficiency × total input."),
    B("Three quarters of 8: 0.75 × 8 = ", 6, "0.75 × 8."),
    B("Scale back up: 6 × 100 = ", 600, "The input was 800, so times 100.", phase="substitute",
      done="600 W."),
    B("Check: 600 ÷ 800 = ", 0.75, "Output over input returns the efficiency.", phase="substitute",
      done="Returns the 0.75 efficiency, so 600 W is right."),
]
GS[("silver",3)] = [
    S("Power from current and resistance uses \\(P = I^2R\\). Square the current first."),
    B("Square the current: 3.0² = ", 9, "3 × 3."),
    B("Multiply by the resistance: 9 × 20 = ", 180, "Times 20 ohms.", phase="substitute",
      done="180 W."),
    B("Check: 180 ÷ 20 = ", 9, "Divide back by the resistance.", phase="substitute",
      done="Returns 9, which is 3², so 180 W is right."),
]
GS[("silver",4)] = [
    S("Percentage efficiency = (useful ÷ total) × 100."),
    B("Simplify: 36000 ÷ 9000 = ", 4, "Divide both by 9000."),
    B("And the total: 45000 ÷ 9000 = ", 5, "Divide both by 9000."),
    B("Divide them: 4 ÷ 5 = ", 0.8, "Four fifths.", phase="substitute"),
    B("Turn into a percentage: 0.8 × 100 = ", 80, "Times 100.", phase="substitute",
      done="80%."),
]
GS[("silver",5)] = [
    S("Two steps: power \\(P = IV\\), then energy \\(E = Pt\\). Convert hours to seconds."),
    B("Power: 0.5 × 5.0 = ", 2.5, "Current times voltage."),
    B("Convert the time: 2 × 3600 = ", 7200, "3600 seconds in an hour."),
    B("Energy: 2.5 × 7200 = ", 18000, "Power times time.", phase="substitute",
      done="18 000 J."),
    B("Check: 18000 ÷ 7200 = ", 2.5, "Divide back by the time.", phase="substitute",
      done="Returns the 2.5 W, so 18 000 J is right."),
]

GS[("gold",0)] = [
    S("Two equations. First the kinetic energy \\(E_k = \\tfrac{1}{2}mv^2\\); all of it becomes heat, then \\(\\Delta E = mc\\Delta\\theta\\)."),
    B("Square the speed: 25² = ", 625, "25 × 25."),
    B("Mass times squared speed: 1500 × 625 = ", 937500, "1500 × 625."),
    B("Halve it for the KE: 937500 ÷ 2 = ", 468750, "This heat all goes to the discs."),
    B("Now mc: 15 × 500 = ", 7500, "Disc mass times specific heat capacity."),
    B("Temperature rise: 468750 ÷ 7500 = ", 62.5, "Heat energy over mc.", phase="substitute",
      done="62.5 °C."),
    B("Check: 7500 × 62.5 = ", 468750, "mc times the rise returns the heat.", phase="substitute",
      done="Returns 468 750 J, so 62.5 °C is right."),
]
GS[("gold",1)] = [
    S("The output power uses \\(P = IV\\). Split the multiplication of 10 × 230."),
    B("First part: 10 × 200 = ", 2000, "Ten lots of 200."),
    B("Now the 30: 10 × 30 = ", 300, "Ten lots of 30.", phase="substitute"),
    B("Add the parts: 2000 + 300 = ", 2300, "Combine the two lines.", phase="substitute",
      done="2300 W output. (The internal I²R = 200 W is wasted separately.)"),
]
GS[("gold",2)] = [
    S("Efficiency = useful ÷ total. Both powers are in MW, so the units cancel."),
    B("Power wasted first: 12 − 5.0 = ", 7, "Total supplied minus useful out."),
    B("Efficiency, to 3 d.p.: 5.0 ÷ 12 = ", 0.417, "Useful over total.", phase="substitute"),
    B("As a percentage: 0.417 × 100 = ", 41.7, "Times 100.", phase="substitute",
      done="0.417 (41.7%), with 7 MW wasted."),
]
GS[("gold",3)] = [
    S("Two steps: GPE gained \\(E_p = mgh\\), then power \\(P = E \\div t\\)."),
    B("Weight: 70 × 9.8 = ", 686, "Mass times g."),
    B("GPE gained: 686 × 5.0 = ", 3430, "Times the 5.0 m height."),
    B("Power: 3430 ÷ 4.0 = ", 857.5, "Energy over time.", phase="substitute",
      done="857.5 W."),
    B("Check: 857.5 × 4.0 = ", 3430, "Power times time returns the energy.", phase="substitute",
      done="Returns the 3430 J, so 857.5 W is right."),
]
GS[("gold",4)] = [
    S("Energy lost = GPE at the start minus GPE after the bounce. Use \\(E_p = mgh\\) for each."),
    B("Weight: 0.4 × 9.8 = ", 3.92, "Mass times g."),
    B("Initial GPE at 20 m: 3.92 × 20 = ", 78.4, "Times the drop height."),
    B("Final GPE at 12 m: 3.92 × 12 = ", 47.04, "Times the bounce height."),
    B("Energy lost: 78.4 − 47.04 = ", 31.36, "Initial minus final.", phase="substitute",
      done="31.36 J lost."),
    B("Check via the 8 m drop: 3.92 × 8 = ", 31.36, "mg times the height difference.", phase="substitute",
      done="Same answer, so 31.36 J is right."),
]
GS[("gold",5)] = [
    S("Two steps: current \\(I = P \\div V\\), then resistance \\(R = V \\div I\\)."),
    B("Current: 1150 ÷ 230 = ", 5.0, "Power over voltage."),
    B("Resistance: 230 ÷ 5.0 = ", 46, "Voltage over current.", phase="substitute",
      done="46.0 Ω."),
    B("Check: 5.0 × 46 = ", 230, "Current times resistance returns the voltage.", phase="substitute",
      done="Returns 230 V, so 46.0 Ω is right."),
]

for t in ("bronze","silver","gold"):
    for i, prob in enumerate(pb[t]):
        prob["guided_steps"] = GS[(t, i)]

# ---------------- tier_guides -------------------------------------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one equation, straight in",
        "steps": [
            "Pick the equation that links the quantities named. The values are already in the right units (kg, m, m/s, s, A, V).",
            "Write it, substitute, and calculate. For \\(E_k = \\tfrac{1}{2}mv^2\\), square the speed first, then multiply by mass and by a half.",
            "State the answer with its unit: joules for energy, watts for power."
        ],
        "example": {
            "question": "A 600 kg car travels at 10 m/s. Calculate its kinetic energy.",
            "steps": [
                {"label": "Equation", "content": "<p>\\(E_k = \\tfrac{1}{2}mv^2\\)</p>"},
                {"label": "Square the speed", "content": "<p>\\(10^2 = 100\\)</p>"},
                {"label": "Substitute", "content": "<p>\\(0.5 \\times 600 \\times 100 = 30\\,000\\)</p>"},
                {"label": "Check", "content": "<p>\\(30\\,000 \\div 600 = 50 = \\tfrac{1}{2}\\times 100\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(30\\,000\\) J</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: convert or rearrange first",
        "steps": [
            "One extra move before you substitute: either convert a unit (minutes or hours to seconds) or rearrange the equation for your unknown.",
            "Rearranging \\(P = E \\div t\\) gives \\(E = P \\times t\\); efficiency rearranges to useful = efficiency × total.",
            "Then it is a bronze substitution. Keep the unit on the answer."
        ],
        "example": {
            "question": "A 500 W lamp is on for 2 minutes. How much energy does it transfer?",
            "steps": [
                {"label": "Rearrange", "content": "<p>\\(E = P \\times t\\)</p>"},
                {"label": "Convert time", "content": "<p>\\(2 \\times 60 = 120\\) s</p>"},
                {"label": "Substitute", "content": "<p>\\(500 \\times 120 = 60\\,000\\)</p>"},
                {"label": "Check", "content": "<p>\\(60\\,000 \\div 120 = 500\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(60\\,000\\) J</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: chain two steps",
        "steps": [
            "Two equations in a row, or a before-and-after comparison. Work out the first quantity, then feed it into the second.",
            "Common chains: GPE then power (mgh, then ÷ time); KE then heating (½mv², then mcΔθ); output power then efficiency.",
            "Watch the unit at every stage and give the final answer with its unit."
        ],
        "example": {
            "question": "A crane lifts 100 kg through 4.0 m in 5.0 s. Its input power is 1000 W. Find the efficiency. (g = 9.8 N/kg)",
            "steps": [
                {"label": "GPE gained", "content": "<p>\\(100 \\times 9.8 \\times 4.0 = 3920\\) J</p>"},
                {"label": "Output power", "content": "<p>\\(3920 \\div 5.0 = 784\\) W</p>"},
                {"label": "Efficiency", "content": "<p>\\(784 \\div 1000 = 0.784\\)</p>"},
                {"label": "Check", "content": "<p>\\(0.784 \\times 1000 = 784\\) W ✓</p>"},
                {"label": "Answer", "content": "<p>\\(0.784\\) (78.4%)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------- guided (opener + teach) -------------------------------
pd["guided"] = {
    "opener": {
        "label": "Before any equations",
        "display": "Two identical cars hit a wall.<br>Car A is doing 20 mph.<br>Car B is doing 40 mph, exactly twice as fast.",
        "steps": [
            S("A crash puzzle. No equations, just compare the two cars."),
            B("Car B is twice as fast. How many times MORE speed is that? ", 2,
              "40 is 2 lots of 20."),
            B("A crash's energy grows with speed times speed. So multiply your 2 by itself: 2 × 2 = ", 4,
              "Two times two.",
              done="Not twice the damage. Four times."),
            S("That is the shock: doubling the speed does not double a crash, it <strong>quadruples</strong> it. Kinetic energy is \\(E_k = \\tfrac{1}{2}mv^2\\), and the little ² is why. Speed counts twice, so every energy question starts by squaring it.")
        ]
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "A 900 kg car travels at 20 m/s. Calculate its kinetic energy. \\(E_k = \\tfrac{1}{2}mv^2\\)",
            "steps": [
                S("Units are already kg and m/s, so go straight in. Square the speed first."),
                B("20² = ", 400, "20 × 20."),
                B("Multiply by the mass: 900 × 400 = ", 360000, "Mass times squared speed.", phase="substitute"),
                B("Halve it: 360000 ÷ 2 = ", 180000, "Divide by 2.", phase="substitute",
                  done="180 000 J (180 kJ)."),
                B("Check: 2 × 180000 ÷ 900 = ", 400, "This should return v².", phase="substitute",
                  done="Returns 400, which is 20², so it is right.")
            ]
        },
        "silver": {
            "label": "Together: the silver move",
            "display": "A 500 W security light is on for 5 minutes. How much energy does it transfer? \\(P = E \\div t\\)",
            "steps": [
                S("Rearrange to \\(E = P \\times t\\), and the time must be in seconds first."),
                B("Convert the time: 5 × 60 = ", 300, "60 seconds in a minute."),
                B("Energy: 500 × 300 = ", 150000, "Power times time.", phase="substitute"),
                B("In kilojoules: 150000 ÷ 1000 = ", 150, "1000 J in a kJ.", phase="substitute",
                  done="150 000 J, or 150 kJ."),
                B("Check: 150000 ÷ 300 = ", 500, "Energy over time returns the power.", phase="substitute",
                  done="Returns the 500 W, so it is right.")
            ]
        },
        "gold": {
            "label": "Together: the gold move",
            "display": "A crane lifts a 200 kg load 6.0 m in 8.0 s. The motor's input power is 2000 W. Find the efficiency. (g = 9.8 N/kg)",
            "steps": [
                S("Chain it: GPE gained, then output power, then efficiency."),
                B("Weight: 200 × 9.8 = ", 1960, "Mass times g."),
                B("GPE gained: 1960 × 6.0 = ", 11760, "Times the height."),
                B("Output power: 11760 ÷ 8.0 = ", 1470, "Energy over time.", phase="substitute"),
                B("Efficiency: 1470 ÷ 2000 = ", 0.735, "Useful power over input power.", phase="substitute",
                  done="0.735 (73.5%). Efficiency has no unit.")
            ]
        }
    }
}

# ---------------- em-dash safety sweep (student-facing only) -------------
def sweep(obj):
    if isinstance(obj, dict):
        return {k: (v if k in ("note","guided_skip_reason") else sweep(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sweep(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace("—", ", ").replace("&mdash;", ". ")
    return obj
pd = sweep(pd)

# ---------------- integrity asserts -------------------------------------
for t in ("bronze","silver","gold"):
    for i, prob in enumerate(pb[t]):
        sols = [float(x) for x in prob["solutions"]]
        answers = [s["answer"] for s in prob["guided_steps"] if s.get("answer") is not None]
        assert any(abs(a - sols[0]) < 0.02 for a in answers), ("solution not in walk", t, i, sols, answers)
        # expects outside correct
        for m in prob.get("misconceptions", []):
            e = m.get("expect")
            if e is not None:
                assert abs(float(e) - sols[0]) > 0.011, ("expect==correct", t, i, e)

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("WROTE", OUT)
print("bronze", len(pb["bronze"]), "silver", len(pb["silver"]), "gold", len(pb["gold"]))
