# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_831aee1062.json", encoding="utf-8"))
pb = live["problem_bank"]

def fmt(x):
    if isinstance(x, float) and x == int(x):
        x = int(x)
    return str(x)

def svg(q, label):
    assert q.count("<svg") == 1, "expected one svg"
    # Inline SVG in HTML needs no xmlns; the http:// namespace trips the
    # validator's external-resources check. Strip it. Also clear any em dash
    # (e.g. inside SVG comments) and add role/aria for accessibility.
    q = q.replace(' xmlns="http://www.w3.org/2000/svg"', "")
    q = q.replace("—", "-").replace("&mdash;", ":")
    return q.replace("<svg ", '<svg role="img" aria-label="%s" ' % label, 1)

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(s):
    return {"say": s}

# ---------- Walk builders (every box value asserted vs solution) ----------
def walk_p_from_FA(F, A, p):
    assert abs(F / A - p) < 1e-6
    return [
        sayonly("Pressure is a force spread over an area: \\(p = F \\div A\\)."),
        box("The area the force presses on is A = ", A, "Read it straight from the question.", post="m²"),
        box("Now divide the force by the area: %s ÷ %s = " % (fmt(F), fmt(A)), p,
            "Dividing by a number below 1 makes the answer bigger, not smaller.", post="Pa", phase="substitute"),
        box("Check by reversing: %s × %s = " % (fmt(p), fmt(A)), F,
            "Multiply your pressure back by the area.", post="N", phase="substitute",
            done="That is the force we started with, so p = %s Pa." % fmt(p)),
    ]

def walk_F_from_pA(p, A, F):
    assert abs(p * A - F) < 1e-6
    return [
        sayonly("Force is pressure times the area it acts on: \\(F = p \\times A\\)."),
        box("The pressure is p = ", p, "Read it from the question.", post="Pa"),
        box("Multiply pressure by area: %s × %s = " % (fmt(p), fmt(A)), F,
            "Just multiply the two numbers.", post="N", phase="substitute"),
        box("Check by reversing: %s ÷ %s = " % (fmt(F), fmt(A)), p,
            "Divide your force back by the area.", post="Pa", phase="substitute",
            done="That is the pressure we started with, so F = %s N." % fmt(F)),
    ]

def walk_p_from_hrg(h, rho, p):
    assert abs(h * rho * 10 - p) < 1e-6
    return [
        sayonly("Pressure from a fluid column is \\(p = h\\rho g\\), with g = 10 N/kg."),
        box("The depth of fluid is h = ", h, "Read the depth from the question.", post="m"),
        box("Multiply depth × density × g: %s × %s × 10 = " % (fmt(h), fmt(rho)), p,
            "Do it in any order, the answer is the same.", post="Pa", phase="substitute"),
        box("Check: divide back by ρg. %s ÷ %s = " % (fmt(p), fmt(rho * 10)), h,
            "Divide your pressure by density times g.", post="m", phase="substitute",
            done="Back to the depth we started with, so p = %s Pa." % fmt(p)),
    ]

def walk_h_from_p(p, rho, h):
    assert abs(p / (rho * 10) - h) < 1e-6
    return [
        sayonly("Rearrange \\(p = h\\rho g\\) to make h the subject: \\(h = p \\div (\\rho g)\\), g = 10 N/kg."),
        box("First work out ρg: %s × 10 = " % fmt(rho), rho * 10, "Multiply the density by 10."),
        box("Now divide the pressure by that: %s ÷ %s = " % (fmt(p), fmt(rho * 10)), h,
            "Divide the pressure by density times g.", post="m", phase="substitute"),
        box("Check: %s × %s × 10 = " % (fmt(h), fmt(rho)), p,
            "Put your depth back into p = hρg.", post="Pa", phase="substitute",
            done="Back to the pressure we started with, so h = %s m." % fmt(h)),
    ]

