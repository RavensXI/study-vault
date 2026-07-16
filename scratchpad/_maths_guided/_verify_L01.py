# -*- coding: utf-8 -*-
# Independent re-solve of every problem + check guided final boxes land on solutions.
import json, io
from fractions import Fraction as F

pd = json.load(io.open("lesson_probability-statistics-L01.json", encoding="utf-8"))
errs = []

# expected fresh solutions per (tier, idx)
expect = {
 ("bronze",0):[0.4], ("bronze",1):[0.7], ("bronze",2):[1,5], ("bronze",3):[0.25],
 ("bronze",4):[5,6], ("bronze",5):[3,4], ("bronze",6):[0.3], ("bronze",7):[0.2],
 ("silver",0):[0.09], ("silver",1):[0.2], ("silver",2):[5,14], ("silver",3):[0.216],
 ("silver",4):[0.12], ("silver",5):[13,15], ("silver",6):[0.38],
 ("gold",0):[14,55], ("gold",1):[0.063], ("gold",2):[1,6], ("gold",3):[5], ("gold",4):[0.4],
}

for (t,i),exp in expect.items():
    got = pd["problem_bank"][t][i]["solutions"]
    if [round(x,6) for x in got] != [round(x,6) for x in exp]:
        errs.append(f"{t}[{i}] solutions {got} != fresh {exp}")

# misconception expects must not equal solution and should be present
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][t]):
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is not None:
                ev=e if isinstance(e,list) else [e]
                sv=p["solutions"]
                if len(ev)==len(sv) and all(abs(float(a)-float(b))<1e-6 for a,b in zip(ev,sv)):
                    errs.append(f"{t}[{i}].mis[{j}] expect==solution")

# check each guided_steps: boundary rules + at least one box == a solution component
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][t]):
        gs=p.get("guided_steps")
        if not gs:
            errs.append(f"{t}[{i}] no guided_steps"); continue
        boxes=[s for s in gs if s.get("answer") is not None]
        sub=[k for k,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not sub: errs.append(f"{t}[{i}] no phase")
        else:
            live=sum(1 for s in gs[sub[0]:] if s.get("answer") is not None)
            if live<2: errs.append(f"{t}[{i}] live<2")
            if sub[0]<1: errs.append(f"{t}[{i}] phase at 0")
        # solution components must appear among box answers
        sol=p["solutions"]
        vals=[s["answer"] for s in boxes]
        for c in sol:
            if not any(abs(float(v)-float(c))<1e-6 for v in vals):
                errs.append(f"{t}[{i}] solution component {c} not among boxes {vals}")

# teach boxes >=4, opener >=1 box
for t in ("bronze","silver","gold"):
    tb=pd["guided"]["teach"][t]["steps"]
    nb=sum(1 for s in tb if s.get("answer") is not None)
    if nb<4: errs.append(f"teach {t} boxes {nb}<4")
ob=sum(1 for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None)
if ob<1: errs.append("opener no box")

# specific hand-recompute checks
def approx(a,b): return abs(a-b)<1e-6
checks=[
 ("b0", 2/5, 0.4),("b6",3/10,0.3),("b7",1-0.45-0.35,0.2),
 ("s0",0.3*0.3,0.09),("s3",0.6**3,0.216),("s4",0.4*0.3,0.12),("s6",0.25+0.09+0.04,0.38),
 ("g1",0.3*0.3*0.7,0.063),("g4",2*0.4*0.6,0.48),
]
for name,a,b in checks:
    if not approx(a,b): errs.append(f"handcheck {name}: {a}!={b}")
# fraction checks
assert F(5,8)*F(4,7)==F(5,14)
assert F(8,12)*F(7,11)*F(6,10)==F(14,55)
assert 1-F(4,10)*F(3,9)==F(13,15)
assert F(4,10)*F(6,9)+F(6,10)*F(4,9)==F(8,15)  # s5 expect
assert (5+5)*(4+5)==90 and F(5,10)*F(4,9)==F(2,9)  # g3
assert F(3,10)*F(2,9)==F(1,15)  # s0 expect 0.067 ~ 1/15
print("1/15 =", float(F(1,15)))

if errs:
    print("VERIFY FAIL:")
    for e in errs: print("  -",e)
else:
    print("VERIFY OK: all solutions fresh-correct, boundaries valid, boxes land on solutions.")
