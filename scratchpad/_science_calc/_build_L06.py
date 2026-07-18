# -*- coding: utf-8 -*-
"""Build guided practice_data for physics-calculations-L06 (Forces, Work Done, Elasticity)."""
import json, io

# ---------------- SVG helpers (theme-safe: text=currentColor, accent arrows) ----------------
DEFS = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#dc2626"/></marker>'
        '<marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>')

def coil(x0, x1, y, n=10):
    """Zigzag spring coil from x0 to x1 at baseline y."""
    step = (x1 - x0) / (n * 2.0)
    pts = ["M %.1f %d" % (x0, y)]
    x = x0
    up = True
    for i in range(n * 2):
        x += step
        yy = y - 10 if up else y + 10
        pts.append("L %.1f %d" % (x, yy))
        up = not up
    pts.append("L %.1f %d" % (x1, y))
    return '<path d="%s" fill="none" stroke="currentColor" stroke-width="2.2"/>' % " ".join(pts)

def svg_open(aria):
    return ('<svg viewBox="0 0 300 150" role="img" aria-label="%s" '
            'style="max-width:300px;margin:0.6em auto;display:block;">%s' % (aria, DEFS))

def txt(x, y, s, anchor="middle", size=12, weight="normal", color="currentColor"):
    return ('<text x="%s" y="%s" text-anchor="%s" font-family="Inter,sans-serif" '
            'font-size="%d" font-weight="%s" fill="%s">%s</text>'
            % (x, y, anchor, size, weight, color, s))

def spring_fig(aria, top_lines, force_label, ext_label, ext_arrow_only=False):
    """Wall + horizontal spring + block + force arrow + extension bracket.
       top_lines: list of strings shown top-left. force_label/ext_label may be '?' bearing."""
    s = svg_open(aria)
    s += '<rect x="10" y="45" width="10" height="70" fill="currentColor"/>'      # wall
    s += coil(20, 150, 80)
    s += ('<rect x="150" y="62" width="40" height="36" rx="3" fill="#60a5fa" '
          'fill-opacity="0.3" stroke="currentColor" stroke-width="1.6"/>')        # block
    # force arrow
    s += '<line x1="190" y1="80" x2="255" y2="80" stroke="#dc2626" stroke-width="3" marker-end="url(#ah)"/>'
    s += txt(222, 72, force_label, size=12, weight="600", color="#dc2626")
    # extension bracket
    s += '<line x1="118" y1="112" x2="150" y2="112" stroke="#dc2626" stroke-width="1.4" stroke-dasharray="4,3"/>'
    s += '<line x1="118" y1="106" x2="118" y2="118" stroke="#dc2626" stroke-width="1.4"/>'
    s += '<line x1="150" y1="106" x2="150" y2="118" stroke="#dc2626" stroke-width="1.4"/>'
    s += txt(134, 132, ext_label, size=11, color="#dc2626")
    # top-left labels
    yy = 24
    for ln in top_lines:
        s += txt(40, yy, ln, anchor="start", size=12)
        yy += 16
    s += '</svg>'
    return s

def weight_fig(aria, mass_label, w_label):
    s = svg_open(aria)
    s += ('<circle cx="150" cy="70" r="30" fill="#60a5fa" fill-opacity="0.3" '
          'stroke="currentColor" stroke-width="1.8"/>')
    s += txt(150, 75, mass_label, size=13)
    s += '<line x1="150" y1="100" x2="150" y2="140" stroke="currentColor" stroke-width="3" marker-end="url(#ag)"/>'
    s += txt(196, 128, w_label, size=12, weight="600")
    s += '</svg>'
    return s

def work_fig(aria, force_label, dist_label, block_label="box"):
    s = svg_open(aria)
    s += ('<rect x="120" y="55" width="56" height="42" rx="3" fill="#60a5fa" fill-opacity="0.3" '
          'stroke="currentColor" stroke-width="1.6"/>')
    s += txt(148, 80, block_label, size=12)
    s += '<line x1="176" y1="76" x2="250" y2="76" stroke="#dc2626" stroke-width="3" marker-end="url(#ah)"/>'
    s += txt(214, 68, force_label, size=12, weight="600", color="#dc2626")
    # floor + distance
    s += '<line x1="60" y1="112" x2="260" y2="112" stroke="currentColor" stroke-width="1.4"/>'
    s += '<line x1="120" y1="118" x2="240" y2="118" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>'
    s += txt(180, 134, dist_label, size=11)
    s += '</svg>'
    return s

