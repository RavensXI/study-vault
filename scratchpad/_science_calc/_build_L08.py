# -*- coding: utf-8 -*-
"""Build guided practice_data for physics-calculations-L08
Newton's Laws, Momentum and Waves. Board-neutral (AQA+Edexcel+OCR share)."""
import json, io

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {}
    if say is not None: d["say"] = say
    d["pre"] = pre
    d["post"] = post
    d["answer"] = answer
    d["hint"] = hint
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

def mc(pattern, message, expect):
    return {"pattern": pattern, "check": "common", "message": message, "expect": expect}

# ---------------- METHOD CARD (slim) ----------------
method_card = {
    "title": "Newton's Laws, Momentum and Waves",
    "steps": [
        "Pick the equation the question points to: \\(F = ma\\), \\(p = mv\\), \\(v = f\\lambda\\) or \\(T = 1/f\\).",
        "Convert to base units first: grams to kilograms, kHz to Hz, cm to metres.",
        "For \\(F = ma\\) use the resultant force (driving force minus friction or weight).",
        "Substitute, calculate, state the unit; use standard form for very large or small numbers."
    ],
    "content": (
        "<p><strong>Newton's second law</strong> \\(F = ma\\) always uses the "
        "<strong>resultant</strong> force. If friction or weight acts, subtract it from the "
        "driving force first. Constant velocity means the resultant force is zero.</p>"
        "<p><strong>Momentum</strong> \\(p = mv\\) is conserved in collisions: total before "
        "equals total after. It is higher tier only.</p>"
        "<p><strong>Waves:</strong> \\(v = f\\lambda\\), and period \\(T = 1/f\\). Convert "
        "frequency to hertz and lengths to metres before substituting. Check whether your "
        "board gives you the period equation.</p>"
    )
}

exam_context = {
    "marks": "3 to 6 per calculation",
    "paper": "Paper 1 (Physics)",
    "frequency": ("Very high. Force and wave calculations appear almost every year. "
                  "Momentum is higher tier only but frequently tested.")
}

# ---------------- BRONZE ----------------
bronze = []

bronze.append({
    "unit": "m/s²", "display": "A resultant force of 240 N acts on an 80 kg trolley. Calculate its acceleration.",
    "solutions": [3], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "\\(F = ma\\)",
    "hint": "Rearrange F = ma to a = F ÷ m, then divide.",
    "misconceptions": [mc("inverse_error",
        "a = F ÷ m = 240 ÷ 80 = 3 m/s². Multiplying (240 × 80) is the slip.", 19200)],
    "guided_steps": [
        box("Resultant force F in newtons = ", 240, "Read it straight from the question.",
            say="The equation is \\(F = ma\\). We want the acceleration, so rearrange to \\(a = F \\div m\\)."),
        box("Mass m in kilograms = ", 80, "It is already in kg, no conversion needed."),
        box("a = 240 ÷ 80 = ", 3, "240 shared into 80 equal parts.", say="Now divide.", phase="substitute"),
        box("Check: does F = m × a? 80 × 3 = ", 240, "Multiply mass by your acceleration.",
            done="It gives back 240 N, so a = 3 m/s²."),
    ]})

bronze.append({
    "unit": "N", "display": "Calculate the force needed to accelerate a 1500 kg car at 2 m/s².",
    "solutions": [3000], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "\\(F = ma\\)",
    "hint": "F = ma. Multiply mass by acceleration.",
    "misconceptions": [mc("inverse_error",
        "F = ma = 1500 × 2 = 3000 N. Dividing (1500 ÷ 2 = 750) is the slip; here you multiply.", 750)],
    "guided_steps": [
        box("Mass m in kilograms = ", 1500, "Straight from the question.",
            say="The equation is \\(F = ma\\). Force is the subject already, so no rearranging."),
        box("Acceleration a in m/s² = ", 2, "Straight from the question."),
        box("F = 1500 × 2 = ", 3000, "Mass times acceleration.", say="Multiply.", phase="substitute"),
        box("Check: a = F ÷ m = 3000 ÷ 1500 = ", 2, "Divide your force by the mass.",
            done="Back to 2 m/s², so F = 3000 N."),
    ]})

