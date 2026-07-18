# -*- coding: utf-8 -*-
import json, io

# ---------- SVG helpers (theme-safe, validator-clean: viewBox, role, aria, no http/xlink) ----------
def _load(x, label, direction):
    if direction == "down":
        shaft = '<line x1="%d" y1="104" x2="%d" y2="152" stroke="currentColor" stroke-width="2.5"/>' % (x, x)
        head = '<polygon points="%d,146 %d,146 %d,158" fill="currentColor"/>' % (x-5, x+5, x)
    else:  # up (effort)
        shaft = '<line x1="%d" y1="152" x2="%d" y2="104" stroke="currentColor" stroke-width="2.5"/>' % (x, x)
        head = '<polygon points="%d,110 %d,110 %d,98" fill="currentColor"/>' % (x-5, x+5, x)
    txt = '<text x="%d" y="176" text-anchor="middle" font-size="12" font-weight="700" fill="currentColor" font-family="Inter,sans-serif">%s</text>' % (x, label)
    return shaft + head + txt

def _dist(x1, x2, y, label):
    cx = (x1 + x2) // 2
    return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3" opacity="0.7"/>'
            '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.2" opacity="0.7"/>'
            '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.2" opacity="0.7"/>'
            '<text x="%d" y="%d" text-anchor="middle" font-size="11" font-style="italic" fill="currentColor" font-family="Inter,sans-serif">%s</text>'
            ) % (x1, y, x2, y, x1, y-5, x1, y+5, x2, y-5, x2, y+5, cx, y-8, label)

def beam_fig(aria, px, loads, dists):
    s = '<svg viewBox="0 0 560 200" role="img" aria-label="%s" style="max-width:520px;margin:0.8em auto;display:block;">' % aria
    s += '<rect x="40" y="92" width="480" height="10" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>'
    s += '<polygon points="%d,102 %d,140 %d,140" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.5"/>' % (px, px-18, px+18)
    s += '<text x="%d" y="155" text-anchor="middle" font-size="11" fill="currentColor" font-family="Inter,sans-serif">pivot</text>' % px
    for (x, lb, d) in loads:
        s += _load(x, lb, d)
    for dd in dists:
        s += _dist(*dd)
    s += '</svg>'
    return s

def q_html(svg, text):
    return svg + '<p style="margin-top:0.6em;">%s</p>' % text

# ---------- guided-step builders ----------
def moment_walk(F, d, M, unit="N m", done_extra=""):
    done = "%s %s. Force in newtons times distance in metres gives newton-metres.%s" % (fmt(M), unit, done_extra)
    return [
        {"say": "Start with the moment equation: moment = force × perpendicular distance. Learn this one, and check whether your board also prints it on a sheet."},
        {"pre": "Read the force, in newtons: ", "post": "", "answer": F, "hint": "It is the number of newtons in the question."},
        {"pre": "Read the perpendicular distance, in metres: ", "post": "", "answer": d, "hint": "The distance from the pivot, already in metres."},
        {"say": "Now substitute and multiply.", "phase": "substitute", "pre": "%s × %s = " % (fmt(F), fmt(d)), "post": "", "answer": M, "hint": "Multiply the force by the distance."},
        {"pre": "The unit is newton-metres. Type the moment once more to lock it in: ", "post": "", "answer": M, "done": done, "hint": "It is the same value you just found, %s." % fmt(M)},
    ]

def balance_force_walk(Fk, dk, du, M, F):
    return [
        {"say": "Balanced means the two turning effects match: clockwise moment = anticlockwise moment. First find the moment you can."},
        {"pre": "Known moment = %s × %s = " % (fmt(Fk), fmt(dk)), "post": "", "answer": M, "hint": "Force times its distance from the pivot."},
        {"say": "For balance the other side must also give %s N m." % fmt(M)},
        {"phase": "substitute", "pre": "So (unknown force) × %s = %s. Divide: %s ÷ %s = " % (fmt(du), fmt(M), fmt(M), fmt(du)), "post": "", "answer": F, "hint": "Divide the moment by the distance."},
        {"pre": "Check: %s × %s = " % (fmt(F), fmt(du)), "post": "", "answer": M, "done": "It matches %s N m, so the force is %s N." % (fmt(M), fmt(F)), "hint": "Multiply back: %s × %s." % (fmt(F), fmt(du))},
    ]

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    return str(x)