def power_fig(aria, force_label, dist_label, time_label):
    s = svg_open(aria)
    s += ('<rect x="110" y="52" width="54" height="40" rx="3" fill="#60a5fa" fill-opacity="0.3" '
          'stroke="currentColor" stroke-width="1.6"/>')
    s += txt(137, 76, "trolley", size=11)
    s += '<line x1="164" y1="72" x2="238" y2="72" stroke="#dc2626" stroke-width="3" marker-end="url(#ah)"/>'
    s += txt(205, 64, force_label, size=12, weight="600", color="#dc2626")
    s += '<line x1="60" y1="108" x2="255" y2="108" stroke="currentColor" stroke-width="1.4"/>'
    s += '<line x1="110" y1="114" x2="228" y2="114" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>'
    s += txt(169, 130, dist_label, size=11)
    s += txt(169, 144, time_label, size=11)
    s += '</svg>'
    return s

def slope_fig(aria, force_label, dist_label, mass_label):
    s = svg_open(aria)
    # incline triangle
    s += '<path d="M30 120 L270 120 L270 40 Z" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="1.6"/>'
    # car (small rect) sitting on slope near middle
    s += ('<rect x="150" y="72" width="40" height="20" rx="3" fill="#60a5fa" fill-opacity="0.4" '
          'stroke="currentColor" stroke-width="1.4" transform="rotate(-18 170 82)"/>')
    s += txt(150, 66, mass_label, size=11)
    # up-slope force arrow (pointing up the incline toward top-right)
    s += '<line x1="150" y1="86" x2="235" y2="58" stroke="#dc2626" stroke-width="3" marker-end="url(#ah)"/>'
    s += txt(210, 92, force_label, size=12, weight="600", color="#dc2626")
    s += txt(210, 108, dist_label, size=11)
    s += '</svg>'
    return s

def launch_fig(aria, k_label, e_label, m_label, v_label):
    s = svg_open(aria)
    s += '<rect x="10" y="45" width="10" height="70" fill="currentColor"/>'
    s += coil(20, 130, 80, n=8)
    s += ('<circle cx="146" cy="80" r="14" fill="#60a5fa" fill-opacity="0.35" '
          'stroke="currentColor" stroke-width="1.6"/>')
    s += txt(146, 84, m_label, size=10)
    s += '<line x1="162" y1="80" x2="245" y2="80" stroke="#dc2626" stroke-width="3" marker-end="url(#ah)"/>'
    s += txt(210, 72, v_label, size=12, weight="600", color="#dc2626")
    s += txt(40, 24, k_label, anchor="start", size=12)
    s += txt(40, 132, e_label, anchor="start", size=11, color="#dc2626")
    s += '</svg>'
    return s

def q(svg, display):
    return svg + '<p>' + display + '</p>'

# ---------------- load canonical (preserve exam_context, worked_examples etc.) ----------------
pd = json.load(io.open("_canonical_L06.json", encoding="utf-8"))

# ============ BANK: displays unchanged; regenerate question SVG; add hint/guided_steps/expects ============
pb = pd["problem_bank"]

# ---- BRONZE ----
B = pb["bronze"]

# B0 weight 5kg -> 50 N
B[0]["question"] = q(weight_fig("A 5 kg object with its weight acting downwards, weight unknown.", "5 kg", "W = ?"),
                     B[0]["display"])
B[0]["hint"] = "Weight is a force: multiply the mass in kg by g."
B[0]["misconceptions"] = [
    {"pattern": "mass_weight", "check": "common", "expect": None,
     "message": "W = mg = 5 × 10 = 50 N. Weight is a force in newtons, not a mass in kg."}]
B[0]["guided_steps"] = [
    {"say": "Weight uses \\(W = m \\times g\\). Here the mass is 5 kg and g = 10 N/kg."},
    {"pre": "Put the mass into the equation: W = ", "post": " × 10", "answer": 5,
     "hint": "The mass in kg goes in first."},
    {"phase": "substitute", "pre": "Now multiply: 5 × 10 = ", "post": "", "answer": 50,
     "hint": "Mass times g gives the weight."},
    {"phase": "substitute", "pre": "Check by reversing: 50 ÷ 10 = ", "post": "", "answer": 5,
     "done": "Back to 5 kg, so W = 50 N is right. Weight is in newtons.",
     "hint": "Dividing the weight by g should give the mass back."}]

# B1 work F=80 d=6 -> 480 J
B[1]["question"] = q(work_fig("A box pushed by an 80 N force over a distance of 6 m.", "F = 80 N", "d = 6 m"),
                     B[1]["display"])
B[1]["hint"] = "Work done is the force multiplied by the distance moved."
B[1]["misconceptions"] = [
    {"pattern": "wrong_formula", "check": "common", "expect": 86,
     "message": "Work is force TIMES distance, not force plus distance. W = 80 × 6 = 480 J."}]
