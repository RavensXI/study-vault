# -*- coding: utf-8 -*-
import json, copy

pd = json.load(open("_mine_L03.json", encoding="utf-8"))

# ---------- 1. Fix em dashes in preserved fields ----------
pd["exam_context"]["frequency"] = pd["exam_context"]["frequency"].replace(" — ", ": ").replace("—", ":")
for we in pd["worked_examples"]:
    for st in we["steps"]:
        if "label" in st:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---------- 2. Slim method_card ----------
pd["method_card"]["content"] = (
    "<p>A <strong>moment</strong> is the turning effect of a force: "
    "<strong>M = F × d</strong>, where d is the perpendicular distance from the pivot, in metres.</p>"
    "<ul>"
    "<li>Rearrange for a missing value: F = M ÷ d, or d = M ÷ F.</li>"
    "<li>Given a mass? Find its weight first: W = m × g (g = 9.8 N/kg).</li>"
    "<li>Balanced beam or lever: clockwise moment = anticlockwise moment, so F₁d₁ = F₂d₂.</li>"
    "<li>Several forces on one side: add their moments before balancing.</li>"
    "<li>A uniform beam's weight acts at its centre.</li>"
    "<li>Gears: ratio = driven teeth ÷ driver teeth; speed ÷ ratio, force × ratio.</li>"
    "</ul>"
)
pd["method_card"]["steps"] = [
    "Spot the pivot and which distance is perpendicular to the force",
    "If given a mass, find its weight with W = mg first",
    "Balanced beam or lever: set clockwise moment = anticlockwise moment",
    "Gears: ratio = driven teeth ÷ driver teeth (speed divides, force multiplies)",
]

# ---------- helpers ----------
def box(pre, ans, hint, post="", phase=None, say=None, done=None):
    b = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if phase: b["phase"] = phase
    if say: b["say"] = say
    if done: b["done"] = done
    return b

def say(s):
    return {"say": s}

# ---------- SVG beam figure builder ----------
def beam_svg(aria, forces, pivot_x):
    # forces: list of dict {x,label,dist}
    by = 50
    p = ['<svg viewBox="0 0 260 118" role="img" aria-label="%s">' % aria]
    p.append('<rect x="20" y="%d" width="220" height="6" rx="2" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>' % (by - 3))
    p.append('<polygon points="%d,%d %d,%d %d,%d" fill="#f59e0b" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>' % (pivot_x, by + 3, pivot_x - 9, by + 24, pivot_x + 9, by + 24))
    for f in forces:
        x = f["x"]
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1.5"/>' % (x, by + 3, x, by + 28))
        p.append('<polygon points="%d,%d %d,%d %d,%d" fill="currentColor"/>' % (x, by + 33, x - 4, by + 26, x + 4, by + 26))
        p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % (x, by + 46, f["label"]))
        midx = (x + pivot_x) // 2
        p.append('<text x="%d" y="%d" font-family="Inter,sans-serif" font-size="10" fill="currentColor" text-anchor="middle">%s</text>' % (midx, by - 7, f["dist"]))
    p.append('</svg>')
    return "".join(p)

CAP = '<span class="figure-caption">Diagram not drawn accurately</span>'

# ---------- 3. Bank: descriptions ----------
pb = pd["problem_bank"]
pb["bronze_description"] = "One moment equation with values already in newtons and metres: substitute straight in, or rearrange once."
pb["silver_description"] = "Turn a mass into a weight (W = mg) first, or balance two moments before solving for the unknown."
pb["gold_description"] = "Chain two steps: add several moments, run a gear ratio, or include a uniform beam's own weight."

