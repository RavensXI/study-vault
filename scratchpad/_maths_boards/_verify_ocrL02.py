# -*- coding: utf-8 -*-
"""Independent fresh-solve check of maths-ocr graphs-L02 shard."""
import json, io
from fractions import Fraction as F

pd = json.load(io.open("lesson_maths-ocr_graphs-L02.json", encoding="utf-8"))
errs = []

def near(a, b): return abs(float(a) - float(b)) < 1e-9

# --- fresh solutions computed from scratch (mirrors displays) ---
def grad(p, q): return F(q[1]-p[1], q[0]-p[0])
fresh = {
  "bronze": [0, 7, 6, -2, 0, -1, F(1,2)*8+4, grad((0,1),(4,9))],
  "silver": [None, 3, -3, grad((2,1),(5,13)), None, -2, F(-1,4)],
  "gold":   [None, F(-1,5), None, 2, grad((2,0),(0,-6))],
}
# silver: S1 c through (1,5),(3,11): m=3 -> c=5-3=2 ; S5 y=mx+2 thru (3,-10): m=(-10-2)/3=-4
fresh["silver"][0] = 5 - grad((1,5),(3,11))*1
fresh["silver"][4] = F(-10-2,3)
# gold G1 c thru (-1,8),(3,-4): m=-3 -> c=8-(-3*-1)=8-3=5 ; G3 x+4y=12 grad -1/4 perp = 4
fresh["gold"][0] = 8 - grad((-1,8),(3,-4))*(-1)
fresh["gold"][2] = F(-1)/F(-1,4)

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        sol = p["solutions"][0]
        fv = fresh[tier][i]
        if p["input_type"] == "multiple_choice":
            if sol != fv: errs.append(f"{tier}[{i}] MC index {sol} != {fv}")
            continue
        if not near(sol, fv):
            errs.append(f"{tier}[{i}] stored {sol} != fresh {float(fv)}")
        # final guided box must equal solution (for the answer-bearing walks)
        gs = p.get("guided_steps") or []
        # completion boundary: >=1 box before substitute, >=2 live after
        boxes = [s for s in gs if s.get("answer") is not None]
        sub_idx = next((j for j,s in enumerate(gs) if s.get("phase")=="substitute"), None)
        if sub_idx is None or sub_idx < 1:
            errs.append(f"{tier}[{i}] bad substitute boundary")
        else:
            live = sum(1 for s in gs[sub_idx:] if s.get("answer") is not None)
            if live < 2: errs.append(f"{tier}[{i}] only {live} live boxes")
        # the box whose answer equals the solution must exist
        if not any(near(b["answer"], sol) for b in boxes):
            errs.append(f"{tier}[{i}] no guided box lands on solution {sol}")

# --- duplicate solutions within tier (non-MC) ---
for tier in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pd["problem_bank"][tier]):
        if p["input_type"]=="multiple_choice": continue
        k=tuple(p["solutions"])
        if k in seen: errs.append(f"{tier}[{i}] duplicate non-MC solution {k}")
        seen.add(k)

# --- expects: must differ from solution, and be numeric or null ---
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        sol=p["solutions"][0]
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is None: continue
            if isinstance(e,(int,float)) and near(e,sol):
                errs.append(f"{tier}[{i}].mis[{j}] expect==solution")

# --- expects recomputed for the ones with determinate errors ---
exp_checks = {
  ("bronze",1): -4, ("bronze",2): -2, ("bronze",3): 2, ("bronze",5): 5,
  ("bronze",6): 4, ("bronze",7): 0.5,
  ("silver",0): 8, ("silver",1): 9, ("silver",2): 3, ("silver",3): 0.25,
  ("silver",4): -12, ("silver",5): -4, ("silver",6): -4,
  ("gold",0): 2, ("gold",1): -5, ("gold",2): -4, ("gold",3): 3, ("gold",4): -3,
}
for (tier,i),want in exp_checks.items():
    got=pd["problem_bank"][tier][i]["misconceptions"][0]["expect"]
    if not near(got,want): errs.append(f"{tier}[{i}] expect {got} != recomputed {want}")

# --- opener + teach box landing checks ---
op=[s["answer"] for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if op!=[30,20,90]: errs.append(f"opener boxes {op} != [30,20,90]")
tb=[[s["answer"] for s in pd["guided"]["teach"][t]["steps"] if s.get("answer") is not None] for t in ("bronze","silver","gold")]
want_tb=[[4,-5,3,-5],[8,1,9,1],[12,4,3,-1,17]]
if tb!=want_tb: errs.append(f"teach boxes {tb} != {want_tb}")

# --- SVG sanity: G5 line should pass through both plotted points ---
import re
disp = pd["problem_bank"]["gold"][4]["display"]
# extract the drawn line endpoints and the two circles
line = re.search(r'<line x1="([\d.]+)" y1="([\d.]+)" x2="([\d.]+)" y2="([\d.]+)" stroke="#60a5fa"', disp)
circles = re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)"', disp)
x1,y1,x2,y2 = map(float, line.groups())
for cx,cy in circles:
    cx,cy=float(cx),float(cy)
    # distance of point to the line segment's infinite line
    d = abs((y2-y1)*cx-(x2-x1)*cy+x2*y1-y2*x1)/(((y2-y1)**2+(x2-x1)**2)**0.5)
    if d > 1.5: errs.append(f"G5 svg: point ({cx},{cy}) off line by {d:.2f}px")

print("PASS - all maths/box/expect/svg checks clean" if not errs else "FAIL:")
for e in errs: print("  -", e)