B[1]["guided_steps"] = [
    {"say": "Work done uses \\(W = F \\times d\\). The force is 80 N and the distance is 6 m."},
    {"pre": "Put the force in: W = ", "post": " × 6", "answer": 80,
     "hint": "The force in newtons goes first."},
    {"phase": "substitute", "pre": "Now multiply: 80 × 6 = ", "post": "", "answer": 480,
     "hint": "Force times distance."},
    {"phase": "substitute", "pre": "Check by reversing: 480 ÷ 6 = ", "post": "", "answer": 80,
     "done": "Back to the 80 N force, so W = 480 J is right.",
     "hint": "Dividing the work by the distance should return the force."}]

# B2 F=ke k=300 e=0.02 -> 6 N
B[2]["question"] = q(spring_fig("A spring of stiffness 300 N/m extended by 0.02 m, force unknown.",
                                ["k = 300 N/m"], "F = ?", "e = 0.02 m"), B[2]["display"])
B[2]["hint"] = "Force equals the spring constant times the extension in metres."
B[2]["misconceptions"] = [
    {"pattern": "unit_error", "check": "common", "expect": 600,
     "message": "Keep the extension in metres. 0.02 m, not 2 cm. F = 300 × 0.02 = 6 N."}]
B[2]["guided_steps"] = [
    {"say": "Hooke's law is \\(F = k \\times e\\). The stiffness is 300 N/m and the extension is 0.02 m."},
    {"pre": "Put the stiffness in: F = ", "post": " × 0.02", "answer": 300,
     "hint": "The spring constant goes first."},
    {"phase": "substitute", "pre": "Now multiply: 300 × 0.02 = ", "post": "", "answer": 6,
     "hint": "Stiffness times extension."},
    {"phase": "substitute", "pre": "Check by reversing: 6 ÷ 0.02 = ", "post": "", "answer": 300,
     "done": "Back to 300 N/m, so F = 6 N is right.",
     "hint": "Dividing the force by the extension should return the stiffness."}]

# B3 k=F/e F=6 e=0.04 -> 150 N/m
B[3]["question"] = q(spring_fig("A spring extended 0.04 m by a 6 N force, stiffness unknown.",
                                ["k = ?"], "F = 6 N", "e = 0.04 m"), B[3]["display"])
B[3]["hint"] = "Rearrange F = ke to k = F divided by e."
B[3]["misconceptions"] = [
    {"pattern": "inverse_error", "check": "common", "expect": 0.24,
     "message": "k = F ÷ e, not F × e. k = 6 ÷ 0.04 = 150 N/m."}]
B[3]["guided_steps"] = [
    {"say": "Rearrange \\(F = k e\\) to \\(k = F \\div e\\). The force is 6 N and the extension is 0.04 m."},
    {"pre": "Put the force on top: k = 6 ÷ ", "post": "", "answer": 0.04,
     "hint": "The extension in metres goes on the bottom."},
    {"phase": "substitute", "pre": "Now divide: 6 ÷ 0.04 = ", "post": "", "answer": 150,
     "hint": "Force divided by extension."},
    {"phase": "substitute", "pre": "Check by reversing: 150 × 0.04 = ", "post": "", "answer": 6,
     "done": "Back to the 6 N force, so k = 150 N/m is right.",
     "hint": "Multiplying the stiffness by the extension should return the force."}]

# B4 weight 70kg -> 700 N
B[4]["question"] = q(weight_fig("A 70 kg person with weight acting downwards, weight unknown.", "70 kg", "W = ?"),
                     B[4]["display"])
B[4]["hint"] = "Multiply the mass in kg by g to get the weight in newtons."
B[4]["misconceptions"] = [
    {"pattern": "mass_weight", "check": "common", "expect": None,
     "message": "W = mg = 70 × 10 = 700 N. Weight is a force in newtons, not a mass in kg."}]
B[4]["guided_steps"] = [
    {"say": "Weight uses \\(W = m \\times g\\). The mass is 70 kg and g = 10 N/kg."},
    {"pre": "Put the mass in: W = ", "post": " × 10", "answer": 70,
     "hint": "The mass in kg goes first."},
    {"phase": "substitute", "pre": "Now multiply: 70 × 10 = ", "post": "", "answer": 700,
     "hint": "Mass times g."},
    {"phase": "substitute", "pre": "Check by reversing: 700 ÷ 10 = ", "post": "", "answer": 70,
     "done": "Back to 70 kg, so W = 700 N is right.",
     "hint": "Dividing the weight by g should return the mass."}]

