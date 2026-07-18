# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_canon_pd.json", encoding="utf-8"))

# ---- 1. Fix em dashes (validator fails on U+2014 anywhere student-facing) ----
mc = pd["method_card"]
mc["content"] = mc["content"].replace("Efficiency is a ratio — it has no unit.",
                                      "Efficiency is a ratio, so it has no unit.")
mc["content"] = mc["content"].replace("after an efficiency answer — it is dimensionless",
                                      "after an efficiency answer, as it is dimensionless")
mc["content"] = mc["content"].replace("—", ",")  # sweep any remaining em dashes
pd["exam_context"]["frequency"] = pd["exam_context"]["frequency"].replace(
    "High — efficiency", "High: efficiency")
for we in pd["worked_examples"]:
    for st in we["steps"]:
        st["label"] = st["label"].replace(" — ", ": ")

# ---- helpers ----
def box(pre, ans, hint, post="", say=None, done=None, phase=False):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase: d["phase"] = "substitute"
    return d
def say(s): return {"say": s}

pb = pd["problem_bank"]
pb["bronze_description"] = "One efficiency equation with the values ready to use. Straight substitution: divide, or multiply by 100, or subtract."
pb["silver_description"] = "Rearrange the efficiency equation to find the input or output, or take two steps to reach wasted power or energy."
pb["gold_description"] = "Multi-part questions: an efficiency plus the wasted energy, or a comparison of two devices, sometimes with a distractor value."

def find(tier, sol):
    for p in pb[tier]:
        if p["solutions"] == sol: return p
    raise KeyError((tier, sol))

MINUS = "−"  # unicode minus
TIMES = "×"  # multiplication sign
DIV = "÷"    # division sign

