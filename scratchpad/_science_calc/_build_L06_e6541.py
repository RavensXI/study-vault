# -*- coding: utf-8 -*-
"""Build guided practice_data for higher-calculations-L06@e6541c99e0
Transformers, Power Transmission (Separate Sciences Higher).
Full conversion: figures rebuilt (theme-safe, role/aria), bank verified,
guided walks + tier_guides + opener added. Board-neutral phrasing."""
import json, io

# ---------- SVG builders (theme-safe: all <text> currentColor) ----------
SVG_OPEN = ('<svg viewBox="0 0 440 190" role="img" aria-label="{aria}" '
            'style="max-width:340px;margin:0.6em auto;display:block;">')

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

def transformer(left, right, cap, aria):
    """left/right: list of up to 3 label strings. Theme-safe schematic."""
    p = [SVG_OPEN.format(aria=esc(aria))]
    # iron core limbs
    p.append('<rect x="195" y="52" width="20" height="96" fill="currentColor" fill-opacity="0.22"/>')
    p.append('<rect x="225" y="52" width="20" height="96" fill="currentColor" fill-opacity="0.22"/>')
    p.append('<rect x="195" y="52" width="50" height="14" fill="currentColor" fill-opacity="0.22"/>')
    p.append('<rect x="195" y="134" width="50" height="14" fill="currentColor" fill-opacity="0.22"/>')
    # primary coils (left limb) red, secondary (right limb) blue
    for cy in (78, 100, 122):
        p.append('<circle cx="205" cy="%d" r="11" fill="none" stroke="#dc2626" stroke-width="2.5"/>' % cy)
    for cy in (74, 92, 110, 128):
        p.append('<circle cx="235" cy="%d" r="10" fill="none" stroke="#2563eb" stroke-width="2.5"/>' % cy)
    # labels
    ys = [88, 106, 124]
    for i, s in enumerate(left):
        p.append('<text x="98" y="%d" text-anchor="middle" font-family="Inter,sans-serif" '
                 'font-size="12" font-weight="600" fill="currentColor">%s</text>' % (ys[i], esc(s)))
    for i, s in enumerate(right):
        p.append('<text x="342" y="%d" text-anchor="middle" font-family="Inter,sans-serif" '
                 'font-size="12" font-weight="600" fill="currentColor">%s</text>' % (ys[i], esc(s)))
    p.append('<text x="220" y="176" text-anchor="middle" font-family="Inter,sans-serif" '
             'font-size="11" font-style="italic" fill="currentColor" fill-opacity="0.75">%s</text>' % esc(cap))
    p.append('</svg>')
    return ''.join(p)

def cable(I, R, aria):
    p = ['<svg viewBox="0 0 400 130" role="img" aria-label="%s" '
         'style="max-width:320px;margin:0.6em auto;display:block;">' % esc(aria)]
    p.append('<line x1="40" y1="58" x2="150" y2="58" stroke="currentColor" stroke-width="2"/>')
    p.append('<line x1="250" y1="58" x2="360" y2="58" stroke="currentColor" stroke-width="2"/>')
    p.append('<polygon points="82,51 100,58 82,65" fill="#dc2626"/>')
    p.append('<text x="96" y="42" text-anchor="middle" font-family="Inter,sans-serif" '
             'font-size="12" font-weight="600" fill="currentColor">I = %s A</text>' % esc(str(I)))
    p.append('<rect x="150" y="45" width="100" height="26" fill="currentColor" fill-opacity="0.14" '
             'stroke="currentColor" stroke-width="1.5"/>')
    p.append('<text x="200" y="62" text-anchor="middle" font-family="Inter,sans-serif" '
             'font-size="11" fill="currentColor">cable, R = %s Ω</text>' % esc(str(R)))
    p.append('<text x="200" y="102" text-anchor="middle" font-family="Inter,sans-serif" '
             'font-size="12" font-weight="600" fill="currentColor">P lost = ?</text>')
    p.append('</svg>')
    return ''.join(p)

def q(svg, text):
    """Compose the rendered question field: figure then problem text."""
    return svg + '<p style="margin-top:0.7em;">' + text + '</p>'

# ---------- problem bank ----------
def prob(display, svg, sols, unit, calc, mis, gs, accept=None, input_type='single_value',
         equation_hint=None, hint=None, options=None, skip=None, higher_only=False):
    o = {
        'display': display,
        'question': q(svg, display),
        'solutions': sols,
        'unit': unit,
        'calculator': calc,
        'input_type': input_type,
        'higher_only': higher_only,
        'misconceptions': mis,
    }
    if accept is not None:
        o['accept'] = accept
    if equation_hint:
        o['equation_hint'] = equation_hint
    if hint:
        o['hint'] = hint
    if options:
        o['options'] = options
    if skip:
        o['guided_skip_reason'] = skip
    if gs is not None:
        o['guided_steps'] = gs
    return o

