# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_l02d5_canonical.json", encoding="utf-8"))

# ---------- method_card (slim, board-neutral, no em dash, <=4 steps, <=140 words) ----------
pd["method_card"] = {
    "title": "Efficiency and Energy Resources",
    "steps": [
        "Identify the useful output and the total input (both energy, or both power, never mixed).",
        "Divide: efficiency = useful output ÷ total input.",
        "Multiply by 100 if the question wants a percentage.",
        "Sense check: efficiency is always below 1 (100%).",
    ],
    "content": ("<p><strong>Efficiency</strong> tells you how much of the energy put into a device "
        "comes out in the useful form you want.</p>"
        "<p>efficiency = useful output ÷ total input. Use energy values or power values, "
        "but never mix them. The answer is a decimal; multiply by 100 for a percentage.</p>"
        "<p>It can never be more than 1 (100%): if yours is, you divided the wrong way round. "
        "Wasted energy = total input − useful output, and it ends up warming the surroundings.</p>"),
}

# ---------- exam_context: strip em dash ----------
pd["exam_context"]["frequency"] = "Very common: efficiency appears in almost every Paper 1"

# ---------- worked_examples: strip em dash in labels ----------
for we in pd["worked_examples"]:
    for st in we["steps"]:
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ")

# ---------- tier descriptions ----------
pb = pd["problem_bank"]
pb["bronze_description"] = ("One efficiency equation, values already in the right form: divide useful "
    "by total, or multiply back to find a missing piece.")
pb["silver_description"] = ("An extra move first: subtract the wasted energy, rearrange for the input, "
    "or work out the energy before you divide.")
pb["gold_description"] = ("Chain two equations: find the useful energy (KE, GPE, or power × time) "
    "first, then bring in efficiency.")

# ---------- helper builders ----------
def sy(s): return {"say": s}
def bx(pre, ans, hint, post="", done=None, phase=False, say=None):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if done: d["done"] = done
    if phase: d["phase"] = "substitute"
    if say is not None: d["say"] = say
    return d

# ---------- guided_steps per problem ----------
EQ = "\\(\\text{efficiency} = \\frac{\\text{useful output}}{\\text{total input}}\\)"

gs = {}

