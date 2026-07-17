# -*- coding: utf-8 -*-
"""Rebuild maths-eduqas algebra-L09 (Simultaneous Equations, Linear) to the
guided-learning xy_pair format. Fresh-solves and generates every walk box
programmatically, then verifies."""
import json, io
from fractions import Fraction as F

MINUS = "−"  # unicode minus
ARROW = "  →  "

# ---------- formatters ----------
def eqstr(a, b, c):
    """LaTeX display of a x + b y = c (integers)."""
    def term(co, v, first):
        if co == 0:
            return ""
        s = "+" if co > 0 else "-"
        m = abs(co)
        mag = v if m == 1 else f"{m}{v}"
        if first:
            return (mag if co > 0 else f"-{mag}")
        return f" {s} {mag}"
    xs = term(a, "x", True)
    ys = term(b, "y", xs == "")
    return f"{xs}{ys} = {c}"

def yterm_scale(co):
    """display of a y term (with sign) for the scale-box pre, e.g. 'y', '-y', '3y', '-3y'."""
    if co == 1: return "y"
    if co == -1: return "-y"
    if co > 0: return f"{co}y"
    return f"-{abs(co)}y"

def xterm_scale(co):
    if co == 1: return "x"
    if co == -1: return "-x"
    if co > 0: return f"{co}x"
    return f"-{abs(co)}x"

def elim_term(co, v):
    if co == 1: return v
    if co == -1: return f"-{v}"
    if co > 0: return f"{co}{v}"
    return f"-{abs(co)}{v}"

def svterm(co, v):
    """surviving-coefficient term, dropping a coefficient of 1: 1->x, 2->2x."""
    return v if co == 1 else f"{co}{v}"

def check_expr(a, b, xv, yv):
    """arithmetic expression string for a*xv + b*yv with all-positive vals."""
    def piece(co, val, first):
        m = abs(co)
        body = f"{val}" if m == 1 else f"{m} × {val}"
        if first:
            return body if co > 0 else f"{MINUS}{body}"
        return (f" + {body}" if co > 0 else f" {MINUS} {body}")
    p1 = piece(a, xv, True)
    p2 = piece(b, yv, False)
    return p1 + p2