# B5 E=1/2 k e^2 k=200 e=0.05 -> 0.25 J
B[5]["question"] = q(spring_fig("A spring of stiffness 200 N/m compressed by 0.05 m, stored energy unknown.",
                                ["k = 200 N/m"], "E = ?", "e = 0.05 m"), B[5]["display"])
B[5]["hint"] = "Square the extension, then use one half times k times e squared."
B[5]["misconceptions"] = [
    {"pattern": "forgot_square", "check": "common", "expect": 5,
     "message": "The extension is squared. E = ½ × 200 × 0.05² = ½ × 200 × 0.0025 = 0.25 J."},
    {"pattern": "forgot_half", "check": "common", "expect": 0.5,
     "message": "Do not drop the one half. E = ½ × 200 × 0.0025 = 0.25 J, not 0.5 J."}]
B[5]["guided_steps"] = [
    {"say": "Elastic PE is \\(E = \\tfrac{1}{2} k e^2\\). Square the extension first: k = 200 N/m, e = 0.05 m."},
    {"pre": "Square the extension: 0.05 × 0.05 = ", "post": "", "answer": 0.0025,
     "hint": "0.05 times 0.05."},
    {"pre": "Work out the half of k: ½ × 200 = ", "post": "", "answer": 100,
     "hint": "Half of 200."},
    {"phase": "substitute", "pre": "Now multiply: 100 × 0.0025 = ", "post": "", "answer": 0.25,
     "hint": "Half of k, times the squared extension."},
    {"phase": "substitute", "pre": "Check: 0.25 ÷ 100 = ", "post": "", "answer": 0.0025,
     "done": "Back to the squared extension, so E = 0.25 J is right.",
     "hint": "Dividing the energy by ½k should return e squared."}]

# ---- SILVER ----
S = pb["silver"]

# S0 e=F/k F=5 k=40 -> 0.125 m
S[0]["question"] = q(spring_fig("A spring of stiffness 40 N/m pulled by a 5 N force, extension unknown.",
                                ["k = 40 N/m"], "F = 5 N", "e = ?"), S[0]["display"])
S[0]["hint"] = "Rearrange F = ke to e = F divided by k."
S[0]["misconceptions"] = [
    {"pattern": "inverse_error", "check": "common", "expect": 8,
     "message": "e = F ÷ k, so 5 ÷ 40 = 0.125 m. Dividing 40 ÷ 5 the wrong way gives 8, which is far too big."}]
S[0]["guided_steps"] = [
    {"say": "Rearrange \\(F = k e\\) to \\(e = F \\div k\\). The force is 5 N and the stiffness is 40 N/m."},
    {"pre": "Put the force on top: e = 5 ÷ ", "post": "", "answer": 40,
     "hint": "The stiffness goes on the bottom."},
    {"phase": "substitute", "pre": "Now divide: 5 ÷ 40 = ", "post": "", "answer": 0.125,
     "hint": "Force divided by stiffness."},
    {"phase": "substitute", "pre": "Check by reversing: 40 × 0.125 = ", "post": "", "answer": 5,
     "done": "Back to the 5 N force, so e = 0.125 m is right.",
     "hint": "Stiffness times extension should return the force."}]

# S1 E=1/2 k e^2 k=40 e=0.125 -> 0.3125 J (accept 0.01)
S[1]["question"] = q(spring_fig("A spring of stiffness 40 N/m extended by 0.125 m, stored energy unknown.",
                                ["k = 40 N/m"], "E = ?", "e = 0.125 m"), S[1]["display"])
S[1]["hint"] = "Square the extension first, then one half times k times e squared."
S[1]["misconceptions"] = [
    {"pattern": "forgot_square", "check": "common", "expect": 2.5,
     "message": "The extension must be squared. E = ½ × 40 × 0.125² = ½ × 40 × 0.015625 = 0.3125 J."},
    {"pattern": "forgot_half", "check": "common", "expect": 0.625,
     "message": "Keep the one half. E = ½ × 40 × 0.015625 = 0.3125 J, not 0.625 J."}]
S[1]["guided_steps"] = [
    {"say": "Elastic PE is \\(E = \\tfrac{1}{2} k e^2\\). Square first: k = 40 N/m, e = 0.125 m."},
    {"pre": "Square the extension: 0.125 × 0.125 = ", "post": "", "answer": 0.015625,
     "hint": "0.125 times 0.125."},
    {"pre": "Half of k: ½ × 40 = ", "post": "", "answer": 20,
     "hint": "Half of 40."},
    {"phase": "substitute", "pre": "Now multiply: 20 × 0.015625 = ", "post": "", "answer": 0.3125,
     "hint": "Half of k, times the squared extension."},
    {"phase": "substitute", "pre": "Check: 0.3125 ÷ 20 = ", "post": "", "answer": 0.015625,
     "done": "Back to the squared extension, so E = 0.3125 J is right.",
     "hint": "Dividing the energy by ½k should return e squared."}]

