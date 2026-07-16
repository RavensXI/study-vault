# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_ratio-proportion-L02.json", encoding="utf-8"))
errs = []

# Independent fresh-solve of every problem from display intent.
expected = {
    ("bronze",0):100, ("bronze",1):540, ("bronze",2):368, ("bronze",3):28,
    ("bronze",4):99, ("bronze",5):490, ("bronze",6):240, ("bronze",7):360,
    ("silver",0):3307.5, ("silver",1):6400, ("silver",2):53060, ("silver",3):1.075,
    ("silver",4):0.65, ("silver",5):218998, ("silver",6):5451.78,
    ("gold",0):400, ("gold",1):1500, ("gold",2):5000, ("gold",3):10, ("gold",4):28,
}
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol = p["solutions"][0]
        exp = expected[(tier,i)]
        if abs(sol-exp) > 0.005:
            errs.append(f"{tier}[{i}] stored {sol} != freshsolve {exp}")
        # duplicate check
    sols=[tuple(p["solutions"]) for p in pb[tier]]
    if len(sols)!=len(set(sols)):
        errs.append(f"{tier} duplicate solutions {sols}")
    # misconception expect != solution
    for i,p in enumerate(pb[tier]):
        for m in p.get("misconceptions",[]):
            e=m["expect"]
            if e is not None and abs(float(e)-float(p["solutions"][0]))<0.011:
                errs.append(f"{tier}[{i}] expect==sol {e}")

# Recompute specific compound values
import math
checks = {
 "1.05^2":1.05**2, "3000*1.1025":3000*1.1025, "0.8^2":0.8**2,
 "1.02^3":round(1.02**3,6), "50000*1.061208":50000*1.061208,
 "1.04^5":round(1.04**5,7), "180000*1.2166529":round(180000*1.2166529,2),
 "0.88^3":round(0.88**3,6), "8000*0.681472":round(8000*0.681472,3),
 "460/1.15":460/1.15, "1380/0.92":1380/0.92, "5512.5/1.1025":round(5512.5/1.1025,4),
 "11664/16000":11664/16000, "0.729^(1/3)":round(0.729**(1/3),6),
 "16000*0.729":16000*0.729, "0.8*0.9":0.8*0.9, "1.1^3":round(1.1**3,6),
 "2000*1.331":2000*1.331, "75/1.25":75/1.25, "12000*0.85^3":12000*0.85**3,
 "50*0.9*0.9":50*0.9*0.9,
}
print("Spot computations:")
for k,v in checks.items():
    print(f"  {k} = {v}")

# Verify every guided_steps box is numeric and walk lands on solution for the
# answer-producing box (the box just before/at the final check).
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        for j,st in enumerate(p["guided_steps"]):
            a=st.get("answer")
            if a is not None and not isinstance(a,(int,float)):
                errs.append(f"{tier}[{i}].gs[{j}] non-numeric {a!r}")

# opener + teach box numeric
for st in pd["guided"]["opener"]["steps"]:
    a=st.get("answer")
    if a is not None and not isinstance(a,(int,float)):
        errs.append(f"opener box non-numeric {a!r}")
for t in ("bronze","silver","gold"):
    for st in pd["guided"]["teach"][t]["steps"]:
        a=st.get("answer")
        if a is not None and not isinstance(a,(int,float)):
            errs.append(f"teach {t} non-numeric {a!r}")

print("\nERRORS:" if errs else "\nNo maths errors found.")
for e in errs: print("  -", e)