# ============ BRONZE ============
b = find("bronze", [0.25])
b["hint"] = "Efficiency is useful output over total input; here that is 50 over 200."
b["misconceptions"][0]["expect"] = 0.75
b["guided_steps"] = [
    say("Efficiency = useful output " + DIV + " total input. It is a ratio, so it has no unit."),
    box("The useful output in joules is: ", 50, "Read it from the question: the energy that does the job."),
    box("The total input in joules is: ", 200, "Read it from the question: the energy put in."),
    box("Now divide useful by total: 50 " + DIV + " 200 = ", 0.25, "Divide 50 by 200.", say="Now finish it off.", phase=True),
    box("Check: 0.25 " + TIMES + " 200 should rebuild the useful output. 0.25 " + TIMES + " 200 = ", 50,
        "Multiply 0.25 by 200.", done="Back to 50 J, so efficiency = 0.25 (no unit). About a quarter of the energy is useful.", phase=True),
]
b = find("bronze", [20])
b["hint"] = "Divide useful by total, then multiply by 100 for a percentage."
b["misconceptions"][0]["expect"] = 0.2
b["guided_steps"] = [
    say("Efficiency as a percentage = (useful " + DIV + " total) " + TIMES + " 100."),
    box("Useful energy transferred as light, in joules: ", 12, "The 12 J is the useful part, the light."),
    box("Total energy taken in, in joules: ", 60, "The 60 J is the total input."),
    box("Divide first: 12 " + DIV + " 60 = ", 0.2, "12 divided by 60.", say="Now finish it off.", phase=True),
    box("Scale to a percentage: 0.2 " + TIMES + " 100 = ", 20, "Multiply the decimal by 100.",
        done="Efficiency = 20%. Only a fifth of the electricity becomes light; the rest is wasted as heat.", phase=True),
]
b = find("bronze", [150])
b["hint"] = "Wasted energy is just total input minus useful output."
b["misconceptions"][0]["pattern"] = "wrong_equation"
b["misconceptions"][0]["expect"] = 0.7
b["misconceptions"][0]["message"] = "Wasted energy is a subtraction, not the efficiency ratio. Wasted = 500 " + MINUS + " 350 = 150 J. Dividing (350/500 = 0.7) gives the efficiency, not the wasted energy."
b["guided_steps"] = [
    say("Wasted energy = total input " + MINUS + " useful output. This is a subtraction, not the efficiency ratio."),
    box("Total input, in joules: ", 500, "The energy put in."),
    box("Useful output, in joules: ", 350, "The energy that does the job."),
    box("Subtract useful from total: 500 " + MINUS + " 350 = ", 150, "500 take away 350.", say="Now finish it off.", phase=True),
    box("Check: useful + wasted should rebuild the input. 350 + 150 = ", 500, "Add 350 and 150.",
        done="Back to 500 J, so 150 J is wasted.", phase=True),
]
b = find("bronze", [0.75])
b["hint"] = "Efficiency is useful power over total power; the units cancel."
b["misconceptions"][0]["expect"] = 0.25
b["misconceptions"][0]["message"] = "Use useful power in the numerator, not wasted power. Efficiency = 300 " + DIV + " 400 = 0.75. Wasted power (100 W) over total gives 0.25, which is the wrong quantity."
b["guided_steps"] = [
    say("Efficiency = useful power " + DIV + " total power. Power works the same as energy here because the shared time cancels."),
    box("Useful power output, in watts: ", 300, "The power that does the job."),
    box("Total power input, in watts: ", 400, "The power supplied."),
    box("Divide useful by total: 300 " + DIV + " 400 = ", 0.75, "300 divided by 400.", say="Now finish it off.", phase=True),
    box("Check: 0.75 " + TIMES + " 400 = ", 300, "Multiply 0.75 by 400.",
        done="Back to 300 W, so efficiency = 0.75 (no unit).", phase=True),
]
b = find("bronze", [1840])
b["hint"] = "Useful output is efficiency times total input."
b["misconceptions"][0]["expect"] = 2173.91
b["misconceptions"][0]["message"] = "Useful = efficiency " + TIMES + " total input = 0.92 " + TIMES + " 2000 = 1840 W. Dividing the input by the efficiency instead gives about 2174 W, which is larger than the input and cannot be right."
b["guided_steps"] = [
    say("Rearrange efficiency = useful " + DIV + " total to get useful output = efficiency " + TIMES + " total input."),
    box("The efficiency (a decimal) is: ", 0.92, "Read it from the question."),
    box("The total input power, in watts: ", 2000, "Read it from the question."),
    box("Multiply: 0.92 " + TIMES + " 2000 = ", 1840, "0.92 times 2000.", say="Now finish it off.", phase=True),
    box("Check: 1840 " + DIV + " 2000 should give the efficiency back. 1840 " + DIV + " 2000 = ", 0.92, "Divide 1840 by 2000.",
        done="Back to 0.92, so the useful output is 1840 W.", phase=True),
]
b = find("bronze", [18000])
b["hint"] = "Useful output is efficiency times total input."
b["misconceptions"][0]["expect"] = 200000
b["misconceptions"][0]["message"] = "Useful = efficiency " + TIMES + " total input = 0.30 " + TIMES + " 60000 = 18000 J. Dividing by the efficiency instead gives 200000 J, more than was put in."
b["guided_steps"] = [
    say("Useful output = efficiency " + TIMES + " total input."),
    box("The efficiency (a decimal) is: ", 0.3, "0.30 written as a decimal."),
    box("The total input, in joules: ", 60000, "Read it from the question."),
    box("Multiply: 0.3 " + TIMES + " 60000 = ", 18000, "0.3 times 60000.", say="Now finish it off.", phase=True),
    box("Check: 18000 " + DIV + " 60000 = ", 0.3, "Divide 18000 by 60000.",
        done="Back to 0.3, so the useful output is 18000 J.", phase=True),
]