# S2 power: work then power F=250 d=12 t=30 -> 100 W
S[2]["question"] = q(power_fig("A trolley pushed by 250 N over 12 m in 30 s, power unknown.",
                               "F = 250 N", "d = 12 m", "t = 30 s"), S[2]["display"])
S[2]["hint"] = "Find the work done first (W = Fd), then divide by the time."
S[2]["misconceptions"] = [
    {"pattern": "forgot_step", "check": "common", "expect": 3000,
     "message": "3000 J is the work done, not the power. Divide by the time: 3000 ÷ 30 = 100 W."}]
S[2]["guided_steps"] = [
    {"say": "Two steps: work done \\(W = F \\times d\\), then power \\(P = W \\div t\\)."},
    {"pre": "Work done: 250 × 12 = ", "post": "", "answer": 3000,
     "hint": "Force times distance."},
    {"phase": "substitute", "pre": "Now the power: 3000 ÷ 30 = ", "post": "", "answer": 100,
     "hint": "Work divided by time."},
    {"phase": "substitute", "pre": "Check by reversing: 100 × 30 = ", "post": "", "answer": 3000,
     "done": "Back to 3000 J of work, so P = 100 W is right.",
     "hint": "Power times time should return the work done."}]

# S3 e=F/k then E=1/2 k e^2, k=500 F=20 -> e=0.04, E=0.4 J
S[3]["question"] = q(spring_fig("A spring of stiffness 500 N/m at its limit force of 20 N, stored energy unknown.",
                                ["k = 500 N/m"], "F = 20 N", "E = ?"), S[3]["display"])
S[3]["hint"] = "Find the extension at that force first (e = F/k), then use one half k e squared."
S[3]["misconceptions"] = [
    {"pattern": "forgot_square", "check": "common", "expect": 10,
     "message": "Square the extension: 0.04² = 0.0016. E = ½ × 500 × 0.0016 = 0.4 J."},
    {"pattern": "wrong_formula", "check": "common", "expect": 0.8,
     "message": "Elastic PE is not force times extension. Use ½ke² = ½ × 500 × 0.0016 = 0.4 J."}]
S[3]["guided_steps"] = [
    {"say": "First find the extension at the limit: \\(e = F \\div k = 20 \\div 500\\). Then \\(E = \\tfrac{1}{2} k e^2\\)."},
    {"pre": "Extension: 20 ÷ 500 = ", "post": "", "answer": 0.04,
     "hint": "Force divided by stiffness."},
    {"pre": "Square it: 0.04 × 0.04 = ", "post": "", "answer": 0.0016,
     "hint": "0.04 times 0.04."},
    {"phase": "substitute", "pre": "Elastic PE: ½ × 500 × 0.0016 = ", "post": "", "answer": 0.4,
     "hint": "Half of 500 is 250, then times 0.0016."},
    {"phase": "substitute", "pre": "Check: 0.4 ÷ 250 = ", "post": "", "answer": 0.0016,
     "done": "Back to the squared extension, so E = 0.4 J is right.",
     "hint": "Dividing the energy by ½k should return e squared."}]

# ---- GOLD ----
G = pb["gold"]

# G0 k=2E/e^2 E=2 e=0.10 -> 400 N/m
G[0]["question"] = q(spring_fig("A spring extended 0.10 m storing 2 J of elastic energy, stiffness unknown.",
                                ["E = 2 J"], "k = ?", "e = 0.10 m"), G[0]["display"])
G[0]["hint"] = "Rearrange E = ½ke² to k = 2E divided by e squared."
G[0]["misconceptions"] = [
    {"pattern": "forgot_square", "check": "common", "expect": 40,
     "message": "The extension is squared. k = 2E ÷ e² = 4 ÷ 0.01 = 400 N/m. Using e (0.1) not e² gives 40."},
    {"pattern": "forgot_rearrange", "check": "common", "expect": None,
     "message": "Rearrange E = ½ke² for k: k = 2E ÷ e² = (2 × 2) ÷ 0.10² = 4 ÷ 0.01 = 400 N/m."}]