EQ_TURNS = "\\(\\frac{V_p}{V_s} = \\frac{n_p}{n_s}\\)"
EQ_POWER = "\\(V_p I_p = V_s I_s\\)"

bronze = [
    prob(
        "A transformer has 500 primary turns and 50 secondary turns. The primary voltage is 230 V. Calculate the secondary voltage.",
        transformer(["Vp = 230 V", "Np = 500"], ["Vs = ?", "Ns = 50"], "Step-down: find Vs",
                    "Transformer, 230 V primary with 500 turns, 50 secondary turns, find secondary voltage"),
        [23.0], "V", True,
        [{"check": "common", "pattern": "inverse_ratio", "expect": 2300,
          "message": "Vs = Vp × (ns/np) = 230 × (50/500) = 230 × 0.1 = 23 V. Fewer secondary turns means a lower voltage."}],
        [
            {"say": "Turns and voltage share the same ratio: " + EQ_TURNS + ", so \\(V_s = V_p \\times \\frac{n_s}{n_p}\\)."},
            {"pre": "Turns ratio ns ÷ np = 50 ÷ 500 = ", "post": "", "answer": 0.1,
             "hint": "Divide the secondary turns by the primary turns."},
            {"pre": "Vs = Vp × 0.1 = 230 × 0.1 = ", "post": "", "answer": 23,
             "hint": "Multiply the primary voltage by the ratio.", "phase": "substitute"},
            {"pre": "Check: Vs ÷ Vp = 23 ÷ 230 = ", "post": "", "answer": 0.1,
             "hint": "Divide the two voltages.", "done": "That equals 50 ÷ 500 = 0.1, so Vs = 23 V is right.",
             "phase": "substitute"},
        ],
        accept=0.5, equation_hint=EQ_TURNS,
        hint="Multiply the primary voltage by the secondary turns, then divide by the primary turns."),
    prob(
        "A transformer has a primary voltage of 12 V and a secondary voltage of 240 V. The primary coil has 100 turns. Calculate the number of secondary turns.",
        transformer(["Vp = 12 V", "Np = 100"], ["Vs = 240 V", "Ns = ?"], "Step-up: find Ns",
                    "Transformer, 12 V primary with 100 turns stepped up to 240 V, find secondary turns"),
        [2000], "", True,
        [{"check": "common", "pattern": "wrong_rearrange", "expect": 5,
          "message": "ns = np × (Vs/Vp) = 100 × (240/12) = 100 × 20 = 2000 turns. Flipping the fraction gives just 5."}],
        [
            {"say": "Rearrange " + EQ_TURNS + " for the secondary turns: \\(n_s = n_p \\times \\frac{V_s}{V_p}\\)."},
            {"pre": "np × Vs = 100 × 240 = ", "post": "", "answer": 24000,
             "hint": "Multiply the primary turns by the secondary voltage."},
            {"pre": "Divide by Vp: 24000 ÷ 12 = ", "post": "", "answer": 2000,
             "hint": "Divide by the primary voltage.", "phase": "substitute"},
            {"pre": "Check: Vs = Vp × ns ÷ np = 12 × 2000 ÷ 100 = ", "post": "", "answer": 240,
             "hint": "Work it left to right.", "done": "It gives 240 V, the stated secondary voltage, so ns = 2000 turns.",
             "phase": "substitute"},
        ],
        equation_hint=EQ_TURNS,
        hint="Multiply the primary turns by the secondary voltage, then divide by the primary voltage."),
    prob(
        "A transformer has 1000 primary turns and 2000 secondary turns. The primary voltage is 230 V. Calculate the secondary voltage.",
        transformer(["Vp = 230 V", "Np = 1000"], ["Vs = ?", "Ns = 2000"], "Step-up: find Vs",
                    "Transformer, 230 V primary with 1000 turns, 2000 secondary turns, find secondary voltage"),
        [460], "V", True,
        [{"check": "common", "pattern": "inverse_ratio", "expect": 115,
          "message": "Vs = Vp × (ns/np) = 230 × (2000/1000) = 230 × 2 = 460 V. More secondary turns means a higher voltage."}],
        [
            {"say": "Use \\(V_s = V_p \\times \\frac{n_s}{n_p}\\)."},
            {"pre": "Turns ratio ns ÷ np = 2000 ÷ 1000 = ", "post": "", "answer": 2,
             "hint": "Divide the secondary turns by the primary turns."},
            {"pre": "Vs = 230 × 2 = ", "post": "", "answer": 460,
             "hint": "Multiply the primary voltage by the ratio.", "phase": "substitute"},
            {"pre": "Check: Vs ÷ Vp = 460 ÷ 230 = ", "post": "", "answer": 2,
             "hint": "Divide the two voltages.", "done": "That matches the turns ratio 2000 ÷ 1000 = 2, so Vs = 460 V.",
             "phase": "substitute"},
        ],
        equation_hint=EQ_TURNS,
        hint="Find the turns ratio, then multiply the primary voltage by it."),
    prob(
        "A transformer has 800 primary turns and 80 secondary turns. The primary voltage is 240 V. Calculate the secondary voltage.",
        transformer(["Vp = 240 V", "Np = 800"], ["Vs = ?", "Ns = 80"], "Step-down: find Vs",
                    "Transformer, 240 V primary with 800 turns, 80 secondary turns, find secondary voltage"),
        [24], "V", True,
        [{"check": "common", "pattern": "inverse_ratio", "expect": 2400,
          "message": "Vs = Vp × (ns/np) = 240 × (80/800) = 240 × 0.1 = 24 V. Flipping the ratio gives 2400 V, far too big."}],
        [
            {"say": "Use \\(V_s = V_p \\times \\frac{n_s}{n_p}\\)."},
            {"pre": "Turns ratio ns ÷ np = 80 ÷ 800 = ", "post": "", "answer": 0.1,
             "hint": "Divide the secondary turns by the primary turns."},
            {"pre": "Vs = 240 × 0.1 = ", "post": "", "answer": 24,
             "hint": "Multiply the primary voltage by the ratio.", "phase": "substitute"},
            {"pre": "Check: Vs ÷ Vp = 24 ÷ 240 = ", "post": "", "answer": 0.1,
             "hint": "Divide the two voltages.", "done": "That equals 80 ÷ 800 = 0.1, so Vs = 24 V is right.",
             "phase": "substitute"},
        ],
        equation_hint=EQ_TURNS,
        hint="Find the turns ratio, then multiply the primary voltage by it."),
    prob(
        "A transformer has 200 primary turns and 1000 secondary turns. Is this a step-up or a step-down transformer?",
        transformer(["Np = 200"], ["Ns = 1000"], "Step-up or step-down?",
                    "Transformer with 200 primary turns and 1000 secondary turns, decide step-up or step-down"),
        [0], "", False,
        [{"check": "common", "pattern": "confused", "expect": None,
          "message": "More secondary turns (1000) than primary (200) means the voltage is stepped UP. This is a step-up transformer."}],
        None, input_type='multiple_choice', options=["Step-up", "Step-down"],
        equation_hint="More secondary turns means step-up",
        skip="Conceptual step-up/step-down identification; no numeric solve to walk through."),
]