# ============ SILVER ============
s = find("silver", [35])
s["hint"] = "Divide useful power by total power, then multiply by 100."
s["misconceptions"][0]["expect"] = 65
s["misconceptions"][0]["message"] = "Efficiency = (useful " + DIV + " total) " + TIMES + " 100 = (2800/8000) " + TIMES + " 100 = 35%. Using the wasted power (5200 W) in the numerator gives 65%, the wrong quantity."
s["guided_steps"] = [
    say("Efficiency as a percentage = (useful power " + DIV + " total power) " + TIMES + " 100."),
    box("Useful electrical power output, in watts: ", 2800, "The power that does the job."),
    box("Total power input from the wind, in watts: ", 8000, "The power available in the wind."),
    box("Divide first: 2800 " + DIV + " 8000 = ", 0.35, "2800 divided by 8000.", say="Now finish it off.", phase=True),
    box("Scale to a percentage: 0.35 " + TIMES + " 100 = ", 35, "Multiply by 100.",
        done="Efficiency = 35%. A good real wind turbine sits near this figure.", phase=True),
]
s = find("silver", [2000])
s["hint"] = "To find the input, divide the useful output by the efficiency."
s["misconceptions"][0]["expect"] = 405
s["misconceptions"][0]["message"] = "Total input = useful output " + DIV + " efficiency = 900 " + DIV + " 0.45 = 2000 W. Multiplying instead (900 " + TIMES + " 0.45 = 405 W) gives less than the output, which is impossible."
s["guided_steps"] = [
    say("Rearrange efficiency = useful " + DIV + " total to make the total the subject: total input = useful " + DIV + " efficiency."),
    box("The useful power output, in watts: ", 900, "The power that does the job."),
    box("The efficiency (a decimal) is: ", 0.45, "Read it from the question."),
    box("Divide useful output by efficiency: 900 " + DIV + " 0.45 = ", 2000, "900 divided by 0.45.", say="Now finish it off.", phase=True),
    box("Check: 0.45 " + TIMES + " 2000 should rebuild the useful output. 0.45 " + TIMES + " 2000 = ", 900, "Multiply 0.45 by 2000.",
        done="Back to 900 W, so the total input is 2000 W.", phase=True),
]
s = find("silver", [51])
s["hint"] = "Find the useful power first, then subtract it from the input."
s["misconceptions"][0]["expect"] = 9
s["misconceptions"][0]["message"] = "Two steps. Useful = 0.15 " + TIMES + " 60 = 9 W. Wasted = 60 " + MINUS + " 9 = 51 W. Stopping at 9 W gives the useful power, not the wasted power."
s["guided_steps"] = [
    say("Two steps. First find the useful power (efficiency " + TIMES + " input), then wasted = input " + MINUS + " useful."),
    box("The efficiency (a decimal) is: ", 0.15, "Read it from the question."),
    box("The total input power, in watts: ", 60, "The power supplied."),
    box("First the useful power: 0.15 " + TIMES + " 60 = ", 9, "0.15 times 60.", say="Now finish it off.", phase=True),
    box("Now the wasted power: 60 " + MINUS + " 9 = ", 51, "Take the useful 9 W from the 60 W input.",
        done="Wasted at a rate of 51 W. Most of the bulb's electricity leaks away as heat.", phase=True),
]
s = find("silver", [32000])
s["hint"] = "Wasted energy is total input minus useful output."
s["misconceptions"][0]["pattern"] = "wrong_equation"
s["misconceptions"][0]["expect"] = 0.36
s["misconceptions"][0]["message"] = "Wasted = total " + MINUS + " useful = 50000 " + MINUS + " 18000 = 32000 J. Dividing (18000/50000 = 0.36) gives the efficiency, not the wasted energy."
s["guided_steps"] = [
    say("Wasted energy = total input " + MINUS + " useful output."),
    box("Total energy input, in joules: ", 50000, "The energy from the fuel."),
    box("Useful kinetic energy output, in joules: ", 18000, "The energy that moves the car."),
    box("Subtract: 50000 " + MINUS + " 18000 = ", 32000, "50000 take away 18000.", say="Now finish it off.", phase=True),
    box("Check: 18000 + 32000 = ", 50000, "Add useful and wasted.",
        done="Back to 50000 J, so 32000 J is wasted.", phase=True),
]

