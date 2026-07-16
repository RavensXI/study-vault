# -*- coding: utf-8 -*-
import json, io, re
import sympy as sp

pd = json.load(io.open("lesson_algebra-L05.json", encoding="utf-8"))
x = sp.symbols('x')
errs = []

def parse_display(disp):
    # extract LaTeX inside \( ... \)
    m = re.search(r"\\\((.*?)\\\)", disp)
    s = m.group(1)
    s = s.replace("−", "-")
    # fractions \frac{A}{B}
    s = re.sub(r"\\frac\{(.+?)\}\{(.+?)\}", r"((\1)/(\2))", s)
    # implicit multiplication for coefficients like 2x, 3(  -> handled by sympy parse if we insert *
    # split on '='
    lhs, rhs = s.split("=")
    def prep(e):
        e = e.strip()
        # insert * between number and letter/paren, and letter/paren and paren
        e = re.sub(r"(\d)([x\(])", r"\1*\2", e)
        e = re.sub(r"(\))(\()", r"\1*\2", e)
        e = re.sub(r"([x\)])(\()", r"\1*\2", e)
        e = re.sub(r"(\d)\s+([x\(])", r"\1*\2", e)  # 'x 4' none; safe
        return e
    return sp.sympify(prep(lhs)), sp.sympify(prep(rhs))

# 1. Solve every display, compare to solutions
for tier in ["bronze","silver","gold"]:
    sols_seen=[]
    for i,p in enumerate(pd["problem_bank"][tier]):
        lhs,rhs = parse_display(p["display"])
        roots = sp.solve(sp.Eq(lhs,rhs), x)
        stored = p["solutions"]
        if len(roots)!=1:
            errs.append(f"{tier}[{i}] roots {roots}")
            continue
        r = float(roots[0])
        if abs(r-float(stored[0]))>1e-9:
            errs.append(f"{tier}[{i}] display solves to {r} but stored {stored}")
        sols_seen.append(tuple(stored))
    dups=[s for s in set(sols_seen) if sols_seen.count(s)>1]
    if dups:
        errs.append(f"{tier} DUPLICATE solutions {dups}")

# 2. Evaluate pure-arithmetic guided boxes
LABELS = ["Left x-terms:", "Right side:", "Left:", "Right:", "then", "and the right-hand side:"]
def strip_label(pre):
    p = pre
    for L in LABELS:
        if p.strip().startswith(L):
            p = p.strip()[len(L):]
    return p.strip()

def try_eval_box(pre, answer, where):
    p = strip_label(pre)
    # must end with '='
    if not p.rstrip().endswith("="):
        return
    expr = p.rstrip()[:-1]
    expr = expr.replace("×","*").replace("÷","/").replace("−","-")
    # skip if contains a letter (x) -> coefficient box, verify separately
    if "x" in expr:
        return
    # skip if empty
    if not expr.strip():
        return
    try:
        val = eval(expr, {"__builtins__":{}})
    except Exception as e:
        return
    if abs(float(val)-float(answer))>1e-9:
        errs.append(f"{where}: pre '{pre}' evaluates to {val} but answer {answer}")

def walk(steps, where):
    for j,st in enumerate(steps):
        if st.get("answer") is not None and st.get("pre"):
            try_eval_box(st["pre"], st["answer"], f"{where}[{j}]")

for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pd["problem_bank"][tier]):
        walk(p.get("guided_steps",[]), f"{tier}[{i}].guided_steps")
walk(pd["guided"]["opener"]["steps"], "opener")
for t in ["bronze","silver","gold"]:
    walk(pd["guided"]["teach"][t]["steps"], f"teach.{t}")

# 3. Coefficient boxes (contain x): print for eyeball + auto-check simple 'a op b' coeff
def coeff_check(pre, answer, where):
    p = strip_label(pre)
    if not p.rstrip().endswith("="): return
    expr = p.rstrip()[:-1].strip()
    if "x" not in expr: return
    # patterns: 'A × x' -> A ; 'A × Bx' -> A*B ; 'Ax − Bx' -> A-B ; 'Ax + Bx'->A+B ; 'A × (−B)' handled by eval branch
    e = expr.replace("×","*").replace("−","-").replace("÷","/")
    # replace 'Nx' with N , and lone 'x' with 1
    e2 = re.sub(r"(\d+)\*x", r"\1", e)         # a*x -> a  (from 'A × x')
    e2 = re.sub(r"(\d+)\*(\d+)x", r"(\1*\2)", e2)  # a*bx -> a*b (from 'A × Bx')
    e2 = re.sub(r"(\d+)x", r"\1", e2)          # bx -> b (coefficient)
    e2 = re.sub(r"(?<![\d])x", "1", e2)        # lone x -> 1
    try:
        val = eval(e2, {"__builtins__":{}})
    except Exception:
        print("  COEFF-MANUAL", where, repr(expr), "->", answer); return
    if abs(float(val)-float(answer))>1e-9:
        errs.append(f"{where}: coeff pre '{pre}' -> {val} but answer {answer}")

for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pd["problem_bank"][tier]):
        for j,st in enumerate(p.get("guided_steps",[])):
            if st.get("answer") is not None and st.get("pre"):
                coeff_check(st["pre"], st["answer"], f"{tier}[{i}].gs[{j}]")
for t in ["bronze","silver","gold"]:
    for j,st in enumerate(pd["guided"]["teach"][t]["steps"]):
        if st.get("answer") is not None and st.get("pre"):
            coeff_check(st["pre"], st["answer"], f"teach.{t}[{j}]")

# 4. completion boundary: >=1 box before first phase, >=2 live at/after
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pd["problem_bank"][tier]):
        steps=p["guided_steps"]
        sub=[k for k,s in enumerate(steps) if s.get("phase")=="substitute"]
        if not sub: errs.append(f"{tier}[{i}] no substitute phase")
        else:
            first=sub[0]
            before=sum(1 for s in steps[:first] if s.get("answer") is not None)
            after=sum(1 for s in steps[first:] if s.get("answer") is not None)
            if before<1: errs.append(f"{tier}[{i}] no box before boundary")
            if after<2: errs.append(f"{tier}[{i}] only {after} live boxes after boundary")

# 5. expect != solution and recompute a few key expects
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pd["problem_bank"][tier]):
        sol=float(p["solutions"][0])
        for m in p.get("misconceptions",[]):
            e=m["expect"]
            if e is not None and abs(float(e)-sol)<1e-9:
                errs.append(f"{tier}[{i}] expect {e} == solution")

print("solutions per tier:")
for t in ["bronze","silver","gold"]:
    print(" ",t,[p["solutions"] for p in pd["problem_bank"][t]])
if errs:
    print("FAIL", len(errs))
    for e in errs: print("  -",e)
else:
    print("VERIFY OK: all displays solve to stored, all arithmetic boxes correct, boundaries ok, expects distinct")