# ---------- 4. Per-problem guided_steps, hints, expects, figures ----------
# BRONZE
bronze_gs = [
 # B0 F50 d0.3 -> M15
 [say("Moments use one equation: M = F × d, the force times the perpendicular distance from the pivot."),
  box("Which distance? Always the perpendicular distance from the pivot, in metres. d = ", 0.3, "It is given as the perpendicular distance in the question."),
  box("Substitute and multiply: M = 50 × 0.3 = ", 15, "Multiply the force by the distance.", phase="substitute", say="So M = 15 Nm."),
  box("Check by dividing back: 15 ÷ 50 = ", 0.3, "Divide the moment by the force.", done="It returns 0.3 m, the distance, so 15 Nm is right.")],
 # B1 M20 d0.4 -> F50
 [say("M = F × d. You know the moment and distance and want the force, so rearrange: F = M ÷ d."),
  box("Which number is the moment, on top? M = ", 20, "In F = M ÷ d the moment is divided by the distance."),
  box("Divide: 20 ÷ 0.4 = ", 50, "Divide the moment by the distance.", phase="substitute", say="So F = 50 N."),
  box("Check by multiplying back: 50 × 0.4 = ", 20, "Force times distance.", done="It returns the 20 Nm moment, so 50 N is right.")],
 # B2 F30 M12 -> d0.4
 [say("M = F × d. You want the distance, so rearrange: d = M ÷ F."),
  box("The moment goes on top. M = ", 12, "In d = M ÷ F the moment is divided by the force."),
  box("Divide: 12 ÷ 30 = ", 0.4, "Divide the moment by the force.", phase="substitute", say="So d = 0.4 m."),
  box("Check: 30 × 0.4 = ", 12, "Force times distance.", done="It returns the 12 Nm moment, so 0.4 m is right.")],
 # B3 F200 d1.5 -> M300
 [say("Moments use one equation: M = F × d."),
  box("The perpendicular distance from the bolt, in metres. d = ", 1.5, "Read it from the question."),
  box("Multiply: M = 200 × 1.5 = ", 300, "Force times distance.", phase="substitute", say="So M = 300 Nm."),
  box("Check: 300 ÷ 200 = ", 1.5, "Divide the moment by the force.", done="It returns 1.5 m, so 300 Nm is right.")],
 # B4 M36 d0.6 -> F60
 [say("M = F × d. The moment is known and you want the force, so rearrange: F = M ÷ d."),
  box("The moment goes on top. M = ", 36, "In F = M ÷ d the moment is divided by the distance."),
  box("Divide: 36 ÷ 0.6 = ", 60, "Divide the moment by the distance.", phase="substitute", say="So F = 60 N."),
  box("Check: 60 × 0.6 = ", 36, "Force times distance.", done="It returns 36 Nm, so 60 N is right.")],
 # B5 F80 d0.25 -> M20
 [say("Moments use one equation: M = F × d."),
  box("The perpendicular distance from the pivot, in metres. d = ", 0.25, "Read it from the question."),
  box("Multiply: M = 80 × 0.25 = ", 20, "Force times distance.", phase="substitute", say="So M = 20 Nm."),
  box("Check: 20 ÷ 80 = ", 0.25, "Divide the moment by the force.", done="It returns 0.25 m, so 20 Nm is right.")],
 # B6 F15 M45 -> d3
 [say("M = F × d. You want the distance, so rearrange: d = M ÷ F."),
  box("The moment goes on top. M = ", 45, "In d = M ÷ F the moment is divided by the force."),
  box("Divide: 45 ÷ 15 = ", 3, "Divide the moment by the force.", phase="substitute", say="So d = 3 m."),
  box("Check: 15 × 3 = ", 45, "Force times distance.", done="It returns the 45 Nm moment, so 3 m is right.")],
 # B7 seesaw 400@2.0 = F@1.6 -> 500
 [say("A balanced seesaw: clockwise moment = anticlockwise moment, so F₁d₁ = F₂d₂."),
  box("Work out the known moment first: 400 × 2.0 = ", 800, "Force times distance on the left."),
  box("This equals F × 1.6. Divide to find F: 800 ÷ 1.6 = ", 500, "Divide the moment by the right-hand distance.", phase="substitute", say="So F = 500 N."),
  box("Check: 500 × 1.6 = ", 800, "Force times distance on the right.", done="It matches the left moment of 800 Nm, so 500 N balances.")],
]
bronze_hint = [
 "Multiply the force by the perpendicular distance.",
 "Rearrange to F = M ÷ d, then divide.",
 "Rearrange to d = M ÷ F, then divide.",
 "Multiply the force by the distance.",
 "Rearrange to F = M ÷ d, then divide.",
 "Multiply the force by the distance.",
 "Rearrange to d = M ÷ F, then divide.",
 "Balance the moments: F₁d₁ = F₂d₂, then rearrange for the unknown force.",
]
bronze_expect = [None, 8, 360, None, 21.6, 320, 675, 320]

