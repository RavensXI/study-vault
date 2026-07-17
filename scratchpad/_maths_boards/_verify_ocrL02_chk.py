# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_maths-ocr_ratio-proportion-L02.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []
def r2(x): return round(x,2)
expected = {
 "bronze": [220,120,15,36,1.05,0.7,20,450],
 "silver": [r2(510/1.15),150,10800,70,5100,576,20],
 "gold":   [r2(3000*1.04**2),round(15000*0.88**3),r2(1102.5/1.05**2),5,r2(500*1.06**2-500)],
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]
        if abs(sol-expected[tier][i])>0.011:
            errs.append(f"{tier}[{i}] stored {sol} != fresh {expected[tier][i]}")
        vals=[b["answer"] for b in p["guided_steps"] if b.get("answer") is not None]
        if not any(abs(v-sol)<0.011 for v in vals):
            errs.append(f"{tier}[{i}] no guided box hits solution {sol}; boxes={vals}")
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m["expect"]
            if e is not None and abs(e-sol)<0.011:
                errs.append(f"{tier}[{i}].misc[{j}] expect==sol")
checks = {
 ("bronze",0):[(20,200*0.10)], ("bronze",1):[(30,150*0.20)], ("bronze",2):[(45,60*0.75)],
 ("bronze",3):[(4,40*0.10)], ("bronze",4):[(0.05,0.05)], ("bronze",5):[(0.3,0.3)],
 ("bronze",6):[(10,60-50),(16.67,r2((60-50)/60*100))], ("bronze",7):[(150,300*0.50)],
 ("silver",0):[(433.5,510*0.85)], ("silver",1):[(50,1000*0.05),(1150,1000+150)],
 ("silver",2):[(1200,12000*0.10)], ("silver",3):[(67.2,56*1.2)], ("silver",4):[(100,5000*0.02)],
 ("silver",5):[(96,480*0.20)], ("silver",6):[(16,80-64),(25,r2((80-64)/64*100))],
 ("gold",0):[(3240,3000+3000*0.04*2)], ("gold",1):[(9600,15000*0.64)], ("gold",2):[(1050,r2(1102.5/1.05))],
 ("gold",3):[(4,4)], ("gold",4):[(561.8,r2(500*1.06**2)),(60,500*0.06*2)],
}
for (tier,i),lst in checks.items():
    stored=[m["expect"] for m in pb[tier][i].get("misconceptions",[])]
    for k,(claimed,computed) in enumerate(lst):
        if abs(claimed-computed)>0.011:
            errs.append(f"{tier}[{i}] expect claimed {claimed} != committed-error {computed}")
        if k<len(stored) and stored[k] is not None and abs(stored[k]-claimed)>0.011:
            errs.append(f"{tier}[{i}] stored expect {stored[k]} != planned {claimed}")
g4msg=pb["gold"][3]["misconceptions"][0]["message"]
if "7082" not in g4msg or "6870" not in g4msg: errs.append("G4 msg missing 7082/6870")
if "7048" in g4msg or "6837" in g4msg: errs.append("G4 msg still has old numbers")
fresh=json.load(io.open("_fresh_L02.json",encoding="utf-8"))
for f in ("topic_links","related_videos","worked_examples"):
    if json.dumps(pd[f],sort_keys=True)!=json.dumps(fresh[f],sort_keys=True):
        errs.append(f"preservation: {f} changed")
op=pd["guided"]["opener"]["steps"]
if op[0]["answer"]!=30 or op[2]["answer"]!=24: errs.append("opener answers")
print("ERRORS:" if errs else "ALL CLEAN")
for e in errs: print("  -",e)
