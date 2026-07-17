# -*- coding: utf-8 -*-
import json, io, sys
from fractions import Fraction as F
import importlib.util
spec = importlib.util.spec_from_file_location("b", "_L09ocr_build.py")
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
num = b.num
sys.stdout.reconfigure(encoding="utf-8")

# ---------- misconception simulators (return determinate wrong (x,y)) ----------
def sim_rhs_added(A, Bq, elim, sub_eq):  # subtract problems: LHS subtracted, RHS ADDED
    ei = 0 if elim == 'x' else 1; ki = 1 - ei; keptvar = 'y' if elim == 'x' else 'x'
    hi, lo = (A, Bq) if A[ki] >= Bq[ki] else (Bq, A)
    kc = hi[ki] - lo[ki]; wrong_rhs = hi[2] + lo[2]
    kept = F(wrong_rhs, kc); sa, sb, sc = sub_eq
    if keptvar == 'x': other = F(sc - sa * kept, sb); return (num(kept), num(other))
    else: other = F(sc - sb * kept, sa); return (num(other), num(kept))

def sim_add_rhs_wrong(A, Bq, elim, sub_eq):  # add problems: LHS added, RHS SUBTRACTED
    ei = 0 if elim == 'x' else 1; ki = 1 - ei; keptvar = 'y' if elim == 'x' else 'x'
    kc = A[ki] + Bq[ki]; wrong_rhs = A[2] - Bq[2]
    kept = F(wrong_rhs, kc); sa, sb, sc = sub_eq
    if keptvar == 'x': other = F(sc - sa * kept, sb); return (num(kept), num(other))
    else: other = F(sc - sb * kept, sa); return (num(other), num(kept))

def sim_scaled_lhs(eqA, eqB, sB, elim, sub_eq):  # silver: eqB LHS ×sB, RHS unscaled
    Bc = (eqB[0] * sB, eqB[1] * sB, eqB[2])
    ei = 0 if elim == 'x' else 1; ki = 1 - ei; keptvar = 'y' if elim == 'x' else 'x'
    if eqA[ei] == Bc[ei]:
        hi, lo = (eqA, Bc) if eqA[ki] >= Bc[ki] else (Bc, eqA)
        kc = hi[ki] - lo[ki]; rhs = hi[2] - lo[2]
    else:
        kc = eqA[ki] + Bc[ki]; rhs = eqA[2] + Bc[2]
    kept = F(rhs, kc); sa, sb, sc = sub_eq
    if keptvar == 'x': other = F(sc - sa * kept, sb); return (num(kept), num(other))
    else: other = F(sc - sb * kept, sa); return (num(other), num(kept))

def sim_sign_slip(known_eq, known_var, known_val):  # add the moved term instead of subtracting
    sa, sb, sc = known_eq
    kc = sa if known_var == 'x' else sb
    oc = sb if known_var == 'x' else sa
    knownterm = kc * known_val
    slip = F(sc + knownterm, oc)
    if known_var == 'x': return (num(known_val), num(slip))
    else: return (num(slip), num(known_val))

# ---------- problem specs: (eqA, eqB, sA, sB, elim, sub_idx, misc_spec) ----------
def mk(eqA, eqB, sA, sB, elim, sub_idx, hint, miscs):
    steps, sol = b.build_walk(eqA, eqB, sA, sB, elim, sub_idx)
    return {
        "display": f"Solve \\({b.eqlatex(*eqA)}\\) and \\({b.eqlatex(*eqB)}\\)",
        "solutions": [num(sol[0]), num(sol[1])],
        "input_type": "xy_pair", "calculator": False,
        "hint": hint, "misconceptions": miscs, "guided_steps": steps,
    }, sol

MSG = {
 "rhs_added": "When you subtract the equations, the right-hand sides subtract too, exactly like the left. Adding them sends every step after that off course.",
 "add_rhs": "The y terms have opposite signs, so you ADD the equations. When you add the left-hand sides, add the right-hand sides too, not subtract them.",
 "scaled_lhs": "When you multiply an equation, multiply BOTH sides. If the right-hand side is left unscaled, the value you find fits neither original equation.",
 "sign_slip": "Moving a term across the equals sign flips its sign. It looks like it was added instead of subtracted, which pushes the second value the wrong way.",
}

problems = {"bronze": [], "silver": [], "gold": []}