G[0]["guided_steps"] = [
    {"say": "Rearrange \\(E = \\tfrac{1}{2} k e^2\\) to \\(k = 2E \\div e^2\\). Here E = 2 J and e = 0.10 m."},
    {"pre": "Top of the fraction: 2 × 2 = ", "post": "", "answer": 4,
     "hint": "Two times the stored energy."},
    {"pre": "Square the extension: 0.10 × 0.10 = ", "post": "", "answer": 0.01,
     "hint": "0.1 times 0.1."},
    {"phase": "substitute", "pre": "Now divide: 4 ÷ 0.01 = ", "post": "", "answer": 400,
     "hint": "The 4 on top, e squared on the bottom."},
    {"phase": "substitute", "pre": "Check: ½ × 400 × 0.01 = ", "post": "", "answer": 2,
     "done": "Back to 2 J stored, so k = 400 N/m is right.",
     "hint": "Putting k back into ½ke² should return 2 J."}]

# G1 work W=Fd F=2400 d=5 -> 12000 J (mass is a distractor)
G[1]["question"] = q(slope_fig("A 1200 kg car on a slope, a 2400 N force along the slope, moved 5 m up the slope.",
                               "F = 2400 N", "d = 5 m", "1200 kg"), G[1]["display"])
G[1]["hint"] = "Use the force acting along the slope, then work done = force times distance."
G[1]["misconceptions"] = [
    {"pattern": "wrong_force", "check": "common", "expect": 6000,
     "message": "Use the 2400 N force along the slope, not the 1200 kg mass. W = 2400 × 5 = 12000 J."}]
G[1]["guided_steps"] = [
    {"say": "Work done is \\(W = F \\times d\\). The useful force along the slope is 2400 N; the 1200 kg is a distractor."},
    {"pre": "Pick the force along the slope: F = ", "post": " N", "answer": 2400,
     "hint": "The component of weight along the slope, in newtons."},
    {"phase": "substitute", "pre": "Now multiply: 2400 × 5 = ", "post": "", "answer": 12000,
     "hint": "Force times distance moved."},
    {"phase": "substitute", "pre": "Check by reversing: 12000 ÷ 5 = ", "post": "", "answer": 2400,
     "done": "Back to the 2400 N force, so W = 12000 J is right.",
     "hint": "Dividing the work by the distance should return the force."}]

# G2 bow: E=1/2 k e^2 = 18 J, then 1/2 m v^2 = 18 -> v = sqrt(720) = 26.83 m/s  (FIX: was 60)
import math
v = math.sqrt(720)
G[2]["display"] = ("A bow (spring constant 400 N/m) is drawn back by 0.30 m. All the stored elastic energy is "
                   "transferred to a 0.05 kg arrow. Calculate the arrow's launch speed. Give your answer to 2 d.p.")
G[2]["question"] = q(launch_fig("A bow of stiffness 400 N/m drawn back 0.30 m launching a 0.05 kg arrow, speed unknown.",
                                "k = 400 N/m", "e = 0.30 m", "0.05 kg", "v = ?"), G[2]["display"])
G[2]["solutions"] = [26.83]
G[2]["accept"] = 0.1
G[2]["unit"] = "m/s"
G[2]["hint"] = "Find the elastic PE first, set it equal to the kinetic energy, then solve for v."
G[2]["misconceptions"] = [
    {"pattern": "forgot_step", "check": "common", "expect": 18,
     "message": "18 J is the stored energy, not the speed. Set ½mv² = 18, so v² = 720 and v = 26.83 m/s."},
    {"pattern": "forgot_square", "check": "common", "expect": None,
     "message": "Square the draw distance in the elastic PE: E = ½ × 400 × 0.30² = 18 J, then v = √(2 × 18 ÷ 0.05) = 26.83 m/s."}]
G[2]["guided_steps"] = [
    {"say": "Elastic PE first: \\(E = \\tfrac{1}{2} k e^2\\), with k = 400 N/m and e = 0.30 m."},
    {"pre": "Square the draw: 0.30 × 0.30 = ", "post": "", "answer": 0.09,
     "hint": "0.3 times 0.3."},
    {"pre": "Stored energy: ½ × 400 × 0.09 = ", "post": "", "answer": 18,
     "hint": "Half of 400 is 200, then times 0.09."},
    {"say": "All 18 J becomes kinetic energy, so \\(\\tfrac{1}{2} m v^2 = 18\\) with m = 0.05 kg."},
    {"phase": "substitute", "pre": "Rearrange for v²: (2 × 18) ÷ 0.05 = ", "post": "", "answer": 720,
     "hint": "Twice the energy, divided by the mass."},
    {"phase": "substitute", "pre": "Take the square root (to 2 d.p.): √720 = ", "post": "", "answer": 26.83,
     "done": "v = 26.83 m/s. The stored elastic energy became the arrow's kinetic energy.",
     "hint": "Square root of 720, rounded to two decimal places."}]

