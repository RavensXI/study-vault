# -*- coding: utf-8 -*-
"""Build guided practice_data for higher-calculations-L04@f4e0c074d0
   (Forces, Acceleration and Motion Equations, OCR-B separate sciences)."""
import json, math, io

# ---------- SVG helpers (self-contained, theme-safe, NO xmlns/http) ----------
def _svg(aria, body, h=160):
    return (f'<svg viewBox="0 0 260 {h}" role="img" aria-label="{aria}" '
            f'style="max-width:280px;margin:0.6em auto;display:block;">{body}</svg>')

def _arrow(x1, y1, x2, y2, color, w=2.5):
    ang = math.atan2(y2 - y1, x2 - x1); L = 8
    ax1, ay1 = x2 - L*math.cos(ang-0.42), y2 - L*math.sin(ang-0.42)
    ax2, ay2 = x2 - L*math.cos(ang+0.42), y2 - L*math.sin(ang+0.42)
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"/>'
            f'<polygon points="{x2},{y2} {ax1:.1f},{ay1:.1f} {ax2:.1f},{ay2:.1f}" fill="{color}"/>')

def _t(x, y, s, color="currentColor", size=11, anchor="middle", weight="normal"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter,sans-serif" '
            f'font-size="{size}" fill="{color}" font-weight="{weight}">{s}</text>')

def _box(label):
    return ('<rect x="92" y="62" width="76" height="42" rx="6" fill="#3b82f6" fill-opacity="0.12" '
            'stroke="currentColor" stroke-width="1.5"/>' + _t(130, 88, label, size=12))

def _circle(label):
    return ('<circle cx="130" cy="82" r="26" fill="#3b82f6" fill-opacity="0.12" '
            'stroke="currentColor" stroke-width="1.5"/>' + _t(130, 86, label, size=12))

RED="#ef4444"; GREEN="#10b981"; BLUE="#3b82f6"

def R(color, lbl):   return _arrow(168,82,234,82,color) + _t(201,74,lbl,color,11)
def L(color, lbl):   return _arrow(92,82,26,82,color)  + _t(59,74,lbl,color,11)
def UP(color, lbl):  return _arrow(130,62,130,16,color) + _t(150,40,lbl,color,11,anchor="start")
def DOWN(color, lbl):return _arrow(130,104,130,150,color)+ _t(150,132,lbl,color,11,anchor="start")
def MOTION(lbl):     return _arrow(70,44,196,44,"currentColor",2)+ _t(130,36,lbl,"currentColor",11)
def TOP(lbl,dy=12):  return _t(130,dy,lbl,"currentColor",11)

# ---------- Figures (only quantities that appear in the problem) ----------
FIG = {}
FIG["b0"] = _svg("Box of mass 500 kg with a driving force F to the right and acceleration 4.0 metres per second squared",
                 _box("500 kg") + R(RED,"F = ?") + TOP("a = 4.0 m/s²"))
FIG["b1"] = _svg("Car of mass 900 kg with a resultant force of 1800 N to the right, acceleration unknown",
                 _box("900 kg") + R(RED,"F = 1800 N") + TOP("a = ?"))
FIG["b2"] = _svg("Car of unknown mass with a force of 4500 N to the right and acceleration 3.0 metres per second squared",
                 _box("? kg") + R(RED,"F = 4500 N") + TOP("a = 3.0 m/s²"))
FIG["b3"] = _svg("Car speeding up from 6 to 30 metres per second in 8.0 seconds",
                 _box("car") + MOTION("6 → 30 m/s") + TOP("t = 8.0 s, a = ?"))
FIG["b4"] = _svg("Van of mass 2500 kg with weight 24500 N acting downward",
                 _box("2500 kg") + DOWN(BLUE,"W = 24500 N"))
FIG["b6"] = _svg("Truck slowing from 20 metres per second to rest in 8.0 seconds",
                 _box("truck") + MOTION("20 m/s → 0") + TOP("t = 8.0 s, a = ?"))
FIG["b7"] = _svg("Object of unknown mass with a force of 300 N to the right and acceleration 6.0 metres per second squared",
                 _box("? kg") + R(RED,"F = 300 N") + TOP("a = 6.0 m/s²"))
FIG["s0"] = _svg("Sprinter of mass 70 kg accelerating from rest to 9.0 metres per second in 3.0 seconds",
                 _box("70 kg") + R(RED,"F = ?") + TOP("0 → 9.0 m/s in 3.0 s"))
FIG["s1"] = _svg("Car of mass 1500 kg moving at 15 metres per second with a braking force of 4500 N",
                 _box("1500 kg") + L(GREEN,"F = 4500 N") + MOTION("15 m/s") + TOP("t = ?"))
FIG["s2"] = _svg("Car travelling at 20 metres per second, reaction time 0.70 seconds",
                 _box("car") + MOTION("20 m/s") + TOP("reaction 0.70 s"))
FIG["s4"] = _svg("Rocket of mass 20000 kg, thrust 300000 N up, weight 196000 N down",
                 '<rect x="112" y="56" width="36" height="60" rx="6" fill="#3b82f6" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>'
                 + _t(130,90,"rocket",size=10) + _arrow(130,56,130,16,RED) + _t(130,12,"thrust = 300000 N",RED,11)
                 + _arrow(130,116,130,150,BLUE) + _t(130,146,"W = 196000 N",BLUE,11))
FIG["s5"] = _svg("Vehicle slowing from 30 metres per second, decelerating at 5.0 metres per second squared, distance unknown",
                 _box("vehicle") + MOTION("30 m/s → 0") + TOP("a = 5.0 m/s², s = ?"))