bronze.append({
    "unit": "m/s", "display": "A wave has a frequency of 500 Hz and a wavelength of 0.68 m. Calculate its speed.",
    "solutions": [340], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "\\(v = f\\lambda\\)",
    "hint": "v = f × λ. Multiply frequency by wavelength.",
    "misconceptions": [mc("inverse_error",
        "v = f × λ = 500 × 0.68 = 340 m/s. Dividing (500 ÷ 0.68) gives about 735, but here you multiply.", 735.29)],
    "guided_steps": [
        box("Frequency f in hertz = ", 500, "Straight from the question.",
            say="The equation is \\(v = f\\lambda\\): speed equals frequency times wavelength."),
        box("Wavelength λ in metres = ", 0.68, "Already in metres."),
        box("v = 500 × 0.68 = ", 340, "Frequency times wavelength.", say="Multiply.", phase="substitute"),
        box("Check: f = v ÷ λ = 340 ÷ 0.68 = ", 500, "Divide your speed by the wavelength.",
            done="Back to 500 Hz, so v = 340 m/s."),
    ]})

bronze.append({
    "unit": "Hz", "display": "A water wave has a speed of 2 m/s and a wavelength of 0.5 m. Calculate its frequency.",
    "solutions": [4], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "\\(v = f\\lambda\\)",
    "hint": "Rearrange v = fλ to f = v ÷ λ.",
    "misconceptions": [mc("inverse_error",
        "f = v ÷ λ = 2 ÷ 0.5 = 4 Hz. Multiplying (2 × 0.5 = 1) is the slip.", 1)],
    "guided_steps": [
        box("Speed v in m/s = ", 2, "Straight from the question.",
            say="The equation is \\(v = f\\lambda\\). We want frequency, so rearrange to \\(f = v \\div \\lambda\\)."),
        box("Wavelength λ in metres = ", 0.5, "Already in metres."),
        box("f = 2 ÷ 0.5 = ", 4, "How many 0.5s fit into 2?", say="Divide.", phase="substitute"),
        box("Check: v = f × λ = 4 × 0.5 = ", 2, "Multiply your frequency by the wavelength.",
            done="Back to 2 m/s, so f = 4 Hz."),
    ]})

bronze.append({
    "unit": "m/s²", "display": "A 10 N force accelerates a 2 kg object. Calculate the acceleration.",
    "solutions": [5], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "\\(F = ma\\)",
    "hint": "a = F ÷ m. Divide force by mass.",
    "misconceptions": [mc("inverse_error",
        "a = F ÷ m = 10 ÷ 2 = 5 m/s². Multiplying (10 × 2 = 20) is the slip.", 20)],
    "guided_steps": [
        box("Force F in newtons = ", 10, "Straight from the question.",
            say="The equation is \\(F = ma\\). We want acceleration, so \\(a = F \\div m\\)."),
        box("Mass m in kilograms = ", 2, "Already in kg."),
        box("a = 10 ÷ 2 = ", 5, "10 shared into 2 equal parts.", say="Divide.", phase="substitute"),
        box("Check: F = m × a = 2 × 5 = ", 10, "Multiply mass by your acceleration.",
            done="Back to 10 N, so a = 5 m/s²."),
    ]})

bronze.append({
    "unit": "s", "display": "A wave has a frequency of 200 Hz. Calculate its period.",
    "solutions": [0.005], "accept": 0.0001, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "Given on equation sheet: \\(T = \\frac{1}{f}\\)",
    "hint": "Period T = 1 ÷ frequency.",
    "misconceptions": [mc("inverse_error",
        "T = 1 ÷ f = 1 ÷ 200 = 0.005 s. Period and frequency are reciprocals; the answer is not 200.", 200)],
    "guided_steps": [
        box("Frequency f in hertz = ", 200, "Straight from the question.",
            say="Period and frequency are reciprocals: \\(T = 1 \\div f\\)."),
        box("T = 1 ÷ 200 = ", 0.005, "1 shared into 200 equal parts is a small decimal.",
            say="Divide 1 by the frequency.", phase="substitute"),
        box("Check: f = 1 ÷ T = 1 ÷ 0.005 = ", 200, "Divide 1 by your period.",
            done="Back to 200 Hz, so T = 0.005 s."),
    ]})

bronze.append({
    "display": "Which equation links force, mass and acceleration?",
    "options": ["\\(p = mv\\)", "\\(F = ma\\)", "\\(v = f\\lambda\\)", "\\(W = mg\\)"],
    "solutions": [1], "calculator": False, "input_type": "multiple_choice", "higher_only": False,
    "hint": "Newton's second law relates force, mass and acceleration.",
    "misconceptions": [mc("wrong_equation",
        "Newton's second law: F = ma. p = mv is momentum, v = fλ is wave speed, W = mg is weight.", None)],
})