# BRONZE
b0, _ = mk((1,1,10),(1,-1,4),1,1,'y',0,
    "The y terms are +y and −y, opposite signs, so ADD the equations.",
    [{"pattern":"add_rhs_wrong","check":"add_rhs_wrong","expect":list(sim_add_rhs_wrong((1,1,10),(1,-1,4),'y',(1,1,10))),"message":MSG["add_rhs"],"note":"add LHS, subtract RHS"}])
b1, _ = mk((2,1,9),(1,1,6),1,1,'y',1,
    "Both equations have +y (same sign), so subtract one from the other.",
    [{"pattern":"rhs_not_subtracted","check":"rhs_not_subtracted","expect":list(sim_rhs_added((2,1,9),(1,1,6),'y',(1,1,6))),"message":MSG["rhs_added"],"note":"RHS added"}])
b2, _ = mk((3,1,11),(1,1,5),1,1,'y',1,
    "Both equations have +y, so subtract to make the y terms vanish.",
    [{"pattern":"rhs_not_subtracted","check":"rhs_not_subtracted","expect":list(sim_rhs_added((3,1,11),(1,1,5),'y',(1,1,5))),"message":MSG["rhs_added"],"note":"RHS added"}])
b3, _ = mk((1,2,8),(1,1,5),1,1,'x',1,
    "The x terms already match, so subtract to remove them.",
    [{"pattern":"rhs_not_subtracted","check":"rhs_not_subtracted","expect":list(sim_rhs_added((1,2,8),(1,1,5),'x',(1,1,5))),"message":MSG["rhs_added"],"note":"RHS added"}])
b4, _ = mk((2,1,7),(3,-1,8),1,1,'y',0,
    "Opposite signs on y, so adding the equations makes y disappear.",
    [{"pattern":"substitute_sign_slip","check":"substitute_sign_slip","expect":list(sim_sign_slip((2,1,7),'x',3)),"message":MSG["sign_slip"],"note":"y = 7 + 6 slip"}])
b5, _ = mk((1,3,13),(1,1,7),1,1,'x',1,
    "The x terms match, so subtract to leave just y terms.",
    [{"pattern":"rhs_not_subtracted","check":"rhs_not_subtracted","expect":list(sim_rhs_added((1,3,13),(1,1,7),'x',(1,1,7))),"message":MSG["rhs_added"],"note":"RHS added"}])
b6, _ = mk((3,1,14),(1,1,6),1,1,'y',1,
    "Both equations have +y, so subtract them.",
    [{"pattern":"rhs_not_subtracted","check":"rhs_not_subtracted","expect":list(sim_rhs_added((3,1,14),(1,1,6),'y',(1,1,6))),"message":MSG["rhs_added"],"note":"RHS added"}])
problems["bronze"] = [b0,b1,b2,b3,b4,b5,b6]

# SILVER (multiply one equation)
s0, _ = mk((3,2,16),(1,1,6),1,2,'y',1,
    "Multiply the second equation by 2 so both have 2y, then subtract.",
    [{"pattern":"scaled_lhs_only","check":"scaled_lhs_only","expect":list(sim_scaled_lhs((3,2,16),(1,1,6),2,'y',(1,1,6))),"message":MSG["scaled_lhs"],"note":"RHS left as 6"}])
s1, _ = mk((2,3,18),(1,1,7),1,3,'y',1,
    "Multiply the second equation by 3 so both have 3y, then subtract.",
    [{"pattern":"scaled_lhs_only","check":"scaled_lhs_only","expect":list(sim_scaled_lhs((2,3,18),(1,1,7),3,'y',(1,1,7))),"message":MSG["scaled_lhs"],"note":"RHS left as 7"}])
s2, _ = mk((3,2,11),(1,1,4),1,2,'y',1,
    "Multiply the second equation by 2 so both have 2y, then subtract.",
    [{"pattern":"scaled_lhs_only","check":"scaled_lhs_only","expect":list(sim_scaled_lhs((3,2,11),(1,1,4),2,'y',(1,1,4))),"message":MSG["scaled_lhs"],"note":"RHS left as 4"}])
s3, _ = mk((5,-2,4),(1,1,5),1,2,'y',1,
    "Multiply the second equation by 2. The y terms are then −2y and +2y, opposite signs, so add.",
    [{"pattern":"substitute_sign_slip","check":"substitute_sign_slip","expect":list(sim_sign_slip((5,-2,4),'x',2)),"message":MSG["sign_slip"],"note":"10 − 2y = 4 mishandled, y = 7 slip"}])
