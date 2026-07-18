# -*- coding: utf-8 -*-
import json, io

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayx(s): return {"say": s}

pd = {}

# ---------------- method_card (slim, no em dash, board-neutral) ----------------
pd["method_card"] = {
    "title": "Energy: KE, GPE and Power",
    "steps": [
        "Decide what you are finding, then choose the matching equation.",
        "Convert every value to base units first: kg, metres, seconds.",
        "Substitute and calculate.",
        "State the answer with its unit (J for energy, W for power)."
    ],
    "content": ("<p>Five recall equations: kinetic energy \\(E_k = \\frac{1}{2}mv^2\\), "
                "gravitational PE \\(E_p = mgh\\), work \\(W = Fs\\), and power \\(P = \\frac{E}{t}\\). "
                "Check whether your board gives you these; knowing them from memory always saves time.</p>"
                "<p>Watch the traps: speed is squared, so doubling it quadruples the KE; convert grams "
                "to kilograms and minutes to seconds before substituting; use \\(g = 9.8\\) N/kg unless "
                "told otherwise.</p>")
}

pd["topic_links"] = {"prerequisites": []}

pd["exam_context"] = {
    "marks": "3–5 per calculation",
    "paper": "Paper 1 (Physics)",
    "frequency": "Very common. Energy calculations appear on almost every Paper 1."
}

