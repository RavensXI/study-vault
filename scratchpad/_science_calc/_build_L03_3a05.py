# -*- coding: utf-8 -*-
import json, io

KEY = "higher-calculations-L03@3a05577182"

# ---------- SVG figures ----------
SVG_OPENER = ('<svg viewBox="0 0 260 120" role="img" aria-label="A seesaw balanced on a central pivot: '
 'a 10 newton weight 2 metres to the left and an unknown weight 1 metre to the right">'
 '<line x1="30" y1="64" x2="230" y2="64" stroke="currentColor" stroke-width="3"/>'
 '<polygon points="130,64 119,92 141,92" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor"/>'
 '<line x1="60" y1="64" x2="60" y2="90" stroke="currentColor" stroke-width="1.5"/>'
 '<polygon points="60,96 55,87 65,87" fill="currentColor"/>'
 '<line x1="165" y1="64" x2="165" y2="90" stroke="currentColor" stroke-width="1.5"/>'
 '<polygon points="165,96 160,87 170,87" fill="currentColor"/>'
 '<text x="60" y="112" font-family="Inter" font-size="11" text-anchor="middle" fill="currentColor">10 N</text>'
 '<text x="165" y="112" font-family="Inter" font-size="11" text-anchor="middle" fill="currentColor">? N</text>'
 '<text x="95" y="56" font-family="Inter" font-size="10" text-anchor="middle" fill="currentColor">2 m</text>'
 '<text x="147" y="56" font-family="Inter" font-size="10" text-anchor="middle" fill="currentColor">1 m</text>'
 '</svg>')

SVG_S0 = ('<svg viewBox="0 0 260 122" role="img" aria-label="A seesaw on a central pivot: a 30 kilogram child '
 '2 metres left of the pivot and a 60 kilogram adult an unknown distance to the right">'
 '<line x1="30" y1="64" x2="230" y2="64" stroke="currentColor" stroke-width="3"/>'
 '<polygon points="130,64 119,92 141,92" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor"/>'
 '<line x1="70" y1="64" x2="70" y2="90" stroke="currentColor" stroke-width="1.5"/>'
 '<polygon points="70,96 65,87 75,87" fill="currentColor"/>'
 '<line x1="178" y1="64" x2="178" y2="90" stroke="currentColor" stroke-width="1.5"/>'
 '<polygon points="178,96 173,87 183,87" fill="currentColor"/>'
 '<text x="70" y="112" font-family="Inter" font-size="11" text-anchor="middle" fill="currentColor">30 kg</text>'
 '<text x="178" y="112" font-family="Inter" font-size="11" text-anchor="middle" fill="currentColor">60 kg</text>'
 '<text x="100" y="56" font-family="Inter" font-size="10" text-anchor="middle" fill="currentColor">2.0 m</text>'
 '<text x="154" y="56" font-family="Inter" font-size="10" text-anchor="middle" fill="currentColor">? m</text>'
 '</svg>')

SVG_G0 = ('<svg viewBox="0 0 280 128" role="img" aria-label="A beam on a central pivot: a 200 newton force 1.5 metres left, '
 'a 100 newton force 0.5 metres left, and an unknown force 0.7 metres right of the pivot">'
 '<line x1="20" y1="64" x2="260" y2="64" stroke="currentColor" stroke-width="3"/>'
 '<polygon points="140,64 129,92 151,92" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor"/>'
 '<line x1="86" y1="64" x2="86" y2="90" stroke="currentColor" stroke-width="1.5"/><polygon points="86,96 81,87 91,87" fill="currentColor"/>'
 '<line x1="122" y1="64" x2="122" y2="90" stroke="currentColor" stroke-width="1.5"/><polygon points="122,96 117,87 127,87" fill="currentColor"/>'
 '<line x1="165" y1="64" x2="165" y2="90" stroke="currentColor" stroke-width="1.5"/><polygon points="165,96 160,87 170,87" fill="currentColor"/>'
 '<text x="86" y="112" font-family="Inter" font-size="11" text-anchor="middle" fill="currentColor">200 N</text>'
 '<text x="122" y="112" font-family="Inter" font-size="11" text-anchor="middle" fill="currentColor">100 N</text>'
 '<text x="165" y="112" font-family="Inter" font-size="11" text-anchor="middle" fill="currentColor">? N</text>'
 '<text x="106" y="52" font-family="Inter" font-size="10" text-anchor="middle" fill="currentColor">1.5 m</text>'
 '<text x="131" y="40" font-family="Inter" font-size="10" text-anchor="middle" fill="currentColor">0.5 m</text>'
 '<text x="153" y="52" font-family="Inter" font-size="10" text-anchor="middle" fill="currentColor">0.7 m</text>'
 '</svg>')

SVG_G3 = ('<svg viewBox="0 0 230 122" role="img" aria-label="A uniform beam 2 metres long with the pivot 0.8 metres from the left end, '
 'a 50 newton load at the left end, the 10 kilogram beam weight acting at the centre, and an unknown force at the right end">'
 '<line x1="20" y1="54" x2="200" y2="54" stroke="currentColor" stroke-width="3"/>'
 '<polygon points="92,54 82,82 102,82" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor"/>'
 '<line x1="20" y1="54" x2="20" y2="80" stroke="currentColor" stroke-width="1.5"/><polygon points="20,86 15,77 25,77" fill="currentColor"/>'
 '<line x1="110" y1="54" x2="110" y2="80" stroke="currentColor" stroke-width="1.5"/><polygon points="110,86 105,77 115,77" fill="currentColor"/>'
 '<line x1="200" y1="54" x2="200" y2="80" stroke="currentColor" stroke-width="1.5"/><polygon points="200,86 195,77 205,77" fill="currentColor"/>'
 '<text x="20" y="102" font-family="Inter" font-size="11" text-anchor="middle" fill="currentColor">50 N</text>'
 '<text x="110" y="102" font-family="Inter" font-size="10" text-anchor="middle" fill="currentColor">10 kg</text>'
 '<text x="200" y="102" font-family="Inter" font-size="11" text-anchor="middle" fill="currentColor">? N</text>'
 '<text x="56" y="46" font-family="Inter" font-size="10" text-anchor="middle" fill="currentColor">0.8 m</text>'
 '<text x="146" y="46" font-family="Inter" font-size="10" text-anchor="middle" fill="currentColor">1.2 m</text>'
 '</svg>')

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def say(s): return {"say": s}

