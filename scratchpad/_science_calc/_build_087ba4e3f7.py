# -*- coding: utf-8 -*-
import json, io

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def say(s):
    return {"say": s}

KE = r"\(E_k = \tfrac{1}{2}mv^2\)"
GPE = r"\(E_p = mgh\)"
Wq = r"\(W = Fd\)"
Pq = r"\(P = E/t\)"

pd = {}

pd["method_card"] = {
    "title": "Energy: KE, GPE and Power",
    "steps": [
        "Pick the equation: KE = ½mv², GPE = mgh, work W = Fd, or power P = E/t.",
        "Convert units first: mass in kg, height and distance in m, time in s.",
        "Substitute, and for KE square the speed before multiplying.",
        "Calculate, then state the answer with its unit (J or W)."
    ],
    "content": (
        "<p>Four equations do the work here; the skill is choosing the right one.</p>"
        "<p><strong>Kinetic energy</strong> " + KE + ": square the speed first. Doubling speed quadruples KE.</p>"
        "<p><strong>GPE</strong> " + GPE + ": use vertical height only. This lesson uses g = 10 N/kg.</p>"
        "<p><strong>Work done</strong> " + Wq + ": force times the distance moved.</p>"
        "<p><strong>Power</strong> " + Pq + ": energy per second, in watts. Find the energy first, then divide by time.</p>"
    )
}

pd["topic_links"] = {"prerequisites": []}
pd["exam_context"] = {
    "marks": "2–4 per calculation",
    "paper": "Physics paper (combined science)",
    "frequency": "High: energy calculations appear in nearly every physics paper"
}
pd["related_videos"] = []
pd["worked_examples"] = [
    {
        "steps": [
            {"label": "Step 1: Identify values", "content": "<p>m = 85 kg, v = 12 m/s</p>"},
            {"label": "Step 2: Square the speed first", "content": "<p>v² = 12² = 144 m²/s²</p>"},
            {"label": "Step 3: Apply the equation", "content": "<p>\\(E_k = \\tfrac{1}{2} \\times 85 \\times 144\\)</p>"},
            {"label": "Answer", "content": "<p>E_k = <strong>6,120 J</strong></p>", "isAnswer": True, "is_answer": True}
        ],
        "question": "A cyclist and their bike have a combined mass of 85 kg. They are travelling at 12 m/s. Calculate the kinetic energy stored.",
        "difficulty": "Bronze"
    },
    {
        "steps": [
            {"label": "Step 1: Identify the equation", "content": "<p>\\(E_p = m \\times g \\times h\\)</p>"},
            {"label": "Step 2: Substitute", "content": "<p>\\(E_p = 40 \\times 10 \\times 3.5\\)</p>"},
            {"label": "Answer", "content": "<p>GPE = <strong>1,400 J</strong></p>", "isAnswer": True, "is_answer": True}
        ],
        "question": "A crate of mass 40 kg is lifted vertically by 3.5 m. Calculate the gain in GPE. (g = 10 N/kg)",
        "difficulty": "Silver"
    },
    {
        "steps": [
            {"label": "Step 1: Find energy transferred (GPE gained)", "content": "<p>\\(E_p = 60 \\times 10 \\times 4 = 2{,}400\\) J</p>"},
            {"label": "Step 2: Apply power equation", "content": "<p>\\(P = \\dfrac{E}{t} = \\dfrac{2400}{8}\\)</p>"},
            {"label": "Answer", "content": "<p>P = <strong>300 W</strong></p>", "isAnswer": True, "is_answer": True}
        ],
        "question": "An electric motor lifts a 60 kg load by 4 m in 8 seconds. Calculate the power output. (g = 10 N/kg)",
        "difficulty": "Gold"
    }
]

pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one equation, straight in",
        "steps": [
            "Read the question and pick the matching equation: KE = ½mv², GPE = mgh, work W = Fd, or power P = E/t.",
            "The numbers are already in kg, m and s, so substitute them straight in. For KE, square the speed first.",
            "Work it out and write the unit: J for energy or work, W for power."
        ],
        "example": {
            "question": "Calculate the kinetic energy of a 4 kg trolley moving at 5 m/s.",
            "steps": [
                {"label": "Square the speed", "content": "v² = 5² = 25"},
                {"label": "Apply ½mv²", "content": "E_k = ½ × 4 × 25"},
                {"label": "Check", "content": "½ × 4 = 2, and 2 × 25 = 50"},
                {"label": "Answer", "content": "E_k = 50 J", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: convert or rearrange first",
        "steps": [
            "Sometimes the equation must be turned around first. To find speed from KE, rearrange E_k = ½mv² to v = √(2E_k ÷ m).",
            "Or a value is in the wrong unit: change grams to kilograms (÷ 1000) before you substitute.",
            "Then substitute and solve as usual, keeping the unit on your answer."
        ],
        "example": {
            "question": "A 0.5 kg ball has 25 J of kinetic energy. Calculate its speed.",
            "steps": [
                {"label": "Rearrange", "content": "v² = 2E_k ÷ m"},
                {"label": "Substitute", "content": "v² = (2 × 25) ÷ 0.5 = 100"},
                {"label": "Check", "content": "√100 = 10"},
                {"label": "Answer", "content": "v = 10 m/s", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: two equations chained",
        "steps": [
            "Gold problems need two steps: work out the first quantity, then use it in a second equation.",
            "Energy is the usual bridge: find GPE or KE first, then feed that energy into P = E/t, or into a height or speed.",
            "Finish the first calculation fully before starting the second, and carry the exact value across."
        ],
        "example": {
            "question": "A motor lifts a 50 kg load by 6 m in 10 s. Calculate the power output. (g = 10 N/kg)",
            "steps": [
                {"label": "Find the energy (GPE)", "content": "E_p = 50 × 10 × 6 = 3000 J"},
                {"label": "Apply power", "content": "P = E ÷ t = 3000 ÷ 10"},
                {"label": "Check", "content": "3000 ÷ 10 = 300"},
                {"label": "Answer", "content": "P = 300 W", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

pd["guided"] = {
    "opener": {
        "prompt": "Two identical bumper cars, same mass. One is going 10 m/s. The other is going twice as fast.",
        "steps": [
            say("Two identical bumper cars, same mass. One does 10 m/s. The other does 20 m/s, twice as fast."),
            box("How many times faster is the second car? 20 ÷ 10 = ", 2, "Divide the two speeds."),
            say("Most people guess it carries twice the energy. But kinetic energy depends on speed <strong>squared</strong>, so we square that factor of 2."),
            box("Square the factor: 2² = ", 4, "2 × 2.", done="So it carries FOUR times the energy, not two."),
            say("That is exactly why " + KE + ": the speed is squared. Double the speed and you get four times the energy, and four times the crash damage. Squaring the speed is the heart of every energy calculation in this lesson.")
        ]
    },
    "teach": {
        "bronze": {
            "display": "A 6 kg box is lifted straight up by 3 m. Calculate the gravitational potential energy gained. (g = 10 N/kg)",
            "steps": [
                say("This is a GPE question, so use " + GPE + "."),
                box("Mass in kg = ", 6, "It is already in kilograms."),
                box("Height in m = ", 3, "The vertical distance lifted."),
                say("Now substitute into m × g × h with g = 10."),
                box("6 × 10 = ", 60, "Mass times gravity gives the weight, 60 N."),
                box("60 × 3 = ", 180, "Weight times height.", done="That was the whole calculation: 180 J of GPE."),
                box("Check the unit is joules: 6 × 10 × 3 = ", 180, "All three multiplied together.", done="180 J confirmed.")
            ]
        },
        "silver": {
            "display": "A 2 kg trolley stores 36 J of kinetic energy. Calculate its speed.",
            "steps": [
                say("We know the energy and want the speed, so rearrange " + KE + " to \\(v = \\sqrt{2E_k \\div m}\\)."),
                box("2 × E_k = 2 × 36 = ", 72, "Double the energy."),
                box("Divide by the mass: 72 ÷ 2 = ", 36, "This is v squared."),
                say("That 36 is v², so take the square root."),
                box("√36 = ", 6, "What number times itself gives 36?", done="Rearranging first was the new move here."),
                box("Check forwards: ½ × 2 × 6² = ½ × 2 × 36 = ", 36, "Square 6, then half of 2 times that.", done="Back to 36 J, so v = 6 m/s is right.")
            ]
        },
        "gold": {
            "display": "A 0.4 kg ball is dropped from a height of 5 m. Assuming no energy losses, calculate its speed just before it lands. (g = 10 N/kg)",
            "steps": [
                say("First find the GPE it loses, using " + GPE + ". All of it becomes kinetic energy."),
                box("GPE = 0.4 × 10 × 5 = ", 20, "Multiply all three."),
                say("So the KE at the bottom is also 20 J. Now rearrange " + KE + " to find v."),
                box("2 × KE = 2 × 20 = ", 40, "Double the energy."),
                box("Divide by the mass: 40 ÷ 0.4 = ", 100, "This is v squared."),
                box("√100 = ", 10, "What times itself is 100?", done="Two equations chained: GPE to KE to speed."),
                box("Check: ½ × 0.4 × 10² = ½ × 0.4 × 100 = ", 20, "Square 10 first.", done="20 J, matching the GPE, so v = 10 m/s.")
            ]
        }
    }
}

def prob(display, sol, unit, hint, misc, guided, accept, eq=None, calc=True):
    p = {
        "unit": unit,
        "display": display,
        "solutions": [sol],
        "accept": accept,
        "calculator": calc,
        "higher_only": False,
        "input_type": "single_value",
        "hint": hint,
        "misconceptions": misc,
        "guided_steps": guided
    }
    if eq is not None:
        p["equation_hint"] = eq
    return p

def mc(pattern, message, expect):
    return {"check": "common", "pattern": pattern, "message": message, "expect": expect}

pb = {}
pb["bronze_description"] = "One equation, all values already in the right units. Substitute straight in."
pb["silver_description"] = "Convert a unit first, or rearrange the equation before you substitute."
pb["gold_description"] = "Two steps chained: find one quantity, then feed it into a second equation."

pb["bronze"] = [
    prob("Calculate the kinetic energy of a 2 kg ball moving at 3 m/s.", 9, "J",
         "Square the speed before multiplying by half the mass.",
         [mc("forgot_square", "Square the speed first: v² = 3² = 9. Then E_k = 0.5 × 2 × 9 = 9 J.", 3),
          mc("forgot_half", "Do not forget the half. E_k = ½ × 2 × 9 = 9 J, not 2 × 9 = 18 J.", 18)],
         [say("Kinetic energy uses " + KE + ". Square the speed first."),
          box("Square the speed: 3² = ", 9, "3 × 3."),
          say("Now put it into ½ × m × v²."),
          box("½ × 2 = ", 1, "Half of the mass.", phase="substitute"),
          box("1 × 9 = ", 9, "Multiply by v squared.", phase="substitute", done="E_k = 9 J. Energy is in joules.")],
         0.5, eq=r"\(E_k = \tfrac{1}{2}mv^2\)"),

    prob("A 5 kg object is lifted 4 m vertically. Calculate the gain in gravitational potential energy. (g = 10 N/kg)", 200, "J",
         "Multiply mass by g by height; g is 10 here.",
         [mc("unit_error", "Use g = 10 N/kg in this lesson. With g = 10, E_p = 5 × 10 × 4 = 200 J. Using 9.8 gives 196 J.", 196)],
         [say("GPE uses " + GPE + ", with g = 10 N/kg."),
          box("Weight first: mass × g = 5 × 10 = ", 50, "5 kg times 10 N/kg."),
          say("That 50 N is the weight. Now multiply by the height."),
          box("50 × 4 = ", 200, "Weight times height gives GPE.", phase="substitute"),
          box("Check the whole thing: 5 × 10 × 4 = ", 200, "All three multiplied.", phase="substitute", done="E_p = 200 J. Energy is in joules.")],
         1, eq=r"\(E_p = mgh\)"),

    prob("A force of 50 N moves an object 3 m in the direction of the force. Calculate the work done.", 150, "J",
         "Multiply the force by the distance.",
         [mc("wrong_equation", "Work done is force × distance: W = 50 × 3 = 150 J.", None)],
         [say("Work done uses " + Wq + ": force times distance."),
          box("Write the force in N = ", 50, "The force is 50 N."),
          say("Multiply by the distance moved."),
          box("50 × 3 = ", 150, "Force times distance.", phase="substitute"),
          box("Check: 50 N × 3 m = ", 150, "Force times distance, in joules.", phase="substitute", done="W = 150 J.")],
         1, eq=r"\(W = F \times d\)"),

    prob("A device transfers 600 J of energy in 20 seconds. Calculate its power.", 30, "W",
         "Divide the energy by the time.",
         [mc("inverse_error", "Power is energy ÷ time: P = 600 ÷ 20 = 30 W. Multiplying gives 12000, which is wrong.", 12000)],
         [say("Power uses " + Pq + ": energy divided by time."),
          box("Energy in J = ", 600, "600 J is transferred."),
          say("Divide by the time in seconds."),
          box("600 ÷ 20 = ", 30, "Energy divided by time.", phase="substitute"),
          box("Check: 600 J ÷ 20 s = ", 30, "Divide, do not multiply.", phase="substitute", done="P = 30 W. Power is in watts.")],
         0.5, eq=r"\(P = E/t\)"),

    prob("Calculate the kinetic energy of a 10 kg skateboard moving at 4 m/s.", 80, "J",
         "Square the speed, then multiply by half the mass.",
         [mc("forgot_square", "Square the speed first: v² = 4² = 16. Then E_k = 0.5 × 10 × 16 = 80 J.", 20),
          mc("forgot_half", "Do not forget the half: E_k = ½ × 10 × 16 = 80 J, not 10 × 16 = 160 J.", 160)],
         [say("Kinetic energy: " + KE + ". Square the speed first."),
          box("Square the speed: 4² = ", 16, "4 × 4."),
          say("Now ½ × mass × v²."),
          box("½ × 10 = ", 5, "Half the mass.", phase="substitute"),
          box("5 × 16 = ", 80, "Times v squared.", phase="substitute", done="E_k = 80 J.")],
         0.5, eq=r"\(E_k = \tfrac{1}{2}mv^2\)"),

    prob("A 3 kg book falls from a shelf 2 m above the floor. Calculate the GPE it loses. (g = 10 N/kg)", 60, "J",
         "Multiply mass by g by height.",
         [mc("unit_error", "With g = 10, E_p = 3 × 10 × 2 = 60 J. Using 9.8 gives 58.8 J.", 58.8)],
         [say("GPE: " + GPE + ", g = 10 N/kg."),
          box("Weight = 3 × 10 = ", 30, "Mass times gravity."),
          say("Multiply by the height fallen."),
          box("30 × 2 = ", 60, "Weight times height.", phase="substitute"),
          box("Check: 3 × 10 × 2 = ", 60, "All three multiplied.", phase="substitute", done="E_p = 60 J lost.")],
         0.5, eq=r"\(E_p = mgh\)"),

    prob("An appliance uses 1,500 J in 5 seconds. What is its power?", 300, "W",
         "Divide the energy by the time.",
         [mc("inverse_error", "P = 1500 ÷ 5 = 300 W. Divide energy by time, do not multiply.", 7500)],
         [say("Power: " + Pq + "."),
          box("Energy in J = ", 1500, "1500 J is used."),
          say("Divide by the time."),
          box("1500 ÷ 5 = ", 300, "Energy over time.", phase="substitute"),
          box("Check: 1500 ÷ 5 = ", 300, "Divide energy by time.", phase="substitute", done="P = 300 W.")],
         1, eq=r"\(P = E/t\)"),

    prob("A horizontal push of 30 N moves a box 4 m along a flat floor. Calculate the work done.", 120, "J",
         "Multiply the force by the distance.",
         [mc("wrong_equation", "Work done is force × distance: W = 30 × 4 = 120 J.", None)],
         [say("Work done: " + Wq + "."),
          box("Force in N = ", 30, "The push is 30 N."),
          say("Multiply by the distance."),
          box("30 × 4 = ", 120, "Force times distance.", phase="substitute"),
          box("Check: 30 N × 4 m = ", 120, "Force times distance.", phase="substitute", done="W = 120 J.")],
         1, eq=r"\(W = F \times d\)")
]

pb["silver"] = [
    prob("A 1,200 kg car accelerates from rest to 20 m/s. Calculate the kinetic energy gained.", 240000, "J",
         "Square the speed, then multiply by half the mass.",
         [mc("forgot_square", "Square the speed first: v² = 20² = 400. Then E_k = 0.5 × 1200 × 400 = 240,000 J.", 12000),
          mc("forgot_half", "Do not forget the half: E_k = ½ × 1200 × 400 = 240,000 J, not 1200 × 400 = 480,000 J.", 480000)],
         [say("Kinetic energy: " + KE + ". It starts from rest, so use the final speed. Square it first."),
          box("Square the speed: 20² = ", 400, "20 × 20."),
          say("Now ½ × mass × v²."),
          box("½ × 1200 = ", 600, "Half the mass.", phase="substitute"),
          box("600 × 400 = ", 240000, "Multiply by v squared.", phase="substitute", done="E_k = 240,000 J (240 kJ).")],
         100, eq=r"\(E_k = \tfrac{1}{2}mv^2\)"),

    prob("A 500 W motor lifts a load for 12 seconds. Calculate the energy transferred.", 6000, "J",
         "Rearrange P = E/t to E = P × t.",
         [mc("inverse_error", "Rearrange P = E/t to E = P × t = 500 × 12 = 6,000 J.", None)],
         [say("Rearrange power " + Pq + " to find energy: \\(E = Pt\\)."),
          box("Power in W = ", 500, "500 W."),
          say("Multiply by the time in seconds."),
          box("500 × 12 = ", 6000, "Power times time.", phase="substitute"),
          box("Check: 6000 ÷ 12 = ", 500, "Energy divided by time returns the power.", phase="substitute", done="Dividing back gives 500 W, so E = 6,000 J.")],
         5, eq=r"\(E = P \times t\)"),

    prob("A 75 kg person runs up a staircase, gaining a vertical height of 6 m. Calculate the GPE gained. (g = 10 N/kg)", 4500, "J",
         "Multiply mass by g by height.",
         [mc("unit_error", "With g = 10, E_p = 75 × 10 × 6 = 4,500 J. Using 9.8 gives 4,410 J.", 4410)],
         [say("GPE: " + GPE + ", g = 10 N/kg."),
          box("Weight = 75 × 10 = ", 750, "Mass times gravity."),
          say("Multiply by the vertical height."),
          box("750 × 6 = ", 4500, "Weight times height.", phase="substitute"),
          box("Check: 75 × 10 × 6 = ", 4500, "All three multiplied.", phase="substitute", done="E_p = 4,500 J.")],
         5, eq=r"\(E_p = mgh\)"),

    prob("A 0.2 kg ball has 10 J of kinetic energy. Calculate its speed.", 10, "m/s",
         "Rearrange for v, then remember the square root.",
         [mc("forgot_square", "v² = 2E_k ÷ m = (2 × 10) ÷ 0.2 = 100. Remember to square root: v = √100 = 10 m/s, not 100.", 100)],
         [say("We have energy, we want speed. Rearrange " + KE + " to \\(v = \\sqrt{2E_k \\div m}\\)."),
          box("2 × E_k = 2 × 10 = ", 20, "Double the energy."),
          say("Divide by the mass to get v squared."),
          box("20 ÷ 0.2 = ", 100, "This is v squared.", phase="substitute"),
          box("√100 = ", 10, "What times itself is 100?", phase="substitute", done="v = 10 m/s.")],
         0.5, eq=r"\(v = \sqrt{\frac{2E_k}{m}}\)"),

    prob("A crane lifts a 200 kg beam by 15 m in 30 s. Calculate the power output. (g = 10 N/kg)", 1000, "W",
         "Find the GPE first, then divide by time.",
         [mc("forgot_step", "First find the GPE: 200 × 10 × 15 = 30,000 J. Then P = 30,000 ÷ 30 = 1,000 W. Stopping at 30,000 forgets the power step.", 30000)],
         [say("Two steps: find the GPE lifted, then the power. Start with " + GPE + ", g = 10."),
          box("GPE = 200 × 10 × 15 = ", 30000, "Multiply all three."),
          say("Now power " + Pq + ": divide by the time."),
          box("30000 ÷ 30 = ", 1000, "Energy over time.", phase="substitute"),
          box("Check: 30000 ÷ 30 = ", 1000, "Divide energy by time.", phase="substitute", done="P = 1,000 W (1 kW).")],
         5, eq=r"Find GPE first, then \(P = E/t\)"),

    prob("A rollercoaster car (mass 600 kg) drops from a height of 20 m. Assuming no energy losses, calculate its speed at the bottom. (g = 10 N/kg)", 20, "m/s",
         "GPE lost equals KE; rearrange for v and square root.",
         [mc("forgot_square", "GPE = 600 × 10 × 20 = 120,000 J = KE. v² = 2 × 120,000 ÷ 600 = 400. Square root: v = √400 = 20 m/s, not 400.", 400)],
         [say("Energy is conserved: the GPE lost becomes KE. Find GPE with " + GPE + ", g = 10."),
          box("GPE = 600 × 10 × 20 = ", 120000, "Multiply all three."),
          say("That 120,000 J is now KE. Rearrange " + KE + " to find v."),
          box("v² = (2 × 120000) ÷ 600 = ", 400, "This is v squared.", phase="substitute"),
          box("√400 = ", 20, "What times itself is 400?", phase="substitute", done="v = 20 m/s.")],
         0.5, eq=r"GPE lost = KE gained. Rearrange \(E_k = \tfrac{1}{2}mv^2\) for v.")
]

pb["gold"] = [
    prob("A 800 kg rollercoaster car starts from rest at the top of a 45 m drop. Calculate its speed at the bottom, assuming no energy losses. (g = 10 N/kg)", 30, "m/s",
         "Find the GPE lost, set it equal to KE, then rearrange for v.",
         [mc("forgot_rearrange", "GPE = 800 × 10 × 45 = 360,000 J = KE. v² = 2 × 360,000 ÷ 800 = 900. v = 30 m/s.", None),
          mc("forgot_square", "Remember to take the square root at the end: v = √900 = 30 m/s, not 900.", 900)],
         [say("Energy conserved: GPE lost becomes KE. First " + GPE + ", g = 10."),
          box("GPE = 800 × 10 × 45 = ", 360000, "Multiply all three."),
          say("This 360,000 J is the KE at the bottom. Rearrange " + KE + " for v."),
          box("v² = (2 × 360000) ÷ 800 = ", 900, "Double the energy, divide by mass.", phase="substitute"),
          box("√900 = ", 30, "What times itself is 900?", phase="substitute", done="v = 30 m/s.")],
         0.5),

    prob("A 1,200 kg car travels at 30 m/s. An emergency forces the driver to brake to rest. Calculate the kinetic energy that must be removed by the brakes. Then calculate the average braking force if the car stops in 50 m.", 10800, "N",
         "Find the KE first, that equals the braking work, then divide by distance for force.",
         [mc("forgot_square", "KE = 0.5 × 1200 × 30² = 0.5 × 1200 × 900 = 540,000 J. F = 540,000 ÷ 50 = 10,800 N. Forgetting the square gives 360 N.", 360),
          mc("wrong_equation", "The braking work equals the KE removed. Rearrange W = Fd to F = W ÷ d.", None)],
         [say("First find the KE to remove: " + KE + ". Square the speed."),
          box("Square the speed: 30² = ", 900, "30 × 30."),
          box("KE = ½ × 1200 × 900 = ", 540000, "Half of 1200 is 600, times 900."),
          say("The brakes do this much work. Rearrange " + Wq + " to \\(F = W \\div d\\)."),
          box("F = 540000 ÷ 50 = ", 10800, "Work divided by distance.", phase="substitute"),
          box("Check: 10800 × 50 = ", 540000, "Force times distance returns the work.", phase="substitute", done="F = 10,800 N.")],
         5),

    prob("A motor lifts a 120 kg load by 8 m in 6 s. Calculate the power output of the motor in watts. (g = 10 N/kg)", 1600, "W",
         "Find the GPE gained, then divide by the time for power.",
         [mc("forgot_step", "GPE = 120 × 10 × 8 = 9,600 J. P = 9,600 ÷ 6 = 1,600 W. Stopping at 9,600 forgets the power step.", 9600),
          mc("inverse_error", "Power is P = E ÷ t, not E × t. Multiplying gives 57,600, which is wrong.", 57600)],
         [say("Two steps: GPE gained, then power. " + GPE + ", g = 10."),
          box("GPE = 120 × 10 × 8 = ", 9600, "Multiply all three."),
          say("Now " + Pq + ": divide by the time."),
          box("9600 ÷ 6 = ", 1600, "Energy over time.", phase="substitute"),
          box("Check: 1600 × 6 = ", 9600, "Power times time returns the energy.", phase="substitute", done="P = 1,600 W.")],
         5),

    prob("A 500 g ball is launched upwards with 90 J of kinetic energy. Assuming all KE converts to GPE, calculate the maximum height reached. (g = 10 N/kg)", 18, "m",
         "Convert grams to kilograms first, then rearrange E = mgh for height.",
         [mc("unit_error", "Convert mass to kg first: 500 g = 0.5 kg. h = E ÷ (mg) = 90 ÷ (0.5 × 10) = 18 m. Leaving mass as 500 gives 0.018 m.", 0.018),
          mc("forgot_rearrange", "Rearrange E_p = mgh to h = E_p ÷ (mg). Use mass in kg.", None)],
         [say("All the KE becomes GPE, so " + GPE + " = 90 J. First convert the mass to kilograms."),
          box("Mass in kg = 500 ÷ 1000 = ", 0.5, "1000 g in a kilogram."),
          say("Rearrange " + GPE + " to \\(h = E_p \\div (mg)\\)."),
          box("Bottom line first: m × g = 0.5 × 10 = ", 5, "Mass times gravity, the weight.", phase="substitute"),
          box("h = 90 ÷ 5 = ", 18, "Energy divided by weight.", phase="substitute", done="h = 18 m.")],
         0.5),

    prob("A 60 kg person climbs stairs, gaining 3 m of vertical height in 4 s. Calculate the useful power output. (g = 10 N/kg)", 450, "W",
         "Find the GPE gained, then divide by time for power.",
         [mc("forgot_step", "GPE = 60 × 10 × 3 = 1,800 J. P = 1,800 ÷ 4 = 450 W. Stopping at 1,800 forgets the power step.", 1800)],
         [say("Two steps: GPE gained, then power. " + GPE + ", g = 10."),
          box("GPE = 60 × 10 × 3 = ", 1800, "Multiply all three."),
          say("Now " + Pq + "."),
          box("1800 ÷ 4 = ", 450, "Energy over time.", phase="substitute"),
          box("Check: 450 × 4 = ", 1800, "Power times time returns the energy.", phase="substitute", done="P = 450 W.")],
         5)
]

pd["problem_bank"] = pb

out = "lesson_physics-calculations-L01@087ba4e3f7.json"
io.open(out, "w", encoding="utf-8").write(json.dumps(pd, indent=1, ensure_ascii=False))
print("wrote", out)
