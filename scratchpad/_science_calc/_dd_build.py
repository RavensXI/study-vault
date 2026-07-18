# -*- coding: utf-8 -*-
import json, os, re

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, "_dd_canonical_live.json")
OUT = os.path.join(HERE, "lesson_higher-calculations-L06@d1cc4db5ec.json")

pd = json.load(open(SRC, encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayd(text):
    return {"say": text}

# ------------------------------------------------------------------ method_card
pd["method_card"]["content"] = (
    "<p>Two equations. The <strong>turns ratio</strong> "
    "\\(V_s = V_p \\times (N_s / N_p)\\) links voltage to the number of turns: "
    "keep primary over primary and secondary over secondary, or the ratio "
    "inverts. The <strong>power balance</strong> \\(V_p I_p = V_s I_s\\) holds "
    "for an ideal transformer, so if voltage steps up, current steps down by "
    "the same factor.</p>"
    "<p>The National Grid steps voltage up to cut the current, because power "
    "wasted as heat in the cables is \\(P = I^2 R\\). Check whether your board "
    "gives you these equations.</p>"
)

# ------------------------------------------------------------------ tier descriptions
pb = pd["problem_bank"]
pb["bronze_description"] = "One transformer equation, values already in the right units, substitute straight in."
pb["silver_description"] = "Rearrange the equation first, or balance the power to find a current."
pb["gold_description"] = "Chain two equations: find the new current, then the power lost in the cables."

# ------------------------------------------------------------------ misconceptions (add expect)
def mis(pattern, expect, message):
    return [{"check": "common", "pattern": pattern, "expect": expect, "message": message}]

MIS = {
    ("bronze",0): mis("inverse_error",0.6,
        "The ratio is Ns/Np, secondary over primary: 2000/100 = 20, so Vs = 12 × 20 = 240 V. Flipping it to 100/2000 gives 0.6 V, far too small for a step-up transformer."),
    ("bronze",1): mis("inverse_error",4,
        "Ns = Np × (Vs/Vp) = 200 × (11 500/230) = 200 × 50 = 10 000 turns. Flipping the voltage ratio to 230/11 500 gives just 4 turns."),
    ("bronze",2): mis("inverse_error",8000,
        "Voltage steps up, so current steps down: Is = (Vp × Ip)/Vs = (1000 × 400)/20 000 = 20 A. Multiplying current up with voltage, 400 × 20, gives 8000 A and breaks energy conservation."),
    ("bronze",3): mis("inverse_error",2400,
        "Ns/Np = 80/800 = 0.1, so Vs = 240 × 0.1 = 24 V, a step-down. Flipping to 800/80 = 10 gives 2400 V, a step-up, which is wrong here."),
    ("bronze",4): mis("inverse_error",1200,
        "Ip = (Vs × Is)/Vp = (20 × 60)/400 = 3 A. Putting Vp on top, (400 × 60)/20, gives 1200 A and ignores that the primary is the high-voltage, low-current side."),
    ("bronze",5): mis("wrong_type",1,
        "The secondary has fewer turns (40 < 400), so the voltage drops: it is a step-down transformer, answer 2. Answer 1, step-up, would need more secondary turns."),
    ("silver",0): mis("inverse_error",15.33,
        "Ns/Np = 4500/300 = 15, so Vs = 230 × 15 = 3450 V. Flipping to 300/4500 gives about 15.3 V, far too small for a step-up."),
    ("silver",1): mis("inverse_error",41.8,
        "Ip = (Vs × Is)/Vp = (11 × 2.0)/230 = 0.0957 A. Putting Vp on top, (230 × 2.0)/11, gives 41.8 A, but the 230 V primary must carry the smaller current."),
    ("silver",2): mis("inverse_error",12800,
        "Is = (Vp × Ip)/Vs = (25 000 × 800)/400 000 = 50 A. Swapping to (Vs × Ip)/Vp gives 12 800 A, but stepping voltage up must lower the current."),
    ("silver",3): mis("forgot_square",100,
        "P = I²R, so square the current first: 50² × 2 = 2500 × 2 = 5000 W. Forgetting to square, 50 × 2, gives only 100 W."),
    ("silver",4): mis("inverse_error",24000,
        "Ns = Np × (Vs/Vp) = 1200 × (12/240) = 1200 × 0.05 = 60 turns. Flipping the ratio to 240/12 = 20 gives 24 000 turns, a step-up, which is wrong for a step-down."),
    ("gold",0): mis("inverse_error",125,
        "Ns/Np = 40 000/200 = 200, so Vs = 25 000 × 200 = 5 000 000 V. Flipping to 200/40 000 gives 125 V, but far more secondary turns must step the voltage up."),
    ("gold",1): mis("inverse_error",100000,
        "Is = (Vp × Ip)/Vs = (25 000 × 500)/5 000 000 = 2.5 A. Swapping Vp and Vs, (5 000 000 × 500)/25 000, gives 100 000 A and ignores that a huge voltage means a tiny current."),
    ("gold",2): mis("forgot_square",250,
        "P = I²R, square first: 2.5² × 100 = 6.25 × 100 = 625 W. Forgetting the square, 2.5 × 100, gives 250 W."),
    ("gold",3): mis("inverse_error",47826,
        "Ns = Np × (Vs/Vp) = 1000 × (230/11 000) ≈ 20.9 turns. Flipping to 11 000/230 ≈ 47 826 turns would step the voltage up, not down."),
    ("gold",4): mis("wrong_formula",3,
        "P = V × I, so Is = P/Vs = 3/9 = 0.333 A. Dividing the wrong way round, 9/3, gives 3 A."),
}

# ------------------------------------------------------------------ gold hints (gold lacks hint/equation_hint)
GOLD_HINT = {
    0: "Find the turns ratio Ns/Np first, then multiply the primary voltage by it.",
    1: "Ideal transformer: power in equals power out. Is = (Vp × Ip) / Vs.",
    2: "Power lost in cables is P = I²R. Square the current before multiplying by R.",
    3: "Ns = Np × (Vs/Vp). The voltage falls, so expect fewer secondary turns.",
    4: "The secondary delivers P = Vs × Is. Rearrange: Is = P / Vs.",
}

# ------------------------------------------------------------------ guided_steps per problem
EQ_TURNS = "Turns ratio: <strong>\\(V_s = V_p \\times (N_s / N_p)\\)</strong>. Volts per turn is the same on both coils, so voltage splits in the same ratio as the turns."
EQ_POWER = "Ideal transformer: power in = power out, <strong>\\(V_p I_p = V_s I_s\\)</strong>. If voltage steps up, current steps down by the same factor."
EQ_LOSS  = "Power wasted as heat in the cables is <strong>\\(P = I^2 R\\)</strong>. Square the current first."

GS = {}

GS[("bronze",0)] = [
    sayd(EQ_TURNS),
    box("Turns ratio Ns/Np = 2000 / 100 = ", 20, "Secondary turns over primary turns."),
    box("Vs = Vp × ratio = 12 × 20 = ", 240, "Multiply the primary voltage by the ratio.", phase="substitute",
        say="The secondary has 20 times the turns, so 20 times the voltage."),
    box("Check by cross-multiplying: Vs × Np = 240 × 100 = ", 24000,
        "This should equal Vp × Ns.",
        done="That equals Vp × Ns = 12 × 2000 = 24 000, so Vs = 240 V is right."),
]

GS[("bronze",1)] = [
    sayd(EQ_TURNS + " Rearranged for turns: \\(N_s = N_p \\times (V_s / V_p)\\)."),
    box("Voltage ratio Vs/Vp = 11 500 / 230 = ", 50, "Secondary voltage over primary voltage."),
    box("Ns = Np × ratio = 200 × 50 = ", 10000, "Multiply the primary turns by the voltage ratio.", phase="substitute",
        say="The voltage is 50 times bigger, so the secondary needs 50 times the turns."),
    box("Check: Vs × Np = 11 500 × 200 = ", 2300000,
        "This should equal Vp × Ns.",
        done="That equals Vp × Ns = 230 × 10 000 = 2 300 000, so Ns = 10 000 turns is right."),
]

GS[("bronze",2)] = [
    sayd(EQ_POWER + " Rearranged for the secondary current: \\(I_s = (V_p I_p) / V_s\\)."),
    box("Power the primary delivers: Vp × Ip = 1000 × 400 = ", 400000, "Multiply primary voltage by primary current.", post=" W"),
    box("Is = power / Vs = 400 000 / 20 000 = ", 20, "Divide the power by the secondary voltage.", post=" A", phase="substitute",
        say="The secondary carries the same power at a higher voltage, so a smaller current."),
    box("Check power out: Vs × Is = 20 000 × 20 = ", 400000, "This should match the power in.", post=" W",
        done="400 000 W in equals 400 000 W out, so Is = 20 A is right."),
]

GS[("bronze",3)] = [
    sayd(EQ_TURNS),
    box("Turns ratio Ns/Np = 80 / 800 = ", 0.1, "Secondary turns over primary turns."),
    box("Vs = Vp × ratio = 240 × 0.1 = ", 24, "Multiply the primary voltage by the ratio.", post=" V", phase="substitute",
        say="Fewer turns on the secondary, so the voltage steps down."),
    box("Check: Vs × Np = 24 × 800 = ", 19200, "This should equal Vp × Ns.",
        done="That equals Vp × Ns = 240 × 80 = 19 200, so Vs = 24 V is right."),
]

GS[("bronze",4)] = [
    sayd(EQ_POWER + " Rearranged for the primary current: \\(I_p = (V_s I_s) / V_p\\)."),
    box("Power the secondary delivers: Vs × Is = 20 × 60 = ", 1200, "Multiply secondary voltage by secondary current.", post=" W"),
    box("Ip = power / Vp = 1200 / 400 = ", 3, "Divide the power by the primary voltage.", post=" A", phase="substitute",
        say="The primary is the high-voltage side, so it draws the smaller current."),
    box("Check power in: Vp × Ip = 400 × 3 = ", 1200, "This should match the power out.", post=" W",
        done="1200 W in equals 1200 W out, so Ip = 3 A is right."),
]

GS[("bronze",5)] = [
    sayd("Compare the number of turns on each coil. More turns on the secondary steps voltage up; fewer steps it down."),
    box("Read off the secondary turns: Ns = ", 40, "It is written on the secondary coil."),
    box("Turns ratio Ns/Np = 40 / 400 = ", 0.1, "Secondary turns over primary turns.", phase="substitute",
        say="The ratio is below 1, so the secondary voltage is smaller than the primary."),
    box("A ratio below 1 means the voltage drops. Enter 2 for step-down: ", 2, "Voltage falls, so it is a step-down transformer.",
        done="Fewer secondary turns than primary, so it is a step-down transformer, answer 2."),
]

GS[("silver",0)] = [
    sayd(EQ_TURNS),
    box("Turns ratio Ns/Np = 4500 / 300 = ", 15, "Secondary turns over primary turns."),
    box("Vs = Vp × ratio = 230 × 15 = ", 3450, "Multiply the primary voltage by the ratio.", post=" V", phase="substitute",
        say="Fifteen times the turns, so fifteen times the voltage."),
    box("Check: Vs × Np = 3450 × 300 = ", 1035000, "This should equal Vp × Ns.",
        done="That equals Vp × Ns = 230 × 4500 = 1 035 000, so Vs = 3450 V is right."),
]

GS[("silver",1)] = [
    sayd(EQ_POWER + " Rearranged for the primary current: \\(I_p = (V_s I_s) / V_p\\)."),
    box("Power the secondary delivers: Vs × Is = 11 × 2.0 = ", 22, "Multiply secondary voltage by secondary current.", post=" W"),
    box("Ip = power / Vp = 22 / 230 = ", 0.0957, "Divide the power by the primary voltage; round to 3 significant figures.", post=" A", phase="substitute",
        say="The 230 V primary carries the same 22 W, so only a small current."),
    box("Check the balance: the primary must handle the same power, Vs × Is = 11 × 2.0 = ", 22, "Power in equals power out.", post=" W",
        done="Both coils carry 22 W, so Ip = 0.0957 A (about 0.096 A) is right."),
]

GS[("silver",2)] = [
    sayd(EQ_POWER + " Rearranged for the secondary current: \\(I_s = (V_p I_p) / V_s\\)."),
    box("Power generated: Vp × Ip = 25 000 × 800 = ", 20000000, "Multiply primary voltage by primary current.", post=" W"),
    box("Is = power / Vs = 20 000 000 / 400 000 = ", 50, "Divide the power by the secondary voltage.", post=" A", phase="substitute",
        say="Voltage rose by 16 times, so current falls by 16 times."),
    box("Check power out: Vs × Is = 400 000 × 50 = ", 20000000, "This should match the power in.", post=" W",
        done="20 000 000 W in equals 20 000 000 W out, so Is = 50 A is right."),
]

GS[("silver",3)] = [
    sayd(EQ_LOSS),
    box("Square the current: 50² = ", 2500, "Fifty times fifty."),
    box("P = I²R = 2500 × 2 = ", 5000, "Multiply the squared current by the resistance.", post=" W", phase="substitute",
        say="Because P depends on the square of the current, keeping the current low keeps the loss low."),
    box("See why it matters: if the current were only 25 A, loss = 25² × 2 = ", 1250, "Square 25, then multiply by 2.", post=" W",
        done="Half the current gives a quarter of the loss (1250 W vs 5000 W), which is why the grid keeps current small. Answer 5000 W."),
]

GS[("silver",4)] = [
    sayd(EQ_TURNS + " Rearranged for turns: \\(N_s = N_p \\times (V_s / V_p)\\)."),
    box("Voltage ratio Vs/Vp = 12 / 240 = ", 0.05, "Secondary voltage over primary voltage."),
    box("Ns = Np × ratio = 1200 × 0.05 = ", 60, "Multiply the primary turns by the voltage ratio.", post=" turns", phase="substitute",
        say="The voltage is one twentieth, so the secondary needs one twentieth of the turns."),
    box("Check: Vs × Np = 12 × 1200 = ", 14400, "This should equal Vp × Ns.",
        done="That equals Vp × Ns = 240 × 60 = 14 400, so Ns = 60 turns is right."),
]

GS[("gold",0)] = [
    sayd(EQ_TURNS),
    box("Turns ratio Ns/Np = 40 000 / 200 = ", 200, "Secondary turns over primary turns."),
    box("Vs = Vp × ratio = 25 000 × 200 = ", 5000000, "Multiply the primary voltage by the ratio.", post=" V", phase="substitute",
        say="Two hundred times the turns, so two hundred times the voltage: a huge step-up."),
    box("Check: Vs × Np = 5 000 000 × 200 = ", 1000000000, "This should equal Vp × Ns.",
        done="That equals Vp × Ns = 25 000 × 40 000 = 1 000 000 000, so Vs = 5 000 000 V is right."),
]

GS[("gold",1)] = [
    sayd(EQ_POWER + " Rearranged for the secondary current: \\(I_s = (V_p I_p) / V_s\\)."),
    box("Power generated: Vp × Ip = 25 000 × 500 = ", 12500000, "Multiply primary voltage by primary current.", post=" W"),
    box("Is = power / Vs = 12 500 000 / 5 000 000 = ", 2.5, "Divide the power by the secondary voltage.", post=" A", phase="substitute",
        say="A huge secondary voltage means a tiny secondary current."),
    box("Check power out: Vs × Is = 5 000 000 × 2.5 = ", 12500000, "This should match the power in.", post=" W",
        done="12 500 000 W in equals 12 500 000 W out, so Is = 2.5 A is right."),
]

GS[("gold",2)] = [
    sayd(EQ_LOSS),
    box("Square the current: 2.5² = ", 6.25, "Two point five times two point five."),
    box("P = I²R = 6.25 × 100 = ", 625, "Multiply the squared current by the resistance.", post=" W", phase="substitute",
        say="Only a small current flows, so the wasted power stays small."),
    box("See why it matters: at ten times the current, 25 A, loss = 25² × 100 = ", 62500, "Square 25, then multiply by 100.", post=" W",
        done="Ten times the current gives a hundred times the loss (62 500 W vs 625 W). Answer 625 W."),
]

GS[("gold",3)] = [
    sayd(EQ_TURNS + " Rearranged for turns: \\(N_s = N_p \\times (V_s / V_p)\\)."),
    box("Voltage ratio Vs/Vp = 230 / 11 000 = ", 0.0209, "Secondary voltage over primary voltage; round to 3 significant figures."),
    box("Ns = Np × ratio = 1000 × 0.0209 = ", 20.9, "Multiply the primary turns by the voltage ratio.", post=" turns", phase="substitute",
        say="The voltage drops a lot, so the secondary needs very few turns."),
    box("A real coil needs whole turns, so round 20.9 up to ", 21, "Round to the nearest whole turn.", post=" turns",
        done="About 21 turns, far fewer than the 1000 primary turns, confirming a step-down. Answer 20.9 turns."),
]

GS[("gold",4)] = [
    sayd("The secondary delivers a power P = Vs × Is. Rearranged for the current: <strong>\\(I_s = P / V_s\\)</strong>."),
    box("Read off the secondary voltage: Vs = ", 9, "It is the stepped-down voltage.", post=" V"),
    box("Is = P / Vs = 3 / 9 = ", 0.333, "Divide the power by the secondary voltage; round to 3 significant figures.", post=" A", phase="substitute",
        say="A small load power at 9 V draws only a third of an amp."),
    box("Check with P = V × I: 9 × 0.333 = ", 3, "This should come back to about 3 W.", post=" W",
        done="That gives about 3 W, matching the stated power, so Is = 0.333 A is right."),
]

# attach misconceptions, hints, guided_steps
TIERS = ["bronze","silver","gold"]
for tier in TIERS:
    for i,p in enumerate(pb[tier]):
        p["misconceptions"] = MIS[(tier,i)]
        p["guided_steps"] = GS[(tier,i)]
        if tier == "gold" and not p.get("equation_hint"):
            p["hint"] = GOLD_HINT[i]

# ------------------------------------------------------------------ tier_guides
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one transformer equation, straight in",
        "steps": [
            "Use the turns ratio <strong>\\(V_s = V_p \\times (N_s / N_p)\\)</strong>. Voltage splits in the same ratio as the turns.",
            "More turns on the secondary steps voltage up; fewer steps it down.",
            "Substitute the values and state your answer with its unit (V, A or turns).",
        ],
        "example": {
            "question": "A transformer has Np = 100 turns, Ns = 400 turns, Vp = 6 V. Find Vs.",
            "steps": [
                {"label": "Turns ratio", "content": "Ns/Np = 400 / 100 = 4"},
                {"label": "Substitute", "content": "Vs = Vp × ratio = 6 × 4 = 24"},
                {"label": "Check", "content": "Vs × Np = 24 × 100 = 2400 = Vp × Ns = 6 × 400"},
                {"label": "Answer", "content": "Vs = <strong>24 V</strong>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: rearrange, or balance the power",
        "steps": [
            "Rearrange before substituting: \\(N_s = N_p \\times (V_s / V_p)\\), or \\(I_p = (V_s I_s) / V_p\\).",
            "For currents use power balance <strong>\\(V_p I_p = V_s I_s\\)</strong>: voltage up means current down by the same factor.",
            "Power lost in cables is \\(P = I^2 R\\); square the current first.",
        ],
        "example": {
            "question": "A transformer steps 230 V down to 23 V. The secondary current is 4 A. For an ideal transformer, find Ip.",
            "steps": [
                {"label": "Power out", "content": "Vs × Is = 23 × 4 = 92 W"},
                {"label": "Rearrange", "content": "Ip = power / Vp = 92 / 230 = 0.4"},
                {"label": "Check", "content": "Vp × Ip = 230 × 0.4 = 92 W, matching the power out"},
                {"label": "Answer", "content": "Ip = <strong>0.4 A</strong>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chain two equations",
        "steps": [
            "Grid problems take two steps: find the new current from power balance, then the loss from \\(P = I^2 R\\).",
            "Stepping voltage up lowers the transmission current, and \\(P = I^2 R\\) means a smaller current wastes far less energy.",
            "Work in order, keep each result, and state every answer with its unit.",
        ],
        "example": {
            "question": "A station gives 10 000 V at 500 A, stepped up to 50 000 V. Cables have R = 4 Ω. Find the transmission current and the power lost.",
            "steps": [
                {"label": "Power", "content": "Vp × Ip = 10 000 × 500 = 5 000 000 W"},
                {"label": "New current", "content": "Is = 5 000 000 / 50 000 = 100 A"},
                {"label": "Power lost", "content": "P = I²R = 100² × 4 = 40 000 W"},
                {"label": "Answer", "content": "Is = <strong>100 A</strong>, P = <strong>40 000 W</strong>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ------------------------------------------------------------------ guided (opener + teach)
OPENER_SVG = (
    '<svg viewBox="0 0 300 130" role="img" aria-label="Two transformer coils sharing a core: input 10 turns at 20 volts, output 5 turns" '
    'style="max-width:280px;margin:0.6em auto;display:block;">'
    '<rect x="140" y="30" width="20" height="72" fill="#94a3b8" fill-opacity="0.3" stroke="currentColor"/>'
    '<circle cx="122" cy="42" r="7" fill="none" stroke="currentColor"/>'
    '<circle cx="122" cy="60" r="7" fill="none" stroke="currentColor"/>'
    '<circle cx="122" cy="78" r="7" fill="none" stroke="currentColor"/>'
    '<circle cx="178" cy="52" r="7" fill="none" stroke="currentColor"/>'
    '<circle cx="178" cy="72" r="7" fill="none" stroke="currentColor"/>'
    '<text x="58" y="55" font-family="Inter,sans-serif" font-size="11" fill="currentColor">20 V in</text>'
    '<text x="52" y="112" font-family="Inter,sans-serif" font-size="11" fill="currentColor">10 turns</text>'
    '<text x="204" y="55" font-family="Inter,sans-serif" font-size="11" fill="currentColor">? V out</text>'
    '<text x="204" y="112" font-family="Inter,sans-serif" font-size="11" fill="currentColor">5 turns</text>'
    '</svg>'
)

pd["guided"] = {
    "opener": {
        "title": "Where does 5 V come from?",
        "display": OPENER_SVG + "<p>A phone charger turns 230 V mains into a few volts. No algebra needed to see how.</p>",
        "steps": [
            sayd("Every phone charger hides a <strong>transformer</strong>: two coils of wire on a shared iron core. The trick is the number of turns on each coil."),
            box("The input coil has 10 turns fed with 20 V. That is 20 ÷ 10 = 2 volts per turn. The output coil has 5 turns, so at 2 volts per turn it puts out ",
                10, "5 turns at 2 volts each.", post=" V"),
            sayd("You just used the transformer rule: <strong>volts per turn is the same on both coils</strong>, so voltage splits in the same ratio as the turns."),
            box("So a 20-turn output coil, still at 2 volts per turn, would give ",
                40, "20 turns at 2 volts each.", post=" V"),
            sayd("More turns on the output steps the voltage <strong>up</strong>; fewer turns steps it <strong>down</strong>. Written as an equation that is \\(V_s = V_p \\times (N_s / N_p)\\). Check whether your board gives it to you."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "Solve this one first: a transformer has 50 turns on the primary and 150 turns on the secondary, with a primary voltage of 24 V. Find the secondary voltage.",
            "steps": [
                sayd(EQ_TURNS),
                box("First the turns ratio Ns/Np = 150 / 50 = ", 3, "Secondary turns over primary turns."),
                box("Vs = Vp × ratio = 24 × 3 = ", 72, "Multiply the primary voltage by the ratio.", post=" V", phase="substitute",
                    say="Three times the turns, so three times the voltage."),
                box("Check by cross-multiplying: Vp × Ns = 24 × 150 = ", 3600, "This should equal Vs × Np."),
                box("and Vs × Np = 72 × 50 = ", 3600, "Compare it with the line above.",
                    done="Both give 3600, so Vs = 72 V is right. That was the whole method."),
            ],
        },
        "silver": {
            "display": "Now a current: a transformer steps 20 V up to 240 V with a primary current of 6 A. For an ideal transformer, find the secondary current.",
            "steps": [
                sayd(EQ_POWER + " Rearrange for Is: \\(I_s = (V_p I_p) / V_s\\)."),
                box("Power the primary delivers: Vp × Ip = 20 × 6 = ", 120, "Multiply primary voltage by primary current.", post=" W"),
                box("Is = power / Vs = 120 / 240 = ", 0.5, "Divide the power by the secondary voltage.", post=" A", phase="substitute",
                    say="The secondary carries the same 120 W at a higher voltage."),
                box("Sense-check the factor: voltage rose from 20 V to 240 V, a factor 240 / 20 = ", 12,
                    "How many times bigger the voltage got.",
                    say="So the current must fall by the same factor: 6 A ÷ 12 = 0.5 A."),
                box("Check power out: Vs × Is = 240 × 0.5 = ", 120, "This should match the power in.", post=" W",
                    done="120 W in equals 120 W out, so Is = 0.5 A. Voltage up 12 times, current down 12 times."),
            ],
        },
        "gold": {
            "display": "A power station produces 20 000 V at 1000 A. A step-up transformer raises it to 100 000 V for transmission, and the cables have a resistance of 5 Ω. For an ideal transformer, find the transmission current and the power lost in the cables.",
            "steps": [
                sayd("Two steps: first the power balance for the new current, then \\(P = I^2 R\\) for the loss."),
                box("Power generated: Vp × Ip = 20 000 × 1000 = ", 20000000, "Multiply primary voltage by primary current.", post=" W"),
                box("Transmission current Is = power / Vs = 20 000 000 / 100 000 = ", 200, "Divide the power by the transmission voltage.", post=" A",
                    say="Stepping voltage up 5 times dropped the current 5 times, from 1000 A to 200 A."),
                box("Square the current: 200² = ", 40000, "Two hundred times two hundred.", phase="substitute"),
                box("Power lost P = I²R = 40 000 × 5 = ", 200000, "Multiply the squared current by the resistance.", post=" W",
                    say="So 200 000 W is lost. The answers are Is = 200 A and P = 200 000 W."),
                box("See why they step it up: at the original 1000 A, the loss would be 1000² × 5 = ", 5000000,
                    "Square 1000, then multiply by 5.", post=" W",
                    done="5 000 000 W lost without stepping up, versus 200 000 W with it. That is why the grid steps voltage up."),
            ],
        },
    },
}

# ------------------------------------------------------------------ string-level fixes (svg xmlns/role, em dashes)
s = json.dumps(pd, ensure_ascii=False, indent=1)
# every existing bank SVG carries xmlns + no role/aria: swap the xmlns token for a11y attrs
s = s.replace(' xmlns=\\"http://www.w3.org/2000/svg\\"',
              ' role=\\"img\\" aria-label=\\"Transformer and transmission-line schematic\\"')
# em dashes anywhere student-facing -> comma / hyphen
s = s.replace(" — ", ", ").replace("—", "-")

pd = json.loads(s)
json.dump(pd, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT)
# quick scans
assert "—" not in json.dumps(pd, ensure_ascii=False), "em dash remains"
assert "http://" not in json.dumps(pd, ensure_ascii=False), "http remains"
print("no em dash, no http. OK")
