# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_canon_215be42800.json", encoding="utf-8"))

# ---------- SVG figures (theme-safe: currentColor strokes/text, soft fills) ----------
SVG_B4 = ('<svg viewBox="0 0 260 60" role="img" aria-label="Three resistors, 4 ohms, 6 ohms and 10 ohms, '
 'connected in series in a line">'
 '<g fill="none" stroke="currentColor" stroke-width="2">'
 '<polyline points="16,35 48,35"/><rect x="48" y="28" width="36" height="14" rx="2" fill="#60a5fa" fill-opacity="0.3"/>'
 '<polyline points="84,35 112,35"/><rect x="112" y="28" width="36" height="14" rx="2" fill="#60a5fa" fill-opacity="0.3"/>'
 '<polyline points="148,35 176,35"/><rect x="176" y="28" width="36" height="14" rx="2" fill="#60a5fa" fill-opacity="0.3"/>'
 '<polyline points="212,35 244,35"/></g>'
 '<g fill="currentColor" font-family="Inter,sans-serif" font-size="11" text-anchor="middle">'
 '<text x="66" y="20">4 &#937;</text><text x="130" y="20">6 &#937;</text><text x="194" y="20">10 &#937;</text></g></svg>')

SVG_S2 = ('<svg viewBox="0 0 260 110" role="img" aria-label="Series circuit: a 12 volt cell with an 8 ohm resistor '
 'and a 16 ohm resistor in one loop">'
 '<g fill="none" stroke="currentColor" stroke-width="2">'
 '<polyline points="30,52 30,30 72,30"/><rect x="72" y="23" width="36" height="14" rx="2" fill="#60a5fa" fill-opacity="0.3"/>'
 '<polyline points="108,30 152,30"/><rect x="152" y="23" width="36" height="14" rx="2" fill="#60a5fa" fill-opacity="0.3"/>'
 '<polyline points="188,30 230,30 230,85 30,85 30,66"/></g>'
 '<line x1="20" y1="58" x2="40" y2="58" stroke="currentColor" stroke-width="2"/>'
 '<line x1="24" y1="64" x2="36" y2="64" stroke="currentColor" stroke-width="4"/>'
 '<g fill="currentColor" font-family="Inter,sans-serif" font-size="11" text-anchor="middle">'
 '<text x="90" y="52">8 &#937;</text><text x="170" y="52">16 &#937;</text><text x="14" y="46">12 V</text></g></svg>')

SVG_S3 = ('<svg viewBox="0 0 200 130" role="img" aria-label="Parallel circuit: a 6 volt cell with a 12 ohm resistor '
 'and a 4 ohm resistor on two separate branches">'
 '<g fill="none" stroke="currentColor" stroke-width="2">'
 '<polyline points="30,30 170,30"/><polyline points="30,100 170,100"/>'
 '<polyline points="110,30 110,44"/><rect x="103" y="44" width="14" height="30" rx="2" fill="#60a5fa" fill-opacity="0.3"/><polyline points="110,74 110,100"/>'
 '<polyline points="170,30 170,44"/><rect x="163" y="44" width="14" height="30" rx="2" fill="#60a5fa" fill-opacity="0.3"/><polyline points="170,74 170,100"/>'
 '<polyline points="30,30 30,58"/><polyline points="30,72 30,100"/></g>'
 '<line x1="20" y1="58" x2="40" y2="58" stroke="currentColor" stroke-width="2"/>'
 '<line x1="24" y1="66" x2="36" y2="66" stroke="currentColor" stroke-width="4"/>'
 '<g fill="currentColor" font-family="Inter,sans-serif" font-size="11">'
 '<text x="124" y="62">12 &#937;</text><text x="182" y="62">4 &#937;</text><text x="4" y="66">6 V</text></g></svg>')

SVG_S4 = ('<svg viewBox="0 0 240 130" role="img" aria-label="Parallel circuit: three identical 12 ohm resistors '
 'on three separate branches">'
 '<g fill="none" stroke="currentColor" stroke-width="2">'
 '<polyline points="30,30 200,30"/><polyline points="30,100 200,100"/>'
 '<polyline points="100,30 100,44"/><rect x="93" y="44" width="14" height="30" rx="2" fill="#60a5fa" fill-opacity="0.3"/><polyline points="100,74 100,100"/>'
 '<polyline points="150,30 150,44"/><rect x="143" y="44" width="14" height="30" rx="2" fill="#60a5fa" fill-opacity="0.3"/><polyline points="150,74 150,100"/>'
 '<polyline points="200,30 200,44"/><rect x="193" y="44" width="14" height="30" rx="2" fill="#60a5fa" fill-opacity="0.3"/><polyline points="200,74 200,100"/>'
 '<polyline points="30,30 30,58"/><polyline points="30,72 30,100"/></g>'
 '<line x1="20" y1="58" x2="40" y2="58" stroke="currentColor" stroke-width="2"/>'
 '<line x1="24" y1="66" x2="36" y2="66" stroke="currentColor" stroke-width="4"/>'
 '<g fill="currentColor" font-family="Inter,sans-serif" font-size="11" text-anchor="middle">'
 '<text x="114" y="62">12 &#937;</text><text x="164" y="62">12 &#937;</text><text x="214" y="62">12 &#937;</text></g></svg>')

