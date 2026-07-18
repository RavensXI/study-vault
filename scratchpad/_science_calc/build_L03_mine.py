# -*- coding: utf-8 -*-
"""Build guided practice_data for physics-calculations-L03@330faf0468 (Circuit Calculations)."""
import json, copy

SRC="_mine330_b2dd6adb.json"
OUT="lesson_physics-calculations-L03@330faf0468.json"
orig=json.load(open(SRC,encoding="utf-8"))

# ---------- SVG helpers (theme-safe: currentColor, soft opacity fills) ----------
FONT="Inter,system-ui,sans-serif"
def _open(w,h,aria):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{aria}" '
            f'style="max-width:{w}px;margin:0.8em auto;display:block;">')

def series_svg(aria, cell_label, resistors, ammeter=True, voltmeter_idx=None,
               caption="", right_label=None):
    W,H=440,190
    s=[_open(W,H,aria)]
    s.append('<path d="M60 55 H380 V135 H60 Z" fill="none" stroke="currentColor" stroke-width="2.5"/>')
    # cell (two plates crossing left wire at x=60)
    s.append('<line x1="46" y1="82" x2="74" y2="82" stroke="currentColor" stroke-width="2"/>')
    s.append('<line x1="53" y1="96" x2="67" y2="96" stroke="currentColor" stroke-width="5"/>')
    if cell_label:
        s.append(f'<text x="30" y="93" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="currentColor">{cell_label}</text>')
    n=len(resistors)
    centers={0:[],1:[250],2:[170,270],3:[150,235,320]}.get(n,[])
    bw=64 if n<=2 else 58
    boxes=[]
    for c,label in zip(centers,resistors):
        x=c-bw/2
        s.append(f'<rect x="{x:.0f}" y="42" width="{bw}" height="26" rx="2" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="2"/>')
        s.append(f'<text x="{c}" y="59" text-anchor="middle" font-family="{FONT}" font-size="12" fill="currentColor">{label}</text>')
        boxes.append((c,x,bw))
    if ammeter:
        s.append('<circle cx="220" cy="135" r="16" fill="#34d399" fill-opacity="0.15" stroke="currentColor" stroke-width="2"/>')
        s.append(f'<text x="220" y="140" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="currentColor">A</text>')
    if voltmeter_idx is not None and boxes:
        c,x,bw2=boxes[voltmeter_idx]
        s.append(f'<line x1="{x:.0f}" y1="42" x2="{x:.0f}" y2="20" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>')
        s.append(f'<line x1="{x+bw2:.0f}" y1="42" x2="{x+bw2:.0f}" y2="20" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>')
        s.append(f'<circle cx="{c}" cy="14" r="11" fill="#f59e0b" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>')
        s.append(f'<text x="{c}" y="18" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="700" fill="currentColor">V</text>')
    if right_label:
        s.append(f'<text x="372" y="122" text-anchor="end" font-family="{FONT}" font-size="11" fill="currentColor">{right_label}</text>')
    if caption:
        s.append(f'<text x="220" y="181" text-anchor="middle" font-family="{FONT}" font-size="11" fill="currentColor" fill-opacity="0.7" font-style="italic">{caption}</text>')
    s.append('</svg>')
    return ''.join(s)

def parallel_svg(aria, cell_label, r1, r2, caption):
    W,H=440,200
    s=[_open(W,H,aria)]
    s.append('<path d="M70 45 H360 V165 H70 Z" fill="none" stroke="currentColor" stroke-width="2.5"/>')
    # cell on left wire
    s.append('<line x1="56" y1="92" x2="84" y2="92" stroke="currentColor" stroke-width="2"/>')
    s.append('<line x1="63" y1="106" x2="77" y2="106" stroke="currentColor" stroke-width="5"/>')
    s.append(f'<text x="40" y="103" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="currentColor">{cell_label}</text>')
    # ammeter in supply line (top-left)
    s.append('<circle cx="145" cy="45" r="15" fill="#34d399" fill-opacity="0.15" stroke="currentColor" stroke-width="2"/>')
    s.append(f'<text x="145" y="50" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="currentColor">A</text>')
    # two node rails
    s.append('<line x1="215" y1="45" x2="215" y2="165" stroke="currentColor" stroke-width="2"/>')
    s.append('<line x1="300" y1="45" x2="300" y2="165" stroke="currentColor" stroke-width="2"/>')
    # branch 1 (top wire) box
    s.append('<rect x="225" y="32" width="65" height="26" rx="2" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="2"/>')
    s.append(f'<text x="257" y="49" text-anchor="middle" font-family="{FONT}" font-size="12" fill="currentColor">{r1}</text>')
    # branch 2 (bottom wire) box
    s.append('<rect x="225" y="152" width="65" height="26" rx="2" fill="#60a5fa" fill-opacity="0.18" stroke="currentColor" stroke-width="2"/>')
    s.append(f'<text x="257" y="169" text-anchor="middle" font-family="{FONT}" font-size="12" fill="currentColor">{r2}</text>')
    s.append(f'<text x="215" y="193" text-anchor="middle" font-family="{FONT}" font-size="11" fill="currentColor" fill-opacity="0.7" font-style="italic">{caption}</text>')
    s.append('</svg>')
    return ''.join(s)

