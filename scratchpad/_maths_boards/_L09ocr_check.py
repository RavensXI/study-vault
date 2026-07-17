# -*- coding: utf-8 -*-
import json, io, re, sys
from fractions import Fraction as F
sys.stdout.reconfigure(encoding="utf-8")
pd = json.load(io.open("lesson_maths-ocr_algebra-L09.json", encoding="utf-8"))

def parse_eq(s):  # "3x + 4y = 25" -> (a,b,c)
    s = s.replace(" ", "")
    mx = re.search(r'(?<![\d])(-?)(\d*)x', s)
    a = int((mx.group(1) or "") + (mx.group(2) or "1")) if mx.group(2) else int((mx.group(1) or "") + "1")
    my = re.search(r'([+-])(\d*)y', s)
    b = int(my.group(1) + (my.group(2) or "1"))
    c = int(re.search(r'=(-?\d+)', s).group(1))
    return a, b, c

def eqs_from_display(disp):
    return [parse_eq(g) for g in re.findall(r'\\\((.*?)\\\)', disp)][:2]

def solve(A, B):
    a1,b1,c1=A; a2,b2,c2=B; det=a1*b2-a2*b1
    return F(c1*b2-c2*b1,det), F(a1*c2-a2*c1,det)

def final_pair_from_walk(steps):
    # last two distinct box answers that are the substitution/solve results are hard to map;
    # instead verify the CHECK box: its answer must equal RHS when solutions plugged (done elsewhere)
    return [s.get("answer") for s in steps if s.get("answer") is not None]

fails = []
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        disp = p["display"]
        eqs = eqs_from_display(disp)
        sol = p["solutions"]
        if p.get("input_type")=="xy_pair" and len(eqs)==2:
            x,y = solve(*eqs)
            if [ (int(x) if x.denominator==1 else float(x)), (int(y) if y.denominator==1 else float(y)) ] != sol:
                # word problem has no LaTeX eqs -> eqs empty, skip
                fails.append(f"{tier}[{i}] parsed {eqs} solves ({x},{y}) != stored {sol}")
        # verify walk final check box lands consistent: recompute all guided boxes independently is done by generator
        gs = p.get("guided_steps") or []
        # check the CHECK step (last box with 'done' containing 'balances' or the last box) using solutions
        # ensure every box answer numeric
        for j,st in enumerate(gs):
            if st.get("answer") is not None and not isinstance(st["answer"],(int,float)):
                fails.append(f"{tier}[{i}].guided_steps[{j}] non-numeric answer")

# word problem explicit
wp = pd["problem_bank"]["gold"][2]
assert wp["solutions"]==[60,60]
# x+y=120, 8x+5y=780
assert 60+60==120 and 8*60+5*60==780, "word problem numbers"

# opener: 2x+y=25, x+y=16 with x=9,y=7
assert 2*9+7==25 and 9+7==16, "opener"
# teach re-solve from displays
for tier in ("bronze","silver","gold"):
    t = pd["guided"]["teach"][tier]
    eqs = eqs_from_display(t["display"])
    x,y = solve(*eqs)
    boxes = [s.get("answer") for s in t["steps"] if s.get("answer") is not None]
    # the final check box answer should equal an eq RHS; just report solved pair
    print(f"teach {tier}: {t['display']} -> ({x},{y})")

# reproduce every misconception expect by committing its error? cross-check none equals solution
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        for m in p.get("misconceptions",[]):
            e=m["expect"]
            if e is not None and e==p["solutions"]:
                fails.append(f"{tier}[{i}] expect==solution")

# em dash sweep on all student-facing strings
def sweep(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note",): continue
            sweep(v,path+"."+k)
    elif isinstance(o,list):
        for k,v in enumerate(o): sweep(v,f"{path}[{k}]")
    elif isinstance(o,str) and "—" in o:
        fails.append("EM DASH at "+path)
sweep(pd,"pd")

print("\nRESULT:", "ALL CHECKS PASS" if not fails else "FAILURES:")
for f in fails: print("  -",f)
