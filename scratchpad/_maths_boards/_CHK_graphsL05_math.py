# -*- coding: utf-8 -*-
import json,math
live=json.load(open("_CHK_graphsL05_LIVE.json",encoding="utf-8"))
pb=live["problem_bank"]
issues=[]

# Independent fresh-solve of each bank problem (by hand-coded truth)
truth={
 ("bronze",0):[8],("bronze",1):[-8],("bronze",2):[2],("bronze",3):[-3],
 ("bronze",4):[16],("bronze",5):[1],("bronze",6):[0],("bronze",7):[32],
 ("silver",0):[0],("silver",1):[3],("silver",2):[-2],("silver",3):[0],
 ("silver",4):[25],("silver",5):[-7],("silver",6):[0],
 ("gold",0):[0],("gold",1):[2],("gold",2):[8000],("gold",3):[0.1],
 ("gold",4):[-3.46,3.46],
}
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        exp=truth[(tier,i)]
        got=p["solutions"]
        if got!=exp:
            issues.append(f"SOLUTION {tier}[{i}] display={p['display'][:60]} stored={got} expected={exp}")
        # calculator:false must be clean (int or simple)
        if p.get("calculator")==False:
            for s in got:
                if isinstance(s,float) and abs(s-round(s))>1e-9 and s not in (0.1,0.5,0.25):
                    issues.append(f"MESSY {tier}[{i}] noncalc value {s}")

# verify guided_steps final boxes land on solution & each box recomputed manually
# spot check: recompute chart points
def check_chart(tier,i,fn,tol=0.01):
    p=pb[tier][i]
    ch=p.get("chart")
    if not ch: return
    for ds in ch["data"]["datasets"]:
        lbl=ds.get("label","")
        if lbl.startswith("asymptote") or "asymptote" in lbl: continue
        for pt in ds["data"]:
            x=pt["x"]; y=pt["y"]
            fy=fn(x)
            if fy is None: continue
            if abs(fy-y)>tol:
                issues.append(f"CHART {tier}[{i}] x={x} stored y={y} computed {round(fy,3)}")

# gold[1]: y=1/x+2 (two branches). label 'y = 1/x + 2' and second unlabeled branch same fn
check_chart("gold",1,lambda x: 1.0/x+2 if x!=0 else None)
# gold[4]: y=x^3-12x
check_chart("gold",4,lambda x: x**3-12*x)

# verify misconception expects reproduce
def expect(tier,i):
    return pb[tier][i]["misconceptions"]
mc_checks={
 ("bronze",0,0):6, ("bronze",1,0):8, ("bronze",2,0):0.5,("bronze",3,0):3,
 ("bronze",4,0):8, ("bronze",5,0):0, ("bronze",7,0):10,
 ("silver",0,0):-2,("silver",1,0):8,("silver",2,0):2,("silver",4,0):10,("silver",5,0):9,
 ("gold",0,0):36,("gold",1,0):0,("gold",2,0):4000,("gold",3,0):-10,("gold",4,0):[-6,6],
}
for (tier,i,mi),ev in mc_checks.items():
    got=pb[tier][i]["misconceptions"][mi]["expect"]
    if got!=ev:
        issues.append(f"EXPECT {tier}[{i}].misconceptions[{mi}] stored={got} recomputed={ev}")

# verify guided_steps land on solutions
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        if p["input_type"]=="multiple_choice": continue
        gs=p.get("guided_steps",[])
        boxes=[s for s in gs if "answer" in s]
        if not boxes:
            issues.append(f"NOGUIDED {tier}[{i}]")
            continue
        final=boxes[-1]["answer"]
        sol=p["solutions"]
        # final box should equal a solution value (for single)
        if p["input_type"]=="single_value":
            if abs(final-sol[0])>1e-9:
                issues.append(f"GUIDED-END {tier}[{i}] final box {final} != sol {sol[0]}")

print("ISSUES:",len(issues))
for x in issues: print(" -",x)
if not issues: print("ALL MATHS CHECKS PASS")