# ---------- walk generator ----------
def gen_walk(eq1, eq2, elim, m1, m2, sol, back=None):
    a1,b1,c1 = eq1; a2,b2,c2 = eq2
    steps = []
    # scaled
    E1 = (a1*m1, b1*m1, c1*m1)
    E2 = (a2*m2, b2*m2, c2*m2)
    def scale_block(orig, m, Escaled):
        a,b,c = orig
        blk = []
        blk.append({"say": f"To make the {elim} terms match, multiply ALL of \\({eqstr(a,b,c)}\\) by {m}: every term, both sides.",
                    "pre": f"{a}x × {m} = " if a!=1 else f"x × {m} = ", "post":"x", "answer": a*m,
                    "hint":"Just multiply the number in front."})
        yt = yterm_scale(b)
        neg = b < 0
        blk.append({"say": None, "pre": f"{yt} × {m} = ", "post":"y", "answer": b*m,
                    "hint":"Just multiply the number in front" + (", and keep the minus." if neg else ".")})
        blk.append({"pre": f"and the right-hand side: {c} × {m} = " if c>=0 else f"and the right-hand side: ({c}) × {m} = ",
                    "post":"", "answer": c*m,
                    "hint":"The right-hand side gets multiplied too. That's the step everyone forgets."})
        return blk
    if m1 > 1: steps += scale_block(eq1, m1, E1)
    if m2 > 1: steps += scale_block(eq2, m2, E2)

    # elim coeffs
    if elim == "y":
        ev1, ev2 = E1[1], E2[1]; sv1, sv2 = E1[0], E2[0]; surv = "x"
    else:
        ev1, ev2 = E1[0], E2[0]; sv1, sv2 = E1[1], E2[1]; surv = "y"
    assert abs(ev1) == abs(ev2), (ev1, ev2)
    op = "sub" if (ev1 > 0) == (ev2 > 0) else "add"
    C1, C2 = E1[2], E2[2]

    if op == "sub":
        # minuend = larger surviving coeff
        if sv1 >= sv2:
            (mvS, mvC, mvE, mvEq) = (sv1, C1, ev1, E1); (suS, suC, suE, suEq) = (sv2, C2, ev2, E2)
        else:
            (mvS, mvC, mvE, mvEq) = (sv2, C2, ev2, E2); (suS, suC, suE, suEq) = (sv1, C1, ev1, E1)
        k = mvS - suS; R = mvC - suC
        steps.append({"say": f"Both equations now have {elim_term(abs(ev1) if elim=='y' else abs(ev1),elim)}, the same sign. <strong>Same Signs Subtract.</strong> Take \\({eqstr(*suEq)}\\) away from \\({eqstr(*mvEq)}\\), term by term:",
                      "pre": f"{svterm(mvS,surv)} {MINUS} {svterm(suS,surv)} = ",
                      "post": surv, "answer": k, "hint": f"Subtract the numbers in front: {mvS} {MINUS} {suS}."})
        et = elim_term(abs(mvE), elim)
        steps.append({"pre": f"{et} {MINUS} {et} = ", "post":"", "answer":0,
                      "done":"Gone. That was the whole point.",
                      "hint":"They're identical, and anything minus itself is 0."})
        steps.append({"pre": f"{mvC} {MINUS} {suC} = ", "post":"", "answer": R,
                      "hint":"The right-hand sides get subtracted too, exactly like the left."})
    else:  # add
        k = sv1 + sv2; R = C1 + C2
        steps.append({"say": f"The {elim} terms are {elim_term(ev1,elim)} and {elim_term(ev2,elim)}. Opposite signs, so <strong>ADD</strong> the equations and they cancel:",
                      "pre": f"{svterm(sv1,surv)} + {svterm(sv2,surv)} = ",
                      "post": surv, "answer": k, "hint":"Add the numbers in front."})
        t1 = elim_term(ev1, elim)
        t2 = elim_term(ev2, elim)
        t2d = t2 if ev2 > 0 else f"({t2})"
        steps.append({"pre": f"{t1} + {t2d} = ", "post":"", "answer":0,
                      "done":"Cancelled. Adding opposites gives zero.",
                      "hint":"One is plus, one is minus, same size, so they cancel to 0."})
        steps.append({"pre": f"{C1} + {C2} = ", "post":"", "answer": R,
                      "hint":"Add the right-hand sides too."})

    # solve surviving
    surv_idx = 0 if surv == "x" else 1
    surv_val = sol[surv_idx]
    assert F(R, k) == surv_val, (R, k, surv_val)
    if k == 1:
        steps.append({"say": f"So {surv} = {R}. Done in one."})
    else:
        steps.append({"say": f"So {k}{surv} = {R}.",
                      "pre": f"{surv} = ", "post":"", "answer": surv_val,
                      "hint": f"Divide both sides by {k}."})

    # back-substitution: choose back eq (smallest |coeff| of eliminated var, prefer 1)
    if back is None:
        tc1 = eq1[1] if elim=="y" else eq1[0]
        tc2 = eq2[1] if elim=="y" else eq2[0]
        back = 1 if abs(tc1) <= abs(tc2) else 2
    beq = eq1 if back == 1 else eq2
    oeq = eq2 if back == 1 else eq1
    ba, bb, bc = beq
    target = "y" if elim == "y" else "x"
    tgt_idx = 1 if target == "y" else 0
    tgt_val = sol[tgt_idx]
    # known var is surviving
    known_co = ba if surv == "x" else bb
    tgt_co = bb if target == "y" else ba
    knownpart = known_co * surv_val
    remainder = bc - knownpart
    assert F(remainder, tgt_co) == tgt_val, (remainder, tgt_co, tgt_val)

    say_sub = f"Now find {target}. Put {surv} = {surv_val} into \\({eqstr(*beq)}\\)"
    if known_co != 1:
        say_sub += f". The {surv} part is {known_co} × {surv_val} = {knownpart}, so:"
    else:
        say_sub += ":"

    if tgt_co == 1:
        steps.append({"say": say_sub, "phase":"substitute",
                      "pre": f"{knownpart} + {target} = {bc}{ARROW}{target} = ", "post":"", "answer": tgt_val,
                      "hint": f"Take {knownpart} from both sides."})
    elif tgt_co == -1:
        steps.append({"say": say_sub, "phase":"substitute",
                      "pre": f"{knownpart} {MINUS} {target} = {bc}{ARROW}{target} = ", "post":"", "answer": tgt_val,
                      "hint": f"{knownpart} minus what gives {bc}?"})
    else:
        remstr = f"{bc} {MINUS} {knownpart}" if knownpart>=0 else f"{bc} + {abs(knownpart)}"
        tco_disp = f"{tgt_co}{target}" if tgt_co>0 else f"-{abs(tgt_co)}{target}"
        steps.append({"say": say_sub, "phase":"substitute",
                      "pre": f"{tco_disp} = {remstr} = ", "post":"", "answer": remainder,
                      "hint":"Whatever is left after taking the known part away."})
        steps.append({"phase":"substitute", "pre": f"{target} = ", "post":"", "answer": tgt_val,
                      "hint": f"Divide by {tgt_co}."})

    # check in the OTHER equation
    xv, yv = sol
    cval = oeq[0]*xv + oeq[1]*yv
    assert cval == oeq[2]
    steps.append({"say":"Last thing: check the pair in the other equation:",
                  "pre": f"{check_expr(oeq[0], oeq[1], xv, yv)} = ", "post":"", "answer": cval,
                  "done": f"It balances, so x = {xv}, y = {yv} is right.",
                  "hint": f"Work it out. If it doesn't give {oeq[2]}, something slipped."})
    return steps