FIG["g0"] = _svg("Car of mass 1200 kg braking from 25 metres per second to rest over 50 metres, braking force unknown",
                 _box("1200 kg") + L(GREEN,"F = ?") + MOTION("25 m/s → 0") + TOP("s = 50 m"))
FIG["g1"] = _svg("Ball dropped from rest falling 20 metres, final speed unknown",
                 _circle("ball") + DOWN("currentColor","falls 20 m") + TOP("u = 0, v = ?"))
FIG["g2"] = _svg("Car travelling at 72 kilometres per hour, reaction time 0.60 seconds",
                 _box("car") + MOTION("72 km/h") + TOP("reaction 0.60 s"))
FIG["g3"] = _svg("Cyclist of mass 75 kg, drag 30 N backward, driving force unknown, acceleration 2.0 metres per second squared",
                 _box("75 kg") + R(RED,"F = ?") + L(GREEN,"drag = 30 N") + TOP("a = 2.0 m/s²"))
FIG["g4"] = _svg("Car of mass 1500 kg stopping from 15 metres per second, comparing stopping times 0.05 s and 0.15 s",
                 _box("1500 kg") + MOTION("15 m/s → 0") + TOP("stop in 0.05 s vs 0.15 s"))
FIG["g5"] = _svg("Ball thrown up at 14 metres per second, maximum height unknown",
                 _circle("ball") + UP("currentColor","14 m/s") + TOP("h = ?, g = 9.8"))

def disp(fig_key, text):
    return FIG[fig_key] + "<p>" + text + "</p>"

# ---------- Problem bank ----------
def mc(pattern, message, expect):
    return {"pattern": pattern, "check": "common", "expect": expect, "message": message}

