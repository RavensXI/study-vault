# Independent recompute of every solution, box chain, and misconception expect.
import json
pd=json.load(open("_CHKR_L04g_pd.json",encoding="utf-8"))
errs=[]

# Fresh-solve each bank problem from first principles (hard-coded from display text)
expected_solutions={
 "gold":[105,5,30,20,40],
 "bronze":[60,1,40,30,20,24,4,90],
 "silver":[5,140,8,60,230,120,25],
}
pb=pd["problem_bank"]
for tier in ("gold","bronze","silver"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"]
        exp=expected_solutions[tier][i]
        if sol!=[exp]:
            errs.append(f"{tier}[{i}] solution {sol} != fresh {exp}")
        # verify final guided box equals solution
        gs=p.get("guided_steps") or []
        boxes=[s["answer"] for s in gs if s.get("answer") is not None]
        # the solution should appear among boxes (final answer box)
        if exp not in boxes:
            errs.append(f"{tier}[{i}] solution {exp} not reached by any guided box {boxes}")

# Misconception expects: recompute the committed error
def near(a,b): return abs(a-b)<1e-6
checks=[
 ("gold",0,150, 4*10+6*10+5*10),           # forget half on triangles
 ("gold",1,180, 30*6),
 ("gold",2,12, 60/5),
 ("gold",3,10, 80/8),
 ("gold",4,2.5, 10/4),
 ("bronze",0,90, 90),
 ("bronze",1,3, 3),
 ("bronze",2,0.025, 3/120),
 ("bronze",3,7.5, 15/2),
 ("bronze",4,0.05, 2.5/50),
 ("bronze",5,9.375, 15/8*5),
 ("bronze",6,0.25, 200/800),
 ("bronze",7,40, 60/1.5),
 ("silver",0,0.2, 5/25),
 ("silver",1,200, 10*20),
 ("silver",2,0.125, 3/24),
 ("silver",3,90, 90),
 ("silver",4,200, 200),
 ("silver",5,60, 0.5*8*15),
 ("silver",6,64, 40/5*8),
]
for tier,i,stored,recomputed in checks:
    m=pb[tier][i]["misconceptions"][0]
    if not near(float(m["expect"]),stored):
        errs.append(f"{tier}[{i}] expect stored {m['expect']} != {stored}")
    if not near(stored,recomputed):
        errs.append(f"{tier}[{i}] committed-error recompute {recomputed} != stored expect {stored}")

# Teach walks arithmetic
teach=pd["guided"]["teach"]
tb={t:[s["answer"] for s in teach[t]["steps"] if s.get("answer") is not None] for t in teach}
if tb["gold"]!=[40,200,60,300]: errs.append(f"gold teach boxes {tb['gold']}")
if tb["bronze"]!=[45,45,135,225]: errs.append(f"bronze teach boxes {tb['bronze']}")
if tb["silver"]!=[4,32,128,160]: errs.append(f"silver teach boxes {tb['silver']}")
# verify: gold 0.5*4*20=40,10*20=200,0.5*6*20=60,sum300
assert 0.5*4*20==40 and 10*20==200 and 0.5*6*20==60 and 40+200+60==300
assert 90/2==45 and 45*3==135 and 90+135==225
assert (16-0)/4==4 and 0.5*4*16==32 and 8*16==128 and 32+128==160

# Opener
ob=[s["answer"] for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if ob!=[30,1,3]: errs.append(f"opener boxes {ob}")

print("ERRORS:",len(errs))
for e in errs: print("  -",e)