# ---------- BRONZE ----------
bronze = [
 {  # b0 M=50x0.3=15
  "unit":"Nm","display":"A force of 50 N acts at a perpendicular distance of 0.3 m from a pivot. Calculate the moment.",
  "solutions":[15],"accept":0.5,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(M = F \\times d\\)","hint":"Moment is force times distance; multiply 50 by 0.3.",
  "misconceptions":[{"pattern":"inverse_error","check":"common","expect":166.67,
    "message":"Moment is force × distance, so 50 × 0.3 = 15 Nm. Dividing (50 ÷ 0.3 = 166.7) is the usual slip."}],
  "guided_steps":[
    say("The moment is the turning effect: \\(M = F \\times d\\). Here F = 50 N and d = 0.3 m, both ready to use."),
    box("Multiply the digits first, ignoring the decimal: 50 × 3 = ",150,"Just 50 times 3 for now."),
    box("Now put the decimal back. 0.3 is 3 tenths, so 150 ÷ 10 = ",15,"One decimal place means divide by 10.",phase="substitute",done="So the moment is 15 Nm."),
    box("Check by dividing back: 15 ÷ 0.3 = ",50,"Moment ÷ distance should return the force.",phase="substitute",done="Back to 50 N, so 15 Nm is right."),
  ]},
 {  # b1 F=20/0.4=50
  "unit":"N","display":"A moment of 20 Nm is produced by a force acting 0.4 m from a pivot. Calculate the force.",
  "solutions":[50],"accept":0.5,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(F = \\frac{M}{d}\\)","hint":"Rearrange to force = moment ÷ distance.",
  "misconceptions":[{"pattern":"inverse_error","check":"common","expect":8,
    "message":"Rearrange to F = M ÷ d = 20 ÷ 0.4 = 50 N. Multiplying (20 × 0.4 = 8) divides the wrong way round."}],
  "guided_steps":[
    say("Rearrange \\(M = F \\times d\\) to \\(F = M \\div d = 20 \\div 0.4\\)."),
    box("Dividing by 0.4 is awkward, so multiply both by 10. The moment 20 becomes 20 × 10 = ",200,"Times 10."),
    box("and 0.4 becomes 0.4 × 10 = ",4,"Times 10 as well.",phase="substitute"),
    box("So F = 200 ÷ 4 = ",50,"How many 4s in 200?",phase="substitute",done="Force = 50 N."),
    box("Check: 50 × 0.4 = ",20,"Force × distance should give the moment.",phase="substitute",done="Back to 20 Nm, so 50 N is right."),
  ]},
 {  # b2 d=12/30=0.4
  "unit":"m","display":"A force of 30 N creates a moment of 12 Nm. Calculate the perpendicular distance from the pivot.",
  "solutions":[0.4],"accept":0.02,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(d = \\frac{M}{F}\\)","hint":"Rearrange to distance = moment ÷ force.",
  "misconceptions":[{"pattern":"wrong_rearrange","check":"common","expect":2.5,
    "message":"Distance = M ÷ F = 12 ÷ 30 = 0.4 m. Dividing the other way (30 ÷ 12 = 2.5) inverts the equation."}],
  "guided_steps":[
    say("Rearrange to \\(d = M \\div F = 12 \\div 30\\)."),
    box("12 ÷ 30 is less than 1. Simplify the fraction 12/30: top, 12 ÷ 6 = ",2,"Divide the top by 6."),
    box("bottom, 30 ÷ 6 = ",5,"Divide the bottom by 6, so the fraction is 2/5.",phase="substitute"),
    box("2/5 as a decimal is 2 ÷ 5 = ",0.4,"Two fifths.",phase="substitute",done="Distance = 0.4 m."),
    box("Check: 30 × 0.4 = ",12,"Force × distance should give the moment.",phase="substitute",done="Back to 12 Nm, so 0.4 m is right."),
  ]},
 {  # b3 M=200x1.5=300
  "unit":"Nm","display":"A spanner applies a force of 200 N at a distance of 1.5 m from the bolt. Calculate the moment about the bolt.",
  "solutions":[300],"accept":1,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(M = F \\times d\\)","hint":"Multiply the force by the distance.",
  "misconceptions":[{"pattern":"inverse_error","check":"common","expect":133.33,
    "message":"Moment = 200 × 1.5 = 300 Nm. Dividing (200 ÷ 1.5 = 133.3) is the wrong operation."}],
  "guided_steps":[
    say("\\(M = F \\times d\\). Force 200 N, distance 1.5 m."),
    box("Multiply the whole numbers first: 200 × 15 = ",3000,"200 times 15."),
    box("1.5 has one decimal place, so 3000 ÷ 10 = ",300,"Divide by 10.",phase="substitute",done="Moment = 300 Nm."),
    box("Check: 300 ÷ 1.5 = ",200,"Moment ÷ distance should give the force.",phase="substitute",done="Back to 200 N, so 300 Nm is right."),
  ]},
 {  # b4 F=36/0.6=60
  "unit":"N","display":"A moment of 36 Nm acts on a door handle. The handle is 0.6 m from the hinge. Calculate the force applied.",
  "solutions":[60],"accept":0.5,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(F = \\frac{M}{d}\\)","hint":"Rearrange to force = moment ÷ distance.",
  "misconceptions":[{"pattern":"inverse_error","check":"common","expect":21.6,
    "message":"Rearrange to F = M ÷ d = 36 ÷ 0.6 = 60 N. Multiplying (36 × 0.6 = 21.6) is the slip."}],
  "guided_steps":[
    say("Rearrange to \\(F = M \\div d = 36 \\div 0.6\\)."),
    box("Multiply both by 10 to clear the decimal: 36 becomes ",360,"Times 10."),
    box("and 0.6 becomes ",6,"Times 10.",phase="substitute"),
    box("F = 360 ÷ 6 = ",60,"How many 6s in 360?",phase="substitute",done="Force = 60 N."),
    box("Check: 60 × 0.6 = ",36,"Force × distance should give the moment.",phase="substitute",done="Back to 36 Nm, so 60 N is right."),
  ]},
 {  # b5 M=80x0.25=20
  "unit":"Nm","display":"A force of 80 N acts at a perpendicular distance of 0.25 m from a pivot. Calculate the moment.",
  "solutions":[20],"accept":0.5,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(M = F \\times d\\)","hint":"Multiply 80 by 0.25 (a quarter).",
  "misconceptions":[{"pattern":"inverse_error","check":"common","expect":320,
    "message":"Moment = 80 × 0.25 = 20 Nm. Dividing (80 ÷ 0.25 = 320) is the wrong way round."}],
  "guided_steps":[
    say("\\(M = F \\times d\\). Force 80 N, distance 0.25 m."),
    box("Multiply the digits: 80 × 25 = ",2000,"80 times 25."),
    box("0.25 has two decimal places, so divide by 100: 2000 ÷ 100 = ",20,"Two decimal places means ÷ 100.",phase="substitute",done="Moment = 20 Nm."),
    box("Check: 20 ÷ 0.25 = ",80,"Dividing by a quarter is the same as ×4.",phase="substitute",done="Back to 80 N, so 20 Nm is right."),
  ]},
 {  # b6 d=45/15=3
  "unit":"m","display":"A force of 15 N creates a moment of 45 Nm. Calculate the perpendicular distance from the pivot.",
  "solutions":[3],"accept":0.1,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(d = \\frac{M}{F}\\)","hint":"Rearrange to distance = moment ÷ force.",
  "misconceptions":[{"pattern":"wrong_rearrange","check":"common","expect":0.33,
    "message":"Distance = M ÷ F = 45 ÷ 15 = 3 m. Dividing the other way (15 ÷ 45 = 0.33) inverts it."}],
  "guided_steps":[
    say("Rearrange to \\(d = M \\div F = 45 \\div 15\\). Build up in fifteens."),
    box("Two lots of 15: 15 × 2 = ",30,"Two 15s."),
    box("That is still short of 45. 45 − 30 = ",15,"How much is left?",phase="substitute"),
    box("That leaves exactly one more 15, so 45 ÷ 15 = ",3,"Two 15s plus one more 15.",phase="substitute",done="Distance = 3 m."),
  ]},
 {  # b7 balance 400x2=F x1.6 ->500
  "unit":"N","display":"A seesaw is balanced. A 400 N force acts 2.0 m from the pivot on the left. A force acts 1.6 m from the pivot on the right. What is the force on the right?",
  "solutions":[500],"accept":1,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(F_1 d_1 = F_2 d_2\\)","hint":"Balance the moments: 400 × 2.0 = F × 1.6, then divide.",
  "misconceptions":[{"pattern":"wrong_rearrange","check":"common","expect":320,
    "message":"Balance the moments: 400 × 2.0 = F × 1.6, so F = 800 ÷ 1.6 = 500 N. Swapping the distances (400 × 1.6 ÷ 2.0 = 320) mixes up which arm is which."}],
  "guided_steps":[
    say("Balanced beam: clockwise moment = anticlockwise moment. Find the left moment first."),
    box("Left moment = 400 × 2.0 = ",800,"Force × distance."),
    say("The right side must match: F × 1.6 = 800, so F = 800 ÷ 1.6. Clear the decimal by ×10: 8000 ÷ 16."),
    box("8000 ÷ 16 = ",500,"How many 16s in 8000?",phase="substitute",done="Force = 500 N."),
    box("Check: 500 × 1.6 = ",800,"This should equal the left moment.",phase="substitute",done="Matches, so 500 N balances it."),
  ]},
]