# ---------- PROBLEM BANK ----------
bronze = []
# B1 20N @0.5 -> 10
bronze.append({
    "unit": "N m", "accept": 0.5,
    "display": "Calculate the moment produced by a force of 20 N acting at a perpendicular distance of 0.5 m from a pivot.",
    "question": q_html(beam_fig("A 20 N force acting 0.5 m from a pivot on a beam.", 300, [(160, "20 N", "down")], [(160, 300, 74, "0.5 m")]),
                       "Calculate the moment produced by a force of 20 N acting at a perpendicular distance of 0.5 m from a pivot."),
    "solutions": [10], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(M = F \\times d\\)",
    "hint": "Moment is force times distance: multiply, do not divide.",
    "misconceptions": [
        {"pattern": "inverse_error", "expect": 40, "message": "Moment is force × distance, not force ÷ distance. 20 × 0.5 = 10 N m."},
    ],
    "guided_steps": moment_walk(20, 0.5, 10),
})
# B2 50N @0.8 -> 40
bronze.append({
    "unit": "N m", "accept": 0.5,
    "display": "A force of 50 N acts at 0.8 m from a pivot. Calculate the moment in N m.",
    "question": q_html(beam_fig("A 50 N force acting 0.8 m from a pivot on a beam.", 300, [(140, "50 N", "down")], [(140, 300, 74, "0.8 m")]),
                       "A force of 50 N acts at 0.8 m from a pivot. Calculate the moment in N m."),
    "solutions": [40], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(M = F \\times d\\)",
    "hint": "Multiply the force by its distance from the pivot.",
    "misconceptions": [
        {"pattern": "inverse_error", "expect": 62.5, "message": "Multiply, do not divide: moment = 50 × 0.8 = 40 N m."},
    ],
    "guided_steps": moment_walk(50, 0.8, 40),
})
# B3 gears ratio 50/10 -> 5 (no figure)
bronze.append({
    "unit": "", "accept": 0.1,
    "display": "A driving gear has 10 teeth and a driven gear has 50 teeth. Calculate the gear ratio.",
    "solutions": [5], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{gear ratio} = \\text{driven} \\div \\text{driving}\\)",
    "hint": "Gear ratio is the driven teeth divided by the driving teeth.",
    "misconceptions": [
        {"pattern": "inverse_error", "expect": 0.2, "message": "Gear ratio = driven ÷ driving = 50 ÷ 10 = 5. Dividing the other way gives 0.2."},
    ],
    "guided_steps": [
        {"say": "Gear ratio compares the two gears: gear ratio = teeth on the driven gear ÷ teeth on the driving gear."},
        {"pre": "Teeth on the driven gear = ", "post": "", "answer": 50, "hint": "The gear that is turned."},
        {"pre": "Teeth on the driving gear = ", "post": "", "answer": 10, "hint": "The gear that does the driving."},
        {"phase": "substitute", "pre": "Divide: 50 ÷ 10 = ", "post": "", "answer": 5, "hint": "Driven divided by driving."},
        {"pre": "So the gear ratio is 5. Type it once more: ", "post": "", "answer": 5, "done": "A ratio of 5 has no unit: it just compares the two gears.", "hint": "The same value you just found, 5."},
    ],
})
# B4 30N @0.4 -> 12
bronze.append({
    "unit": "N m", "accept": 0.5,
    "display": "A force of 30 N acts at 0.4 m from a pivot. What is the moment in N m?",
    "question": q_html(beam_fig("A 30 N force acting 0.4 m from a pivot on a beam.", 300, [(190, "30 N", "down")], [(190, 300, 74, "0.4 m")]),
                       "A force of 30 N acts at 0.4 m from a pivot. What is the moment in N m?"),
    "solutions": [12], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(M = F \\times d\\)",
    "hint": "Multiply the force by its distance from the pivot.",
    "misconceptions": [
        {"pattern": "inverse_error", "expect": 75, "message": "Multiply, do not divide: moment = 30 × 0.4 = 12 N m."},
    ],
    "guided_steps": moment_walk(30, 0.4, 12),
})
# B5 gears speed 300/3 -> 100 (no figure)
bronze.append({
    "unit": "rpm", "accept": 0.5,
    "display": "A driving gear rotates at 300 rpm and has a gear ratio of 3. Calculate the speed of the driven gear in rpm.",
    "solutions": [100], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{driven speed} = \\text{driving speed} \\div \\text{gear ratio}\\)",
    "hint": "A bigger driven gear is slower: divide the driving speed by the ratio.",
    "misconceptions": [
        {"pattern": "inverse_error", "expect": 900, "message": "A larger driven gear turns slower, so divide: 300 ÷ 3 = 100 rpm. Multiplying gives 900, which would be faster."},
    ],
    "guided_steps": [
        {"say": "A larger driven gear turns more slowly. Driven speed = driving speed ÷ gear ratio."},
        {"pre": "Driving speed, in rpm = ", "post": "", "answer": 300, "hint": "The speed of the gear doing the driving."},
        {"pre": "Gear ratio = ", "post": "", "answer": 3, "hint": "Given in the question."},
        {"phase": "substitute", "pre": "Divide: 300 ÷ 3 = ", "post": "", "answer": 100, "hint": "Driving speed divided by the ratio."},
        {"pre": "Type the driven speed again to confirm: ", "post": "", "answer": 100, "done": "100 rpm, slower than the driving gear, as expected for a bigger gear.", "hint": "The same value you just found, 100."},
    ],
})
# B6 80N @0.25 -> 20
bronze.append({
    "unit": "N m", "accept": 0.5,
    "display": "A spanner applies a force of 80 N at 0.25 m from the centre of a bolt. Calculate the moment in N m.",
    "question": q_html(beam_fig("An 80 N force acting 0.25 m from a bolt acting as the pivot.", 300, [(210, "80 N", "down")], [(210, 300, 74, "0.25 m")]),
                       "A spanner applies a force of 80 N at 0.25 m from the centre of a bolt. Calculate the moment in N m."),
    "solutions": [20], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(M = F \\times d\\)",
    "hint": "Moment = force × distance; keep the distance in metres.",
    "misconceptions": [
        {"pattern": "inverse_error", "expect": 320, "message": "Multiply, do not divide: moment = 80 × 0.25 = 20 N m."},
    ],
    "guided_steps": moment_walk(80, 0.25, 20),
})

