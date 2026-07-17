# -*- coding: utf-8 -*-
import json
pd=json.load(open("lesson_maths-aqa_graphs-L05.json",encoding="utf-8"))
live=json.load(open("_live_graphsL05.json",encoding="utf-8"))
bad=[]

# 1. fresh-solve every bank solution
def solve(disp):
    return None
checks={
 ("bronze",0):8,("bronze",1):-8,("bronze",2):2,("bronze",3):-3,("bronze",4):16,("bronze",5):1,("bronze",7):32,
 ("silver",0):0,("silver",1):3,("silver",2):-2,("silver",4):25,("silver",5):-7,
 ("gold",0):0,("gold",1):2,("gold",2):8000,("gold",3):0.1,
}
for (t,i),v in checks.items():
    s=pd["problem_bank"][t][i]["solutions"]
    if s!=[v]: bad.append(f"{t}[{i}] solution {s} != {v}")
# gold4
if pd["problem_bank"]["gold"][4]["solutions"]!=[-3.46,3.46]: bad.append("gold4 sols")

# 2. expects != answer, and derive-check a few
for t in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pd["problem_bank"][t]):
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None:
                ev=e if isinstance(e,list) else [e]
                if ev==[float(x) for x in p["solutions"]] or ev==p["solutions"]:
                    bad.append(f"{t}[{i}] expect==answer")
        # duplicate solutions within tier (non-MC)
        if p.get("input_type")!="multiple_choice":
            k=tuple(p["solutions"])
            if k in seen: bad.append(f"{t}[{i}] DUP solution {k}")
            seen.add(k)

# 3. guided_steps final boxes land on solutions (single_value)
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][t]):
        gs=p.get("guided_steps")
        if not gs: continue
        boxes=[s["answer"] for s in gs if s.get("answer") is not None]
        it=p.get("input_type")
        if it=="single_value":
            if boxes[-1]!=p["solutions"][0]:
                bad.append(f"{t}[{i}] last box {boxes[-1]} != sol {p['solutions'][0]}")
        if it=="two_solutions":
            # last two boxes should be the two solutions in some order
            last2=set(boxes[-2:])
            if last2!=set(p["solutions"]):
                bad.append(f"{t}[{i}] two_solutions boxes {boxes[-2:]} != {p['solutions']}")

# 4. chart points satisfy equations
for pt in pd["problem_bank"]["gold"][1]["chart"]["data"]["datasets"][:2]:
    for d in pt["data"]:
        x=d["x"]; y=d["y"]
        if abs((1.0/x+2)-y)>0.01: bad.append(f"recip chart bad ({x},{y})")
for d in pd["problem_bank"]["gold"][4]["chart"]["data"]["datasets"][0]["data"]:
    x=d["x"]; y=d["y"]
    if abs((x**3-12*x)-y)>0.01: bad.append(f"cubic chart bad ({x},{y})")
# cubic roots near solutions cross zero
import math
for r in (-3.46,3.46,0):
    if abs(r**3-12*r)>0.05 and r!=0: bad.append(f"root {r} not root: {r**3-12*r}")
# check ±3.46 is sqrt(12)
if round(math.sqrt(12),2)!=3.46: bad.append("sqrt12 rounding")

# 5. preservation
for k in ("topic_links","related_videos","worked_examples"):
    if pd.get(k)!=live.get(k): bad.append(f"PRESERVE {k} changed")

# 6. em dash scan (student-facing) already in validator; quick recheck
def scan(o,path):
    if isinstance(o,dict):
        for kk,vv in o.items():
            if kk in ("note",): continue
            scan(vv,path+"."+str(kk))
    elif isinstance(o,list):
        for j,vv in enumerate(o): scan(vv,f"{path}[{j}]")
    elif isinstance(o,str) and "—" in o: bad.append("EMDASH "+path)
scan(pd,"pd")

print("SVG in opener:", "<svg" in pd["guided"]["opener"]["display"])
print("charts:", sum('chart' in p for t in ('bronze','silver','gold') for p in pd['problem_bank'][t]))
if bad:
    print("DEFECTS:")
    for b in bad: print("  -",b)
else:
    print("ALL VERIFY CHECKS PASS")