def walk_A_from_Fp(F, p, A):
    assert abs(F / p - A) < 1e-6
    return [
        sayonly("Rearrange \\(p = F \\div A\\) to make A the subject: \\(A = F \\div p\\)."),
        box("The force is F = ", F, "Read it from the question.", post="N"),
        box("Divide the force by the pressure: %s ÷ %s = " % (fmt(F), fmt(p)), A,
            "Divide the force by the pressure.", post="m²", phase="substitute"),
        box("Check: %s × %s = " % (fmt(p), fmt(A)), F,
            "Multiply pressure by your area.", post="N", phase="substitute",
            done="That is the force we started with, so A = %s m²." % fmt(A)),
    ]

def walk_delta_p():
    assert abs((0.8 - 0.5) * 1000 * 10 - 3000) < 1e-6
    return [
        sayonly("Pressure difference uses the difference in depth: \\(\\Delta p = \\Delta h \\times \\rho \\times g\\), g = 10 N/kg."),
        box("First the depth difference: 0.8 − 0.5 = ", 0.3, "Subtract the top depth from the bottom depth.", post="m"),
        box("Now Δh × ρ × g: 0.3 × 1000 × 10 = ", 3000, "Multiply the 0.3 m gap by density and g.", post="Pa", phase="substitute"),
        box("Check: 3000 ÷ (1000 × 10) = ", 0.3, "Divide back by ρg to get the depth gap.", post="m", phase="substitute",
            done="Back to the 0.3 m gap, so Δp = 3000 Pa."),
    ]

def walk_submarine():
    assert 120 * 1025 * 10 == 1230000 and 1230000 * 500 == 615000000
    return [
        sayonly("Two steps. First the water pressure with \\(p = h\\rho g\\) (g = 10), then the force with \\(F = p \\times A\\)."),
        box("Depth of water above the hull, h = ", 120, "Read the depth from the question.", post="m"),
        box("Pressure: 120 × 1025 × 10 = ", 1230000, "Multiply depth, density and g.", post="Pa"),
        box("Now the force: p × A = 1230000 × 500 = ", 615000000, "Multiply your pressure by the hull area.", post="N", phase="substitute"),
        box("Check: 615000000 ÷ 500 = ", 1230000, "Divide the force back by the area.", post="Pa", phase="substitute",
            done="Back to the pressure, so F = 615 000 000 N (6.15 × 10⁸ N)."),
    ]

def walk_gas():
    assert abs(0.5 * 1.2 * 10 - 6) < 1e-9
    return [
        sayonly("Use \\(p = h\\rho g\\), g = 10. The gas density is tiny, so expect a tiny pressure."),
        box("Height of the gas column, h = ", 0.5, "Read the height from the question.", post="m"),
        box("Pressure: 0.5 × 1.2 × 10 = ", 6, "Multiply height, density and g.", post="Pa", phase="substitute"),
        box("Check: 6 ÷ (1.2 × 10) = ", 0.5, "Divide back by density times g.", post="m", phase="substitute",
            done="Back to the 0.5 m height, so p = 6 Pa."),
    ]

def walk_upthrust():
    assert 1000 * 0.18 * 10 == 1800
    return [
        sayonly("Upthrust equals the weight of fluid pushed aside: \\(\\text{upthrust} = \\rho V g\\), g = 10."),
        box("Submerged volume, V = ", 0.18, "Read the submerged volume from the question.", post="m³"),
        box("Upthrust: 1000 × 0.18 × 10 = ", 1800, "Multiply density, volume and g.", post="N", phase="substitute"),
        box("The block weighs 1800 N. Write that weight to compare: ", 1800, "Type the block's weight from the question.", post="N", phase="substitute",
            done="Upthrust = weight = 1800 N, so the block floats. Upthrust = 1800 N."),
    ]