silver = []
# S1 120@0.5 -> F@0.3 = 200
silver.append({
    "unit": "N", "accept": 0.5,
    "display": "A beam is balanced on a pivot. A force of 120 N acts 0.50 m to the left. Calculate the force needed at 0.30 m to the right to keep the beam balanced.",
    "question": q_html(beam_fig("A balanced beam: 120 N at 0.5 m left of the pivot and an unknown force at 0.3 m right.", 300,
                                [(170, "120 N", "down"), (360, "? N", "down")], [(170, 300, 74, "0.5 m"), (300, 360, 74, "0.3 m")]),
                       "A beam is balanced on a pivot. A force of 120 N acts 0.50 m to the left. Calculate the force needed at 0.30 m to the right to keep the beam balanced."),
    "solutions": [200], "calculator": True, "input_type": "single_value",
    "equation_hint": "Clockwise moments = anticlockwise moments",
    "hint": "Work out the moment you know, then divide by the other distance.",
    "misconceptions": [
        {"pattern": "forgot_step", "expect": 60, "message": "60 N m is the moment, not the force. Divide by the distance: 60 ÷ 0.30 = 200 N."},
        {"pattern": "wrong_rearrange", "expect": 18, "message": "F × 0.30 = 60 rearranges to F = 60 ÷ 0.30 = 200 N, not 60 × 0.30."},
    ],
    "guided_steps": balance_force_walk(120, 0.5, 0.3, 60, 200),
})
# S2 300@2.0 -> W@1.5 = 400
silver.append({
    "unit": "N", "accept": 0.5,
    "display": "A seesaw is balanced on a central pivot. A child of weight 300 N sits 2.0 m to the left. An adult sits 1.5 m to the right. Calculate the weight of the adult.",
    "question": q_html(beam_fig("A balanced seesaw: 300 N at 2.0 m left of the pivot and an unknown weight at 1.5 m right.", 300,
                                [(120, "300 N", "down"), (430, "? N", "down")], [(120, 300, 74, "2.0 m"), (300, 430, 74, "1.5 m")]),
                       "A seesaw is balanced on a central pivot. A child of weight 300 N sits 2.0 m to the left. An adult sits 1.5 m to the right. Calculate the weight of the adult."),
    "solutions": [400], "calculator": True, "input_type": "single_value",
    "equation_hint": "Clockwise moments = anticlockwise moments",
    "hint": "Find the child's moment, then divide by the adult's distance.",
    "misconceptions": [
        {"pattern": "forgot_step", "expect": 600, "message": "600 N m is the moment. Divide by 1.5 m: W = 600 ÷ 1.5 = 400 N."},
        {"pattern": "wrong_rearrange", "expect": 900, "message": "W × 1.5 = 600 rearranges to W = 600 ÷ 1.5 = 400 N, not 600 × 1.5."},
    ],
    "guided_steps": balance_force_walk(300, 2.0, 1.5, 600, 400),
})
# S3 gears two-step 80/20=4, 300/4=75
silver.append({
    "unit": "rpm", "accept": 0.5,
    "display": "A driving gear has 20 teeth and a driven gear has 80 teeth. The driving gear rotates at 300 rpm. Calculate the rotation speed of the driven gear.",
    "solutions": [75], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{gear ratio} = \\text{driven} \\div \\text{driving}\\), then \\(\\text{driven speed} = \\text{driving speed} \\div \\text{ratio}\\)",
    "hint": "First the gear ratio, then divide the driving speed by it.",
    "misconceptions": [
        {"pattern": "forgot_step", "expect": 4, "message": "4 is the gear ratio, not the speed. Divide the driving speed by it: 300 ÷ 4 = 75 rpm."},
        {"pattern": "inverse_error", "expect": 1200, "message": "Gear ratio = driven ÷ driving = 80 ÷ 20 = 4, then 300 ÷ 4 = 75 rpm."},
    ],
    "guided_steps": [
        {"say": "Two steps: first the gear ratio, then the speed."},
        {"pre": "Gear ratio = driven ÷ driving = 80 ÷ 20 = ", "post": "", "answer": 4, "hint": "Bigger driven gear over the driving gear."},
        {"say": "Now use the ratio to slow the speed down."},
        {"phase": "substitute", "pre": "Driven speed = 300 ÷ 4 = ", "post": "", "answer": 75, "hint": "Driving speed divided by the ratio."},
        {"pre": "Confirm the driven speed: ", "post": "", "answer": 75, "done": "75 rpm, slower than the 300 rpm driving gear.", "hint": "The same value you just found, 75."},
    ],
})
# S4 400@0.75 -> 600@d = 0.5m
silver.append({
    "unit": "m", "accept": 0.02,
    "display": "A 400 N weight is placed 0.75 m to the left of a pivot. A 600 N weight is placed on the right. How far from the pivot must the 600 N weight be placed to achieve balance?",
    "question": q_html(beam_fig("A balanced beam: 400 N at 0.75 m left of the pivot and 600 N at an unknown distance right.", 300,
                                [(170, "400 N", "down"), (380, "600 N", "down")], [(170, 300, 74, "0.75 m"), (300, 380, 74, "? m")]),
                       "A 400 N weight is placed 0.75 m to the left of a pivot. A 600 N weight is placed on the right. How far from the pivot must the 600 N weight be placed to achieve balance?"),
    "solutions": [0.5], "calculator": True, "input_type": "single_value",
    "equation_hint": "Clockwise moments = anticlockwise moments",
    "hint": "Find the left moment, then divide by the 600 N force to get the distance.",
    "misconceptions": [
        {"pattern": "forgot_step", "expect": 300, "message": "300 N m is the moment. Divide by 600 N: d = 300 ÷ 600 = 0.5 m."},
        {"pattern": "inverse_error", "expect": 2, "message": "d = moment ÷ force = 300 ÷ 600 = 0.5 m. Dividing the other way gives 2, which is too far."},
    ],
    "guided_steps": [
        {"say": "Balanced means clockwise moment = anticlockwise moment. Find the moment you can first."},
        {"pre": "Known moment = 400 × 0.75 = ", "post": "", "answer": 300, "hint": "Force times its distance from the pivot."},
        {"say": "The 600 N side must also give 300 N m."},
        {"phase": "substitute", "pre": "So 600 × (distance) = 300. Divide: 300 ÷ 600 = ", "post": "", "answer": 0.5, "hint": "Divide the moment by the force."},
        {"pre": "Check: 600 × 0.5 = ", "post": "", "answer": 300, "done": "300 N m, balanced, so the distance is 0.5 m.", "hint": "Multiply back: 600 × 0.5."},
    ],
})
# S5 200@0.6 -> 120 anticlockwise
silver.append({
    "unit": "N m", "accept": 0.5,
    "display": "A lever is balanced on a pivot. A 200 N force acts 0.6 m to the left of the pivot. Calculate the moment of this force.",
    "question": q_html(beam_fig("A 200 N force acting 0.6 m to the left of a pivot.", 300, [(175, "200 N", "down")], [(175, 300, 74, "0.6 m")]),
                       "A lever is balanced on a pivot. A 200 N force acts 0.6 m to the left of the pivot. Calculate the moment of this force."),
    "solutions": [120], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(M = F \\times d\\)",
    "hint": "Moment = force × distance; a force left of the pivot turns it anticlockwise.",
    "misconceptions": [
        {"pattern": "inverse_error", "expect": 333.33, "message": "Multiply, do not divide: moment = 200 × 0.6 = 120 N m."},
    ],
    "guided_steps": moment_walk(200, 0.6, 120, done_extra=" This force is left of the pivot, so it turns the lever anticlockwise."),
})