# SILVER
silver_gs = [
 # S0 child 30@2.0, adult 60@d -> 1
 [say("First turn the masses into weights with W = mg (g = 9.8), then balance: W₁d₁ = W₂d₂."),
  box("Child's weight: W = 30 × 9.8 = ", 294, "Mass times 9.8."),
  box("Adult's weight: W = 60 × 9.8 = ", 588, "Mass times 9.8."),
  box("Child's moment: 294 × 2.0 = ", 588, "Weight times distance."),
  box("Balance: this equals 588 × d. Divide: 588 ÷ 588 = ", 1, "Divide the child's moment by the adult's weight.", phase="substitute", say="So d = 1.0 m."),
  box("Check: 588 × 1.0 = ", 588, "Adult's weight times distance.", done="It equals the child's 588 Nm moment, so 1.0 m balances.")],
 # S1 600@0.8 cw vs F@1.2 acw -> 400
 [say("Balance: clockwise moment = anticlockwise moment."),
  box("Clockwise moment: 600 × 0.8 = ", 480, "Force times distance."),
  box("This equals F × 1.2. Divide: 480 ÷ 1.2 = ", 400, "Divide the moment by 1.2.", phase="substitute", say="So F = 400 N."),
  box("Check: 400 × 1.2 = ", 480, "Force times distance.", done="It matches the 480 Nm clockwise moment, so 400 N balances.")],
 # S2 nutcracker 5kg, nut0.08 handle0.4 -> 9.8
 [say("First turn the mass into a weight (W = mg), then balance the load and effort moments."),
  box("Weight on the nut: W = 5 × 9.8 = ", 49, "Mass times 9.8."),
  box("Load moment: 49 × 0.08 = ", 3.92, "Weight times the nut's distance from the pivot."),
  box("This equals F × 0.4. Divide: 3.92 ÷ 0.4 = ", 9.8, "Divide by the handle distance.", phase="substitute", say="So you apply 9.8 N at the handle."),
  box("Check: 9.8 × 0.4 = ", 3.92, "Force times distance.", done="It equals the 3.92 Nm load moment, so 9.8 N is right.")],
 # S3 200@1.0 acw, 150@2.0 cw -> resultant 100
 [say("Work out each moment, then subtract, because the two forces turn opposite ways."),
  box("Anticlockwise moment: 200 × 1.0 = ", 200, "Force times distance."),
  box("Clockwise moment: 150 × 2.0 = ", 300, "Force times distance."),
  box("They oppose, so subtract the smaller from the larger: 300 − 200 = ", 100, "Subtract the anticlockwise moment from the clockwise one.", phase="substitute", say="So the resultant is 100 Nm, clockwise."),
  box("Check: 200 + 100 = ", 300, "Add the resultant back to the anticlockwise moment.", done="It equals the 300 Nm clockwise moment, so 100 Nm is right.")],
 # S4 8kg @0.25 -> 19.6
 [say("Turn the mass into a weight (W = mg), then take the moment."),
  box("Weight: W = 8 × 9.8 = ", 78.4, "Mass times 9.8."),
  box("Moment = weight × distance = 78.4 × 0.25 = ", 19.6, "Multiply the weight by 0.25.", phase="substitute", say="So the moment is 19.6 Nm."),
  box("Check: 19.6 ÷ 0.25 = ", 78.4, "Divide the moment by the distance.", done="It returns the 78.4 N weight, so 19.6 Nm is right.")],
 # S5 wheelbarrow load150@0.4 handle1.2 -> 50
 [say("A wheelbarrow is a lever: load × load distance = effort × effort distance."),
  box("Load moment: 150 × 0.4 = ", 60, "Load times its distance from the wheel."),
  box("This equals effort × 1.2. Divide: 60 ÷ 1.2 = ", 50, "Divide by the handle distance.", phase="substitute", say="So the effort needed is 50 N."),
  box("Check: 50 × 1.2 = ", 60, "Force times distance.", done="It equals the 60 Nm load moment, so 50 N lifts it.")],
]
silver_hint = [
 "Turn both masses into weights with W = mg, then balance the moments.",
 "Set the clockwise moment equal to the anticlockwise one, then divide.",
 "Turn the mass into a weight first, then balance the load and effort moments.",
 "Find each moment, then subtract because they turn opposite ways.",
 "Turn the mass into a weight with W = mg, then multiply by the distance.",
 "Balance the load moment against the effort moment, then divide.",
]
silver_expect = [None, 480, 1.0, 500, 2.0, 60]

