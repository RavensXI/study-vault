# -*- coding: utf-8 -*-
import json, io

MINUS = "−"  # unicode minus for plain text
TIMES = "×"

def num(v):
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return v

def s(v):
    """plain-text number: use unicode minus, drop trailing .0"""
    v = num(v)
    txt = str(v)
    if isinstance(v, (int, float)) and v < 0:
        txt = MINUS + str(abs(v))
    return txt

def latexnum(v):
    v = num(v)
    return str(v)  # inside \(...\) ASCII hyphen renders as minus

def coefterm(coef, letter):
    """Plain-text coefficient+letter, dropping 1: y, -y, 2y, -3y."""
    coef = num(coef)
    if coef == 1:
        return letter
    if coef == -1:
        return MINUS + letter
    return "%s%s" % (s(coef), letter)

def eqstr(A, B, C):
    """LaTeX equation string A x + B y = C, explicit coefficients."""
    A = num(A); B = num(B); C = num(C)
    xt = "%sx" % A
    if B >= 0:
        yt = " + %sy" % B
    else:
        yt = " - %sy" % abs(B)
    return "%s%s = %s" % (xt, yt, C)

STEPS = []  # collected error log for asserts

def build_elim_walk(plan):
    """Generate guided_steps for a standard elimination problem and assert arithmetic."""
    (a0, b0, c0) = plan["e0"]
    (a1, b1, c1) = plan["e1"]
    elim = plan["elim"]
    kept = "x" if elim == "y" else "y"
    k0 = plan.get("k0", 1)
    k1 = plan.get("k1", 1)
    sub_into = plan["sub_into"]
    sols = plan["sols"]
    steps = []

    if plan.get("intro_say"):
        steps.append({"say": plan["intro_say"]})

    # coefficient helpers
    def coef(eq, letter):
        return eq[0] if letter == "x" else eq[1]

    e0 = (a0, b0, c0)
    e1 = (a1, b1, c1)

    # ---- scaling blocks ----
    def scale_block(eq, k, which):
        A, B, C = eq
        letterlabel = "the %s terms" % elim
        sy = "To make %s match, multiply ALL of \\(%s\\) by %d: every term, both sides." % (
            letterlabel, eqstr(A, B, C), k)
        blk = []
        # x term
        blk.append({"say": sy, "pre": "%s %s %d = " % (coefterm(A, "x"), TIMES, k), "post": "x",
                    "answer": num(A * k),
                    "hint": "Just multiply the number in front." + ("" if A >= 0 else " Keep the minus.")})
        blk.append({"say": None, "pre": "%s %s %d = " % (coefterm(B, "y"), TIMES, k), "post": "y",
                    "answer": num(B * k),
                    "hint": "Just multiply the number in front." + ("" if B >= 0 else " Keep the minus.")})
        blk.append({"pre": "and the right-hand side: %s %s %d = " % (s(C), TIMES, k), "post": "",
                    "answer": num(C * k),
                    "hint": "The right-hand side gets multiplied too. That's the step everyone forgets."})
        return blk

    if k0 > 1:
        steps += scale_block(e0, k0, 0)
    if k1 > 1:
        steps += scale_block(e1, k1, 1)

    # scaled equations
    se0 = (a0 * k0, b0 * k0, c0 * k0)
    se1 = (a1 * k1, b1 * k1, c1 * k1)

    ke0 = coef(se0, elim)
    ke1 = coef(se1, elim)
    kk0 = coef(se0, kept)
    kk1 = coef(se1, kept)
    assert abs(ke0) == abs(ke1), ("elim coeff mismatch", plan["disp"], ke0, ke1)

    same_sign = (ke0 * ke1) > 0

    if same_sign:
        # subtract: big - small on kept coeff to stay positive
        if kk0 >= kk1:
            big, small = se0, se1
        else:
            big, small = se1, se0
        kbig = coef(big, kept); ksmall = coef(small, kept)
        ke = abs(ke0)
        coef_diff = kbig - ksmall
        rhs_diff = big[2] - small[2]
        say = ("Both equations now have %s%s, the same sign. <strong>Same Signs Subtract.</strong> "
               "Take \\(%s\\) away from \\(%s\\), term by term:") % (
               s(ke), elim, eqstr(*small), eqstr(*big))
        steps.append({"say": say,
                      "pre": "%s %s %s = " % (coefterm(kbig, kept), MINUS, coefterm(ksmall, kept)), "post": kept,
                      "answer": num(coef_diff),
                      "hint": "Subtract the numbers in front: %s %s %s." % (s(kbig), MINUS, s(ksmall))})
        steps.append({"pre": "%s %s %s = " % (coefterm(ke, elim), MINUS, coefterm(ke, elim)), "post": "",
                      "answer": 0, "done": "Gone. That was the whole point.",
                      "hint": "They're identical, and anything minus itself is 0."})
        steps.append({"pre": "%s %s %s = " % (s(big[2]), MINUS, s(small[2])), "post": "",
                      "answer": num(rhs_diff),
                      "hint": "The right-hand sides get subtracted too, exactly like the left."})
        kept_coef = coef_diff
        kept_rhs = rhs_diff
    else:
        # add
        ksum = kk0 + kk1
        rhs_sum = se0[2] + se1[2]
        def plusterm(t2):
            return "(%s)" % t2 if t2.startswith(MINUS) else t2
        say = ("The %s terms are %s and %s. Opposite signs, so <strong>ADD</strong> the "
               "equations and they cancel:") % (elim, coefterm(ke0, elim), coefterm(ke1, elim))
        steps.append({"say": say,
                      "pre": "%s + %s = " % (coefterm(kk0, kept), plusterm(coefterm(kk1, kept))), "post": kept,
                      "answer": num(ksum),
                      "hint": "Add the numbers in front."})
        steps.append({"pre": "%s + %s = " % (coefterm(ke0, elim), plusterm(coefterm(ke1, elim))), "post": "",
                      "answer": 0, "done": "Cancelled. Adding opposites gives zero.",
                      "hint": "One is plus, one is minus, same size, so they cancel to 0."})
        steps.append({"pre": "%s + %s = " % (s(se0[2]), s(se1[2])), "post": "",
                      "answer": num(rhs_sum),
                      "hint": "Add the right-hand sides too."})
        kept_coef = ksum
        kept_rhs = rhs_sum

    kept_val = kept_rhs / kept_coef
    kept_val = num(kept_val)
    # verify kept value matches solution
    exp_kept = sols[0] if kept == "x" else sols[1]
    assert abs(kept_val - exp_kept) < 1e-9, ("kept mismatch", plan["disp"], kept_val, exp_kept)

    if kept_coef == 1:
        steps.append({"say": "So %s = %s. Done in one." % (kept, s(kept_val))})
    else:
        steps.append({"say": "So %s%s = %s." % (s(kept_coef), kept, s(kept_rhs)),
                      "pre": "%s = " % kept, "post": "",
                      "answer": kept_val,
                      "hint": "Divide both sides by %s." % s(kept_coef)})

    # ---- substitution phase ----
    sub_eq = e0 if sub_into == 0 else e1
    A, B, C = sub_eq
    coef_kept = A if kept == "x" else B
    coef_elim = A if elim == "x" else B
    known = coef_kept * kept_val
    known = num(known)
    rem = C - known
    elim_val = rem / coef_elim
    elim_val = num(elim_val)
    exp_elim = sols[0] if elim == "x" else sols[1]
    assert abs(elim_val - exp_elim) < 1e-9, ("elim val mismatch", plan["disp"], elim_val, exp_elim)

    sub_say = "Now find %s. Put %s = %s into \\(%s\\).%s" % (
        elim, kept, s(kept_val), eqstr(A, B, C),
        (" The %s part is %s %s %s = %s, so:" % (kept, s(coef_kept), TIMES, s(kept_val), s(known)))
        if abs(coef_kept) != 1 else "")

    if abs(coef_elim) == 1:
        if coef_elim == 1:
            pre = "%s + %s = %s  %s  %s = " % (s(known), elim, s(C), "→", elim)
        else:  # -1
            pre = "%s %s %s = %s  %s  %s = " % (s(known), MINUS, elim, s(C), "→", elim)
        steps.append({"say": sub_say, "phase": "substitute", "pre": pre, "post": "",
                      "answer": elim_val,
                      "hint": "Rearrange for %s." % elim})
    else:
        # two boxes
        steps.append({"say": sub_say, "phase": "substitute",
                      "pre": "%s%s = %s %s %s = " % (s(coef_elim), elim, s(C), MINUS, s(known)),
                      "post": "", "answer": num(rem),
                      "hint": "Whatever is left after taking the known part away."})
        steps.append({"phase": "substitute", "pre": "%s = " % elim, "post": "",
                      "answer": elim_val,
                      "hint": "Divide by %s." % s(coef_elim)})

    # ---- check in the OTHER original equation ----
    other_eq = e1 if sub_into == 0 else e0
    A2, B2, C2 = other_eq
    xval = sols[0]; yval = sols[1]
    # build check expression "A2 * x  +/-  B2 * y ="
    def valpar(v):
        return "(%s)" % s(v) if num(v) < 0 else s(v)
    def mag(coefv, val):
        coefv = num(coefv)
        if abs(coefv) == 1:
            return valpar(val)
        return "%s %s %s" % (s(abs(coefv)), TIMES, valpar(val))
    # construct with signs between terms (drop unit coefficients)
    t1 = ("%s" % MINUS if A2 < 0 else "") + mag(A2, xval)
    t2 = (" + " if B2 >= 0 else " %s " % MINUS) + mag(B2, yval)
    check_val = A2 * xval + B2 * yval
    check_val = num(check_val)
    assert abs(check_val - C2) < 1e-9, ("check mismatch", plan["disp"], check_val, C2)
    steps.append({"say": "Last thing: check the pair in the other equation:",
                  "pre": "%s%s = " % (t1, t2), "post": "",
                  "answer": check_val,
                  "done": "It balances, so x = %s, y = %s is right." % (s(xval), s(yval)),
                  "hint": "Work it out. If it doesn't give %s, something slipped." % s(C2)})

    # verify at least one pre-phase step and >=2 live boxes at/after phase
    sub_idx = next((i for i, st in enumerate(steps) if st.get("phase") == "substitute"), None)
    assert sub_idx is not None and sub_idx >= 1
    live_after = sum(1 for st in steps[sub_idx:] if st.get("answer") is not None)
    assert live_after >= 2, ("live after", plan["disp"], live_after)
    return steps


