# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("../_maths_guided/lesson_maths-eduqas_number-L05.json", encoding="utf-8"))
errs = []
expected = {
 ("bronze",0):20,("bronze",1):35,("bronze",2):9,("bronze",3):65,("bronze",4):25,
 ("bronze",5):15,("bronze",6):11,("bronze",7):30,
 ("silver",0):392,("silver",1):408,("silver",2):420,("silver",3):2700,("silver",4):42,("silver",5):60,("silver",6):78,
 ("gold",0):200000,("gold",1):4243.6,("gold",2):25000,("gold",3):26000,("gold",4):4,
}
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    seen=set()
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"]
        if abs(sol[0]-expected[(tier,i)])>1e-6:
            errs.append((tier,i,"solution %s != expected %s"%(sol[0],expected[(tier,i)])))
        key=tuple(sol)
        if key in seen: errs.append((tier,i,"DUP within tier %s"%sol))
        seen.add(key)
        boxes=[s["answer"] for s in p["guided_steps"] if s.get("answer") is not None]
        if expected[(tier,i)] not in boxes:
            errs.append((tier,i,"solution not among guided box answers %s"%boxes))
        for m_ in p.get("misconceptions",[]):
            e=m_["expect"]
            if e is not None and abs(float(e)-sol[0])<1e-6:
                errs.append((tier,i,"expect==correct"))
checks = [
  ("g1", 4000*1.03**2, 4243.6),("g0", 225000/1.125, 200000),("g2cube", 0.8**3, 0.512),
  ("g2rev", 12800/0.512, 25000),("g3rev", 27300/1.05, 26000),("g4y1", 5000*1.025, 5125),
  ("g4y2", 5125*1.025, 5253.125),("g4y4", round(5253.125*1.025**2,2), 5519.06),
  ("s5", 54/0.9, 60),("s4", 24+12+6, 42),("b6", 55/5, 11),
  ("s0", 350*1.12, 392),("s1",480*0.85,408),("s2",600*0.7,420),("s3",2500*1.08,2700),
  ("s6",75*1.04,78),("s4mul",240*0.175,42),
]
for name,got,exp in checks:
    if abs(got-exp)>0.02: errs.append(("calc",name,"%s != %s"%(got,exp)))
exp_checks=[("s5add",54*1.1,59.4),("g0sub",225000*0.875,196875),("g3sub",27300*0.95,25935),
  ("g1simple",4000+240,4240),("g2one",12800/0.8,16000)]
for name,got,exp in exp_checks:
    if abs(got-exp)>0.01: errs.append(("expect",name,"%s != %s"%(got,exp)))
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            scan(v,path+"."+k)
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,path+"[%d]"%j)
    elif isinstance(o,str) and "—" in o: errs.append(("emdash",path,o[:40]))
scan(pd,"pd")
teach_final={"bronze":21,"silver":270,"gold":84}
for t,v in teach_final.items():
    tb=[s["answer"] for s in pd["guided"]["teach"][t]["steps"] if s.get("answer") is not None]
    if len(tb)<4: errs.append(("teach",t,"only %d boxes"%len(tb)))
    if tb[-1]!=v: errs.append(("teach",t,"final %s != %s"%(tb[-1],v)))
live=json.load(io.open("_live_L05.json",encoding="utf-8"))
for f in("topic_links","related_videos","worked_examples"):
    if json.dumps(pd.get(f),sort_keys=True)!=json.dumps(live.get(f),sort_keys=True):
        errs.append(("preserve",f,"changed"))
if errs:
    print("FAIL",len(errs))
    for e in errs: print("  ",e)
else:
    print("ALL VERIFIED CLEAN")