# GOLD
gold_gs = [
 # G0 left 100@0.5 +200@1.5, right F@0.7 -> 500
 [say("Multiple forces on the left: work out each moment, add them, then balance against the right."),
  box("First moment: 100 × 0.5 = ", 50, "Force times distance."),
  box("Second moment: 200 × 1.5 = ", 300, "Force times distance."),
  box("Total anticlockwise moment: 50 + 300 = ", 350, "Add the two moments."),
  box("Balance: F × 0.7 = 350. Divide: 350 ÷ 0.7 = ", 500, "Divide the total moment by 0.7.", phase="substitute", say="So F = 500 N."),
  box("Check: 500 × 0.7 = ", 350, "Force times distance.", done="It equals the 350 Nm total, so 500 N balances the beam.")],
 # G1 gears 20/60, 120 rpm -> 40
 [say("Gears: work out the gear ratio = driven teeth ÷ driver teeth. A bigger driven gear turns slower."),
  box("Gear ratio = 60 ÷ 20 = ", 3, "Divide driven teeth by driver teeth."),
  box("The driven gear turns 3 times slower, so divide the speed: 120 ÷ 3 = ", 40, "Divide the input speed by the gear ratio.", phase="substitute", say="So the driven gear turns at 40 rpm."),
  box("Check: 40 × 3 = ", 120, "Multiply back by the ratio.", done="It returns the driver's 120 rpm, so 40 rpm is right.")],
 # G2 gears 20/60, force 15 -> 45
 [say("Same gear ratio, but force behaves the opposite way to speed: a bigger driven gear gives MORE force."),
  box("Gear ratio = 60 ÷ 20 = ", 3, "Divide driven teeth by driver teeth."),
  box("More force by the ratio: 15 × 3 = ", 45, "Multiply the input force by the gear ratio.", phase="substitute", say="So the output force is 45 N."),
  box("Check: 45 ÷ 3 = ", 15, "Divide back by the ratio.", done="It returns the 15 N input, so 45 N is right.")],
 # G3 uniform beam 2.0m 10kg, pivot0.8, load50 at left end -> 17
 [say("A uniform beam's own weight acts at its centre. Find that weight and where it acts, then balance."),
  box("Beam weight: W = 10 × 9.8 = ", 98, "Mass times 9.8."),
  box("The centre is 1.0 m from the left; the pivot is at 0.8 m, so the weight acts 1.0 − 0.8 = ", 0.2, "Centre distance minus pivot distance."),
  box("Anticlockwise moment from the 50 N load, 0.8 m left of the pivot: 50 × 0.8 = ", 40, "Load times its distance from the pivot."),
  box("Clockwise moment from the beam weight: 98 × 0.2 = ", 19.6, "Weight times its distance right of the pivot."),
  box("The right force acts 2.0 − 0.8 = 1.2 m from the pivot. Balance gives 40 = 19.6 + F × 1.2. First, 40 − 19.6 = ", 20.4, "Subtract the beam's moment from the load's moment.", phase="substitute"),
  box("Now divide: 20.4 ÷ 1.2 = ", 17, "Divide by the right-hand distance.", say="So F = 17 N."),
  box("Check the clockwise side: 19.6 + 17 × 1.2 = ", 40, "Add the two clockwise moments.", done="It equals the 40 Nm anticlockwise moment, so 17 N balances.")],
 # G4 lever 12@0.3 + gear 15/45 -> 10.8
 [say("Two steps: first the lever's moment (torque), then multiply by the gear ratio."),
  box("Lever torque: M = 12 × 0.3 = ", 3.6, "Force times distance."),
  box("Gear ratio = 45 ÷ 15 = ", 3, "Driven teeth ÷ driver teeth."),
  box("Output torque = input torque × ratio = 3.6 × 3 = ", 10.8, "Multiply the lever torque by the gear ratio.", phase="substitute", say="So the output torque is 10.8 Nm."),
  box("Check: 10.8 ÷ 3 = ", 3.6, "Divide back by the ratio.", done="It returns the 3.6 Nm lever torque, so 10.8 Nm is right.")],
 # G5 crowbar effort80@0.75, load@0.05 -> 1200
 [say("A lever multiplies force: effort × effort distance = load × load distance."),
  box("Effort moment: 80 × 0.75 = ", 60, "Effort force times its distance from the pivot."),
  box("This equals load × 0.05. Divide: 60 ÷ 0.05 = ", 1200, "Divide by the load's distance from the pivot.", phase="substitute", say="So the force on the stone is 1200 N."),
  box("Check: 1200 × 0.05 = ", 60, "Force times distance.", done="It equals the 60 Nm effort moment, so 1200 N is right.")],
]
gold_hint = [
 "Add both left moments, then divide the total by the right-hand distance.",
 "Gear ratio = driven ÷ driver; a bigger driven gear turns slower, so divide the speed.",
 "Gear ratio = driven ÷ driver; a bigger driven gear gives more force, so multiply.",
 "Find the beam's weight and where its centre acts, then balance the moments about the pivot.",
 "Work out the lever's torque first, then multiply by the gear ratio.",
 "Effort × effort distance = load × load distance; rearrange for the load force.",
]
gold_eqhint = [
 "\\(F_1 d_1 = F_2 d_2\\)",
 "\\(\\text{ratio} = \\frac{\\text{driven teeth}}{\\text{driver teeth}}\\)",
 "\\(\\text{ratio} = \\frac{\\text{driven teeth}}{\\text{driver teeth}}\\)",
 "\\(F_1 d_1 = F_2 d_2\\), \\(W = mg\\)",
 "\\(M = F \\times d\\), then \\(\\times\\) gear ratio",
 "\\(F_1 d_1 = F_2 d_2\\)",
]
gold_expect = [350, 360, 5, 33.33, 3.6, 60]

