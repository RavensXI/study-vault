# -*- coding: utf-8 -*-
import json, io, math
pd = json.load(io.open("lesson_higher-calculations-L01@8a0771bf50.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# independent fresh solves keyed by (tier,index)
def close(a, b, tol): return abs(a-b) <= tol
solve = {
 ("bronze",0): 40*0.05,               # F=ke
 ("bronze",1): 5.0/0.10,              # k=F/e
 ("bronze",2): 10/200.0,             # e=F/k
 ("bronze",3): 3/0.03,               # k, e=23-20=3cm
 ("bronze",4): 0.5*50*0.04**2,       # Epe
 ("silver",0): 0.5*120*0.08**2,      # Epe
 ("silver",1): math.sqrt(2*(0.5*500*0.10**2)/0.20),  # v
 ("silver",2): 15/0.06,              # k
 ("silver",3): math.sqrt(2*5.4/300), # e
 ("silver",4): 2*(0.5*60*0.15**2),   # total Epe
 ("gold",0): math.sqrt(2*(0.5*400*0.12**2)/0.16),   # v
 ("gold",1): 2*0.450/0.06**2,        # k
 ("gold",2): 0.20*9.8*3.0,           # Epe=GPE
 ("gold",3): 10/100.0 + 10/200.0,    # total extension
}
for (tier,i),val in solve.items():
    p = pb[tier][i]
    sol = p["solutions"][0]
    acc = p.get("accept", 0.005)
    if not close(val, sol, max(acc,0.005)+1e-9):
        errs.append(f"{tier}[{i}] SOLUTION mismatch: fresh={val:.5f} stored={sol} accept={acc}")

# check every misconception expect: present, != correct within accept window
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=float(p["solutions"][0]); acc=p.get("accept",0.005)
        for j,m in enumerate(p.get("misconceptions",[])):
            if "expect" not in m: errs.append(f"{tier}[{i}].m{j} no expect"); continue
            e=m["expect"]
            if e is None: continue
            if abs(float(e)-sol) < max(acc,0.011):
                errs.append(f"{tier}[{i}].m{j} expect {e} INSIDE accept window of {sol}")

# recompute guided_steps boxes: verify final live box == solution, boundary rules,
# and internal arithmetic continuity where boxes are numeric.
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps");
        if not gs: errs.append(f"{tier}[{i}] no guided_steps"); continue
        boxes=[s for s in gs if s.get("answer") is not None]
        subidx=[k for k,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not subidx: errs.append(f"{tier}[{i}] no phase boundary")
        sol=float(p["solutions"][0]); acc=p.get("accept",0.005)
        # the compute/answer for the solution should appear as one of the boxes at/after boundary
        after=[s for k,s in enumerate(gs) if subidx and k>=subidx[0] and s.get("answer") is not None]
        if len(after)<2: errs.append(f"{tier}[{i}] <2 live boxes after boundary")
        vals=[float(b["answer"]) for b in boxes]
        if not any(close(v,sol,max(acc,0.005)+1e-6) for v in vals):
            errs.append(f"{tier}[{i}] no box equals solution {sol}; boxes={vals}")

# spot-check specific box arithmetic
checks = [
 ("bronze",0,[0.05,2,40]),
 ("bronze",3,[3,0.03,100,3]),
 ("bronze",4,[0.0016,0.04,0.08]),
 ("silver",0,[0.08,0.0064,0.384,0.768]),
 ("silver",1,[2.5,0.1,25,5,2.5]),
 ("silver",3,[0.036,0.1897,5.4]),
 ("silver",4,[0.0225,0.675,1.35,0.675]),
 ("gold",0,[2.88,0.08,36,6,2.88]),
 ("gold",1,[6,0.0036,250,0.45]),
 ("gold",2,[1.96,5.88,1.96]),
 ("gold",3,[0.1,0.05,0.15,10]),
]
for tier,i,expected in checks:
    boxes=[float(s["answer"]) for s in pb[tier][i]["guided_steps"] if s.get("answer") is not None]
    if boxes!=[float(x) for x in expected]:
        errs.append(f"{tier}[{i}] box sequence {boxes} != expected {expected}")

# teach walk arithmetic
teach=pd["guided"]["teach"]
tb={"bronze":[80,9.6,0.125,10],"silver":[0.08,0.0064,0.8,0.08],"gold":[4,0.2,20,4.47]}
for t,exp in tb.items():
    got=[float(s["answer"]) for s in teach[t]["steps"] if s.get("answer") is not None]
    if got!=[float(x) for x in exp]:
        errs.append(f"teach.{t} boxes {got} != {exp}")
# verify teach maths (float-safe)
for got,exp in [(4/0.05,80),(80*0.12,9.6),(10/80,0.125),(0.5*250*0.08**2,0.8),
                (0.5*800*0.10**2,4),(4/0.2,20),(round(math.sqrt(20),2),4.47)]:
    if not close(got,exp,1e-6): errs.append(f"teach maths {got}!={exp}")

# opener
op=[float(s["answer"]) for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if op!=[4.0,6.0]: errs.append(f"opener boxes {op}")

# svg cleanliness
def walk(o):
    if isinstance(o,dict):
        for v in o.values(): yield from walk(v)
    elif isinstance(o,list):
        for v in o: yield from walk(v)
    elif isinstance(o,str): yield o
for s in walk(pd):
    if "<svg" in s:
        if "http://" in s.lower() or "https://" in s.lower(): errs.append("svg has http")
        if 'role="img"' not in s: errs.append("svg missing role")
        if "aria-label" not in s: errs.append("svg missing aria-label")
    if "—" in s: errs.append("EM DASH remains: "+s[:40])

# units present
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if not p.get("unit"): errs.append(f"{tier}[{i}] no unit")

print("SOLUTIONS:", {k:round(v,4) for k,v in solve.items()})
if errs:
    print("FAIL", len(errs))
    for e in errs: print("  -",e)
else:
    print("ALL VERIFICATION CHECKS PASS")