# tier descriptions
pb["bronze_description"] = "One equation, values already in the right units. Pick it, put the numbers in, calculate."
pb["silver_description"] = "Rearrange the equation first, or chain two equations to reach the answer."
pb["gold_description"] = "Multi-step: chain equations (such as elastic energy into kinetic energy) or pick the useful force out from distractors."

# ============ tier_guides ============
pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one equation, straight in",
   "steps": [
     "Pick the equation the words point to: <strong>W = mg</strong> (weight), <strong>W = Fd</strong> (work), <strong>F = ke</strong> (spring force) or <strong>E = ½ke²</strong> (elastic energy).",
     "Put the numbers straight in, then calculate.",
     "State the answer with its unit: N, J or N/m."],
   "example": {
     "question": "A spring of stiffness 250 N/m is extended by 0.04 m. Calculate the force.",
     "steps": [
       {"label": "Equation", "content": "\\(F = k \\times e\\)"},
       {"label": "Substitute", "content": "F = 250 × 0.04"},
       {"label": "Check the unit", "content": "N/m × m gives N"},
       {"label": "Answer", "content": "<strong>F = 10 N</strong>", "isAnswer": True, "is_answer": True}]}},
 "silver": {
   "title": "Silver: rearrange or chain",
   "steps": [
     "Rearrange before you substitute: <strong>e = F ÷ k</strong>, or <strong>k = F ÷ e</strong>.",
     "Or take two steps: find one quantity, then feed it into the next equation.",
     "Square the extension before halving in <strong>E = ½ke²</strong>."],
   "example": {
     "question": "A spring of stiffness 20 N/m is pulled by a 4 N force. Calculate the extension.",
     "steps": [
       {"label": "Rearrange", "content": "\\(e = F \\div k\\)"},
       {"label": "Substitute", "content": "e = 4 ÷ 20"},
       {"label": "Check", "content": "N ÷ N/m gives m"},
       {"label": "Answer", "content": "<strong>e = 0.2 m</strong>", "isAnswer": True, "is_answer": True}]}},
 "gold": {
   "title": "Gold: chain the equations",
   "steps": [
     "Two equations in a row: work out the first quantity, then use it in the second.",
     "For a launch, elastic energy becomes kinetic energy: <strong>½ke² = ½mv²</strong>, then solve for v.",
     "Ignore distractor numbers; use only the force or energy the question actually needs."],
   "example": {
     "question": "A spring stores 9 J of elastic energy. All of it is given to a 0.5 kg ball. Calculate the ball's speed.",
     "steps": [
       {"label": "Set energies equal", "content": "\\(\\tfrac{1}{2} m v^2 = 9\\)"},
       {"label": "Rearrange for v²", "content": "v² = (2 × 9) ÷ 0.5 = 36"},
       {"label": "Check", "content": "take the square root of 36"},
       {"label": "Answer", "content": "<strong>v = 6 m/s</strong>", "isAnswer": True, "is_answer": True}]}}}