bronze = [
 {"unit":"N","display":disp("b0","Calculate the force needed to accelerate a 500 kg motorbike at 4.0 m/s²."),
  "solutions":[2000],"accept":1,"calculator":True,"input_type":"single_value",
  "equation_hint":"\\(F = ma\\)","hint":"Multiply mass by acceleration.",
  "misconceptions":[mc("wrong_formula","F = ma = 500 × 4.0 = 2000 N. Multiply the numbers, do not add them.",504)],
  "guided_steps":[
    {"say":"Newton's second law: force = mass × acceleration, \\(F = ma\\)."},
    {"pre":"Mass in kg: m = ","answer":500,"hint":"Read the mass from the question."},
    {"pre":"Acceleration in m/s²: a = ","answer":4.0,"hint":"It is already in m/s², use it as it is."},
    {"pre":"F = 500 × 4.0 = ","answer":2000,"hint":"Multiply mass by acceleration.","say":"Now multiply.","phase":"substitute"},
    {"pre":"Check: 2000 ÷ 500 = ","answer":4.0,"hint":"Divide your force by the mass.","done":"Back to 4.0 m/s², so F = 2000 N."}]},

 {"unit":"m/s²","display":disp("b1","A 900 kg car has a resultant force of 1800 N acting on it. Calculate its acceleration."),
  "solutions":[2.0],"accept":0.05,"calculator":True,"input_type":"single_value",
  "equation_hint":"Rearrange \\(F = ma\\) to \\(a = F \\div m\\)","hint":"Divide the force by the mass.",
  "misconceptions":[mc("wrong_rearrange","a = F ÷ m = 1800 ÷ 900 = 2.0 m/s². Do not divide mass by force.",0.5)],
  "guided_steps":[
    {"say":"\\(F = ma\\) rearranges to \\(a = F \\div m\\)."},
    {"pre":"Force in N: F = ","answer":1800,"hint":"Read the resultant force."},
    {"pre":"Mass in kg: m = ","answer":900,"hint":"Read the mass."},
    {"pre":"a = 1800 ÷ 900 = ","answer":2.0,"hint":"Divide force by mass.","say":"Divide to find acceleration.","phase":"substitute"},
    {"pre":"Check: 900 × 2.0 = ","answer":1800,"hint":"Multiply mass by your acceleration.","done":"Back to 1800 N, so a = 2.0 m/s²."}]},

 {"unit":"kg","display":disp("b2","A resultant force of 4500 N gives a car an acceleration of 3.0 m/s². What is the mass of the car?"),
  "solutions":[1500],"accept":1,"calculator":True,"input_type":"single_value",
  "equation_hint":"Rearrange \\(F = ma\\) to \\(m = F \\div a\\)","hint":"Divide the force by the acceleration.",
  "misconceptions":[mc("wrong_rearrange","m = F ÷ a = 4500 ÷ 3.0 = 1500 kg. Do not multiply force by acceleration.",13500)],
  "guided_steps":[
    {"say":"\\(F = ma\\) rearranges to \\(m = F \\div a\\)."},
    {"pre":"Force in N: F = ","answer":4500,"hint":"Read the resultant force."},
    {"pre":"Acceleration in m/s²: a = ","answer":3.0,"hint":"Read the acceleration."},
    {"pre":"m = 4500 ÷ 3.0 = ","answer":1500,"hint":"Divide force by acceleration.","say":"Divide to find mass.","phase":"substitute"},
    {"pre":"Check: 1500 × 3.0 = ","answer":4500,"hint":"Multiply your mass by the acceleration.","done":"Back to 4500 N, so m = 1500 kg."}]},

 {"unit":"m/s²","display":disp("b3","A car accelerates from 6 m/s to 30 m/s in 8.0 s. Calculate its acceleration."),
  "solutions":[3.0],"accept":0.05,"calculator":True,"input_type":"single_value",
  "equation_hint":"\\(a = \\Delta v \\div \\Delta t = (v - u) \\div t\\)","hint":"Change in velocity divided by time.",
  "misconceptions":[mc("forgot_step","Δv = 30 − 6 = 24 m/s. a = 24 ÷ 8.0 = 3.0 m/s². Do not divide the final velocity by time.",3.75)],
  "guided_steps":[
    {"say":"Acceleration is the change in velocity each second: \\(a = (v - u) \\div t\\)."},
    {"pre":"Change in velocity: 30 − 6 = ","answer":24,"hint":"Final velocity minus starting velocity."},
    {"pre":"Time in s: t = ","answer":8.0,"hint":"Read the time."},
    {"pre":"a = 24 ÷ 8.0 = ","answer":3.0,"hint":"Divide the change by the time.","say":"Divide the change by the time.","phase":"substitute"},
    {"pre":"Check: 6 + 3.0 × 8.0 = ","answer":30,"hint":"Start speed plus acceleration times time.","done":"Back to 30 m/s, so a = 3.0 m/s²."}]},

 {"unit":"N/kg","display":disp("b4","A van of mass 2500 kg has a weight of 24 500 N on Earth. What is the gravitational field strength? Give units."),
  "solutions":[9.8],"accept":0.05,"calculator":True,"input_type":"single_value",
  "equation_hint":"\\(g = W \\div m\\)","hint":"Divide the weight by the mass.",
  "misconceptions":[mc("inverse_error","g = W ÷ m = 24500 ÷ 2500 = 9.8 N/kg. Divide weight by mass, not mass by weight.",0.102)],
  "guided_steps":[
    {"say":"Weight, mass and gravity link by \\(W = mg\\), so \\(g = W \\div m\\)."},
    {"pre":"Weight in N: W = ","answer":24500,"hint":"Read the weight."},
    {"pre":"Mass in kg: m = ","answer":2500,"hint":"Read the mass."},
    {"pre":"g = 24500 ÷ 2500 = ","answer":9.8,"hint":"Divide weight by mass.","say":"Divide to find the field strength.","phase":"substitute"},
    {"pre":"Check: 2500 × 9.8 = ","answer":24500,"hint":"Multiply mass by your value of g.","done":"Back to 24500 N, so g = 9.8 N/kg."}]},

 {"display":"Which of the following correctly explains why crumple zones reduce injury in a crash?",
  "options":["They absorb force like a sponge","They act as a rigid barrier between the car and the engine",
             "They increase the stopping time, reducing the deceleration and the force on passengers","They make the car lighter"],
  "solutions":[2],"calculator":False,"input_type":"multiple_choice",
  "hint":"Think about what a longer collision time does to the deceleration.",
  "misconceptions":[mc("wrong_equation","Longer stopping time gives a smaller deceleration (a = Δv ÷ t), so a smaller force (F = ma). Crumple zones extend the collision time, they do not block the force.",None)]},

 {"unit":"m/s²","display":disp("b6","A truck decelerates from 20 m/s to rest in 8.0 s. Calculate the deceleration."),
  "solutions":[2.5],"accept":0.05,"calculator":True,"input_type":"single_value",
  "equation_hint":"\\(a = \\Delta v \\div \\Delta t\\). The answer is a deceleration, state it as positive.","hint":"Change in velocity divided by time.",
  "misconceptions":[mc("inverse_error","Divide the change in velocity by the time, not time by velocity. a = 20 ÷ 8.0 = 2.5 m/s².",0.4)],
  "guided_steps":[
    {"say":"Deceleration uses \\(a = (v - u) \\div t\\); state the size as positive."},
    {"pre":"Change in velocity: 20 − 0 = ","answer":20,"hint":"Starting speed minus final speed."},
    {"pre":"Time in s: t = ","answer":8.0,"hint":"Read the time."},
    {"pre":"a = 20 ÷ 8.0 = ","answer":2.5,"hint":"Divide the change by the time.","say":"Divide the change by the time.","phase":"substitute"},
    {"pre":"Check: 2.5 × 8.0 = ","answer":20,"hint":"Your deceleration times the time.","done":"The truck loses 20 m/s, so the deceleration = 2.5 m/s²."}]},

 {"unit":"kg","display":disp("b7","A force of 300 N acts on an object that accelerates at 6.0 m/s². Calculate the mass of the object."),
  "solutions":[50],"accept":0.5,"calculator":True,"input_type":"single_value",
  "equation_hint":"\\(m = F \\div a\\)","hint":"Divide the force by the acceleration.",
  "misconceptions":[mc("wrong_rearrange","m = F ÷ a = 300 ÷ 6.0 = 50 kg. Do not multiply force by acceleration.",1800)],
  "guided_steps":[
    {"say":"\\(F = ma\\) rearranges to \\(m = F \\div a\\)."},
    {"pre":"Force in N: F = ","answer":300,"hint":"Read the force."},
    {"pre":"Acceleration in m/s²: a = ","answer":6.0,"hint":"Read the acceleration."},
    {"pre":"m = 300 ÷ 6.0 = ","answer":50,"hint":"Divide force by acceleration.","say":"Divide to find mass.","phase":"substitute"},
    {"pre":"Check: 50 × 6.0 = ","answer":300,"hint":"Your mass times the acceleration.","done":"Back to 300 N, so m = 50 kg."}]},
]