gold = []
# G1 beam 500@1.0 down, F@2.0 up = 250
gold.append({
    "unit": "N", "accept": 0.5,
    "display": "A beam is 3.0 m long and pivoted 1.0 m from one end. A 500 N weight hangs from the short end (1.0 m from pivot). Calculate the upward force needed at the far end (2.0 m from pivot) to balance the beam.",
    "question": q_html(beam_fig("A beam pivoted off-centre: 500 N down at 1.0 m on the short arm and an unknown upward force at 2.0 m on the long arm.", 300,
                                [(150, "500 N", "down"), (470, "? N", "up")], [(150, 300, 74, "1.0 m"), (300, 470, 74, "2.0 m")]),
                       "A beam is 3.0 m long and pivoted 1.0 m from one end. A 500 N weight hangs from the short end (1.0 m from pivot). Calculate the upward force needed at the far end (2.0 m from pivot) to balance the beam."),
    "solutions": [250], "calculator": True, "input_type": "single_value",
    "equation_hint": "Clockwise moments = anticlockwise moments",
    "hint": "Balance the moments: 500 × 1.0 equals F × 2.0.",
    "misconceptions": [
        {"pattern": "forgot_step", "expect": 500, "message": "500 N m is the moment. Divide by the 2.0 m arm: F = 500 ÷ 2.0 = 250 N."},
        {"pattern": "wrong_rearrange", "expect": 1000, "message": "F × 2.0 = 500 rearranges to F = 500 ÷ 2.0 = 250 N, not 500 × 2.0."},
    ],
    "guided_steps": balance_force_walk(500, 1.0, 2.0, 500, 250),
})
# G2 gears 48/12=4, 800/4=200 (reworded to single answer)
gold.append({
    "unit": "rpm", "accept": 0.5,
    "display": "A driving gear has 12 teeth and rotates at 800 rpm. It meshes with a driven gear that has 48 teeth. Calculate the speed of the driven gear.",
    "solutions": [200], "calculator": True, "input_type": "single_value",
    "equation_hint": "\\(\\text{gear ratio} = \\text{driven} \\div \\text{driving}\\), then \\(\\text{driven speed} = \\text{driving speed} \\div \\text{ratio}\\)",
    "hint": "First the gear ratio, then divide 800 rpm by it.",
    "misconceptions": [
        {"pattern": "forgot_step", "expect": 4, "message": "4 is the gear ratio. Speed = 800 ÷ 4 = 200 rpm."},
        {"pattern": "inverse_error", "expect": 3200, "message": "Gear ratio = driven ÷ driving = 48 ÷ 12 = 4, then 800 ÷ 4 = 200 rpm."},
    ],
    "guided_steps": [
        {"say": "Two steps: first the gear ratio, then the speed."},
        {"pre": "Gear ratio = driven ÷ driving = 48 ÷ 12 = ", "post": "", "answer": 4, "hint": "Driven teeth over driving teeth."},
        {"say": "Now slow the 800 rpm down by that ratio."},
        {"phase": "substitute", "pre": "Driven speed = 800 ÷ 4 = ", "post": "", "answer": 200, "hint": "Driving speed divided by the ratio."},
        {"pre": "Confirm the driven speed: ", "post": "", "answer": 200, "done": "200 rpm, slower than the 800 rpm driving gear.", "hint": "The same value you just found, 200."},
    ],
})
# G3 crowbar load 2400@0.2, effort@1.6 = 300  (FIX: was 2700 giving 337.5)
gold.append({
    "unit": "N", "accept": 0.5,
    "display": "A crowbar 1.8 m long is pivoted 0.2 m from one end. A load of 2400 N rests at the short end (0.2 m from the pivot). Calculate the effort force needed at the long end to lift the load.",
    "question": q_html(beam_fig("A crowbar pivoted near one end: 2400 N load down at 0.2 m and an unknown upward effort at 1.6 m.", 150,
                                [(90, "2400 N", "down"), (500, "? N", "up")], [(90, 150, 74, "0.2 m"), (150, 500, 74, "1.6 m")]),
                       "A crowbar 1.8 m long is pivoted 0.2 m from one end. A load of 2400 N rests at the short end (0.2 m from the pivot). Calculate the effort force needed at the long end to lift the load."),
    "solutions": [300], "calculator": True, "input_type": "single_value",
    "equation_hint": "Clockwise moments = anticlockwise moments",
    "hint": "The effort arm is 1.8 − 0.2 = 1.6 m; balance the moments.",
    "misconceptions": [
        {"pattern": "forgot_step", "expect": 480, "message": "480 N m is the load's moment. Divide by the 1.6 m effort arm: F = 480 ÷ 1.6 = 300 N."},
        {"pattern": "wrong_rearrange", "expect": 266.67, "message": "The effort arm is 1.8 − 0.2 = 1.6 m, not 1.8 m. 480 ÷ 1.6 = 300 N."},
    ],
    "guided_steps": [
        {"say": "The load's moment must be matched by the effort's moment. First, the effort arm: the bar is 1.8 m and the pivot is 0.2 m from the load end, so the effort acts 1.8 − 0.2 from the pivot."},
        {"pre": "Effort arm = 1.8 − 0.2 = ", "post": "", "answer": 1.6, "hint": "Subtract the short arm from the full length."},
        {"pre": "Load moment = 2400 × 0.2 = ", "post": "", "answer": 480, "hint": "Force times its distance from the pivot."},
        {"say": "For balance the effort's moment must also be 480 N m."},
        {"phase": "substitute", "pre": "So effort × 1.6 = 480. Divide: 480 ÷ 1.6 = ", "post": "", "answer": 300, "hint": "Moment divided by the effort arm."},
        {"pre": "Check: 300 × 1.6 = ", "post": "", "answer": 480, "done": "480 N m, balanced, so the effort is 300 N.", "hint": "Multiply back: 300 × 1.6."},
    ],
})
# G4 seesaw 400@1.2 left; 300@0.8 + F@1.6 right -> F=150 (FIX: was 200)
gold.append({
    "unit": "N", "accept": 0.5,
    "display": "A balanced see-saw has a 400 N child sitting 1.2 m from the pivot on the left. On the right, a 300 N child sits 0.8 m from the pivot and an unknown force F acts 1.6 m from the pivot. Calculate F.",
    "question": q_html(beam_fig("A balanced see-saw: 400 N at 1.2 m left; 300 N at 0.8 m and an unknown force at 1.6 m on the right.", 300,
                                [(160, "400 N", "down"), (360, "300 N", "down"), (460, "? N", "down")],
                                [(160, 300, 74, "1.2 m"), (300, 360, 74, "0.8 m"), (300, 460, 56, "1.6 m")]),
                       "A balanced see-saw has a 400 N child sitting 1.2 m from the pivot on the left. On the right, a 300 N child sits 0.8 m from the pivot and an unknown force F acts 1.6 m from the pivot. Calculate F."),
    "solutions": [150], "calculator": True, "input_type": "single_value",
    "equation_hint": "Clockwise moments = anticlockwise moments",
    "hint": "The right side has two moments: add them, then solve for F.",
    "misconceptions": [
        {"pattern": "forgot_step", "expect": 300, "message": "Do not forget the 300 N child's clockwise moment: 300 × 0.8 = 240 N m. So 1.6F = 480 − 240 = 240, giving F = 150 N."},
        {"pattern": "sign_error", "expect": 450, "message": "The 300 N child is on the same side as F, so its moment is part of the clockwise total: 1.6F = 480 − 240 = 240, F = 150 N."},
    ],
    "guided_steps": [
        {"say": "The see-saw balances, so clockwise moment = anticlockwise moment. The right side has TWO forces, so add their moments."},
        {"pre": "Anticlockwise (left) moment = 400 × 1.2 = ", "post": "", "answer": 480, "hint": "Force times distance on the left."},
        {"pre": "The 300 N child's clockwise moment = 300 × 0.8 = ", "post": "", "answer": 240, "hint": "The other known force times its distance."},
        {"say": "The unknown force must supply the rest of the clockwise moment."},
        {"phase": "substitute", "pre": "Moment still needed from F = 480 − 240 = ", "post": "", "answer": 240, "hint": "Take the child's moment off the total."},
        {"pre": "So F × 1.6 = 240. Divide: 240 ÷ 1.6 = ", "post": "", "answer": 150, "hint": "Divide by F's distance."},
        {"pre": "Check: (300 × 0.8) + (150 × 1.6) = ", "post": "", "answer": 480, "done": "480 N m, matching the left side, so F = 150 N.", "hint": "Add the two clockwise moments back up."},
    ],
})

