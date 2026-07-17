# -*- coding: utf-8 -*-
import json, io
from fractions import Fraction as F

MIN = "−"   # minus sign
TMS = "×"   # times
ARR = "  →  "  # arrow

def num(v):
    v = F(v)
    return int(v) if v.denominator == 1 else float(v)

def paren(v):
    v = num(v)
    return f"({v})" if (isinstance(v, int) and v < 0) or (isinstance(v, float) and v < 0) else str(v)

def coefpre(c, var):
    c = int(c)
    if c == 1: return var
    if c == -1: return "-" + var
    return f"{c}{var}"

def rhspre(c):
    c = num(c)
    return f"({c})" if c < 0 else str(c)

def eqlatex(a, b, c):
    # a x + b y = c  (LaTeX, ascii minus)
    a, b, c = int(a), int(b), int(c)
    xt = "x" if a == 1 else ("-x" if a == -1 else f"{a}x")
    if b >= 0:
        yt = "+ y" if b == 1 else f"+ {b}y"
    else:
        yt = "- y" if b == -1 else f"- {abs(b)}y"
    return f"{xt} {yt} = {c}"

def solve(eqA, eqB):
    a1,b1,c1 = eqA; a2,b2,c2 = eqB
    det = a1*b2 - a2*b1
    return num(F(c1*b2 - c2*b1, det)), num(F(a1*c2 - a2*c1, det))

def scale(eq, k):
    return (eq[0]*k, eq[1]*k, eq[2]*k)

def mult_block(eq, k, elim, first_say=True):
    a,b,c = eq
    steps = []
    say = f"To make the {elim} terms match, multiply ALL of \\({eqlatex(*eq)}\\) by {k}: every term, both sides."
    steps.append({"say": say, "pre": f"{coefpre(a,'x')} {TMS} {k} = ", "post": "x", "answer": num(a*k),
                  "hint": "Just multiply the number in front."})
    hy = "Just multiply the number in front, and keep the minus." if b < 0 else "Just multiply the number in front."
    steps.append({"say": None, "pre": f"{coefpre(b,'y')} {TMS} {k} = ", "post": "y", "answer": num(b*k), "hint": hy})
    steps.append({"pre": f"and the right-hand side: {rhspre(c)} {TMS} {k} = ", "post": "", "answer": num(c*k),
                  "hint": "The right-hand side gets multiplied too. That's the step everyone forgets."})
    return steps

def elim_block(A, B, elim):
    # A, B already scaled tuples. elim in {'x','y'}. Returns (steps, kept_var, kept_coeff, kept_rhs)
    ei = 0 if elim == 'x' else 1
    ki = 1 - ei
    keptvar = 'y' if elim == 'x' else 'x'
    eA, eB = A[ei], B[ei]
    kA, kB = A[ki], B[ki]
    steps = []
    if eA == eB:  # same sign -> subtract
        if kA >= kB:
            hi, lo = A, B
        else:
            hi, lo = B, A
        kc = hi[ki] - lo[ki]
        rhs = hi[2] - lo[2]
        elimcoef = coefpre(eA, elim)
        steps.append({"say": f"Both equations now have {elimcoef}, the same sign. <strong>Same Signs Subtract.</strong> Take \\({eqlatex(*lo)}\\) away from \\({eqlatex(*hi)}\\), term by term:",
                      "pre": f"{coefpre(hi[ki],keptvar)} {MIN} {coefpre(lo[ki],keptvar)} = ", "post": keptvar, "answer": num(kc),
                      "hint": f"Subtract the numbers in front: {hi[ki]} {MIN} {lo[ki]}."})
        steps.append({"pre": f"{coefpre(hi[ei],elim)} {MIN} {coefpre(lo[ei],elim)} = ", "post": "", "answer": 0,
                      "done": "Gone. That was the whole point.", "hint": "They're identical, and anything minus itself is 0."})
        steps.append({"pre": f"{rhspre(hi[2])} {MIN} {rhspre(lo[2])} = ", "post": "", "answer": num(rhs),
                      "hint": "The right-hand sides get subtracted too, exactly like the left."})
        return steps, keptvar, num(kc), num(rhs)
    else:  # opposite -> add
        kc = kA + kB
        rhs = A[2] + B[2]
        steps.append({"say": f"The {elim} terms are {coefpre(A[ei],elim)} and {coefpre(B[ei],elim)}. Opposite signs, so <strong>ADD</strong> the equations and they cancel:",
                      "pre": f"{coefpre(A[ki],keptvar)} + {coefpre(B[ki],keptvar)} = ", "post": keptvar, "answer": num(kc),
                      "hint": "Add the numbers in front."})
        bterm = coefpre(B[ei], elim)
        bterm = f"({bterm})" if B[ei] < 0 else bterm
        steps.append({"pre": f"{coefpre(A[ei],elim)} + {bterm} = ", "post": "", "answer": 0,
                      "done": "Cancelled. Adding opposites gives zero.", "hint": "One is plus, one is minus, same size, so they cancel to 0."})
        steps.append({"pre": f"{rhspre(A[2])} + {rhspre(B[2])} = ", "post": "", "answer": num(rhs),
                      "hint": "Add the right-hand sides too."})
        return steps, keptvar, num(kc), num(rhs)