# ============ GOLD ============
g = find("gold", [40])
g["hint"] = "Efficiency is useful over total, times 100; wasted is total minus useful."
g["misconceptions"][0]["expect"] = 60
g["misconceptions"][0]["message"] = "Efficiency = (800/2000) " + TIMES + " 100 = 40%. Wasted = 2000 " + MINUS + " 800 = 1200 MW. Putting the wasted power in the numerator gives 60%, the wrong quantity."
g["guided_steps"] = [
    say("Two things are asked. Efficiency as a percentage = (useful " + DIV + " total) " + TIMES + " 100, and wasted = total " + MINUS + " useful. The typed answer is the efficiency."),
    box("Useful electrical power output, in MW: ", 800, "The power sent to the grid."),
    box("Total thermal power input, in MW: ", 2000, "The power from burning coal."),
    box("Efficiency first: 800 " + DIV + " 2000 = ", 0.4, "800 divided by 2000.", say="Now finish it off.", phase=True),
    box("As a percentage: 0.4 " + TIMES + " 100 = ", 40, "Multiply by 100.", phase=True),
    box("And the wasted power for the second part: 2000 " + MINUS + " 800 = ", 1200, "Total minus useful.",
        done="Efficiency = 40%, and 1200 MW is wasted as heat. Enter 40.", phase=True),
]
g = find("gold", [975])
g["hint"] = "The time is a distractor; useful output is efficiency times input."
g["misconceptions"][0]["pattern"] = "inverse_error"
g["misconceptions"][0]["expect"] = 2307.69
g["misconceptions"][0]["message"] = "Useful output = efficiency " + TIMES + " input = 0.65 " + TIMES + " 1500 = 975 J. Dividing by the efficiency instead gives about 2308 J, which is bigger than the input and cannot be right. The 30 seconds is not needed."
g["guided_steps"] = [
    say("The 30 seconds is a distractor: efficiency already links the two energies. Useful output = efficiency " + TIMES + " input."),
    box("The efficiency (a decimal) is: ", 0.65, "Read it from the question."),
    box("The input energy over the 30 seconds, in joules: ", 1500, "The energy taken in."),
    box("Multiply: 0.65 " + TIMES + " 1500 = ", 975, "0.65 times 1500.", say="Now finish it off.", phase=True),
    box("Check: 975 " + DIV + " 1500 = ", 0.65, "Divide 975 by 1500.",
        done="Back to 0.65, so the useful output is 975 J. The 30 seconds never mattered.", phase=True),
]
g = find("gold", [15000])
g["hint"] = "The input is unknown, so divide the useful output by the efficiency."
g["misconceptions"][0]["expect"] = 10837.5
g["misconceptions"][0]["message"] = "The useful output is given and the input is unknown, so total input = useful " + DIV + " efficiency = 12750 " + DIV + " 0.85 = 15000 J. Multiplying instead (12750 " + TIMES + " 0.85 = 10837.5 J) gives less than the output, which is impossible."
g["guided_steps"] = [
    say("Here the useful output is given and the input is unknown. Rearrange to total input = useful " + DIV + " efficiency."),
    box("The useful heat energy to deliver, in joules: ", 12750, "The heat the boiler must supply."),
    box("The efficiency (a decimal) is: ", 0.85, "Read it from the question."),
    box("Divide useful by efficiency: 12750 " + DIV + " 0.85 = ", 15000, "12750 divided by 0.85.", say="Now finish it off.", phase=True),
    box("Check: 0.85 " + TIMES + " 15000 = ", 12750, "Multiply 0.85 by 15000.",
        done="Back to 12750 J, so the total input needed is 15000 J.", phase=True),
]
g = find("gold", [0.2])
g["hint"] = "Work out each lamp's efficiency and compare the decimals."
g["misconceptions"][0]["expect"] = None
g["misconceptions"][0]["message"] = "Lamp A: 8/40 = 0.20. Lamp B: 3/12 = 0.25. Lamp B is more efficient because 0.25 > 0.20. The typed answer is Lamp A's efficiency, 0.20."
g["guided_steps"] = [
    say("Compare by working out each efficiency (useful " + DIV + " total). The bigger decimal wins."),
    box("Lamp A useful light output, in watts: ", 8, "Lamp A's output."),
    box("Lamp A total input, in watts: ", 40, "Lamp A's input."),
    box("Efficiency of Lamp A: 8 " + DIV + " 40 = ", 0.2, "8 divided by 40.", say="Now finish it off.", phase=True),
    box("Now Lamp B for the comparison: 3 " + DIV + " 12 = ", 0.25, "3 divided by 12.",
        done="Lamp A is 0.20, Lamp B is 0.25, so Lamp B is more efficient. The typed answer, Lamp A's efficiency, is 0.20.", phase=True),
]