# BRONZE
gs["b0"] = [
    sy("Efficiency compares the useful energy out with the total energy in: " + EQ + "."),
    bx("Useful output (the heat for the room), in J = ", 1600, "The energy that does the job you want is the 1600 J of heat."),
    bx("Total input, in J = ", 2000, "Everything that goes in: the 2000 J of electrical energy."),
    bx("Now divide, useful ÷ total: 1600 ÷ 2000 = ", 0.8, "Useful divided by total.", phase=True),
    bx("Check by working backwards: 0.8 × 2000 = ", 1600, "This should give back the useful output.", done="Matches the 1600 J we started with, so 0.8 is right."),
    sy("So the efficiency is <strong>0.8</strong> (or 80%). Efficiency has no unit."),
]
gs["b1"] = [
    sy("Efficiency is useful ÷ total, then turned into a percentage: " + EQ + "."),
    bx("Useful output, in J = ", 350, "The energy you actually get out: 350 J."),
    bx("Total input, in J = ", 500, "Everything put in: 500 J."),
    bx("Divide: 350 ÷ 500 = ", 0.7, "Useful over total.", phase=True),
    bx("Turn the decimal into a percentage: 0.7 × 100 = ", 70, "Multiply by 100.", done="That is the step people forget."),
    sy("So the efficiency is <strong>70%</strong>."),
]
gs["b2"] = [
    sy("You can put power straight into the efficiency equation: " + EQ + " works with watts too."),
    bx("Useful power output, in W = ", 7, "The light you actually get: 7 W."),
    bx("Total power input, in W = ", 10, "Everything supplied: 10 W."),
    bx("Divide: 7 ÷ 10 = ", 0.7, "Useful power over total power.", phase=True),
    bx("Check: 0.7 × 10 = ", 7, "Should return the useful power.", done="Back to 7 W, so 0.7 is right."),
    sy("So the efficiency is <strong>0.7</strong> (or 70%)."),
]
gs["b3"] = [
    sy("Efficiency is useful ÷ total, then as a percentage: " + EQ + "."),
    bx("Useful output (the kinetic energy), in J = ", 12000, "The energy you want: 12,000 J of KE."),
    bx("Total input, in J = ", 40000, "The chemical energy from fuel: 40,000 J."),
    bx("Divide: 12000 ÷ 40000 = ", 0.3, "Useful over total.", phase=True),
    bx("As a percentage: 0.3 × 100 = ", 30, "Multiply by 100.", done="30% of the fuel energy becomes movement."),
    sy("So the efficiency is <strong>30%</strong>."),
]
gs["b4"] = [
    sy("Here we know the efficiency and the total input, and want the useful output. Rearrange: useful output = efficiency × total input."),
    bx("First write 90% as a decimal: 90 ÷ 100 = ", 0.9, "Divide the percentage by 100."),
    bx("Total input, in J = ", 200000, "The electrical energy supplied: 200,000 J."),
    bx("Multiply: 0.9 × 200000 = ", 180000, "Efficiency times the total input.", phase=True),
    bx("Check the direction: 180000 ÷ 200000 = ", 0.9, "Should return the 0.9 we were given.", done="Back to 90%, so the useful energy is right."),
    sy("So the useful heat transferred is <strong>180,000 J</strong>."),
]
gs["b5"] = [
    sy("We want the useful power out, knowing the efficiency and total power in. Rearrange: useful output = efficiency × total input."),
    bx("Total input power, in MW = ", 800, "Everything supplied: 800 MW."),
    bx("Multiply by the efficiency: 0.35 × 800 = ", 280, "Efficiency times the total.", phase=True),
    bx("Check: 280 ÷ 800 = ", 0.35, "Should return the 0.35 efficiency.", done="Both values were in MW, so the answer stays in MW."),
    sy("So the useful electrical power output is <strong>280 MW</strong>."),
]
gs["b6"] = [
    sy("Energy is conserved: total in = useful out + wasted. So wasted = total input − useful output."),
    bx("Total input, in J = ", 80, "The electrical energy supplied: 80 J."),
    bx("Useful output (the light), in J = ", 8, "The useful light arrow: 8 J."),
    bx("Subtract: 80 − 8 = ", 72, "Total minus useful.", phase=True),
    bx("Check: 8 + 72 = ", 80, "Useful plus wasted should give the total.", done="Adds back to the 80 J input, so 72 J is right."),
    sy("So the wasted energy is <strong>72 J</strong>."),
]

