# -*- coding: utf-8 -*-
import json, io, re

CANON = "_my_L06_4fbd_canonical.json"
OUT = "lesson_higher-calculations-L06@4fbd5cf5b9.json"

pd = json.load(io.open(CANON, encoding="utf-8"))

# ---------- 1. SLIM METHOD CARD (<=4 steps, content <=140 words) ----------
pd["method_card"] = {
    "title": "Waves, Half-Life and Density",
    "steps": [
        "Waves: use v = fλ. Rearrange to f = v ÷ λ or λ = v ÷ f when needed.",
        "Density: use ρ = m ÷ V. Convert cm³ to m³ (÷ 1 000 000) for kg/m³.",
        "Half-life: find n = time ÷ half-life, then halve the activity n times (never divide by n).",
        "State every answer with its unit: m/s, Hz, m, kg/m³ or Bq."
    ],
    "content": "<p>Three recall equations from different corners of physics. Waves: v = fλ, where speed is in m/s, frequency in Hz and wavelength in m. Density: ρ = m ÷ V, where mass is in kg and volume in m³ (1 cm³ = 0.000001 m³). Check whether your board gives you either equation.</p><p>Half-life needs no formula: each half-life the activity halves. Work out n = total time ÷ half-life, then halve the starting activity n times. To find a half-life from data, count how many halvings link the start and end activity, then divide the time by that count. Always finish with the correct unit.</p>"
}

# ---------- 2. FIX EM DASHES IN PRESERVED exam_context ----------
ec = pd.get("exam_context", {})
for k in list(ec.keys()):
    if isinstance(ec[k], str):
        ec[k] = ec[k].replace("—", ":")

# ---------- 3. FIX SVGs (remove xmlns http, add role+aria-label, theme-safe stroke) ----------
def fix_svg(s):
    if not isinstance(s, str) or "<svg" not in s:
        return s
    s = s.replace(
        'xmlns="http://www.w3.org/2000/svg"',
        'role="img" aria-label="A transverse wave with its wavelength marked"'
    )
    s = s.replace("#1e3a8a", "currentColor")
    return s

# ---------- 4. TIER DESCRIPTIONS ----------
pb = pd["problem_bank"]
pb["bronze_description"] = "One equation with the values already in the right units: v = fλ, ρ = m ÷ V, or a whole number of half-lives."
pb["silver_description"] = "Convert a unit or rearrange the equation first, or find a half-life by counting halvings in the data."
pb["gold_description"] = "Multi-step problems: chain two wave steps, read decay data, or reason about density and usability."