def walk_depth():
    assert abs(3500 / (1000 * 10) - 0.35) < 1e-9
    return [
        sayonly("Rearrange \\(p = h\\rho g\\) to \\(h = p \\div (\\rho g)\\), g = 10."),
        box("First work out ρg: 1000 × 10 = ", 10000, "Multiply density by 10."),
        box("Now divide: 3500 ÷ 10000 = ", 0.35, "Divide the gauge pressure by ρg.", post="m", phase="substitute"),
        box("Check: 0.35 × 1000 × 10 = ", 3500, "Put your depth back into p = hρg.", post="Pa", phase="substitute",
            done="Back to the 3500 Pa reading, so h = 0.35 m."),
    ]

# ---------- Bronze ----------
B = pb["bronze"]
bronze = [
    {"unit": "Pa", "display": B[0]["display"],
     "question": svg(B[0]["question"], "Block pushing down with force 600 N on an area of 0.2 m squared"),
     "solutions": [3000], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(p = F \\div A\\)",
     "hint": "Pressure is force divided by area: 600 divided by 0.2.",
     "misconceptions": [{"check": "common", "pattern": "inverse_error", "expect": 120,
        "message": "Divide, do not multiply: p = F ÷ A = 600 ÷ 0.2 = 3000 Pa. Multiplying gives 120, far too small."}],
     "guided_steps": walk_p_from_FA(600, 0.2, 3000)},
    {"unit": "N", "display": B[1]["display"],
     "question": svg(B[1]["question"], "Hydraulic piston, pressure 5000 Pa acting on area 2 m squared, force unknown"),
     "solutions": [10000], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(F = p \\times A\\)",
     "hint": "Rearrange to F = p times A, then multiply.",
     "misconceptions": [{"check": "common", "pattern": "inverse_error", "expect": 2500,
        "message": "Multiply, do not divide: F = p × A = 5000 × 2 = 10 000 N. Dividing gives 2500, which is wrong."}],
     "guided_steps": walk_F_from_pA(5000, 2, 10000)},
    {"unit": "Pa", "display": B[2]["display"],
     "question": svg(B[2]["question"], "Water column 5 m deep, density 1000 kg per m cubed"),
     "solutions": [50000], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(p = h\\rho g\\)",
     "hint": "Multiply depth, density and g: 5 times 1000 times 10.",
     "misconceptions": [{"check": "common", "pattern": "forgot_step", "expect": 5000,
        "message": "Do not forget the g. p = hρg = 5 × 1000 × 10 = 50 000 Pa. Leaving out the ×10 gives 5000."}],
     "guided_steps": walk_p_from_hrg(5, 1000, 50000)},
    {"unit": "Pa", "display": B[3]["display"],
     "question": svg(B[3]["question"], "Block pushing down with force 200 N on an area of 0.04 m squared"),
     "solutions": [5000], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(p = F \\div A\\)",
     "hint": "Divide the force by the area: 200 divided by 0.04.",
     "misconceptions": [{"check": "common", "pattern": "inverse_error", "expect": 8,
        "message": "p = F ÷ A = 200 ÷ 0.04 = 5000 Pa. Multiplying instead gives 8, far too small."}],
     "guided_steps": walk_p_from_FA(200, 0.04, 5000)},
    {"unit": "Pa", "display": B[4]["display"],
     "question": svg(B[4]["question"], "Liquid column 3 m deep, density 800 kg per m cubed"),
     "solutions": [24000], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(p = h\\rho g\\)",
     "hint": "Multiply depth, density and g: 3 times 800 times 10.",
     "misconceptions": [{"check": "common", "pattern": "forgot_step", "expect": 2400,
        "message": "Do not forget the g. p = hρg = 3 × 800 × 10 = 24 000 Pa. Leaving out the ×10 gives 2400."}],
     "guided_steps": walk_p_from_hrg(3, 800, 24000)},
    # B[5] was 900/0.3 = 3000, a DUPLICATE of B[0]. Change force 900 -> 1200 -> 4000 Pa.
    {"unit": "Pa", "display": B[5]["display"].replace("900", "1200"),
     "question": svg(B[5]["question"].replace("900", "1200"), "Block exerting force 1200 N on a floor area of 0.3 m squared"),
     "solutions": [4000], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(p = F \\div A\\)",
     "hint": "Divide the force by the floor area: 1200 divided by 0.3.",
     "misconceptions": [{"check": "common", "pattern": "inverse_error", "expect": 360,
        "message": "p = F ÷ A = 1200 ÷ 0.3 = 4000 Pa. Multiplying instead gives 360, which is wrong."}],
     "guided_steps": walk_p_from_FA(1200, 0.3, 4000)},
]