silver = [
 {"unit":"N","display":disp("s0","A 70 kg sprinter accelerates from rest to 9.0 m/s in 3.0 s. Calculate the average resultant force."),
  "solutions":[210],"accept":1,"calculator":True,"input_type":"single_value",
  "equation_hint":"First find acceleration using \\(a = \\Delta v \\div t\\), then \\(F = ma\\)","hint":"Find the acceleration first, then use F = ma.",
  "misconceptions":[mc("forgot_step","Find acceleration first: a = 9.0 ÷ 3.0 = 3.0 m/s². Then F = 70 × 3.0 = 210 N. Do not use velocity in place of acceleration.",630)],
  "guided_steps":[
    {"say":"First the acceleration, \\(a = (v - u) \\div t\\), then \\(F = ma\\)."},
    {"pre":"Change in velocity: 9.0 − 0 = ","answer":9,"hint":"Started from rest, so u = 0."},
    {"pre":"a = 9.0 ÷ 3.0 = ","answer":3.0,"hint":"Change in velocity divided by time."},
    {"pre":"F = 70 × 3.0 = ","answer":210,"hint":"Mass times acceleration.","say":"Now use F = ma.","phase":"substitute"},
    {"pre":"Check: 210 ÷ 70 = ","answer":3.0,"hint":"Divide your force by the mass.","done":"Acceleration 3.0 m/s², so F = 210 N."}]},

 {"unit":"s","display":disp("s1","A car travelling at 15 m/s applies a braking force of 4500 N. The car has a mass of 1500 kg. Calculate how long it takes to stop."),
  "solutions":[5.0],"accept":0.05,"calculator":True,"input_type":"single_value",
  "equation_hint":"First find deceleration: \\(a = F \\div m\\), then rearrange \\(a = \\Delta v \\div t\\) to find \\(t\\)","hint":"Find the deceleration first, then the time.",
  "misconceptions":[mc("forgot_step","a = 4500 ÷ 1500 = 3.0 m/s². Then t = Δv ÷ a = 15 ÷ 3.0 = 5.0 s.",0.2)],
  "guided_steps":[
    {"say":"Find the deceleration with \\(a = F \\div m\\), then the time from \\(a = \\Delta v \\div t\\)."},
    {"pre":"Force in N: F = ","answer":4500,"hint":"Read the braking force."},
    {"pre":"a = 4500 ÷ 1500 = ","answer":3.0,"hint":"Force divided by mass."},
    {"pre":"t = 15 ÷ 3.0 = ","answer":5.0,"hint":"Change in velocity divided by deceleration.","say":"Time = change in velocity ÷ deceleration.","phase":"substitute"},
    {"pre":"Check: 3.0 × 5.0 = ","answer":15,"hint":"Deceleration times your time.","done":"The car loses 15 m/s, so t = 5.0 s."}]},

 {"unit":"m","display":disp("s2","A driver takes 0.70 s to react before braking. The car is travelling at 20 m/s. Calculate the thinking distance."),
  "solutions":[14],"accept":0.5,"calculator":True,"input_type":"single_value",
  "equation_hint":"Thinking distance = speed × reaction time. Use \\(s = vt\\) (no acceleration during thinking phase).","hint":"Speed multiplied by the reaction time.",
  "misconceptions":[mc("wrong_formula","During the thinking phase the speed is constant. s = v × t = 20 × 0.70 = 14 m. Do not divide.",28.57)],
  "guided_steps":[
    {"say":"During the reaction time the speed is constant, so \\(s = vt\\)."},
    {"pre":"Speed in m/s: v = ","answer":20,"hint":"Read the speed."},
    {"pre":"Reaction time in s: t = ","answer":0.70,"hint":"Read the reaction time."},
    {"pre":"s = 20 × 0.70 = ","answer":14,"hint":"Multiply speed by reaction time.","say":"Multiply speed by reaction time.","phase":"substitute"},
    {"pre":"Check: 14 ÷ 20 = ","answer":0.70,"hint":"Divide your distance by the speed.","done":"Back to 0.70 s, so thinking distance = 14 m."}]},

 {"unit":"m","display":"A car has a thinking distance of 12 m and a braking distance of 36 m at a certain speed. What is its total stopping distance?",
  "solutions":[48],"calculator":False,"input_type":"single_value",
  "equation_hint":"Stopping distance = thinking distance + braking distance","hint":"Add the thinking and braking distances.",
  "misconceptions":[mc("wrong_formula","Stopping distance = thinking + braking = 12 + 36 = 48 m. Add them, do not subtract.",24)],
  "guided_steps":[
    {"say":"Total stopping distance = thinking distance + braking distance."},
    {"pre":"Thinking distance in m = ","answer":12,"hint":"Read the thinking distance."},
    {"pre":"Braking distance in m = ","answer":36,"hint":"Read the braking distance."},
    {"pre":"12 + 36 = ","answer":48,"hint":"Add the two distances.","say":"Add the two distances.","phase":"substitute"},
    {"pre":"Check: 48 − 36 = ","answer":12,"hint":"Take the braking distance back off.","done":"Back to the thinking distance, so total = 48 m."}]},

 {"unit":"m/s²","accept":0.1,"display":disp("s4","A rocket of mass 20 000 kg produces a thrust of 300 000 N. Its weight is 196 000 N. Calculate the resultant force and the initial acceleration upwards."),
  "solutions":[5.2],"calculator":True,"input_type":"single_value","higher_only":False,
  "equation_hint":"Resultant force = thrust − weight, then \\(a = F \\div m\\)","hint":"Subtract weight from thrust, then divide by mass.",
  "misconceptions":[mc("forgot_step","Resultant = thrust − weight = 300000 − 196000 = 104000 N. a = 104000 ÷ 20000 = 5.2 m/s². Do not forget to subtract the weight.",15)],
  "guided_steps":[
    {"say":"Find the resultant upward force, then \\(a = F \\div m\\)."},
    {"pre":"Resultant force: 300000 − 196000 = ","answer":104000,"hint":"Thrust up minus weight down."},
    {"pre":"Mass in kg: m = ","answer":20000,"hint":"Read the mass."},
    {"pre":"a = 104000 ÷ 20000 = ","answer":5.2,"hint":"Divide resultant force by mass.","say":"Divide the resultant force by the mass.","phase":"substitute"},
    {"pre":"Check: 20000 × 5.2 = ","answer":104000,"hint":"Mass times your acceleration.","done":"Back to 104000 N, so a = 5.2 m/s² upward."}]},

 {"unit":"m","display":disp("s5","A vehicle travelling at 30 m/s decelerates at 5.0 m/s². How far does it travel before stopping? Use v² = u² + 2as."),
  "solutions":[90],"accept":0.5,"calculator":True,"input_type":"single_value","higher_only":True,
  "equation_hint":"\\(v^2 = u^2 + 2as\\). Here v = 0, u = 30, a = −5.0. Rearrange to find s.","hint":"Use v squared equals u squared plus 2as, with v = 0.",
  "misconceptions":[mc("forgot_square","Square u first: 30² = 900, not 30. 0 = 900 − 10s, so s = 90 m.",3),
                    mc("sign_error","Deceleration is negative: 0 = 30² + 2×(−5.0)×s = 900 − 10s, so s = 90 m.",None)],
  "guided_steps":[
    {"say":"Use \\(v^2 = u^2 + 2as\\) with v = 0, u = 30, a = −5.0."},
    {"pre":"Square the start speed: 30² = ","answer":900,"hint":"30 × 30."},
    {"pre":"2 × the deceleration size: 2 × 5.0 = ","answer":10,"hint":"This is the number multiplying s."},
    {"pre":"s = 900 ÷ 10 = ","answer":90,"hint":"Distance = u² ÷ (2a).","say":"Divide u squared by 2a.","phase":"substitute"},
    {"pre":"Check: 2 × 5.0 × 90 = ","answer":900,"hint":"This should equal u squared.","done":"900 − 900 = 0 = v², so s = 90 m."}]},
]

