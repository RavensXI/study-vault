# -*- coding: utf-8 -*-
import json, io, math
pd = json.load(io.open("lesson_physics-calculations-L06@5d1494be41.json", encoding="utf-8"))
errs = []
solve = {
 ("bronze",0): 5*10, ("bronze",1): 80*6, ("bronze",2): 300*0.02,
 ("bronze",3): 6/0.04, ("bronze",4): 70*10, ("bronze",5): 0.5*200*0.05**2,
 ("silver",0): 5/40, ("silver",1): 0.5*40*0.125**2, ("silver",2): (250*12)/30,
 ("silver",3): 0.5*500*(20/500)**2,
 ("gold",0): 2*2/0.10**2, ("gold",1): 2400*5, ("gold",2): math.sqrt(2*(0.5*400*0.30**2)/0.05),
}
pb = pd["problem_bank"]
for (tier,i),val in solve.items():
    stored = pb[tier][i]["solutions"][0]; acc = pb[tier][i].get("accept",0.01)
    if abs(stored-val) > max(acc,0.02):
        errs.append("SOLVE %s[%d] stored %s computed %.4f"%(tier,i,stored,val))
def boxes(steps): return [s for s in steps if s.get("answer") is not None]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if not gs: continue
        pf=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not pf: errs.append("%s[%d] no phase"%(tier,i))
        elif len(boxes(gs[pf[0]:]))<2: errs.append("%s[%d] <2 live"%(tier,i))
checks = {
 ("bronze",1):("wrong_formula",86,80+6),("bronze",2):("unit_error",600,300*2),
 ("bronze",3):("inverse_error",0.24,6*0.04),("bronze",5):("forgot_square",5,0.5*200*0.05),
 ("silver",0):("inverse_error",8,40/5),("silver",1):("forgot_square",2.5,0.5*40*0.125),
 ("silver",2):("forgot_step",3000,250*12),("silver",3):("forgot_square",10,0.5*500*0.04),
 ("gold",0):("forgot_square",40,2*2/0.10),("gold",1):("wrong_force",6000,1200*5),
 ("gold",2):("forgot_step",18,0.5*400*0.30**2),
}
for (tier,i),(pat,exp,commit) in checks.items():
    if abs(exp-commit)>0.001: errs.append("EXPECT %s[%d] %s %s!=%.4f"%(tier,i,pat,exp,commit))
    sol=pb[tier][i]["solutions"][0]
    if abs(exp-sol)<0.011: errs.append("EXPECT %s[%d]==sol"%(tier,i))
    found=[m for m in pb[tier][i]["misconceptions"] if m["pattern"]==pat]
    if not found or found[0].get("expect")!=exp: errs.append("EXPECT %s[%d] %s mismatch"%(tier,i,pat))
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+str(k))
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,path+"[%d]"%j)
    elif isinstance(o,str) and "—" in o: errs.append("EMDASH "+path)
scan(pd,"pd")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        qh=p.get("question","")
        if "<svg" in qh and ('role="img"' not in qh or "aria-label" not in qh):
            errs.append("SVG %s[%d] attrs"%(tier,i))
print("PROBLEMS:" if errs else "ALL CHECKS PASS")
for e in errs: print("  -",e)
if not errs: print("gold[2] v=%.4f stored %s accept %s"%(math.sqrt(720),pb["gold"][2]["solutions"],pb["gold"][2].get("accept")))