# ---------- Silver ----------
S = pb["silver"]
silver = [
    {"unit": "Pa", "display": S[0]["display"],
     "question": svg(S[0]["question"], "Diver 40 m deep in fresh water, density 1000 kg per m cubed"),
     "solutions": [400000], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(p = h\\rho g\\)",
     "hint": "Use p = h times rho times g with h = 40 and g = 10.",
     "misconceptions": [{"check": "common", "pattern": "forgot_step", "expect": 40000,
        "message": "Do not forget the g. p = 40 × 1000 × 10 = 400 000 Pa. Leaving out the ×10 gives 40 000."}],
     "guided_steps": walk_p_from_hrg(40, 1000, 400000)},
    {"unit": "N", "display": S[1]["display"],
     "question": svg(S[1]["question"], "Hydraulic press, pressure 200000 Pa on a piston of area 0.05 m squared"),
     "solutions": [10000], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(F = p \\times A\\)",
     "hint": "Force = pressure times area, so multiply.",
     "misconceptions": [{"check": "common", "pattern": "inverse_error", "expect": 4000000,
        "message": "Multiply, do not divide: F = p × A = 200 000 × 0.05 = 10 000 N. Dividing gives 4 000 000."}],
     "guided_steps": walk_F_from_pA(200000, 0.05, 10000)},
    {"unit": "m", "display": S[2]["display"],
     "question": svg(S[2]["question"], "Seawater column, pressure 102500 Pa at the base, depth unknown"),
     "solutions": [10], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(h = p \\div (\\rho g)\\)",
     "hint": "Rearrange to h = p divided by rho g; work out rho g first.",
     "misconceptions": [{"check": "common", "pattern": "forgot_step", "expect": 100,
        "message": "Divide by ρg, not just ρ. h = 102 500 ÷ (1025 × 10) = 102 500 ÷ 10 250 = 10 m. Dividing by 1025 alone gives 100."}],
     "guided_steps": walk_h_from_p(102500, 1025, 10)},
    {"unit": "m²", "display": S[3]["display"],
     "question": svg(S[3]["question"], "Force 1200 N producing pressure 6000 Pa, area unknown"),
     "solutions": [0.2], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(A = F \\div p\\)",
     "hint": "Rearrange to A = F divided by p, then divide.",
     "misconceptions": [{"check": "common", "pattern": "inverse_error", "expect": 5,
        "message": "A = F ÷ p = 1200 ÷ 6000 = 0.2 m². Dividing the wrong way (6000 ÷ 1200) gives 5."}],
     "guided_steps": walk_A_from_Fp(1200, 6000, 0.2)},
    {"unit": "Pa", "display": S[4]["display"],
     "question": svg(S[4]["question"], "Submerged object with top face at 0.5 m and bottom face at 0.8 m depth"),
     "solutions": [3000], "calculator": True, "input_type": "single_value",
     "equation_hint": "\\(\\Delta p = \\Delta h \\times \\rho \\times g\\)",
     "hint": "Find the depth difference first, then use delta-p = delta-h times rho times g.",
     "misconceptions": [{"check": "common", "pattern": "forgot_step", "expect": 8000,
        "message": "Use the depth difference, not the full depth. Δh = 0.8 − 0.5 = 0.3 m, so Δp = 0.3 × 1000 × 10 = 3000 Pa. Using 0.8 m gives 8000."}],
     "guided_steps": walk_delta_p()},
]