# figures: bronze[7]=B7, silver[1]=S1, silver[3]=S3, gold[0]=G0, gold[3]=G3
fig_b7 = beam_svg("Seesaw balanced on a central pivot: a 400 N force acts 2.0 m to the left and an unknown force acts 1.6 m to the right.",
                  [{"x":55,"label":"400 N","dist":"2.0 m"},{"x":205,"label":"F = ?","dist":"1.6 m"}], 130)
fig_s1 = beam_svg("Beam on a central pivot: an unknown force acts 1.2 m to the left (anticlockwise) and a 600 N force acts 0.8 m to the right (clockwise).",
                  [{"x":60,"label":"F = ?","dist":"1.2 m"},{"x":190,"label":"600 N","dist":"0.8 m"}], 130)
fig_s3 = beam_svg("Beam on a central pivot: a 200 N force acts 1.0 m to the left (anticlockwise) and a 150 N force acts 2.0 m to the right (clockwise).",
                  [{"x":60,"label":"200 N","dist":"1.0 m"},{"x":205,"label":"150 N","dist":"2.0 m"}], 130)
fig_g0 = beam_svg("Beam on a central pivot: a 200 N force 1.5 m and a 100 N force 0.5 m to the left, an unknown force 0.7 m to the right.",
                  [{"x":40,"label":"200 N","dist":"1.5 m"},{"x":100,"label":"100 N","dist":"0.5 m"},{"x":200,"label":"F = ?","dist":"0.7 m"}], 130)
fig_g3 = beam_svg("Uniform beam with a pivot 0.8 m from the left end: a 50 N load at the left end, the beam's 10 kg weight at the centre, an unknown force at the right end.",
                  [{"x":22,"label":"50 N","dist":"0.8 m"},{"x":130,"label":"10 kg","dist":"0.2 m"},{"x":235,"label":"F = ?","dist":"1.2 m"}], 108)

# apply
def apply(tier, gs_list, hint_list, expect_list, eqhint_list=None):
    for i, prob in enumerate(pb[tier]):
        prob["guided_steps"] = gs_list[i]
        prob["hint"] = hint_list[i]
        if eqhint_list is not None:
            prob["equation_hint"] = eqhint_list[i]
        # expects
        exp = expect_list[i]
        mcs = prob.get("misconceptions") or []
        for j, m in enumerate(mcs):
            if "expect" not in m:
                m["expect"] = exp if j == 0 else None