# ============ PROBLEM PLANS ============
BRONZE = [
    dict(disp="Solve \\(x + y = 10\\) and \\(x - y = 4\\)", sols=[7, 3], calc=False,
         e0=(1, 1, 10), e1=(1, -1, 4), elim="y", sub_into=0,
         hint="The y terms are +y and -y, opposite signs, so add the equations.",
         misc=[dict(pattern="rhs_wrong_operation", expect=[3, 7],
                    message="Adding the equations means adding both right-hand sides: 10 + 4 = 14, so 2x = 14 and x = 7. Using 10 - 4 = 6 gives x = 3, which fits neither equation.")]),
    dict(disp="Solve \\(2x + y = 9\\) and \\(x + y = 5\\)", sols=[4, 1], calc=False,
         e0=(2, 1, 9), e1=(1, 1, 5), elim="y", sub_into=1,
         hint="Both equations have +y, the same sign, so subtract one from the other.",
         misc=[dict(pattern="rhs_not_subtracted", expect=[14, -9],
                    message="When you subtract the equations, the right-hand sides subtract too: 9 - 5 = 4, so x = 4. Adding them gives 14, which is too big to fit either equation.")]),
    dict(disp="Solve \\(x + 3y = 13\\) and \\(x + y = 7\\)", sols=[4, 3], calc=False,
         e0=(1, 3, 13), e1=(1, 1, 7), elim="x", sub_into=1,
         hint="The x terms already match, so subtract to leave only y terms.",
         misc=[dict(pattern="rhs_not_subtracted", expect=[-3, 10],
                    message="After subtracting, 2y = 13 - 7 = 6, so y = 3. It looks like the right-hand sides were added instead. Both sides get subtracted the same way.")]),
    dict(disp="Solve \\(3x + y = 14\\) and \\(x + y = 6\\)", sols=[4, 2], calc=False,
         e0=(3, 1, 14), e1=(1, 1, 6), elim="y", sub_into=1,
         hint="Both equations have +y, so subtract them to remove y.",
         misc=[dict(pattern="rhs_not_subtracted", expect=[10, -4],
                    message="Subtracting gives 2x = 14 - 6 = 8, so x = 4. Adding the right-hand sides (20) instead sends the whole answer off course.")]),
    dict(disp="Solve \\(2x + y = 11\\) and \\(x - y = 4\\)", sols=[5, 1], calc=False,
         e0=(2, 1, 11), e1=(1, -1, 4), elim="y", sub_into=1,
         hint="The y terms are +y and -y, opposite signs, so add the equations.",
         misc=[dict(pattern="substitute_sign_slip", expect=[5, -1],
                    message="x = 5 is right. Substituting into x - y = 4 gives 5 - y = 4, so y = 1, positive. Getting -1 means the subtraction was done the wrong way round.")]),
    dict(disp="Solve \\(3x + y = 17\\) and \\(x + y = 7\\)", sols=[5, 2], calc=False,
         e0=(3, 1, 17), e1=(1, 1, 7), elim="y", sub_into=1,
         hint="Both equations have +y, so subtract to eliminate y.",
         misc=[dict(pattern="rhs_not_subtracted", expect=[12, -5],
                    message="Subtract the right-hand sides too: 17 - 7 = 10, so 2x = 10 and x = 5. Adding them gives 24 and everything after that comes out wrong.")]),
    dict(disp="Solve \\(5x + y = 19\\) and \\(2x + y = 10\\)", sols=[3, 4], calc=False,
         e0=(5, 1, 19), e1=(2, 1, 10), elim="y", sub_into=1,
         hint="Same sign on y in both, so subtract.",
         misc=[dict(pattern="substitute_sign_slip", expect=[3, 16],
                    message="x = 3 is right. Substituting into 2x + y = 10 gives 6 + y = 10, so y = 4. Getting 16 means the 6 was added instead of subtracted when moving it across.")]),
    dict(disp="Solve \\(x + y = 9\\) and \\(2x - y = 0\\)", sols=[3, 6], calc=False,
         e0=(1, 1, 9), e1=(2, -1, 0), elim="y", sub_into=0,
         hint="The y terms are +y and -y, opposite signs, so add the equations.",
         misc=[dict(pattern="substitute_sign_slip", expect=[3, -6],
                    message="x = 3 is right. Substituting into 2x - y = 0 gives 6 - y = 0, so y = 6, positive. Getting -6 means a sign was flipped once too often.")]),
]