SVG_G = ('<svg viewBox="0 0 260 120" role="img" aria-label="Circuit: a 24 volt cell with a 10 ohm resistor in series, '
 'then an 8 ohm and a 24 ohm resistor in parallel">'
 '<g fill="none" stroke="currentColor" stroke-width="2">'
 '<polyline points="30,25 60,25"/><rect x="60" y="18" width="36" height="14" rx="2" fill="#60a5fa" fill-opacity="0.3"/>'
 '<polyline points="96,25 140,25 140,75"/>'
 '<polyline points="140,45 152,45"/><rect x="152" y="38" width="36" height="14" rx="2" fill="#60a5fa" fill-opacity="0.3"/><polyline points="188,45 210,45"/>'
 '<polyline points="140,75 152,75"/><rect x="152" y="68" width="36" height="14" rx="2" fill="#60a5fa" fill-opacity="0.3"/><polyline points="188,75 210,75"/>'
 '<polyline points="210,75 210,25 230,25 230,95 30,95 30,68"/>'
 '<polyline points="30,54 30,25"/></g>'
 '<line x1="20" y1="54" x2="40" y2="54" stroke="currentColor" stroke-width="2"/>'
 '<line x1="24" y1="62" x2="36" y2="62" stroke="currentColor" stroke-width="4"/>'
 '<g fill="currentColor" font-family="Inter,sans-serif" font-size="11" text-anchor="middle">'
 '<text x="78" y="13">10 &#937;</text><text x="170" y="34">8 &#937;</text><text x="170" y="64">24 &#937;</text><text x="12" y="62">24 V</text></g></svg>')

SVG_OPENER = ('<svg viewBox="0 0 200 110" role="img" aria-label="A cell connected to a single resistor in one loop, '
 'illustrating Ohm\'s law">'
 '<g fill="none" stroke="currentColor" stroke-width="2">'
 '<polyline points="30,52 30,30 80,30"/><rect x="80" y="23" width="40" height="14" rx="2" fill="#60a5fa" fill-opacity="0.3"/>'
 '<polyline points="120,30 170,30 170,85 30,85 30,66"/></g>'
 '<line x1="20" y1="58" x2="40" y2="58" stroke="currentColor" stroke-width="2"/>'
 '<line x1="24" y1="64" x2="36" y2="64" stroke="currentColor" stroke-width="4"/>'
 '<g fill="currentColor" font-family="Inter,sans-serif" font-size="11" text-anchor="middle">'
 '<text x="100" y="52">R</text><text x="14" y="46">V</text></g></svg>')

# ---------- helpers ----------
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

def mc(pattern, expect, message):
    return {"pattern": pattern, "check": "common", "expect": expect, "message": message}

pb = live["problem_bank"]