# SILVER
gs["s0"] = [
    sy("First find the useful energy. Useful = total input − all the wasted energy."),
    bx("Total input, in J = ", 5000, "The electrical energy supplied: 5000 J."),
    bx("Add up ALL the wasted energy: 1500 + 500 = ", 2000, "Heat plus sound."),
    bx("Useful = total − wasted: 5000 − 2000 = ", 3000, "Take the wasted energy off the input."),
    sy("Now apply " + EQ + "."),
    bx("Divide: 3000 ÷ 5000 = ", 0.6, "Useful over total.", phase=True),
    bx("As a percentage: 0.6 × 100 = ", 60, "Multiply by 100.", done="Both wasted amounts were removed first, so 60% is right."),
    sy("So the efficiency is <strong>60%</strong>."),
]
gs["s1"] = [
    sy("We know the useful output and efficiency, and want the total input. Rearrange: total input = useful output ÷ efficiency."),
    bx("Useful output, in kJ = ", 720, "The electrical energy generated: 720 kJ."),
    bx("Divide by the efficiency: 720 ÷ 0.40 = ", 1800, "Useful divided by efficiency gives the bigger total.", phase=True),
    bx("Check: 0.40 × 1800 = ", 720, "Should return the useful output.", done="The total (1800 kJ) is larger than the useful output, as it must be."),
    sy("So the total energy input from the wind is <strong>1800 kJ</strong>."),
]
gs["s2"] = [
    sy("Two steps: find the total input, then the wasted energy. First rearrange: total input = useful output ÷ efficiency."),
    bx("Useful output, in J = ", 46000, "The useful heat provided: 46,000 J."),
    bx("Divide by the efficiency: 46000 ÷ 0.92 = ", 50000, "Useful over efficiency."),
    sy("Now the finish. Wasted = total − useful."),
    bx("Subtract: 50000 − 46000 = ", 4000, "Total input minus useful output.", phase=True),
    bx("Check: 46000 + 4000 = ", 50000, "Useful plus wasted should give the total.", done="Adds back to the 50,000 J input, so 4000 J wasted is right."),
    sy("So the energy wasted is <strong>4000 J</strong>."),
]
gs["s3"] = [
    sy("The falling water's GPE becomes electricity. Find the GPE gained each second, \\(E_p = mgh\\); because it is per second, that is the input power in watts."),
    bx("First m × g: 8000 × 9.8 = ", 78400, "Mass times gravitational field strength."),
    bx("Now × h: 78400 × 50 = ", 3920000, "Multiply by the height to get GPE per second."),
    sy("That is the total input power. Useful output = efficiency × input power."),
    bx("Multiply: 0.85 × 3920000 = ", 3332000, "Efficiency times the input power.", phase=True),
    bx("Check: 3332000 ÷ 3920000 = ", 0.85, "Should return the 0.85 efficiency.", done="Back to 0.85, so the useful power is right."),
    sy("So the useful power output is <strong>3,332,000 W</strong> (about 3.3 MW)."),
]
gs["s4"] = [
    sy("Two steps: find the useful power, then the wasted power. Useful = efficiency × total input."),
    bx("Total input power, in W = ", 750, "The drill's power rating: 750 W."),
    bx("Useful power: 0.60 × 750 = ", 450, "Efficiency times the total."),
    sy("Now the finish. Wasted = total − useful."),
    bx("Subtract: 750 − 450 = ", 300, "Total power minus useful power.", phase=True),
    bx("Check: 450 + 300 = ", 750, "Useful plus wasted should give the total.", done="Adds back to 750 W, so 300 W wasted is right."),
    sy("So the power wasted as heat and sound is <strong>300 W</strong>."),
]
gs["s5"] = [
    sy("Energy is conserved: everything in must come out somewhere. Other waste = total − useful − known waste."),
    bx("Total input, in MJ = ", 1000, "The coal energy supplied: 1000 MJ."),
    bx("Add the outputs you know: 350 + 500 = ", 850, "Useful electricity plus cooling-tower waste."),
    bx("Subtract from the total: 1000 − 850 = ", 150, "What is left must be the other waste.", phase=True),
    bx("Check: 350 + 500 + 150 = ", 1000, "All the outputs should add to the input.", done="Adds back to 1000 MJ, so 150 MJ is right."),
    sy("So the energy lost through other pathways is <strong>150 MJ</strong>."),
]

