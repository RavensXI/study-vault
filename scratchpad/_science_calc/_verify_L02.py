# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("lesson_higher-calculations-L02@6e6bcbcbc7.json", encoding="utf-8"))
errs = []

# 1. Fresh-solve every problem (independent recompute) keyed by expected solution
Vm = 24.0
def close(a, b, t=0.005): return abs(a - b) <= t
expected = {  # tier,index -> recomputed answer
 ("bronze",0): 0.5*24, ("bronze",1): 4.8/24, ("bronze",2): 2*24,
 ("bronze",3): 56/(56+44)*100, ("bronze",4): 100.0, ("bronze",5): 7.5/10*100,
 ("bronze",6): (0.1/2)*24, ("bronze",7): 7.2/24,
 ("silver",0): (5.0/100)*24, ("silver",1): ((4.6/23)/2)*24, ("silver",2): (0.6/24)*24,
 ("silver",3): (5.6/((10/160*2)*56))*100, ("silver",4): (2*56)/((2*56)+(3*44))*100,
 ("silver",5): 100.0,
 ("gold",0): (960/((3.25/65)*24*1000))*100, ("gold",1): 56/(56+18)*100,
 ("gold",2): (32/160*3)*24, ("gold",3): (12.25/122.5*3/2)*24,
 ("gold",4): (504/((2.5/100)*24*1000))*100, ("gold",5): (3*32)/((3*32)+(2*74.5))*100,
}
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol = p["solutions"][0]
        exp = expected[(tier,i)]
        acc = p.get("accept", 0.05)
        if abs(sol-exp) > acc + 1e-9:
            errs.append(f"{tier}[{i}] stored {sol} != recomputed {exp:.4f} (accept {acc})")
        # misconception expect: outside accept, not equal correct
        for j,m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is not None and abs(float(e)-sol) < max(acc,0.011)+1e-9:
                errs.append(f"{tier}[{i}].mis[{j}] expect {e} inside accept of {sol}")
        # every problem has a hint or equation_hint
        if not (p.get("hint") or p.get("equation_hint")):
            errs.append(f"{tier}[{i}] no hint")

# 2. Recompute every guided_steps box: last live box lands on solution; check-box arithmetic
def eval_box(pre):
    # extract 'a OP b = ' or 'a OP b OP c = ' simple arithmetic in pre text
    expr = pre
    return None
# Instead assert final numeric box equals solution (or stated rounding), and
# that each box value is internally consistent by manual table.
box_expect = {
 # (tier,i): [list of box answers in order]
 ("bronze",0): [0.5,12,0.5], ("bronze",1): [4.8,0.2,4.8], ("bronze",2): [2,48,2],
 ("bronze",3): [100,56,44], ("bronze",4): [1,100,0], ("bronze",5): [10,75,7.5],
 ("bronze",6): [2,0.05,1.2,0.05], ("bronze",7): [7.2,0.3,7.2],
 ("silver",0): [0.05,0.05,1.2,0.05], ("silver",1): [0.2,0.1,2.4,0.1],
 ("silver",2): [0.025,0.025,0.6,0.025], ("silver",3): [0.0625,0.125,7,80,5.6],
 ("silver",4): [112,132,244,45.9,54.1], ("silver",5): [1,100,0],
 ("gold",0): [0.05,0.05,1.2,1200,80,960], ("gold",1): [74,75.68,24.32],
 ("gold",2): [0.2,0.6,14.4,0.6], ("gold",3): [122.5,0.1,0.15,3.6,0.15],
 ("gold",4): [0.025,0.025,0.6,600,84,504], ("gold",5): [96,149,245,39.18,60.82],
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        boxes = [s["answer"] for s in p["guided_steps"] if s.get("answer") is not None]
        want = box_expect[(tier,i)]
        if boxes != want:
            errs.append(f"{tier}[{i}] boxes {boxes} != {want}")
        # substitute boundary sanity
        idx = [k for k,s in enumerate(p["guided_steps"]) if s.get("phase")=="substitute"]
        if not idx:
            errs.append(f"{tier}[{i}] no substitute phase")
        else:
            live = sum(1 for s in p["guided_steps"][idx[0]:] if s.get("answer") is not None)
            if live < 2: errs.append(f"{tier}[{i}] <2 live after boundary")
            if idx[0] < 1: errs.append(f"{tier}[{i}] boundary at 0")

# 3. teach boxes >=4 and opener has a box
for t in ("bronze","silver","gold"):
    tb = [s for s in pd["guided"]["teach"][t]["steps"] if s.get("answer") is not None]
    if len(tb) < 4: errs.append(f"teach.{t} <4 boxes")
if not any(s.get("answer") is not None for s in pd["guided"]["opener"]["steps"]):
    errs.append("opener no box")

# verify specific rounding boxes are within 0.005 of true value
assert close(75.68, 56/74*100), "G1 75.68"
assert close(39.18, 96/245*100), "G5 39.18"
assert close(45.9, 112/244*100), "S4 45.9"
assert close(24.32, 100-56/74*100, 0.01), "G1 check"  # 24.3243 vs 24.32 -> 0.0043
assert close(60.82, 100-96/245*100, 0.01), "G5 check"

print("VERIFY ERRORS:", len(errs))
for e in errs: print("  -", e)
print("rounding-box precision OK")