# ================= BRONZE =================
b = pb["bronze"]
b[0]["hint"] = "Rearrange Ohm's law to I = V ÷ R."
b[0]["accept"] = 0.05; b[0]["higher_only"] = False
b[0]["misconceptions"] = [
  mc("wrong_rearrange", 72, "To find current, divide: I = V ÷ R = 12 ÷ 6 = 2 A. Multiplying V × R = 72 is the slip."),
  mc("inverse_error", 0.5, "Current = voltage ÷ resistance = 12 ÷ 6 = 2 A. Doing R ÷ V = 6 ÷ 12 gives 0.5, which is upside down."),
]
b[0]["guided_steps"] = [
  sayonly("Ohm's law is \\(V = IR\\). We want current, so rearrange to \\(I = V/R\\)."),
  box("The voltage is V = ", 12, "The battery is 12 V.", post=" V"),
  box("Now divide: I = 12 ÷ 6 = ", 2, "Twelve divided by six.", post=" A", phase="substitute"),
  box("Check with V = IR: 2 × 6 = ", 12, "Multiply your current by the resistance.", post=" V",
      done="Back to the 12 V battery, so I = 2 A is right."),
]
b[1]["hint"] = "V = IR, just multiply current by resistance."
b[1]["accept"] = 0.5; b[1]["higher_only"] = False
b[1]["misconceptions"] = [
  mc("wrong_rearrange", None, "Voltage is already the subject: V = IR = 3 × 10 = 30 V. Just multiply, no rearranging needed."),
]
b[1]["guided_steps"] = [
  sayonly("Ohm's law is \\(V = IR\\). Voltage is already the subject, so substitute and multiply."),
  box("The current is I = ", 3, "Straight from the question.", post=" A"),
  box("Multiply: V = 3 × 10 = ", 30, "Current times resistance.", post=" V", phase="substitute"),
  box("Check: 30 ÷ 10 = ", 3, "Divide voltage by resistance to get back the current.", post=" A",
      done="Back to 3 A, so V = 30 V is right."),
]
b[2]["hint"] = "Turn the minutes into seconds, then Q = I × t."
b[2]["accept"] = 0.5; b[2]["higher_only"] = False
b[2]["misconceptions"] = [
  mc("unit_error", 1, "Convert the time first: 2 min = 120 s. Q = It = 0.5 × 120 = 60 C. Using 2 instead of 120 gives just 1 C."),
]
b[2]["guided_steps"] = [
  sayonly("Charge is \\(Q = It\\). The time must be in seconds first."),
  box("Convert the time: 2 minutes = 2 × 60 = ", 120, "Sixty seconds in a minute.", post=" s"),
  box("Now Q = It = 0.5 × 120 = ", 60, "Current times the time in seconds.", post=" C", phase="substitute"),
  box("Check: 60 ÷ 120 = ", 0.5, "Charge divided by time gives the current.", post=" A",
      done="Back to 0.5 A, so Q = 60 C is right."),
]
b[3]["hint"] = "In series, add the resistances."
b[3]["accept"] = 0.5; b[3]["higher_only"] = False
b[3]["display"] = SVG_B4 + "Three resistors of 4 Ω, 6 Ω and 10 Ω are connected in series. Calculate the total resistance."
b[3]["misconceptions"] = [
  mc("wrong_formula", None, "In series just add: 4 + 6 + 10 = 20 Ω. The reciprocal (parallel) method does not apply here."),
]
b[3]["guided_steps"] = [
  sayonly("In series, resistances simply add: \\(R = R_1 + R_2 + R_3\\)."),
  box("Add the first two: 4 + 6 = ", 10, "A simple sum.", post=" Ω"),
  box("Add the third: 10 + 10 = ", 20, "Add the last resistor.", post=" Ω", phase="substitute"),
  box("Check all three at once: 4 + 6 + 10 = ", 20, "Add them straight.", post=" Ω",
      done="20 Ω total. Series resistances always add."),
]
b[4]["hint"] = "Rearrange to R = V ÷ I."
b[4]["accept"] = 0.5; b[4]["higher_only"] = False
b[4]["misconceptions"] = [
  mc("wrong_rearrange", 1.5, "Rearrange to R = V ÷ I = 6 ÷ 0.25 = 24 Ω. Multiplying 6 × 0.25 = 1.5 is the slip."),
  mc("inverse_error", None, "Resistance = voltage ÷ current, so R = 6 ÷ 0.25 = 24 Ω, not I ÷ V."),
]
b[4]["guided_steps"] = [
  sayonly("Ohm's law \\(V = IR\\), rearranged for resistance: \\(R = V/I\\)."),
  box("The voltage is V = ", 6, "From the question.", post=" V"),
  box("Divide: R = 6 ÷ 0.25 = ", 24, "Dividing by a quarter multiplies by four.", post=" Ω", phase="substitute"),
  box("Check with V = IR: 0.25 × 24 = ", 6, "Current times your resistance.", post=" V",
      done="Back to 6 V, so R = 24 Ω is right."),
]
b[5]["hint"] = "Convert minutes to seconds, then I = Q ÷ t."
b[5]["accept"] = 0.05; b[5]["higher_only"] = False
b[5]["misconceptions"] = [
  mc("unit_error", 90, "Convert first: 5 min = 300 s. I = Q ÷ t = 450 ÷ 300 = 1.5 A. Using 5 gives 90 A, far too big."),
]
b[5]["guided_steps"] = [
  sayonly("Charge \\(Q = It\\), rearranged for current: \\(I = Q/t\\). Put the time in seconds first."),
  box("Convert: 5 minutes = 5 × 60 = ", 300, "Sixty seconds per minute.", post=" s"),
  box("Now I = Q ÷ t = 450 ÷ 300 = ", 1.5, "Charge divided by time.", post=" A", phase="substitute"),
  box("Check: 1.5 × 300 = ", 450, "Current times time gives back the charge.", post=" C",
      done="Back to 450 C, so I = 1.5 A is right."),
]
b[6]["hint"] = "Which one has V, I and R in it?"
b[6]["higher_only"] = False
b[6]["misconceptions"] = [
  mc("wrong_equation", None, "V = IR (Ohm's law) links voltage, current and resistance. P = VI is power; Q = It is charge flow."),
]
b[7]["hint"] = "Q = I × t. The voltage is not needed."
b[7]["accept"] = 0.2; b[7]["higher_only"] = False
b[7]["misconceptions"] = [
  mc("wrong_formula", 360, "Q = It = 0.3 × 40 = 12 C. The 9 V is a distractor: multiplying 9 × 40 = 360 uses the wrong quantity."),
]
b[7]["guided_steps"] = [
  sayonly("Charge \\(Q = It\\). The time is already in seconds, and the voltage is a distractor here."),
  box("The current is I = ", 0.3, "From the question.", post=" A"),
  box("Now Q = It = 0.3 × 40 = ", 12, "Current times time. Ignore the 9 V.", post=" C", phase="substitute"),
  box("Check: 12 ÷ 40 = ", 0.3, "Charge divided by time gives the current.", post=" A",
      done="Back to 0.3 A, so Q = 12 C is right."),
]