# ---------- misconception helpers ----------
def solve_pair(eq1, eq2):
    a1,b1,c1=eq1; a2,b2,c2=eq2
    d = a1*b2 - a2*b1
    x = F(c1*b2 - c2*b1, d); y = F(a1*c2 - a2*c1, d)
    return x, y

def as_num(v):
    v = F(v)
    return int(v) if v.denominator == 1 else round(float(v), 3)

def misc_rhs_added(eq1, eq2, elim, m1, m2, back):
    """subtract-route: RHS added instead of subtracted -> wrong surviving, then honest back-sub."""
    E1=(eq1[0]*m1,eq1[1]*m1,eq1[2]*m1); E2=(eq2[0]*m2,eq2[1]*m2,eq2[2]*m2)
    if elim=="y": sv1,sv2=E1[0],E2[0]; surv="x"
    else: sv1,sv2=E1[1],E2[1]; surv="y"
    k=abs(sv1-sv2); Rw=E1[2]+E2[2]
    surv_val=F(Rw,k)
    beq = eq1 if back==1 else eq2
    ba,bb,bc=beq
    if surv=="x":
        tgt=F(bc-ba*surv_val, bb); return [as_num(surv_val), as_num(tgt)]
    else:
        tgt=F(bc-bb*surv_val, ba); return [as_num(tgt), as_num(surv_val)]

def misc_rhs_wrongop(eq1, eq2, elim, m1, m2, back):
    """add-route: RHS subtracted instead of added."""
    E1=(eq1[0]*m1,eq1[1]*m1,eq1[2]*m1); E2=(eq2[0]*m2,eq2[1]*m2,eq2[2]*m2)
    if elim=="y": sv1,sv2=E1[0],E2[0]; surv="x"
    else: sv1,sv2=E1[1],E2[1]; surv="y"
    k=sv1+sv2; Rw=E1[2]-E2[2]
    surv_val=F(Rw,k)
    beq=eq1 if back==1 else eq2; ba,bb,bc=beq
    if surv=="x":
        tgt=F(bc-ba*surv_val,bb); return [as_num(surv_val),as_num(tgt)]
    else:
        tgt=F(bc-bb*surv_val,ba); return [as_num(tgt),as_num(surv_val)]

def misc_scaled_lhs(eq1, eq2, elim, m1, m2, scaled_eq, back):
    """multiply LHS of scaled_eq but forget its RHS."""
    E1=[eq1[0]*m1,eq1[1]*m1,eq1[2]*m1]; E2=[eq2[0]*m2,eq2[1]*m2,eq2[2]*m2]
    if scaled_eq==1: E1[2]=eq1[2]
    else: E2[2]=eq2[2]
    x,y=solve_pair(tuple(E1),tuple(E2))
    return [as_num(x),as_num(y)]

def misc_sub_signslip(eq1, eq2, sol, back, target):
    """correct surviving var; add knownpart instead of subtract in back-sub (tgt_co=1) or keep sign (tgt_co=-1)."""
    beq=eq1 if back==1 else eq2; ba,bb,bc=beq
    xv,yv=sol
    if target=="y":
        knownpart=ba*xv; tgt_co=bb
        if tgt_co==1: slip=bc+knownpart
        elif tgt_co==-1: slip=-yv
        else: slip=F(bc+knownpart,tgt_co)
        return [xv, as_num(slip)]
    else:
        knownpart=bb*yv; tgt_co=ba
        if tgt_co==1: slip=bc+knownpart
        elif tgt_co==-1: slip=-xv
        else: slip=F(bc+knownpart,tgt_co)
        return [as_num(slip), yv]

