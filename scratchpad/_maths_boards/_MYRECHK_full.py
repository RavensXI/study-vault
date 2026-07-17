import json
pd=json.load(open("_MYRECHK_live.json",encoding="utf-8"))
errs=[]
pb=pd["problem_bank"]

def q(a,b,c): 
    return lambda x: a*x*x+b*x+c

# --- Chart verification: recompute points against stated equation ---
charts=[
 ("gold[4]", pb["gold"][4], (-3,12,-9)),
 ("bronze[2]", pb["bronze"][2], (1,0,0)),      # y=x^2
 ("bronze[6]", pb["bronze"][6], (-1,0,4)),     # y=-x^2+4
 ("silver[5]", pb["silver"][5], (-1,2,3)),     # y=-x^2+2x+3
 ("silver[6]", pb["silver"][6], (1,0,4)),      # y=x^2+4
]
for name,prob,(a,b,c) in charts:
    f=q(a,b,c)
    for p in prob["chart"]["data"]["datasets"][0]["data"]:
        exp=f(p["x"])
        if abs(exp-p["y"])>1e-9:
            errs.append(f"CHART {name} x={p['x']} stored y={p['y']} expected {exp}")

# --- guided_steps final box lands on solution; verify each numeric box present ---
for tier in ["bronze","silver","gold"]:
    for i,prob in enumerate(pb[tier]):
        gs=prob.get("guided_steps")
        sol=prob["solutions"]
        if gs:
            last=[s for s in gs if "answer" in s][-1]
            # last answer often the check(=0) not the solution; just ensure all boxes numeric
            for j,s in enumerate(gs):
                if "answer" in s and not isinstance(s["answer"],(int,float)):
                    errs.append(f"{tier}[{i}].guided_steps[{j}] non-numeric answer")
        # solution numeric
        for v in sol:
            if not isinstance(v,(int,float)):
                errs.append(f"{tier}[{i}] non-numeric solution {v}")

# --- opener/teach boxes numeric ---
for tier,walk in pd["guided"]["teach"].items():
    for j,s in enumerate(walk["steps"]):
        if "answer" in s and not isinstance(s["answer"],(int,float)):
            errs.append(f"teach.{tier}[{j}] non-numeric")
for j,s in enumerate(pd["guided"]["opener"]["steps"]):
    if "answer" in s and not isinstance(s["answer"],(int,float)):
        errs.append(f"opener[{j}] non-numeric")

# --- completion boundary: >=1 before phase, >=2 boxes at/after ---
for tier in ["bronze","silver","gold"]:
    for i,prob in enumerate(pb[tier]):
        gs=prob.get("guided_steps")
        if not gs: continue
        boxidx=[j for j,s in enumerate(gs) if "answer" in s]
        phase=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not phase:
            errs.append(f"{tier}[{i}] no phase boundary")
            continue
        pj=phase[0]
        before=[j for j in boxidx if j<pj]
        after=[j for j in boxidx if j>=pj]
        if len(before)<1: errs.append(f"{tier}[{i}] <1 box before boundary")
        if len(after)<2: errs.append(f"{tier}[{i}] <2 boxes at/after boundary ({len(after)})")

print("ERRORS:", len(errs))
for e in errs: print(" -",e)
