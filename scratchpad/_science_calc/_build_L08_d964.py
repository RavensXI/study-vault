# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_canon_live.json", encoding="utf-8"))

# ---- 1. Fix em dashes in preserved fields (validator hard gate) ----
mc = pd["method_card"]
mc["content"] = ("<p>Three equation families run this lesson.</p>"
    "<p><strong>F = ma:</strong> resultant force = mass × acceleration. A zero resultant force means constant speed (Newton's first law); a non-zero resultant causes acceleration (second law).</p>"
    "<p><strong>Momentum:</strong> p = mv, measured in kg m/s, and it is conserved in a closed system. The force from a momentum change is F = Δp ÷ Δt, so a longer collision time gives a smaller force. That is why crumple zones save lives.</p>"
    "<p><strong>Wave speed:</strong> v = f × λ. Convert any wavelength to metres before substituting.</p>")

pd["exam_context"]["frequency"] = "High: F = ma and wave speed appear in most papers"

for we in pd["worked_examples"]:
    for st in we["steps"]:
        if "label" in st:
            st["label"] = st["label"].replace(" — ", ": ")

# ---- 2. Fix existing SVGs (remove xmlns/http, add role + aria-label) ----
ARIA_QMARK = "A transverse wave with its wavelength labelled as unknown"
ARIA_300 = "A radio wave with its wavelength labelled 300 m"
ARIA_004 = "A transverse wave with its wavelength labelled 0.04 m"
def fix_svg(q):
    q = q.replace(' xmlns="http://www.w3.org/2000/svg"', '')
    if "λ = ?" in q:
        label = ARIA_QMARK
    elif "300 m" in q:
        label = ARIA_300
    else:
        label = ARIA_004
    q = q.replace('<svg viewBox="0 0 480 190"',
                  '<svg viewBox="0 0 480 190" role="img" aria-label="%s"' % label, 1)
    return q

pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    for p in pb[tier]:
        if "question" in p and "<svg" in p["question"]:
            p["question"] = fix_svg(p["question"])

# ---- 3. Repair silver[1] duplicate solution (18000 collides with silver[3]) ----
s1 = pb["silver"][1]
assert "900 kg car brakes" in s1["display"], s1["display"]
s1["display"] = "A 1,000 kg car brakes from 20 m/s to rest. Calculate the change in momentum."
s1["solutions"] = [20000]

# ---- 4. Attach hint, misconceptions(+expect), guided_steps per problem ----
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d
def sayonly(say):
    return {"say": say}