def wrap(svg, text):
    """Clean single-figure display string: svg then question text in one <p>."""
    return f'{svg}<p style="margin:0.9em 0 0;">{text}</p>'

# ---------- Bank problems (fresh-solved, repaired, guided) ----------
# helper to make the 3-box standard walk
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d={"pre":pre,"post":post,"answer":answer,"hint":hint}
    if say is not None: d["say"]=say
    if done is not None: d["done"]=done
    if phase is not None: d["phase"]=phase
    return d
def sayonly(say): return {"say":say}

bronze=[]
# b0: Q = I x t, I=3, t=12 -> 36 C  (was t=10 ->30, changed to de-dup with b1=30)
bronze.append({
 "unit":"C","input_type":"single_value","calculator":True,"solutions":[36],
 "equation_hint":"\\(Q = I \\times t\\)",
 "hint":"Charge = current × time. Both are already in amps and seconds, so just multiply.",
 "svg":series_svg("Circuit loop with a cell and an ammeter, current 3 amps for 12 seconds",
      "cell",[],ammeter=True,right_label="t = 12 s",caption="I = 3 A, t = 12 s: find the charge Q"),
 "text":"A current of 3 A flows through a circuit for 12 seconds. Calculate the charge that passes.",
 "mis":[{"pattern":"inverse_error","expect":0.25,
    "message":"Q = I × t, so multiply: 3 × 12 = 36 C. Dividing (3 ÷ 12 = 0.25) is the slip here."}],
 "steps":[sayonly("Charge uses <strong>Q = I × t</strong>. Current is in amps and time in seconds already, so no conversion."),
    box("Write the current in amps: I = ",3,"The question gives it directly: 3 A."),
    box("Q = I × t = 3 × 12 = ",36,"Multiply the two values.",phase="substitute"),
    box("Check by dividing back: 36 ÷ 12 = ",3,"That returns the current, so the charge is right.",phase="substitute",done="Back to 3 A, so Q = 36 C is correct.")],
})
# b1: R = V/I, V=9, I=0.3 -> 30
bronze.append({
 "unit":"Ω","input_type":"single_value","calculator":True,"solutions":[30],
 "equation_hint":"\\(R = V \\div I\\)",
 "hint":"Rearrange V = IR to R = V ÷ I, then divide.",
 "svg":series_svg("Circuit with a 9 volt cell, one resistor of unknown value and a voltmeter, current 0.3 amps",
      "9 V",["R = ?"],ammeter=True,voltmeter_idx=0,caption="I = 0.3 A: find the resistance R"),
 "text":"A resistor has 9 V across it and 0.3 A through it. Calculate its resistance.",
 "mis":[{"pattern":"inverse_error","expect":2.7,
    "message":"R = V ÷ I = 9 ÷ 0.3 = 30 Ω. Multiplying (9 × 0.3 = 2.7) is the slip: divide instead."}],
 "steps":[sayonly("Ohm's law is <strong>V = I × R</strong>. You want R, so rearrange to R = V ÷ I."),
    box("Write the pd in volts: V = ",9,"Straight from the question: 9 V."),
    box("R = V ÷ I = 9 ÷ 0.3 = ",30,"Divide 9 by 0.3.",phase="substitute"),
    box("Check with V = I × R = 0.3 × 30 = ",9,"It returns 9 V, so R is right.",phase="substitute",done="Back to 9 V, so R = 30 Ω.")],
})
# b2: V = IR, R=20, I=0.5 -> 10
bronze.append({
 "unit":"V","input_type":"single_value","calculator":True,"solutions":[10],
 "equation_hint":"\\(V = I \\times R\\)",
 "hint":"Ohm's law: multiply current by resistance.",
 "svg":series_svg("Circuit with a cell, one 20 ohm resistor and an ammeter reading 0.5 amps",
      "V",["20 Ω"],ammeter=True,caption="I = 0.5 A: find the pd across the resistor"),
 "text":"A resistor of 20 Ω has a current of 0.5 A through it. Calculate the potential difference.",
 "mis":[{"pattern":"inverse_error","expect":0.025,
    "message":"V = I × R = 0.5 × 20 = 10 V. Dividing (0.5 ÷ 20 = 0.025) is the slip: multiply here."}],
 "steps":[sayonly("Ohm's law <strong>V = I × R</strong>. Current and resistance are given, so substitute straight in."),
    box("Write the current in amps: I = ",0.5,"Straight from the question: 0.5 A."),
    box("V = I × R = 0.5 × 20 = ",10,"Multiply 0.5 by 20.",phase="substitute"),
    box("Check with I = V ÷ R = 10 ÷ 20 = ",0.5,"It returns 0.5 A, so V is right.",phase="substitute",done="Back to 0.5 A, so V = 10 V.")],
})
# b3: series 7 + 5 -> 12  (was 6+4 ->10, changed to de-dup with b2=10)
bronze.append({
 "unit":"Ω","input_type":"single_value","calculator":True,"solutions":[12],
 "equation_hint":"\\(R_{total} = R_1 + R_2\\)",
 "hint":"In series, total resistance is the sum of the parts.",
 "svg":series_svg("Series circuit with a cell and two resistors of 7 ohms and 5 ohms",
      "V",["7 Ω","5 Ω"],ammeter=True,caption="Series: find the total resistance"),
 "text":"Two resistors of 7 Ω and 5 Ω are connected in series. What is the total resistance?",
 "mis":[{"pattern":"parallel_formula","expect":2.92,
    "message":"In series, add the resistances: 7 + 5 = 12 Ω. Using the parallel rule (about 2.92 Ω) is wrong here; parallel is for branches, not a chain."}],
 "steps":[sayonly("In a <strong>series</strong> chain the resistances simply add: R = R₁ + R₂."),
    box("Write the first resistance: R₁ = ",7,"The first resistor: 7 Ω."),
    box("Add them: 7 + 5 = ",12,"Sum the two resistances.",phase="substitute"),
    box("A series total is larger than either part. 12 Ω is bigger than 7 and 5, so type ",12,"Confirm the total.",phase="substitute",done="Bigger than both parts, so R = 12 Ω.")],
})
# b4: I = V/R, V=12, R=40 -> 0.3
bronze.append({
 "unit":"A","input_type":"single_value","calculator":True,"solutions":[0.3],
 "equation_hint":"\\(I = V \\div R\\)",
 "hint":"Rearrange V = IR to I = V ÷ R, then divide.",
 "svg":series_svg("Circuit with a 12 volt cell, one 40 ohm resistor and an ammeter",
      "12 V",["40 Ω"],ammeter=True,caption="Find the current from the battery"),
 "text":"A circuit has a 12 V battery and a single 40 Ω resistor. Calculate the current.",
 "mis":[{"pattern":"wrong_equation","expect":480,
    "message":"I = V ÷ R = 12 ÷ 40 = 0.3 A. Multiplying (12 × 40 = 480) is the slip: divide the pd by the resistance."}],
 "steps":[sayonly("Ohm's law rearranged for current: <strong>I = V ÷ R</strong>."),
    box("Write the resistance in ohms: R = ",40,"Straight from the question: 40 Ω."),
    box("I = V ÷ R = 12 ÷ 40 = ",0.3,"Divide 12 by 40.",phase="substitute"),
    box("Check with V = I × R = 0.3 × 40 = ",12,"It returns 12 V, so the current is right.",phase="substitute",done="Back to 12 V, so I = 0.3 A.")],
})
# b5: I = Q/t, Q=100, t=25 -> 4
bronze.append({
 "unit":"A","input_type":"single_value","calculator":True,"solutions":[4],
 "equation_hint":"\\(I = Q \\div t\\)",
 "hint":"Rearrange Q = I × t to I = Q ÷ t.",
 "svg":series_svg("Circuit loop with a cell and an ammeter, 100 coulombs passing in 25 seconds",
      "cell",[],ammeter=True,right_label="t = 25 s",caption="Q = 100 C in 25 s: find the current"),
 "text":"A charge of 100 C passes through a wire in 25 seconds. Calculate the current.",
 "mis":[{"pattern":"inverse_error","expect":0.25,
    "message":"I = Q ÷ t = 100 ÷ 25 = 4 A. Dividing the wrong way (25 ÷ 100 = 0.25) is the slip."}],
 "steps":[sayonly("Current is charge per second, so rearrange Q = I × t to <strong>I = Q ÷ t</strong>."),
    box("Write the charge in coulombs: Q = ",100,"Straight from the question: 100 C."),
    box("I = Q ÷ t = 100 ÷ 25 = ",4,"Divide 100 by 25.",phase="substitute"),
    box("Check with Q = I × t = 4 × 25 = ",100,"It returns 100 C, so the current is right.",phase="substitute",done="Back to 100 C, so I = 4 A.")],
})