apply("bronze", bronze_gs, bronze_hint, bronze_expect)
apply("silver", silver_gs, silver_hint, silver_expect)
apply("gold", gold_gs, gold_hint, gold_expect, gold_eqhint)

# Special expect placement overrides (where the determinate error is in mc index 1, not 0)
def set_expect(tier, idx, mc_idx, val):
    pb[tier][idx]["misconceptions"][mc_idx]["expect"] = val
# S2 used_mass -> mc[1] gives 1.0 ; mc[0] null
set_expect("silver",2,0,None); set_expect("silver",2,1,1.0)
# G1 multiplied -> mc[1]=360 ; mc[0] null
set_expect("gold",1,0,None); set_expect("gold",1,1,360)
# G2 divided -> mc[1]=5 ; mc[0] null
set_expect("gold",2,0,None); set_expect("gold",2,1,5)
# G0 forgot_step -> mc[0]=350 ; mc[1] single_force null
set_expect("gold",0,0,350); set_expect("gold",0,1,None)
# G3 forgot_beam_weight mc[0]=33.33 ; mc[1] forgot_centre null
set_expect("gold",3,0,33.33); set_expect("gold",3,1,None)
# G4 forgot_step mc[0]=3.6 ; inverse_ratio mc[1]=1.2
set_expect("gold",4,0,3.6); set_expect("gold",4,1,1.2)
# G5 wrong_rearrange mc[0]=60 ; inverse_error mc[1] null
set_expect("gold",5,0,60); set_expect("gold",5,1,None)

# apply figures (prepend svg + caption to display)
pb["bronze"][7]["display"] = fig_b7 + CAP + pb["bronze"][7]["display"]
pb["silver"][1]["display"] = fig_s1 + CAP + pb["silver"][1]["display"]
pb["silver"][3]["display"] = fig_s3 + CAP + pb["silver"][3]["display"]
pb["gold"][0]["display"]   = fig_g0 + CAP + pb["gold"][0]["display"]
pb["gold"][3]["display"]   = fig_g3 + CAP + pb["gold"][3]["display"]

# ---------- 5. tier_guides ----------
def ex_step(label, content, ans=False):
    s = {"label": label, "content": content}
    if ans:
        s["isAnswer"] = True; s["is_answer"] = True
    return s

pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one moment, straight in",
   "steps": [
     "<strong>Moment = force × perpendicular distance</strong> from the pivot: M = F × d.",
     "Use the distance measured from the pivot, at a right angle to the force, in metres.",
     "To find a force or distance instead, rearrange: F = M ÷ d, or d = M ÷ F.",
   ],
   "example": {
     "question": "A force of 40 N acts 0.5 m from a pivot. Calculate the moment.",
     "steps": [
       ex_step("Equation", "<p>M = F × d</p>"),
       ex_step("Substitute", "<p>M = 40 × 0.5</p>"),
       ex_step("Check", "<p>40 × 0.5 = 20, and 20 ÷ 0.5 = 40 N, the original force.</p>"),
       ex_step("Answer", "<p><strong>20 Nm</strong></p>", ans=True),
     ]}},
 "silver": {
   "title": "Silver: weight first, or balance two moments",
   "steps": [
     "Given a mass? Turn it into a weight first: <strong>W = m × g</strong>, with g = 9.8 N/kg.",
     "For a balanced beam or lever, clockwise moment = anticlockwise moment: F₁d₁ = F₂d₂.",
     "Substitute the known moment, then divide to find the missing force or distance.",
   ],
   "example": {
     "question": "A 4 kg mass hangs 0.5 m from a pivot. Calculate the moment. (g = 9.8 N/kg)",
     "steps": [
       ex_step("Weight", "<p>W = 4 × 9.8 = 39.2 N</p>"),
       ex_step("Moment", "<p>M = 39.2 × 0.5</p>"),
       ex_step("Check", "<p>39.2 × 0.5 = 19.6, and 19.6 ÷ 0.5 = 39.2 N.</p>"),
       ex_step("Answer", "<p><strong>19.6 Nm</strong></p>", ans=True),
     ]}},
 "gold": {
   "title": "Gold: chain the steps",
   "steps": [
     "Several forces on one side? Work out each moment, then add them before balancing.",
     "Gears: ratio = driven teeth ÷ driver teeth. Speed divides by the ratio; force multiplies by it.",
     "A uniform beam's own weight (W = mg) acts at its centre; include it as another moment.",
   ],
   "example": {
     "question": "A 10-tooth driver gear turns a 40-tooth gear with an input force of 20 N. Find the output force.",
     "steps": [
       ex_step("Ratio", "<p>ratio = 40 ÷ 10 = 4</p>"),
       ex_step("Apply", "<p>output force = 20 × 4</p>"),
       ex_step("Check", "<p>20 × 4 = 80, and 80 ÷ 4 = 20 N, the input.</p>"),
       ex_step("Answer", "<p><strong>80 N</strong></p>", ans=True),
     ]}},
}