DATA = {
 "bronze": {
  0: {
   "hint": "Use F = m × a: multiply the mass by the acceleration.",
   "misc": [{"pattern":"wrong_equation","check":"common","expect":9,
             "message":"F = m × a means multiply, not add. F = 5 × 4 = 20 N."}],
   "gs": [
     box("Read off the mass, m = ",5,"It is the mass given in the question.",post=" kg",
         say="Choose the equation. A force from mass and acceleration means <strong>F = m × a</strong>."),
     box("Read off the acceleration, a = ",4,"It is the acceleration given in the question.",post=" m/s²"),
     box("F = 5 × 4 = ",20,"Multiply mass by acceleration.",post=" N",phase="substitute",
         say="Both values are already in base units, so substitute straight in.",done="F = 20 N."),
     box("F ÷ m = 20 ÷ 5 = ",4,"Divide the force by the mass to get back the acceleration.",
         say="Check by working backwards.",done="That returns a = 4 m/s², so F = 20 N is right."),
   ]},
  1: {
   "hint": "Use F = m × a: multiply the mass by the acceleration.",
   "misc": [{"pattern":"wrong_equation","check":"common","expect":1203,
             "message":"F = m × a means multiply: F = 1200 × 3 = 3,600 N. Adding gives 1203, which is wrong."}],
   "gs": [
     box("Mass m = ",1200,"The mass given.",post=" kg",
         say="A force from mass and acceleration: <strong>F = m × a</strong>."),
     box("Acceleration a = ",3,"The acceleration given.",post=" m/s²"),
     box("F = 1200 × 3 = ",3600,"Multiply mass by acceleration.",post=" N",phase="substitute",
         say="Values already in base units, substitute in.",done="F = 3,600 N."),
     box("F ÷ m = 3600 ÷ 1200 = ",3,"Divide force by mass.",
         say="Check backwards.",done="Returns a = 3 m/s². Correct."),
   ]},
  2: {
   "hint": "Use v = f × λ: multiply frequency by wavelength.",
   "misc": [{"pattern":"inverse_error","check":"common","expect":125,
             "message":"Wave speed multiplies: v = f × λ = 5 × 0.04 = 0.2 m/s. Dividing gives 125, which is wrong."}],
   "gs": [
     box("Frequency f = ",5,"The frequency given.",post=" Hz",
         say="Wave speed links frequency and wavelength: <strong>v = f × λ</strong>."),
     box("Wavelength λ = ",0.04,"The wavelength given, in metres.",post=" m",
         say="The wavelength is 0.04 m, already in metres, so no conversion."),
     box("v = 5 × 0.04 = ",0.2,"Multiply frequency by wavelength.",post=" m/s",phase="substitute",
         say="Substitute in.",done="v = 0.2 m/s."),
     box("v ÷ f = 0.2 ÷ 5 = ",0.04,"Divide speed by frequency to get back the wavelength.",
         say="Check backwards.",done="Returns λ = 0.04 m. Correct."),
   ]},
  3: {
   "hint": "Rearrange v = f × λ to λ = v ÷ f, then divide.",
   "misc": [{"pattern":"inverse_error","check":"common","expect":57800,
             "message":"Rearrange to λ = v ÷ f = 340 ÷ 170 = 2 m. Multiplying gives 57,800, far too big."}],
   "gs": [
     box("Speed v = ",340,"The speed given.",post=" m/s",
         say="Rearrange <strong>v = f × λ</strong> to make wavelength the subject: λ = v ÷ f."),
     box("Frequency f = ",170,"The frequency given.",post=" Hz"),
     box("λ = 340 ÷ 170 = ",2,"Divide speed by frequency.",post=" m",phase="substitute",
         say="Substitute in.",done="λ = 2 m."),
     box("f × λ = 170 × 2 = ",340,"Multiply frequency by wavelength to get back the speed.",
         say="Check backwards.",done="Returns v = 340 m/s. Correct."),
   ]},
  4: {
   "hint": "Rearrange F = m × a to a = F ÷ m, then divide.",
   "misc": [{"pattern":"inverse_error","check":"common","expect":120000,
             "message":"Rearrange to a = F ÷ m = 600 ÷ 200 = 3 m/s². Multiplying gives 120,000, which is wrong."}],
   "gs": [
     box("Force F = ",600,"The force given.",post=" N",
         say="Rearrange <strong>F = m × a</strong> to make acceleration the subject: a = F ÷ m."),
     box("Mass m = ",200,"The mass given.",post=" kg"),
     box("a = 600 ÷ 200 = ",3,"Divide force by mass.",post=" m/s²",phase="substitute",
         say="Substitute in.",done="a = 3 m/s²."),
     box("m × a = 200 × 3 = ",600,"Multiply mass by acceleration to get back the force.",
         say="Check backwards.",done="Returns F = 600 N. Correct."),
   ]},
  5: {
   "hint": "Use p = m × v: multiply mass by velocity.",
   "misc": [{"pattern":"wrong_equation","check":"common","expect":75,
             "message":"Momentum multiplies: p = m × v = 70 × 5 = 350 kg m/s. Adding gives 75, which is wrong."}],
   "gs": [
     box("Mass m = ",70,"The mass given.",post=" kg",
         say="Momentum links mass and velocity: <strong>p = m × v</strong>."),
     box("Velocity v = ",5,"The speed given.",post=" m/s"),
     box("p = 70 × 5 = ",350,"Multiply mass by velocity.",post=" kg m/s",phase="substitute",
         say="Substitute in.",done="p = 350 kg m/s."),
     box("p ÷ m = 350 ÷ 70 = ",5,"Divide momentum by mass to get back the velocity.",
         say="Check backwards.",done="Returns v = 5 m/s. Correct."),
   ]},
 },
 "silver": {
  0: {
   "hint": "Rearrange to f = v ÷ λ, then divide, keeping the power of ten.",
   "misc": [{"pattern":"inverse_error","check":"common","expect":90000000000,
             "message":"Frequency is f = v ÷ λ = 3×10⁸ ÷ 300 = 1×10⁶ Hz. Multiplying gives 9×10¹⁰, far too large."}],
   "gs": [
     box("Divide the front numbers: 3 ÷ 300 = ",0.01,"3 divided by 300.",
         say="Rearrange <strong>v = f × λ</strong> for frequency: f = v ÷ λ. The wavelength 300 m is already in metres."),
     box("Write 0.01 × 10⁸ in full: f = ",1000000,"0.01 × 100,000,000.",post=" Hz",phase="substitute",
         say="The power of ten stays: 0.01 × 10⁸.",done="f = 1,000,000 Hz, which is 1 MHz."),
     box("f × λ = 1000000 × 300 = ",300000000,"Multiply frequency by wavelength to get back the speed.",
         say="Check backwards.",done="Returns 3 × 10⁸ m/s, the speed. Correct."),
   ]},
  1: {
   "hint": "Change in velocity is 20 m/s (down to rest); use Δp = m × Δv.",
   "misc": [{"pattern":"wrong_equation","check":"common","expect":1020,
             "message":"Change in momentum is m × Δv = 1000 × 20 = 20,000 kg m/s. Adding the numbers gives 1020, which is wrong."}],
   "gs": [
     box("Mass m = ",1000,"The mass given.",post=" kg",
         say="Change in momentum: <strong>Δp = m × Δv</strong>. The car brakes from 20 m/s to rest, so Δv = 20 m/s."),
     box("Change in velocity Δv = ",20,"From 20 m/s down to 0 is a change of 20.",post=" m/s"),
     box("Δp = 1000 × 20 = ",20000,"Multiply mass by the change in velocity.",post=" kg m/s",phase="substitute",
         say="Substitute in.",done="Δp = 20,000 kg m/s."),
     box("Δp ÷ m = 20000 ÷ 1000 = ",20,"Divide by mass to get back the change in velocity.",
         say="Check backwards.",done="Returns Δv = 20 m/s. Correct."),
   ]},
  2: {
   "hint": "Rearrange F = m × a to m = F ÷ a, then divide.",
   "misc": [{"pattern":"inverse_error","check":"common","expect":3750,
             "message":"Rearrange to m = F ÷ a = 1500 ÷ 2.5 = 600 kg. Multiplying gives 3750, which is wrong."}],
   "gs": [
     box("Force F = ",1500,"The force given.",post=" N",
         say="Rearrange <strong>F = m × a</strong> for mass: m = F ÷ a."),
     box("Acceleration a = ",2.5,"The acceleration given.",post=" m/s²"),
     box("m = 1500 ÷ 2.5 = ",600,"Divide force by acceleration.",post=" kg",phase="substitute",
         say="Substitute in.",done="m = 600 kg."),
     box("m × a = 600 × 2.5 = ",1500,"Multiply mass by acceleration to get back the force.",
         say="Check backwards.",done="Returns F = 1,500 N. Correct."),
   ]},
  3: {
   "hint": "Use F = Δp ÷ Δt: divide the momentum change by the time.",
   "misc": [{"pattern":"inverse_error","check":"common","expect":45,
             "message":"Force is Δp ÷ Δt = 900 ÷ 0.05 = 18,000 N. Multiplying by the time gives 45, which is wrong."}],
   "gs": [
     box("Change in momentum Δp = ",900,"The change in momentum given.",post=" kg m/s",
         say="Force from a momentum change: <strong>F = Δp ÷ Δt</strong>."),
     box("Time Δt = ",0.05,"The collision time given, in seconds.",post=" s"),
     box("F = 900 ÷ 0.05 = ",18000,"Divide the momentum change by the time.",post=" N",phase="substitute",
         say="Substitute in.",done="F = 18,000 N."),
     box("F × Δt = 18000 × 0.05 = ",900,"Multiply force by time to get back the momentum change.",
         say="Check backwards.",done="Returns Δp = 900 kg m/s. Correct."),
   ]},
 },
 "gold": {
  0: {
   "hint": "Use the longer time, 0.25 s, in F = Δp ÷ Δt.",
   "misc": [
     {"pattern":"wrong_time","check":"common","expect":18000,
      "message":"With the crumple zone use the longer time, 0.25 s: F = 900 ÷ 0.25 = 3,600 N. Using 0.05 s gives 18,000 N, the force without the zone."},
     {"pattern":"inverse_error","check":"common","expect":225,
      "message":"Force is Δp ÷ Δt = 900 ÷ 0.25 = 3,600 N. Multiplying by the time gives 225, which is wrong."}],
   "gs": [
     box("Change in momentum Δp = ",900,"The change in momentum given.",post=" kg m/s",
         say="Force from a momentum change: <strong>F = Δp ÷ Δt</strong>. The crumple zone means use the LONGER time, 0.25 s."),
     box("Time with the crumple zone, Δt = ",0.25,"Use the longer time, 0.25 s, not 0.05 s.",post=" s"),
     box("F = 900 ÷ 0.25 = ",3600,"Divide the momentum change by the longer time.",post=" N",phase="substitute",
         say="Substitute in.",done="F = 3,600 N with the crumple zone."),
     box("900 ÷ 0.05 = ",18000,"Divide by the shorter time 0.05 s.",post=" N",
         say="Compare with no crumple zone, where the time is only 0.05 s:",
         done="Without the zone the force is 18,000 N. The crumple zone cuts it to 3,600 N."),
   ]},
  1: {
   "hint": "First find impulse F × t (the change in momentum), then divide by mass for speed.",
   "misc": [
     {"pattern":"forgot_step","check":"common","expect":60,
      "message":"Impulse = F × t = 120 × 0.5 = 60 N s. That is the change in momentum, not the speed. Divide by mass: v = 60 ÷ 60 = 1 m/s."},
     {"pattern":"forgot_step","check":"common","expect":2,
      "message":"You must include the time. v = (F × t) ÷ m = (120 × 0.5) ÷ 60 = 1 m/s. Using F ÷ m alone gives 2 m/s."}],
   "gs": [
     box("F × t = 120 × 0.5 = ",60,"Multiply the force by the time.",post=" N s",
         say="Two steps. First the impulse, which equals the change in momentum: impulse = F × t.",
         done="The change in momentum is 60 N s."),
     box("v = 60 ÷ 60 = ",1,"Divide the change in momentum by the mass.",post=" m/s",phase="substitute",
         say="Now the speed from the change in momentum: v = Δp ÷ m.",done="v = 1 m/s."),
     box("m × v = 60 × 1 = ",60,"Multiply mass by speed to get back the change in momentum.",
         say="Check backwards.",done="Returns Δp = 60 N s, matching the impulse. Correct."),
   ]},
  2: {
   "hint": "Total momentum stays 0: the 3 kg trolley carries the same momentum as the 2 kg one, the other way.",
   "misc": [
     {"pattern":"forgot_step","check":"common","expect":6,
      "message":"6 kg m/s is the momentum of the 3 kg trolley, not its speed. Divide by its mass: v = 6 ÷ 3 = 2 m/s."},
     {"pattern":"wrong_conservation","check":"common","expect":3,
      "message":"The trolleys do not share the same speed because their masses differ. Momentum is conserved: 2 × 3 = 3 × v, so v = 6 ÷ 3 = 2 m/s."}],
   "gs": [
     box("2 × 3 = ",6,"Multiply its mass by its speed.",post=" kg m/s",
         say="Both trolleys start at rest, so the total momentum is 0 and must stay 0. Momentum of the 2 kg trolley after: mass × speed.",
         done="The 2 kg trolley carries 6 kg m/s."),
     box("v = 6 ÷ 3 = ",2,"Divide the momentum by the 3 kg mass.",post=" m/s",phase="substitute",
         say="To keep the total at 0, the 3 kg trolley must carry the same 6 kg m/s the other way: v = 6 ÷ mass.",
         done="Speed = 2 m/s (moving the opposite way)."),
     box("3 × 2 = ",6,"Multiply the 3 kg mass by its speed.",post=" kg m/s",
         say="Check backwards.",done="The 3 kg trolley carries 6 kg m/s, balancing the other. Total = 0. Correct."),
   ]},
 },
}