# ---- 3. tier_guides ----
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one efficiency equation, values ready to use",
        "steps": [
            "<strong>Efficiency = useful output " + DIV + " total input.</strong> It is a ratio, so it never carries a unit.",
            "For a percentage, multiply the decimal by 100. For wasted energy, use wasted = total input " + MINUS + " useful output.",
            "Read the two values straight from the question, then substitute and calculate."
        ],
        "example": {
            "question": "A speaker takes in 30 J and outputs 6 J as sound. Find its efficiency as a decimal.",
            "steps": [
                {"label": "Write the equation", "content": "<p>Efficiency = useful " + DIV + " total</p>"},
                {"label": "Substitute", "content": "<p>= 6 " + DIV + " 30</p>"},
                {"label": "Check", "content": "<p>0.2 " + TIMES + " 30 = 6</p>"},
                {"label": "Answer", "content": "<p><strong>0.2</strong> (no unit)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: rearrange the equation or take a second step",
        "steps": [
            "If the efficiency is given, find the useful output (useful = efficiency " + TIMES + " total) or the total input (total = useful " + DIV + " efficiency).",
            "Wasted power or energy needs two steps: find the useful amount first, then subtract it from the input.",
            "Power (W) and energy (J) both fit the efficiency equation because the shared time cancels."
        ],
        "example": {
            "question": "A motor has efficiency 0.60 and a useful output of 240 W. Find the total input power.",
            "steps": [
                {"label": "Rearrange", "content": "<p>total = useful " + DIV + " efficiency</p>"},
                {"label": "Substitute", "content": "<p>= 240 " + DIV + " 0.60</p>"},
                {"label": "Check", "content": "<p>0.60 " + TIMES + " 400 = 240</p>"},
                {"label": "Answer", "content": "<p><strong>400 W</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: multi-step and comparison problems",
        "steps": [
            "Gold questions ask for more than one thing: an efficiency AND the wasted energy, or a comparison of two devices.",
            "Work each device's efficiency separately (useful " + DIV + " total). The larger decimal is the more efficient one.",
            "Watch for distractors like a stated time: efficiency links the energies directly, so a time value is often not needed."
        ],
        "example": {
            "question": "Engine X: 80 kJ in, 20 kJ useful. Engine Y: 50 kJ in, 15 kJ useful. Which is more efficient?",
            "steps": [
                {"label": "Engine X", "content": "<p>20 " + DIV + " 80 = 0.25</p>"},
                {"label": "Engine Y", "content": "<p>15 " + DIV + " 50 = 0.30</p>"},
                {"label": "Compare", "content": "<p>0.30 &gt; 0.25</p>"},
                {"label": "Answer", "content": "<p><strong>Engine Y</strong> is more efficient</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---- 4. guided (opener + teach) ----
pd["guided"] = {
    "opener": {
        "display": "Efficiency: how much of what you pay for actually does the job.",
        "steps": [
            say("A quick one, no equations. An old light bulb glows, but hold your hand near it and it is hot. You pay for light, yet a lot of the electricity leaks away as heat."),
            say("Say you pay for 100 joules of electricity. 80 joules leak away as heat you can feel. The rest comes out as light."),
            box("How many joules come out as light? 100 " + MINUS + " 80 = ", 20, "Take the 80 wasted joules from the 100 you paid for."),
            say("So out of every 100 joules, only 20 do the job you actually wanted."),
            box("Write that useful share as a decimal fraction of 100: 20 " + DIV + " 100 = ", 0.2, "20 out of 100."),
            say("That number, <strong>useful out of total</strong>, is <strong>efficiency</strong>. 0.2 means only a fifth of what you paid for did the job. The equation just writes it: efficiency = useful " + DIV + " total, and it has no unit.")
        ]
    },
    "teach": {
        "bronze": {
            "display": "A phone charger takes in 5 J of electrical energy and delivers 4 J to the battery. Calculate its efficiency as a decimal.",
            "steps": [
                say("Efficiency = useful output " + DIV + " total input, and it has no unit."),
                box("Useful energy delivered to the battery, in joules: ", 4, "The energy that reaches the battery."),
                box("Total energy taken in, in joules: ", 5, "The energy drawn from the mains."),
                box("Divide useful by total: 4 " + DIV + " 5 = ", 0.8, "4 divided by 5.", done="That is the efficiency: 0.8, no unit."),
                box("Check: 0.8 " + TIMES + " 5 should give back 4. 0.8 " + TIMES + " 5 = ", 4, "Multiply 0.8 by 5.",
                    done="Back to 4 J. A charger this good wastes only a fifth.")
            ]
        },
        "silver": {
            "display": "A pump has efficiency 0.40 and a useful power output of 120 W. Calculate the total power input.",
            "steps": [
                say("The efficiency is given and the input is unknown, so rearrange: total input = useful " + DIV + " efficiency."),
                box("The useful power output, in watts: ", 120, "The power that does the job."),
                box("The efficiency as a decimal: ", 0.4, "Read it from the question."),
                box("Divide useful by efficiency: 120 " + DIV + " 0.4 = ", 300, "120 divided by 0.4.", done="Total input = 300 W."),
                box("Check: 0.4 " + TIMES + " 300 = ", 120, "Multiply 0.4 by 300.", done="Back to 120 W, so 300 W input is right.")
            ]
        },
        "gold": {
            "display": "A diesel generator takes in 90,000 J of chemical energy and delivers 27,000 J of useful electrical energy. Calculate its efficiency as a percentage and the energy wasted.",
            "steps": [
                say("Two parts. Efficiency as a percentage = (useful " + DIV + " total) " + TIMES + " 100, then wasted = total " + MINUS + " useful."),
                box("Useful electrical energy, in joules: ", 27000, "The energy delivered as electricity."),
                box("Total chemical energy input, in joules: ", 90000, "The energy from the diesel."),
                box("Efficiency: 27000 " + DIV + " 90000 = ", 0.3, "27000 divided by 90000."),
                box("As a percentage: 0.3 " + TIMES + " 100 = ", 30, "Multiply by 100.", done="Efficiency = 30%."),
                box("Wasted energy: 90000 " + MINUS + " 27000 = ", 63000, "Total minus useful.",
                    done="63000 J is wasted as heat and sound.")
            ]
        }
    }
}

json.dump(pd, io.open("lesson_physics-calculations-L02@ffe1cce606.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("built OK")