# ---------- Gold ----------
G = pb["gold"]
gold = [
    {"unit": "N", "display": G[0]["display"],
     "question": svg(G[0]["question"], "Submarine 120 m below seawater surface, hull area 500 m squared"),
     "solutions": [615000000], "calculator": True, "input_type": "single_value",
     "hint": "Two steps: pressure with p = h rho g, then force with F = p times A.",
     "misconceptions": [{"check": "common", "pattern": "forgot_step", "expect": 1230000,
        "message": "That is only the pressure. p = 120 × 1025 × 10 = 1 230 000 Pa, then F = p × A = 1 230 000 × 500 = 615 000 000 N."}],
     "guided_steps": walk_submarine()},
    {"unit": "Pa", "display": G[1]["display"],
     "question": svg(G[1]["question"], "Gas column 0.5 m tall, density 1.2 kg per m cubed"),
     "solutions": [6], "calculator": True, "input_type": "single_value",
     "hint": "Use p = h rho g; the density is small so the pressure is small.",
     "misconceptions": [{"check": "common", "pattern": "forgot_step", "expect": 0.6,
        "message": "Do not forget the g. p = hρg = 0.5 × 1.2 × 10 = 6 Pa. Leaving out the ×10 gives 0.6."}],
     "guided_steps": walk_gas()},
    {"unit": "N", "display": G[2]["display"],
     "question": svg(G[2]["question"], "Block floating in water, weight 1800 N, submerged volume 0.18 m cubed, upthrust unknown"),
     "solutions": [1800], "calculator": True, "input_type": "single_value",
     "hint": "Upthrust = weight of water displaced = rho times V times g.",
     "misconceptions": [{"check": "common", "pattern": "forgot_step", "expect": 180,
        "message": "Do not forget the g. Upthrust = ρVg = 1000 × 0.18 × 10 = 1800 N. Leaving out the ×10 gives 180."}],
     "guided_steps": walk_upthrust()},
    {"unit": "m", "display": G[3]["display"],
     "question": svg(G[3]["question"], "Fish tank, pressure gauge reads 3500 Pa at the bottom, depth unknown"),
     "solutions": [0.35], "calculator": True, "input_type": "single_value",
     "hint": "Rearrange p = h rho g to h = p divided by rho g.",
     "misconceptions": [{"check": "common", "pattern": "forgot_step", "expect": 3.5,
        "message": "Divide by ρg, not just ρ. h = 3500 ÷ (1000 × 10) = 3500 ÷ 10 000 = 0.35 m. Dividing by 1000 alone gives 3.5."}],
     "guided_steps": walk_depth()},
]

# ---------- worked_examples: strip em dashes from step labels ----------
we = json.loads(json.dumps(live["worked_examples"]))
for ex in we:
    for st in ex["steps"]:
        st["label"] = st["label"].replace(" — ", ": ")

# ---------- guided.opener ----------
opener = {
    "label": "Before any equation",
    "display": "Two people weigh the same, 600 N.<br>One stands on wide skis (area 2 m²). The other balances on a single stiletto heel (area 0.001 m²).<br>The 'squash' on the snow is the weight shared over the area it touches.",
    "steps": [
        {"say": "Skis first. Share the 600 N over 2 m² of snow.",
         "pre": "600 ÷ 2 = ", "post": "per m²", "answer": 300, "hint": "Just divide 600 by 2."},
        {"say": "Now the heel: the same 600 N over only 0.001 m².",
         "pre": "600 ÷ 0.001 = ", "post": "per m²", "answer": 600000,
         "hint": "Dividing by 0.001 is the same as multiplying by 1000.",
         "done": "The heel presses 600 000 into the snow, 2000 times more than the ski, from the SAME weight. That is why heels sink and skis do not."},
        {"say": "That 'weight shared over area' is <strong>pressure</strong>. You just used \\(p = F \\div A\\): same force, smaller area, much higher pressure. Squeeze that force into a column of fluid instead and you get \\(p = h\\rho g\\)."},
    ],
}

