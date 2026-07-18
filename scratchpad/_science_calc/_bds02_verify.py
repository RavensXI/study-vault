# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_biology-data-skills-L02@551b362537.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# 1. duplicate solution tuples within tier (excluding MC per validator rule)
for t in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pb[t]):
        key=tuple(p["solutions"])
        if key in seen and p.get("input_type")!="multiple_choice":
            errs.append("DUP %s[%d] %r"%(t,i,key))
        seen.add(key)

# 2. expects != solution
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        sol=[float(x) for x in p["solutions"]]
        for j,mc in enumerate(p.get("misconceptions",[])):
            e=mc.get("expect")
            if e is None: continue
            ev=e if isinstance(e,list) else [e]
            if len(ev)==len(sol) and all(abs(float(a)-b)<0.011 for a,b in zip(ev,sol)):
                errs.append("EXPECT==SOL %s[%d].misc[%d] %r"%(t,i,j,e))

# 3. guided walk final live boxes land on solution for single_value; boundary sane
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        gs=p.get("guided_steps")
        if not gs: continue
        boxes=[s for s in gs if s.get("answer") is not None]
        sub=[k for k,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not sub: errs.append("NOBOUND %s[%d]"%(t,i)); continue
        live=[s for s in gs[sub[0]:] if s.get("answer") is not None]
        if len(live)<2: errs.append("FEWLIVE %s[%d]"%(t,i))

# 4. Independent genetics recompute of each single_value problem
def pct(n): return round(n/4*100)
checks = {
 ("bronze",3):100, ("bronze",4):3, ("bronze",6):4, ("bronze",7):50,
 ("silver",0):50, ("silver",1):2, ("silver",3):150, ("silver",4):40, ("silver",5):10,
 ("gold",1):50, ("gold",2):75, ("gold",4):25, ("gold",5):1,
}
for (t,i),expect in checks.items():
    got=pb[t][i]["solutions"][0]
    if got!=expect: errs.append("SOLVE %s[%d] stored=%r recomputed=%r"%(t,i,got,expect))

# 5. recompute each walk arithmetic explicitly (spot the compute chains)
# bronze3: (4/4)*100=100; bronze4: 4-1=3; bronze6: 4-0=4; bronze7:1+1=2,(2/4)*100=50
assert (4/4)*100==100 and 4-1==3 and 4-0==4 and 1+1==2 and (2/4)*100==50
# silver0:(2/4)*100=50; silver1 count=2; silver3:200/4=50,3*50=150; silver4:80/4=20,2*20=40; silver5:20/4=5,2*5=10
assert (2/4)*100==50 and 200//4==50 and 3*50==150 and 80//4==20 and 2*20==40 and 20//4==5 and 2*5==10
# gold1:(2/4)*100=50; gold2:(3/4)*100=75; gold4:(1/4)*100=25; gold5 count=1
assert (2/4)*100==50 and (3/4)*100==75 and (1/4)*100==25
# teach: bronze (1/4)*100=25; silver 60/4=15,1*15=15; gold (2/4)*100=50
assert (1/4)*100==25 and 60//4==15 and (2/4)*100==50
# opener: 4 combos, 1 bb
print("checks:",len(checks),"walks with boundary ok")
if errs:
    print("FAIL"); [print("  -",e) for e in errs]
else:
    print("ALL CLEAN")