gold = [
 {"unit":"N","display":disp("g0","A car of mass 1200 kg travelling at 25 m/s stops in 50 m. Calculate the braking force. Use v² = u² + 2as."),
  "solutions":[7500],"accept":1,"calculator":True,"input_type":"single_value","higher_only":True,
  "equation_hint":"Find the deceleration from \\(v^2 = u^2 + 2as\\), then \\(F = ma\\)","hint":"Find the deceleration first, then use F = ma.",
  "misconceptions":[mc("forgot_square","Square u: 25² = 625. 0 = 625 + 2a×50, so a = −6.25 m/s². F = 1200 × 6.25 = 7500 N.",300),
                    mc("wrong_rearrange","Find a from v² = u² + 2as first, then F = ma. a = −6.25, F = 1200 × 6.25 = 7500 N.",None)],
  "guided_steps":[
    {"say":"Find the deceleration from \\(v^2 = u^2 + 2as\\), then \\(F = ma\\)."},
    {"pre":"Square the start speed: 25² = ","answer":625,"hint":"25 × 25."},
    {"pre":"0 = 625 + 100a, so a = −625 ÷ 100 = ","answer":-6.25,"hint":"Divide 625 by 100, negative for deceleration."},
    {"pre":"F = 1200 × 6.25 = ","answer":7500,"hint":"Mass times the size of the deceleration.","say":"Use the size of the deceleration in F = ma.","phase":"substitute"},
    {"pre":"Check: 7500 ÷ 1200 = ","answer":6.25,"hint":"Divide your force by the mass.","done":"Deceleration 6.25 m/s², so braking force = 7500 N."}]},

 {"unit":"m/s","accept":0.1,"display":disp("g1","A ball is dropped from rest and falls 20 m. Use v² = u² + 2as (g = 9.8 m/s²) to find the speed just before impact. Give your answer to 3 significant figures."),
  "solutions":[19.8],"calculator":True,"input_type":"single_value","higher_only":True,
  "equation_hint":"\\(v^2 = u^2 + 2as\\) with u = 0. Square-root at the end.","hint":"Work out 2gs, then take the square root.",
  "misconceptions":[mc("forgot_square","v² = 2 × 9.8 × 20 = 392. Then v = √392 = 19.8 m/s. Do not forget to square-root at the end.",392),
                    mc("wrong_formula","Dropped from rest so u = 0. v² = u² + 2as = 0 + 2×9.8×20 = 392, v = 19.8 m/s.",None)],
  "guided_steps":[
    {"say":"Dropped from rest so u = 0. Use \\(v^2 = u^2 + 2as\\)."},
    {"pre":"2 × 9.8 × 20 = ","answer":392,"hint":"This is 2 × g × distance, and equals v²."},
    {"pre":"v = √392 = ","answer":19.8,"hint":"Square root of 392, to 3 significant figures.","say":"Square root at the end.","phase":"substitute"},
    {"pre":"Check: 19.8² ÷ 20 ÷ 2 = ","answer":9.8,"hint":"This should return g.","done":"Returns g = 9.8 m/s², so v = 19.8 m/s."}]},

 {"unit":"m","display":disp("g2","A car is travelling at 72 km/h. Convert this to m/s, then calculate the thinking distance if the reaction time is 0.60 s."),
  "solutions":[12],"accept":0.5,"calculator":True,"input_type":"single_value",
  "equation_hint":"Convert km/h to m/s by ÷ 3.6, then \\(s = vt\\)","hint":"Convert to m/s first, then multiply by the reaction time.",
  "misconceptions":[mc("unit_error","Convert first: 72 ÷ 3.6 = 20 m/s. Then s = 20 × 0.60 = 12 m. Do not use 72 in the distance calculation.",43.2),
                    mc("forgot_step","Always convert km/h to m/s (÷ 3.6) before finding distances in metres.",None)],
  "guided_steps":[
    {"say":"Convert to m/s first, then \\(s = vt\\)."},
    {"pre":"Speed in m/s: 72 ÷ 3.6 = ","answer":20,"hint":"Divide km/h by 3.6."},
    {"pre":"Reaction time in s: t = ","answer":0.60,"hint":"Read the reaction time."},
    {"pre":"s = 20 × 0.60 = ","answer":12,"hint":"Multiply speed by reaction time.","say":"Multiply the converted speed by the reaction time.","phase":"substitute"},
    {"pre":"Check: 12 ÷ 0.60 = ","answer":20,"hint":"Divide your distance by the reaction time.","done":"Back to 20 m/s, so thinking distance = 12 m."}]},

 {"unit":"N","display":disp("g3","A cyclist and bicycle together have a mass of 75 kg. The cyclist accelerates at 2.0 m/s² against a resistive force of 30 N. What is the driving force from the cyclist's legs?"),
  "solutions":[180],"accept":1,"calculator":True,"input_type":"single_value",
  "equation_hint":"\\(F = ma\\) gives the resultant. Driving force = resultant + resistance.","hint":"Find the resultant force, then add the resistance.",
  "misconceptions":[mc("forgot_step","Resultant = ma = 75 × 2.0 = 150 N. Driving force = resultant + resistance = 150 + 30 = 180 N.",150),
                    mc("wrong_formula","F = ma gives the resultant force only. Add the resistance the legs must overcome: 150 + 30 = 180 N.",None)],
  "guided_steps":[
    {"say":"\\(F = ma\\) gives the resultant. Driving force = resultant + drag."},
    {"pre":"Resultant force: 75 × 2.0 = ","answer":150,"hint":"Mass times acceleration."},
    {"pre":"Driving force = 150 + 30 = ","answer":180,"hint":"Add the drag the legs must overcome.","say":"Add the drag to the resultant.","phase":"substitute"},
    {"pre":"Check: 180 − 30 = ","answer":150,"hint":"Take the drag back off.","done":"Resultant 150 N, so driving force = 180 N."}]},

 {"unit":"times greater without crumple zones","display":disp("g4","A car crashes into a wall. Without crumple zones it stops in 0.05 s. With crumple zones it stops in 0.15 s. The car and driver have a combined mass of 1500 kg and are travelling at 15 m/s. Calculate the force with and without crumple zones and find the ratio."),
  "solutions":[3],"accept":0.05,"calculator":True,"input_type":"single_value","higher_only":True,
  "equation_hint":"Use \\(a = \\Delta v \\div t\\) then \\(F = ma\\) for each case, then compare.","hint":"Find each force, then divide the larger by the smaller.",
  "misconceptions":[mc("forgot_step","Without: a = 15÷0.05 = 300, F = 450000 N. With: a = 15÷0.15 = 100, F = 150000 N. Ratio = 450000÷150000 = 3.",0.3333),
                    mc("wrong_formula","Use a = Δv ÷ t for each scenario, then F = ma, then compare the two forces.",None)],
  "guided_steps":[
    {"say":"Force is bigger when the stop is quicker. Find each force with \\(a = \\Delta v \\div t\\) then \\(F = ma\\)."},
    {"pre":"Without crumple zones: a = 15 ÷ 0.05 = ","answer":300,"hint":"Change in velocity divided by the short time."},
    {"pre":"F = 1500 × 300 = ","answer":450000,"hint":"Mass times acceleration."},
    {"pre":"With crumple zones: a = 15 ÷ 0.15 = ","answer":100,"hint":"Change in velocity divided by the longer time."},
    {"pre":"F = 1500 × 100 = ","answer":150000,"hint":"Mass times acceleration.","say":"Now the gentler stop."},
    {"pre":"Ratio = 450000 ÷ 150000 = ","answer":3,"hint":"Larger force divided by smaller force.","say":"Compare the two forces.","phase":"substitute"},
    {"pre":"Check: 150000 × 3 = ","answer":450000,"hint":"Smaller force times your ratio.","done":"Force is 3 times greater without crumple zones."}]},

 {"unit":"m","accept":0.5,"display":disp("g5","A 0.50 kg ball is thrown upward at 14 m/s. Using v² = u² + 2as (g = 9.8 m/s²), calculate the maximum height reached. Give your answer to 2 significant figures."),
  "solutions":[10],"calculator":True,"input_type":"single_value","higher_only":True,
  "equation_hint":"At the top v = 0. Use \\(v^2 = u^2 + 2as\\) with a = −9.8.","hint":"At the top v = 0; rearrange for s.",
  "misconceptions":[mc("forgot_square","Square u: 14² = 196. s = 196 ÷ 19.6 = 10 m. Do not use 14 unsquared.",0.714),
                    mc("sign_error","At the top v = 0. 0 = 14² + 2×(−9.8)×s = 196 − 19.6s, so s = 10 m.",None)],
  "guided_steps":[
    {"say":"At the top v = 0. Use \\(v^2 = u^2 + 2as\\) with a = −9.8."},
    {"pre":"Square the launch speed: 14² = ","answer":196,"hint":"14 × 14."},
    {"pre":"2 × g: 2 × 9.8 = ","answer":19.6,"hint":"This is the number multiplying s."},
    {"pre":"s = 196 ÷ 19.6 = ","answer":10,"hint":"Height = u² ÷ (2g).","say":"Divide u squared by 2g.","phase":"substitute"},
    {"pre":"Check: 19.6 × 10 = ","answer":196,"hint":"This should equal u squared.","done":"Back to 196, so maximum height = 10 m (2 s.f.)."}]},
]