# ============ guided (opener + teach) ============
pd["guided"] = {
 "opener": {
   "steps": [
     {"say": "A spring hangs from a hook. Hang 1 N on it and it stretches 2 cm. Hang 2 N and it stretches 4 cm. No formulas, just spot the pattern."},
     {"pre": "Hang 3 N on it. How many cm does it stretch? ", "post": " cm", "answer": 6,
      "hint": "Each newton adds another 2 cm."},
     {"say": "That steady 2 cm per newton is the spring's <strong>stiffness</strong>. The stretch grows in step with the force."},
     {"pre": "The spring is now stretched 10 cm. What force is pulling it? ", "post": " N", "answer": 5,
      "hint": "If each newton gives 2 cm, how many newtons give 10 cm?"},
     {"say": "You just used Hooke's law, \\(F = ke\\): force equals stiffness times extension. Stretch it twice as far and it pulls back twice as hard, but it stores <strong>four</strong> times the energy, because elastic PE is \\(\\tfrac{1}{2}ke^2\\) and the extension is squared."}]},
 "teach": {
   "bronze": {
     "display": "A spring of stiffness 200 N/m is stretched by 10 cm. Calculate the elastic PE stored. Watch the units.",
     "steps": [
       {"say": "Elastic PE is \\(E = \\tfrac{1}{2} k e^2\\). But the extension is in centimetres, and the equation needs metres."},
       {"pre": "Convert the extension: 10 ÷ 100 = ", "post": " m", "answer": 0.1,
        "hint": "100 cm in a metre, so divide by 100."},
       {"pre": "Square it: 0.1 × 0.1 = ", "post": "", "answer": 0.01,
        "hint": "0.1 times 0.1."},
       {"pre": "Half of the stiffness: ½ × 200 = ", "post": "", "answer": 100,
        "hint": "Half of 200."},
       {"pre": "Multiply: 100 × 0.01 = ", "post": "", "answer": 1,
        "done": "1 J. If you had left the extension as 10 cm it would have been 10000 times too big.",
        "hint": "Half of k, times the squared extension."},
       {"say": "So the spring stores <strong>1 J</strong>. The unit of energy is the joule."}]},
   "silver": {
     "display": "A spring of stiffness 80 N/m has a 4 N force applied. Calculate the elastic PE stored.",
     "steps": [
       {"say": "Two steps. First the extension from \\(e = F \\div k\\), then the energy from \\(E = \\tfrac{1}{2} k e^2\\)."},
       {"pre": "Extension: 4 ÷ 80 = ", "post": " m", "answer": 0.05,
        "hint": "Force divided by stiffness."},
       {"pre": "Square it: 0.05 × 0.05 = ", "post": "", "answer": 0.0025,
        "hint": "0.05 times 0.05."},
       {"pre": "Half of the stiffness: ½ × 80 = ", "post": "", "answer": 40,
        "hint": "Half of 80."},
       {"pre": "Multiply: 40 × 0.0025 = ", "post": "", "answer": 0.1,
        "done": "That chained two equations together, which is the silver move.",
        "hint": "Half of k, times the squared extension."},
       {"say": "The spring stores <strong>0.1 J</strong>."}]},
   "gold": {
     "display": "A catapult of stiffness 500 N/m is drawn back 0.20 m. All the stored energy is given to a 0.02 kg stone. Calculate the stone's launch speed to 2 d.p.",
     "steps": [
       {"say": "Elastic PE first: \\(E = \\tfrac{1}{2} k e^2\\), with k = 500 N/m and e = 0.20 m."},
       {"pre": "Square the draw: 0.20 × 0.20 = ", "post": "", "answer": 0.04,
        "hint": "0.2 times 0.2."},
       {"pre": "Stored energy: ½ × 500 × 0.04 = ", "post": "", "answer": 10,
        "hint": "Half of 500 is 250, then times 0.04."},
       {"say": "All 10 J becomes kinetic energy: \\(\\tfrac{1}{2} m v^2 = 10\\), with m = 0.02 kg."},
       {"pre": "Rearrange for v²: (2 × 10) ÷ 0.02 = ", "post": "", "answer": 1000,
        "hint": "Twice the energy, divided by the mass."},
       {"pre": "Square root (to 2 d.p.): √1000 = ", "post": "", "answer": 31.62,
        "done": "31.62 m/s. Elastic energy became kinetic energy, chained through two equations.",
        "hint": "Square root of 1000, to two decimal places."},
       {"say": "The stone launches at <strong>31.62 m/s</strong>."}]}}}

# ============ method_card (slim, no em dash, <=140 words, <=4 steps) ============
pd["method_card"] = {
 "title": "Forces, Work Done and Elasticity",
 "content": ("<p>Four equations that are easy to mix up. <strong>Weight</strong> \\(W = mg\\) is a "
             "force in newtons, not a mass. <strong>Work done</strong> \\(W = Fd\\) needs the distance "
             "moved along the force (joules). <strong>Hooke's law</strong> \\(F = ke\\) links spring "
             "force to extension, with e in metres. <strong>Elastic PE</strong> \\(E = \\tfrac{1}{2}ke^2\\) "
             "squares the extension, so doubling it quadruples the energy. Check whether your board gives "
             "you these equations or expects them from memory. The usual slips are extension in cm not m, "
             "and forgetting to square e.</p>"),
 "steps": [
   "Choose the equation the question points to.",
   "Convert the extension to metres if it is given in cm.",
   "Substitute and, for elastic PE, square the extension.",
   "State the answer with its unit (N, J or N/m)."]}

# ============ exam_context (fix em dash) ============
pd["exam_context"] = {
 "marks": "2 to 4 per calculation",
 "paper": "Physics paper (combined science)",
 "frequency": "Medium. Springs and forces appear regularly across the physics papers."}

# ============ worked_examples: replace em dashes in labels ============
for ex in pd.get("worked_examples", []):
    for st in ex.get("steps", []):
        if "label" in st and st["label"]:
            st["label"] = st["label"].replace(" — ", ": ")

json.dump(pd, io.open("lesson_physics-calculations-L06@5d1494be41.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written. gold[2] solution:", G[2]["solutions"], "v=", round(v, 4))