# ---------- 5. HINTS / MISCONCEPTIONS / GUIDED_STEPS PER PROBLEM ----------
def box(pre, answer, hint, post="", phase=None, done=None, say=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if phase: d["phase"] = phase
    if done: d["done"] = done
    if say: d["say"] = say
    return d
def say(t): return {"say": t}
def m(pattern, message, expect, note):
    return {"pattern": pattern, "message": message, "expect": expect, "note": note}

SUB = "substitute"

bronze_steps = {
0:[say("One equation: v = fλ. Both units are already right (Hz and m)."),
   box("Frequency f (Hz) = ",50,"Read it from the question."),
   box("Wavelength λ (m) = ",6.8,"Read it from the question."),
   box("v = f × λ = 50 × 6.8 = ",340,"Multiply frequency by wavelength.",phase=SUB,done="That is the wave speed."),
   box("Check: 340 ÷ 6.8 = ",50,"Divide the speed back by the wavelength.",done="Gives back 50 Hz, so 340 m/s is right."),
   say("So the wave speed is <strong>340 m/s</strong>.")],
1:[say("Rearrange v = fλ to f = v ÷ λ. Units are already right."),
   box("Speed v (m/s) = ",300000000,"300 000 000 m/s."),
   box("Wavelength λ (m) = ",0.1,"0.10 m."),
   box("f = v ÷ λ = 300000000 ÷ 0.10 = ",3000000000,"Divide speed by wavelength.",phase=SUB,done="That is 3 × 10⁹ Hz."),
   box("Check: 3000000000 × 0.10 = ",300000000,"Multiply back by the wavelength.",done="Back to the speed, so 3 × 10⁹ Hz is right."),
   say("So the frequency is <strong>3 × 10⁹ Hz</strong> (3 000 000 000 Hz).")],
2:[say("Units match (g and cm³), so density comes out in g/cm³. Use ρ = m ÷ V."),
   box("Mass m (g) = ",500,"Read it from the question."),
   box("Volume V (cm³) = ",250,"Read it from the question."),
   box("ρ = m ÷ V = 500 ÷ 250 = ",2,"Divide mass by volume.",phase=SUB,done="That is 2.0 g/cm³."),
   box("Check: 2 × 250 = ",500,"Multiply density by volume.",done="Back to the mass, so 2.0 g/cm³ is right."),
   say("So the density is <strong>2.0 g/cm³</strong>.")],
3:[say("After each half-life the count rate halves. Here it is one half-life."),
   box("Number of half-lives = ",1,"The question says after one half-life."),
   box("Halve once: 800 ÷ 2 = ",400,"Divide by 2.",phase=SUB,done="That is 400 Bq."),
   box("Check: 400 × 2 = ",800,"Double it back.",done="Doubling returns 800, so 400 Bq is right."),
   say("So the count rate is <strong>400 Bq</strong>.")],
4:[say("Find how many half-lives fit in the time, then halve that many times."),
   box("n = 15 ÷ 5 = ",3,"Total time ÷ half-life."),
   box("Halve once: 320 ÷ 2 = ",160,"Divide by 2.",phase=SUB),
   box("Halve again: 160 ÷ 2 = ",80,"Divide by 2."),
   box("Halve a third time: 80 ÷ 2 = ",40,"Divide by 2.",done="Three halvings for n = 3."),
   box("Check: 40 × 8 = ",320,"40 × 2³.",done="Back to the start 320 Bq, so 40 Bq is right."),
   say("So the activity is <strong>40 Bq</strong>.")],
5:[say("Rearrange v = fλ to λ = v ÷ f."),
   box("Speed v (m/s) = ",300000000,"3 × 10⁸ m/s."),
   box("Frequency f (Hz) = ",100000000,"100 MHz = 1 × 10⁸ Hz."),
   box("λ = v ÷ f = 300000000 ÷ 100000000 = ",3,"Divide speed by frequency.",phase=SUB,done="That is 3 m."),
   box("Check: 3 × 100000000 = ",300000000,"Multiply back by the frequency.",done="Back to the speed, so 3 m is right."),
   say("So the wavelength is <strong>3 m</strong>.")],
6:[say("Units are already kg and m³, so ρ = m ÷ V gives kg/m³."),
   box("Mass m (kg) = ",7.8,"Read it from the question."),
   box("Volume V (m³) = ",0.001,"1.0 × 10⁻³ = 0.001."),
   box("ρ = m ÷ V = 7.8 ÷ 0.001 = ",7800,"Divide mass by volume.",phase=SUB,done="That is 7800 kg/m³."),
   box("Check: 7800 × 0.001 = ",7.8,"Multiply back by the volume.",done="Back to the mass, so 7800 kg/m³ is right."),
   say("So the density is <strong>7800 kg/m³</strong>.")],
7:[say("Find n, then halve n times."),
   box("n = 40 ÷ 10 = ",4,"Total time ÷ half-life."),
   box("Halve once: 3200 ÷ 2 = ",1600,"Divide by 2.",phase=SUB),
   box("Halve again: 1600 ÷ 2 = ",800,"Divide by 2."),
   box("800 ÷ 2 = ",400,"Divide by 2."),
   box("400 ÷ 2 = ",200,"Divide by 2.",done="Four halvings for n = 4."),
   box("Check: 200 × 16 = ",3200,"200 × 2⁴.",done="Back to the start 3200 Bq, so 200 Bq is right."),
   say("So the activity is <strong>200 Bq</strong>.")],
}
bronze_hint = {
0:"Multiply frequency by wavelength: v = fλ.",
1:"Rearrange to f = v ÷ λ, then divide.",
2:"Divide mass by volume: ρ = m ÷ V.",
3:"One half-life means halve the count once.",
4:"Find n = 15 ÷ 5, then halve that many times.",
5:"Rearrange to λ = v ÷ f, then divide.",
6:"Divide mass by volume; the volume is already in m³.",
7:"Find n = 40 ÷ 10, then halve that many times.",
}
bronze_mis = {
0:[m("wrong_formula","v = f × λ, so 50 × 6.8 = 340 m/s. Adding the two (50 + 6.8) is not the wave equation.",56.8,"committed f+lambda")],
1:[m("wrong_rearrange","f = v ÷ λ = (3 × 10⁸) ÷ 0.10 = 3 × 10⁹ Hz. Multiplying instead gives 3 × 10⁷ Hz, ten times too small.",30000000,"committed v x lambda")],
2:[m("inverse_error","ρ = m ÷ V = 500 ÷ 250 = 2.0 g/cm³. Dividing volume by mass (250 ÷ 500 = 0.5) is upside down.",0.5,"V/m")],
3:[m("wrong_formula","After one half-life the count halves: 800 ÷ 2 = 400 Bq. Leaving it at 800 forgets to halve.",800,"forgot to halve")],
4:[m("forgot_step","n = 15 ÷ 5 = 3 half-lives: 320 → 160 → 80 → 40 Bq. Stopping after two halvings leaves 80 Bq.",80,"stopped at n=2")],
5:[m("wrong_rearrange","λ = v ÷ f = (3 × 10⁸) ÷ (1 × 10⁸) = 3 m. Dividing f by v instead gives about 0.33 m, upside down.",0.33,"f/v")],
6:[m("inverse_error","ρ = m ÷ V = 7.8 ÷ 0.001 = 7800 kg/m³. Multiplying (7.8 × 0.001 = 0.0078) is the wrong operation.",0.0078,"m x V")],
7:[m("forgot_step","n = 40 ÷ 10 = 4 half-lives: 3200 → 1600 → 800 → 400 → 200 Bq. Stopping at three halvings leaves 400 Bq.",400,"stopped at n=3")],
}

silver_steps = {
0:[say("You are given the start and end activity. Count how many halvings link them, then divide the time by that count."),
   box("1000 ÷ 2 = ",500,"Divide by 2."),
   box("500 ÷ 2 = ",250,"Divide by 2."),
   box("250 ÷ 2 = ",125,"Divide by 2.",done="Reached 125 Bq."),
   box("Number of halvings counted, n = ",3,"How many times you divided by 2."),
   box("Half-life = total time ÷ n = 30 ÷ 3 = ",10,"Divide the time by the number of halvings.",phase=SUB,done="That is 10 days."),
   box("Check: 1000 ÷ 8 = ",125,"1000 ÷ 2³.",done="Gives the end activity 125 Bq, so a 10 day half-life is right."),
   say("So the half-life is <strong>10 days</strong>.")],
1:[say("The wavelength is in millimetres but the speed is in metres per second. Convert λ to metres first."),
   box("λ in metres: 0.15 ÷ 1000 = ",0.00015,"1 mm = 0.001 m, so divide by 1000."),
   box("f = v ÷ λ = 1500 ÷ 0.00015 = ",10000000,"Divide speed by the wavelength in metres.",phase=SUB,done="That is 10 000 000 Hz (10 MHz)."),
   box("Check: 10000000 × 0.00015 = ",1500,"Multiply back by the wavelength.",done="Back to the speed, so 10 000 000 Hz is right."),
   say("So the frequency is <strong>10 000 000 Hz</strong> (10 MHz).")],
2:[say("You want mass, so rearrange ρ = m ÷ V to m = ρ × V. Units g/cm³ and cm³ give grams."),
   box("Density ρ (g/cm³) = ",0.8,"Read it from the question."),
   box("Volume V (cm³) = ",500,"Read it from the question."),
   box("m = ρ × V = 0.80 × 500 = ",400,"Multiply density by volume.",phase=SUB,done="That is 400 g."),
   box("Check: 400 ÷ 500 = ",0.8,"Divide the mass back by the volume.",done="Gives back 0.80 g/cm³, so 400 g is right."),
   say("So the mass is <strong>400 g</strong>.")],
3:[say("25% is a quarter. Count how many halvings take you from 100% to 25%, then multiply by the half-life."),
   box("After 1 half-life: 100 ÷ 2 = ",50,"Half of 100."),
   box("After 2 half-lives: 50 ÷ 2 = ",25,"Half of 50.",done="Reached 25%."),
   box("Number of half-lives to reach 25%, n = ",2,"You halved twice."),
   box("Age = n × half-life = 2 × 5700 = ",11400,"Multiply the number of half-lives by 5700.",phase=SUB,done="That is 11 400 years."),
   box("Check: 100 ÷ 4 = ",25,"Two halvings is ÷ 4.",done="Gives 25%, so 11 400 years is right."),
   say("So the fossil is about <strong>11 400 years</strong> old.")],
4:[say("Density in kg/m³ needs the volume in m³. Convert cm³ to m³ first: divide by 1 000 000."),
   box("Volume in m³: 600 ÷ 1000000 = ",0.0006,"600 millionths = 0.0006."),
   box("ρ = m ÷ V = 1.62 ÷ 0.0006 = ",2700,"Divide mass by the volume in m³.",phase=SUB,done="That is 2700 kg/m³."),
   box("Check: 2700 × 0.0006 = ",1.62,"Multiply back by the volume.",done="Back to the mass 1.62 kg, so 2700 kg/m³ is right."),
   say("So the density is <strong>2700 kg/m³</strong>.")],
5:[say("Rearrange v = fλ to λ = v ÷ f. Watch out: dividing by 0.5 makes the answer bigger."),
   box("Speed v (m/s) = ",6000,"Read it from the question."),
   box("Frequency f (Hz) = ",0.5,"Read it from the question."),
   box("λ = v ÷ f = 6000 ÷ 0.5 = ",12000,"Dividing by 0.5 is the same as multiplying by 2.",phase=SUB,done="That is 12 000 m (12 km)."),
   box("Check: 12000 × 0.5 = ",6000,"Multiply back by the frequency.",done="Back to the speed, so 12 000 m is right."),
   say("So the wavelength is <strong>12 000 m</strong> (12 km).")],
}
silver_hint = {
0:"Count the halvings from 1000 to 125, then divide 30 by that count.",
1:"Convert 0.15 mm to metres first, then f = v ÷ λ.",
2:"Rearrange to m = ρ × V, then multiply.",
3:"25% is 2 half-lives; multiply 2 by the half-life.",
4:"Convert 600 cm³ to m³ (÷ 1 000 000), then ρ = m ÷ V.",
5:"Rearrange to λ = v ÷ f; dividing by 0.5 makes it bigger.",
}
silver_mis = {
0:[m("forgot_step","1000 → 500 → 250 → 125 is 3 halvings, so half-life = 30 ÷ 3 = 10 days. Dividing 30 by the activity ratio 8 gives 3.75, which is wrong.",3.75,"30 / ratio")],
1:[m("unit_error","Convert first: 0.15 mm = 0.00015 m, so f = 1500 ÷ 0.00015 = 10 000 000 Hz. Forgetting to convert gives 1500 ÷ 0.15 = 10 000 Hz, a thousand times too small.",10000,"no mm to m")],
2:[m("inverse_error","m = ρ × V = 0.80 × 500 = 400 g. Dividing instead (500 ÷ 0.80 = 625) is the wrong way round.",625,"V/rho")],
3:[m("forgot_step","25% is a quarter: 100% → 50% → 25% is 2 half-lives, so age = 2 × 5700 = 11 400 years. Using one half-life gives 5700 years.",5700,"n=1 not 2")],
4:[m("unit_error","Convert 600 cm³ to 0.0006 m³ first, so ρ = 1.62 ÷ 0.0006 = 2700 kg/m³. Skipping the conversion gives 1.62 ÷ 600 = 0.0027, far too small.",0.0027,"no cm3 to m3")],
5:[m("wrong_rearrange","λ = v ÷ f = 6000 ÷ 0.5 = 12 000 m. Multiplying instead (6000 × 0.5 = 3000) is wrong; dividing by 0.5 must make it bigger.",3000,"v x f")],
}

gold_steps = {
0:[say("The activity drops from 5400 Bq to 675 Bq. Count the halvings, then divide the time by that count."),
   box("5400 ÷ 2 = ",2700,"Divide by 2."),
   box("2700 ÷ 2 = ",1350,"Divide by 2."),
   box("1350 ÷ 2 = ",675,"Divide by 2.",done="Reached 675 Bq."),
   box("Number of halvings, n = ",3,"How many times you divided by 2."),
   box("Half-life = 60 ÷ n = 60 ÷ 3 = ",20,"Total time ÷ number of halvings.",phase=SUB,done="That is 20 minutes."),
   box("Check: 5400 ÷ 8 = ",675,"5400 ÷ 2³.",done="Gives the end activity 675 Bq, so a 20 minute half-life is right."),
   say("So the half-life is <strong>20 minutes</strong>.")],
1:[say("Two steps. Turn the period into frequency with f = 1 ÷ T, then find the wavelength with λ = v ÷ f."),
   box("f = 1 ÷ T = 1 ÷ 8 = ",0.125,"One divided by the period."),
   box("λ = v ÷ f = 15 ÷ 0.125 = ",120,"Divide speed by frequency.",phase=SUB,done="That is 120 m."),
   box("Check another way, λ = v × T = 15 × 8 = ",120,"Speed times period.",done="Same 120 m, so the wavelength is right."),
   say("So (a) the frequency is 0.125 Hz and (b) the wavelength is <strong>120 m</strong>.")],
3:[say("Count how many times you halve 6400 to reach 50, then divide 96 by that number."),
   box("6400 ÷ 2 = ",3200,"Divide by 2."),
   box("Keep halving to 50 (6400 → 3200 → 1600 → 800 → 400 → 200 → 100 → 50). Number of halvings, n = ",7,"Count the steps from 6400 down to 50."),
   box("Half-life = 96 ÷ n = 96 ÷ 7 = ",13.7,"Divide 96 by 7 and round to 1 d.p.",phase=SUB,done="96 ÷ 7 = 13.714..., so 13.7 minutes."),
   box("Check n: 6400 ÷ 128 = ",50,"128 = 2⁷.",done="Gives the end activity 50 Bq, so n = 7 and 13.7 min is right."),
   say("So the half-life is <strong>13.7 minutes</strong>.")],
4:[say("Frequency f = v ÷ λ. Handle the powers of ten separately from the front numbers."),
   box("Divide the front numbers: 3.0 ÷ 1.0 = ",3,"3.0 divided by 1.0."),
   box("Subtract the powers: 8 − (−10) = ",18,"8 minus negative 10 is 8 + 10.",done="So f = 3.0 × 10¹⁸ Hz."),
   box("The answer is 3.0 × 10¹⁸ Hz. Enter the coefficient = ",3,"The number in front of × 10¹⁸.",phase=SUB,done="The coefficient is 3.0."),
   box("Check the power: 8 + 10 = ",18,"Confirms the exponent.",done="10¹⁸ confirms f = 3.0 × 10¹⁸ Hz."),
   say("So the frequency is <strong>3.0 × 10¹⁸ Hz</strong>.")],
}
gold_hint = {
0:"Count the halvings from 5400 to 675, then divide 60 by that count.",
1:"Find f = 1 ÷ T first, then λ = v ÷ f.",
2:"Density uses the total outer volume, including the hollow space: ρ = m ÷ V.",
3:"Count how many halvings reach 50, then half-life = 96 ÷ that count.",
4:"f = v ÷ λ; divide the front numbers and subtract the powers of ten.",
5:"Find how many half-lives fit in 12 hours, then the fraction left.",
}
gold_mis = {
0:[m("forgot_step","5400 → 2700 → 1350 → 675 is 3 halvings, so half-life = 60 ÷ 3 = 20 minutes. Dividing 60 by the ratio 8 gives 7.5, which is wrong.",7.5,"60 / ratio")],
1:[m("forgot_step","First f = 1 ÷ T = 1 ÷ 8 = 0.125 Hz, then λ = v ÷ f = 15 ÷ 0.125 = 120 m. Using the period as the frequency (15 ÷ 8) gives about 1.9 m.",1.875,"used T as f")],
2:[m("wrong_formula","ρ = 250 ÷ 120 = 2.1 g/cm³. This is below solid steel (7.8) because the outer volume includes the hollow air space, not just steel.",None,"MC")],
3:[m("forgot_step","6400 halves 7 times to reach 50 (6400 ÷ 128 = 50), so half-life = 96 ÷ 7 = 13.7 minutes. Using 6 halvings gives 96 ÷ 6 = 16 minutes.",16,"n=6 not 7")],
4:[m("wrong_rearrange","f = v ÷ λ = (3.0 × 10⁸) ÷ (1.0 × 10⁻¹⁰) = 3.0 × 10¹⁸ Hz, so the coefficient is 3.0. A power slip changes the exponent, not the coefficient.",None,"coefficient unchanged")],
5:[m("forgot_step","n = 12 ÷ 6 = 2 half-lives, leaving (½)² = ¼ = 25%. Exactly 25% remains, just meeting the threshold, so the sample is usable.",None,"MC")],
}

def apply(tier_list, steps_map, hint_map, mis_map):
    for i, p in enumerate(tier_list):
        # fix any svg in the question / display fields
        for f in ("question", "display"):
            if f in p:
                p[f] = fix_svg(p[f])
        p["hint"] = hint_map[i]
        p["misconceptions"] = mis_map[i]
        if p.get("input_type") != "multiple_choice" and i in steps_map:
            p["guided_steps"] = steps_map[i]

apply(pb["bronze"], bronze_steps, bronze_hint, bronze_mis)
apply(pb["silver"], silver_steps, silver_hint, silver_mis)
apply(pb["gold"], gold_steps, gold_hint, gold_mis)

# ---------- 6. TIER GUIDES ----------
def exs(q, steps):
    return {"question": q, "steps": steps}
def gstep(label, content, ans=False):
    d = {"label": label, "content": content}
    if ans: d["isAnswer"] = True; d["is_answer"] = True
    return d

pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one equation, units already right",
   "steps": [
     "Pick the equation: v = fλ for waves, ρ = m ÷ V for density, or halve the activity for half-life.",
     "Check the units are the base ones, then substitute the two known values straight in.",
     "State the answer with its unit: m/s, kg/m³ or Bq."
   ],
   "example": exs("A wave has frequency 25 Hz and wavelength 8 m. Find the wave speed.", [
     gstep("Multiply","<p>v = fλ = 25 × 8 = 200 m/s</p>"),
     gstep("Check","<p>200 ÷ 8 = 25 Hz ✓</p>"),
     gstep("Answer","<p><strong>200 m/s</strong></p>",True)
   ])
 },
 "silver": {
   "title": "Silver: convert units or rearrange first",
   "steps": [
     "If a length is in mm or a volume in cm³, convert to metres or m³ before substituting.",
     "If the unknown is not the subject, rearrange first: m = ρV, λ = v ÷ f, or f = v ÷ λ.",
     "For a half-life from data, count how many times the activity halves, then divide the time by that count."
   ],
   "example": exs("A stone has mass 1.5 kg and volume 500 cm³. Find its density in kg/m³.", [
     gstep("Convert","<p>500 cm³ = 500 ÷ 1 000 000 = 0.0005 m³</p>"),
     gstep("Divide","<p>ρ = m ÷ V = 1.5 ÷ 0.0005 = 3000 kg/m³</p>"),
     gstep("Check","<p>3000 × 0.0005 = 1.5 kg ✓</p>"),
     gstep("Answer","<p><strong>3000 kg/m³</strong></p>",True)
   ])
 },
 "gold": {
   "title": "Gold: chain two steps or read the data",
   "steps": [
     "Multi-step waves: turn the period into frequency with f = 1 ÷ T, then use v = fλ.",
     "Half-life from data: find how many halvings link the start and end activity, then half-life = time ÷ that number.",
     "Always finish with a check and the correct unit."
   ],
   "example": exs("A source falls from 4000 Bq to 500 Bq in 30 hours. Find the half-life.", [
     gstep("Count halvings","<p>4000 → 2000 → 1000 → 500 is 3 halvings</p>"),
     gstep("Divide","<p>half-life = 30 ÷ 3 = 10 hours</p>"),
     gstep("Check","<p>4000 ÷ 2³ = 4000 ÷ 8 = 500 Bq ✓</p>"),
     gstep("Answer","<p><strong>10 hours</strong></p>",True)
   ])
 }
}