SILVER = [
    dict(disp="Solve \\(3x + 2y = 19\\) and \\(2x - y = 1\\)", sols=[3, 5], calc=False,
         e0=(3, 2, 19), e1=(2, -1, 1), elim="y", k1=2, sub_into=1,
         hint="Multiply the second equation by 2, then the y terms are opposite, so add.",
         misc=[dict(pattern="substitute_sign_slip", expect=[3, -5],
                    message="x = 3 is right. Substituting into 2x - y = 1 gives 6 - y = 1, so y = 5, positive. Getting -5 means the subtraction was reversed.")]),
    dict(disp="Solve \\(4x + 3y = 23\\) and \\(2x + y = 9\\)", sols=[2, 5], calc=False,
         e0=(4, 3, 23), e1=(2, 1, 9), elim="y", k1=3, sub_into=1,
         hint="Multiply the second equation by 3 so both have 3y, then subtract.",
         misc=[dict(pattern="scaled_lhs_only", expect=[-7, 23],
                    message="When you multiply an equation, multiply BOTH sides. Trebling 2x + y = 9 gives 6x + 3y = 27, and the 9 becomes 27. Leaving it at 9 makes x come out as -7, which fits neither equation.")]),
    dict(disp="Solve \\(2x + 3y = 13\\) and \\(x + 4y = 14\\)", sols=[2, 3], calc=False,
         e0=(2, 3, 13), e1=(1, 4, 14), elim="x", k1=2, sub_into=1,
         hint="Multiply the second equation by 2 so both have 2x, then subtract.",
         misc=[dict(pattern="substitute_sign_slip", expect=[11, 3],
                    message="y = 3 is right. Substituting into 2x + 3y = 13 gives 2x + 9 = 13, so 2x = 4 and x = 2. Getting 11 means the 9 was added instead of subtracted.")]),
    dict(disp="Solve \\(y = 3x - 1\\) and \\(2x + y = 14\\)", sols=[3, 8], calc=False,
         input_type="xy_pair", special="subst",
         hint="One equation already gives y. Substitute 3x - 1 in place of y in the other.",
         misc=[dict(pattern="substitute_sign_slip", expect=[3, 10],
                    message="x = 3 is right. Then y = 3x - 1 = 3(3) - 1 = 8. Getting 10 means the -1 was added instead of subtracted.")]),
    dict(disp="Solve \\(4x - y = 17\\) and \\(2x + 3y = 19\\)", sols=[5, 3], calc=False,
         e0=(4, -1, 17), e1=(2, 3, 19), elim="y", k0=3, sub_into=0,
         hint="Multiply the first equation by 3. The y terms are then opposite, so add.",
         misc=[dict(pattern="substitute_sign_slip", expect=[5, -3],
                    message="x = 5 is right. Substituting into 4x - y = 17 gives 20 - y = 17, so y = 3, positive. Getting -3 reverses the subtraction.")]),
]