# ---------- tier_guides ----------
tier_guides = {
 "bronze":{"title":"Bronze: one equation, values ready to use",
   "steps":["Pick the equation: <strong>F = ma</strong>, or <strong>a = Δv ÷ t</strong>, or <strong>W = mg</strong>.",
            "Read the two known values straight from the question.",
            "Substitute and work out the answer, then write its unit."],
   "example":{"question":"A 250 kg go-kart accelerates at 3.0 m/s². Calculate the resultant force.",
     "steps":[{"label":"Equation","content":"\\(F = ma\\)"},
              {"label":"Substitute","content":"F = 250 × 3.0"},
              {"label":"Check","content":"750 ÷ 250 = 3.0 m/s² ✓"},
              {"label":"Answer","content":"<strong>750 N</strong>","isAnswer":True,"is_answer":True}]}},
 "silver":{"title":"Silver: rearrange, or find the acceleration first",
   "steps":["Some questions need two steps: find acceleration with <strong>a = Δv ÷ t</strong> or <strong>a = F ÷ m</strong> first.",
            "Then substitute into the second equation (usually F = ma or s = vt).",
            "Rearrange before you put numbers in, and keep every unit in SI."],
   "example":{"question":"A 60 kg cyclist speeds up from 4 m/s to 10 m/s in 3.0 s. Calculate the resultant force.",
     "steps":[{"label":"Acceleration","content":"a = (10 − 4) ÷ 3.0 = 2.0 m/s²"},
              {"label":"Force","content":"F = 60 × 2.0"},
              {"label":"Check","content":"120 ÷ 60 = 2.0 m/s² ✓"},
              {"label":"Answer","content":"<strong>120 N</strong>","isAnswer":True,"is_answer":True}]}},
 "gold":{"title":"Gold: chain two equations or use v² = u² + 2as",
   "steps":["When time is not given, use <strong>v² = u² + 2as</strong>. Square the speed and watch the sign of a.",
            "Often you find acceleration first, then feed it into F = ma.",
            "Convert km/h to m/s (÷ 3.6) before any distance step."],
   "example":{"question":"A 1000 kg car brakes from 20 m/s to rest in 40 m. Calculate the braking force.",
     "steps":[{"label":"Find a","content":"0 = 20² + 2a×40, so a = −5.0 m/s²"},
              {"label":"Force","content":"F = 1000 × 5.0"},
              {"label":"Check","content":"20² − 2×5×40 = 0 ✓"},
              {"label":"Answer","content":"<strong>5000 N</strong>","isAnswer":True,"is_answer":True}]}},
}