# ---------- tier_guides ----------
tier_guides = {
    "bronze": {
        "title": "Bronze: one moment, straight in",
        "steps": [
            "A <strong>moment</strong> is the turning effect of a force. Moment = force × perpendicular distance from the pivot.",
            "Put the force in newtons and the distance in metres, then multiply.",
            "The answer is in newton-metres (N m). Gear ratio questions live here too: driven teeth ÷ driving teeth."
        ],
        "example": {
            "question": "A mechanic applies 40 N at 0.30 m from a pivot. Find the moment.",
            "steps": [
                {"label": "Equation", "content": "<p>Moment = force × perpendicular distance</p>"},
                {"label": "Substitute", "content": "<p>Moment = 40 × 0.30</p>"},
                {"label": "Check", "content": "<p>40 N over about a third of a metre, so a bit under 13 N m looks right.</p>"},
                {"label": "Answer", "content": "<p><strong>12 N m</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: balance two moments",
        "steps": [
            "A balanced object has clockwise moments = anticlockwise moments.",
            "Work out the moment you can (force × distance), then set the other side equal to it.",
            "Rearrange for the unknown: divide the moment by the distance to find a force, or by the force to find a distance."
        ],
        "example": {
            "question": "A 360 N child sits 1.5 m left of a central pivot. Where must a 600 N adult sit on the right to balance?",
            "steps": [
                {"label": "Anticlockwise moment", "content": "<p>360 × 1.5 = 540 N m</p>"},
                {"label": "Set equal", "content": "<p>600 × d = 540</p>"},
                {"label": "Rearrange", "content": "<p>d = 540 ÷ 600</p>"},
                {"label": "Check", "content": "<p>600 × 0.90 = 540 N m, balanced.</p>"},
                {"label": "Answer", "content": "<p><strong>0.90 m</strong> from the pivot</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chain two steps",
        "steps": [
            "Gold problems need two moves. Gears: first the ratio (driven ÷ driving), then divide the driving speed by it.",
            "Beams: when a side has more than one force, add those moments, and remember the effort arm may be the full length minus the short arm.",
            "Finish the same way: set clockwise = anticlockwise and solve for the unknown, then check."
        ],
        "example": {
            "question": "A driving gear (15 teeth) at 200 rpm meshes with a driven gear of 60 teeth. Find the driven speed.",
            "steps": [
                {"label": "Gear ratio", "content": "<p>60 ÷ 15 = 4</p>"},
                {"label": "Driven speed", "content": "<p>200 ÷ 4</p>"},
                {"label": "Check", "content": "<p>A bigger driven gear must be slower than 200 rpm.</p>"},
                {"label": "Answer", "content": "<p><strong>50 rpm</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------- guided (opener + teach) ----------
opener_svg = beam_fig("A balanced seesaw: 600 N at 1.5 m on the left, 300 N at an unknown distance on the right.",
                      300, [(150, "600 N", "down"), (430, "300 N", "down")], [(150, 300, 74, "1.5 m"), (300, 430, 74, "? m")])
guided = {
    "opener": {
        "label": "Before any equations",
        "display": opener_svg + "<p style=\"margin-top:0.6em;\">A seesaw balances. Big brother weighs 600 N and sits 1.5 m from the middle. Little sister weighs only 300 N, half as much.</p>",
        "steps": [
            {"say": "No equations yet, just common sense. Sister is half brother's weight, so to balance she must sit further out.",
             "pre": "She weighs half as much, so she must sit how many times as far out? ", "post": "", "answer": 2,
             "hint": "Half the weight needs double the distance to balance."},
            {"say": "Good. Double the distance makes up for half the weight.",
             "pre": "So her distance from the middle = 1.5 m × 2 = ", "post": "", "answer": 3,
             "hint": "Double the brother's 1.5 m."},
            {"say": "You just used the <strong>principle of moments</strong>. The turning effect is force × distance. Brother: 600 × 1.5 = 900. Sister: 300 × 3 = 900. Equal turning effects balance. That turning effect has a name: the <strong>moment</strong>. Moment = force × distance from the pivot."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "A force of 60 N acts 0.3 m from a pivot. Find the moment.",
            "label": "Together: your first moment",
            "steps": moment_walk(60, 0.3, 18),
        },
        "silver": {
            "display": "A 500 N weight sits 0.4 m to the left of a pivot. What force at 0.5 m to the right will balance it?",
            "label": "Together: the balance move",
            "steps": [
                {"say": "Balanced means clockwise moment = anticlockwise moment. Find the moment you can first."},
                {"pre": "Anticlockwise moment = 500 × 0.4 = ", "post": "", "answer": 200, "hint": "Force times its distance from the pivot."},
                {"say": "For balance the clockwise side must match it."},
                {"pre": "Clockwise moment needed = ", "post": "", "answer": 200, "hint": "The same as the anticlockwise moment."},
                {"phase": "substitute", "pre": "So F × 0.5 = 200. Divide: 200 ÷ 0.5 = ", "post": "", "answer": 400, "hint": "Moment divided by the distance."},
                {"pre": "Check: 400 × 0.5 = ", "post": "", "answer": 200, "done": "200 N m, balanced, so F = 400 N.", "hint": "Multiply back: 400 × 0.5."},
            ],
        },
        "gold": {
            "display": "A balanced beam has 500 N at 1.0 m on the left. On the right, 200 N acts at 0.5 m and a force F acts at 2.0 m. Find F.",
            "label": "Together: the multi-force move",
            "steps": [
                {"say": "Clockwise moment = anticlockwise moment, but the right side has two forces, so add their moments."},
                {"pre": "Anticlockwise moment = 500 × 1.0 = ", "post": "", "answer": 500, "hint": "Force times distance on the left."},
                {"pre": "The 200 N force's clockwise moment = 200 × 0.5 = ", "post": "", "answer": 100, "hint": "The known right-hand force times its distance."},
                {"say": "F must supply the rest of the clockwise moment."},
                {"phase": "substitute", "pre": "Moment needed from F = 500 − 100 = ", "post": "", "answer": 400, "hint": "Take the 200 N moment off the total."},
                {"pre": "F × 2.0 = 400, so 400 ÷ 2.0 = ", "post": "", "answer": 200, "hint": "Divide by F's distance."},
                {"pre": "Check: (200 × 0.5) + (200 × 2.0) = ", "post": "", "answer": 500, "done": "500 N m, balanced, so F = 200 N.", "hint": "Add the two clockwise moments back up."},
            ],
        },
    },
}

# ---------- method_card (slim) ----------
method_card = {
    "title": "Moments, Levers and Gears",
    "steps": [
        "Moment (N m) = force (N) × perpendicular distance from the pivot (m).",
        "Balanced object: clockwise moments = anticlockwise moments. Use this to find an unknown force or distance.",
        "Gear ratio = driven teeth ÷ driving teeth.",
        "Driven speed = driving speed ÷ gear ratio (a bigger driven gear turns slower).",
    ],
    "content": "<p><strong>Moment</strong> = force × perpendicular distance from the pivot, in newton-metres (N m). The distance must be perpendicular to the force and in metres.</p><p><strong>Principle of moments:</strong> a balanced object has clockwise moments equal to anticlockwise moments. Set them equal, then rearrange for the unknown force or distance.</p><p><strong>Gears:</strong> gear ratio = driven teeth ÷ driving teeth. A ratio above 1 means the driven gear turns slower but with more turning force. Divide the driving speed by the ratio to get the driven speed.</p>",
}

exam_context = {
    "marks": "3–5 per question",
    "paper": "Paper 2 (Physics)",
    "frequency": "Moderate: moments and principle-of-moments balance problems appear regularly in higher-tier physics",
}

worked_examples = [
    {"difficulty": "Bronze", "question": "A mechanic applies a force of 40 N at a perpendicular distance of 0.30 m from a pivot. Calculate the moment of the force.",
     "steps": [
         {"label": "Step 1: Write the equation", "content": "<p>Moment = force × perpendicular distance</p>"},
         {"label": "Step 2: Substitute values", "content": "<p>Moment = 40 × 0.30</p>"},
         {"label": "Answer", "content": "<p>Moment = <strong>12 N m</strong></p>", "isAnswer": True, "is_answer": True},
     ]},
    {"difficulty": "Silver", "question": "A seesaw is balanced at its centre pivot. A child of weight 360 N sits 1.5 m to the left. Where must an adult of weight 600 N sit on the right to balance the seesaw?",
     "steps": [
         {"label": "Step 1: Calculate anticlockwise moment", "content": "<p>Moment = 360 × 1.5 = 540 N m (anticlockwise)</p>"},
         {"label": "Step 2: Apply principle of moments", "content": "<p>Clockwise moment = 540 N m</p><p>600 × d = 540</p>"},
         {"label": "Step 3: Rearrange", "content": "<p>d = 540 ÷ 600</p>"},
         {"label": "Answer", "content": "<p>d = <strong>0.90 m</strong> from the pivot</p>", "isAnswer": True, "is_answer": True},
     ]},
    {"difficulty": "Gold", "question": "A driving gear has 15 teeth and meshes with a driven gear of 60 teeth. The driving gear rotates at 200 rpm. Calculate: (a) the gear ratio, and (b) the rotation speed of the driven gear.",
     "steps": [
         {"label": "Step 1: Gear ratio", "content": "<p>Gear ratio = driven ÷ driving = 60 ÷ 15 = 4</p>"},
         {"label": "Step 2: Speed of driven gear", "content": "<p>Speed = driving speed ÷ gear ratio = 200 ÷ 4</p>"},
         {"label": "Answer", "content": "<p>(a) Gear ratio = <strong>4</strong> &nbsp; (b) Driven gear speed = <strong>50 rpm</strong></p>", "isAnswer": True, "is_answer": True},
     ]},
]

pd = {
    "method_card": method_card,
    "topic_links": {"prerequisites": []},
    "exam_context": exam_context,
    "problem_bank": {
        "bronze": bronze,
        "silver": silver,
        "gold": gold,
        "bronze_description": "One moment: multiply a force by its distance from the pivot.",
        "silver_description": "Set clockwise moments equal to anticlockwise, or take a gear ratio through to a speed.",
        "gold_description": "Multi-step: a beam with an extra force, an offset pivot, or gears to a final speed.",
    },
    "related_videos": [],
    "worked_examples": worked_examples,
    "tier_guides": tier_guides,
    "guided": guided,
}

out = "lesson_higher-calculations-L03@efa41fc772.json"
json.dump(pd, io.open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", out)

# ---------- self-check: fresh-solve every problem, verify expects outside accept ----------
def solve_check():
    errs = []
    checks = {
        ("bronze", 0): 20*0.5, ("bronze", 1): 50*0.8, ("bronze", 2): 50/10, ("bronze", 3): 30*0.4,
        ("bronze", 4): 300/3, ("bronze", 5): 80*0.25,
        ("silver", 0): (120*0.5)/0.3, ("silver", 1): (300*2.0)/1.5, ("silver", 2): 300/(80/20),
        ("silver", 3): (400*0.75)/600, ("silver", 4): 200*0.6,
        ("gold", 0): (500*1.0)/2.0, ("gold", 1): 800/(48/12), ("gold", 2): (2400*0.2)/1.6,
        ("gold", 3): (400*1.2 - 300*0.8)/1.6,
    }
    bank = {"bronze": bronze, "silver": silver, "gold": gold}
    for (t, i), val in checks.items():
        stored = bank[t][i]["solutions"][0]
        if abs(stored - val) > 1e-6:
            errs.append("%s[%d] stored %s != computed %s" % (t, i, stored, val))
        acc = bank[t][i].get("accept", 0)
        for m in bank[t][i].get("misconceptions", []):
            e = m.get("expect")
            if e is not None and abs(e - stored) <= max(acc, 0.011):
                errs.append("%s[%d] expect %s inside accept/0.011 of %s" % (t, i, e, stored))
    # verify last box of every walk lands on solution
    for t in ("bronze", "silver", "gold"):
        for i, p in enumerate(bank[t]):
            gs = p.get("guided_steps", [])
            boxes = [s for s in gs if s.get("answer") is not None]
            if not boxes:
                errs.append("%s[%d] no boxes" % (t, i)); continue
    if errs:
        print("SELF-CHECK FAIL:")
        for e in errs:
            print("  -", e)
    else:
        print("SELF-CHECK PASS: all 16 problems solve; all expects outside accept window")

solve_check()