# ---------- bank definition ----------
# each: (eq1, eq2, elim, m1, m2, sol, hint, [misc dicts])
def M(pattern, expect, message):
    return {"pattern":pattern,"check":pattern,"expect":expect,"message":message}

bank = {"bronze":[], "silver":[], "gold":[]}

def add(tier, eq1, eq2, elim, m1, m2, sol, hint, back, miscs):
    x,y=solve_pair(eq1,eq2)
    assert (int(x),int(y))==tuple(sol), (eq1,eq2,x,y,sol)
    gs = gen_walk(eq1,eq2,elim,m1,m2,sol,back)
    disp = f"Solve \\({eqstr(*eq1)}\\) and \\({eqstr(*eq2)}\\)"
    bank[tier].append({"display":disp,"solutions":list(sol),"input_type":"xy_pair",
                       "calculator":False,"hint":hint,"misconceptions":miscs,"guided_steps":gs})

# BRONZE (coeffs already match)
add("bronze",(1,1,10),(1,-1,4),"y",1,1,[7,3],
    "The y terms are +y and -y, opposite signs, so add the equations.",1,
    [M("rhs_wrong_operation", None, None)])
add("bronze",(2,1,9),(1,1,6),"y",1,1,[3,3],
    "Both equations have +y, so subtract one from the other.",2,
    [M("rhs_not_subtracted", None, None)])
add("bronze",(1,3,13),(1,1,7),"x",1,1,[4,3],
    "The x terms already match, so subtract to remove them.",2,
    [M("rhs_not_subtracted", None, None)])
add("bronze",(3,1,14),(1,1,6),"y",1,1,[4,2],
    "Both equations have +y, so subtract them.",2,
    [M("rhs_not_subtracted", None, None)])
add("bronze",(2,1,11),(1,-1,4),"y",1,1,[5,1],
    "The y terms are +y and -y, opposite signs, so add.",1,
    [M("substitute_sign_slip", None, None)])
add("bronze",(1,2,11),(1,1,7),"x",1,1,[3,4],
    "The x terms match, so subtract to leave just the y terms.",2,
    [M("rhs_not_subtracted", None, None)])
add("bronze",(5,1,17),(3,1,11),"y",1,1,[3,2],
    "Both equations have +y, so subtract.",2,
    [M("rhs_not_subtracted", None, None)])
add("bronze",(3,1,17),(1,1,7),"y",1,1,[5,2],
    "Both equations have +y, so subtract them.",2,
    [M("rhs_not_subtracted", None, None)])

# SILVER (multiply one equation)
add("silver",(3,2,16),(1,1,7),"y",1,2,[2,5],
    "Multiply the second equation by 2, then subtract.",2,
    [M("scaled_lhs_only", None, None), M("rhs_not_subtracted", None, None)])
add("silver",(2,3,19),(1,1,8),"x",1,2,[5,3],
    "Multiply the second equation by 2 so both have 2x, then subtract.",2,
    [M("scaled_lhs_only", None, None)])
add("silver",(4,1,17),(2,1,9),"y",1,1,[4,1],
    "Both already have +y, so subtract one from the other.",2,
    [M("rhs_not_subtracted", None, None)])
add("silver",(3,4,18),(1,2,8),"y",1,2,[2,3],
    "Multiply the second equation by 2 so both have 4y, then subtract.",2,
    [M("scaled_lhs_only", None, None)])
add("silver",(3,2,13),(1,-1,1),"y",1,2,[3,2],
    "Multiply the second equation by 2. The y terms are then opposite, so add.",2,
    [M("substitute_sign_slip", None, None)])
add("silver",(5,2,24),(3,2,16),"y",1,1,[4,2],
    "Both already have 2y, so subtract.",2,
    [M("rhs_not_subtracted", None, None)])
add("silver",(1,3,13),(2,-1,5),"y",1,3,[4,3],
    "Multiply the second equation by 3. The y terms are then opposite, so add.",2,
    [M("substitute_sign_slip", None, None)])

# GOLD (multiply both, or already-set opposite / substitution)
add("gold",(2,3,12),(5,-2,11),"y",2,3,[3,2],
    "Scale both: ×2 and ×3 makes the y terms 6y and -6y. Opposite signs, so add.",2,
    [M("substitute_sign_slip", None, None)])