# ---------------- tier_guides ----------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one equation, straight in",
        "steps": [
            "Pick the equation the quantity needs: kinetic energy \\(E_k = \\frac{1}{2}mv^2\\), gravitational PE \\(E_p = mgh\\), work \\(W = Fs\\), or power \\(P = \\frac{E}{t}\\).",
            "Substitute the numbers exactly as given, then calculate.",
            "Write the answer with its unit: joules (J) for energy, watts (W) for power."
        ],
        "example": {
            "question": "A 4 kg box is lifted 3 m. Calculate the GPE gained. (g = 9.8 N/kg)",
            "steps": [
                {"label": "Equation", "content": "\\(E_p = mgh\\)"},
                {"label": "Substitute", "content": "4 × 9.8 × 3"},
                {"label": "Check", "content": "Units: kg × N/kg × m = J"},
                {"label": "Answer", "content": "<strong>117.6 J</strong>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: convert first, or rearrange first",
        "steps": [
            "If a value is not in the base unit, convert before you substitute: grams to kilograms (÷1000), minutes to seconds (×60), kilojoules to joules (×1000).",
            "If the unknown is not the subject, rearrange the equation first, then substitute.",
            "Give the answer in the unit the question asks for."
        ],
        "example": {
            "question": "A 250 g ball moves at 6 m/s. Calculate its kinetic energy.",
            "steps": [
                {"label": "Convert", "content": "250 g = 0.25 kg"},
                {"label": "Substitute", "content": "½ × 0.25 × 6² = ½ × 0.25 × 36"},
                {"label": "Check", "content": "0.125 × 36"},
                {"label": "Answer", "content": "<strong>4.5 J</strong>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: two steps chained",
        "steps": [
            "These need two equations or two stages. Finish the first fully before starting the second.",
            "Energy is conserved: GPE lost becomes KE gained, so \\(mgh = \\frac{1}{2}mv^2\\) lets you find a speed.",
            "For efficiency, divide the useful energy by the total energy, then multiply by 100 for a percentage."
        ],
        "example": {
            "question": "A 2 kg ball falls from 10 m. Find its speed at the bottom. (g = 9.8 N/kg)",
            "steps": [
                {"label": "GPE", "content": "2 × 9.8 × 10 = 196 J"},
                {"label": "Set equal", "content": "½ × 2 × v² = 196, so v² = 196"},
                {"label": "Check", "content": "√196 = 14, and ½ × 2 × 14² = 196"},
                {"label": "Answer", "content": "<strong>14 m/s</strong>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------- guided (opener + teach) ----------------
pd["guided"] = {
    "opener": {
        "steps": [
            sayx("Two identical cars crash into a wall. Car A is going 15 mph. Car B is going 30 mph, exactly twice as fast."),
            box("Car B is travelling how many times as fast as Car A? ", 2, "30 is double 15."),
            sayx("You might guess the crash is twice as bad. It is worse than that. Energy depends on the speed <strong>squared</strong>, so doubling the speed multiplies the energy by 2 × 2."),
            box("So 2 squared = ", 4, "2 × 2."),
            sayx("Four times the energy, four times the damage. That squared speed is the heart of the kinetic energy equation, \\(E_k = \\frac{1}{2}mv^2\\). This lesson uses it alongside four partner equations for energy and power.")
        ]
    },
    "teach": {
        "bronze": {
            "display": "A 2 kg ball moves at 3 m/s. Calculate its kinetic energy.",
            "steps": [
                sayx("Kinetic energy needs the speed squared: \\(E_k = \\frac{1}{2}mv^2\\)."),
                box("Square the speed: 3² = ", 9, "3 × 3."),
                box("Half the mass: ½ × 2 = ", 1, "Halve 2."),
                box("Multiply: 1 × 9 = ", 9, "1 × 9.", done="That is the kinetic energy, 9 J."),
                box("Check by recovering the speed: √(2 × 9 ÷ 2) = ", 3, "This should give back 3.", done="Back to 3 m/s, so 9 J is right.")
            ]
        },
        "silver": {
            "display": "A 500 g trolley moves at 4 m/s. Calculate its kinetic energy.",
            "steps": [
                sayx("The mass is in grams, but the equation needs kilograms. Convert first."),
                box("Mass in kg: 500 ÷ 1000 = ", 0.5, "1000 g = 1 kg."),
                box("Square the speed: 4² = ", 16, "4 × 4."),
                box("Half the mass: ½ × 0.5 = ", 0.25, "Halve 0.5."),
                box("Multiply: 0.25 × 16 = ", 4, "0.25 × 16.", done="4 J. The only new move was the gram-to-kilogram conversion.")
            ]
        },
        "gold": {
            "display": "A 3 kg rock falls from a height of 10 m. Calculate its speed just before it lands, assuming all GPE becomes KE. (g = 9.8 N/kg)",
            "steps": [
                sayx("Two steps. First the GPE at the top, then set it equal to KE to find the speed."),
                box("GPE = mgh = 3 × 9.8 × 10 = ", 294, "Multiply the three numbers."),
                box("Set ½ × 3 × v² = 294, so first 2 × 294 = ", 588, "Double both sides."),
                box("Divide by the mass: 588 ÷ 3 = ", 196, "That gives v².", done="v² = 196."),
                box("v = √196 = ", 14, "Square root of 196."),
                box("Check the KE: ½ × 3 × 196 = ", 294, "Recompute the KE.", done="Matches the GPE, so 14 m/s is right.")
            ]
        }
    }
}

# ---------------- problem_bank ----------------
pb = {}
pb["bronze_description"] = "One equation, all values already in the right units. Recall it, substitute, and calculate."
pb["silver_description"] = "Convert a unit first (grams to kilograms, minutes to seconds, joules to kilojoules) or rearrange the equation before you substitute."
pb["gold_description"] = "Chain two steps: convert energy between GPE and KE, find work from a change in KE, or work out an efficiency or a difference."

def mis(pattern, message, expect):
    return {"pattern": pattern, "message": message, "expect": expect}

# ===== BRONZE =====
bronze = []

bronze.append({
    "unit": "J",
    "display": "A car has a mass of 1200 kg and travels at 15 m/s. Calculate its kinetic energy.",
    "solutions": [135000], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(E_k = \\frac{1}{2}mv^2\\)",
    "misconceptions": [
        mis("forgot_square", "Square the speed first: 15² = 225. Then KE = ½ × 1200 × 225 = 135,000 J.", 9000),
        mis("forgot_half", "Do not forget the ½. KE = ½ × 1200 × 225 = 135,000 J, not 270,000 J.", 270000),
    ],
    "hint": "Square the speed, then multiply by half the mass.",
    "guided_steps": [
        sayx("Kinetic energy needs the speed squared: \\(E_k = \\frac{1}{2}mv^2\\)."),
        box("Square the speed: 15² = ", 225, "15 × 15."),
        box("Half the mass: ½ × 1200 = ", 600, "Halve 1200.", phase="substitute"),
        box("Multiply: 600 × 225 = ", 135000, "600 × 225.", phase="substitute", done="135,000 J."),
        box("Check by recovering the speed: √(2 × 135000 ÷ 1200) = ", 15, "This should give back 15.", phase="substitute", done="Back to 15 m/s, so 135,000 J is right."),
    ],
})

bronze.append({
    "unit": "J",
    "display": "A 0.5 kg ball is held 4 m above the ground. Calculate its gravitational potential energy. (g = 9.8 N/kg)",
    "solutions": [19.6], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(E_p = mgh\\)",
    "misconceptions": [
        mis("wrong_formula", "Use GPE = mgh = 0.5 × 9.8 × 4 = 19.6 J. This is a mass held above the ground, so it stores gravitational PE, not KE.", None),
    ],
    "hint": "Multiply mass by g, then by height.",
    "guided_steps": [
        sayx("Lifting something gives it gravitational PE: \\(E_p = mgh\\)."),
        box("Mass × g: 0.5 × 9.8 = ", 4.9, "0.5 × 9.8."),
        box("Now × height: 4.9 × 4 = ", 19.6, "4.9 × 4.", phase="substitute", done="19.6 J."),
        box("Check: 19.6 ÷ 4 ÷ 0.5 recovers g = ", 9.8, "Divide back by height then mass.", phase="substitute", done="Gives 9.8 N/kg, so 19.6 J is right."),
    ],
})

bronze.append({
    "unit": "J",
    "display": "A force of 50 N pushes a box 8 m along the floor. Calculate the work done.",
    "solutions": [400], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(W = Fs\\)",
    "misconceptions": [
        mis("wrong_formula", "Work done = force × distance = 50 × 8 = 400 J.", None),
    ],
    "hint": "Work done is force times distance.",
    "guided_steps": [
        sayx("Work done is force times distance: \\(W = Fs\\)."),
        box("Write the force: F = ", 50, "It is given as 50 N."),
        box("Work = force × distance = 50 × 8 = ", 400, "50 × 8.", phase="substitute", done="400 J."),
        box("Check: 400 ÷ 8 recovers the force = ", 50, "Divide back by the distance.", phase="substitute", done="Recovers 50 N, so 400 J is right."),
    ],
})

bronze.append({
    "unit": "W",
    "display": "A kettle transfers 180,000 J of energy in 3 minutes. Calculate its power in watts.",
    "solutions": [1000], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(P = \\frac{E}{t}\\)",
    "misconceptions": [
        mis("unit_error", "Convert minutes to seconds first: 3 min = 180 s. P = 180,000 ÷ 180 = 1000 W. Dividing by 3 gives 60,000 W, which is far too big.", 60000),
    ],
    "hint": "Convert minutes to seconds, then divide energy by time.",
    "guided_steps": [
        sayx("Power is energy per second: \\(P = \\frac{E}{t}\\). Time must be in seconds."),
        box("Time in seconds: 3 × 60 = ", 180, "1 minute = 60 seconds."),
        box("Power = 180000 ÷ 180 = ", 1000, "180000 ÷ 180.", phase="substitute", done="1000 W."),
        box("Check: 1000 × 180 recovers the energy = ", 180000, "Multiply back by the time.", phase="substitute", done="Recovers 180,000 J, so 1000 W is right."),
    ],
})

bronze.append({
    "unit": "J",
    "display": "A runner of mass 60 kg sprints at 8 m/s. Calculate their kinetic energy.",
    "solutions": [1920], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(E_k = \\frac{1}{2}mv^2\\)",
    "misconceptions": [
        mis("forgot_square", "Square the speed: 8² = 64. KE = ½ × 60 × 64 = 1920 J. Forgetting to square gives 240 J.", 240),
    ],
    "hint": "Square the speed, then multiply by half the mass.",
    "guided_steps": [
        sayx("Kinetic energy: \\(E_k = \\frac{1}{2}mv^2\\)."),
        box("Square the speed: 8² = ", 64, "8 × 8."),
        box("Half the mass: ½ × 60 = ", 30, "Halve 60.", phase="substitute"),
        box("Multiply: 30 × 64 = ", 1920, "30 × 64.", phase="substitute", done="1920 J."),
        box("Check by recovering the speed: √(2 × 1920 ÷ 60) = ", 8, "This should give back 8.", phase="substitute", done="Back to 8 m/s, so 1920 J is right."),
    ],
})

bronze.append({
    "unit": "J",
    "display": "A bag of mass 3 kg is lifted onto a shelf 2.5 m high. Calculate the GPE gained. (g = 9.8 N/kg)",
    "solutions": [73.5], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(E_p = mgh\\)",
    "misconceptions": [
        mis("wrong_formula", "GPE = mgh = 3 × 9.8 × 2.5 = 73.5 J.", None),
    ],
    "hint": "Multiply mass by g, then by height.",
    "guided_steps": [
        sayx("Lifting gives gravitational PE: \\(E_p = mgh\\)."),
        box("Mass × g: 3 × 9.8 = ", 29.4, "3 × 9.8."),
        box("Now × height: 29.4 × 2.5 = ", 73.5, "29.4 × 2.5.", phase="substitute", done="73.5 J."),
        box("Check: 73.5 ÷ 2.5 ÷ 3 recovers g = ", 9.8, "Divide back by height then mass.", phase="substitute", done="Gives 9.8 N/kg, so 73.5 J is right."),
    ],
})

bronze.append({
    "unit": "W",
    "display": "A motor does 5000 J of work in 20 seconds. Calculate its power.",
    "solutions": [250], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(P = \\frac{E}{t}\\)",
    "misconceptions": [
        mis("inverse_error", "Power = energy ÷ time = 5000 ÷ 20 = 250 W. Multiplying instead gives 100,000, which is not a power.", 100000),
    ],
    "hint": "Divide the energy by the time.",
    "guided_steps": [
        sayx("Power is energy per second: \\(P = \\frac{E}{t}\\)."),
        box("Write the energy: E = ", 5000, "Given as 5000 J."),
        box("Power = 5000 ÷ 20 = ", 250, "Divide, do not multiply.", phase="substitute", done="250 W."),
        box("Check: 250 × 20 recovers the energy = ", 5000, "Multiply back by the time.", phase="substitute", done="Recovers 5000 J, so 250 W is right."),
    ],
})

bronze.append({
    "display": "Which equation would you use to calculate the energy stored by an object lifted above the ground?",
    "options": ["\\(E_k = \\frac{1}{2}mv^2\\)", "\\(E_p = mgh\\)", "\\(P = \\frac{E}{t}\\)", "\\(W = Fs\\)"],
    "solutions": [1], "calculator": False, "input_type": "multiple_choice",
    "hint": "Above the ground means gravitational potential energy.",
    "misconceptions": [
        mis("wrong_equation", "An object above the ground has gravitational PE. Use \\(E_p = mgh\\). KE is for moving objects.", None),
    ],
})

pb["bronze"] = bronze

# ===== SILVER =====
silver = []

silver.append({
    "unit": "kJ", "accept": 0.01,
    "display": "A cyclist and bike have a combined mass of 80 kg and travel at 12 m/s. Calculate the kinetic energy in kJ.",
    "solutions": [5.76], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(E_k = \\frac{1}{2}mv^2\\)",
    "misconceptions": [
        mis("unit_error", "KE = ½ × 80 × 12² = 5760 J. The question asks for kJ: 5760 ÷ 1000 = 5.76 kJ.", 5760),
        mis("forgot_square", "Square the speed first: 12² = 144. Then ½ × 80 × 144 = 5760 J = 5.76 kJ. Forgetting to square gives 0.48 kJ.", 0.48),
    ],
    "hint": "Work out the KE in joules, then convert to kilojoules.",
    "guided_steps": [
        sayx("Kinetic energy in joules first, then convert to kilojoules."),
        box("Square the speed: 12² = ", 144, "12 × 12."),
        box("Half the mass: ½ × 80 = ", 40, "Halve 80."),
        box("KE in joules: 40 × 144 = ", 5760, "40 × 144.", phase="substitute"),
        box("Convert to kJ: 5760 ÷ 1000 = ", 5.76, "1 kJ = 1000 J.", phase="substitute", done="5.76 kJ."),
        box("Check: 5.76 × 1000 back to joules = ", 5760, "Multiply back up.", phase="substitute", done="Recovers 5760 J, so 5.76 kJ is right."),
    ],
})

silver.append({
    "unit": "kJ",
    "display": "A 60 W light bulb is left on for 2 hours. Calculate the energy transferred in kJ.",
    "solutions": [432], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(E = Pt\\)",
    "misconceptions": [
        mis("unit_error", "Convert hours to seconds: 2 h = 7200 s. E = 60 × 7200 = 432,000 J = 432 kJ. Leaving the answer in joules gives 432,000.", 432000),
    ],
    "hint": "Convert hours to seconds, then convert the answer to kJ.",
    "guided_steps": [
        sayx("Energy transferred: \\(E = Pt\\). Time in seconds, then convert joules to kilojoules."),
        box("Time in seconds: 2 × 3600 = ", 7200, "1 hour = 3600 seconds."),
        box("Energy in joules: 60 × 7200 = ", 432000, "60 × 7200.", phase="substitute"),
        box("Convert to kJ: 432000 ÷ 1000 = ", 432, "Divide by 1000.", phase="substitute", done="432 kJ."),
        box("Check: 432000 ÷ 7200 recovers the power = ", 60, "Divide the joules by the time.", phase="substitute", done="Gives 60 W, so 432 kJ is right."),
    ],
})

silver.append({
    "unit": "J",
    "display": "A crane lifts a 400 kg load to a height of 15 m. Calculate the work done by the crane. (g = 9.8 N/kg)",
    "solutions": [58800], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(W = Fs\\) and \\(W = mg\\)",
    "misconceptions": [
        mis("forgot_step", "First find the weight to lift: W = mg = 400 × 9.8 = 3920 N. Then work = Fs = 3920 × 15 = 58,800 J. Using the mass as the force gives 6000 J.", 6000),
    ],
    "hint": "Find the weight first, then multiply by the height.",
    "guided_steps": [
        sayx("Work against gravity: first the weight \\(W = mg\\), then work \\(W = Fs\\)."),
        box("Weight: 400 × 9.8 = ", 3920, "Mass × g."),
        box("Work = force × distance = 3920 × 15 = ", 58800, "3920 × 15.", phase="substitute", done="58,800 J."),
        box("Check: 58800 ÷ 15 recovers the weight = ", 3920, "Divide back by the height.", phase="substitute", done="Recovers 3920 N, so 58,800 J is right."),
    ],
})

silver.append({
    "unit": "J",
    "display": "A car of mass 900 kg accelerates from rest to 30 m/s. Calculate the work done on the car.",
    "solutions": [405000], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(E_k = \\frac{1}{2}mv^2\\)",
    "misconceptions": [
        mis("wrong_formula", "Work done = the KE gained = ½ × 900 × 30² = 405,000 J. It starts from rest, so there is no KE to subtract.", None),
        mis("forgot_square", "Square the speed: 30² = 900. KE = ½ × 900 × 900 = 405,000 J. Forgetting to square gives 13,500 J.", 13500),
    ],
    "hint": "Work done equals the kinetic energy gained from rest.",
    "guided_steps": [
        sayx("Work done equals the KE gained: \\(\\frac{1}{2}mv^2\\), since it starts from rest."),
        box("Square the speed: 30² = ", 900, "30 × 30."),
        box("Half the mass: ½ × 900 = ", 450, "Halve 900."),
        box("Multiply: 450 × 900 = ", 405000, "450 × 900.", phase="substitute", done="405,000 J."),
        box("Check by recovering the speed: √(2 × 405000 ÷ 900) = ", 30, "This should give back 30.", phase="substitute", done="Back to 30 m/s, so 405,000 J is right."),
    ],
})

silver.append({
    "unit": "m", "accept": 0.1,
    "display": "A 1500 W motor lifts a 50 kg mass. How high can it lift the mass in 10 seconds? Give your answer to 1 d.p. (g = 9.8 N/kg)",
    "solutions": [30.6], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(E = Pt\\) and \\(E_p = mgh\\)",
    "misconceptions": [
        mis("wrong_rearrange", "Energy = Pt = 15,000 J. Height = E ÷ (mg) = 15,000 ÷ 490 = 30.6 m. Dividing by the mass alone (forgetting g) gives 300 m.", 300),
    ],
    "hint": "Find the energy from Pt, then rearrange mgh to h = E divided by mg.",
    "guided_steps": [
        sayx("Two equations: energy in from \\(E = Pt\\), then height from \\(E_p = mgh\\) rearranged to \\(h = \\frac{E}{mg}\\)."),
        box("Energy in: 1500 × 10 = ", 15000, "P × t."),
        box("Weight: 50 × 9.8 = ", 490, "Mass × g."),
        box("Height: 15000 ÷ 490, rounded to 1 d.p. = ", 30.6, "Divide, then round to 1 d.p.", phase="substitute", done="30.6 m."),
        box("Check: 490 × 30.6 = ", 14994, "Weight × height recovers the energy, close to 15,000.", phase="substitute", done="About 15,000 J, so 30.6 m is right."),
    ],
})

silver.append({
    "unit": "J",
    "display": "A 200 g tennis ball is served at 50 m/s. Calculate its kinetic energy.",
    "solutions": [250], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(E_k = \\frac{1}{2}mv^2\\)",
    "misconceptions": [
        mis("unit_error", "Convert grams to kilograms: 200 g = 0.2 kg. KE = ½ × 0.2 × 50² = 250 J. Leaving the mass in grams gives 250,000 J.", 250000),
    ],
    "hint": "Convert the mass to kilograms first, then square the speed.",
    "guided_steps": [
        sayx("Kinetic energy: convert the mass to kilograms first."),
        box("Mass in kg: 200 ÷ 1000 = ", 0.2, "1000 g = 1 kg."),
        box("Square the speed: 50² = ", 2500, "50 × 50."),
        box("Half the mass: ½ × 0.2 = ", 0.1, "Halve 0.2.", phase="substitute"),
        box("Now × 2500: 0.1 × 2500 = ", 250, "0.1 × 2500.", phase="substitute", done="250 J."),
        box("Check by recovering the speed: √(2 × 250 ÷ 0.2) = ", 50, "This should give back 50.", phase="substitute", done="Back to 50 m/s, so 250 J is right."),
    ],
})

pb["silver"] = silver

# ===== GOLD =====
gold = []

gold.append({
    "unit": "m/s", "accept": 0.5,
    "display": "A skydiver of mass 75 kg falls from 4000 m to 3000 m. Calculate the speed they would reach if all the lost GPE converted to KE. (g = 9.8 N/kg)",
    "solutions": [140], "calculator": True, "input_type": "single_value",
    "misconceptions": [
        mis("wrong_rearrange", "GPE lost = mgh = 75 × 9.8 × 1000 = 735,000 J. Set ½mv² = 735,000, so v² = 2 × 735,000 ÷ 75 = 19,600 and v = 140 m/s. Forgetting the 2 gives about 99 m/s.", 98.99),
        mis("forgot_step", "Use the height dropped (4000 − 3000 = 1000 m), not the total 4000 m. Using 4000 m gives 280 m/s.", 280),
    ],
    "hint": "Find the GPE lost over the 1000 m drop, then solve half m v squared for v.",
    "guided_steps": [
        sayx("All the lost GPE becomes KE. Find the GPE dropped, then solve \\(\\frac{1}{2}mv^2\\) for v."),
        box("Height dropped: 4000 − 3000 = ", 1000, "The difference in height."),
        box("GPE lost: 75 × 9.8 × 1000 = ", 735000, "mgh."),
        box("Rearrange: v² = 2 × 735000 ÷ 75 = ", 19600, "Double it, then divide by the mass.", phase="substitute"),
        box("v = √19600 = ", 140, "Square root.", phase="substitute", done="140 m/s."),
        box("Check the KE: ½ × 75 × 140² = ", 735000, "Recompute the KE.", phase="substitute", done="Matches the GPE lost, so 140 m/s is right."),
    ],
})

gold.append({
    "unit": "J",
    "display": "A car of mass 1100 kg travels at 20 m/s. The driver brakes, and the car decelerates to 8 m/s. Calculate the work done by the brakes.",
    "solutions": [184800], "calculator": True, "input_type": "single_value",
    "misconceptions": [
        mis("forgot_step", "Find the KE at both speeds and subtract: ½ × 1100 × 20² = 220,000 J and ½ × 1100 × 8² = 35,200 J, so work = 184,800 J. Squaring the difference (12²) gives 79,200 J, which is wrong.", 79200),
    ],
    "hint": "Work done is the kinetic energy lost: KE at 20 minus KE at 8.",
    "guided_steps": [
        sayx("Work done by the brakes is the KE lost: \\(\\frac{1}{2}mv^2\\) before minus after."),
        box("KE at 20 m/s: ½ × 1100 × 20² = ½ × 1100 × 400 = ", 220000, "Square 20 first."),
        box("KE at 8 m/s: ½ × 1100 × 8² = ½ × 1100 × 64 = ", 35200, "Square 8 first."),
        box("Work done = 220000 − 35200 = ", 184800, "Subtract the smaller from the larger.", phase="substitute", done="184,800 J."),
        box("Check: 35200 + 184800 = ", 220000, "Add back to the starting KE.", phase="substitute", done="Recovers 220,000 J, so 184,800 J is right."),
    ],
})

gold.append({
    "unit": "%", "accept": 1,
    "display": "An electric motor has a power rating of 2.5 kW. It lifts an 80 kg object 6 m in 4 seconds. Calculate the efficiency of the motor. Give your answer as a percentage. (g = 9.8 N/kg)",
    "solutions": [47.04], "calculator": True, "input_type": "single_value",
    "misconceptions": [
        mis("unit_error", "Convert kW to W: 2.5 kW = 2500 W, so total input = 2500 × 4 = 10,000 J. Leaving it as 2.5 gives a total input of 10 J and an impossible 47,040%.", 47040),
        mis("wrong_rearrange", "Efficiency = useful ÷ total × 100 = 4704 ÷ 10,000 × 100 = 47.04%. Dividing total by useful instead gives about 212%.", 212.59),
    ],
    "hint": "Useful output is the GPE gained; total input is power times time.",
    "guided_steps": [
        sayx("Efficiency = useful output ÷ total input × 100. Useful output is the GPE gained; total input is \\(Pt\\)."),
        box("Useful output (GPE): 80 × 9.8 × 6 = ", 4704, "mgh."),
        box("Total input: 2.5 kW = 2500 W, then 2500 × 4 = ", 10000, "Convert to watts, then × time."),
        box("Efficiency = 4704 ÷ 10000 × 100 = ", 47.04, "Divide, then × 100.", phase="substitute", done="47.04%."),
        box("Check: 10000 × 0.4704 = ", 4704, "Total input × the efficiency fraction recovers the useful output.", phase="substitute", done="Recovers 4704 J, so 47.04% is right."),
    ],
})

gold.append({
    "unit": "W",
    "display": "Two students climb the same flight of stairs (height 4 m). Student A has mass 50 kg and takes 5 seconds. Student B has mass 70 kg and takes 8 seconds. Calculate the difference in their power output. (g = 9.8 N/kg)",
    "solutions": [49], "calculator": True, "input_type": "single_value",
    "misconceptions": [
        mis("forgot_step", "Power, not energy: divide each student's work by their time. P_A = 1960 ÷ 5 = 392 W, P_B = 2744 ÷ 8 = 343 W, difference = 49 W. Comparing energies (2744 − 1960) gives 784.", 784),
    ],
    "hint": "Work out each student's power with mgh divided by time, then subtract.",
    "guided_steps": [
        sayx("Find each student's power with \\(P = \\frac{mgh}{t}\\), then subtract."),
        box("Student A: (50 × 9.8 × 4) ÷ 5 = ", 392, "Work done ÷ time."),
        box("Student B: (70 × 9.8 × 4) ÷ 8 = ", 343, "Work done ÷ time."),
        box("Difference = 392 − 343 = ", 49, "Larger minus smaller.", phase="substitute", done="49 W."),
        box("Check: 343 + 49 = ", 392, "Add back to Student B's power.", phase="substitute", done="Recovers 392 W, so 49 W is right."),
    ],
})

gold.append({
    "unit": "J", "accept": 0.1,
    "display": "A ball of mass 0.3 kg is dropped from a height of 10 m. It bounces back to a height of 6 m. Calculate the energy dissipated during the bounce. (g = 9.8 N/kg)",
    "solutions": [11.76], "calculator": True, "input_type": "single_value",
    "misconceptions": [
        mis("forgot_step", "Energy dissipated is the GPE lost: mgh before minus mgh after = 29.4 − 17.64 = 11.76 J. Quoting only the starting GPE gives 29.4 J.", 29.4),
    ],
    "hint": "Find the GPE before and after, then subtract.",
    "guided_steps": [
        sayx("Energy dissipated is the GPE lost: mgh before the bounce minus mgh after."),
        box("GPE before: 0.3 × 9.8 × 10 = ", 29.4, "mgh at 10 m."),
        box("GPE after: 0.3 × 9.8 × 6 = ", 17.64, "mgh at 6 m."),
        box("Dissipated = 29.4 − 17.64 = ", 11.76, "Subtract.", phase="substitute", done="11.76 J."),
        box("Check: 17.64 + 11.76 = ", 29.4, "Add back to the bounce GPE.", phase="substitute", done="Recovers 29.4 J, so 11.76 J is right."),
    ],
})

gold.append({
    "display": "A wind turbine generates 1.5 MW of power. How much energy does it transfer in one day? Give your answer in standard form.",
    "solutions": [1.296, 11], "calculator": True, "input_type": "standard_form",
    "misconceptions": [
        mis("unit_error", "Convert first: 1.5 MW = 1,500,000 W and one day = 86,400 s. E = Pt = 1,500,000 × 86,400 = 1.296 × 10¹¹ J.", None),
    ],
    "hint": "Convert MW to watts and one day to seconds, then multiply.",
    "guided_steps": [
        sayx("Energy is \\(E = Pt\\). Convert the power to watts and one day to seconds first."),
        box("1.5 MW in watts: 1.5 × 1000000 = ", 1500000, "Mega means a million."),
        box("One day in seconds: 24 × 60 × 60 = ", 86400, "Hours × minutes × seconds."),
        box("Energy: 1500000 × 86400 = ", 129600000000, "Multiply the two.", phase="substitute"),
        box("In standard form, the power of 10 is ", 11, "Move the point 11 places left from 129,600,000,000.", phase="substitute"),
        box("and the number in front (between 1 and 10) is ", 1.296, "Put the decimal after the first digit.", phase="substitute", done="So E = 1.296 × 10¹¹ J."),
    ],
})

pb["gold"] = gold

pd["problem_bank"] = pb
pd["related_videos"] = []

# ---------------- worked_examples (fix em dashes in labels) ----------------
pd["worked_examples"] = [
    {
        "steps": [
            {"label": "Step 1: Recall the equation", "content": "<p>\\(E_k = \\frac{1}{2}mv^2\\)</p>"},
            {"label": "Step 2: Substitute", "content": "<p>\\(E_k = \\frac{1}{2} \\times 0.4 \\times 10^2 = \\frac{1}{2} \\times 0.4 \\times 100\\)</p>"},
            {"label": "Answer", "content": "<p>\\(E_k = 20\\) <strong>J</strong></p>", "is_answer": True},
        ],
        "question": "A ball of mass 0.4 kg is thrown at a speed of 10 m/s. Calculate its kinetic energy.",
        "difficulty": "Bronze",
    },
    {
        "steps": [
            {"label": "Step 1: Find the energy transferred (GPE)", "content": "<p>\\(E_p = mgh = 250 \\times 9.8 \\times 12 = 29{,}400\\) J</p>"},
            {"label": "Step 2: Use the power equation", "content": "<p>\\(P = \\frac{E}{t} = \\frac{29{,}400}{30}\\)</p>"},
            {"label": "Answer", "content": "<p>\\(P = 980\\) <strong>W</strong></p>", "is_answer": True},
        ],
        "question": "A crane lifts a 250 kg beam to a height of 12 m in 30 seconds. Calculate the power of the crane. (g = 9.8 N/kg)",
        "difficulty": "Silver",
    },
    {
        "steps": [
            {"label": "Step 1: Calculate GPE at the top", "content": "<p>\\(E_p = mgh = 500 \\times 9.8 \\times 40 = 196{,}000\\) J</p>"},
            {"label": "Step 2: Set GPE = KE and rearrange for v", "content": "<p>\\(\\frac{1}{2}mv^2 = 196{,}000\\)</p><p>\\(v^2 = \\frac{2 \\times 196{,}000}{500} = 784\\)</p>"},
            {"label": "Answer", "content": "<p>\\(v = \\sqrt{784} = 28\\) <strong>m/s</strong></p>", "is_answer": True},
        ],
        "question": "A roller coaster car of mass 500 kg is at the top of a 40 m hill. Calculate its speed at the bottom, assuming all GPE converts to KE. (g = 9.8 N/kg)",
        "difficulty": "Gold",
    },
]

# ---------------- verify worked_examples arithmetic ----------------
assert 0.5*0.4*10**2 == 20
assert 250*9.8*12 == 29400 and 29400/30 == 980
assert 500*9.8*40 == 196000 and (2*196000/500) == 784 and 784**0.5 == 28

out = "lesson_physics-calculations-L01@32fbb0cae2.json"
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("WROTE", out)