s4, _ = mk((3,4,23),(1,2,11),1,2,'y',1,
    "Multiply the second equation by 2 so both have 4y, then subtract.",
    [{"pattern":"scaled_lhs_only","check":"scaled_lhs_only","expect":list(sim_scaled_lhs((3,4,23),(1,2,11),2,'y',(1,2,11))),"message":MSG["scaled_lhs"],"note":"RHS left as 11"}])
problems["silver"] = [s0,s1,s2,s3,s4]

# GOLD (multiply both)
g0, _ = mk((2,3,12),(5,-2,11),2,3,'y',0,
    "Scale both equations: ×2 and ×3 make the y terms +6y and −6y. Opposite signs, so add.",
    [{"pattern":"substitute_sign_slip","check":"substitute_sign_slip","expect":list(sim_sign_slip((2,3,12),'x',3)),"message":MSG["sign_slip"],"note":"3y = 12 + 6 slip"}])
g1, _ = mk((3,4,5),(2,-3,9),3,4,'y',0,
    "Scale both equations: ×3 and ×4 make the y terms +12y and −12y. Opposite signs, so add.",
    [{"pattern":"substitute_sign_slip","check":"substitute_sign_slip","expect":list(sim_sign_slip((3,4,5),'x',3)),"message":MSG["sign_slip"],"note":"4y = 5 + 9 slip"}])

# GOLD word problem (xy_pair: x = adult tickets, y = child tickets)
word_steps = [
 {"say":"Let x = the number of adult tickets and y = the number of child tickets. Two facts give two equations: total tickets \\(x + y = 120\\), and total money \\(8x + 5y = 780\\)."},
 {"say":"Make the y terms match. Multiply ALL of \\(x + y = 120\\) by 5: every term, both sides.",
  "pre":"x × 5 = ","post":"x","answer":5,"hint":"Just multiply the number in front."},
 {"say":None,"pre":"y × 5 = ","post":"y","answer":5,"hint":"Just multiply the number in front."},
 {"pre":"and the right-hand side: 120 × 5 = ","post":"","answer":600,"hint":"The right-hand side gets multiplied too. That's the step everyone forgets."},
 {"say":"Both equations now have 5y, the same sign. <strong>Same Signs Subtract.</strong> Take \\(5x + 5y = 600\\) away from \\(8x + 5y = 780\\), term by term:",
  "pre":"8x − 5x = ","post":"x","answer":3,"hint":"Subtract the numbers in front: 8 − 5."},
 {"pre":"5y − 5y = ","post":"","answer":0,"done":"Gone. That was the whole point.","hint":"They're identical, and anything minus itself is 0."},
 {"pre":"780 − 600 = ","post":"","answer":180,"hint":"The right-hand sides get subtracted too, exactly like the left."},
 {"say":"So 3x = 180.","pre":"x = ","post":"","answer":60,"hint":"Divide both sides by 3. That is the number of adult tickets."},
 {"say":"Now find y, the child tickets. Put x = 60 into \\(x + y = 120\\):","phase":"substitute",
  "pre":"60 + y = 120  →  y = ","post":"","answer":60,"hint":"Take 60 from both sides."},
 {"say":"Check the money adds up in the other equation:","phase":"substitute",
  "pre":"8 × 60 + 5 × 60 = ","post":"","answer":780,"done":"480 + 300 = 780, so 60 adult tickets and 60 child tickets is right.","hint":"Work it out. If it doesn't give 780, something slipped."},
]
g2 = {
 "display":"A cinema sells adult tickets for £8 and child tickets for £5. One evening 120 tickets are sold for a total of £780. Taking x as the number of adult tickets and y as the number of child tickets, how many of each are sold?",
 "solutions":[60,60],"input_type":"xy_pair","calculator":True,
 "hint":"Write two equations: x + y = 120 and 8x + 5y = 780. Multiply the first by 5, then subtract.",
 "misconceptions":[],"guided_steps":word_steps,
}
problems["gold"] = [g0,g1,g2]