# ---------- SILVER ----------
silver = [
 {  # s0 child/adult seesaw d=1.0
  "unit":"m","display":SVG_S0+"A child of mass 30 kg sits 2.0 m from the pivot of a seesaw. An adult of mass 60 kg sits on the other side. How far from the pivot must the adult sit to balance? (g = 9.8 N/kg)",
  "solutions":[1],"accept":0.05,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(F_1 d_1 = F_2 d_2\\) where \\(F = mg\\)","hint":"Turn masses into weights, then balance the moments.",
  "misconceptions":[
    {"pattern":"wrong_rearrange","check":"common","expect":4,
     "message":"Each side is weight × its own distance: 294 × 2.0 = 588 × d, so d = 1.0 m. Pairing the adult's weight with the child's distance instead gives d = 4.0 m, which unbalances the seesaw."},
    {"pattern":"used_mass","check":"common","expect":None,
     "message":"Here mass and weight give the same distance because g cancels on both sides, but always turn mass into weight (W = mg) in the moment equation as a habit."}],
  "guided_steps":[
    say("Turn the masses into weights with \\(W = mg\\), g = 9.8 N/kg."),
    box("Child's weight = 30 × 9.8 = ",294,"Mass × 9.8."),
    box("Adult's weight = 60 × 9.8 = ",588,"Mass × 9.8."),
    say("Balance: child's moment = adult's moment. Child's moment = 294 × 2.0."),
    box("294 × 2.0 = ",588,"Weight × distance."),
    say("So 588 = 588 × d. Rearrange: d = 588 ÷ 588."),
    box("588 ÷ 588 = ",1,"A number divided by itself.",phase="substitute",done="Distance = 1.0 m."),
    box("Check: 588 × 1.0 = ",588,"This should equal the child's moment.",phase="substitute",done="Equals 588 Nm, so 1.0 m balances it."),
  ]},
 {  # s1 600x0.8=Fx1.2 ->400
  "unit":"N","display":"A 600 N force acts 0.8 m from a pivot (clockwise). What force at 1.2 m from the pivot (anticlockwise) is needed to balance it?",
  "solutions":[400],"accept":1,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(F_1 d_1 = F_2 d_2\\)","hint":"Balance: 600 × 0.8 = F × 1.2, then divide by 1.2.",
  "misconceptions":[
    {"pattern":"forgot_step","check":"common","expect":480,
     "message":"480 Nm is the clockwise moment (600 × 0.8). You still divide by 1.2 m to get the balancing force: 480 ÷ 1.2 = 400 N."},
    {"pattern":"wrong_rearrange","check":"common","expect":900,
     "message":"Balance: 600 × 0.8 = F × 1.2, so F = 480 ÷ 1.2 = 400 N. Swapping the distances (600 × 1.2 ÷ 0.8 = 900) uses the wrong arm."}],
  "guided_steps":[
    say("Balanced beam: clockwise moment = anticlockwise moment. Left moment first."),
    box("600 × 0.8 = ",480,"Force × distance."),
    say("Match on the right: F × 1.2 = 480, so F = 480 ÷ 1.2. Clear the decimal by ×10: 4800 ÷ 12."),
    box("4800 ÷ 12 = ",400,"How many 12s in 4800?",phase="substitute",done="Force = 400 N."),
    box("Check: 400 × 1.2 = ",480,"This should equal the clockwise moment.",phase="substitute",done="Matches, so 400 N balances it."),
  ]},
 {  # s2 nutcracker F=9.8
  "unit":"N","display":"A nutcracker has the nut 0.08 m from the pivot and the handle 0.4 m from the pivot. A 5 kg mass is placed in the nutcracker. Calculate the force you need to apply at the handle to crack it. (g = 9.8 N/kg)",
  "solutions":[9.8],"accept":0.1,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(F_1 d_1 = F_2 d_2\\)","hint":"Find the load's weight first, then balance the moments.",
  "misconceptions":[
    {"pattern":"used_mass","check":"common","expect":1,
     "message":"Use weight, not mass: W = 5 × 9.8 = 49 N. Then 49 × 0.08 = F × 0.4 gives F = 9.8 N. Using the mass 5 kg instead gives F = 1.0 N, ten times too small."}],
  "guided_steps":[
    say("First the load's weight: \\(W = mg = 5 \\times 9.8\\)."),
    box("5 × 9.8 = ",49,"Mass × 9.8."),
    say("That weight sits 0.08 m from the pivot, so its moment = 49 × 0.08."),
    box("49 × 0.08 = ",3.92,"49 × 8 = 392, then two decimal places."),
    say("Your effort at 0.4 m must match: F × 0.4 = 3.92, so F = 3.92 ÷ 0.4."),
    box("3.92 ÷ 0.4 = ",9.8,"Times 10 on both: 39.2 ÷ 4.",phase="substitute",done="Effort = 9.8 N."),
    box("Check: 9.8 × 0.4 = ",3.92,"This should equal the load's moment.",phase="substitute",done="Matches, so 9.8 N is right."),
  ]},
 {  # s3 resultant 300-200=100
  "unit":"Nm","display":"A beam has a pivot in the centre. A 200 N force acts 1.0 m to the left of the pivot. A 150 N force acts 2.0 m to the right. Calculate the resultant moment. State the direction (clockwise or anticlockwise). Give your answer as the magnitude only.",
  "solutions":[100],"accept":1,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(M = F \\times d\\)","hint":"Work out both moments and subtract the smaller from the larger.",
  "misconceptions":[
    {"pattern":"forgot_direction","check":"common","expect":500,
     "message":"The moments oppose, so subtract: 300 − 200 = 100 Nm clockwise. Adding them (200 + 300 = 500) ignores that they turn opposite ways."}],
  "guided_steps":[
    say("Work out each moment, then find the difference. \\(M = F \\times d\\)."),
    box("Anticlockwise (left): 200 × 1.0 = ",200,"Force × distance."),
    box("Clockwise (right): 150 × 2.0 = ",300,"Force × distance."),
    say("They turn opposite ways, so the resultant is the difference, in the direction of the larger."),
    box("300 − 200 = ",100,"Bigger moment minus smaller.",phase="substitute",done="Resultant = 100 Nm clockwise."),
    box("Sanity check: the larger moment minus the resultant should equal the opposing moment. 300 − 100 = ",200,"This should match the anticlockwise moment.",phase="substitute",done="Equals 200 Nm, so 100 Nm is the leftover turning effect."),
  ]},
 {  # s4 8kg at 0.25 -> 19.6
  "unit":"Nm","display":"An 8 kg mass hangs from a horizontal bar at a distance of 0.25 m from the pivot. Calculate the moment about the pivot. (g = 9.8 N/kg)",
  "solutions":[19.6],"accept":0.1,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(M = F \\times d\\) where \\(F = mg\\)","hint":"Find the weight (mg) first, then multiply by the distance.",
  "misconceptions":[
    {"pattern":"used_mass","check":"common","expect":2,
     "message":"Find the weight first: W = 8 × 9.8 = 78.4 N, then M = 78.4 × 0.25 = 19.6 Nm. Using the mass 8 kg gives 8 × 0.25 = 2.0 Nm, which leaves out gravity."}],
  "guided_steps":[
    say("Turn the mass into weight: \\(W = mg = 8 \\times 9.8\\)."),
    box("8 × 9.8 = ",78.4,"Mass × 9.8."),
    say("Now the moment of that weight at 0.25 m: M = 78.4 × 0.25."),
    box("0.25 is a quarter, so 78.4 ÷ 4 = ",19.6,"A quarter of 78.4.",phase="substitute",done="Moment = 19.6 Nm."),
    box("Check: 19.6 ÷ 0.25 = ",78.4,"Dividing by a quarter is the same as ×4.",phase="substitute",done="Back to the weight, so 19.6 Nm is right."),
  ]},
 {  # s5 wheelbarrow 150x0.4=Fx1.2 ->50
  "unit":"N","display":"A wheelbarrow has its load of 150 N at 0.4 m from the wheel (pivot). The handles are 1.2 m from the wheel. Calculate the effort needed at the handles to lift the load.",
  "solutions":[50],"accept":0.5,"calculator":True,"higher_only":False,"input_type":"single_value",
  "equation_hint":"\\(F_1 d_1 = F_2 d_2\\)","hint":"Balance the load and effort moments, then divide.",
  "misconceptions":[
    {"pattern":"forgot_step","check":"common","expect":60,
     "message":"60 Nm is the load's moment (150 × 0.4). Divide by the handle distance 1.2 m to get the effort: 50 N."},
    {"pattern":"wrong_rearrange","check":"common","expect":450,
     "message":"Balance: 150 × 0.4 = F × 1.2, so F = 60 ÷ 1.2 = 50 N. Swapping the distances (150 × 1.2 ÷ 0.4 = 450) uses the wrong arms."}],
  "guided_steps":[
    say("Lever balance: load moment = effort moment. Load moment first."),
    box("150 × 0.4 = ",60,"Load force × its distance."),
    say("Effort at 1.2 m must match: F × 1.2 = 60, so F = 60 ÷ 1.2. Clear the decimal by ×10: 600 ÷ 12."),
    box("600 ÷ 12 = ",50,"How many 12s in 600?",phase="substitute",done="Effort = 50 N."),
    box("Check: 50 × 1.2 = ",60,"This should equal the load moment.",phase="substitute",done="Matches, so 50 N lifts it."),
  ]},
]