GOLD = [
    dict(disp="A café sells coffee and tea. 3 coffees and 2 teas cost £11.50. 2 coffees and 3 teas cost £11.00. Taking \\(x\\) as the cost of a coffee and \\(y\\) as the cost of a tea (in £), find x and y.",
         sols=[2.5, 2], calc=True,
         e0=(3, 2, 11.5), e1=(2, 3, 11), elim="y", k0=3, k1=2, sub_into=1,
         intro_say="Write a coffee as \\(x\\) and a tea as \\(y\\): \\(3x + 2y = 11.5\\) and \\(2x + 3y = 11\\). Match the y terms.",
         hint="Let x be a coffee and y a tea. Scale both equations so the y terms both become 6y.",
         misc=[]),
    dict(disp="Solve \\(3x + 5y = 26\\) and \\(7x + 2y = 22\\)", sols=[2, 4], calc=False,
         e0=(3, 5, 26), e1=(7, 2, 22), elim="y", k0=2, k1=5, sub_into=0,
         hint="No single multiplication works, so scale both (try x2 and x5 to make 10y).",
         misc=[dict(pattern="substitute_sign_slip", expect=[2, 18],
                    message="x = 2 is right. Substituting into 7x + 2y = 22 gives 14 + 2y = 22, so 2y = 8 and y = 4. Getting 18 means the 14 was added instead of subtracted.")]),
    dict(disp="The sum of two numbers is 15. Twice the first number minus the second is 6. Taking \\(x\\) as the first number and \\(y\\) as the second, find x and y.",
         sols=[7, 8], calc=False,
         e0=(1, 1, 15), e1=(2, -1, 6), elim="y", sub_into=0,
         intro_say="Turn the words into algebra: \\(x + y = 15\\) and \\(2x - y = 6\\). The y terms are opposite, so add.",
         hint="Write x + y = 15 and 2x - y = 6, then add the equations to remove y.",
         misc=[dict(pattern="rhs_wrong_operation", expect=[3, 12],
                    message="Adding the equations adds both right-hand sides: 15 + 6 = 21, so 3x = 21 and x = 7. Using 15 - 6 = 9 gives x = 3, which fits neither statement.")]),
    dict(disp="Solve \\(4x - 3y = 11\\) and \\(3x + 2y = 4\\)", sols=[2, -1], calc=False,
         e0=(4, -3, 11), e1=(3, 2, 4), elim="y", k0=2, k1=3, sub_into=0,
         hint="Scale both equations: x2 and x3 makes the y terms -6y and +6y, so add.",
         misc=[dict(pattern="substitute_sign_slip", expect=[2, 5],
                    message="x = 2 is right. Substituting into 3x + 2y = 4 gives 6 + 2y = 4, so 2y = -2 and y = -1. Getting 5 means the 6 was added instead of subtracted.")]),
]