# ---------- guided opener + teach ----------
opener = {"label":"Before any equation",
 "display":"You push two supermarket trolleys with the same steady force of 60 N.<br>Trolley A holds 10 kg of shopping. Trolley B holds 30 kg.",
 "steps":[
   {"pre":"Trolley A (10 kg): share the 60 N push over the mass. 60 ÷ 10 = ","answer":6,
    "hint":"Divide the force by the mass.","say":"No equation yet, just share the push out over the mass it has to move."},
   {"pre":"Trolley B (30 kg): 60 ÷ 30 = ","answer":2,
    "hint":"Divide the same 60 N by the bigger mass.","say":"Now the heavier trolley, same push."},
   {"say":"Same 60 N push: the light trolley gains speed at 6 each second, the heavy one only 2. Sharing the force over the mass IS acceleration, \\(a = F \\div m\\), which rearranges to \\(F = ma\\). More mass means less acceleration for the same force."}]}

teach = {
 "bronze":{"display":"A 250 kg go-kart accelerates at 3.0 m/s². Find the resultant force.",
   "steps":[
     {"say":"Straight into \\(F = ma\\)."},
     {"pre":"Mass in kg: m = ","answer":250,"hint":"Read the mass."},
     {"pre":"Acceleration in m/s²: a = ","answer":3.0,"hint":"Read the acceleration."},
     {"pre":"F = 250 × 3.0 = ","answer":750,"hint":"Multiply mass by acceleration."},
     {"pre":"Check: 750 ÷ 250 = ","answer":3.0,"hint":"Divide your force by the mass.","done":"Back to 3.0 m/s², so F = 750 N. That is the whole Bronze move."}]},
 "silver":{"display":"A 60 kg cyclist speeds up from 4 m/s to 10 m/s in 3.0 s. Find the resultant force.",
   "steps":[
     {"say":"Time is given, so find acceleration first, then \\(F = ma\\)."},
     {"pre":"Change in velocity: 10 − 4 = ","answer":6,"hint":"Final minus starting velocity."},
     {"pre":"a = 6 ÷ 3.0 = ","answer":2.0,"hint":"Change in velocity divided by time."},
     {"pre":"F = 60 × 2.0 = ","answer":120,"hint":"Mass times acceleration."},
     {"pre":"Check: 120 ÷ 60 = ","answer":2.0,"hint":"Divide your force by the mass.","done":"Two steps chained: that is the Silver move."}]},
 "gold":{"display":"A 1000 kg car brakes from 20 m/s to rest in 40 m. Find the braking force. Use v² = u² + 2as.",
   "steps":[
     {"say":"No time given, so reach for \\(v^2 = u^2 + 2as\\)."},
     {"pre":"Square the start speed: 20² = ","answer":400,"hint":"20 × 20."},
     {"pre":"0 = 400 + 80a, so a = −400 ÷ 80 = ","answer":-5.0,"hint":"Divide 400 by 80, negative for braking."},
     {"pre":"F = 1000 × 5.0 = ","answer":5000,"hint":"Mass times the size of the deceleration."},
     {"pre":"Check: 20² − 2×5×40 = ","answer":0,"hint":"Should return v² = 0.","done":"Kinematic equation then F = ma: the Gold move."}]},
}