# ---------- 7. GUIDED (opener + teach) ----------
pd["guided"] = {
 "opener": {
   "label": "Before any physics",
   "display": "A tiny steel nail sinks in water at once. Yet a steel supertanker, thousands of tonnes of the same steel, floats.<br>Two blocks help explain it. A wood block and a steel block are the same size (both 100 cm³). The wood weighs 60 g; the steel weighs 780 g.",
   "steps": [
     {"say": "No equations yet, just judgement. Same size, so which block has more mass crammed into that space?",
      "pre": "Heavier block, mass in g = ", "post": "", "answer": 780, "hint": "Compare 60 g and 780 g."},
     {"say": "Now compare how much more is packed into the same space.",
      "pre": "How many times more mass? 780 ÷ 60 = ", "post": "", "answer": 13, "hint": "Divide 780 by 60."},
     {"say": "That 'mass packed into a space' is <strong>density</strong>: ρ = m ÷ V. Steel is 13 times denser than this wood. A ship floats by spreading its steel around a huge hollow volume, dropping its overall density below water's. Today: density ρ = m ÷ V, the wave equation v = fλ (both 'how much per unit'), and half-life (repeated halving)."}
   ]
 },
 "teach": {
   "bronze": {
     "label": "One equation, straight in",
     "display": "A wave has frequency 20 Hz and wavelength 4 m. Find the wave speed.",
     "steps": [
       {"say": "One equation: v = fλ. Both values are already in the right units, so go straight in."},
       {"pre": "Frequency f (Hz) = ", "post": "", "answer": 20, "hint": "Given in the question."},
       {"pre": "Wavelength λ (m) = ", "post": "", "answer": 4, "hint": "Given in the question."},
       {"pre": "v = f × λ = 20 × 4 = ", "post": "", "answer": 80, "hint": "Multiply frequency by wavelength."},
       {"pre": "Check: 80 ÷ 4 = ", "post": "", "answer": 20, "done": "Gives back 20 Hz, so 80 m/s is right.", "hint": "Divide the speed by the wavelength."},
       {"say": "So the wave speed is <strong>80 m/s</strong>."}
     ]
   },
   "silver": {
     "label": "Convert the unit, then divide",
     "display": "A metal cube has mass 2.4 kg and volume 300 cm³. Find its density in kg/m³.",
     "steps": [
       {"say": "Volume is in cm³ but density in kg/m³ needs m³. Convert first: 1 cm³ = 0.000001 m³."},
       {"pre": "300 cm³ in m³ = 300 × 0.000001 = ", "post": "", "answer": 0.0003, "hint": "300 millionths = 0.0003."},
       {"pre": "Density ρ = m ÷ V = 2.4 ÷ 0.0003 = ", "post": "", "answer": 8000, "hint": "Divide mass by the volume in m³."},
       {"pre": "Sense check against water (1000 kg/m³): 8000 ÷ 1000 = ", "post": "", "answer": 8, "hint": "Divide by 1000."},
       {"pre": "Reverse check: 8000 × 0.0003 = ", "post": "", "answer": 2.4, "done": "Back to 2.4 kg, so 8000 kg/m³ is right.", "hint": "Multiply density by volume."},
       {"say": "So the density is <strong>8000 kg/m³</strong>, about 8 times water, which is right for a metal."}
     ]
   },
   "gold": {
     "label": "Chain two wave steps",
     "display": "A wave has speed 20 m/s and period 4 s. Find its wavelength.",
     "steps": [
       {"say": "Two steps. The period is time per wave; first turn it into frequency with f = 1 ÷ T, then use λ = v ÷ f."},
       {"pre": "f = 1 ÷ T = 1 ÷ 4 = ", "post": "", "answer": 0.25, "hint": "One divided by the period."},
       {"pre": "λ = v ÷ f = 20 ÷ 0.25 = ", "post": "", "answer": 80, "hint": "Divide speed by frequency."},
       {"pre": "Same as multiplying by 4: 20 × 4 = ", "post": "", "answer": 80, "done": "Same answer, 80 m, so it checks.", "hint": "Dividing by 0.25 is multiplying by 4."},
       {"pre": "Check v = fλ: 0.25 × 80 = ", "post": "", "answer": 20, "done": "Gives back 20 m/s, so λ = 80 m is right.", "hint": "Multiply frequency by wavelength."},
       {"say": "So the wavelength is <strong>80 m</strong>."}
     ]
   }
 }
}

# ---------- 8. FINAL EM-DASH SWEEP (preserved fields: MC options, worked_examples, hints) ----------
def dedash(o):
    if isinstance(o, dict):
        return {k: (v if k in ("note",) else dedash(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [dedash(v) for v in o]
    if isinstance(o, str):
        return o.replace(" — ", ": ").replace("—", ": ")
    return o
pd = dedash(pd)

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("WROTE", OUT)