# ================= SILVER =================
s = pb["silver"]
s[0]["hint"] = "Use the reciprocal formula, then flip your answer."
s[0]["accept"] = 0.1; s[0]["higher_only"] = False
s[0]["misconceptions"] = [
  mc("wrong_formula", 25, "Parallel uses reciprocals: 1/R = 1/10 + 1/15 = 5/30 = 1/6, so R = 6 Ω. Adding them (25 Ω) is the series rule."),
  mc("forgot_step", None, "After 1/R = 1/6 you must flip it to get R = 6 Ω. Leaving the answer as 1/6 is unfinished."),
]
s[0]["guided_steps"] = [
  sayonly("Parallel: \\(\\frac{1}{R} = \\frac{1}{R_1} + \\frac{1}{R_2}\\). Use a common denominator of 30."),
  box("1/10 is 3/30 and 1/15 is 2/30. Add the tops: 3 + 2 = ", 5, "Just add the numerators.", post="/30"),
  box("So 1/R = 5/30, which is 1/6. Flip it: R = 30 ÷ 5 = ", 6, "Flip 5/30 to get R.", post=" Ω", phase="substitute"),
  box("Check the parallel total is smaller than both. 30 ÷ 5 = ", 6, "Thirty over five.", post=" Ω",
      done="6 Ω, smaller than both 10 and 15, exactly right for parallel."),
]
s[1]["hint"] = "Find the total resistance, then the current, then V = IR for that resistor."
s[1]["accept"] = 0.1; s[1]["higher_only"] = False
s[1]["display"] = SVG_S2 + "A series circuit has a 12 V battery and two resistors: 8 Ω and 16 Ω. Calculate the voltage across the 16 Ω resistor."
s[1]["misconceptions"] = [
  mc("wrong_formula", 12, "The 12 V is shared. Find the current first (0.5 A), then V = IR = 0.5 × 16 = 8 V. Using the full 12 V is wrong."),
  mc("forgot_step", None, "Total R = 8 + 16 = 24 Ω, current = 12 ÷ 24 = 0.5 A, then V across 16 Ω = 0.5 × 16 = 8 V."),
]
s[1]["guided_steps"] = [
  sayonly("First the total resistance in series: \\(R = 8 + 16\\)."),
  box("Total resistance: 8 + 16 = ", 24, "Add in series.", post=" Ω"),
  sayonly("Current from Ohm's law: \\(I = V/R\\)."),
  box("Current: 12 ÷ 24 = ", 0.5, "Half an amp.", post=" A", phase="substitute"),
  box("Voltage across the 16 Ω: V = IR = 0.5 × 16 = ", 8, "Current times that resistor.", post=" V"),
  box("Check: the 8 Ω drops 0.5 × 8 = 4 V, so the two add to 4 + 8 = ", 12, "Add the two voltage drops.", post=" V",
      done="They add to the 12 V battery, so 8 V across the 16 Ω is right."),
]
s[2]["hint"] = "Each branch gets the full voltage. Find each current and add them."
s[2]["accept"] = 0.05; s[2]["higher_only"] = False
s[2]["display"] = SVG_S3 + "A parallel circuit has a 6 V battery connected to two branches. Branch 1 has a 12 Ω resistor and branch 2 has a 4 Ω resistor. Calculate the total current drawn from the battery."
s[2]["misconceptions"] = [
  mc("wrong_formula", 0.375, "Do not add the resistances. Each branch gets the full 6 V: I₁ = 0.5 A, I₂ = 1.5 A, total 2 A. Treating it as series (16 Ω) gives 0.375 A."),
  mc("forgot_step", None, "In parallel each branch gets the full 6 V: I₁ = 6 ÷ 12 = 0.5 A, I₂ = 6 ÷ 4 = 1.5 A, total 2 A."),
]
s[2]["guided_steps"] = [
  sayonly("In parallel, each branch gets the full 6 V. Find each branch current with \\(I = V/R\\)."),
  box("Branch 1: I₁ = 6 ÷ 12 = ", 0.5, "Six over twelve.", post=" A"),
  box("Branch 2: I₂ = 6 ÷ 4 = ", 1.5, "Six over four.", post=" A", phase="substitute"),
  box("Total current = 0.5 + 1.5 = ", 2, "Add the branch currents.", post=" A"),
  box("Check with the combined resistance: 12 and 4 in parallel is 3 Ω, so 6 ÷ 3 = ", 2, "Six over three.", post=" A",
      done="Same 2 A both ways, so the total current is right."),
]
s[3]["hint"] = "Reciprocals add; for identical resistors the total is R ÷ n."
s[3]["accept"] = 0.1; s[3]["higher_only"] = False
s[3]["display"] = SVG_S4 + "Three identical resistors of 12 Ω are connected in parallel. Calculate the total resistance."
s[3]["misconceptions"] = [
  mc("wrong_formula", 36, "Parallel: 1/R = 3/12 = 1/4, so R = 4 Ω. For n identical resistors, R = R ÷ n. Adding them (36 Ω) is the series rule."),
]
s[3]["guided_steps"] = [
  sayonly("Parallel: \\(\\frac{1}{R} = \\frac{1}{12} + \\frac{1}{12} + \\frac{1}{12}\\)."),
  box("Add the twelfths: 1 + 1 + 1 = ", 3, "Three twelfths.", post="/12"),
  box("So 1/R = 3/12, which is 1/4. Flip it: R = 12 ÷ 3 = ", 4, "Flip 3/12.", post=" Ω", phase="substitute"),
  box("Check with the shortcut R ÷ n: 12 ÷ 3 = ", 4, "Twelve over three.", post=" Ω",
      done="4 Ω, smaller than 12, correct for parallel."),
]
s[4]["hint"] = "Convert mA to A and kΩ to Ω first, then V = IR."
s[4]["accept"] = 1; s[4]["higher_only"] = False
s[4]["misconceptions"] = [
  mc("unit_error", 0.3, "Convert both: 250 mA = 0.25 A and 1.2 kΩ = 1200 Ω. V = 0.25 × 1200 = 300 V. Forgetting the kΩ (using 1.2) gives only 0.3 V."),
  mc("forgot_step", 300000, "Both units must change. Leaving the current as 250 A gives 250 × 1200 = 300000, nonsense. Use 0.25 A and 1200 Ω."),
]
s[4]["guided_steps"] = [
  sayonly("Ohm's law \\(V = IR\\), but convert to base units first."),
  box("Current: 250 mA in amps = 250 ÷ 1000 = ", 0.25, "A thousand milliamps in an amp.", post=" A"),
  box("Resistance: 1.2 kΩ in ohms = 1.2 × 1000 = ", 1200, "A thousand ohms in a kilo-ohm.", post=" Ω"),
  box("Now V = IR = 0.25 × 1200 = ", 300, "Multiply the converted values.", post=" V", phase="substitute"),
  box("Check: 300 ÷ 1200 = ", 0.25, "Voltage over resistance gives the current.", post=" A",
      done="Back to 0.25 A, so V = 300 V is right."),
]
s[5]["hint"] = "Convert minutes to seconds, then I = Q ÷ t."
s[5]["accept"] = 0.05; s[5]["higher_only"] = False
s[5]["misconceptions"] = [
  mc("unit_error", 60, "Convert first: 3 min = 180 s. I = Q ÷ t = 180 ÷ 180 = 1 A. Using 3 gives 60 A."),
]
s[5]["guided_steps"] = [
  sayonly("Charge \\(Q = It\\), rearranged: \\(I = Q/t\\). Put the time in seconds."),
  box("Convert: 3 minutes = 3 × 60 = ", 180, "Sixty seconds per minute.", post=" s"),
  box("Now I = Q ÷ t = 180 ÷ 180 = ", 1, "One hundred and eighty over one hundred and eighty.", post=" A", phase="substitute"),
  box("Check: 1 × 180 = ", 180, "Current times time gives back the charge.", post=" C",
      done="Back to 180 C, so I = 1 A is right."),
]