bronze.append({
    "unit": "m", "display": "A wave has a speed of 330 m/s and a frequency of 660 Hz. Calculate the wavelength.",
    "solutions": [0.5], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "\\(v = f\\lambda\\)",
    "hint": "Rearrange v = fλ to λ = v ÷ f.",
    "misconceptions": [mc("inverse_error",
        "λ = v ÷ f = 330 ÷ 660 = 0.5 m. Dividing the wrong way (660 ÷ 330 = 2) is the slip.", 2)],
    "guided_steps": [
        box("Speed v in m/s = ", 330, "Straight from the question.",
            say="The equation is \\(v = f\\lambda\\). We want wavelength, so \\(\\lambda = v \\div f\\)."),
        box("Frequency f in hertz = ", 660, "Already in Hz."),
        box("λ = 330 ÷ 660 = ", 0.5, "330 is exactly half of 660.", say="Divide.", phase="substitute"),
        box("Check: v = f × λ = 660 × 0.5 = ", 330, "Multiply frequency by your wavelength.",
            done="Back to 330 m/s, so λ = 0.5 m."),
    ]})

# ---------------- SILVER ----------------
silver = []

silver.append({
    "unit": "m/s²", "display": "A car has a driving force of 3500 N and a friction force of 500 N. Its mass is 1200 kg. Calculate its acceleration.",
    "solutions": [2.5], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "\\(F = ma\\)",
    "hint": "Find the resultant force (driving minus friction) first, then a = F ÷ m.",
    "misconceptions": [
        mc("forgot_step", "Use the resultant force, not the driving force. Resultant = 3500 − 500 = 3000 N, so a = 3000 ÷ 1200 = 2.5 m/s². Using 3500 N gives about 2.92.", 2.92),
        mc("inverse_error", "Divide the resultant by the mass: a = 3000 ÷ 1200 = 2.5 m/s², not 1200 ÷ 3000.", 0.4)],
    "guided_steps": [
        box("Resultant force = 3500 − 500 = ", 3000, "Take the friction off the driving force.",
            say="First find the resultant force: driving force minus friction."),
        box("Mass m in kilograms = ", 1200, "Already in kg."),
        box("a = 3000 ÷ 1200 = ", 2.5, "3000 shared into 1200 equal parts.",
            say="Now \\(a = F \\div m\\) with the resultant force.", phase="substitute"),
        box("Check: F = m × a = 1200 × 2.5 = ", 3000, "Multiply mass by your acceleration.",
            done="Back to 3000 N, so a = 2.5 m/s²."),
    ]})

silver.append({
    "unit": "m/s", "display": "A sound wave has a frequency of 2 kHz and a wavelength of 17 cm. Calculate the speed of sound.",
    "solutions": [340], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "\\(v = f\\lambda\\)",
    "hint": "Convert to Hz and metres first, then v = f × λ.",
    "misconceptions": [mc("unit_error",
        "Convert 17 cm to 0.17 m first. v = 2000 × 0.17 = 340 m/s. Leaving it as 17 gives 34000.", 34000)],
    "guided_steps": [
        box("2 kHz in hertz = 2 × 1000 = ", 2000, "Kilo means times 1000.",
            say="Convert to base units first. \\(v = f\\lambda\\) needs hertz and metres."),
        box("17 cm in metres = 17 ÷ 100 = ", 0.17, "100 centimetres in a metre."),
        box("v = 2000 × 0.17 = ", 340, "Frequency times wavelength.", say="Now multiply.", phase="substitute"),
        box("Check: f = v ÷ λ = 340 ÷ 0.17 = ", 2000, "Divide your speed by the wavelength.",
            done="Back to 2000 Hz, so v = 340 m/s."),
    ]})

silver.append({
    "unit": "m/s²", "display": "A 500 g toy car is pushed with a force of 4 N. Friction is 2 N. Calculate its acceleration.",
    "solutions": [4], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "\\(F = ma\\)",
    "hint": "Convert grams to kg, subtract friction for the resultant, then a = F ÷ m.",
    "misconceptions": [
        mc("unit_error", "Convert 500 g to 0.5 kg. Resultant = 4 − 2 = 2 N, so a = 2 ÷ 0.5 = 4 m/s². Using 500 kg gives 0.004.", 0.004),
        mc("forgot_step", "Subtract friction first: resultant = 4 − 2 = 2 N, then a = 2 ÷ 0.5 = 4 m/s². Using 4 N gives 8.", 8)],
    "guided_steps": [
        box("500 g in kilograms = 500 ÷ 1000 = ", 0.5, "1000 grams in a kilogram.",
            say="Convert the mass, then find the resultant force."),
        box("Resultant force = 4 − 2 = ", 2, "Take the friction off the push."),
        box("a = 2 ÷ 0.5 = ", 4, "How many halves fit into 2?", say="Now \\(a = F \\div m\\).", phase="substitute"),
        box("Check: F = m × a = 0.5 × 4 = ", 2, "Multiply mass by your acceleration.",
            done="Back to 2 N, so a = 4 m/s²."),
    ]})