# ---------- GOLD ----------
gold = [
 {  # g0 multi-force beam ->500
  "unit":"N","display":SVG_G0+"A beam is balanced on a pivot. On the left side: a 100 N force acts 0.5 m from the pivot, and a 200 N force acts 1.5 m from the pivot. What single force on the right, at 0.7 m from the pivot, is needed to balance the beam?",
  "solutions":[500],"accept":1,"calculator":True,"higher_only":False,"input_type":"single_value",
  "hint":"Add both left moments, then balance against F × 0.7.",
  "misconceptions":[
    {"pattern":"forgot_step","check":"common","expect":350,
     "message":"350 Nm is the total left moment: (100 × 0.5) + (200 × 1.5). Divide by 0.7 m to get the balancing force: 500 N."},
    {"pattern":"single_force","check":"common","expect":None,
     "message":"With two forces on one side, work out each moment and add them: 50 + 300 = 350 Nm. Using only one force loses part of the turning effect."}],
  "guided_steps":[
    say("Two forces on the left, so add their moments, then balance the right."),
    box("First force: 100 × 0.5 = ",50,"Force × distance."),
    box("Second force: 200 × 1.5 = ",300,"Force × distance."),
    box("Total left moment: 50 + 300 = ",350,"Add both moments."),
    say("The right force at 0.7 m must match: F × 0.7 = 350, so F = 350 ÷ 0.7. Clear the decimal by ×10: 3500 ÷ 7."),
    box("3500 ÷ 7 = ",500,"How many 7s in 3500?",phase="substitute",done="Force = 500 N."),
    box("Check: 500 × 0.7 = ",350,"This should equal the total left moment.",phase="substitute",done="Matches, so 500 N balances it."),
  ]},
 {  # g1 gear speed 40
  "unit":"rpm","display":"A gear system has a driver gear with 20 teeth and a driven gear with 60 teeth. The driver gear rotates at 120 rpm. Calculate the speed of the driven gear in rpm.",
  "solutions":[40],"accept":0.5,"calculator":True,"higher_only":False,"input_type":"single_value",
  "hint":"Gear ratio = 60 ÷ 20; divide the speed by it.",
  "misconceptions":[
    {"pattern":"multiplied","check":"common","expect":360,
     "message":"A larger driven gear turns slower, so divide: 120 ÷ 3 = 40 rpm. Multiplying (120 × 3 = 360) speeds it up instead."},
    {"pattern":"inverse_ratio","check":"common","expect":None,
     "message":"Gear ratio = driven ÷ driver = 60 ÷ 20 = 3, then divide the input speed by the ratio."}],
  "guided_steps":[
    say("Gears change speed by the gear ratio. Gear ratio = driven teeth ÷ driver teeth."),
    box("Gear ratio = 60 ÷ 20 = ",3,"Driven 60, driver 20."),
    say("A bigger driven gear turns slower, so divide the input speed by the ratio."),
    box("120 ÷ 3 = ",40,"Input speed ÷ ratio.",phase="substitute",done="Driven gear speed = 40 rpm."),
    box("Check: 40 × 3 = ",120,"This should return the driver's speed.",phase="substitute",done="Back to 120 rpm, so 40 rpm is right."),
  ]},
 {  # g2 gear force 45
  "unit":"N","display":"A gear system has a driver gear with 20 teeth and a driven gear with 60 teeth. If the input force is 15 N, calculate the output force (assuming no energy losses).",
  "solutions":[45],"accept":0.5,"calculator":True,"higher_only":False,"input_type":"single_value",
  "hint":"Gear ratio = 60 ÷ 20; multiply the force by it.",
  "misconceptions":[
    {"pattern":"divided","check":"common","expect":5,
     "message":"A larger driven gear gives more force, so multiply: 15 × 3 = 45 N. Dividing (15 ÷ 3 = 5) shrinks the force instead."},
    {"pattern":"inverse_ratio","check":"common","expect":None,
     "message":"Gear ratio = driven ÷ driver = 60 ÷ 20 = 3, then multiply the input force by the ratio."}],
  "guided_steps":[
    say("Gears also change force by the gear ratio. Gear ratio = driven teeth ÷ driver teeth."),
    box("Gear ratio = 60 ÷ 20 = ",3,"Driven 60, driver 20."),
    say("A bigger driven gear gives more force, so multiply the input force by the ratio."),
    box("15 × 3 = ",45,"Input force × ratio.",phase="substitute",done="Output force = 45 N."),
    box("Check: 45 ÷ 3 = ",15,"This should return the input force.",phase="substitute",done="Back to 15 N, so 45 N is right."),
  ]},
 {  # g3 uniform beam F=17
  "unit":"N","display":SVG_G3+"A uniform beam is 2.0 m long with mass 10 kg. The pivot is 0.8 m from the left end. A 50 N load hangs from the left end. Calculate the force needed at the right end to balance the beam. (g = 9.8 N/kg)",
  "solutions":[17],"accept":0.3,"calculator":True,"higher_only":False,"input_type":"single_value",
  "hint":"Include the beam's own weight at its centre, then balance.",
  "misconceptions":[
    {"pattern":"forgot_beam_weight","check":"common","expect":33.33,
     "message":"The beam's own weight (10 × 9.8 = 98 N) makes a clockwise moment of 98 × 0.2 = 19.6 Nm. Leaving it out gives 50 × 0.8 = F × 1.2, so F = 33.3 N instead of 17 N."},
    {"pattern":"forgot_centre","check":"common","expect":None,
     "message":"A uniform beam's weight acts at its centre, 1.0 m from the left end, which is 0.2 m from the pivot."}],
  "guided_steps":[
    say("Three forces act: the 50 N load (left of the pivot), the beam's own weight at its centre, and the unknown F (right of the pivot). Start with the beam's weight."),
    box("Beam weight = 10 × 9.8 = ",98,"Mass × 9.8."),
    say("The weight acts at the centre, 1.0 m from the left end. The pivot is at 0.8 m, so the weight is 1.0 − 0.8 = 0.2 m to the right of the pivot."),
    box("Anticlockwise moment (the 50 N load, 0.8 m left): 50 × 0.8 = ",40,"Force × distance."),
    box("Clockwise moment from the beam weight: 98 × 0.2 = ",19.6,"Weight × its distance from the pivot."),
    say("Balance: anticlockwise = clockwise, so 40 = 19.6 + F × 1.2. Take the beam's part across first."),
    box("40 − 19.6 = ",20.4,"This is the moment F must provide.",phase="substitute"),
    box("So F × 1.2 = 20.4, F = 20.4 ÷ 1.2 = ",17,"Times 10 on both: 204 ÷ 12.",phase="substitute",done="Force = 17 N."),
    box("Check: 19.6 + 17 × 1.2 = ",40,"This should equal the anticlockwise moment.",phase="substitute",done="Equals 40 Nm, so 17 N balances the beam."),
  ]},
 {  # g4 lever+gear 10.8
  "unit":"Nm","display":"A lever is connected to an input gear with 15 teeth. A force of 12 N is applied 0.3 m from the pivot on the lever. The output gear has 45 teeth. Calculate the output torque (moment) from the gear system in Nm.",
  "solutions":[10.8],"accept":0.1,"calculator":True,"higher_only":False,"input_type":"single_value",
  "hint":"Lever torque first, then multiply by the gear ratio.",
  "misconceptions":[
    {"pattern":"forgot_step","check":"common","expect":3.6,
     "message":"3.6 Nm is only the lever's input torque (12 × 0.3). The gears multiply it by the ratio 3: output torque = 3.6 × 3 = 10.8 Nm."},
    {"pattern":"inverse_ratio","check":"common","expect":1.2,
     "message":"More teeth on the output gear means more torque, so multiply: 3.6 × 3 = 10.8 Nm. Dividing (3.6 ÷ 3 = 1.2) is the wrong way."}],
  "guided_steps":[
    say("Two steps: the lever makes a torque, then the gears multiply it."),
    box("Input torque from the lever = 12 × 0.3 = ",3.6,"Force × distance."),
    box("Gear ratio = 45 ÷ 15 = ",3,"Output teeth ÷ input teeth."),
    say("More teeth on the output gear means more torque, so multiply."),
    box("3.6 × 3 = ",10.8,"Input torque × gear ratio.",phase="substitute",done="Output torque = 10.8 Nm."),
    box("Check: 10.8 ÷ 3 = ",3.6,"This should return the input torque.",phase="substitute",done="Back to 3.6 Nm, so 10.8 Nm is right."),
  ]},
 {  # g5 crowbar 1200
  "unit":"N","display":"A crowbar is used to lift a heavy stone. The effort of 80 N is applied 0.75 m from the pivot. The stone rests 0.05 m from the pivot. Calculate the maximum force exerted on the stone.",
  "solutions":[1200],"accept":2,"calculator":True,"higher_only":False,"input_type":"single_value",
  "hint":"Balance effort and load moments, then divide by 0.05.",
  "misconceptions":[
    {"pattern":"forgot_step","check":"common","expect":60,
     "message":"60 Nm is the effort's moment (80 × 0.75). Divide by the load distance 0.05 m to get the force on the stone: 1200 N."},
    {"pattern":"inverse_error","check":"common","expect":None,
     "message":"The load is much closer to the pivot, so the force is multiplied. Mechanical advantage = 0.75 ÷ 0.05 = 15, and 80 × 15 = 1200 N."}],
  "guided_steps":[
    say("A crowbar is a lever: effort moment = load moment. Effort moment first."),
    box("80 × 0.75 = ",60,"Effort force × effort distance."),
    say("The stone is only 0.05 m from the pivot. F × 0.05 = 60, so F = 60 ÷ 0.05. Dividing by 0.05 is the same as ×20."),
    box("60 × 20 = ",1200,"0.05 goes into 1 twenty times.",phase="substitute",done="Force on the stone = 1200 N."),
    box("Check: 1200 × 0.05 = ",60,"This should equal the effort moment.",phase="substitute",done="Matches, so 1200 N is right."),
  ]},
]