# ---------- method_card (slim, neutral, no em dash) ----------
method_card = {
 "title":"Forces, Acceleration and Motion Equations",
 "steps":[
   "Choose the equation: F = ma, a = Δv ÷ Δt, or v² = u² + 2as.",
   "List the known values and check every unit is SI (kg, m, s, N).",
   "Rearrange first, then substitute the numbers.",
   "Write the answer with its unit; for stopping distance add thinking and braking distances."],
 "content":("<p>Three linked ideas. <strong>Newton's second law</strong> F = ma links resultant force, mass and "
   "acceleration. <strong>Acceleration</strong> a = Δv ÷ Δt is the change in velocity each second. "
   "<strong>Weight</strong> W = mg. Check whether your board gives you the kinematic equation v² = u² + 2as, "
   "used when the time is not known.</p><p>Convert km/h to m/s by dividing by 3.6. Stopping distance = thinking "
   "distance + braking distance. Crumple zones work by increasing the time a force acts over, so from F = ma the "
   "deceleration and the force on passengers are smaller.</p>")}

# ---------- assemble ----------
pd = {
 "method_card": method_card,
 "topic_links": {"prerequisites": []},
 "exam_context": {
   "marks":"2 to 5 marks per calculation; crumple zone safety questions often 3 to 6 marks",
   "paper":"Physics",
   "frequency":"Very high: forces and motion calculations appear on almost every Physics paper"},
 "problem_bank": {
   "bronze": bronze, "silver": silver, "gold": gold,
   "bronze_description":"One equation, values already in the right units. Pick F = ma (or its rearrangement) and substitute.",
   "silver_description":"Find the acceleration first, or rearrange for time or force before substituting.",
   "gold_description":"Two steps chained, or the kinematic equation v² = u² + 2as. Watch the signs and square the speed."},
 "related_videos": [],
 "worked_examples": [
   {"difficulty":"Bronze","question":"A car of mass 1200 kg accelerates at 3.0 m/s². Calculate the resultant force acting on it.",
    "steps":[{"label":"Step 1: Write the equation","content":"<p>\\(F = ma\\)</p>"},
             {"label":"Step 2: Substitute","content":"<p>\\(F = 1200 \\times 3.0\\)</p>"},
             {"label":"Answer","content":"<p>Force = <strong>3600 N</strong></p>","is_answer":True}]},
   {"difficulty":"Silver","question":"A cyclist accelerates from 2.0 m/s to 8.0 m/s in 4.0 s. The total mass of cyclist and bike is 80 kg. Calculate the resultant force.",
    "steps":[{"label":"Step 1: Find acceleration","content":"<p>\\(a = \\dfrac{\\Delta v}{\\Delta t} = \\dfrac{8.0 - 2.0}{4.0} = \\dfrac{6.0}{4.0} = 1.5 \\text{ m/s}^2\\)</p>"},
             {"label":"Step 2: Use F = ma","content":"<p>\\(F = 80 \\times 1.5 = 120 \\text{ N}\\)</p>"},
             {"label":"Answer","content":"<p>Resultant force = <strong>120 N</strong></p>","is_answer":True}]},
   {"difficulty":"Gold","question":"A car travelling at 20 m/s brakes to rest. The braking force is 6000 N and the car has a mass of 1500 kg. Calculate the braking distance. Use v² = u² + 2as.",
    "steps":[{"label":"Step 1: Find deceleration using F = ma","content":"<p>\\(a = F \\div m = 6000 \\div 1500 = 4.0 \\text{ m/s}^2\\) (deceleration, so negative)</p>"},
             {"label":"Step 2: Identify values for v² = u² + 2as","content":"<p>v = 0 (comes to rest), u = 20 m/s, a = −4.0 m/s², s = ?</p>"},
             {"label":"Step 3: Rearrange and calculate","content":"<p>\\(0 = 20^2 + 2 \\times (-4.0) \\times s\\)</p><p>\\(0 = 400 - 8s\\)</p><p>\\(s = 400 \\div 8 = 50 \\text{ m}\\)</p>"},
             {"label":"Answer","content":"<p>Braking distance = <strong>50 m</strong></p>","is_answer":True}]}],
 "tier_guides": tier_guides,
 "guided": {"opener": opener, "teach": teach},
}

with io.open("lesson_higher-calculations-L04@f4e0c074d0.json","w",encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written; bronze",len(bronze),"silver",len(silver),"gold",len(gold))