silver.append({
    "unit": "m/s", "display": "A moving object of mass 4 kg has a momentum of 20 kg m/s. Calculate its velocity.",
    "solutions": [5], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": True, "equation_hint": "\\(p = mv\\)",
    "hint": "Rearrange p = mv to v = p ÷ m.",
    "misconceptions": [mc("inverse_error",
        "v = p ÷ m = 20 ÷ 4 = 5 m/s. Multiplying (20 × 4 = 80) is the slip.", 80)],
    "guided_steps": [
        box("Momentum p in kg m/s = ", 20, "Straight from the question.",
            say="The equation is \\(p = mv\\). We want velocity, so \\(v = p \\div m\\)."),
        box("Mass m in kilograms = ", 4, "Already in kg."),
        box("v = 20 ÷ 4 = ", 5, "20 shared into 4 equal parts.", say="Divide.", phase="substitute"),
        box("Check: p = m × v = 4 × 5 = ", 20, "Multiply mass by your velocity.",
            done="Back to 20 kg m/s, so v = 5 m/s."),
    ]})

silver.append({
    "unit": "m", "accept": 0.005,
    "display": "A microwave has a frequency of 2.45 GHz. The speed of EM waves is \\(3 \\times 10^8\\) m/s. Calculate the wavelength. Give your answer to 2 significant figures.",
    "solutions": [0.12], "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "\\(v = f\\lambda\\)",
    "hint": "Convert GHz to Hz (× 10⁹), then λ = v ÷ f.",
    "misconceptions": [mc("unit_error",
        "2.45 GHz = 2.45 × 10⁹ Hz. λ = v ÷ f = (3 × 10⁸) ÷ (2.45 × 10⁹) = 0.12 m. Dividing the other way gives about 8.2.", 8.17)],
    "guided_steps": [
        box("2.45 GHz written as 2.45 × 10ⁿ hertz: the power n = ", 9, "Giga means times a thousand million, 10⁹.",
            say="The equation is \\(v = f\\lambda\\). We want wavelength, so \\(\\lambda = v \\div f\\). First convert GHz."),
        box("Now the numbers: 3 ÷ 2.45 = ", 1.22, "To 2 decimal places."),
        box("10⁸ ÷ 10⁹ = 10ⁿ, so n = ", -1, "Subtract the powers: 8 − 9.", say="Now the powers of ten.", phase="substitute"),
        box("So λ = 1.22 × 10⁻¹ = ", 0.12, "Move the decimal one place left. To 2 d.p."),
        sayonly("The wavelength is <strong>0.12 m</strong>, about 12 cm."),
    ]})

silver.append({
    "unit": "m", "display": "A wave has a period of 0.02 s. Calculate its frequency, then find the wavelength if the wave speed is 5 m/s.",
    "solutions": [0.1], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "Given on equation sheet: \\(T = \\frac{1}{f}\\), then \\(v = f\\lambda\\)",
    "hint": "Find frequency (f = 1 ÷ T) first, then λ = v ÷ f.",
    "misconceptions": [mc("forgot_step",
        "f = 1 ÷ 0.02 = 50 Hz, then λ = 5 ÷ 50 = 0.1 m. Stopping at 50 gives the frequency, not the wavelength.", 50)],
    "guided_steps": [
        box("f = 1 ÷ 0.02 = ", 50, "1 shared into 0.02 is large.",
            say="Two steps. First frequency from the period: \\(f = 1 \\div T\\)."),
        box("λ = 5 ÷ 50 = ", 0.1, "5 shared into 50 equal parts.",
            say="Now the wavelength: \\(\\lambda = v \\div f\\).", phase="substitute"),
        box("Check: v = f × λ = 50 × 0.1 = ", 5, "Multiply frequency by your wavelength.",
            done="Back to 5 m/s, so λ = 0.1 m."),
    ]})

# ---------------- GOLD ----------------
gold = []