# ================= GOLD =================
g = pb["gold"]
g[0]["hint"] = "Combine the parallel pair first, then add the series resistor."
g[0]["accept"] = 0.05; g[0]["higher_only"] = False
g[0]["display"] = SVG_G + "A 24 V battery is connected to a 10 Ω resistor in series with two parallel resistors of 8 Ω and 24 Ω. Calculate the current drawn from the battery."
g[0]["misconceptions"] = [
  mc("wrong_formula", None, "The 8 Ω and 24 Ω are in parallel: combine them to 6 Ω first, then add the series 10 Ω to get 16 Ω. I = 24 ÷ 16 = 1.5 A. Adding all three (42 Ω) is wrong."),
  mc("forgot_step", None, "Parallel of 8 and 24: 1/R = 1/8 + 1/24 = 1/6, so R = 6 Ω. Total = 10 + 6 = 16 Ω. I = 24 ÷ 16 = 1.5 A."),
]
g[0]["guided_steps"] = [
  sayonly("Deal with the parallel pair first: \\(\\frac{1}{R_p} = \\frac{1}{8} + \\frac{1}{24}\\), common denominator 24."),
  box("1/8 is 3/24, plus 1/24. Add the tops: 3 + 1 = ", 4, "Add the numerators.", post="/24"),
  box("So 1/Rₚ = 4/24, which is 1/6. Flip: Rₚ = 24 ÷ 4 = ", 6, "Flip 4/24.", post=" Ω"),
  box("Total resistance in series: 10 + 6 = ", 16, "Add the series 10 Ω.", post=" Ω", phase="substitute"),
  box("Battery current: I = V ÷ R = 24 ÷ 16 = ", 1.5, "Twenty-four over sixteen.", post=" A"),
  box("Check: 1.5 A through 16 Ω drops 1.5 × 16 = ", 24, "Current times total resistance.", post=" V",
      done="Back to the 24 V battery, so 1.5 A is right."),
]
g[1]["hint"] = "Find the total current, then V = IR across the 6 Ω combination."
g[1]["accept"] = 0.1; g[1]["higher_only"] = False
g[1]["display"] = SVG_G + "A 24 V battery is connected to a 10 Ω resistor in series with two parallel resistors of 8 Ω and 24 Ω. Calculate the voltage across the parallel combination."
g[1]["misconceptions"] = [
  mc("forgot_step", None, "The current is 1.5 A. Voltage across the parallel pair = IR = 1.5 × 6 = 9 V, or 24 − 15 = 9 V."),
  mc("wrong_formula", None, "Find the total current first, then use V = IR with the parallel combination's 6 Ω, not the full 24 V."),
]
g[1]["guided_steps"] = [
  sayonly("Same circuit: the parallel pair combines to 6 Ω and the total is 16 Ω."),
  box("Battery current: I = 24 ÷ 16 = ", 1.5, "Twenty-four over sixteen.", post=" A"),
  box("Voltage across the parallel pair: V = IR = 1.5 × 6 = ", 9, "Current times the 6 Ω combination.", post=" V", phase="substitute"),
  box("Check: the 10 Ω drops 1.5 × 10 = 15 V, so the parallel gets 24 − 15 = ", 9, "Subtract the 10 Ω drop from 24 V.", post=" V",
      done="24 V splits as 15 V plus 9 V, so 9 V across the parallel pair is right."),
]
g[2]["hint"] = "Find the current, then square it for P = I²R."
g[2]["accept"] = 0.2; g[2]["higher_only"] = False
g[2]["misconceptions"] = [
  mc("forgot_square", 6, "Square the current: I² = 2² = 4, so P = I²R = 4 × 3 = 12 W. Forgetting to square (2 × 3) gives only 6 W."),
  mc("forgot_step", None, "First find I = V ÷ R = 6 ÷ 3 = 2 A, then P = I²R = 4 × 3 = 12 W."),
]
g[2]["guided_steps"] = [
  sayonly("Two steps: first the current \\(I = V/R\\), then the power \\(P = I^2R\\)."),
  box("Current: I = 6 ÷ 3 = ", 2, "Six over three.", post=" A"),
  box("Square the current: I² = 2² = ", 4, "Two squared.", phase="substitute"),
  box("Now P = I²R = 4 × 3 = ", 12, "Squared current times resistance.", post=" W"),
  box("Check with P = VI: 6 × 2 = ", 12, "Voltage times current.", post=" W",
      done="Same 12 W, so the power is right."),
]
g[3]["hint"] = "Find the current with I = P ÷ V, then R = V ÷ I."
g[3]["accept"] = 0.1; g[3]["higher_only"] = False
g[3]["misconceptions"] = [
  mc("forgot_step", None, "From P = VI: I = 36 ÷ 12 = 3 A. Then R = V ÷ I = 12 ÷ 3 = 4 Ω, or R = V² ÷ P = 144 ÷ 36 = 4 Ω."),
  mc("wrong_rearrange", None, "You need two steps: current first (I = P ÷ V), then R = V ÷ I."),
]
g[3]["guided_steps"] = [
  sayonly("Use \\(P = VI\\) to get the current, then \\(R = V/I\\)."),
  box("Current: I = P ÷ V = 36 ÷ 12 = ", 3, "Power over voltage.", post=" A"),
  box("Now resistance: R = V ÷ I = 12 ÷ 3 = ", 4, "Voltage over current.", post=" Ω", phase="substitute"),
  box("Check with P = V²/R: 144 ÷ 4 = ", 36, "One hundred and forty-four over your resistance.", post=" W",
      done="Back to 36 W, so R = 4 Ω is right."),
]
g[4]["hint"] = "Find the total resistance, then subtract the known resistor."
g[4]["accept"] = 0.2; g[4]["higher_only"] = False
g[4]["misconceptions"] = [
  mc("wrong_rearrange", 25, "Total R = V ÷ I = 10 ÷ 0.4 = 25 Ω, then subtract the known 15 Ω to get 10 Ω. Stopping at 25 forgets to subtract."),
  mc("forgot_step", None, "Find the total resistance from Ohm's law, then subtract the resistor you already know."),
]
g[4]["guided_steps"] = [
  sayonly("Total resistance from Ohm's law: \\(R = V/I\\), then subtract the known resistor."),
  box("Total R = 10 ÷ 0.4 = ", 25, "Ten over nought point four.", post=" Ω"),
  box("Subtract the known 15 Ω: 25 − 15 = ", 10, "Series resistances add, so the rest is the second resistor.", post=" Ω", phase="substitute"),
  box("Check: 15 + 10 = 25 Ω total, and I = 10 ÷ 25 = ", 0.4, "Ten over twenty-five.", post=" A",
      done="Back to 0.4 A, so the second resistor is 10 Ω."),
]
g[5]["hint"] = "Find the current, convert the time, then Q = I × t."
g[5]["accept"] = 1; g[5]["higher_only"] = False
g[5]["misconceptions"] = [
  mc("unit_error", 2, "Convert the time: 10 min = 600 s. I = 9 ÷ 45 = 0.2 A, then Q = It = 0.2 × 600 = 120 C. Using 10 s gives only 2 C."),
  mc("forgot_step", None, "Two steps: I = V ÷ R = 9 ÷ 45 = 0.2 A, then convert the time to 600 s and Q = It = 120 C."),
]
g[5]["guided_steps"] = [
  sayonly("Two steps: current \\(I = V/R\\), then charge \\(Q = It\\) with the time in seconds."),
  box("Current: I = 9 ÷ 45 = ", 0.2, "Nine over forty-five.", post=" A"),
  box("Convert the time: 10 minutes = 10 × 60 = ", 600, "Sixty seconds per minute.", post=" s"),
  box("Now Q = It = 0.2 × 600 = ", 120, "Current times time in seconds.", post=" C", phase="substitute"),
  box("Check: 120 ÷ 600 = ", 0.2, "Charge over time gives the current.", post=" A",
      done="Back to 0.2 A, so Q = 120 C is right."),
]