# ---------- teach ----------
tb_steps, tb_sol = b.build_walk((3,1,12),(1,1,6),1,1,'y',1)
ts_steps, ts_sol = b.build_walk((2,3,13),(1,1,5),1,3,'y',1)
tg_steps, tg_sol = b.build_walk((4,3,18),(3,2,13),2,3,'y',1)
teach = {
 "bronze":{"display":"Solve \\(3x + y = 12\\) and \\(x + y = 6\\)","label":"Together: your first one","steps":tb_steps},
 "silver":{"display":"Solve \\(2x + 3y = 13\\) and \\(x + y = 5\\)","label":"Together: the silver move","steps":ts_steps},
 "gold":{"display":"Solve \\(4x + 3y = 18\\) and \\(3x + 2y = 13\\)","label":"Together: the gold move","steps":tg_steps},
}

opener = {
 "label":"Before any algebra",
 "display":"2 cinema tickets + 1 popcorn = £25<br>1 cinema ticket + 1 popcorn = £16",
 "steps":[
  {"say":"A trip to the cinema. No algebra, just compare the two orders.",
   "pre":"One cinema ticket costs £","post":"","answer":9,
   "hint":"The only difference between the two orders is one extra ticket, and £9 of price."},
  {"say":"That move, comparing the orders so the popcorn cancels out, is called <strong>elimination</strong>. You just subtracted two equations without noticing.",
   "pre":"And the popcorn? £","post":"","answer":7,
   "hint":"One ticket (£9) and a popcorn cost £16 together."},
  {"say":"Using a value you already know to find the one you don't is <strong>substitution</strong>. Those two moves are the whole topic. Algebra just writes ticket as \\(x\\) and popcorn as \\(y\\): \\(2x + y = 25\\) and \\(x + y = 16\\)."},
 ],
}

tier_guides = {
 "bronze":{"title":"Bronze: the pair already matches","steps":[
   "You need the one pair, an \\(x\\) AND a \\(y\\), that fits both equations. In bronze a matching pair is already there, like \\(+y\\) in both.",
   "<strong>Same Signs Subtract</strong>: subtract one equation from the other (right-hand sides too) and the matched letter vanishes. Opposite signs (\\(+y\\) and \\(-y\\))? Add instead.",
   "Solve the one-letter equation left, then substitute that value into the simpler original equation to find the other letter.",
  ],"example":{"question":"Solve 3x + y = 12 and x + y = 6","steps":[
   {"label":"Match","content":"<p>Both equations have \\(+y\\), the same sign, so subtract.</p>"},
   {"label":"Subtract","content":"<p>\\((3x + y) - (x + y) = 12 - 6\\), so \\(2x = 6\\) and \\(x = 3\\).</p>"},
   {"label":"Substitute","content":"<p>\\(3 + y = 6\\), so \\(y = 3\\).</p>"},
   {"label":"Check","content":"<p>\\(3(3) + 3 = 12\\) ✓</p>"},
   {"label":"Answer","content":"<p>\\(x = 3\\), \\(y = 3\\)</p>","isAnswer":True,"is_answer":True},
  ]}},
 "silver":{"title":"Silver: make a match first","steps":[
   "Nothing matches yet. Multiply ONE whole equation (every term, both sides of the equals sign) until one pair of coefficients matches.",
   "Then it is a bronze question: same signs subtract, opposite signs add, and a letter vanishes.",
   "Substitute your value back, then check the pair in both equations.",
  ],"example":{"question":"Solve 2x + 3y = 13 and x + y = 5","steps":[
   {"label":"Multiply","content":"<p>Second equation \\(\\times 3\\): \\(3x + 3y = 15\\). The 5 is multiplied too.</p>"},
   {"label":"Subtract","content":"<p>\\((3x + 3y) - (2x + 3y) = 15 - 13\\), so \\(x = 2\\).</p>"},
   {"label":"Substitute","content":"<p>\\(2 + y = 5\\), so \\(y = 3\\).</p>"},
   {"label":"Check","content":"<p>\\(2(2) + 3(3) = 13\\) ✓</p>"},
   {"label":"Answer","content":"<p>\\(x = 2\\), \\(y = 3\\)</p>","isAnswer":True,"is_answer":True},
  ]}},
 "gold":{"title":"Gold: multiply both equations","steps":[
   "Sometimes no single multiplication works. Multiply BOTH equations to hit a common coefficient: \\(3y\\) and \\(2y\\) both become \\(6y\\) with \\(\\times 2\\) and \\(\\times 3\\).",
   "Everything else is the same: same signs subtract, opposite signs add, substitute back, check.",
   "Prefer rearranging? <strong>Substitution</strong> also works: make one letter the subject, put it into the other equation. Either method earns full marks.",
  ],"example":{"question":"Solve 4x + 3y = 18 and 3x + 2y = 13","steps":[
   {"label":"Multiply both","content":"<p>First \\(\\times 2\\): \\(8x + 6y = 36\\). Second \\(\\times 3\\): \\(9x + 6y = 39\\).</p>"},
   {"label":"Subtract","content":"<p>\\((9x + 6y) - (8x + 6y) = 39 - 36\\), so \\(x = 3\\).</p>"},
   {"label":"Substitute","content":"<p>\\(9 + 2y = 13\\), so \\(y = 2\\).</p>"},
   {"label":"Check","content":"<p>\\(4(3) + 3(2) = 18\\) ✓</p>"},
   {"label":"Answer","content":"<p>\\(x = 3\\), \\(y = 2\\)</p>","isAnswer":True,"is_answer":True},
  ]}},
}