gold.append({
    "unit": "m/s", "display": "A 3 kg trolley moving at 4 m/s collides with a stationary 1 kg trolley. They stick together and move off. Calculate the velocity after the collision.",
    "solutions": [3], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": True, "equation_hint": "\\(p = mv\\)",
    "hint": "Total momentum before = total momentum after; divide by the combined mass.",
    "misconceptions": [mc("forgot_step",
        "After they stick, combined mass = 3 + 1 = 4 kg. v = 12 ÷ 4 = 3 m/s. Using only 3 kg gives 4.", 4)],
    "guided_steps": [
        box("Momentum before = 3 × 4 = ", 12, "Only the moving trolley has momentum.",
            say="Momentum is conserved: total \\(mv\\) before equals total after. Find the momentum before."),
        box("After they stick, the combined mass = 3 + 1 = ", 4, "Both trolleys move together now."),
        box("v = 12 ÷ 4 = ", 3, "12 shared into 4 equal parts.",
            say="That 12 kg m/s is shared by 4 kg. \\(v = p \\div m\\).", phase="substitute"),
        box("Check: momentum after = 4 × 3 = ", 12, "Combined mass times your velocity.",
            done="Matches the 12 kg m/s before, so v = 3 m/s."),
    ]})

gold.append({
    "unit": "m/s", "accept": 0.1,
    "display": "A 0.05 kg bullet is fired at 400 m/s into a 2.95 kg block of wood on a frictionless surface. The bullet embeds in the block. Calculate the velocity of the block and bullet after the collision.",
    "solutions": [6.67], "calculator": True, "input_type": "single_value",
    "higher_only": True, "equation_hint": "\\(p = mv\\)",
    "hint": "Momentum before = bullet only; divide by the total mass after.",
    "misconceptions": [mc("forgot_step",
        "Total mass after = 0.05 + 2.95 = 3 kg. v = 20 ÷ 3 = 6.67 m/s. Using only 2.95 kg gives 6.78.", 6.78)],
    "guided_steps": [
        box("Momentum before = 0.05 × 400 = ", 20, "Only the bullet is moving.",
            say="Momentum is conserved. The bullet carries all the momentum before."),
        box("Total mass after = 0.05 + 2.95 = ", 3, "Bullet plus block, now stuck together."),
        box("v = 20 ÷ 3 = ", 6.67, "To 2 decimal places.",
            say="That 20 kg m/s is shared by 3 kg. \\(v = p \\div m\\).", phase="substitute"),
        box("Check: total mass = p ÷ v = 20 ÷ 6.67 = ", 3, "Momentum divided by your velocity. Round to the nearest whole.",
            done="Back to 3 kg, so v = 6.67 m/s."),
    ]})

gold.append({
    "unit": "m/s²", "display": "A rocket of mass 500 kg fires its engines, producing a thrust of 8000 N. Its weight is 4900 N. Calculate the resultant force and the acceleration.",
    "solutions": [6.2], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "\\(F = ma\\)",
    "hint": "Resultant force = thrust − weight, then a = F ÷ m.",
    "misconceptions": [mc("forgot_step",
        "Resultant = thrust − weight = 8000 − 4900 = 3100 N. a = 3100 ÷ 500 = 6.2 m/s². Using 8000 N gives 16.", 16)],
    "guided_steps": [
        box("Resultant force = 8000 − 4900 = ", 3100, "Weight pulls down, so subtract it.",
            say="Find the resultant force: thrust up minus weight down."),
        box("Mass m in kilograms = ", 500, "Straight from the question."),
        box("a = 3100 ÷ 500 = ", 6.2, "3100 shared into 500 equal parts.",
            say="Now \\(a = F \\div m\\).", phase="substitute"),
        box("Check: F = m × a = 500 × 6.2 = ", 3100, "Mass times your acceleration.",
            done="Back to 3100 N, so a = 6.2 m/s²."),
    ]})