# ---------- 6. guided (opener + teach) ----------
pd["guided"] = {
 "opener": {
   "label": "Before any equation",
   "display": "A stiff bolt. A short spanner, then a long one.",
   "steps": [
     say("Picture a stiff bolt that will not move with a short spanner."),
     box("You swap to a spanner twice as long and push exactly as hard. Its turning effect is now ___ times bigger. ", 2, "Twice the distance from the pivot, same push, so twice the turn."),
     say("That turning effect has a name: the <strong>moment</strong>. Moment = force × distance from the pivot, so doubling the distance doubles the moment. In symbols, \\(M = F \\times d\\)."),
     box("Try it: a 10 N push, 0.5 m from a pivot. Moment = 10 × 0.5 = ", 5, "Multiply the force by the distance.", done="That is a moment of 5 Nm. Every question in this lesson is built from M = F × d."),
   ]},
 "teach": {
   "bronze": {
     "display": "A spanner turns a bolt with a force of 60 N applied 0.2 m from the bolt.",
     "label": "Together: your first moment",
     "steps": [
       say("Moments use one equation: M = F × d."),
       box("The distance from the bolt, in metres. d = ", 0.2, "Read the perpendicular distance."),
       box("The force, in newtons. F = ", 60, "Read the push from the question."),
       box("Multiply: 60 × 0.2 = ", 12, "Force times distance.", say="So M = 12 Nm."),
       box("Now, what if the spanner were twice as long, 0.4 m? Moment = 60 × 0.4 = ", 24, "Same force, double the distance.", done="Double the distance doubles the moment. That is the whole idea of a moment."),
     ]},
   "silver": {
     "display": "A 6 kg mass hangs 0.5 m from a pivot. On the other side a force acts 1.5 m from the pivot. Balance it. (g = 9.8 N/kg)",
     "label": "Together: weight then balance",
     "steps": [
       say("First turn the mass into a weight: W = m × g."),
       box("Weight of the mass: W = 6 × 9.8 = ", 58.8, "Mass times 9.8."),
       box("Its moment: 58.8 × 0.5 = ", 29.4, "Weight times distance."),
       box("This must equal F × 1.5. Divide: 29.4 ÷ 1.5 = ", 19.6, "Divide the moment by 1.5.", say="So F = 19.6 N."),
       box("Check: 19.6 × 1.5 = ", 29.4, "Force times distance.", done="It matches the 29.4 Nm moment, so 19.6 N balances the beam."),
     ]},
   "gold": {
     "display": "A beam balances on a pivot. On the left, a 60 N force acts 0.5 m from the pivot and a 40 N force acts 1.0 m from the pivot. A single force acts 0.5 m from the pivot on the right. Find it.",
     "label": "Together: add the moments",
     "steps": [
       say("Two forces on the left, so work out each moment and add them."),
       box("First moment: 60 × 0.5 = ", 30, "Force times distance."),
       box("Second moment: 40 × 1.0 = ", 40, "Force times distance."),
       box("Total left moment: 30 + 40 = ", 70, "Add the two moments."),
       box("Balance: F × 0.5 = 70. Divide: 70 ÷ 0.5 = ", 140, "Divide the total by 0.5.", say="So F = 140 N."),
       box("Check: 140 × 0.5 = ", 70, "Force times distance.", done="It equals the 70 Nm total, so 140 N balances the beam."),
     ]},
 }
}

json.dump(pd, open("lesson_higher-calculations-L03@4def3c722e.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written")