def build_subst_walk(plan):
    """Custom walk for y = 3x - 1 and 2x + y = 14."""
    steps = [
        {"say": "One equation is already rearranged: \\(y = 3x - 1\\). Substitute it into \\(2x + y = 14\\) in place of y."},
        {"pre": "Replace y: 2x + (3x - 1). Collect the x terms: 2x + 3x = ", "post": "x",
         "answer": 5, "hint": "Add the numbers in front of x: 2 + 3."},
        {"pre": "So 5x - 1 = 14. Add 1 to both sides: 5x = ", "post": "",
         "answer": 15, "hint": "Move the 1 across: 14 + 1."},
        {"say": "So 5x = 15.", "pre": "x = ", "post": "", "answer": 3,
         "hint": "Divide both sides by 5."},
        {"say": "Now find y with \\(y = 3x - 1\\):", "phase": "substitute",
         "pre": "y = 3 %s 3 %s 1 = " % (TIMES, MINUS), "post": "", "answer": 8,
         "hint": "Work out 3 times 3, then take 1."},
        {"say": "Last thing: check the pair in the other equation:", "phase": "substitute",
         "pre": "2 %s 3 + 8 = " % TIMES, "post": "", "answer": 14,
         "done": "It balances, so x = 3, y = 8 is right.",
         "hint": "Work it out. If it doesn't give 14, something slipped."}]
    return steps


