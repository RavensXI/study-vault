# -*- coding: utf-8 -*-
import json, math, re
sind=lambda d:math.sin(math.radians(d)); cosd=lambda d:math.cos(math.radians(d))
R=lambda x:round(x,1)
d=json.load(open("lesson_maths-aqa_geometry-L06.json",encoding="utf-8"))
pb=d["problem_bank"]; errs=[]

# fresh solutions
exp={
 "bronze":[8.9,49.9,21.2,12,9,10,46.8,7.7],
 "silver":[53.1,35.4,15.4,55.2,9.7,28.8,4.4],
 "gold":[[66.7,113.3],8.2,41.8,84,17.3],
}
for t in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pb[t]):
        sol=p["solutions"]; e=exp[t][i]
        e=e if isinstance(e,list) else [e]
        if [float(x) for x in sol]!=[float(x) for x in e]:
            errs.append(f"{t}[{i}] solution {sol} != fresh {e}")
        key=tuple(sol)
        if key in seen and p.get("input_type")!="multiple_choice":
            errs.append(f"{t}[{i}] duplicate solution {sol}")
        seen.add(key)
        # walk continuity: final box lands on a solution value
        gs=p.get("guided_steps") or []
        boxes=[s for s in gs if s.get("answer") is not None]
        if boxes:
            fin=boxes[-1]["answer"]
            # final box should equal a solution or the check value; verify at least one box equals sol[0]
            vals=[b["answer"] for b in boxes]
            if not any(abs(float(v)-float(sol[0]))<0.05 for v in vals):
                errs.append(f"{t}[{i}] no box lands on solution {sol[0]} (boxes {vals})")
        # expects reproduce
        for j,m in enumerate(p.get("misconceptions") or []):
            ev=m.get("expect")
            if ev is not None:
                evl=ev if isinstance(ev,list) else [ev]
                if any(abs(float(a)-float(b))<0.011 for a in evl for b in [float(x) for x in sol]) and len(evl)==len(sol) and all(abs(float(a)-float(b))<0.011 for a,b in zip(evl,[float(x) for x in sol])):
                    errs.append(f"{t}[{i}].misc[{j}] expect==solution")

# independently reproduce each expect from committed error
def close(a,b):return abs(float(a)-float(b))<0.06
checks=[
 ("bronze",0,16.2,12*sind(60)/sind(40)),
 ("bronze",1,25.5,math.degrees(math.asin(9*sind(35)/12))),
 ("bronze",2,42.4,6*10*sind(45)),
 ("bronze",3,24,8*6*sind(30)),
 ("bronze",4,5.4,7*sind(50)/sind(80)),
 ("bronze",5,100,100),
 ("bronze",6,93.5,12*9*sind(60)),
 ("bronze",7,15.5,math.sqrt(149+2*70*cosd(50))),
 ("silver",0,126.9,math.degrees(math.acos(-0.6))),
 ("silver",1,144.6,math.degrees(math.acos((49-144-81)/216))),
 ("silver",2,19.9,math.sqrt(317+308*cosd(75))),
 ("silver",3,110.4,15*11*sind(42)),
 ("silver",4,2.6,5*sind(30)/sind(105)),
 ("silver",5,20.5,math.sqrt(625-600*cosd(110))),
 ("silver",6,7,math.sqrt(34+15)),
 ("gold",1,11.5,math.sqrt(100-96*cosd(110))),
 ("gold",2,19.5,math.degrees(math.asin(40/120))),
 ("gold",3,91,0.5*13*14),
 ("gold",4,10.1,math.sqrt(202-99)),
]
for t,i,claimed,recomputed in checks:
    if not close(claimed,R(recomputed)) and not close(claimed,recomputed):
        errs.append(f"{t}[{i}] expect {claimed} != recomputed {round(recomputed,3)}")

# figure label check: every number shown in svg must be in problem text or a solution
def nums(s): return set(re.findall(r'\d+\.?\d*', s))
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        disp=p["display"]
        if "<svg" not in disp: continue
        svg=disp[:disp.index("</svg>")]
        text=disp[disp.index("</svg>"):]
        # collect text-label numbers inside svg <text>..</text>
        labels=re.findall(r'>([^<]*?)</text>', svg)
        labelnums=set()
        for L in labels:
            labelnums|=set(re.findall(r'\d+\.?\d*', L))
        # allowed = numbers in problem text + solutions
        allowed=nums(text) | {str(x) for x in p["solutions"]} | {str(int(x)) for x in p["solutions"] if float(x)==int(x)}
        for n in labelnums:
            # ignore font-size style leaked? we only grabbed <text> content. degrees etc fine.
            if n not in allowed:
                errs.append(f"{t}[{i}] svg label '{n}' not in problem text/solutions (labels={sorted(labelnums)}, allowed={sorted(allowed)})")

print("ERRORS:",len(errs))
for e in errs: print("  -",e)
if not errs: print("CHECKER CLEAN")