silver=[]
# s0: series 4+6+2 -> 12
silver.append({
 "unit":"Ω","input_type":"single_value","calculator":True,"solutions":[12],
 "equation_hint":"\\(R_{total} = R_1 + R_2 + R_3\\)",
 "hint":"Series resistances add: sum all three.",
 "svg":series_svg("Series circuit with a 6 volt cell and three resistors of 4, 6 and 2 ohms",
      "6 V",["4 Ω","6 Ω","2 Ω"],ammeter=True,caption="Series: find the total resistance"),
 "text":"A 6 V battery is connected to three resistors in series: 4 Ω, 6 Ω and 2 Ω. Calculate the total resistance.",
 "mis":[{"pattern":"wrong_formula","expect":1.09,
    "message":"Series resistances add: 4 + 6 + 2 = 12 Ω. Combining them as parallel branches (about 1.09 Ω) is the wrong rule for a chain."}],
 "steps":[sayonly("A <strong>series</strong> chain adds every resistance: R = R₁ + R₂ + R₃."),
    box("Add the first two: 4 + 6 = ",10,"Start with 4 + 6."),
    box("Add the third: 10 + 2 = ",12,"Add the last resistor.",phase="substitute"),
    box("The series total is the sum of all three, so type ",12,"Confirm the total.",phase="substitute",done="4 + 6 + 2 = 12 Ω.")],
})
# s1: I = V/R, 6/12 -> 0.5
silver.append({
 "unit":"A","input_type":"single_value","calculator":True,"solutions":[0.5],
 "equation_hint":"\\(I = V \\div R\\)",
 "hint":"Use the total resistance in I = V ÷ R.",
 "svg":series_svg("Series circuit, 6 volt cell with total resistance 12 ohms and an ammeter",
      "6 V",["R = 12 Ω"],ammeter=True,caption="Find the current in the circuit"),
 "text":"Using the 6 V battery and 12 Ω total resistance from the previous question, calculate the current in the circuit.",
 "mis":[{"pattern":"wrong_equation","expect":72,
    "message":"I = V ÷ R = 6 ÷ 12 = 0.5 A. Multiplying (6 × 12 = 72) is the slip: divide the pd by the total resistance."}],
 "steps":[sayonly("The whole supply pd drives the current through the total resistance: <strong>I = V ÷ R</strong>."),
    box("Write the total resistance in ohms: R = ",12,"From the previous part: 12 Ω."),
    box("I = V ÷ R = 6 ÷ 12 = ",0.5,"Divide 6 by 12.",phase="substitute"),
    box("Check with V = I × R = 0.5 × 12 = ",6,"It returns 6 V, so the current is right.",phase="substitute",done="Back to 6 V, so I = 0.5 A.")],
})
# s2: V = IR across the 6 ohm, 0.5*6 -> 3
silver.append({
 "unit":"V","input_type":"single_value","calculator":True,"solutions":[3],
 "equation_hint":"\\(V = I \\times R\\)",
 "hint":"Same current flows through every series component: use V = I × R for the 6 Ω.",
 "svg":series_svg("Series circuit of three resistors with a voltmeter across the 6 ohm resistor, current 0.5 amps",
      "6 V",["4 Ω","6 Ω","2 Ω"],ammeter=True,voltmeter_idx=1,caption="I = 0.5 A: find the pd across 6 Ω"),
 "text":"The current in the series circuit above is 0.5 A. Calculate the pd across the 6 Ω resistor.",
 "mis":[{"pattern":"wrong_equation","expect":0.083,
    "message":"V = I × R = 0.5 × 6 = 3 V. Dividing (0.5 ÷ 6 ≈ 0.083) is the slip: multiply the current by that one resistance."}],
 "steps":[sayonly("In series the same current flows through each resistor, so for one component <strong>V = I × R</strong>."),
    box("Write the current in amps: I = ",0.5,"The series current: 0.5 A."),
    box("V = I × R = 0.5 × 6 = ",3,"Multiply 0.5 by 6.",phase="substitute"),
    box("Check with I = V ÷ R = 3 ÷ 6 = ",0.5,"It returns 0.5 A, so the pd is right.",phase="substitute",done="Back to 0.5 A, so the pd is 3 V.")],
})
# s3: I = V/R, 12/240 -> 0.05
silver.append({
 "unit":"A","input_type":"single_value","calculator":True,"solutions":[0.05],
 "equation_hint":"\\(I = V \\div R\\)",
 "hint":"A big resistance gives a small current: I = V ÷ R.",
 "svg":series_svg("Circuit with a 12 volt cell, a lamp filament of 240 ohms and an ammeter",
      "12 V",["240 Ω"],ammeter=True,caption="Hot filament 240 Ω: find the current"),
 "text":"A lamp filament has resistance 240 Ω when hot. Connected to 12 V supply, calculate the current in amperes.",
 "mis":[{"pattern":"wrong_equation","expect":2880,
    "message":"I = V ÷ R = 12 ÷ 240 = 0.05 A. Multiplying (12 × 240 = 2880) is the slip: divide the pd by the resistance."}],
 "steps":[sayonly("Ohm's law for current: <strong>I = V ÷ R</strong>. A large resistance means a small current."),
    box("Write the resistance in ohms: R = ",240,"The hot filament: 240 Ω."),
    box("I = V ÷ R = 12 ÷ 240 = ",0.05,"Divide 12 by 240.",phase="substitute"),
    box("Check with V = I × R = 0.05 × 240 = ",12,"It returns 12 V, so the current is right.",phase="substitute",done="Back to 12 V, so I = 0.05 A.")],
})
# s4: Q = It, 2*15 -> 30
silver.append({
 "unit":"C","input_type":"single_value","calculator":True,"solutions":[30],
 "equation_hint":"\\(Q = I \\times t\\)",
 "hint":"Charge = current × time.",
 "svg":series_svg("Circuit loop with a cell and an ammeter, 2 amps flowing for 15 seconds",
      "cell",[],ammeter=True,right_label="t = 15 s",caption="I = 2 A, t = 15 s: find the charge"),
 "text":"A circuit has 2 A flowing for 15 seconds. Calculate the charge transferred in coulombs.",
 "mis":[{"pattern":"inverse_error","expect":7.5,
    "message":"Q = I × t = 2 × 15 = 30 C. Dividing (15 ÷ 2 = 7.5) is the slip: multiply current by time."}],
 "steps":[sayonly("Charge is current times time: <strong>Q = I × t</strong>, with time in seconds."),
    box("Write the current in amps: I = ",2,"Straight from the question: 2 A."),
    box("Q = I × t = 2 × 15 = ",30,"Multiply 2 by 15.",phase="substitute"),
    box("Check with I = Q ÷ t = 30 ÷ 15 = ",2,"It returns 2 A, so the charge is right.",phase="substitute",done="Back to 2 A, so Q = 30 C.")],
})

