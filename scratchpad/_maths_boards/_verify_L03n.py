# -*- coding: utf-8 -*-
"""Independent fresh-solve check of the built shard: every stored solution,
every guided_steps final-box landing, no dup solutions per tier, expect!=answer."""
import json, io, math

pd = json.load(io.open("lesson_maths-eduqas_number-L03.json", encoding="utf-8"))
errs = []

# expected solutions computed independently from the display maths
EXPECT = {
 "bronze": [3.5, 7.8, 12.37, 0.55, 6.05, 3.33, 0.18, 8],
 "silver": [4600, 0.0037, 38500, 0.12, 80, 30, 0.0605],
 "gold":   [200, 35, 0.25, 120, 60],
}
# recompute a few from raw arithmetic to be sure
assert round(3.6+2.45,2)==6.05
assert round(5.2-1.87,2)==3.33
assert round(0.6*0.3,2)==0.18
assert round(4.8/0.6,6)==8
assert round(0.24*0.5,3)==0.12
assert round(7.2/0.09,6)==80
assert 6*5==30 and round(6.2*4.8,2)==29.76
assert round(0.3**2+0.4**2,4)==0.25
assert 5*20/0.5==200
assert 7/0.2==35
assert 36/0.3==120
assert round(1.2*3.5/0.07,6)==60

for tier in ("bronze","silver","gold"):
    probs = pd["problem_bank"][tier]
    exp = EXPECT[tier]
    if len(probs)!=len(exp):
        errs.append(f"{tier}: {len(probs)} probs vs {len(exp)} expected")
    seen=set()
    for i,p in enumerate(probs):
        sol = p["solutions"][0]
        if abs(sol-exp[i])>1e-9:
            errs.append(f"{tier}[{i}] stored {sol} != fresh {exp[i]}")
        if sol in seen:
            errs.append(f"{tier}[{i}] DUP solution {sol}")
        seen.add(sol)
        # last live box lands on solution
        gs=p["guided_steps"]
        boxes=[s for s in gs if s.get("answer") is not None]
        # final 'done' box should equal solution (the answer-writing box)
        # find the box whose answer==sol
        if not any(abs(b["answer"]-sol)<1e-9 for b in boxes):
            errs.append(f"{tier}[{i}] no guided box lands on solution {sol}")
        # substitute boundary present, >=1 before, >=2 live at/after
        sub=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not sub:
            errs.append(f"{tier}[{i}] no substitute phase")
        else:
            k=sub[0]
            live_after=sum(1 for s in gs[k:] if s.get("answer") is not None)
            if k<1: errs.append(f"{tier}[{i}] boundary at 0")
            if live_after<2: errs.append(f"{tier}[{i}] only {live_after} live after boundary")
        # expect != solution
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None and abs(float(e)-sol)<1e-9:
                errs.append(f"{tier}[{i}] expect {e} == solution")

# teach walks land correctly
teach_final = {"bronze":8.46,"silver":0.072,"gold":160}
for tier,val in teach_final.items():
    t=pd["guided"]["teach"][tier]
    boxes=[s for s in t["steps"] if s.get("answer") is not None]
    if not any(abs(b["answer"]-val)<1e-9 for b in boxes):
        errs.append(f"teach.{tier} does not reach {val}")
    if len(boxes)<4:
        errs.append(f"teach.{tier} only {len(boxes)} boxes")
# teach maths recompute
assert 4*8/0.2==160
# opener boxes
ob=[s for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if [b["answer"] for b in ob]!=[4,3]:
    errs.append(f"opener answers {[b['answer'] for b in ob]} != [4,3]")

if errs:
    print("VERIFY FAIL:")
    for e in errs: print("  -",e)
else:
    print("VERIFY OK: all solutions, boxes, boundaries, expects check out")