# ================= tier descriptions =================
pb["bronze_description"] = "One equation, values already in the right units: pick V = IR or Q = It, rearrange if the unknown is not the subject, and substitute straight in."
pb["silver_description"] = "Convert an awkward unit first (mA, kΩ, minutes) or combine two resistors in series or parallel, then use Ohm's law."
pb["gold_description"] = "Chain two steps: reduce a series-and-parallel network, or find the current then the power or charge, and check your result."

# ================= tier_guides =================
live["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one equation, straight in",
   "steps": [
     "Pick the equation the quantities point to: \\(V = IR\\) for voltage, current or resistance, \\(Q = It\\) for charge. In series, resistances add.",
     "Rearrange if the unknown is not the subject: \\(I = V/R\\) or \\(R = V/I\\). Then substitute and compute.",
     "State the unit with your answer: A, V, \\(\\Omega\\) or C."
   ],
   "example": {
     "question": "A 12 V battery drives a current through a 4 Ω resistor. Find the current.",
     "steps": [
       {"label": "Equation", "content": "<p>Rearrange \\(V = IR\\) to \\(I = V/R\\).</p>"},
       {"label": "Substitute", "content": "<p>\\(I = 12 / 4\\)</p>"},
       {"label": "Check", "content": "<p>\\(3 \\times 4 = 12\\) V ✓</p>"},
       {"label": "Answer", "content": "<p><strong>3 A</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 },
 "silver": {
   "title": "Silver: convert or combine first",
   "steps": [
     "One thing stands between you and Ohm's law. Convert any awkward unit to the base: mA ÷ 1000 to A, k\\(\\Omega\\) × 1000 to \\(\\Omega\\), minutes × 60 to seconds.",
     "Or combine resistors first. Series: add them. Parallel: \\(\\frac{1}{R} = \\frac{1}{R_1} + \\frac{1}{R_2}\\), then flip. A parallel total is always smaller than the smallest resistor.",
     "Then it is a bronze question: substitute and compute."
   ],
   "example": {
     "question": "Two resistors of 6 Ω and 12 Ω are in parallel. Find the total resistance.",
     "steps": [
       {"label": "Reciprocals", "content": "<p>\\(\\frac{1}{R} = \\frac{1}{6} + \\frac{1}{12} = \\frac{3}{12} = \\frac{1}{4}\\)</p>"},
       {"label": "Flip", "content": "<p>\\(R = 4\\) \\(\\Omega\\)</p>"},
       {"label": "Check", "content": "<p>4 \\(\\Omega\\) is smaller than 6 \\(\\Omega\\) ✓</p>"},
       {"label": "Answer", "content": "<p><strong>4 \\(\\Omega\\)</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 },
 "gold": {
   "title": "Gold: two steps chained",
   "steps": [
     "Break a mixed network down: reduce the parallel part first, then add the series resistor to get the total.",
     "Or chain equations: find the current with \\(I = V/R\\), then feed it into \\(P = I^2R\\) or \\(Q = It\\).",
     "Always check: put your answer back into the original equation and confirm it returns a given value."
   ],
   "example": {
     "question": "A 24 V battery feeds a 10 Ω resistor in series with 8 Ω and 24 Ω in parallel. Find the battery current.",
     "steps": [
       {"label": "Parallel first", "content": "<p>\\(\\frac{1}{R_p} = \\frac{1}{8} + \\frac{1}{24} = \\frac{1}{6}\\), so \\(R_p = 6\\) \\(\\Omega\\).</p>"},
       {"label": "Total", "content": "<p>\\(R = 10 + 6 = 16\\) \\(\\Omega\\)</p>"},
       {"label": "Current", "content": "<p>\\(I = 24 / 16 = 1.5\\) A</p>"},
       {"label": "Check", "content": "<p>\\(1.5 \\times 16 = 24\\) V ✓</p>"},
       {"label": "Answer", "content": "<p><strong>1.5 A</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 }
}

# ================= guided (opener + teach) =================
live["guided"] = {
 "opener": {
   "label": "Before any circuit maths",
   "display": SVG_OPENER + "<br>A bulb runs off a 3 V battery and draws a current of 1 A. You swap in a 6 V battery, same bulb.",
   "steps": [
     box("Twice the push. The current becomes ", 2,
         "Double the voltage, double the current through the same bulb.", post=" A",
         say="No equations yet. Just think about pushing twice as hard through the same bulb."),
     box("The bulb fights the flow by the same amount each time, and that fight is its resistance. With the 3 V battery: R = 3 ÷ 1 = ", 3,
         "Voltage divided by current.", post=" Ω",
         say="That 'fight' has a name: <strong>resistance</strong>. It equals voltage ÷ current."),
     sayonly("You just used <strong>Ohm's law</strong>: \\(V = IR\\). Voltage is the push, current is the flow, resistance is the fight. Rearranged, \\(I = V/R\\) and \\(R = V/I\\). Nearly every circuit question is this one relationship, sometimes after adding resistors up first.")
   ]
 },
 "teach": {
   "bronze": {
     "display": "A 9 V battery is connected to a 3 Ω resistor. Calculate the current.",
     "label": "Together: your first one",
     "steps": [
       sayonly("Ohm's law is \\(V = IR\\). We want current, so rearrange to \\(I = V/R\\)."),
       box("The voltage is V = ", 9, "Straight from the question.", post=" V"),
       box("The resistance is R = ", 3, "Straight from the question.", post=" Ω"),
       box("Now divide: I = 9 ÷ 3 = ", 3, "Nine over three.", post=" A", phase="substitute"),
       box("Check with V = IR: 3 × 3 = ", 9, "Current times resistance.", post=" V",
           done="Back to the 9 V battery, so I = 3 A is right.")
     ]
   },
   "silver": {
     "display": "A current of 500 mA flows through a 2 kΩ resistor. Calculate the voltage.",
     "label": "Together: the silver move",
     "steps": [
       sayonly("Ohm's law \\(V = IR\\), but the units are not base units yet. Convert first."),
       box("Current: 500 mA in amps = 500 ÷ 1000 = ", 0.5, "A thousand milliamps in an amp.", post=" A"),
       box("Resistance: 2 kΩ in ohms = 2 × 1000 = ", 2000, "A thousand ohms in a kilo-ohm.", post=" Ω"),
       box("Now V = IR = 0.5 × 2000 = ", 1000, "Multiply the converted values.", post=" V", phase="substitute"),
       box("Check: 1000 ÷ 2000 = ", 0.5, "Voltage over resistance gives the current.", post=" A",
           done="Back to 0.5 A, so V = 1000 V is right.")
     ]
   },
   "gold": {
     "display": "A 12 V battery is connected to a 2 Ω resistor in series with two parallel resistors of 3 Ω and 6 Ω. Calculate the current drawn from the battery.",
     "label": "Together: the gold move",
     "steps": [
       sayonly("Deal with the parallel pair first: \\(\\frac{1}{R_p} = \\frac{1}{3} + \\frac{1}{6}\\), common denominator 6."),
       box("1/3 is 2/6, plus 1/6. Add the tops: 2 + 1 = ", 3, "Add the numerators.", post="/6"),
       box("So 1/Rₚ = 3/6, which is 1/2. Flip: Rₚ = 6 ÷ 3 = ", 2, "Flip 3/6.", post=" Ω"),
       box("Total resistance in series: 2 + 2 = ", 4, "Add the series 2 Ω.", post=" Ω", phase="substitute"),
       box("Battery current: I = V ÷ R = 12 ÷ 4 = ", 3, "Twelve over four.", post=" A"),
       box("Check: 3 A through 4 Ω drops 3 × 4 = ", 12, "Current times total resistance.", post=" V",
           done="Back to the 12 V battery, so 3 A is right.")
     ]
   }
 }
}

# ================= slim method_card =================
live["method_card"] = {
 "title": "Circuit Calculations",
 "steps": [
   "Decide: series (resistances add) or parallel (reciprocals add, total is smaller).",
   "Pick the equation: V = IR, or Q = It for charge.",
   "Convert units to base (A, Ω, V, seconds), then substitute.",
   "State the unit and check the answer fits the circuit."
 ],
 "content": "<p>Circuit questions rest on <strong>Ohm's law</strong> \\(V = IR\\) and <strong>charge flow</strong> \\(Q = It\\), plus the rules for combining resistors.</p><p>In <strong>series</strong> the current is the same everywhere and resistances add. In <strong>parallel</strong> each branch sees the full voltage, branch currents add, and the total resistance is smaller than the smallest resistor. For power use \\(P = VI\\) or \\(P = I^2R\\). Put time in seconds before \\(Q = It\\).</p>"
}

# ================= fix preserved fields (em dashes) =================
live["exam_context"]["frequency"] = "Every exam: circuit calculations appear on every Paper 1"
live["exam_context"]["marks"] = "3 to 5 per calculation"
for we in live.get("worked_examples", []):
  for st in we.get("steps", []):
    if "label" in st:
      st["label"] = st["label"].replace(" — ", ": ")

json.dump(live, io.open("lesson_physics-calculations-L03@215be42800.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

sj = json.dumps(live, ensure_ascii=False)
print("written; em dash count:", sj.count("—"))
def words(x): return len([w for w in x.replace("\\("," ").replace("\\)"," ").split() if w])
print("mc content words:", words(live["method_card"]["content"]))
for t in ("bronze","silver","gold"):
    print(t, "tier words:", sum(words(x) for x in live["tier_guides"][t]["steps"]))