# GOLD
gs["g0"] = [
    sy("Two equations chained. First the useful output, the GPE gained: \\(E_p = mgh\\)."),
    bx("m × g: 120 × 9.8 = ", 1176, "Mass times gravitational field strength."),
    bx("× h: 1176 × 20 = ", 23520, "Multiply by the height to get the GPE."),
    sy("That GPE is the useful output. Rearrange efficiency: total input = useful ÷ efficiency."),
    bx("Divide: 23520 ÷ 0.75 = ", 31360, "Useful over efficiency.", phase=True),
    bx("Check: 0.75 × 31360 = ", 23520, "Should return the GPE.", done="Back to 23,520 J, so the input is right."),
    sy("So the total electrical energy input is <strong>31,360 J</strong>."),
]
gs["g1"] = [
    sy("First the useful output, the kinetic energy gained: \\(E_k = \\frac{1}{2}mv^2\\). Square the speed first."),
    bx("Square the speed: 25² = ", 625, "25 × 25, not 25 × 2."),
    bx("Now ½ × 1200 × 625 = ", 375000, "Half of mass times speed squared."),
    sy("That KE is the useful output. Rearrange efficiency: total input = useful ÷ efficiency."),
    bx("Divide: 375000 ÷ 0.30 = ", 1250000, "Useful over efficiency.", phase=True),
    bx("Check: 0.30 × 1250000 = ", 375000, "Should return the KE.", done="Back to 375,000 J, so the input is right."),
    sy("So the total chemical energy released is <strong>1,250,000 J</strong> (1.25 MJ)."),
]
gs["g2"] = [
    sy("Two steps. First the total power the panel must receive: total input = useful ÷ efficiency."),
    bx("Write 20% as a decimal: 20 ÷ 100 = ", 0.2, "Divide the percentage by 100."),
    bx("Total power: 240 ÷ 0.20 = ", 1200, "Useful power over efficiency."),
    sy("The Sun delivers 800 W for every m². Area = total power ÷ power per m²."),
    bx("Divide: 1200 ÷ 800 = ", 1.5, "Total power over the intensity.", phase=True),
    bx("Check: 1.5 × 800 = ", 1200, "Should return the total power needed.", done="1.5 m² collects 1200 W, so the area is right."),
    sy("So the panel area is <strong>1.5 m²</strong>."),
]
gs["g3"] = [
    sy("Several steps. First convert the time, because power is joules per second."),
    bx("5 minutes in seconds: 5 × 60 = ", 300, "60 seconds in a minute."),
    sy("Total energy supplied = power × time."),
    bx("600 × 300 = ", 180000, "Watts × seconds gives joules."),
    sy("Now the finish. Only 70% of that energy lifts the water. Useful energy = efficiency × total."),
    bx("0.70 × 180000 = ", 126000, "Multiply by the efficiency.", phase=True),
    sy("This useful energy is the GPE, \\(E_p = mgh\\), so \\(m = \\frac{E_p}{gh}\\). First find \\(gh\\)."),
    bx("9.8 × 8 = ", 78.4, "g times the height.", phase=True),
    bx("Divide (to 1 d.p.): 126000 ÷ 78.4 = ", 1607.1, "Useful energy over gh; round to 1 decimal place.", phase=True,
       done="So the mass is about 1607.1 kg."),
    sy("Check: 1607 kg of water lifted 8 m gains close to 126,000 J of GPE, matching the useful energy, so the answer is right (given to 1 d.p.)."),
]

# ---------- expects for misconceptions (None means non-firing) ----------
# order matches existing misconceptions list per problem
expects = {
    ("bronze",0): [1.25, None],
    ("bronze",1): [0.7],
    ("bronze",2): [None],
    ("bronze",3): [None],
    ("bronze",4): [222222.22],
    ("bronze",5): [2285.71, None],
    ("bronze",6): [None],
    ("bronze",7): [None],          # multiple_choice
    ("silver",0): [70, None],
    ("silver",1): [288, None],
    ("silver",2): [50000],
    ("silver",3): [3920000, None],
    ("silver",4): [450, None],
    ("silver",5): [None],
    ("gold",0):   [None, 17640],
    ("gold",1):   [None, 100000],
    ("gold",2):   [0.3, None],
    ("gold",3):   [26.79, 2295.92],
    ("gold",4):   [None],          # multiple_choice (rebuilt below)
    ("gold",5):   [None],          # multiple_choice
}

# ---------- hints per problem ----------
hints = {
    ("bronze",0): "Divide the useful heat by the total electrical energy.",
    ("bronze",1): "Divide useful by total, then multiply by 100 for a percentage.",
    ("bronze",2): "You can divide powers directly: useful power over total power.",
    ("bronze",3): "Divide the 12,000 J of KE by the 40,000 J input, then times 100.",
    ("bronze",4): "Turn 90% into 0.9, then multiply by the total input.",
    ("bronze",5): "Multiply the total input power by the efficiency.",
    ("bronze",6): "Wasted = total in − useful out.",
    ("bronze",7): "Work out useful ÷ total for each device, then compare.",
    ("silver",0): "Take BOTH wasted amounts off the input first, then divide.",
    ("silver",1): "Divide the useful output by the efficiency to get the bigger total.",
    ("silver",2): "Find the total input first (useful ÷ efficiency), then subtract the useful.",
    ("silver",3): "mgh each second is the input power; multiply it by the efficiency.",
    ("silver",4): "Find useful power (efficiency × total), then subtract from the total.",
    ("silver",5): "All the outputs must add up to the input; subtract the ones you know.",
    ("gold",0): "Find the GPE first (mgh), then divide it by the efficiency.",
    ("gold",1): "Square the speed for KE, then divide the KE by the efficiency.",
    ("gold",2): "Find the total power (useful ÷ efficiency), then divide by 800 for the area.",
    ("gold",3): "Convert minutes to seconds, find useful energy, then use mgh rearranged.",
    ("gold",4): "Useful energy = efficiency × power × time. Work both out and compare.",
    ("gold",5): "Think about conservation of energy and where wasted energy goes.",
}