def add_misc(plan):
    out = []
    sols = plan["sols"]
    for m in plan.get("misc", []):
        e = m["expect"]
        # guard: expect must not equal solution
        if e is not None and len(e) == len(sols) and all(abs(float(a) - float(b)) < 0.011 for a, b in zip(e, sols)):
            raise AssertionError(("expect==sol", plan["disp"], e))
        out.append({"pattern": m["pattern"], "check": m["pattern"],
                    "expect": [num(x) for x in e] if isinstance(e, list) else e,
                    "message": m["message"]})
    return out


def build_problem(plan):
    p = {
        "display": plan["disp"],
        "solutions": [num(x) for x in plan["sols"]],
        "input_type": plan.get("input_type", "xy_pair"),
        "calculator": plan["calc"],
        "hint": plan["hint"],
        "misconceptions": add_misc(plan),
    }
    if plan.get("special") == "subst":
        p["guided_steps"] = build_subst_walk(plan)
    else:
        p["guided_steps"] = build_elim_walk(plan)
    return p


# ---- teach walks (problems NOT in the bank) ----
def teach_bronze():
    plan = dict(disp="Solve \\(4x + y = 14\\) and \\(x + y = 5\\)", sols=[3, 2],
                e0=(4, 1, 14), e1=(1, 1, 5), elim="y", sub_into=1)
    return {"display": plan["disp"], "label": "Together: your first one",
            "steps": build_elim_walk(plan)}

def teach_silver():
    plan = dict(disp="Solve \\(2x + 3y = 18\\) and \\(x + y = 8\\)", sols=[6, 2],
                e0=(2, 3, 18), e1=(1, 1, 8), elim="x", k1=2, sub_into=1)
    return {"display": plan["disp"], "label": "Together: the silver move",
            "steps": build_elim_walk(plan)}

def teach_gold():
    plan = dict(disp="Solve \\(3x + 5y = 23\\) and \\(2x + 3y = 14\\)", sols=[1, 4],
                e0=(3, 5, 23), e1=(2, 3, 14), elim="y", k0=3, k1=5, sub_into=0)
    return {"display": plan["disp"], "label": "Together: the gold move",
            "steps": build_elim_walk(plan)}