silver = [
    prob(
        "A step-up transformer at a power station has a primary voltage of 25 000 V and a secondary voltage of 400 000 V. The primary coil has 500 turns. Calculate the number of secondary turns.",
        transformer(["Vp = 25 000 V", "Np = 500"], ["Vs = 400 000 V", "Ns = ?"], "Step-up: find Ns",
                    "Power-station transformer stepping 25 000 V up to 400 000 V with 500 primary turns, find secondary turns"),
        [8000], "", True,
        [{"check": "common", "pattern": "wrong_rearrange", "expect": 31.25,
          "message": "ns = np × (Vs/Vp) = 500 × (400 000/25 000) = 500 × 16 = 8000 turns. Flipping the ratio gives about 31."}],
        [
            {"say": "Rearrange " + EQ_TURNS + " for the secondary turns: \\(n_s = n_p \\times \\frac{V_s}{V_p}\\)."},
            {"pre": "Voltage ratio Vs ÷ Vp = 400000 ÷ 25000 = ", "post": "", "answer": 16,
             "hint": "Divide the secondary voltage by the primary voltage."},
            {"pre": "ns = np × 16 = 500 × 16 = ", "post": "", "answer": 8000,
             "hint": "Multiply the primary turns by the ratio.", "phase": "substitute"},
            {"pre": "Check: ns ÷ np = 8000 ÷ 500 = ", "post": "", "answer": 16,
             "hint": "Divide the two turn numbers.", "done": "That matches the voltage ratio 16, so ns = 8000 turns.",
             "phase": "substitute"},
        ],
        equation_hint=EQ_TURNS,
        hint="Find the voltage ratio, then multiply the primary turns by it."),
    prob(
        "A transformer steps down 230 V to 12 V. The secondary current is 4 A. Calculate the primary current, assuming 100% efficiency.",
        transformer(["Vp = 230 V", "Ip = ?"], ["Vs = 12 V", "Is = 4 A"], "Ideal: find Ip",
                    "Step-down transformer 230 V to 12 V, secondary current 4 A, 100 percent efficient, find primary current"),
        [0.209], "A", True,
        [{"check": "common", "pattern": "inverse_error", "expect": 76.67,
          "message": "Ip = VsIs/Vp = (12 × 4)/230 = 48/230 = 0.209 A. Scaling the current up with the voltage ratio gives about 77 A, which is wrong."}],
        [
            {"say": "For a 100% efficient transformer, power in = power out: " + EQ_POWER + ", so \\(I_p = \\frac{V_s I_s}{V_p}\\)."},
            {"pre": "Vs × Is = 12 × 4 = ", "post": "", "answer": 48,
             "hint": "Multiply the secondary voltage by the secondary current."},
            {"pre": "Divide by Vp (to 3 d.p.): 48 ÷ 230 = ", "post": "", "answer": 0.209,
             "hint": "Divide by the primary voltage.", "phase": "substitute"},
            {"pre": "Check the power balance, power out = Vs × Is = 12 × 4 = ", "post": "", "answer": 48,
             "hint": "Multiply the secondary voltage by the secondary current.",
             "done": "Power in is Vp × Ip ≈ 230 × 0.209 = 48 W too, so Ip = 0.209 A.",
             "phase": "substitute"},
        ],
        accept=0.005, equation_hint=EQ_POWER,
        hint="Multiply the secondary voltage by the secondary current, then divide by the primary voltage."),
    prob(
        "Electricity is transmitted at 50 A through cables with a total resistance of 5 Ω. Calculate the power wasted as heat in the cables.",
        cable(50, 5, "Transmission cable carrying 50 A with resistance 5 ohms, find power lost as heat"),
        [12500], "W", True,
        [{"check": "common", "pattern": "forgot_square", "expect": 250,
          "message": "P = I²R = 50² × 5 = 2500 × 5 = 12 500 W. Square the current first, or you get only 250 W."}],
        [
            {"say": "Cable loss uses \\(P = I^2 R\\). Square the current before multiplying by the resistance."},
            {"pre": "Square the current: 50 × 50 = ", "post": "", "answer": 2500,
             "hint": "Multiply the current by itself."},
            {"pre": "Multiply by R: 2500 × 5 = ", "post": "", "answer": 12500,
             "hint": "Multiply by the resistance.", "phase": "substitute"},
            {"pre": "Check by dividing back: 12500 ÷ 5 = ", "post": "", "answer": 2500,
             "hint": "Divide the power by the resistance.",
             "done": "That is 50² = 2500, so P = 12 500 W is right.", "phase": "substitute"},
        ],
        equation_hint="\\(P = I^2 R\\)",
        hint="Square the current, then multiply by the resistance."),
    prob(
        "A local substation steps voltage down from 11 000 V to 230 V. The primary coil has 1000 turns. Calculate the number of secondary turns.",
        transformer(["Vp = 11 000 V", "Np = 1000"], ["Vs = 230 V", "Ns = ?"], "Step-down: find Ns",
                    "Substation transformer stepping 11 000 V down to 230 V with 1000 primary turns, find secondary turns"),
        [20.9], "", True,
        [{"check": "common", "pattern": "wrong_rearrange", "expect": 47826,
          "message": "ns = np × (Vs/Vp) = 1000 × (230/11 000) ≈ 20.9 turns. Flipping the ratio gives about 47 800, far too many."}],
        [
            {"say": "Rearrange " + EQ_TURNS + " for the secondary turns: \\(n_s = n_p \\times \\frac{V_s}{V_p}\\)."},
            {"pre": "np × Vs = 1000 × 230 = ", "post": "", "answer": 230000,
             "hint": "Multiply the primary turns by the secondary voltage."},
            {"pre": "Divide by Vp (to 1 d.p.): 230000 ÷ 11000 = ", "post": "", "answer": 20.9,
             "hint": "Divide by the primary voltage.", "phase": "substitute"},
            {"pre": "Check: Vs = Vp × ns ÷ np = 11000 × 20.9 ÷ 1000 = ", "post": "", "answer": 229.9,
             "hint": "Work it left to right.",
             "done": "That is about 230 V, the stated secondary voltage, so ns = 20.9 turns.", "phase": "substitute"},
        ],
        accept=0.5, equation_hint=EQ_TURNS,
        hint="Multiply the primary turns by the secondary voltage, then divide by the primary voltage."),
    prob(
        "A transformer steps 230 V down to 9 V a.c. The secondary coil delivers 3 W. Calculate the secondary current.",
        transformer(["Vp = 230 V", "Ps = 3 W"], ["Vs = 9 V", "Is = ?"], "Find Is from power",
                    "Transformer with 9 V secondary delivering 3 W, find the secondary current"),
        [0.333], "A", True,
        [{"check": "common", "pattern": "inverse_error", "expect": 3,
          "message": "P = Vs × Is, so Is = P/Vs = 3/9 = 0.333 A. Dividing the wrong way (9/3) gives 3 A."}],
        [
            {"say": "The secondary side obeys \\(P = V_s I_s\\), so \\(I_s = \\frac{P}{V_s}\\)."},
            {"pre": "Write the secondary power in watts, Ps = ", "post": "", "answer": 3,
             "hint": "The coil delivers 3 W."},
            {"pre": "Is = Ps ÷ Vs (to 3 d.p.) = 3 ÷ 9 = ", "post": "", "answer": 0.333,
             "hint": "Divide the power by the secondary voltage.", "phase": "substitute"},
            {"pre": "Check the power, Vs × Is to the nearest watt = 9 × 0.333 = ", "post": "", "answer": 3,
             "hint": "Multiply the secondary voltage by your answer.",
             "done": "That is about 3 W, the stated power, so Is = 0.333 A.", "phase": "substitute"},
        ],
        accept=0.005, equation_hint="\\(P = V_s I_s\\)",
        hint="Divide the secondary power by the secondary voltage."),
]