def solve_kept(keptvar, kc, rhs):
    val = num(F(rhs, kc))
    if kc == 1:
        return [{"say": f"So {keptvar} = {val}. Done in one."}], val
    return [{"say": f"So {kc}{keptvar} = {rhs}.", "pre": f"{keptvar} = ", "post": "", "answer": val,
             "hint": f"Divide both sides by {kc}."}], val

def sub_phase(sub_eq, known_var, known_val, find_var, find_val):
    sa, sb, sc = sub_eq
    kc = sa if known_var == 'x' else sb
    oc = sb if known_var == 'x' else sa
    knownterm = num(kc * known_val)
    say = f"Now find {find_var}. Put {known_var} = {paren(known_val)} into \\({eqlatex(*sub_eq)}\\)."
    if abs(kc) != 1:
        say += f" The {known_var} part is {abs(kc)} {TMS} {paren(known_val)} = {knownterm}, so:"
    steps = []
    if abs(oc) == 1:
        sign = "+" if oc > 0 else MIN
        pre = f"{knownterm} {sign} {find_var} = {sc}{ARR}{find_var} = "
        if oc > 0:
            hint = f"Take {knownterm} from both sides."
        else:
            hint = f"{knownterm} minus what gives {sc}?"
        steps.append({"say": say, "phase": "substitute", "pre": pre, "post": "", "answer": num(find_val), "hint": hint})
    else:
        rem = num(sc - knownterm)
        steps.append({"say": say, "phase": "substitute", "pre": f"{coefpre(oc,find_var)} = {sc} {MIN} {knownterm} = ",
                      "post": "", "answer": rem, "hint": "Whatever is left after taking the known part away."})
        steps.append({"phase": "substitute", "pre": f"{find_var} = ", "post": "", "answer": num(find_val),
                      "hint": f"Divide by {oc}."})
    return steps

def check_phase(check_eq, x, y):
    a, b, c = check_eq
    def piece(coef, val):
        mag = abs(int(coef)); vs = paren(val)
        return f"{mag} {TMS} {vs}" if mag != 1 else vs
    p1 = piece(a, x)
    op = "+" if b > 0 else MIN
    p2 = piece(b, y)
    return [{"say": "Last thing: check the pair in the other equation:",
             "pre": f"{p1} {op} {p2} = ", "post": "", "answer": num(c),
             "done": f"It balances, so x = {paren(x)}, y = {paren(y)} is right.",
             "hint": f"Work it out. If it doesn't give {c}, something slipped."}]

def build_walk(eqA, eqB, sA, sB, elim, sub_idx):
    steps = []
    A = scale(eqA, sA); B = scale(eqB, sB)
    if sA != 1:
        steps += mult_block(eqA, sA, elim)
    if sB != 1:
        steps += mult_block(eqB, sB, elim)
    eb, keptvar, kc, rhs = elim_block(A, B, elim)
    steps += eb
    sk, kval = solve_kept(keptvar, kc, rhs)
    steps += sk
    x, y = solve(eqA, eqB)
    known_val = kval
    find_var = 'y' if keptvar == 'x' else 'x'
    find_val = y if find_var == 'y' else x
    sub_eq = eqA if sub_idx == 0 else eqB
    check_eq = eqB if sub_idx == 0 else eqA
    steps += sub_phase(sub_eq, keptvar, kval, find_var, find_val)
    steps += check_phase(check_eq, x, y)
    return steps, (x, y)

if __name__ == "__main__":
    # smoke test
    s, sol = build_walk((2,1,9),(1,1,6),1,1,'y',1)
    for st in s:
        print(st)
    print("SOL", sol)