# ---------- tier guides / opener / teach ----------
tier_guides = {
 "bronze":{"title":"Bronze: one moment, straight in","steps":[
   "A moment is the turning effect of a force: \\(M = F \\times d\\), measured in newton metres (Nm).",
   "The distance d is measured perpendicular to the force, from the pivot, and must be in metres. Convert cm to m first (divide by 100).",
   "Rearrange when the unknown is not the moment: \\(F = M \\div d\\) or \\(d = M \\div F\\)."],
   "example":{"question":"A force of 60 N acts 0.4 m from a pivot. Find the moment.","steps":[
     {"label":"Equation","content":"<p>\\(M = F \\times d\\)</p>"},
     {"label":"Substitute","content":"<p>\\(M = 60 \\times 0.4\\)</p>"},
     {"label":"Check","content":"<p>60 × 0.4 = 24, and 24 ÷ 0.4 = 60</p>"},
     {"label":"Answer","content":"<p><strong>24 Nm</strong></p>","isAnswer":True,"is_answer":True}]}},
 "silver":{"title":"Silver: convert or rearrange first","steps":[
   "If a value is given as a mass, turn it into weight before using it: \\(W = mg\\), with g = 9.8 N/kg.",
   "For a balanced beam or lever, clockwise moment = anticlockwise moment. Set \\(F_1 d_1 = F_2 d_2\\) and rearrange for the unknown.",
   "For a resultant, work out each moment separately, then subtract the smaller from the larger."],
   "example":{"question":"A 5 kg mass hangs 0.4 m from a pivot. Find its moment. (g = 9.8 N/kg)","steps":[
     {"label":"Weight","content":"<p>\\(W = 5 \\times 9.8 = 49\\) N</p>"},
     {"label":"Moment","content":"<p>\\(M = 49 \\times 0.4\\)</p>"},
     {"label":"Check","content":"<p>49 × 0.4 = 19.6</p>"},
     {"label":"Answer","content":"<p><strong>19.6 Nm</strong></p>","isAnswer":True,"is_answer":True}]}},
 "gold":{"title":"Gold: chain the steps","steps":[
   "Add up several moments on one side before balancing, or bring in the beam's own weight acting at its centre.",
   "Gears change a torque: gear ratio = driven teeth ÷ driver teeth. More teeth means more force (multiply) but slower turning (divide for speed).",
   "Two ideas often chain: a lever makes a torque, then a gear scales it. Do them in order."],
   "example":{"question":"A 10 N force acts 0.5 m from a lever pivot, driving a 10-tooth gear into a 30-tooth gear. Find the output torque.","steps":[
     {"label":"Input torque","content":"<p>10 × 0.5 = 5 Nm</p>"},
     {"label":"Gear ratio","content":"<p>30 ÷ 10 = 3</p>"},
     {"label":"Check","content":"<p>5 × 3 = 15</p>"},
     {"label":"Answer","content":"<p><strong>15 Nm</strong></p>","isAnswer":True,"is_answer":True}]}},
}