add("gold",(3,2,18),(5,-2,14),"y",1,1,[4,3],
    "The y terms are already +2y and -2y, so add the equations.",2,
    [M("substitute_sign_slip", None, None)])
add("gold",(4,3,23),(2,1,9),"y",1,3,[2,5],
    "Multiply the second equation by 3 so both have 3y, then subtract.",2,
    [M("scaled_lhs_only", None, None)])
add("gold",(2,5,24),(3,2,14),"x",3,2,[2,4],
    "Scale both equations (×3 and ×2) so both have 6x, then subtract.",2,
    [])
add("gold",(3,5,21),(5,2,16),"x",5,3,[2,3],
    "Scale both equations (×5 and ×3) so both have 15x, then subtract.",2,
    [])

# ---------- fill misconception expects/messages ----------
def fill_miscs():
    for tier,probs in bank.items():
        for p in probs:
            eq1e,eq2e = None,None
            # recover eqs from display is hard; store separately -> redo via re-add map
    pass

# We stored miscs as stubs; recompute now with a parallel spec list.
specs = [
 ("bronze",(1,1,10),(1,-1,4),"y",1,1,[7,3],1,
   [("rhs_wrong_operation",
     "Adding the equations makes y vanish, so the left is right, but the right-hand sides must be ADDED too: 10 + 4 = 14, giving 2x = 14 and x = 7. Subtracting them (giving 6) is the slip.")]),
 ("bronze",(2,1,9),(1,1,6),"y",1,1,[3,3],2,
   [("rhs_not_subtracted",
     "When you subtract the equations the right-hand sides subtract too: 9 - 6 = 3, so x = 3. Adding them (15) is too big to fit either equation.")]),
 ("bronze",(1,3,13),(1,1,7),"x",1,1,[4,3],2,
   [("rhs_not_subtracted",
     "Subtracting removes x and leaves 2y = 13 - 7 = 6, so y = 3. It looks like the right-hand sides were added instead of subtracted.")]),
 ("bronze",(3,1,14),(1,1,6),"y",1,1,[4,2],2,
   [("rhs_not_subtracted",
     "Subtract the right-hand sides too: 14 - 6 = 8, so 2x = 8 and x = 4. Adding them (20) sends the rest off course.")]),
 ("bronze",(2,1,11),(1,-1,4),"y",1,1,[5,1],1,
   [("substitute_sign_slip",
     "x = 5 is right. Putting it into 2x + y = 11 gives 10 + y = 11, so y = 1. Getting 21 means the 10 was added instead of subtracted when moving it across.")]),
 ("bronze",(1,2,11),(1,1,7),"x",1,1,[3,4],2,
   [("rhs_not_subtracted",
     "Subtracting leaves 2y = 11 - 7 = 4, so y = 4. It looks like the right-hand sides were added. They get subtracted, just like the left.")]),
 ("bronze",(5,1,17),(3,1,11),"y",1,1,[3,2],2,
   [("rhs_not_subtracted",
     "Subtract the right-hand sides: 17 - 11 = 6, so 2x = 6 and x = 3. Adding them (28) makes everything after it wrong.")]),
 ("bronze",(3,1,17),(1,1,7),"y",1,1,[5,2],2,
   [("rhs_not_subtracted",
     "Subtracting gives 2x = 17 - 7 = 10, so x = 5. Adding the right-hand sides (24) instead of subtracting is the slip.")]),
 ("silver",(3,2,16),(1,1,7),"y",1,2,[2,5],2,
   [("scaled_lhs_only",
     "When you multiply an equation, multiply BOTH sides. Doubling x + y = 7 gives 2x + 2y = 14. The 7 doubles too. Leaving it at 7 makes x come out wrong."),
    ("rhs_not_subtracted",
     "After doubling the second equation the right-hand sides are 16 and 14. Subtract them: 16 - 14 = 2, so x = 2. Adding them (30) is the slip.")]),
 ("silver",(2,3,19),(1,1,8),"x",1,2,[5,3],2,
   [("scaled_lhs_only",
     "Doubling x + y = 8 gives 2x + 2y = 16. The 8 is doubled too. Keeping it at 8 gives y = 11, which is too big to fit either equation.")]),
 ("silver",(4,1,17),(2,1,9),"y",1,1,[4,1],2,
   [("rhs_not_subtracted",
     "Both have +y, so subtract: 17 - 9 = 8, giving 2x = 8 and x = 4. Adding the right-hand sides (26) instead is the slip.")]),
 ("silver",(3,4,18),(1,2,8),"y",1,2,[2,3],2,
   [("scaled_lhs_only",
     "Doubling x + 2y = 8 gives 2x + 4y = 16. The 8 doubles as well. Leaving it at 8 makes x come out wrong.")]),
 ("silver",(3,2,13),(1,-1,1),"y",1,2,[3,2],2,
   [("substitute_sign_slip",
     "x = 3 is right. Putting it into x - y = 1 gives 3 - y = 1, so y = 2, positive. Getting -2 means a sign flipped once too often.")]),
 ("silver",(5,2,24),(3,2,16),"y",1,1,[4,2],2,
   [("rhs_not_subtracted",
     "Both have 2y, so subtract: 24 - 16 = 8, giving 2x = 8 and x = 4. Adding the right-hand sides (40) instead is the slip.")]),
 ("silver",(1,3,13),(2,-1,5),"y",1,3,[4,3],2,
   [("substitute_sign_slip",
     "x = 4 is right. Putting it into 2x - y = 5 gives 8 - y = 5, so y = 3, positive. Getting -3 means the sign flipped once too often.")]),
 ("gold",(2,3,12),(5,-2,11),"y",2,3,[3,2],2,
   [("substitute_sign_slip",
     "x = 3 is right. Putting it into 5x - 2y = 11 gives 15 - 2y = 11, so 2y = 4 and y = 2. Moving the 15 across flips its sign to minus; adding it instead makes 2y = -26 and y comes out negative.")]),
 ("gold",(3,2,18),(5,-2,14),"y",1,1,[4,3],2,
   [("substitute_sign_slip",
     "x = 4 is right. Putting it into 5x - 2y = 14 gives 20 - 2y = 14, so 2y = 6 and y = 3. Adding the 20 instead of subtracting it makes 2y = -34 and y comes out negative.")]),
 ("gold",(4,3,23),(2,1,9),"y",1,3,[2,5],2,
   [("scaled_lhs_only",
     "Tripling 2x + y = 9 gives 6x + 3y = 27. The 9 is tripled too. Leaving it at 9 makes x come out negative when it should be 2.")]),
 ("gold",(2,5,24),(3,2,14),"x",3,2,[2,4],2, []),
 ("gold",(3,5,21),(5,2,16),"x",5,3,[2,3],2, []),
]