# ---------- em-dash fix for existing messages ----------
def deem(s):
    return s.replace(" — ", ", ").replace("—", ", ")

# ---------- rebuild gold[4] as multiple_choice ----------
pb["gold"][4] = {
    "display": ("Kettle A is 88% efficient and takes 3 minutes to boil using 2000 W. "
        "Kettle B is 95% efficient and takes 3 minutes to boil using 1800 W. "
        "Which kettle transfers more useful energy to the water?"),
    "options": ["Kettle A", "Kettle B", "They transfer exactly the same amount",
                "You cannot tell without the water's mass"],
    "solutions": [0],
    "calculator": True,
    "input_type": "multiple_choice",
    "hint": hints[("gold",4)],
    "misconceptions": [{
        "pattern": "wrong_formula", "check": "common", "expect": None,
        "message": ("Kettle A: useful = 0.88 × 2000 × 180 = 316,800 J. "
            "Kettle B: useful = 0.95 × 1800 × 180 = 307,800 J. Even though B is more "
            "efficient, A transfers more useful energy because its power rating is higher."),
    }],
}

# ---------- apply expects, hints, guided_steps, em-dash fixes ----------
gsmap = {
    ("bronze",0):"b0",("bronze",1):"b1",("bronze",2):"b2",("bronze",3):"b3",
    ("bronze",4):"b4",("bronze",5):"b5",("bronze",6):"b6",
    ("silver",0):"s0",("silver",1):"s1",("silver",2):"s2",("silver",3):"s3",
    ("silver",4):"s4",("silver",5):"s5",
    ("gold",0):"g0",("gold",1):"g1",("gold",2):"g2",("gold",3):"g3",
}
for tier in ("bronze","silver","gold"):
    for i, pr in enumerate(pb[tier]):
        key = (tier, i)
        # hint
        pr["hint"] = hints[key]
        # em dash in messages
        for m in pr.get("misconceptions") or []:
            if "message" in m:
                m["message"] = deem(m["message"])
        # expects
        exp = expects.get(key)
        if exp is not None:
            ms = pr.get("misconceptions") or []
            assert len(exp) == len(ms), (key, len(exp), len(ms))
            for m, e in zip(ms, exp):
                m["expect"] = e
        # guided steps
        if key in gsmap:
            pr["guided_steps"] = gs[gsmap[key]]