gold.append({
    "display": "A radio station broadcasts at 98.5 MHz. The speed of radio waves is \\(3 \\times 10^8\\) m/s. Calculate the wavelength in standard form.",
    "solutions": [3.05, 0], "calculator": True, "input_type": "standard_form",
    "higher_only": False, "equation_hint": "\\(v = f\\lambda\\)",
    "hint": "Convert MHz to Hz (× 10⁶), then λ = v ÷ f; give the answer in standard form.",
    "misconceptions": [mc("unit_error",
        "98.5 MHz = 9.85 × 10⁷ Hz. λ = (3 × 10⁸) ÷ (9.85 × 10⁷) = 3.05 × 10⁰ m. Forgetting to convert MHz gives 3.05 × 10⁶.",
        [3.05, 6])],
    "guided_steps": [
        box("98.5 MHz = 98.5 × 10⁶ Hz. Written as A × 10⁷, A = ", 9.85, "Shift one place: 98.5 × 10⁶ = 9.85 × 10⁷.",
            say="The equation is \\(v = f\\lambda\\), rearranged to \\(\\lambda = v \\div f\\). Give the answer in standard form. First fix the frequency."),
        box("Now the numbers: 3 ÷ 9.85 = ", 0.305, "To 3 decimal places."),
        box("10⁸ ÷ 10⁷ = 10ⁿ, so n = ", 1, "Subtract the powers: 8 − 7.", say="Now the powers of ten.", phase="substitute"),
        box("So λ = 0.305 × 10¹ = ", 3.05, "Move the decimal one place right. To 2 d.p."),
        box("In standard form the number in front sits between 1 and 10. 3.05 already does, so λ = 3.05 × 10ⁿ, where n = ", 0,
            "3.05 needs no further shift, so the power is zero.",
            done="The wavelength is 3.05 m, written 3.05 × 10⁰ m."),
    ]})

gold.append({
    "unit": "N", "display": "A car of mass 1000 kg accelerates at 2 m/s² for 8 seconds. The driving force is 3200 N. Calculate the friction force acting on the car.",
    "solutions": [1200], "accept": 0.005, "calculator": True, "input_type": "single_value",
    "higher_only": False, "equation_hint": "\\(F = ma\\)",
    "hint": "Resultant = m × a, then friction = driving − resultant.",
    "misconceptions": [mc("wrong_rearrange",
        "Resultant = ma = 2000 N. Friction = driving − resultant = 3200 − 2000 = 1200 N. Adding gives 5200.", 5200)],
    "guided_steps": [
        box("Resultant force = 1000 × 2 = ", 2000, "Mass times acceleration. The 8 seconds is not needed.",
            say="First the resultant force from \\(F = ma\\)."),
        box("Driving force from the question = ", 3200, "Read it straight off."),
        box("friction = 3200 − 2000 = ", 1200, "Take the resultant off the driving force.",
            say="Friction is what is left: driving force minus resultant.", phase="substitute"),
        box("Check: driving − friction = 3200 − 1200 = ", 2000, "It should equal the resultant force.",
            done="Gives back the resultant 2000 N, so friction = 1200 N."),
    ]})

gold.append({
    "display": "An X-ray has a wavelength of \\(1 \\times 10^{-10}\\) m. The speed of EM waves is \\(3 \\times 10^8\\) m/s. Calculate the frequency of the X-ray. Give your answer in standard form.",
    "solutions": [3, 18], "calculator": True, "input_type": "standard_form",
    "higher_only": False, "equation_hint": "\\(v = f\\lambda\\)",
    "hint": "Rearrange v = fλ to f = v ÷ λ; subtract the powers of ten.",
    "misconceptions": [mc("unit_error",
        "f = v ÷ λ. Dividing subtracts the powers: 8 − (−10) = 18, so f = 3 × 10¹⁸ Hz. Adding them by mistake gives 10⁻².",
        [3, -2])],
    "guided_steps": [
        box("The numbers: 3 ÷ 1 = ", 3, "Just the fronts of each number.",
            say="The equation is \\(v = f\\lambda\\), rearranged to \\(f = v \\div \\lambda\\). Give the answer in standard form."),
        box("8 − (−10) = ", 18, "8 plus 10.",
            say="Now the powers of ten. Dividing subtracts them, and subtracting a negative adds.", phase="substitute"),
        box("Check by reversing: v = f × λ, so the powers add: 18 + (−10) = ", 8, "Multiply back: powers add.",
            done="Gives 3 × 10⁸ m/s, the original speed, so f = 3 × 10¹⁸ Hz."),
    ]})

problem_bank = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "One equation, values already in the right units: substitute straight in.",
    "silver_description": "Convert units first, or rearrange the equation, or find the resultant force before substituting.",
    "gold_description": "Two steps chained: momentum conservation, standard form, or a resultant force feeding into F = ma.",
}