guided = {
 "opener":{"label":"Before any equations","display":SVG_OPENER+"A seesaw balances. On the left, a 10 N push acts 2 m from the middle. On the right you push down only 1 m from the middle, half as far out.",
   "steps":[
     box("Closer in, so you need a bigger push. Half the distance means double the force. How many newtons on the right? ",20,"The 10 N was twice as far out, so the closer push must be twice as big."),
     say("You just made 10 × 2 = 20 × 1: force times distance, matched on both sides. That product, <strong>force × distance</strong>, is the <strong>moment</strong>, the turning effect. Every balance question is moment = moment, and every moment is \\(M = F \\times d\\).")]},
 "teach":{
   "bronze":{"label":"Together: your first one","display":"A force of 150 N acts 20 cm from a pivot. (a) Find the moment. (b) What force at 0.6 m would give the same moment?",
     "steps":[
       say("\\(M = F \\times d\\), but the distance must be in metres first."),
       box("Convert: 20 cm ÷ 100 = ",0.2,"There are 100 cm in a metre."),
       box("Moment = 150 × 0.2 = ",30,"Force × distance, in Nm."),
       say("Part (b): the same 30 Nm, but now over 0.6 m. Rearrange \\(F = M \\div d\\)."),
       box("F = 30 ÷ 0.6 = ",50,"Divide the moment by the new distance.",phase="substitute"),
       box("Check: 50 × 0.6 = ",30,"Force × distance should give the moment back.",done="Same 30 Nm, so 50 N is right. Bigger distance, smaller force.")]},
   "silver":{"label":"Together: weigh it first","display":"A 4 kg mass hangs 0.5 m from a pivot on one side of a balanced beam. On the other side a force acts 0.4 m from the pivot. Find that force. (g = 9.8 N/kg)",
     "steps":[
       say("First turn the mass into weight: \\(W = mg\\)."),
       box("W = 4 × 9.8 = ",39.2,"Mass × gravitational field strength."),
       say("That weight makes a moment at 0.5 m."),
       box("Left moment = 39.2 × 0.5 = ",19.6,"Weight × distance."),
       say("Balance: the right force at 0.4 m must give the same moment. Rearrange \\(F = M \\div d\\)."),
       box("F = 19.6 ÷ 0.4 = ",49,"Divide the moment by 0.4.",phase="substitute"),
       box("Check: 49 × 0.4 = ",19.6,"This should equal the left moment.",done="Equals 19.6 Nm, so 49 N balances it.")]},
   "gold":{"label":"Together: lever into gear","display":"A 20 N force is applied 0.4 m from a lever pivot, driving an input gear of 10 teeth. The output gear has 40 teeth. Find the output torque.",
     "steps":[
       say("Two steps: first the lever's torque, then the gears multiply it."),
       box("Input torque = 20 × 0.4 = ",8,"Force × distance."),
       say("The gears change the torque. Gear ratio = output teeth ÷ input teeth."),
       box("Gear ratio = 40 ÷ 10 = ",4,"Divide the driven teeth by the driver teeth."),
       say("More teeth on the output means more torque, so multiply."),
       box("Output torque = 8 × 4 = ",32,"Input torque × gear ratio.",phase="substitute"),
       box("Check: 32 ÷ 4 = ",8,"This should return the input torque.",done="Back to 8 Nm, so 32 Nm is right.")]},
 },
}

