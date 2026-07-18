# -*- coding: utf-8 -*-
import json

OMEGA = "Ω"
SQ = "²"
MUL = "×"
DIV = "÷"
GBP = "£"
APPROX = "≈"
MINUS = "−"

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(text):
    return {"say": text}

def mis(pattern, message, expect):
    return {"check": "common", "pattern": pattern, "message": message, "expect": expect}

pd = {}

pd["method_card"] = {
    "title": "Electrical Power and Energy Bills",
    "steps": [
        "Choose the equation from what you know: P = VI, P = I" + SQ + "R, E = Pt or E = QV.",
        "Convert units first: watts to kilowatts (" + DIV + "1000), minutes to seconds (" + MUL + "60).",
        "Substitute, calculate, and always write the unit.",
        "For bills: energy (kWh) = power (kW) " + MUL + " time (hours), then cost = kWh " + MUL + " price per unit."
    ],
    "content": ("<p>Four recall equations give electrical power and energy: \\(P = VI\\), "
                "\\(P = I^2R\\), \\(E = Pt\\) and \\(E = QV\\). Pick the one that matches the "
                "quantities you are given.</p>"
                "<p>Bills measure energy in <strong>kilowatt hours</strong>. One kWh is the "
                "energy a 1 kW appliance uses in 1 hour, which is 3,600,000 J. Convert power "
                "to kW and time to hours, multiply for the energy in kWh, then multiply by the "
                "price per unit for the cost.</p>"
                "<p>Check whether your exam gives you these equations or expects them from memory.</p>")
}

pd["topic_links"] = {"prerequisites": ["circuit-calculations"]}
pd["exam_context"] = {
    "marks": "2" + MINUS + "5 per calculation",
    "paper": "Paper 1 (Physics)",
    "frequency": "Very common: energy bills and power questions appear regularly on Paper 1"
}

pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one equation, values already in the right units",
        "steps": [
            "Pick the equation from what you are given. Voltage and current: \\(P = VI\\). "
            "Current and resistance: \\(P = I^2R\\). Power and time: \\(E = Pt\\). "
            "Charge and voltage: \\(E = QV\\).",
            "Substitute the numbers straight in, work it out, and write the unit."
        ],
        "example": {
            "question": "A 12 V battery drives a current of 3 A through a bulb. Calculate the power.",
            "steps": [
                {"label": "Equation", "content": "\\(P = VI\\)"},
                {"label": "Substitute", "content": "\\(P = 12 " + MUL + " 3\\)"},
                {"label": "Check", "content": "36 " + DIV + " 12 = 3 A, the current given."},
                {"label": "Answer", "content": "<strong>36 W</strong>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: convert the units first, or rearrange the equation",
        "steps": [
            "Watts to kilowatts: divide by 1000. Minutes to seconds: multiply by 60. "
            "Do every conversion before you substitute.",
            "To find a current or a time, rearrange first: \\(I = P/V\\), \\(t = E/P\\). "
            "Then substitute and state the unit."
        ],
        "example": {
            "question": "A 2 kW kettle runs for 3 minutes. Calculate the energy transferred in joules.",
            "steps": [
                {"label": "Convert", "content": "2 kW = 2000 W, 3 min = 180 s"},
                {"label": "Equation", "content": "\\(E = Pt\\)"},
                {"label": "Substitute", "content": "\\(E = 2000 " + MUL + " 180\\)"},
                {"label": "Check", "content": "360000 " + DIV + " 180 = 2000 W, the power."},
                {"label": "Answer", "content": "<strong>360 000 J</strong>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: chain two equations, or work through a bill",
        "steps": [
            "Multi step problems join two equations. Find the power first (\\(P = VI\\) or "
            "\\(P = I^2R\\)), then feed it into \\(E = Pt\\) or \\(Q = It\\).",
            "For bills: convert power to kW and time to hours, multiply for kWh, then multiply "
            "by the price per unit. Add appliances before costing, and give money in pounds."
        ],
        "example": {
            "question": "A 3 kW oven runs 2 hours and a 0.5 kW lamp runs 4 hours. At 30p per unit, find the total cost.",
            "steps": [
                {"label": "Energy", "content": "Oven: 3 " + MUL + " 2 = 6 kWh. Lamp: 0.5 " + MUL + " 4 = 2 kWh. Total 8 kWh."},
                {"label": "Cost", "content": "8 " + MUL + " 30 = 240p"},
                {"label": "Check", "content": "240 " + DIV + " 30 = 8 units, as found."},
                {"label": "Answer", "content": "<strong>" + GBP + "2.40</strong>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

pd["guided"] = {
    "opener": {
        "display": ("Your electricity meter counts 'units'. One unit runs a 1 kilowatt appliance "
                    "for 1 hour, and it costs about 30p.<br><br>A 1 kW heater is left on for 3 hours."),
        "steps": [
            box("If 1 hour costs 30p, then 3 hours cost: 30 " + MUL + " 3 = ", 90,
                "Three lots of 30p.", say="90p, and the heater has used 3 units."),
            box("A 2 kW heater is twice as powerful. For those same 3 hours it uses: 2 " + MUL + " 3 = ", 6,
                "Power in kW times hours.", say="6 units, double the 1 kW heater."),
            sayonly("You just used the billing rule: <strong>energy (kWh) = power (kW) " + MUL +
                    " time (hours)</strong>. Everything here is that idea, plus the equations that "
                    "give the power itself: \\(P = VI\\), \\(P = I^2R\\), \\(E = Pt\\) and \\(E = QV\\).")
        ]
    },
    "teach": {
        "bronze": {
            "display": "A phone charger draws a current of 0.4 A from a 5 V supply. Work out its power.",
            "steps": [
                sayonly("Power from voltage and current is \\(P = VI\\). Both values are already in base units."),
                box("Write the voltage in volts: V = ", 5, "Given: 5 V."),
                box("Write the current in amps: I = ", 0.4, "Given: 0.4 A."),
                box("Multiply them: 5 " + MUL + " 0.4 = ", 2, "Five times four tenths.",
                    say="So the power is 2 W."),
                box("Check: divide back, 2 " + DIV + " 5 = ", 0.4, "Power divided by voltage returns the current.",
                    done="Returns 0.4 A, the current, so 2 W is right.")
            ]
        },
        "silver": {
            "display": "A 1.5 kW hairdryer runs for 4 minutes. Calculate the energy it transfers, in joules.",
            "steps": [
                sayonly("Energy is \\(E = Pt\\), with power in watts and time in seconds. Convert both first."),
                box("Power in watts = 1.5 " + MUL + " 1000 = ", 1500, "1000 W in a kW."),
                box("Time in seconds = 4 " + MUL + " 60 = ", 240, "60 seconds in each minute."),
                box("Multiply: 1500 " + MUL + " 240 = ", 360000, "1500 lots of 240.",
                    say="So the energy is 360,000 J."),
                box("Check: divide back, 360000 " + DIV + " 240 = ", 1500, "Energy divided by time returns the power.",
                    done="Returns 1500 W, the power, so 360,000 J is right.")
            ]
        },
        "gold": {
            "display": "A heating element of resistance 12 " + OMEGA + " carries a current of 5 A for 3 minutes. Calculate the energy it transfers, in joules.",
            "steps": [
                sayonly("Chain two equations: power with \\(P = I^2R\\), then energy with \\(E = Pt\\). "
                        "Square the current and convert the time."),
                box("Square the current: 5 " + MUL + " 5 = ", 25, "Five squared is 25."),
                box("Power = 25 " + MUL + " 12 = ", 300, "25 lots of 12.", say="So the power is 300 W."),
                box("Time in seconds = 3 " + MUL + " 60 = ", 180, "60 seconds in each minute."),
                box("Energy = 300 " + MUL + " 180 = ", 54000, "300 lots of 180.",
                    say="So the energy is 54,000 J."),
                box("Check: divide back, 54000 " + DIV + " 180 = ", 300, "Energy divided by time returns the power.",
                    done="Returns 300 W, the power, so 54,000 J is right.")
            ]
        }
    }
}

bronze = [
    {"unit": "W", "display": "A lamp draws a current of 0.5 A from a 12 V battery. Calculate the power of the lamp.",
     "solutions": [6], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(P = VI\\)", "hint": "Multiply the voltage by the current.",
     "misconceptions": [mis("wrong_rearrange", "P = VI = 12 " + MUL + " 0.5 = 6 W. Multiply the voltage by the current.", None)],
     "guided_steps": [
         sayonly("Power from voltage and current is \\(P = VI\\). Here 12 V and 0.5 A are already in base units."),
         box("Write the current in amps: I = ", 0.5, "It is given directly: 0.5 A."),
         box("Multiply voltage by current: 12 " + MUL + " 0.5 = ", 6, "Twelve halves make six.",
             say="That product is the power in watts.", phase="substitute"),
         box("Check: divide back, 6 " + DIV + " 12 = ", 0.5, "Power divided by voltage should return the current.",
             done="It returns 0.5 A, the current we started with, so the lamp's power is 6 W.")
     ]},
    {"unit": "J", "display": "A 100 W light bulb is on for 60 seconds. Calculate the energy transferred.",
     "solutions": [6000], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(E = Pt\\)", "hint": "Multiply the power by the time; seconds are already correct.",
     "misconceptions": [mis("wrong_formula", "E = Pt = 100 " + MUL + " 60 = 6000 J. The time is already in seconds, so just multiply.", None)],
     "guided_steps": [
         sayonly("Energy transferred is \\(E = Pt\\). Power 100 W and time 60 s are both base units."),
         box("Write the time in seconds: t = ", 60, "Already in seconds: 60."),
         box("Multiply power by time: 100 " + MUL + " 60 = ", 6000, "One hundred lots of 60.",
             say="That is the energy in joules.", phase="substitute"),
         box("Check: divide back, 6000 " + DIV + " 60 = ", 100, "Energy divided by time returns the power.",
             done="Returns 100 W, the power, so the energy is 6000 J.")
     ]},
    {"unit": "W", "display": "A current of 2 A flows through a 5 " + OMEGA + " resistor. Calculate the power dissipated.",
     "solutions": [20], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(P = I^2R\\)", "hint": "Square the current, then multiply by the resistance.",
     "misconceptions": [
         mis("forgot_square", "Square the current first: 2" + SQ + " = 4. Then P = I" + SQ + "R = 4 " + MUL + " 5 = 20 W.", 10),
         mis("wrong_formula", "You have current and resistance, so use P = I" + SQ + "R, not P = VI. P = 4 " + MUL + " 5 = 20 W.", None)],
     "guided_steps": [
         sayonly("With current and resistance, power is \\(P = I^2R\\). Square the current first."),
         box("Square the current: 2 " + MUL + " 2 = ", 4, "Two squared is four."),
         box("Multiply by the resistance: 4 " + MUL + " 5 = ", 20, "Four fives.",
             say="So the power dissipated is 20 W.", phase="substitute"),
         box("Check: divide by resistance, 20 " + DIV + " 5 = ", 4, "This should return the current squared.",
             done="Returns 4, which is 2 squared, so 20 W is right.")
     ]},
    {"unit": "A", "display": "A 230 V mains appliance has a power rating of 920 W. Calculate the current it draws.",
     "solutions": [4], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(P = VI\\)", "hint": "Rearrange to current = power " + DIV + " voltage.",
     "misconceptions": [
         mis("wrong_rearrange", "Rearrange P = VI to I = P/V = 920 " + DIV + " 230 = 4 A.", None),
         mis("inverse_error", "Divide, do not multiply: I = P " + DIV + " V = 920 " + DIV + " 230 = 4 A.", 211600)],
     "guided_steps": [
         sayonly("You know power and voltage, so rearrange \\(P = VI\\) to \\(I = P/V\\)."),
         box("Write the power in watts: P = ", 920, "Given directly: 920."),
         box("Divide power by voltage: 920 " + DIV + " 230 = ", 4, "How many 230s fit into 920?",
             say="So the current is 4 A.", phase="substitute"),
         box("Check: multiply back, 230 " + MUL + " 4 = ", 920, "Voltage times current returns the power.",
             done="Returns 920 W, the power, so the current is 4 A.")
     ]},
    {"unit": "J", "display": "A charge of 60 C flows through a component with a voltage of 5 V across it. Calculate the energy transferred.",
     "solutions": [300], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(E = QV\\)", "hint": "Multiply the charge by the voltage.",
     "misconceptions": [mis("wrong_formula", "E = QV = 60 " + MUL + " 5 = 300 J. Multiply the charge by the voltage.", None)],
     "guided_steps": [
         sayonly("Energy from charge and voltage is \\(E = QV\\)."),
         box("Write the charge in coulombs: Q = ", 60, "Given directly: 60."),
         box("Multiply charge by voltage: 60 " + MUL + " 5 = ", 300, "Sixty fives.",
             say="So the energy transferred is 300 J.", phase="substitute"),
         box("Check: divide back, 300 " + DIV + " 5 = ", 60, "Energy divided by voltage returns the charge.",
             done="Returns 60 C, the charge, so the energy is 300 J.")
     ]},
    {"unit": "kWh", "display": "A 2 kW heater is used for 4 hours. Calculate the energy used in kWh.",
     "solutions": [8], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(\\text{Energy (kWh)} = \\text{power (kW)} \\times \\text{time (hours)}\\)",
     "hint": "Multiply the power in kW by the time in hours.",
     "misconceptions": [mis("unit_error", "The power is already in kW and the time in hours, so just multiply: 2 " + MUL + " 4 = 8 kWh.", None)],
     "guided_steps": [
         sayonly("Energy in kilowatt hours is power in kW " + MUL + " time in hours. Both are already in those units."),
         box("Write the power in kW: P = ", 2, "Given directly: 2 kW."),
         box("Multiply power by time: 2 " + MUL + " 4 = ", 8, "Two fours.",
             say="So the heater uses 8 kWh.", phase="substitute"),
         box("Check: divide back, 8 " + DIV + " 4 = ", 2, "Energy divided by time returns the power.",
             done="Returns 2 kW, the power, so the energy is 8 kWh.")
     ]},
    {"unit": "W", "display": "A motor transfers 12,000 J of energy in 30 seconds. Calculate its power.",
     "solutions": [400], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(E = Pt\\)", "hint": "Rearrange to power = energy " + DIV + " time.",
     "misconceptions": [
         mis("wrong_rearrange", "Rearrange E = Pt to P = E/t = 12000 " + DIV + " 30 = 400 W.", None),
         mis("inverse_error", "Divide, do not multiply: P = E " + DIV + " t = 12000 " + DIV + " 30 = 400 W.", 360000)],
     "guided_steps": [
         sayonly("Rearrange \\(E = Pt\\) to \\(P = E/t\\)."),
         box("Write the time in seconds: t = ", 30, "Already in seconds: 30."),
         box("Divide energy by time: 12000 " + DIV + " 30 = ", 400, "How many 30s fit into 12000?",
             say="So the motor's power is 400 W.", phase="substitute"),
         box("Check: multiply back, 400 " + MUL + " 30 = ", 12000, "Power times time returns the energy.",
             done="Returns 12,000 J, so the power is 400 W.")
     ]},
    {"display": "Which equation would you use to find the power of a device if you know the current through it and its resistance?",
     "options": ["\\(P = VI\\)", "\\(P = I^2R\\)", "\\(E = Pt\\)", "\\(E = QV\\)"],
     "solutions": [1], "calculator": False, "input_type": "multiple_choice",
     "equation_hint": "\\(P = I^2R\\)", "hint": "You know the current and the resistance.",
     "misconceptions": [mis("wrong_equation", "With current and resistance, use P = I" + SQ + "R. You would need P = VI only if you knew the voltage.", None)]},
]

silver = [
    {"unit": "p", "display": "A 3 kW immersion heater is used for 2 hours. Electricity costs 28p per kWh. Calculate the cost of heating the water in pence.",
     "solutions": [168], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(\\text{Energy (kWh)} = \\text{power (kW)} \\times \\text{time (hours)}\\)",
     "hint": "Find the energy in kWh first, then multiply by the price.",
     "misconceptions": [
         mis("forgot_step", "Energy = 3 " + MUL + " 2 = 6 kWh. Cost = 6 " + MUL + " 28 = 168p. Do not stop at the energy.", None),
         mis("unit_error", "Power must be in kW and time in hours for kWh: 3 " + MUL + " 2 = 6 kWh, then 6 " + MUL + " 28 = 168p.", None)],
     "guided_steps": [
         sayonly("First find the energy in kWh: power (kW) " + MUL + " time (hours). Both are already in the right units."),
         box("Energy = 3 " + MUL + " 2 = ", 6, "Three twos.",
             say="That is 6 kWh, the number of units on the bill."),
         box("Now the cost in pence: units " + MUL + " price, 6 " + MUL + " 28 = ", 168, "Six lots of 28p.",
             say="So the cost is 168p.", phase="substitute"),
         box("Check: divide back, 168 " + DIV + " 28 = ", 6, "Cost divided by price returns the units.",
             done="Returns 6 kWh, so the cost is 168p.")
     ]},
    {"display": "A microwave has a power rating of 800 W and operates on a 230 V supply. The available fuse ratings are 3 A, 5 A and 13 A. Which fuse should be fitted?",
     "options": ["3 A", "5 A", "13 A"], "solutions": [1], "calculator": True, "input_type": "multiple_choice",
     "equation_hint": "\\(P = VI\\)", "hint": "Find the current, then pick the next fuse above it.",
     "misconceptions": [mis("forgot_step", "I = P/V = 800 " + DIV + " 230 = 3.48 A. The fuse must be just above the normal current, so 5 A. A 3 A fuse would blow; 13 A is too high to protect the device.", None)]},
    {"unit": "kJ", "display": "A 500 W washing machine runs for 45 minutes. Calculate the energy transferred in kJ.",
     "solutions": [1350], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(E = Pt\\)", "hint": "Convert minutes to seconds, then use energy = power " + MUL + " time.",
     "misconceptions": [
         mis("unit_error", "Convert 45 minutes to 2700 seconds first. E = 500 " + MUL + " 2700 = 1,350,000 J = 1350 kJ. Using 45 seconds gives only 22.5 kJ.", 22.5),
         mis("forgot_step", "Convert minutes to seconds (" + MUL + " 60), work in joules, then convert to kJ (" + DIV + " 1000).", None)],
     "guided_steps": [
         sayonly("Energy is \\(E = Pt\\), with time in seconds. Convert the 45 minutes first."),
         box("Time in seconds = 45 " + MUL + " 60 = ", 2700, "60 seconds in each minute."),
         box("Multiply power by time: 500 " + MUL + " 2700 = ", 1350000, "500 lots of 2700.",
             say="That is 1,350,000 J.", phase="substitute"),
         box("Convert to kilojoules, divide by 1000: 1350000 " + DIV + " 1000 = ", 1350, "1000 J in each kJ.",
             done="So the energy transferred is 1350 kJ.")
     ]},
    {"unit": GBP, "accept": 0.01, "display": "A 60 W laptop is used for 8 hours a day for 30 days. Electricity costs 30p per kWh. Calculate the total cost in pounds.",
     "solutions": [4.32], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(\\text{Energy (kWh)} = \\text{power (kW)} \\times \\text{time (hours)}\\)",
     "hint": "Convert watts to kilowatts and find the total hours before costing.",
     "misconceptions": [
         mis("unit_error", "Convert 60 W to 0.06 kW. Total time = 8 " + MUL + " 30 = 240 hours. Energy = 0.06 " + MUL + " 240 = 14.4 kWh. Cost = 14.4 " + MUL + " 30 = 432p = " + GBP + "4.32.", 4320),
         mis("forgot_step", "Change watts to kilowatts (" + DIV + " 1000), then multiply by the total hours across all 30 days.", None)],
     "guided_steps": [
         sayonly("For a bill, work in kW and hours. Convert the power and find the total time first."),
         box("Power in kW = 60 " + DIV + " 1000 = ", 0.06, "1000 W in a kW."),
         box("Total hours = 8 " + MUL + " 30 = ", 240, "Eight hours on each of 30 days."),
         box("Energy in kWh = 0.06 " + MUL + " 240 = ", 14.4, "Multiply kW by hours.",
             say="That is 14.4 units.", phase="substitute"),
         box("Cost in pence = 14.4 " + MUL + " 30 = ", 432, "14.4 lots of 30p.",
             say="That is 432p."),
         box("Convert to pounds: 432 " + DIV + " 100 = ", 4.32, "100 pence in a pound.",
             done="So the total cost is " + GBP + "4.32.")
     ]},
    {"unit": "J", "display": "A current of 3 A flows through a 15 " + OMEGA + " heating element. Calculate the energy transferred in 2 minutes.",
     "solutions": [16200], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(P = I^2R\\) and \\(E = Pt\\)",
     "hint": "Square the current for the power, convert the time, then energy = power " + MUL + " time.",
     "misconceptions": [
         mis("forgot_step", "P = I" + SQ + "R = 3" + SQ + " " + MUL + " 15 = 135 W. Convert 2 minutes to 120 s. Energy = 135 " + MUL + " 120 = 16,200 J.", None),
         mis("forgot_square", "Square the current: 3" + SQ + " = 9, not 3. P = 9 " + MUL + " 15 = 135 W, then E = 135 " + MUL + " 120 = 16,200 J.", 5400)],
     "guided_steps": [
         sayonly("Two steps: power first with \\(P = I^2R\\), then energy with \\(E = Pt\\). Square the current and convert the time."),
         box("Square the current: 3 " + MUL + " 3 = ", 9, "Three squared is nine."),
         box("Power = 9 " + MUL + " 15 = ", 135, "Nine fifteens.", say="So the power is 135 W."),
         box("Time in seconds = 2 " + MUL + " 60 = ", 120, "60 seconds in each minute."),
         box("Energy = power " + MUL + " time = 135 " + MUL + " 120 = ", 16200, "135 lots of 120.",
             say="So the energy transferred is 16,200 J.", phase="substitute"),
         box("Check: divide back, 16200 " + DIV + " 120 = ", 135, "Energy divided by time returns the power.",
             done="Returns 135 W, the power, so 16,200 J is right.")
     ]},
    {"unit": "kJ", "accept": 1, "display": "A 230 V kettle draws 12 A and takes 3 minutes to boil. Calculate the energy transferred to the water in kJ.",
     "solutions": [496.8], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(P = VI\\) and \\(E = Pt\\)",
     "hint": "Find the power first, convert the time, then energy = power " + MUL + " time.",
     "misconceptions": [
         mis("forgot_step", "P = VI = 230 " + MUL + " 12 = 2760 W. Convert 3 minutes to 180 s. E = 2760 " + MUL + " 180 = 496,800 J = 496.8 kJ.", None),
         mis("unit_error", "Convert 3 minutes to 180 seconds before finding the energy. Using 3 gives only 8.28 kJ.", 8.28)],
     "guided_steps": [
         sayonly("Power first with \\(P = VI\\), then energy with \\(E = Pt\\). Convert the time to seconds."),
         box("Power = 230 " + MUL + " 12 = ", 2760, "230 lots of 12.", say="So the power is 2760 W."),
         box("Time in seconds = 3 " + MUL + " 60 = ", 180, "60 seconds in each minute."),
         box("Energy = 2760 " + MUL + " 180 = ", 496800, "2760 lots of 180.",
             say="That is 496,800 J.", phase="substitute"),
         box("Convert to kilojoules, divide by 1000: 496800 " + DIV + " 1000 = ", 496.8, "1000 J in each kJ.",
             done="So the energy transferred is 496.8 kJ.")
     ]},
]

gold = [
    {"unit": GBP, "accept": 0.01, "display": "Two appliances are used in a house: a 2 kW heater for 5 hours and a 800 W TV for 3 hours. Electricity costs 32p per kWh. Calculate the total cost in pounds.",
     "solutions": [3.97], "calculator": True, "input_type": "single_value",
     "hint": "Find each appliance's kWh, add them, then cost in pence.",
     "misconceptions": [
         mis("forgot_step", "Heater: 2 " + MUL + " 5 = 10 kWh. TV: 0.8 " + MUL + " 3 = 2.4 kWh. Total = 12.4 kWh. Cost = 12.4 " + MUL + " 32 = 396.8p = " + GBP + "3.97.", None),
         mis("unit_error", "Convert 800 W to 0.8 kW, and add both energy values before working out the cost.", None)],
     "guided_steps": [
         sayonly("Find each appliance's energy in kWh, add them, then cost. Convert the TV's power to kW."),
         box("Heater energy = 2 " + MUL + " 5 = ", 10, "Power in kW times hours."),
         box("TV power in kW = 800 " + DIV + " 1000 = ", 0.8, "1000 W in a kW."),
         box("TV energy = 0.8 " + MUL + " 3 = ", 2.4, "0.8 times 3."),
         box("Total energy = 10 + 2.4 = ", 12.4, "Add both appliances.", say="That is 12.4 units."),
         box("Cost in pence = 12.4 " + MUL + " 32 = ", 396.8, "12.4 lots of 32p.",
             say="That is 396.8p.", phase="substitute"),
         box("Convert to pounds and round to the nearest penny: 396.8p = " + GBP, 3.97,
             "100 pence in a pound, rounded to the nearest penny.",
             done="So the total cost is " + GBP + "3.97.")
     ]},
    {"unit": "s", "accept": 1, "display": "A kettle is rated at 2.8 kW and is 92% efficient. It transfers 336,000 J of useful energy to the water. Calculate how long the kettle was on for, in seconds.",
     "solutions": [130.4], "calculator": True, "input_type": "single_value",
     "hint": "Divide by efficiency for the input energy, then time = energy " + DIV + " power.",
     "misconceptions": [
         mis("forgot_step", "Total input = useful " + DIV + " efficiency = 336,000 " + DIV + " 0.92 " + APPROX + " 365,217 J. Convert 2.8 kW to 2800 W. Time = E/P = 365,217 " + DIV + " 2800 " + APPROX + " 130.4 s.", None),
         mis("wrong_rearrange", "The 336,000 J is the useful output, not the input. Divide by the efficiency (0.92) first, then find the time. Skipping that gives 120 s.", 120)],
     "guided_steps": [
         sayonly("The 336,000 J is the useful output. Total input = useful " + DIV + " efficiency. The power 2.8 kW is 2800 W. Then \\(t = E/P\\)."),
         box("Power in watts = 2.8 " + MUL + " 1000 = ", 2800, "1000 W in a kW."),
         box("Total input energy = 336000 " + DIV + " 0.92 = (to the nearest joule) ", 365217,
             "Useful energy divided by 0.92.", phase="substitute"),
         box("Time = energy " + DIV + " power = 365217 " + DIV + " 2800 = (to 1 d.p.) ", 130.4,
             "Total energy divided by power.",
             done="So the kettle was on for about 130.4 s.")
     ]},
    {"unit": "W", "display": "An electric shower has a heating element with a resistance of 9.2 " + OMEGA + " and draws a current of 10 A. Calculate the power of the shower.",
     "solutions": [920], "calculator": True, "input_type": "single_value",
     "hint": "Square the current, then multiply by the resistance.",
     "misconceptions": [
         mis("forgot_square", "P = I" + SQ + "R = 10" + SQ + " " + MUL + " 9.2 = 100 " + MUL + " 9.2 = 920 W. Square the current before multiplying.", 92),
         mis("wrong_formula", "You have current and resistance, so use P = I" + SQ + "R, not P = VI (you do not know V).", None)],
     "guided_steps": [
         sayonly("With current and resistance, use \\(P = I^2R\\). Square the current first."),
         box("Square the current: 10 " + MUL + " 10 = ", 100, "Ten squared is a hundred."),
         box("Multiply by resistance: 100 " + MUL + " 9.2 = ", 920, "A hundred lots of 9.2.",
             say="So the shower's power is 920 W.", phase="substitute"),
         box("Check: divide by resistance, 920 " + DIV + " 9.2 = ", 100, "This should return the current squared.",
             done="Returns 100, which is 10 squared, so 920 W is right.")
     ]},
    {"unit": GBP, "accept": 0.01, "display": "A student wants to compare the running cost of two devices over 30 days. Device A: 150 W, used 6 hours/day. Device B: 2 kW, used 30 minutes/day. Electricity costs 30p per kWh. Calculate the difference in cost between the two devices in pounds.",
     "solutions": [0.9], "calculator": True, "input_type": "single_value",
     "hint": "Cost each device over 30 days, then subtract.",
     "misconceptions": [
         mis("forgot_step", "A: 0.15 " + MUL + " 6 " + MUL + " 30 = 27 kWh, so 810p. B: 2 " + MUL + " 0.5 " + MUL + " 30 = 30 kWh, so 900p. Difference = " + GBP + "9.00 " + MINUS + " " + GBP + "8.10 = " + GBP + "0.90.", None),
         mis("unit_error", "Convert 150 W to 0.15 kW and 30 minutes to 0.5 hours, then work out the kWh for each device.", None)],
     "guided_steps": [
         sayonly("Find each device's energy in kWh over 30 days, then the cost, then the difference. Convert A's power to kW and B's time to hours."),
         box("A power in kW = 150 " + DIV + " 1000 = ", 0.15, "1000 W in a kW."),
         box("A energy = 0.15 " + MUL + " 6 " + MUL + " 30 = ", 27, "kW " + MUL + " hours per day " + MUL + " days.",
             say="That is 27 kWh."),
         box("B time in hours = 30 " + DIV + " 60 = ", 0.5, "60 minutes in an hour."),
         box("B energy = 2 " + MUL + " 0.5 " + MUL + " 30 = ", 30, "kW " + MUL + " hours per day " + MUL + " days.",
             say="That is 30 kWh."),
         box("A cost in pence = 27 " + MUL + " 30 = ", 810, "27 lots of 30p.", phase="substitute"),
         box("B cost in pence = 30 " + MUL + " 30 = ", 900, "30 lots of 30p."),
         box("Difference in pence = 900 " + MINUS + " 810 = ", 90, "Larger minus smaller.",
             say="That is 90p."),
         box("In pounds: 90 " + DIV + " 100 = ", 0.9, "100 pence in a pound.",
             done="So device B costs " + GBP + "0.90 more.")
     ]},
    {"unit": "C", "display": "A 230 V iron has a power rating of 2300 W. It is used for 20 minutes. Calculate the total charge that flows through the iron.",
     "solutions": [12000], "calculator": True, "input_type": "single_value",
     "hint": "Find the current, convert the time, then charge = current " + MUL + " time.",
     "misconceptions": [
         mis("forgot_step", "First I = P/V = 2300 " + DIV + " 230 = 10 A. Convert 20 minutes to 1200 s. Then Q = It = 10 " + MUL + " 1200 = 12,000 C.", None),
         mis("unit_error", "Convert 20 minutes to 1200 seconds before using Q = It. Using 20 gives only 200 C.", 200),
         mis("wrong_formula", "You need two equations: P = VI to find the current, then Q = It for the charge.", None)],
     "guided_steps": [
         sayonly("Two steps: current with \\(I = P/V\\), then charge with \\(Q = It\\). Convert the time to seconds."),
         box("Current = 2300 " + DIV + " 230 = ", 10, "How many 230s fit into 2300?", say="So the current is 10 A."),
         box("Time in seconds = 20 " + MUL + " 60 = ", 1200, "60 seconds in each minute."),
         box("Charge = current " + MUL + " time = 10 " + MUL + " 1200 = ", 12000, "Ten lots of 1200.",
             say="So the charge is 12,000 C.", phase="substitute"),
         box("Check: divide back, 12000 " + DIV + " 1200 = ", 10, "Charge divided by time returns the current.",
             done="Returns 10 A, the current, so 12,000 C is right.")
     ]},
    {"unit": GBP, "accept": 0.1, "display": "A 40 W LED TV and a 150 W plasma TV are both used for 5 hours a day. Calculate how much more the plasma TV costs to run per year (365 days) than the LED TV. Electricity costs 30p per kWh. Give your answer in pounds.",
     "solutions": [60.23], "calculator": True, "input_type": "single_value",
     "hint": "Use the power difference, convert to kW, then energy and cost over the year.",
     "misconceptions": [
         mis("forgot_step", "Work with the power difference: 0.11 kW " + MUL + " 5 " + MUL + " 365 = 200.75 kWh. Cost = 200.75 " + MUL + " 30 = 6022.5p = " + GBP + "60.23.", None),
         mis("unit_error", "Convert watts to kilowatts (40 W = 0.04 kW, 150 W = 0.15 kW), then multiply by hours per day and days per year.", None)],
     "guided_steps": [
         sayonly("The quickest route uses the power difference. Find it, convert to kW, then energy over the year, then cost."),
         box("Power difference = 150 " + MINUS + " 40 = ", 110, "Plasma minus LED.", say="That is 110 W."),
         box("In kW = 110 " + DIV + " 1000 = ", 0.11, "1000 W in a kW."),
         box("Extra energy = 0.11 " + MUL + " 5 " + MUL + " 365 = ", 200.75, "kW " + MUL + " hours per day " + MUL + " days.",
             say="That is 200.75 kWh."),
         box("Extra cost in pence = 200.75 " + MUL + " 30 = ", 6022.5, "200.75 lots of 30p.",
             say="That is 6022.5p.", phase="substitute"),
         box("In pounds, rounded to the nearest penny: 6022.5p = " + GBP, 60.23,
             "100 pence in a pound, rounded to the nearest penny.",
             done="So the plasma TV costs about " + GBP + "60.23 more per year.")
     ]},
]

pd["problem_bank"] = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "One equation, with every value already in volts, amps, ohms, watts, seconds or coulombs. Substitute and solve.",
    "silver_description": "Convert a unit first (watts to kilowatts, minutes to seconds) or rearrange the equation before you substitute.",
    "gold_description": "Two equations chained, an efficiency step, or a full energy bill with several appliances. Work in stages."
}

pd["worked_examples"] = [
    {"difficulty": "Bronze", "question": "A toaster draws a current of 4 A from a 230 V mains supply. Calculate its power.",
     "steps": [
         {"label": "Step 1: Recall the equation", "content": "<p>\\(P = VI\\)</p>"},
         {"label": "Step 2: Substitute", "content": "<p>\\(P = 230 \\times 4\\)</p>"},
         {"label": "Answer", "content": "<p>\\(P = 920\\) <strong>W</strong></p>", "is_answer": True}
     ]},
    {"difficulty": "Silver", "question": "A 2.5 kW oven is used for 1.5 hours. Electricity costs 30p per kWh. Calculate the cost of running the oven.",
     "steps": [
         {"label": "Step 1: Calculate energy in kWh", "content": "<p>Energy = power (kW) " + MUL + " time (hours) = 2.5 " + MUL + " 1.5 = 3.75 kWh</p>"},
         {"label": "Step 2: Calculate cost", "content": "<p>Cost = kWh " + MUL + " price per unit = 3.75 " + MUL + " 30</p>"},
         {"label": "Answer", "content": "<p>Cost = 112.5 <strong>p</strong> (" + GBP + "1.13 to the nearest penny)</p>", "is_answer": True}
     ]},
    {"difficulty": "Gold", "question": "A hairdryer has a power rating of 2000 W and operates on a 230 V supply. Available fuse ratings are 3 A, 5 A and 13 A. Which fuse should be used?",
     "steps": [
         {"label": "Step 1: Calculate the current", "content": "<p>Rearrange \\(P = VI\\) to \\(I = P/V = 2000/230\\)</p>"},
         {"label": "Step 2: Find the current", "content": "<p>\\(I = 8.70\\) A (to 2 d.p.)</p>"},
         {"label": "Step 3: Choose the fuse", "content": "<p>The current is 8.70 A. The fuse must be the next size <em>above</em> the normal operating current.</p>"},
         {"label": "Answer", "content": "<p><strong>13 A</strong> fuse (the 5 A would blow under normal use)</p>", "is_answer": True}
     ]},
]

pd["related_videos"] = []

with open("_mine_lesson_L04_b7ce.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)

def words(s): return len([w for w in s.replace("\\(", " ").replace("\\)", " ").split() if w])
print("method_card.content words:", words(pd["method_card"]["content"]))
print("wrote _mine_lesson_L04_b7ce.json")