for tier, items in DATA.items():
    for idx, spec in items.items():
        p = pb[tier][idx]
        p["hint"] = spec["hint"]
        p["misconceptions"] = spec["misc"]
        p["guided_steps"] = spec["gs"]

# ---- 5. Tier descriptions ----
pb["bronze_description"] = "One equation, all values already in base units. Write it, substitute, compute, state the unit."
pb["silver_description"] = "Rearrange the equation first, or handle a value in standard form, then substitute and compute."
pb["gold_description"] = "Chain two ideas: impulse then speed, or conservation of momentum, working through more than one step."

# ---- 6. tier_guides ----
pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one equation, straight in",
   "steps": [
     "Pick the equation the quantities point to: F = m × a for forces, v = f × λ for waves, p = m × v for momentum.",
     "The values are already in base units (kg, m/s, m, s), so substitute them straight in.",
     "Compute, then write the answer with its unit (N, m/s, m, kg m/s)."
   ],
   "example": {
     "question": "A 4 kg mass accelerates at 5 m/s². Calculate the resultant force.",
     "steps": [
       {"label":"Equation","content":"<p>F = m × a</p>"},
       {"label":"Substitute","content":"<p>F = 4 × 5</p>"},
       {"label":"Check","content":"<p>F ÷ m = 20 ÷ 4 = 5 m/s² ✓</p>"},
       {"label":"Answer","content":"<p><strong>F = 20 N</strong></p>","isAnswer":True,"is_answer":True}
     ]
   }
 },
 "silver": {
   "title": "Silver: rearrange, then substitute",
   "steps": [
     "The quantity you want is not the subject yet. Rearrange first: from F = m × a you get a = F ÷ m or m = F ÷ a; from v = f × λ you get f = v ÷ λ or λ = v ÷ f.",
     "Large or small numbers may be in standard form. Divide the front numbers, keep the power of ten, then write it out.",
     "Substitute, compute, and state the unit."
   ],
   "example": {
     "question": "A wave travels at 480 m/s with a frequency of 160 Hz. Calculate its wavelength.",
     "steps": [
       {"label":"Rearrange","content":"<p>v = f × λ, so λ = v ÷ f</p>"},
       {"label":"Substitute","content":"<p>λ = 480 ÷ 160</p>"},
       {"label":"Check","content":"<p>f × λ = 160 × 3 = 480 m/s ✓</p>"},
       {"label":"Answer","content":"<p><strong>λ = 3 m</strong></p>","isAnswer":True,"is_answer":True}
     ]
   }
 },
 "gold": {
   "title": "Gold: chain two steps",
   "steps": [
     "Gold problems need two moves. A common chain: impulse (F × t) gives the change in momentum, then divide by mass for the speed.",
     "Or use conservation of momentum: total momentum before = total momentum after. If everything starts at rest, the total is zero, so the two parts carry equal and opposite momentum.",
     "Finish the second step and state the unit."
   ],
   "example": {
     "question": "A 0.2 kg ball is pushed from rest by a 6 N force for 0.5 s. Calculate its final speed.",
     "steps": [
       {"label":"Impulse","content":"<p>Impulse = F × t = 6 × 0.5 = 3 N s = Δp</p>"},
       {"label":"Speed","content":"<p>v = Δp ÷ m = 3 ÷ 0.2</p>"},
       {"label":"Check","content":"<p>Δp = m × v = 0.2 × 15 = 3 N s ✓</p>"},
       {"label":"Answer","content":"<p><strong>v = 15 m/s</strong></p>","isAnswer":True,"is_answer":True}
     ]
   }
 }
}