method_card = {
 "title":"Moments, Levers and Gears",
 "steps":[
   "Identify the pivot and which forces turn clockwise vs anticlockwise",
   "If given a mass, find its weight first with W = mg",
   "For a balanced beam or lever: set clockwise moment = anticlockwise moment",
   "For gears: gear ratio = driven teeth ÷ driver teeth"],
 "content":("<p>A <strong>moment</strong> is the turning effect of a force: \\(M = F \\times d\\), in newton metres (Nm).</p>"
  "<p>The distance is measured <strong>perpendicular</strong> to the force, from the pivot, and must be in metres.</p>"
  "<p>For a <strong>balanced</strong> beam or lever, clockwise moment = anticlockwise moment. If several forces act on one side, work out each moment and add them. Given a mass, find its weight first with \\(W = mg\\).</p>"
  "<p>For <strong>gears</strong>, the gear ratio = driven teeth ÷ driver teeth. A larger driven gear turns slower but with more force.</p>"),
}

exam_context = {
 "marks":"3–5 per calculation",
 "paper":"Paper 1 (Physics)",
 "frequency":"Common: appears frequently on Paper 1",
}

worked_examples = [
 {"difficulty":"Bronze","question":"A force of 50 N acts at a perpendicular distance of 0.3 m from a pivot. Calculate the moment.",
  "steps":[
    {"label":"Step 1: Recall the equation","content":"<p>\\(M = F \\times d\\)</p>"},
    {"label":"Step 2: Substitute","content":"<p>\\(M = 50 \\times 0.3\\)</p>"},
    {"label":"Answer","content":"<p>Moment = <strong>15 Nm</strong></p>","is_answer":True}]},
 {"difficulty":"Silver","question":"A child of mass 30 kg sits 2.0 m from the pivot of a seesaw. An adult of mass 60 kg sits on the other side. How far from the pivot must the adult sit to balance the seesaw? (g = 9.8 N/kg)",
  "steps":[
    {"label":"Step 1: Calculate weights","content":"<p>Child: W = 30 × 9.8 = 294 N</p><p>Adult: W = 60 × 9.8 = 588 N</p>"},
    {"label":"Step 2: Apply principle of moments","content":"<p>Clockwise = anticlockwise</p><p>588 × d = 294 × 2.0</p>"},
    {"label":"Step 3: Solve for d","content":"<p>588d = 588</p><p>d = 588 ÷ 588</p>"},
    {"label":"Answer","content":"<p>d = <strong>1.0 m</strong></p>","is_answer":True}]},
 {"difficulty":"Gold","question":"A uniform beam is 2.0 m long and has a mass of 10 kg. The pivot is 0.8 m from the left end. A 50 N load hangs from the left end. Calculate the force needed at the right end to balance the beam. (g = 9.8 N/kg)",
  "steps":[
    {"label":"Step 1: Find weight of beam","content":"<p>W = 10 × 9.8 = 98 N, acting at the centre (1.0 m from left end)</p>"},
    {"label":"Step 2: Find distances from pivot","content":"<p>50 N load: 0.8 m from pivot (anticlockwise)</p><p>Beam weight 98 N: centre is at 1.0 m from left, so 1.0 − 0.8 = 0.2 m from pivot (clockwise)</p><p>Unknown force F: 2.0 − 0.8 = 1.2 m from pivot (clockwise)</p>"},
    {"label":"Step 3: Apply principle of moments","content":"<p>ACW: 50 × 0.8 = 40 Nm</p><p>CW: (98 × 0.2) + (F × 1.2) = 19.6 + 1.2F</p><p>40 = 19.6 + 1.2F</p>"},
    {"label":"Step 4: Solve","content":"<p>1.2F = 40 − 19.6 = 20.4</p><p>F = 20.4 ÷ 1.2</p>"},
    {"label":"Answer","content":"<p>F = <strong>17 N</strong></p>","is_answer":True}]},
]