# ---------- guided.teach ----------
teach = {
    "bronze": {"label": "Together: your first one",
        "display": "A force of 800 N presses on an area of 0.4 m². Find the pressure in Pa.",
        "steps": [
            sayonly("Force and area, so use \\(p = F \\div A\\)."),
            box("The force is F = ", 800, "Read it from the question.", post="N"),
            box("The area is A = ", 0.4, "Read it from the question.", post="m²"),
            box("Divide: 800 ÷ 0.4 = ", 2000, "Dividing by 0.4 is multiplying by 2.5.", post="Pa"),
            box("Check: 2000 × 0.4 = ", 800, "Multiply your pressure back by the area.", post="N",
                done="Back to 800 N, so p = 2000 Pa."),
        ]},
    "silver": {"label": "Together: rearrange first",
        "display": "A column of oil (density 900 kg/m³) gives a pressure of 45 000 Pa at its base. Find the depth. (g = 10 N/kg)",
        "steps": [
            sayonly("The unknown is the depth, so rearrange \\(p = h\\rho g\\) to \\(h = p \\div (\\rho g)\\)."),
            box("The pressure is p = ", 45000, "Read it from the question.", post="Pa"),
            box("Work out ρg: 900 × 10 = ", 9000, "Multiply density by 10."),
            box("Divide: 45000 ÷ 9000 = ", 5, "Divide the pressure by ρg.", post="m"),
            box("Check: 5 × 900 × 10 = ", 45000, "Put your depth back into p = hρg.", post="Pa",
                done="Back to 45 000 Pa, so h = 5 m."),
        ]},
    "gold": {"label": "Together: chain two steps",
        "display": "A tank holds water 8 m deep (ρ = 1000 kg/m³, g = 10). A hatch in the base has area 2 m². Find the force on the hatch.",
        "steps": [
            sayonly("Two steps: pressure with \\(p = h\\rho g\\), then force with \\(F = p \\times A\\)."),
            box("Depth of water, h = ", 8, "Read the depth from the question.", post="m"),
            box("Pressure: 8 × 1000 × 10 = ", 80000, "Multiply depth, density and g.", post="Pa"),
            box("Force: 80000 × 2 = ", 160000, "Multiply your pressure by the hatch area.", post="N"),
            box("Check: 160000 ÷ 2 = ", 80000, "Divide the force back by the area.", post="Pa",
                done="Back to the 80 000 Pa pressure, so F = 160 000 N."),
        ]},
}