# ---- 7. guided (opener + teach) ----
pd["guided"] = {
 "opener": {
   "label": "Before any equations",
   "display": "You give two shopping trolleys the SAME shove.<br>Empty trolley: 10 kg. Full of bricks: 50 kg.",
   "steps": [
     box("Which speeds up more, the 10 kg or the 50 kg? Type its mass: ",10,
         "The lighter one is easier to get moving.",
         say="No physics yet, just instinct. One shove, two trolleys, which shoots off faster?"),
     box("100 ÷ 10 = ",10,"Divide the force by the mass.",post=" m/s²",
         say="Now put a number on it. The shove is a force of 100 N. Acceleration = force ÷ mass. For the empty trolley:"),
     box("100 ÷ 50 = ",2,"Divide the force by the mass.",post=" m/s²",
         say="And the heavy one:"),
     sayonly("You just used <strong>F = ma</strong>, rearranged to a = F ÷ m. Same force, but the 10 kg trolley gets 10 m/s² and the 50 kg one only 2 m/s². More mass, less acceleration. That one equation drives most of this lesson.")
   ]
 },
 "teach": {
   "bronze": {
     "display": "A 3 kg ball accelerates at 6 m/s². Calculate the resultant force.",
     "label": "Together: your first one",
     "steps": [
       box("Mass m = ",3,"The mass given.",post=" kg",
           say="The move: pick the equation, put the numbers in, compute. Equation: <strong>F = m × a</strong>."),
       box("Acceleration a = ",6,"The acceleration given.",post=" m/s²"),
       box("F = 3 × 6 = ",18,"Multiply mass by acceleration.",post=" N",
           say="Substitute straight in.",done="F = 18 N."),
       box("F ÷ m = 18 ÷ 3 = ",6,"Divide force by mass to get back the acceleration.",
           say="Check backwards.",done="Returns 6 m/s². Correct. That was the whole move: substitute and compute.")
     ]
   },
   "silver": {
     "display": "A wave travels at 320 m/s with a frequency of 80 Hz. Calculate its wavelength.",
     "label": "Together: the silver move",
     "steps": [
       box("Speed v = ",320,"The speed given.",post=" m/s",
           say="The new move: rearrange first. <strong>v = f × λ</strong>, so λ = v ÷ f."),
       box("Frequency f = ",80,"The frequency given.",post=" Hz"),
       box("λ = 320 ÷ 80 = ",4,"Divide speed by frequency.",post=" m",
           say="Now substitute.",done="λ = 4 m."),
       box("f × λ = 80 × 4 = ",320,"Multiply frequency by wavelength to get back the speed.",
           say="Check backwards.",done="Returns 320 m/s. Correct. The one new move was rearranging before substituting.")
     ]
   },
   "gold": {
     "display": "A 2 kg trolley speeds up from 3 m/s to 8 m/s in 0.5 s. Calculate the change in momentum, then the resultant force.",
     "label": "Together: the gold move",
     "steps": [
       box("Δv = 8 − 3 = ",5,"Subtract the starting speed from the final speed.",post=" m/s",
           say="Gold problems chain two equations. First the change in momentum: <strong>Δp = m × Δv</strong>."),
       box("Δp = 2 × 5 = ",10,"Multiply mass by the change in velocity.",post=" kg m/s",
           done="Δp = 10 kg m/s."),
       box("F = 10 ÷ 0.5 = ",20,"Divide the momentum change by the time.",post=" N",
           say="Now the force: <strong>F = Δp ÷ Δt</strong>.",done="F = 20 N."),
       box("F × Δt = 20 × 0.5 = ",10,"Multiply force by time to get back Δp.",
           say="Check backwards.",done="Returns Δp = 10 kg m/s. Correct. The gold move was chaining two equations.")
     ]
   }
 }
}

json.dump(pd, io.open("lesson_physics-calculations-L08@d964afae07.json","w",encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("MINE written")