gold=[]
# g0: total R = V/I = 60, R = 60-10-20 = 30
gold.append({
 "unit":"Ω","input_type":"single_value","calculator":True,"solutions":[30],
 "hint":"Find the total resistance from V ÷ I first, then subtract the two known resistors.",
 "svg":series_svg("Series circuit, 12 volt cell driving 0.2 amps through resistors 10 ohms, 20 ohms and unknown R",
      "12 V",["10 Ω","20 Ω","R₃"],ammeter=True,caption="I = 0.2 A: find the third resistance R"),
 "text":"A 12 V battery drives a current of 0.2 A through a series circuit of three resistors (10 Ω, 20 Ω and R). Calculate R.",
 "mis":[{"pattern":"forgot_step","expect":60,
    "message":"60 Ω is the total resistance (V ÷ I). The question wants only R, so subtract the known resistors: 60 − 10 − 20 = 30 Ω."},
   {"pattern":"wrong_rearrange","expect":None,
    "message":"Find the total resistance with R = V ÷ I = 12 ÷ 0.2 = 60 Ω, then take away the two known resistors: R = 60 − 10 − 20 = 30 Ω."}],
 "steps":[sayonly("In series the resistances add to the total. Find that total from Ohm's law, then peel off the known ones."),
    box("Total resistance R = V ÷ I = 12 ÷ 0.2 = ",60,"Divide 12 by 0.2 for the whole-circuit resistance."),
    box("Subtract the known resistors: 60 − 10 − 20 = ",30,"Take both known values off the total.",phase="substitute"),
    box("Check: 10 + 20 + 30 = 60 Ω, and 12 ÷ 60 = ",0.2,"The three add to 60 Ω and give 0.2 A.",phase="substitute",done="Back to 0.2 A, so R = 30 Ω.")],
})
# g1: total R = 6/0.03 = 200, thermistor = 200-100 = 100
gold.append({
 "unit":"Ω","input_type":"single_value","calculator":True,"solutions":[100],
 "hint":"Total resistance is V ÷ I; the thermistor is the total minus the fixed resistor.",
 "svg":series_svg("Series circuit, 6 volt supply driving 0.03 amps through a thermistor and a 100 ohm fixed resistor",
      "6 V",["Rₜ","100 Ω"],ammeter=True,caption="I = 0.03 A: find the thermistor resistance"),
 "text":"A thermistor in series with a 100 Ω fixed resistor is connected to a 6 V supply. The current is 0.03 A. Calculate the resistance of the thermistor.",
 "mis":[{"pattern":"forgot_step","expect":200,
    "message":"200 Ω is the total resistance (V ÷ I). The thermistor is the total minus the fixed resistor: 200 − 100 = 100 Ω."},
   {"pattern":"inverse_error","expect":None,
    "message":"Total R = V ÷ I = 6 ÷ 0.03 = 200 Ω. Thermistor = total − fixed = 200 − 100 = 100 Ω."}],
 "steps":[sayonly("Series resistances add, so the total is thermistor + fixed. Find the total from Ohm's law first."),
    box("Total resistance R = V ÷ I = 6 ÷ 0.03 = ",200,"Divide 6 by 0.03."),
    box("Thermistor = total − fixed = 200 − 100 = ",100,"Take the fixed resistor off the total.",phase="substitute"),
    box("Check: 100 + 100 = 200 Ω, and 6 ÷ 200 = ",0.03,"The two add to 200 Ω and give 0.03 A.",phase="substitute",done="Back to 0.03 A, so the thermistor is 100 Ω.")],
})
# g2: parallel, I1 = 9/30 = 0.3   (fix caption)
gold.append({
 "unit":"A","input_type":"single_value","calculator":True,"solutions":[0.3],
 "hint":"In parallel each branch has the full supply pd across it: I = V ÷ R for that branch.",
 "svg":parallel_svg("Parallel circuit, 9 volt cell with two branches of 30 ohms and 45 ohms",
      "9 V","30 Ω","45 Ω","Branch 1: find the current I₁"),
 "text":"A 9 V battery drives current through two parallel branches. Branch 1 has a 30 Ω resistor. Branch 2 has a 45 Ω resistor. Calculate the current through branch 1 in amperes.",
 "mis":[{"pattern":"series_mistake","expect":0.12,
    "message":"The branches are in parallel, not series. Treating them as series gives 30 + 45 = 75 Ω and 9 ÷ 75 = 0.12 A, which is wrong. Each branch has the full 9 V, so I₁ = 9 ÷ 30 = 0.3 A."},
   {"pattern":"wrong_equation","expect":0.2,
    "message":"Use branch 1's own resistance: I₁ = 9 ÷ 30 = 0.3 A. Using 45 Ω (9 ÷ 45 = 0.2 A) gives branch 2, not branch 1."}],
 "steps":[sayonly("In a <strong>parallel</strong> circuit every branch has the full supply pd across it, so treat branch 1 on its own."),
    box("The pd across branch 1 equals the supply: V = ",9,"Parallel branches all get the full supply pd: 9 V."),
    box("I₁ = V ÷ R = 9 ÷ 30 = ",0.3,"Divide 9 by branch 1's resistance.",phase="substitute"),
    box("Check with V = I × R = 0.3 × 30 = ",9,"It returns 9 V, so the branch current is right.",phase="substitute",done="Back to 9 V, so I₁ = 0.3 A.")],
})
# g3: I = Q/t = 12, V = IR = 60
gold.append({
 "unit":"V","input_type":"single_value","calculator":True,"solutions":[60],
 "hint":"Find the current from Q ÷ t first, then use V = I × R.",
 "svg":series_svg("Circuit with a cell, a 5 ohm resistor and an ammeter, 2400 coulombs passing in 200 seconds",
      "V",["5 Ω"],ammeter=True,right_label="t = 200 s",caption="Q = 2400 C in 200 s: find the pd"),
 "text":"A charge of 2,400 C passes through a resistor of 5 Ω in 200 seconds. Calculate the potential difference across the resistor.",
 "mis":[{"pattern":"forgot_step","expect":12,
    "message":"12 A is the current (Q ÷ t). The question asks for pd, so keep going: V = I × R = 12 × 5 = 60 V."},
   {"pattern":"wrong_equation","expect":12000,
    "message":"First find the current: I = Q ÷ t = 2400 ÷ 200 = 12 A. Then V = I × R = 12 × 5 = 60 V. Multiplying charge by resistance (2400 × 5) is not a real step."}],
 "steps":[sayonly("Two steps: turn the charge and time into a current, then use Ohm's law."),
    box("Current I = Q ÷ t = 2400 ÷ 200 = ",12,"Divide the charge by the time."),
    box("V = I × R = 12 × 5 = ",60,"Multiply the current by the resistance.",phase="substitute"),
    box("Check with I = V ÷ R = 60 ÷ 5 = ",12,"It returns 12 A, so the pd is right.",phase="substitute",done="Back to 12 A, so V = 60 V.")],
})