gold = [
    prob(
        "A power station transformer has 200 primary turns connected to 25 000 V and 40 000 secondary turns. Calculate the secondary voltage.",
        transformer(["Vp = 25 000 V", "Np = 200"], ["Vs = ?", "Ns = 40 000"], "Large step-up: find Vs",
                    "Power-station transformer, 25 000 V primary with 200 turns, 40 000 secondary turns, find secondary voltage"),
        [5000000], "V", True,
        [{"check": "common", "pattern": "inverse_ratio", "expect": 125,
          "message": "Vs = Vp × (ns/np) = 25 000 × (40 000/200) = 25 000 × 200 = 5 000 000 V. Flipping the ratio gives only 125 V."}],
        [
            {"say": "Use \\(V_s = V_p \\times \\frac{n_s}{n_p}\\). This is a very large step-up."},
            {"pre": "Turns ratio ns ÷ np = 40000 ÷ 200 = ", "post": "", "answer": 200,
             "hint": "Divide the secondary turns by the primary turns."},
            {"pre": "Vs = 25000 × 200 = ", "post": "", "answer": 5000000,
             "hint": "Multiply the primary voltage by the ratio.", "phase": "substitute"},
            {"pre": "Check: Vs ÷ Vp = 5000000 ÷ 25000 = ", "post": "", "answer": 200,
             "hint": "Divide the two voltages.", "done": "That matches the turns ratio 40 000 ÷ 200 = 200, so Vs = 5 000 000 V.",
             "phase": "substitute"},
        ],
        equation_hint=EQ_TURNS,
        hint="Find the turns ratio, then multiply the primary voltage by it."),
    prob(
        "Using the transformer above (Vp = 25 000 V, Ip = 500 A, Vs = 5 000 000 V), calculate the secondary current assuming 100% efficiency.",
        transformer(["Vp = 25 000 V", "Ip = 500 A"], ["Vs = 5 000 000 V", "Is = ?"], "Ideal: find Is",
                    "Transformer with 25 000 V primary at 500 A stepped up to 5 000 000 V, 100 percent efficient, find secondary current"),
        [2.5], "A", True,
        [{"check": "common", "pattern": "inverse_error", "expect": 100000,
          "message": "Is = VpIp/Vs = (25 000 × 500)/5 000 000 = 2.5 A. Scaling the current up with the voltage gives 100 000 A, which is wrong: step-up raises voltage but lowers current."}],
        [
            {"say": "Power in = power out: " + EQ_POWER + ", so \\(I_s = \\frac{V_p I_p}{V_s}\\)."},
            {"pre": "Power in = Vp × Ip = 25000 × 500 = ", "post": "", "answer": 12500000,
             "hint": "Multiply the primary voltage by the primary current."},
            {"pre": "Is = 12500000 ÷ Vs = 12500000 ÷ 5000000 = ", "post": "", "answer": 2.5,
             "hint": "Divide the power by the secondary voltage.", "phase": "substitute"},
            {"pre": "Check: power out = Vs × Is = 5000000 × 2.5 = ", "post": "", "answer": 12500000,
             "hint": "Multiply the secondary voltage by your answer.",
             "done": "Power out equals the power in, 12 500 000 W, so Is = 2.5 A.", "phase": "substitute"},
        ],
        accept=0.1, equation_hint=EQ_POWER,
        hint="Multiply the primary voltage by the primary current, then divide by the secondary voltage."),
    prob(
        "The transmission cables carry a current of 2.5 A and have a resistance of 2 Ω. Calculate the power lost as heat in the cables.",
        cable(2.5, 2, "Transmission cable carrying 2.5 A with resistance 2 ohms, find power lost as heat"),
        [12.5], "W", True,
        [{"check": "common", "pattern": "forgot_square", "expect": 5,
          "message": "P = I²R = 2.5² × 2 = 6.25 × 2 = 12.5 W. Square the current first, or you get only 5 W."}],
        [
            {"say": "Cable loss uses \\(P = I^2 R\\). Square the current before multiplying by the resistance."},
            {"pre": "Square the current: 2.5 × 2.5 = ", "post": "", "answer": 6.25,
             "hint": "Multiply the current by itself."},
            {"pre": "Multiply by R: 6.25 × 2 = ", "post": "", "answer": 12.5,
             "hint": "Multiply by the resistance.", "phase": "substitute"},
            {"pre": "Check by dividing back: 12.5 ÷ 2 = ", "post": "", "answer": 6.25,
             "hint": "Divide the power by the resistance.",
             "done": "That is 2.5² = 6.25, so P = 12.5 W. Keeping the current low keeps this loss tiny.",
             "phase": "substitute"},
        ],
        equation_hint="\\(P = I^2 R\\)",
        hint="Square the current, then multiply by the resistance."),
    prob(
        "A transformer steps down 230 V to 12 V. The secondary current is 5 A. The transformer is 85% efficient. Calculate the primary current. Give your answer to 3 decimal places.",
        transformer(["Vp = 230 V", "Ip = ?"], ["Vs = 12 V", "Is = 5 A"], "85% efficient: find Ip",
                    "Step-down transformer 230 V to 12 V, secondary current 5 A, 85 percent efficient, find primary current"),
        [0.307], "A", True,
        [{"check": "common", "pattern": "assumed_100", "expect": 0.261,
          "message": "Do not assume 100% efficiency. Power out = 12 × 5 = 60 W, but power in is larger: 60 ÷ 0.85 = 70.6 W. Ip = 70.6 ÷ 230 = 0.307 A. Ignoring the efficiency gives 0.261 A."},
         {"check": "common", "pattern": "wrong_rearrange", "expect": 0.222,
          "message": "Efficiency divides, it does not multiply the output. Ip = (power out ÷ efficiency) ÷ Vp = (60 ÷ 0.85)/230 = 0.307 A. Multiplying by 0.85 gives 0.222 A."}],
        [
            {"say": "Efficiency = useful power out ÷ total power in. Find the input power first, then \\(I_p = \\frac{\\text{power in}}{V_p}\\)."},
            {"pre": "Power out = Vs × Is = 12 × 5 = ", "post": "", "answer": 60,
             "hint": "Multiply the secondary voltage by the secondary current."},
            {"pre": "Power in = power out ÷ efficiency (to 1 d.p.) = 60 ÷ 0.85 = ", "post": "", "answer": 70.6,
             "hint": "Divide the output power by 0.85."},
            {"pre": "Ip = power in ÷ Vp (to 3 d.p.) = 70.6 ÷ 230 = ", "post": "", "answer": 0.307,
             "hint": "Divide the input power by the primary voltage.", "phase": "substitute"},
            {"pre": "Check the efficiency: power out ÷ power in = 60 ÷ 70.6 = ", "post": "", "answer": 0.85,
             "hint": "Divide the two powers.",
             "done": "That is about 0.85, or 85%, so Ip = 0.307 A.", "phase": "substitute"},
        ],
        accept=0.005,
        hint="Find the input power (output power divided by the efficiency), then divide by the primary voltage."),
]