# ---------------- TIER GUIDES ----------------
tier_guides = {
    "bronze": {
        "title": "Bronze: one equation, units already right",
        "steps": [
            "Choose the recall equation the question points to: \\(F = ma\\), \\(v = f\\lambda\\) or \\(T = 1/f\\).",
            "If you need something other than the subject, rearrange first: \\(a = F/m\\), \\(f = v/\\lambda\\).",
            "Substitute the numbers, calculate, and write the unit."
        ],
        "example": {
            "question": "A resultant force of 30 N acts on a 6 kg mass. Calculate its acceleration.",
            "steps": [
                {"label": "Equation", "content": "<p>\\(F = ma\\), so \\(a = F \\div m\\)</p>"},
                {"label": "Substitute", "content": "<p>\\(a = 30 \\div 6\\)</p>"},
                {"label": "Check", "content": "<p>\\(6 \\times 5 = 30\\) N ✓</p>"},
                {"label": "Answer", "content": "<p><strong>5 m/s²</strong></p>", "isAnswer": True, "is_answer": True},
            ]
        }
    },
    "silver": {
        "title": "Silver: convert units or rearrange first",
        "steps": [
            "Convert everything to base units before you substitute: grams to kilograms (÷ 1000), kHz to Hz (× 1000), cm to metres (÷ 100).",
            "For a resultant force, subtract friction or weight from the driving force, then use \\(a = F/m\\).",
            "Rearrange the equation for the quantity you want, then substitute and check."
        ],
        "example": {
            "question": "A 200 g ball is pushed with 5 N against 1 N of friction. Calculate its acceleration.",
            "steps": [
                {"label": "Convert", "content": "<p>\\(200\\) g \\(= 0.2\\) kg</p>"},
                {"label": "Substitute", "content": "<p>resultant \\(= 5 - 1 = 4\\) N, so \\(a = 4 \\div 0.2\\)</p>"},
                {"label": "Check", "content": "<p>\\(0.2 \\times 20 = 4\\) N ✓</p>"},
                {"label": "Answer", "content": "<p><strong>20 m/s²</strong></p>", "isAnswer": True, "is_answer": True},
            ]
        }
    },
    "gold": {
        "title": "Gold: two steps chained",
        "steps": [
            "Some problems need two equations. Momentum: total \\(mv\\) before a collision equals total \\(mv\\) after.",
            "Find the intermediate value first (a resultant force, a combined mass, or a frequency), then feed it into the second equation.",
            "For very large or very small numbers, give the answer in standard form."
        ],
        "example": {
            "question": "A 2 kg trolley at 5 m/s hits a stationary 3 kg trolley and they stick together. Calculate their combined velocity.",
            "steps": [
                {"label": "Momentum before", "content": "<p>\\(p = 2 \\times 5 = 10\\) kg m/s</p>"},
                {"label": "Substitute", "content": "<p>combined mass \\(= 5\\) kg, so \\(10 = 5v\\)</p>"},
                {"label": "Check", "content": "<p>\\(5 \\times 2 = 10\\) kg m/s ✓</p>"},
                {"label": "Answer", "content": "<p><strong>2 m/s</strong></p>", "isAnswer": True, "is_answer": True},
            ]
        }
    },
}