# ---------- tier_guides ----------
tier_guides = {
    "bronze": {"title": "Bronze: one equation, values ready to use",
        "steps": [
            "Pick the equation. Force on an area? Use \\(p = F \\div A\\). Depth in a fluid? Use \\(p = h\\rho g\\) with g = 10 N/kg.",
            "Every value is already in base units (m, kg/m³, m², N), so substitute straight in.",
            "Work out the arithmetic and write the unit: pascals (Pa) for pressure, newtons (N) for force.",
        ],
        "example": {"question": "A force of 750 N acts on an area of 0.5 m². Find the pressure.",
            "steps": [
                {"label": "Equation", "content": "<p>\\(p = F \\div A\\)</p>"},
                {"label": "Substitute", "content": "<p>\\(p = 750 \\div 0.5\\)</p>"},
                {"label": "Check", "content": "<p>\\(1500 \\times 0.5 = 750\\) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>1500 Pa</strong></p>", "isAnswer": True, "is_answer": True},
            ]}},
    "silver": {"title": "Silver: rearrange before you substitute",
        "steps": [
            "The unknown may not be on its own. Rearrange first: \\(F = p \\times A\\), \\(A = F \\div p\\), or \\(h = p \\div (\\rho g)\\).",
            "For depth, work out \\(\\rho g\\) as one number first, then divide the pressure by it.",
            "Substitute, calculate, and give the unit: N, m² or m depending on what you found.",
        ],
        "example": {"question": "A pressure of 30 000 Pa acts on a piston of area 0.02 m². Find the force.",
            "steps": [
                {"label": "Rearrange", "content": "<p>\\(F = p \\times A\\)</p>"},
                {"label": "Substitute", "content": "<p>\\(F = 30000 \\times 0.02\\)</p>"},
                {"label": "Check", "content": "<p>\\(600 \\div 0.02 = 30000\\) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>600 N</strong></p>", "isAnswer": True, "is_answer": True},
            ]}},
    "gold": {"title": "Gold: chain two steps together",
        "steps": [
            "Gold problems need two calculations. Usually find the pressure first with \\(p = h\\rho g\\).",
            "Then feed that pressure into \\(F = p \\times A\\) for the force, or compare an upthrust \\(\\rho V g\\) with a weight to test floating.",
            "Write the first answer down, then use it. Give each answer its unit.",
        ],
        "example": {"question": "Water 5 m deep (ρ = 1000, g = 10) sits above a hatch of area 3 m². Find the force on the hatch.",
            "steps": [
                {"label": "Pressure", "content": "<p>\\(p = h\\rho g = 5 \\times 1000 \\times 10 = 50000\\) Pa</p>"},
                {"label": "Force", "content": "<p>\\(F = p \\times A = 50000 \\times 3\\)</p>"},
                {"label": "Check", "content": "<p>\\(150000 \\div 3 = 50000\\) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>150 000 N</strong></p>", "isAnswer": True, "is_answer": True},
            ]}},
}

# ---------- method_card (slim, no em dash, <=140 words, <=4 steps) ----------
method_card = {
    "title": "Pressure in Fluids",
    "steps": [
        "Choose the equation: p = F ÷ A for a force on an area, p = hρg for depth in a fluid.",
        "Check units are base: area in m², depth in m, density in kg/m³. Use g = 10 N/kg.",
        "Rearrange if the unknown is F, A or h, then substitute.",
        "Calculate and state the unit: Pa, N, m² or m.",
    ],
    "content": "<p>Two equations cover pressure in fluids. Use <strong>p = F ÷ A</strong> when a force is spread over an area (pascals, Pa = N/m²), and <strong>p = hρg</strong> for the pressure caused by a fluid column of depth h.</p><p>Take g = 10 N/kg. Density ρ is in kg/m³ (water ≈ 1000, seawater ≈ 1025), depth h in metres, area A in m².</p><p>Rearrange when needed: F = p × A, A = F ÷ p, or h = p ÷ (ρg). An object floats when the upthrust (ρVg, the weight of fluid pushed aside) equals its own weight.</p>",
}

exam_context = {
    "marks": "3–5 per calculation",
    "paper": "Paper 2 (Physics)",
    "frequency": "Common in higher-tier physics papers; pressure and floating appear regularly.",
}

out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "exam_context": exam_context,
    "problem_bank": {
        "bronze": bronze, "silver": silver, "gold": gold,
        "bronze_description": "One equation, values already in base units: substitute straight in.",
        "silver_description": "Rearrange the equation, or work out ρg first, before substituting.",
        "gold_description": "Two steps chained: find the pressure, then the force or test for floating.",
    },
    "related_videos": live["related_videos"],
    "worked_examples": we,
    "tier_guides": tier_guides,
    "guided": {"opener": opener, "teach": teach},
}

json.dump(out, io.open("lesson_831aee1062.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# quick em-dash self-scan (excluding note fields, none used here)
blob = json.dumps(out, ensure_ascii=False)
print("built lesson_831aee1062.json  em-dash present:", "—" in blob)