def main():
    live = json.load(io.open("_live_L09_aqa.json", encoding="utf-8"))
    pd = {}
    # preserve
    pd["method_card"] = live["method_card"]
    pd["topic_links"] = live.get("topic_links", {"prerequisites": []})
    pd["related_videos"] = live.get("related_videos", [])
    pd["worked_examples"] = live.get("worked_examples", [])

    pb = {
        "bronze": [build_problem(p) for p in BRONZE],
        "silver": [build_problem(p) for p in SILVER],
        "gold": [build_problem(p) for p in GOLD],
        "bronze_description": "The numbers in front already match: add or subtract once and a letter vanishes",
        "silver_description": "Multiply one equation first to make a matching pair",
        "gold_description": "Multiply both equations (or use substitution) to make a match",
    }
    pd["problem_bank"] = pb

    # dedupe check within tier
    for tier in ("bronze", "silver", "gold"):
        seen = set()
        for i, p in enumerate(pb[tier]):
            k = tuple(p["solutions"])
            assert k not in seen, ("DUP", tier, i, k)
            seen.add(k)

    # tier guides
    pd["tier_guides"] = {
        "bronze": {
            "title": "Bronze: the pair already matches",
            "steps": [
                "You need the one pair of values, an \\(x\\) AND a \\(y\\), that fits both equations. In bronze a matching pair is already there (like \\(+y\\) in both).",
                "<strong>Same Signs Subtract</strong>: subtract one equation from the other, right-hand sides too, and the matched letter vanishes. Opposite signs (\\(+y\\) and \\(-y\\))? Add instead.",
                "Solve the one-letter equation that is left, then substitute your value into the easier original equation to find the other letter.",
            ],
            "example": {
                "question": "Solve 4x + y = 14 and x + y = 5",
                "steps": [
                    {"label": "Match", "content": "<p>Both equations have \\(+y\\), the same sign, so subtract.</p>"},
                    {"label": "Subtract", "content": "<p>\\((4x + y) - (x + y) = 14 - 5\\), so \\(3x = 9\\) and \\(x = 3\\).</p>"},
                    {"label": "Substitute", "content": "<p>\\(3 + y = 5\\), so \\(y = 2\\).</p>"},
                    {"label": "Check", "content": "<p>\\(4(3) + 2 = 14\\) ✓</p>"},
                    {"label": "Answer", "content": "<p>\\(x = 3\\), \\(y = 2\\)</p>", "isAnswer": True, "is_answer": True},
                ],
            },
        },
        "silver": {
            "title": "Silver: make a match first",
            "steps": [
                "Nothing matches yet. Multiply ONE whole equation, every term and both sides, until one letter has a matching coefficient.",
                "Then it is a bronze question: same signs subtract, opposite signs add.",
                "Substitute back and check your pair in both equations.",
            ],
            "example": {
                "question": "Solve 2x + 3y = 18 and x + y = 8",
                "steps": [
                    {"label": "Multiply", "content": "<p>Second equation \\(\\times 2\\): \\(2x + 2y = 16\\). The 8 is doubled too.</p>"},
                    {"label": "Subtract", "content": "<p>\\((2x + 3y) - (2x + 2y) = 18 - 16\\), so \\(y = 2\\).</p>"},
                    {"label": "Substitute", "content": "<p>\\(x + 2 = 8\\), so \\(x = 6\\).</p>"},
                    {"label": "Check", "content": "<p>\\(2(6) + 3(2) = 18\\) ✓</p>"},
                    {"label": "Answer", "content": "<p>\\(x = 6\\), \\(y = 2\\)</p>", "isAnswer": True, "is_answer": True},
                ],
            },
        },
        "gold": {
            "title": "Gold: multiply both equations",
            "steps": [
                "Sometimes no single multiplication works. Multiply BOTH equations to a common target: \\(5y\\) and \\(3y\\) both reach \\(15y\\) with \\(\\times 3\\) and \\(\\times 5\\).",
                "Everything else is the same: same signs subtract, opposite signs add, substitute back, check.",
                "Prefer rearranging? <strong>Substitution</strong> also works: make a letter the subject and put it into the other equation. Either method gets full marks.",
            ],
            "example": {
                "question": "Solve 3x + 5y = 23 and 2x + 3y = 14",
                "steps": [
                    {"label": "Multiply both", "content": "<p>First \\(\\times 3\\): \\(9x + 15y = 69\\). Second \\(\\times 5\\): \\(10x + 15y = 70\\).</p>"},
                    {"label": "Subtract", "content": "<p>\\((10x + 15y) - (9x + 15y) = 70 - 69\\), so \\(x = 1\\).</p>"},
                    {"label": "Substitute", "content": "<p>\\(3 + 5y = 23\\), so \\(y = 4\\).</p>"},
                    {"label": "Check", "content": "<p>\\(2(1) + 3(4) = 14\\) ✓</p>"},
                    {"label": "Answer", "content": "<p>\\(x = 1\\), \\(y = 4\\)</p>", "isAnswer": True, "is_answer": True},
                ],
            },
        },
    }

    # guided: opener + teach
    pd["guided"] = {
        "opener": {
            "label": "Before any algebra",
            "display": "2 teas + 1 slice of cake = £5<br>1 tea + 1 slice of cake = £3",
            "steps": [
                {"say": "A café bill puzzle. No algebra, just compare the two orders.",
                 "pre": "A tea costs £", "post": "", "answer": 2,
                 "hint": "The orders differ by exactly one tea, and by £2 of price."},
                {"say": "Comparing the orders so the cake cancels out is called <strong>elimination</strong>: you just subtracted two equations without noticing.",
                 "pre": "And the slice of cake? £", "post": "", "answer": 1,
                 "hint": "One tea (£2) and a cake cost £3 together."},
                {"say": "Using the value you know to find the one you don't is <strong>substitution</strong>. Those two moves are the whole topic. Algebra just writes tea as \\(x\\) and cake as \\(y\\): \\(2x + y = 5\\) and \\(x + y = 3\\)."},
            ],
        },
        "teach": {
            "bronze": teach_bronze(),
            "silver": teach_silver(),
            "gold": teach_gold(),
        },
    }

    json.dump(pd, io.open("lesson_algebra-L09.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print("WROTE lesson_algebra-L09.json")
    # summary
    for tier in ("bronze", "silver", "gold"):
        print(tier, [p["solutions"] for p in pb[tier]])


if __name__ == "__main__":
    main()
