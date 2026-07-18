# -*- coding: utf-8 -*-
import json, re
pd=json.load(open("lesson_physics-calculations-L03@330faf0468.json",encoding="utf-8"))
problems=0; errs=[]

def evalexpr(e):
    e=e.replace("×","*").replace("÷","/").replace("−","-").replace("·","*")
    e=e.replace("−","-")
    return eval(e,{"__builtins__":{}})

# check every guided box whose pre ends with "<expr> = "
box_re=re.compile(r"([-\d.,]+\s*[×÷+\-*/]\s*[-\d.,()]+(?:\s*[×÷+\-*/]\s*[-\d.,()]+)*)\s*=\s*$")
def check_walk(steps,label):
    for i,st in enumerate(steps):
        if st.get("answer") is None: continue
        pre=st.get("pre","")
        m=box_re.search(pre.replace(",",""))
        if m:
            try:
                val=evalexpr(m.group(1))
                if abs(val-st["answer"])>0.005:
                    errs.append(f"{label}[{i}] pre '{pre.strip()}' computes {val} != answer {st['answer']}")
            except Exception as ex:
                errs.append(f"{label}[{i}] eval fail '{m.group(1)}': {ex}")

# fresh-solve expected answers (author's independent solve)
expect_sol={
 ("bronze",0):36,("bronze",1):30,("bronze",2):10,("bronze",3):12,("bronze",4):0.3,("bronze",5):4,
 ("silver",0):12,("silver",1):0.5,("silver",2):3,("silver",3):0.05,("silver",4):30,
 ("gold",0):30,("gold",1):100,("gold",2):0.3,("gold",3):60,
}
for tier in ["bronze","silver","gold"]:
    seen=set()
    for i,p in enumerate(pd["problem_bank"][tier]):
        problems+=1
        sol=p["solutions"][0]
        if abs(sol-expect_sol[(tier,i)])>1e-9:
            errs.append(f"{tier}[{i}] stored {sol} != fresh {expect_sol[(tier,i)]}")
        key=tuple(p["solutions"])
        if key in seen: errs.append(f"{tier}[{i}] DUP solution {key}")
        seen.add(key)
        check_walk(p["guided_steps"],f"{tier}[{i}].gs")
        # expects
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is not None and abs(float(e)-float(sol))<0.011:
                errs.append(f"{tier}[{i}].mc[{j}] expect {e} == solution {sol}")
        # svg numbers present in text? check resistor/voltage labels appear in text
# walks in opener + teach
check_walk(pd["guided"]["opener"]["steps"],"opener")
for t in ["bronze","silver","gold"]:
    check_walk(pd["guided"]["teach"][t]["steps"],f"teach.{t}")

# expect error re-derivation (manual map): confirm each expect equals the committed error
exp_checks={
 ("bronze",0,0):3/12, ("bronze",1,0):9*0.3, ("bronze",2,0):0.5/20, ("bronze",3,0):1/(1/7+1/5),
 ("bronze",4,0):12*40, ("bronze",5,0):25/100,
 ("silver",0,0):1/(1/4+1/6+1/2), ("silver",1,0):6*12, ("silver",2,0):0.5/6, ("silver",3,0):12*240, ("silver",4,0):15/2,
 ("gold",0,0):60, ("gold",1,0):200, ("gold",2,0):9/75, ("gold",2,1):9/45, ("gold",3,0):12, ("gold",3,1):2400*5,
}
for (tier,i,j),val in exp_checks.items():
    stored=pd["problem_bank"][tier][i]["misconceptions"][j].get("expect")
    if stored is None:
        errs.append(f"{tier}[{i}].mc[{j}] expect is None but check expects ~{val}")
    elif abs(float(stored)-val)>0.02:
        errs.append(f"{tier}[{i}].mc[{j}] expect {stored} != derived error {round(val,3)}")

# em-dash scan
EM="—"
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,path+f"[{i}]")
    elif isinstance(o,str) and EM in o:
        errs.append(f"EMDASH {path}")
scan(pd,"pd")

print("problems:",problems)
if errs:
    print("ERRORS",len(errs))
    for e in errs: print("  -",e)
else:
    print("ALL CHECKS PASS: answers, boxes, expects, dedup, em-dashes")