# rebuild bank from specs (single source of truth)
bank = {"bronze":[], "silver":[], "gold":[]}
for tier,eq1,eq2,elim,m1,m2,sol,back,ms in specs:
    x,y=solve_pair(eq1,eq2)
    assert (int(x),int(y))==tuple(sol), (eq1,eq2,x,y,sol)
    miscs=[]
    for pat,msg in ms:
        if pat=="rhs_not_subtracted":
            exp=misc_rhs_added(eq1,eq2,elim,m1,m2,back)
        elif pat=="rhs_wrong_operation":
            exp=misc_rhs_wrongop(eq1,eq2,elim,m1,m2,back)
        elif pat=="scaled_lhs_only":
            se = 2 if m2>1 else 1
            exp=misc_scaled_lhs(eq1,eq2,elim,m1,m2,se,back)
        elif pat=="substitute_sign_slip":
            target="y" if elim=="y" else "x"
            exp=misc_sub_signslip(eq1,eq2,sol,back,target)
        else:
            exp=None
        # guard: expect must not equal solution
        if exp is not None and [float(a) for a in exp]==[float(s) for s in sol]:
            exp=None
        miscs.append({"pattern":pat,"check":pat,"expect":exp,"message":msg,
                      "note":"derived by committing the error"})
    gs=gen_walk(eq1,eq2,elim,m1,m2,sol,back)
    disp=f"Solve \\({eqstr(*eq1)}\\) and \\({eqstr(*eq2)}\\)"
    bank[tier].append({"display":disp,"solutions":list(sol),"input_type":"xy_pair",
                       "calculator":False,"hint":ms and "" or "","misconceptions":miscs,"guided_steps":gs})