def assemble(pblist):
    out=[]
    for p in pblist:
        disp=wrap(p["svg"],p["text"])
        prob={
          "display":disp,
          "question":disp,
          "input_type":p["input_type"],
          "solutions":p["solutions"],
          "unit":p["unit"],
          "calculator":p["calculator"],
          "hint":p["hint"],
          "misconceptions":[{"pattern":m["pattern"],"check":"common","message":m["message"],"expect":m["expect"]} for m in p["mis"]],
          "guided_steps":p["steps"],
        }
        if "equation_hint" in p: prob["equation_hint"]=p["equation_hint"]
        out.append(prob)
    return out

pd=copy.deepcopy(orig)
pd["problem_bank"]={
  "bronze":assemble(bronze),
  "silver":assemble(silver),
  "gold":assemble(gold),
  "bronze_description":"One equation, values already in the right units. Pick it, substitute and solve.",
  "silver_description":"Rearrange the equation first, or chain two together (a series total, then a current or pd).",
  "gold_description":"Work backwards from the total resistance, or handle a parallel branch, over several steps.",
}

# ---------- tier_guides ----------
pd["tier_guides"]={
 "bronze":{"title":"Bronze: one equation, straight in",
   "steps":["Read what you are <strong>given</strong> and what you must <strong>find</strong>.",
            "Pick the matching equation: <strong>Q = I × t</strong>, <strong>V = I × R</strong>, or add resistances for a series total.",
            "Substitute the numbers and calculate. Finish with the unit (C, V, A or Ω)."],
   "example":{"question":"A 4 A current flows for 5 s. Find the charge.",
     "steps":[{"label":"Equation","content":"\\(Q = I \\times t\\)"},
              {"label":"Substitute","content":"Q = 4 × 5"},
              {"label":"Check","content":"Multiply, not divide: 4 × 5 = 20"},
              {"label":"Answer","content":"<strong>20 C</strong>","isAnswer":True,"is_answer":True}]}},
 "silver":{"title":"Silver: rearrange or chain two steps",
   "steps":["Rearrange Ohm's law before substituting: <strong>R = V ÷ I</strong> or <strong>I = V ÷ R</strong>.",
            "For a series circuit, add the resistances to a total first, then use that total.",
            "Keep the same current through every series component."],
   "example":{"question":"A 12 V supply drives current through 3 Ω and 9 Ω in series. Find the current.",
     "steps":[{"label":"Total resistance","content":"3 + 9 = 12 Ω"},
              {"label":"Rearrange","content":"\\(I = V \\div R\\)"},
              {"label":"Check","content":"12 ÷ 12 = 1, and 1 × 12 = 12 V"},
              {"label":"Answer","content":"<strong>1 A</strong>","isAnswer":True,"is_answer":True}]}},
 "gold":{"title":"Gold: work backwards or combine branches",
   "steps":["Find the total resistance from <strong>R = V ÷ I</strong>, then subtract known resistors to reach an unknown one.",
            "In parallel, every branch has the <strong>full supply pd</strong>, so treat each branch on its own.",
            "Some problems need two equations chained: charge to current, then Ohm's law."],
   "example":{"question":"A 10 V supply drives 0.5 A through two series resistors; one is 6 Ω. Find the other.",
     "steps":[{"label":"Total resistance","content":"\\(R = V \\div I = 10 \\div 0.5 = 20\\) Ω"},
              {"label":"Subtract","content":"20 − 6 = 14"},
              {"label":"Check","content":"6 + 14 = 20 Ω, and 10 ÷ 20 = 0.5 A"},
              {"label":"Answer","content":"<strong>14 Ω</strong>","isAnswer":True,"is_answer":True}]}},
}

