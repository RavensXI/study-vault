# -*- coding: utf-8 -*-
import json, io, math
pd = json.load(io.open("lesson_maths-ocr_ratio-proportion-L06.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []
def close(a,b,t=1e-6): return abs(a-b) < t

expect = {
 ("bronze",0):[2],("bronze",1):[3],("bronze",2):[7],("bronze",3):[5],
 ("bronze",4):[4],("bronze",5):[6],("bronze",6):[8],("bronze",7):[14],
 ("silver",0):[2.333],("silver",1):[3.317],("silver",2):[3.364],("silver",3):[0],
 ("silver",4):[2],("silver",5):[1],("silver",6):[1.667],
 ("gold",0):[2.552],("gold",1):[-4],("gold",2):[2.6458],("gold",3):[0],("gold",4):[3.111],
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        got=p["solutions"]; exp=expect[(tier,i)]
        if [round(float(x),4) for x in got]!=[round(float(x),4) for x in exp]:
            errs.append("%s[%d] solution %r != fresh %r"%(tier,i,got,exp))

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if not gs:
            if p.get("input_type")!="multiple_choice":
                errs.append("%s[%d] missing guided_steps"%(tier,i))
            continue
        boxes=[s for s in gs if s.get("answer") is not None]
        if not boxes: errs.append("%s[%d] no boxes"%(tier,i)); continue
        sol=float(p["solutions"][0])
        if not any(close(float(b["answer"]),sol,0.02) for b in boxes):
            errs.append("%s[%d] solution %r not reached by any box"%(tier,i,sol))
        sub=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not sub: errs.append("%s[%d] no phase:substitute"%(tier,i))
        else:
            after=sum(1 for s in gs[sub[0]:] if s.get("answer") is not None)
            before=sum(1 for s in gs[:sub[0]] if s.get("answer") is not None)
            if after<2: errs.append("%s[%d] <2 live boxes after boundary"%(tier,i))
            if before<1: errs.append("%s[%d] <1 box before boundary"%(tier,i))

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=float(p["solutions"][0])
        for j,m in enumerate(p.get("misconceptions") or []):
            if "expect" not in m: errs.append("%s[%d].m[%d] no expect key"%(tier,i,j))
            e=m.get("expect")
            if e is not None and close(float(e),sol,0.011):
                errs.append("%s[%d].m[%d] expect==answer"%(tier,i,j))

def box_answers(tier,i):
    return [s["answer"] for s in pb[tier][i]["guided_steps"] if s.get("answer") is not None]
g0=box_answers("gold",0)
chk=[14, round(14**(1/3),4), round((5*round(14**(1/3),4)+4)**(1/3),4), round(5*2.5225+4,4), round((16.6125)**(1/3),3)]
if [round(x,4) for x in g0]!=[round(x,4) for x in chk]:
    errs.append("gold0 chain %r vs %r"%(g0,chk))
g2=box_answers("gold",2)
if g2!=[16,2.6667,7.1113,14.1113,2.6458]: errs.append("gold2 chain %r"%(g2,))
s2=box_answers("silver",2)
if s2!=[11,3.317,11.317,3.364]: errs.append("silver2 chain %r"%(s2,))

for tier in ("bronze","silver","gold"):
    t=pd["guided"]["teach"][tier]
    nb=sum(1 for s in t["steps"] if s.get("answer") is not None)
    if nb<4: errs.append("teach.%s <4 boxes"%tier)
if round(41**(1/3),3)!=3.448: errs.append("cbrt41 mismatch")
opb=[s["answer"] for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if opb!=[8,7]: errs.append("opener boxes %r"%(opb,))

def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+str(k))
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,path+"[%d]"%j)
    elif isinstance(o,str) and "—" in o: errs.append("EMDASH at "+path)
scan(pd,"pd")

# preservation check vs pre-dump
pre=json.load(io.open("_pre_dump_maths-ocr.json",encoding="utf-8"))
row=[r for r in pre if r["id"]=="4e8ba0ab-6dca-4615-98e2-2fac39408f5c"][0]["practice_data"]
for k in ("related_videos","topic_links","worked_examples"):
    if json.dumps(row.get(k),sort_keys=True)!=json.dumps(pd.get(k),sort_keys=True):
        errs.append("PRESERVATION changed: %s"%k)

if errs:
    print("VERIFY FAIL (%d):"%len(errs))
    for e in errs: print("  -",e)
else:
    print("VERIFY OK: solutions fresh, walks land, boundaries valid, expects clean, no em dashes, preserved fields intact")