method_card = {
 "title":"Simultaneous Equations (Linear)",
 "steps":[
   "Match a pair: the same number in front of x, or of y, in both equations.",
   "Same signs? Subtract. Opposite signs? Add. The matched letter vanishes.",
   "Solve what is left, then substitute back to find the other letter.",
   "Check your pair in both original equations.",
 ],
 "content":"<p><strong>Simultaneous equations</strong> are two equations sharing two unknowns. One pair, an \\(x\\) and a \\(y\\), fits both, and you find it by making one letter disappear.</p><p>Remember <strong>SSS: Same Signs Subtract</strong>. Opposite signs? Add. If nothing matches yet, multiply one or both equations first.</p>",
 "example":"<p><strong>Solve</strong> \\(2x + y = 7\\) and \\(3x - y = 8\\)</p><p>Opposite signs on y, so add: \\(5x = 15\\), \\(x = 3\\). Then \\(6 + y = 7\\), so \\(y = 1\\). Check: \\(3(3) - 1 = 8\\) ✓</p>",
}

# ---------- preserve from live ----------
live = json.load(io.open("_L09ocr_live.json", encoding="utf-8"))

def desanitize(obj):  # replace pre-existing em dashes in preserved fields (style rule)
    if isinstance(obj, dict):
        return {k: desanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [desanitize(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace(" — ", ": ").replace("—", ": ")
    return obj
live_worked = desanitize(live.get("worked_examples", []))

pd = {
 "method_card": method_card,
 "topic_links": live.get("topic_links", {"prerequisites": []}),
 "problem_bank": {
   "bronze": problems["bronze"],
   "silver": problems["silver"],
   "gold": problems["gold"],
   "bronze_description": "The numbers in front already match: add or subtract once and a letter vanishes",
   "silver_description": "Multiply one equation first to make a matching pair",
   "gold_description": "Multiply both equations, or switch to the substitution method",
 },
 "related_videos": live.get("related_videos", []),
 "worked_examples": live_worked,
 "tier_guides": tier_guides,
 "guided": {"opener": opener, "teach": teach},
}

json.dump(pd, io.open("lesson_maths-ocr_algebra-L09.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---------- verify final boxes land on solutions + expects != solution ----------
def last_boxes(steps):
    return [s["answer"] for s in steps if s.get("answer") is not None]

errs = []
for tier, ps in problems.items():
    for i, p in enumerate(ps):
        sol = p["solutions"]
        # recompute pair for abstract problems
        for m in p["misconceptions"]:
            e = m["expect"]
            ev = e if isinstance(e, list) else [e]
            if len(ev) == len(sol) and all(abs(float(a)-float(b)) < 1e-9 for a,b in zip(ev, sol)):
                errs.append(f"{tier}[{i}] expect == solution {e}")
print("misc/solution collisions:", errs if errs else "none")

# print teach solutions
print("teach sols:", tb_sol, ts_sol, tg_sol)
# print all expects
for tier, ps in problems.items():
    for i, p in enumerate(ps):
        for m in p["misconceptions"]:
            print(f"  {tier}[{i}] sol={p['solutions']} {m['pattern']} expect={m['expect']}")
print("WROTE lesson_maths-ocr_algebra-L09.json")