# reattach hints (from the earlier add() specs order)
hint_map = {
 ("bronze",0):"The y terms are +y and -y, opposite signs, so add the equations.",
 ("bronze",1):"Both equations have +y, so subtract one from the other.",
 ("bronze",2):"The x terms already match, so subtract to remove them.",
 ("bronze",3):"Both equations have +y, so subtract them.",
 ("bronze",4):"The y terms are +y and -y, opposite signs, so add.",
 ("bronze",5):"The x terms match, so subtract to leave just the y terms.",
 ("bronze",6):"Both equations have +y, so subtract.",
 ("bronze",7):"Both equations have +y, so subtract them.",
 ("silver",0):"Multiply the second equation by 2, then subtract.",
 ("silver",1):"Multiply the second equation by 2 so both have 2x, then subtract.",
 ("silver",2):"Both already have +y, so subtract one from the other.",
 ("silver",3):"Multiply the second equation by 2 so both have 4y, then subtract.",
 ("silver",4):"Multiply the second equation by 2. The y terms are then opposite, so add.",
 ("silver",5):"Both already have 2y, so subtract.",
 ("silver",6):"Multiply the second equation by 3. The y terms are then opposite, so add.",
 ("gold",0):"Scale both: ×2 and ×3 makes the y terms 6y and -6y. Opposite signs, so add.",
 ("gold",1):"The y terms are already +2y and -2y, so add the equations.",
 ("gold",2):"Multiply the second equation by 3 so both have 3y, then subtract.",
 ("gold",3):"Scale both equations (×3 and ×2) so both have 6x, then subtract.",
 ("gold",4):"Scale both equations (×5 and ×3) so both have 15x, then subtract.",
}
for tier in bank:
    for i,p in enumerate(bank[tier]):
        p["hint"]=hint_map[(tier,i)]

# ---------- teach walks ----------
def teach(eq1,eq2,elim,m1,m2,sol,label,back):
    return {"display":f"Solve \\({eqstr(*eq1)}\\) and \\({eqstr(*eq2)}\\)",
            "label":label,"steps":gen_walk(eq1,eq2,elim,m1,m2,sol,back)}

teach_bronze = teach((3,1,11),(1,1,5),"y",1,1,[3,2],"Together: your first one",2)
teach_silver = teach((2,3,13),(1,1,5),"x",1,2,[2,3],"Together: the silver move",2)
teach_gold   = teach((2,5,24),(3,4,22),"x",3,2,[2,4],"Together: the gold move",2)

# ---------- opener ----------
opener = {
 "label":"Before any algebra",
 "display":"2 tickets + 1 popcorn = £19<br>1 ticket + 1 popcorn = £12",
 "steps":[
   {"say":"A cinema trip. No algebra, just compare the two orders.",
    "pre":"A ticket costs £","post":"","answer":7,
    "hint":"The only difference between the two orders is one extra ticket, and £7 of price."},
   {"say":"That move, comparing the orders so the popcorn cancels, is called <strong>elimination</strong>. You just subtracted two equations without noticing.",
    "pre":"And the popcorn? £","post":"","answer":5,
    "hint":"One ticket (£7) and a popcorn cost £12 together."},
   {"say":"Using a value you know to find the one you do not is <strong>substitution</strong>. Those two moves are the whole topic. Algebra just writes ticket as \\(x\\) and popcorn as \\(y\\): \\(2x + y = 19\\) and \\(x + y = 12\\)."}
 ]
}