# ---------------- GUIDED (opener + teach) ----------------
guided = {
    "opener": {
        "label": "Before any equations",
        "display": "Same push. Empty trolley: it leaps.<br>Trolley loaded with shopping: it barely moves.",
        "steps": [
            box("A 2 kg ball needs a 10 N push to speed up at a certain rate. To make a 4 kg ball, twice as heavy, speed up at the SAME rate, how many newtons do you need? ",
                20, "Twice the mass needs twice the push.",
                say="Forget equations for a second. Picture two balls on a smooth floor."),
            box("Turn it around. For the 2 kg ball, that 10 N push gives an acceleration of 10 ÷ 2 = ",
                5, "Acceleration = force ÷ mass.",
                say="You just felt <strong>Newton's second law</strong>: force = mass × acceleration, \\(F = ma\\). Double the mass, double the force for the same acceleration."),
            sayonly("So \\(a = F/m\\). That one equation, plus \\(p = mv\\) for momentum and \\(v = f\\lambda\\) for waves, is this whole lesson."),
        ]
    },
    "teach": {
        "bronze": {
            "display": "A resultant force of 60 N acts on a 15 kg box. Calculate its acceleration.",
            "label": "Together: your first one",
            "steps": [
                box("Force F in newtons = ", 60, "Straight from the question.",
                    say="The equation is \\(F = ma\\). We want the acceleration, so rearrange to \\(a = F \\div m\\)."),
                box("Mass m in kilograms = ", 15, "Already in kg."),
                box("a = 60 ÷ 15 = ", 4, "60 shared into 15 equal parts.", say="Divide.", phase="substitute"),
                box("Check: F = m × a = 15 × 4 = ", 60, "Multiply mass by your acceleration.",
                    done="Back to 60 N, so a = 4 m/s². Gone in one move."),
            ]
        },
        "silver": {
            "display": "A 250 g ball is pushed with 3 N against 1 N of friction. Calculate its acceleration.",
            "label": "Together: the silver move",
            "steps": [
                box("250 g in kilograms = 250 ÷ 1000 = ", 0.25, "1000 grams in a kilogram.",
                    say="This one hides two traps: the mass is in grams, and there is friction. Convert the mass first."),
                box("Resultant force = 3 − 1 = ", 2, "Take the friction off the push."),
                box("a = 2 ÷ 0.25 = ", 8, "How many quarters fit into 2?", say="Now \\(a = F \\div m\\).", phase="substitute"),
                box("Check: F = m × a = 0.25 × 8 = ", 2, "Multiply mass by your acceleration.",
                    done="Back to 2 N, so a = 8 m/s². Convert and subtract: that was the whole point."),
            ]
        },
        "gold": {
            "display": "A 2 kg trolley moving at 6 m/s hits a stationary 4 kg trolley. They stick together. Calculate the velocity after the collision.",
            "label": "Together: the gold move",
            "steps": [
                box("Momentum before = 2 × 6 = ", 12, "Only the moving trolley has momentum.",
                    say="Momentum is conserved: total \\(mv\\) before equals total after. Find it before the collision."),
                box("Combined mass after = 2 + 4 = ", 6, "Both trolleys move together now."),
                box("v = 12 ÷ 6 = ", 2, "12 shared into 6 equal parts.",
                    say="That 12 kg m/s is now shared by 6 kg. \\(v = p \\div m\\).", phase="substitute"),
                box("Check: momentum after = 6 × 2 = ", 12, "Combined mass times your velocity.",
                    done="Matches the 12 before, so v = 2 m/s. Conservation is the whole trick."),
            ]
        },
    }
}

# ---------------- WORKED EXAMPLES (preserve, fix em dashes in labels) ----------------
worked_examples = [
    {"difficulty": "Bronze",
     "question": "A resultant force of 600 N acts on a 50 kg object. Calculate its acceleration.",
     "steps": [
         {"label": "Step 1: Recall the equation", "content": "<p>\\(F = ma\\)</p>"},
         {"label": "Step 2: Rearrange for a", "content": "<p>\\(a = \\frac{F}{m} = \\frac{600}{50}\\)</p>"},
         {"label": "Answer", "content": "<p>\\(a = 12\\) <strong>m/s²</strong></p>", "is_answer": True},
     ]},
    {"difficulty": "Silver",
     "question": "A car has a driving force of 4000 N and friction of 1200 N. Its mass is 1400 kg. Calculate its acceleration.",
     "steps": [
         {"label": "Step 1: Find resultant force", "content": "<p>Resultant = 4000 − 1200 = 2800 N</p>"},
         {"label": "Step 2: Use F = ma", "content": "<p>\\(a = \\frac{F}{m} = \\frac{2800}{1400}\\)</p>"},
         {"label": "Answer", "content": "<p>\\(a = 2\\) <strong>m/s²</strong></p>", "is_answer": True},
     ]},
    {"difficulty": "Gold",
     "question": "A 2 kg trolley moving at 3 m/s collides with a stationary 1 kg trolley. They stick together. Calculate the velocity after the collision.",
     "steps": [
         {"label": "Step 1: Momentum before", "content": "<p>p = mv. Trolley A: 2 × 3 = 6 kg m/s. Trolley B: 1 × 0 = 0. Total = 6 kg m/s</p>"},
         {"label": "Step 2: Momentum after (conservation)", "content": "<p>Total mass = 2 + 1 = 3 kg. p = mv, so 6 = 3 × v</p>"},
         {"label": "Answer", "content": "<p>\\(v = 6 \\div 3 = 2\\) <strong>m/s</strong></p>", "is_answer": True},
     ]},
]

practice_data = {
    "method_card": method_card,
    "topic_links": {"prerequisites": []},
    "exam_context": exam_context,
    "problem_bank": problem_bank,
    "related_videos": [],
    "worked_examples": worked_examples,
    "tier_guides": tier_guides,
    "guided": guided,
}

with io.open("lesson_physics-calculations-L08@8ebcc02072.json", "w", encoding="utf-8") as f:
    json.dump(practice_data, f, ensure_ascii=False, indent=1)
print("written")
