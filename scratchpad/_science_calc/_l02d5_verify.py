# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_physics-calculations-L02@d5abd25397.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# independent fresh solves keyed by (tier,i) -> expected solution(s)
solve = {
 ("bronze",0): 1600/2000,
 ("bronze",1): 350/500*100,
 ("bronze",2): 7/10,
 ("bronze",3): 12000/40000*100,
 ("bronze",4): 0.9*200000,
 ("bronze",5): 0.35*800,
 ("bronze",6): 80-8,
 ("bronze",7): "mc:1",
 ("silver",0): (5000-1500-500)/5000*100,
 ("silver",1): 720/0.40,
 ("silver",2): 46000/0.92-46000,
 ("silver",3): 0.85*(8000*9.8*50),
 ("silver",4): 750-0.60*750,
 ("silver",5): 1000-350-500,
 ("gold",0): (120*9.8*20)/0.75,
 ("gold",1): (0.5*1200*25**2)/0.30,
 ("gold",2): (240/0.20)/800,
 ("gold",3): (0.70*600*300)/(9.8*8),
 ("gold",4): "mc:0",
 ("gold",5): "mc:2",
}
for tier in ("bronze","silver","gold"):
    for i,pr in enumerate(pb[tier]):
        exp = solve[(tier,i)]
        sol = pr["solutions"]
        acc = pr.get("accept", 0.005)
        if isinstance(exp,str):
            want=int(exp.split(":")[1])
            if sol!=[want]: errs.append(("SOL",tier,i,sol,exp))
            continue
        if abs(sol[0]-exp) > max(acc,0.01):
            errs.append(("SOL",tier,i,sol[0],"calc",round(exp,4)))
        # expects outside accept window
        for j,m in enumerate(pr.get("misconceptions") or []):
            e=m.get("expect")
            if e is not None and isinstance(e,(int,float)):
                if abs(e-sol[0]) <= acc:
                    errs.append(("EXPECT_INSIDE",tier,i,j,e,sol[0],acc))

# recompute every guided_steps / teach / opener box by evaluating pre arithmetic where possible
import re
def check_boxes(steps,label):
    for k,st in enumerate(steps):
        if st.get("answer") is None: continue
        pre=st.get("pre","")
        # extract last "A op B = " arithmetic on the pre
        m=re.findall(r'([0-9][0-9,\.]*)\s*([×x*÷/\-−+])\s*([0-9][0-9,\.]*)\s*=\s*$',pre.replace('  ',' '))
        # fallthrough: try find "= " expression
        ans=st["answer"]
        # try a simple two-operand eval from pre
        mm=re.search(r'([0-9][0-9,\.]*)\s*([×÷\-−+])\s*([0-9][0-9,\.]*)\s*=\s*$',pre)
        if mm:
            a=float(mm.group(1).replace(',',''));op=mm.group(2);b=float(mm.group(3).replace(',',''))
            v={'×':a*b,'÷':a/b,'−':a-b,'-':a-b,'+':a+b}[op]
            if abs(v-ans)>0.05:
                errs.append(("BOX",label,k,pre.strip(),ans,round(v,4)))

for tier in ("bronze","silver","gold"):
    for i,pr in enumerate(pb[tier]):
        if pr.get("guided_steps"): check_boxes(pr["guided_steps"],"%s[%d].gs"%(tier,i))
check_boxes(pd["guided"]["opener"]["steps"],"opener")
for t in ("bronze","silver","gold"):
    check_boxes(pd["guided"]["teach"][t]["steps"],"teach.%s"%t)

# check squared box g1: 25²=625 (not matched by regex) verify manually
if pb["gold"][1]["guided_steps"][1]["answer"]!=625: errs.append(("BOX_SQ","g1",625))

if errs:
    print("ERRORS:")
    for e in errs: print("  ",e)
else:
    print("ALL CLEAN: solutions, expects-outside-accept, and boxes verified")