# ---------- guided (opener + teach) ----------
pd["guided"] = {
    "opener": {
        "title": "How much actually gets through?",
        "display": ("An old light bulb is like a leaky bucket. You pour in <strong>100 joules</strong> "
            "of electrical energy, but only <strong>10 joules</strong> come out as light. The other "
            "90 joules leak away as heat you can feel on the glass."),
        "steps": [
            bx("Out of every 100 J you put in, how many joules come out as useful light? ", 10,
               "It is given in the story: the light output is 10 J."),
            bx("So the useful fraction is 10 out of 100. As a decimal, 10 ÷ 100 = ", 0.1,
               "Ten hundredths."),
            sy("That number, 0.1, is the bulb's <strong>efficiency</strong>: useful out ÷ total in. "
               "Every question in this lesson is that one idea, " + EQ + ", sometimes turned around to "
               "find a missing piece."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "A torch takes in 60 J of energy and gives out 45 J as light. Find its efficiency.",
            "steps": [
                sy("Efficiency is useful ÷ total: " + EQ + "."),
                bx("Useful output (the light), in J = ", 45, "The energy you want out: 45 J."),
                bx("Total input, in J = ", 60, "Everything put in: 60 J."),
                bx("Divide: 45 ÷ 60 = ", 0.75, "Useful over total."),
                bx("Check: 0.75 × 60 = ", 45, "Should return the useful output.",
                   done="Gone. Useful over total, that is the whole method."),
                sy("So the efficiency is <strong>0.75</strong> (75%)."),
            ],
        },
        "silver": {
            "display": ("A fan heater takes in 3000 J. It wastes 600 J as sound and light, and the "
                "rest becomes useful heat. Find its efficiency as a percentage."),
            "steps": [
                sy("Silver adds a step: work out the useful energy before you divide."),
                bx("Total input, in J = ", 3000, "Everything supplied: 3000 J."),
                bx("Useful = total − wasted: 3000 − 600 = ", 2400, "Take the wasted energy off the input."),
                bx("Divide: 2400 ÷ 3000 = ", 0.8, "Useful over total."),
                bx("As a percentage: 0.8 × 100 = ", 80, "Multiply by 100.",
                   done="The extra move was just finding the useful energy first."),
                sy("So the efficiency is <strong>80%</strong>."),
            ],
        },
        "gold": {
            "display": ("A winch motor is 0.60 efficient. It lifts a 50 kg load to a height of 12 m. "
                "Find the total electrical energy it uses. (g = 9.8 N/kg)"),
            "steps": [
                sy("Gold chains two equations. First the useful output, the GPE: \\(E_p = mgh\\)."),
                bx("m × g: 50 × 9.8 = ", 490, "Mass times gravitational field strength."),
                bx("× h: 490 × 12 = ", 5880, "Multiply by the height to get the GPE."),
                sy("Now rearrange efficiency: total input = useful ÷ efficiency."),
                bx("Divide: 5880 ÷ 0.60 = ", 9800, "Useful over efficiency."),
                bx("Check: 0.60 × 9800 = ", 5880, "Should return the GPE.",
                   done="Back to 5880 J, so the input is right."),
                sy("So the total electrical energy input is <strong>9800 J</strong>."),
            ],
        },
    },
}

# ---------- tier_guides ----------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one efficiency equation",
        "steps": [
            "Write <strong>efficiency = useful output ÷ total input</strong>.",
            "Put the useful energy (or power) on top, the total underneath, and divide.",
            "For a percentage, multiply the decimal by 100. Efficiency is always below 1 (100%).",
        ],
        "example": {
            "question": "A lamp takes in 50 J and gives out 20 J of light. Find its efficiency.",
            "steps": [
                {"label": "Divide useful by total", "content": "20 ÷ 50 = 0.4"},
                {"label": "Check", "content": "0.4 × 50 = 20 ✓"},
                {"label": "Answer", "content": "Efficiency = 0.4 (40%)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: one move before you divide",
        "steps": [
            "Sometimes find the useful energy first: useful = total − wasted.",
            "Sometimes rearrange: total input = useful ÷ efficiency, or useful = efficiency × total.",
            "Then finish the division (or subtraction) and give a unit or percentage.",
        ],
        "example": {
            "question": "A motor takes in 800 J and wastes 200 J. Find its efficiency.",
            "steps": [
                {"label": "Useful first", "content": "800 − 200 = 600 J"},
                {"label": "Divide", "content": "600 ÷ 800 = 0.75"},
                {"label": "Check", "content": "0.75 × 800 = 600 ✓"},
                {"label": "Answer", "content": "0.75 (75%)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chain two equations",
        "steps": [
            "First find the useful energy: KE (\\(\\frac{1}{2}mv^2\\)), GPE (\\(mgh\\)), or power × time.",
            "Then use efficiency to reach the missing quantity, rearranging to total = useful ÷ efficiency where needed.",
            "Convert units first (minutes to seconds), and keep energy with energy, power with power.",
        ],
        "example": {
            "question": "A hoist is 0.50 efficient and lifts 20 kg to 5 m. Find the energy input. (g = 9.8 N/kg)",
            "steps": [
                {"label": "GPE", "content": "20 × 9.8 × 5 = 980 J"},
                {"label": "Rearrange", "content": "input = 980 ÷ 0.50 = 1960 J"},
                {"label": "Check", "content": "0.50 × 1960 = 980 ✓"},
                {"label": "Answer", "content": "1960 J", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

with open("lesson_physics-calculations-L02@d5abd25397.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("built OK")
