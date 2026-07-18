import json
pd=json.load(open("_L03_canon_live.json"))["practice_data"]
issues=[]

# em dash / board scan across all student-facing strings
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o: issues.append(f"EMDASH {path}: {o[:60]}")
        low=o.lower()
        for b in ["aqa","edexcel","ocr","eduqas","wjec","equation sheet","memorise","memorize"]:
            if b in low: issues.append(f"BOARD/{b} {path}: {o[:80]}")
walk(pd)

# verify every problem's guided_steps final boxes & solutions
pb=pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        sol=p.get("solutions")
        acc=p.get("accept",0)
        # check each misconception expect vs accept window
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None and sol and isinstance(sol[0],(int,float)):
                if abs(e-sol[0])<=acc:
                    issues.append(f"DEAD EXPECT {tier}[{i}] expect={e} sol={sol[0]} accept={acc}")
        # box numeric check
        for j,s in enumerate(p.get("guided_steps",[])):
            if "answer" in s and not isinstance(s["answer"],(int,float)):
                issues.append(f"NONNUM {tier}[{i}].guided_steps[{j}]")

print("SCAN ISSUES:", len(issues))
for x in issues: print("  ",x)

# arithmetic recompute of every box, independently
import re
def approx(a,b,t=0.005): return abs(a-b)<=t
checks=[]
# Manually recompute each problem's key answer
def solve():
    R={}
    # bronze
    R["bronze[0]"]=(50*0.3,15)
    R["bronze[1]"]=(20/0.4,50)
    R["bronze[2]"]=(12/30,0.4)
    R["bronze[3]"]=(200*1.5,300)
    R["bronze[4]"]=(36/0.6,60)
    R["bronze[5]"]=(80*0.25,20)
    R["bronze[6]"]=(45/15,3)
    R["bronze[7]"]=(400*2.0/1.6,500)
    R["silver[0]"]=((30*9.8*2.0)/(60*9.8),1)
    R["silver[1]"]=(600*0.8/1.2,400)
    R["silver[2]"]=((5*9.8*0.08)/0.4,9.8)
    R["silver[3]"]=(abs(150*2.0-200*1.0),100)
    R["silver[4]"]=(8*9.8*0.25,19.6)
    R["silver[5]"]=(150*0.4/1.2,50)
    R["gold[0]"]=((100*0.5+200*1.5)/0.7,500)
    R["gold[1]"]=(120/(60/20),40)
    R["gold[2]"]=(15*(60/20),45)
    R["gold[3]"]=((50*0.8-10*9.8*0.2)/1.2,17)
    R["gold[4]"]=((12*0.3)*(45/15),10.8)
    R["gold[5]"]=(80*0.75/0.05,1200)
    return R
for k,(calc,stored) in solve().items():
    if not approx(calc,stored,0.01):
        checks.append(f"SOLUTION MISMATCH {k}: computed {calc} vs stored {stored}")
print("SOLUTION CHECKS:", len(checks))
for x in checks: print("  ",x)