# ---------- guided: opener + teach ----------
pd["guided"]={
 "opener":{
   "display":"Picture a turnstile at a stadium. People click through it one after another.",
   "steps":[
     sayonly("The turnstile lets <strong>3 people</strong> through every second."),
     box("After 10 seconds, how many people have passed? ",30,"Three every second, for 10 seconds: 3 × 10."),
     sayonly("You just multiplied a <strong>rate</strong> by a <strong>time</strong>. Electric charge behaves in exactly the same way."),
     box("If 3 coulombs of charge flow every second (a current of 3 A) for 10 seconds, the total charge is ",30,"Same sum as the people: 3 × 10."),
     sayonly("That is the equation <strong>Q = I × t</strong>: current is charge per second, so charge = current × time. Every circuit question starts by naming the right equation like this."),
   ]},
 "teach":{
   "bronze":{
     "display":wrap(series_svg("Circuit with a 6 volt cell, one resistor and an ammeter reading 2 amps","6 V",["R = ?"],ammeter=True,voltmeter_idx=0,caption="I = 2 A: find the resistance"),
        "A 6 V supply pushes 2 A through a resistor. Find its resistance."),
     "steps":[
       sayonly("Ohm's law is <strong>V = I × R</strong>. You want R, so rearrange to R = V ÷ I."),
       box("Write the pd in volts: V = ",6,"Straight from the question: 6 V."),
       box("Write the current in amps: I = ",2,"Straight from the question: 2 A."),
       box("R = V ÷ I = 6 ÷ 2 = ",3,"Divide 6 by 2.",phase="substitute"),
       box("Check with V = I × R = 2 × 3 = ",6,"It returns 6 V, so R is right.",phase="substitute",done="Rearrange, substitute, divide. That is the whole Bronze move.")]},
   "silver":{
     "display":wrap(series_svg("Series circuit, 8 volt cell with two resistors of 3 ohms and 5 ohms","8 V",["3 Ω","5 Ω"],ammeter=True,caption="Find the current in the circuit"),
        "Two resistors, 3 Ω and 5 Ω, are in series across an 8 V supply. Find the current."),
     "steps":[
       sayonly("Two moves chained: add the series resistances to a <strong>total</strong>, then use <strong>I = V ÷ R</strong>."),
       box("Write the first resistance: R₁ = ",3,"The first resistor: 3 Ω."),
       box("Add for the total: 3 + 5 = ",8,"Series resistances add."),
       box("I = V ÷ R = 8 ÷ 8 = ",1,"Divide the supply pd by the total resistance.",phase="substitute"),
       box("Check with V = I × R = 1 × 8 = ",8,"It returns 8 V, so the current is right.",phase="substitute",done="Total first, then Ohm's law. That is the Silver chain.")]},
   "gold":{
     "display":wrap(series_svg("Series circuit, 10 volt cell driving 0.5 amps through an 8 ohm resistor and an unknown resistor","10 V",["8 Ω","R = ?"],ammeter=True,caption="I = 0.5 A: find the missing resistor"),
        "A 10 V supply drives 0.5 A through two resistors in series. One is 8 Ω. Find the other."),
     "steps":[
       sayonly("Work <strong>backwards</strong>: get the total resistance from Ohm's law, then subtract the known resistor."),
       box("Total resistance R = V ÷ I = 10 ÷ 0.5 = ",20,"Divide 10 by 0.5 for the whole circuit."),
       box("Write the known resistor: ",8,"The one you are told: 8 Ω."),
       box("The other = 20 − 8 = ",12,"Subtract the known resistor from the total.",phase="substitute"),
       box("Check: 8 + 12 = 20 Ω, and 10 ÷ 20 = ",0.5,"The two add to 20 Ω and give 0.5 A.",phase="substitute",done="Total, then subtract. That is the Gold move.")]},
 },
}