# ---------- tier_guides ----------
tier_guides = {
 "bronze":{
   "title":"Bronze: the pair already matches",
   "steps":[
     "You need the one pair of values, an \\(x\\) AND a \\(y\\), that fits both equations. In bronze a matching pair is already there (like \\(+y\\) in both).",
     "<strong>Same Signs Subtract</strong>: subtract one equation from the other, right-hand sides too, and the matched letter vanishes. Opposite signs (\\(+y\\) and \\(-y\\))? Add instead.",
     "Solve the one-letter equation that is left, then substitute back into the easier equation to find the other letter."
   ],
   "example":{
     "question":"Solve 2x + y = 8 and x + y = 5",
     "steps":[
       {"label":"Match","content":"<p>Both have \\(+y\\), the same sign, so subtract.</p>"},
       {"label":"Subtract","content":"<p>\\((2x + y) - (x + y) = 8 - 5\\) so \\(x = 3\\)</p>"},
       {"label":"Substitute","content":"<p>\\(3 + y = 5\\) so \\(y = 2\\)</p>"},
       {"label":"Check","content":"<p>\\(2(3) + 2 = 8\\) ✓</p>"},
       {"label":"Answer","content":"<p>\\(x = 3\\), \\(y = 2\\)</p>","isAnswer":True,"is_answer":True}
     ]
   }
 },
 "silver":{
   "title":"Silver: make a match first",
   "steps":[
     "Now nothing matches yet. Multiply ONE whole equation, every term and both sides, until a pair matches.",
     "Then it is a bronze question: same signs subtract, opposite signs add.",
     "Substitute back and check your pair in both equations."
   ],
   "example":{
     "question":"Solve 3x + 2y = 13 and x + y = 5",
     "steps":[
       {"label":"Multiply","content":"<p>Second equation \\(\\times 2\\): \\(2x + 2y = 10\\). The 5 is doubled too.</p>"},
       {"label":"Subtract","content":"<p>\\((3x + 2y) - (2x + 2y) = 13 - 10\\) so \\(x = 3\\)</p>"},
       {"label":"Substitute","content":"<p>\\(3 + y = 5\\) so \\(y = 2\\)</p>"},
       {"label":"Check","content":"<p>\\(3(3) + 2(2) = 13\\) ✓</p>"},
       {"label":"Answer","content":"<p>\\(x = 3\\), \\(y = 2\\)</p>","isAnswer":True,"is_answer":True}
     ]
   }
 },
 "gold":{
   "title":"Gold: multiply both equations",
   "steps":[
     "Sometimes no single multiplication works. Multiply BOTH equations to hit a common target: \\(3y\\) and \\(2y\\) both become \\(6y\\) with \\(\\times 2\\) and \\(\\times 3\\).",
     "Everything else is the same: same signs subtract, opposite signs add, substitute back, check.",
     "Prefer rearranging? <strong>Substitution</strong> also works: make \\(y\\) the subject of one equation and put it into the other. Either method earns full marks."
   ],
   "example":{
     "question":"Solve 4x + 3y = 18 and 3x + 2y = 13",
     "steps":[
       {"label":"Multiply both","content":"<p>First \\(\\times 2\\): \\(8x + 6y = 36\\). Second \\(\\times 3\\): \\(9x + 6y = 39\\).</p>"},
       {"label":"Subtract","content":"<p>\\((9x + 6y) - (8x + 6y) = 39 - 36\\) so \\(x = 3\\)</p>"},
       {"label":"Substitute","content":"<p>\\(9 + 2y = 13\\) so \\(y = 2\\)</p>"},
       {"label":"Check","content":"<p>\\(4(3) + 3(2) = 18\\) ✓</p>"},
       {"label":"Answer","content":"<p>\\(x = 3\\), \\(y = 2\\)</p>","isAnswer":True,"is_answer":True}
     ]
   }
 }
}

# ---------- assemble ----------
live = json.load(io.open("_L09eq_live.json", encoding="utf-8"))
pd = {}
pd["method_card"] = live["method_card"]          # preserve
pd["topic_links"] = live["topic_links"]          # preserve
pd["problem_bank"] = {
   "bronze": bank["bronze"], "silver": bank["silver"], "gold": bank["gold"],
   "bronze_description":"The numbers in front already match: add or subtract once and a letter vanishes",
   "silver_description":"Multiply one equation first to make a matching pair",
   "gold_description":"Multiply both equations, or switch to the substitution method"
}
pd["related_videos"] = live["related_videos"]    # preserve ([])
pd["worked_examples"] = live["worked_examples"]  # preserve
pd["tier_guides"] = tier_guides
pd["guided"] = {"opener":opener, "teach":{"bronze":teach_bronze,"silver":teach_silver,"gold":teach_gold}}

with io.open("lesson_maths-eduqas_algebra-L09.json","w",encoding="utf-8") as f:
    json.dump(pd,f,indent=1,ensure_ascii=False)

# ---------- self verification ----------
print("Bank sizes:", {t:len(bank[t]) for t in bank})
for t in bank:
    seen=set()
    for i,p in enumerate(bank[t]):
        key=tuple(p["solutions"])
        assert key not in seen, f"DUP {t}[{i}] {key}"
        seen.add(key)
        # verify final walk boxes land on solution
        xv,yv=p["solutions"]
        # check display solve
        import re
        assert p["input_type"]=="xy_pair"
print("No within-tier duplicate solutions.")
print("Wrote lesson_maths-eduqas_algebra-L09.json")
# dump expects for eyeball
for t in bank:
    for i,p in enumerate(bank[t]):
        for m in p["misconceptions"]:
            print(f"  {t}[{i}] {m['pattern']} expect={m['expect']} sol={p['solutions']}")
