# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_higher-calculations-L01@146c1cc6d7.json", encoding="utf-8"))
pb = pd["problem_bank"]
prob=[]
# independent fresh-solve of each problem -> expected answer
solves = {
 "bronze":[0.1*0.025, 0.5/0.25, 0.2/0.5, 4.0/40, 0.15/0.5, 0.25*0.1, 50/1000, round(2.0/36.5,4)],
 "silver":[
    (0.125*0.02)/0.025,                       # S0 1:1
    (0.2*0.025/2)/0.02,                        # S1 1:2
    (0.15*0.025)/0.01875,                      # S2 1:1
    (0.15*0.025*2)/0.02,                       # S3 Ca(OH)2 1:2 -> 0.375
    (0.2*0.025)/0.02,                          # S4 1:1 -> 0.25
    (0.5*0.025/2)/0.0125,                      # S5 -> 0.5
 ],
 "gold":[
    ((2.0/40)/0.2*0.025)/0.03125,              # G0 -> 0.2
    ((5.3/106)/0.25*0.025*2)/0.025,            # G1 -> 0.4
    round(0.5*0.25*36.5,4),                    # G2 -> 4.5625 -> 4.6
    ((0.1*0.02)/0.025*0.5)*56,                 # G3 -> 2.24
    ((0.2*0.02)/0.025*0.25)*40,                # G4 -> 1.6
    ((0.1*0.0125)/0.025*0.5)*106,              # G5 -> 2.65
 ],
}
bad=0
for tier in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]; mine=solves[tier][i]
        acc=p.get("accept",0.005)
        ok = abs(sol-mine)<=max(acc,1e-9)+1e-9
        # G2 rounding special
        if tier=="gold" and i==2: ok = abs(4.6-sol)<1e-9 and abs(mine-4.5625)<1e-4
        if not ok:
            print(f"  ANSWER MISMATCH {tier}[{i}] stored={sol} mine={mine}"); bad+=1
        # duplicate within tier
        seen.setdefault(sol,[]).append(i)
        # last computing box lands on/near sol (exclude check boxes): verify a final-answer box exists == sol
        gs=p["guided_steps"]
        boxvals=[s["answer"] for s in gs if s.get("answer") is not None]
        if sol not in [round(b,6) for b in boxvals] and not (tier=="gold" and i==2):
            print(f"  WALK no box equals solution {tier}[{i}] sol={sol} boxes={boxvals}"); bad+=1
        # misconception expects outside accept window
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is None: continue
            if abs(e-sol)<=acc:
                print(f"  DEAD EXPECT {tier}[{i}].mc[{j}] expect={e} sol={sol} accept={acc}"); bad+=1
    dups={k:v for k,v in seen.items() if len(v)>1}
    if dups: print(f"  DUPLICATE SOLUTIONS in {tier}: {dups}"); bad+=1
    print(f"{tier}: solutions {[p['solutions'][0] for p in pb[tier]]}")

# board neutrality scan
import re
blob=json.dumps(pd,ensure_ascii=False).lower()
for term in ["aqa","edexcel"," ocr","equation sheet","must memorise","must memorize","on your sheet","given in the exam"]:
    if term in blob: print("  BOARD TERM FOUND:",term); bad+=1
# em dash
if "—" in json.dumps(pd,ensure_ascii=False):
    # allow in note fields only
    def scan(o,p):
        g=0
        if isinstance(o,dict):
            for k,v in o.items():
                if k in ("note",): continue
                g+=scan(v,p+"."+k)
        elif isinstance(o,list):
            for i,v in enumerate(o): g+=scan(v,f"{p}[{i}]")
        elif isinstance(o,str) and "—" in o: print("  EMDASH",p); return 1
        return g
    bad+=scan(pd,"pd")

print("\nBOARD/DUP/EXPECT/WALK ISSUES:",bad)
print("OK" if bad==0 else "REVIEW NEEDED")