problem_bank = {
    "bronze": bronze,
    "silver": silver,
    "gold": gold,
    "bronze_description": "One equation, values already in the right units. Use the turns ratio Vp/Vs = np/ns to find a voltage or a number of turns.",
    "silver_description": "Rearrange or chain: use the power equation VpIp = VsIs, find a missing voltage first, or work out a cable loss with P = I squared R.",
    "gold_description": "Multi-step: combine turns with power, bring in efficiency below 100%, or find grid loss with P = I squared R.",
}

tier_guides = {
    "bronze": {
        "title": "Bronze: one equation, straight in",
        "steps": [
            "Transformers link voltage to turns: " + EQ_TURNS + ". The primary is the input coil, the secondary is the output.",
            "To find a secondary voltage: \\(V_s = V_p \\times \\frac{n_s}{n_p}\\). More secondary turns gives a higher voltage (step-up); fewer gives a lower one (step-down).",
            "Put the numbers straight in and work left to right.",
        ],
        "example": {
            "question": "A transformer has 400 primary turns and 100 secondary turns. Vp = 240 V. Find the secondary voltage.",
            "steps": [
                {"label": "Equation", "content": "<p>\\(V_s = V_p \\times \\frac{n_s}{n_p}\\)</p>"},
                {"label": "Substitute", "content": "<p>\\(V_s = 240 \\times \\frac{100}{400} = 240 \\times 0.25\\)</p>"},
                {"label": "Check", "content": "<p>Fewer secondary turns, so a step-down: 60 V is below 240 V.</p>"},
                {"label": "Answer", "content": "<p>\\(V_s\\) = <strong>60 V</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: rearrange or use power",
        "steps": [
            "For currents, a 100% efficient transformer obeys " + EQ_POWER + " (power in = power out).",
            "Rearrange before you substitute, for example \\(I_p = \\frac{V_s I_s}{V_p}\\). The higher-voltage side always carries the lower current.",
            "For a cable loss, use \\(P = I^2 R\\): square the current first.",
        ],
        "example": {
            "question": "A transformer has Vp = 200 V, Vs = 50 V and Is = 8 A. Find the primary current (100% efficient).",
            "steps": [
                {"label": "Equation", "content": "<p>\\(I_p = \\frac{V_s I_s}{V_p}\\)</p>"},
                {"label": "Substitute", "content": "<p>\\(I_p = \\frac{50 \\times 8}{200} = \\frac{400}{200}\\)</p>"},
                {"label": "Check", "content": "<p>The higher-voltage side (200 V) carries the lower current, so Ip < Is.</p>"},
                {"label": "Answer", "content": "<p>\\(I_p\\) = <strong>2 A</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chain two ideas",
        "steps": [
            "Gold questions combine steps: turns then power, an efficiency below 100%, or a grid loss.",
            "For a grid loss, find the current with \\(I = \\frac{P}{V}\\), then the heat lost with \\(P = I^2 R\\). The current is squared, so high voltage (low current) wastes far less.",
            "Efficiency = useful power out ÷ total power in. Work in base units and convert to kW or MW only at the end.",
        ],
        "example": {
            "question": "20 MW is sent at 40 000 V through cables of resistance 5 Ω. Find the power lost.",
            "steps": [
                {"label": "Current", "content": "<p>\\(I = \\frac{P}{V} = \\frac{20\\,000\\,000}{40\\,000} = 500\\) A</p>"},
                {"label": "Loss", "content": "<p>\\(P = I^2 R = 500^2 \\times 5 = 250\\,000 \\times 5\\)</p>"},
                {"label": "Check", "content": "<p>1 250 000 W = 1.25 MW, a small fraction of 20 MW.</p>"},
                {"label": "Answer", "content": "<p>\\(P\\) = <strong>1.25 MW</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

guided = {
    "opener": {
        "label": "Before any equations",
        "display": "A power line must carry 2000 W to a village.<br>You can push it through the wire at a low voltage or a high voltage.",
        "steps": [
            {"pre": "At 20 V, the current needed is 2000 ÷ 20 = ", "post": "", "answer": 100,
             "hint": "Power = voltage × current, so current = power ÷ voltage.",
             "say": "Power = voltage × current. The power is fixed; the voltage is your choice."},
            {"pre": "At 2000 V, the current needed is 2000 ÷ 2000 = ", "post": "", "answer": 1,
             "hint": "2000 divided by 2000.",
             "say": "Now push the same power through at a much higher voltage."},
            {"say": "Same 2000 W, but 100 A versus 1 A. Wires heat up as the current <strong>squared</strong> (loss = \\(I^2 R\\)), so 100 A wastes ten thousand times more than 1 A. That is why power travels at very high voltage. A <strong>transformer</strong> trades voltage for current without losing power: " + EQ_POWER + "."},
        ],
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "A transformer has 200 primary turns and 1000 secondary turns. The primary voltage is 30 V. Find the secondary voltage.",
            "steps": [
                {"say": "Turns ratio " + EQ_TURNS + ", so \\(V_s = V_p \\times \\frac{n_s}{n_p}\\)."},
                {"pre": "Divide to get the ratio: 1000 ÷ 200 = ", "post": "", "answer": 5,
                 "hint": "Secondary turns divided by primary turns."},
                {"pre": "Multiply: Vs = 30 × 5 = ", "post": "", "answer": 150,
                 "hint": "Primary voltage times the ratio."},
                {"pre": "Sanity check the voltage ratio: 150 ÷ 30 = ", "post": "", "answer": 5,
                 "hint": "Divide the two voltages."},
                {"pre": "And the turns match: 5 × 200 = ", "post": "", "answer": 1000,
                 "hint": "Ratio times primary turns.",
                 "done": "Back to 1000 secondary turns, so Vs = 150 V. More turns, higher voltage: a step-up."},
            ],
        },
        "silver": {
            "label": "Together: your first one",
            "display": "A transformer has Vp = 400 V, Vs = 100 V and Is = 12 A. Find the primary current, assuming 100% efficiency.",
            "steps": [
                {"say": "Power in = power out: " + EQ_POWER + ", so \\(I_p = \\frac{V_s I_s}{V_p}\\)."},
                {"pre": "Power out = Vs × Is = 100 × 12 = ", "post": "", "answer": 1200,
                 "hint": "Multiply the secondary voltage by the secondary current."},
                {"pre": "That is the power in too. Ip = 1200 ÷ 400 = ", "post": "", "answer": 3,
                 "hint": "Divide the power by the primary voltage."},
                {"pre": "Check power in: Vp × Ip = 400 × 3 = ", "post": "", "answer": 1200,
                 "hint": "Multiply the primary voltage by your answer."},
                {"pre": "Current check: Vp is 4× Vs, so Ip = Is ÷ 4 = 12 ÷ 4 = ", "post": "", "answer": 3,
                 "hint": "Divide the secondary current by 4.",
                 "done": "The higher-voltage side carries the lower current. Ip = 3 A."},
            ],
        },
        "gold": {
            "label": "Together: your first one",
            "display": "A power station sends 40 MW at 40 000 V through cables of resistance 6 Ω. Find the power lost in the cables.",
            "steps": [
                {"say": "Two steps: the current with \\(I = \\frac{P}{V}\\), then the heat loss with \\(P = I^2 R\\)."},
                {"pre": "Current: I = 40000000 ÷ 40000 = ", "post": "", "answer": 1000,
                 "hint": "Divide power by voltage. 40 MW = 40000000 W."},
                {"pre": "Square it: 1000 × 1000 = ", "post": "", "answer": 1000000,
                 "hint": "The current is squared in the loss equation."},
                {"pre": "Multiply by resistance: 1000000 × 6 = ", "post": "", "answer": 6000000,
                 "hint": "Multiply by R = 6."},
                {"pre": "In megawatts: 6000000 ÷ 1000000 = ", "post": "", "answer": 6,
                 "hint": "Divide by a million.",
                 "done": "6 MW lost. A higher voltage would cut the current and slash this loss, because it depends on current squared."},
            ],
        },
    },
}

method_card = {
    "title": "Transformers and Power Transmission",
    "steps": [
        "Use the turns ratio Vp/Vs = np/ns to find a missing voltage or number of turns.",
        "For currents, use VpIp = VsIs (true when 100% efficient).",
        "Step-up means more secondary turns: higher voltage, lower current.",
        "Grid loss is P = I squared R, so high voltage (low current) wastes far less.",
    ],
    "content": ("<p>Transformers use two equations: the turns ratio " + EQ_TURNS +
                " and, for currents, " + EQ_POWER + " (true when 100% efficient). "
                "Check whether your board gives you these or expects them from memory.</p>"
                "<p><strong>Step-up</strong>: more secondary turns, so voltage rises and current falls. "
                "<strong>Step-down</strong> is the reverse. The National Grid sends power at very high "
                "voltage to keep the current low, because cable loss \\(P = I^2 R\\) grows with the "
                "current squared.</p>"),
}

worked_examples = [
    {
        "difficulty": "Bronze",
        "question": "A transformer has 200 primary turns and 1000 secondary turns. The primary voltage is 25 V. Calculate the secondary voltage.",
        "steps": [
            {"label": "Step 1: Write the turns ratio equation", "content": "<p>" + EQ_TURNS + "</p>"},
            {"label": "Step 2: Rearrange and substitute", "content": "<p>\\(V_s = V_p \\times \\frac{n_s}{n_p} = 25 \\times \\frac{1000}{200}\\)</p>"},
            {"label": "Answer", "content": "<p>\\(V_s\\) = <strong>125 V</strong></p>", "is_answer": True},
        ],
    },
    {
        "difficulty": "Silver",
        "question": "A step-up transformer has primary voltage 25 000 V and secondary voltage 400 000 V. The primary current is 800 A. Calculate the secondary current (assume 100% efficiency).",
        "steps": [
            {"label": "Step 1: Write the power equation", "content": "<p>" + EQ_POWER + "</p>"},
            {"label": "Step 2: Rearrange for Is", "content": "<p>\\(I_s = \\frac{V_p I_p}{V_s} = \\frac{25\\,000 \\times 800}{400\\,000}\\)</p>"},
            {"label": "Answer", "content": "<p>\\(I_s\\) = <strong>50 A</strong></p>", "is_answer": True},
        ],
    },
    {
        "difficulty": "Gold",
        "question": "Electricity is transmitted at 50 A through cables with total resistance 5 Ω. Calculate the power wasted as heat.",
        "steps": [
            {"label": "Step 1: Write the equation", "content": "<p>\\(P = I^2 R\\)</p>"},
            {"label": "Step 2: Substitute", "content": "<p>\\(P = 50^2 \\times 5 = 2500 \\times 5\\)</p>"},
            {"label": "Answer", "content": "<p>\\(P\\) = <strong>12 500 W</strong></p>", "is_answer": True},
        ],
    },
]

pd = {
    "method_card": method_card,
    "topic_links": {"prerequisites": [{"slug": "higher-calculations/5", "title": "Nuclear Equations and Half-Life Drill"}]},
    "exam_context": {
        "marks": "3 to 6 per question",
        "paper": "Paper 2 (Physics)",
        "frequency": "High. Transformer and National Grid questions appear on almost every Higher Physics paper.",
    },
    "problem_bank": problem_bank,
    "related_videos": [],
    "worked_examples": worked_examples,
    "tier_guides": tier_guides,
    "guided": guided,
}

with io.open("lesson_higher-calculations-L06@e6541c99e0.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written")
