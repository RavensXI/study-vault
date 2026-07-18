# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("lesson_physics-calculations-L08@d964afae07.json", encoding="utf-8"))
errs=[]
# Fresh-solve each problem independently
def close(a,b,tol=1e-6): return abs(a-b)<=tol
expected = {
 ("bronze",0):("F=ma",5*4,20),
 ("bronze",1):("F=ma",1200*3,3600),
 ("bronze",2):("v=fl",5*0.04,0.2),
 ("bronze",3):("l=v/f",340/170,2),
 ("bronze",4):("a=F/m",600/200,3),
 ("bronze",5):("p=mv",70*5,350),
 ("silver",0):("f=v/l",3e8/300,1000000),
 ("silver",1):("dp=mdv",1000*20,20000),
 ("silver",2):("m=F/a",1500/2.5,600),
 ("silver",3):("F=dp/dt",900/0.05,18000),
 ("gold",0):("F=dp/dt",900/0.25,3600),
 ("gold",1):("impulse",(120*0.5)/60,1),
 ("gold",2):("cons",6/3,2),
}
pb=pd["problem_bank"]
for (tier,i),(nm,calc,sol) in expected.items():
    p=pb[tier][i]
    if not close(calc,sol): errs.append(f"{tier}[{i}] my calc {calc} != claimed {sol}")
    if not close(float(p["solutions"][0]),sol): errs.append(f"{tier}[{i}] stored sol {p['solutions']} != {sol}")
# expect outside correct
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=float(p["solutions"][0])
        for m in p.get("misconceptions",[]):
            e=m["expect"]
            if e is None: continue
            if close(float(e),sol,0.011): errs.append(f"{tier}[{i}] expect {e} == correct {sol}")
# Recompute every guided_step box arithmetically from its pre text
opre=re.compile(r'([-\d\.]+)\s*([×x*÷/+\-−])\s*([-\d\.]+)\s*=\s*$')
def evalbox(pre):
    # normalise
    s=pre.replace("×","*").replace("÷","/").replace("−","-").replace("x*","*")
    m=re.search(r'([-\d\.]+)\s*([*/+\-])\s*([-\d\.]+)\s*=\s*$', s)
    if not m: return None
    a,op,b=float(m.group(1)),m.group(2),float(m.group(3))
    return {"*":a*b,"/":a/b,"+":a+b,"-":a-b}[op]
def check_walk(steps,label):
    for j,st in enumerate(steps):
        if st.get("answer") is None: continue
        pre=st.get("pre","")
        v=evalbox(pre)
        if v is not None and not close(v,float(st["answer"]),1e-6):
            errs.append(f"{label}[{j}] box '{pre}' computes {v} != answer {st['answer']}")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        check_walk(p.get("guided_steps",[]),f"{tier}[{i}].gs")
check_walk(pd["guided"]["opener"]["steps"],"opener")
for tier in ("bronze","silver","gold"):
    check_walk(pd["guided"]["teach"][tier]["steps"],f"teach.{tier}")
# duplicate solutions within tier
for tier in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[tier]):
        k=tuple(p["solutions"])
        if k in seen and p.get("input_type")!="multiple_choice":
            errs.append(f"{tier}[{i}] duplicate sol {k} with {tier}[{seen[k]}]")
        seen[k]=i
# em dash scan
def scan(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,f"{path}[{i}]")
    elif isinstance(o,str) and "—" in o: errs.append("EMDASH "+path)
scan(pd)
# preservation check vs live
live=json.load(io.open("_canon_live.json",encoding="utf-8"))
if pd["related_videos"]!=live["related_videos"]: errs.append("related_videos changed")
if pd["topic_links"]!=live["topic_links"]: errs.append("topic_links changed")
# worked_examples: only labels changed (em->colon), questions/content same
for a,b in zip(pd["worked_examples"],live["worked_examples"]):
    if a["question"]!=b["question"]: errs.append("worked_example question changed")
if errs:
    print("ERRORS:")
    for e in errs: print(" -",e)
else:
    print("ALL VERIFY CHECKS PASS")
    # print box count summary
    for tier in ("bronze","silver","gold"):
        print(tier, [len([s for s in p.get("guided_steps",[]) if s.get("answer") is not None]) for p in pb[tier]])