pd = {
 "method_card":method_card,
 "topic_links":{"prerequisites":[]},
 "exam_context":exam_context,
 "tier_guides":tier_guides,
 "guided":guided,
 "problem_bank":{
   "bronze":bronze,"silver":silver,"gold":gold,
   "bronze_description":"One equation, values already in the right units: use M = F × d or rearrange it.",
   "silver_description":"Convert a mass to weight first, or balance two moments and rearrange for the unknown.",
   "gold_description":"Multi-step: add several moments, include the beam's own weight, or chain a lever into a gear system.",
 },
 "related_videos":[],
 "worked_examples":worked_examples,
}

# ---------- arithmetic self-check ----------
import math
def approx(a,b,t=1e-9): return abs(a-b)<=t
for t,probs in (("bronze",bronze),("silver",silver),("gold",gold)):
    for i,p in enumerate(probs):
        for st in p["guided_steps"]:
            if st.get("answer") is not None:
                assert isinstance(st["answer"],(int,float)), (t,i,st)
for tt in ("bronze","silver","gold"):
    for st in guided["teach"][tt]["steps"]:
        if st.get("answer") is not None:
            assert isinstance(st["answer"],(int,float))
for st in guided["opener"]["steps"]:
    if st.get("answer") is not None:
        assert isinstance(st["answer"],(int,float))

out = "lesson_%s.json" % KEY
json.dump(pd, io.open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("WROTE", out)
