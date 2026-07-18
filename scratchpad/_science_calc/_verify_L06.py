# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_higher-calculations-L06@e6541c99e0.json", encoding="utf-8"))
pb = pd["problem_bank"]
issues = []
def close(a,b,tol): return abs(a-b)<=tol
expected = {
 "bronze":[23.0,2000,460,24,0],
 "silver":[8000,48/230,12500,230000/11000,3/9],
 "gold":[25000*40000/200,25000*500/5000000,2.5**2*2,(60/0.85)/230],
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]; exp=expected[tier][i]; acc=p.get("accept",0.005)
        if p["input_type"]=="multiple_choice":
            print(f"{tier}[{i}] MC sol={sol} OK"); continue
        if not close(float(sol),exp,max(acc,0.02)):
            issues.append(f"{tier}[{i}] stored {sol} vs fresh {exp:.4f}")
        else:
            print(f"{tier}[{i}] sol={sol} fresh={exp:.4f} acc={acc} unit={p.get('unit')!r} OK")
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None and abs(float(e)-float(sol))<=acc:
                issues.append(f"{tier}[{i}] expect {e} inside accept of {sol}")
assert round(48/230,3)==0.209
assert 11000*20.9/1000==229.9
assert round(3/9,3)==0.333
assert round(60/0.85,1)==70.6 and round(70.6/230,3)==0.307 and round(60/70.6,2)==0.85
assert 40000/200==200 and 25000*200==5000000
assert 25000*500==12500000 and 12500000/5000000==2.5
assert 2000/20==100 and 2000/2000==1
assert 40000000/40000==1000 and 1000000*6==6000000
print("\nASSERTIONS PASSED")
print("ISSUES:", issues if issues else "NONE")