# ---------- method_card (slim) ----------
pd["method_card"]={
 "title":"Circuit Calculations",
 "steps":["Pick the equation from what you are given and asked to find",
          "Rearrange it before you put any numbers in",
          "Substitute, keeping amps, volts, ohms and seconds",
          "Calculate and state the answer with its unit"],
 "content":("<p>Three equations cover this lesson.</p>"
   "<p><strong>Charge:</strong> Q = I × t (coulombs, amps, seconds).</p>"
   "<p><strong>Ohm's law:</strong> V = I × R. Rearrange to R = V ÷ I or I = V ÷ R first.</p>"
   "<p><strong>Series:</strong> same current everywhere; add the resistances.</p>"
   "<p><strong>Parallel:</strong> same pd across every branch; total resistance is less than the smallest branch.</p>"),
}

# ---------- de-dash preserved fields ----------
ec=pd.get("exam_context",{})
if isinstance(ec.get("frequency"),str):
    ec["frequency"]=ec["frequency"].replace(" — ",": ").replace("—","-")
for w in pd.get("worked_examples",[]):
    for st in w.get("steps",[]):
        if isinstance(st.get("label"),str):
            st["label"]=st["label"].replace(" — ",": ").replace("—","-")
        if isinstance(st.get("content"),str):
            st["content"]=st["content"].replace(" — ",": ").replace("—","-")
    if isinstance(w.get("question"),str):
        w["question"]=w["question"].replace(" — ",": ").replace("—","-")

json.dump(pd, open(OUT,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote",OUT)
print("bronze sols",[p["solutions"] for p in pd["problem_bank"]["bronze"]])
print("silver sols",[p["solutions"] for p in pd["problem_bank"]["silver"]])
print("gold sols",[p["solutions"] for p in pd["problem_bank"]["gold"]])
