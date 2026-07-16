# -*- coding: utf-8 -*-
import json, io, math
p=math.pi
new=json.load(io.open("lesson_geometry-L02.json",encoding="utf-8"))
pre=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
# find pre entry
ID="fe5f6191-4452-4313-934d-8e5d16ba1032"
pe=None
if isinstance(pre,dict):
    for k,v in pre.items():
        if k==ID or (isinstance(v,dict) and v.get("id")==ID):
            pe=v; break
        if isinstance(v,dict) and v.get("practice_data") and (v.get("id")==ID):
            pe=v; break
print("pre entry found:", pe is not None, "| pre top type:", type(pre).__name__)
# Try common shapes
if pe is None and isinstance(pre,dict):
    # maybe keyed by lesson key
    for k in ["geometry-L02"]:
        if k in pre: pe=pre[k]; print("found by key",k)
problems=[]
pb=new["problem_bank"]
for t in ("bronze","silver","gold"):
    for i,q in enumerate(pb[t]):
        problems.append((t,i,q))

fails=[]
# Fresh solve each display
def approxeq(a,b,tol=0.06): return abs(a-b)<=tol

sols={}
# compute expected answers
def solve(t,i,q):
    d=q["display"]
    s=q["solutions"]
    return s

# Independent fresh solve values
expected={
 ("bronze",0):45,("bronze",1):38,("bronze",2):30,("bronze",3):40,
 ("bronze",4):round(14*p,1),("bronze",5):round(25*p,1),("bronze",6):42,("bronze",7):144,
 ("silver",0):round(81*p,1),("silver",1):31.4/(2*3.14),("silver",2):47,("silver",3):round(25*p,1),
 ("silver",4):6,("silver",5):round(14+7*p,1),("silver",6):round(math.sqrt(50.3/p),1),
 ("gold",0):round(200+60*p),("gold",1):round(0.375*64*p,1),("gold",2):round(2*p*math.sqrt(200/p),1),
 ("gold",3):round(12*360/(2*p*9)),("gold",4):round(64*p,1),
}
for (t,i,q) in problems:
    exp=expected[(t,i)]
    stored=q["solutions"]
    if len(stored)!=1:
        fails.append(f"{t}[{i}] solutions not single: {stored}")
    elif not approxeq(float(stored[0]),float(exp)):
        fails.append(f"{t}[{i}] solution {stored[0]} != fresh {exp}")
    # duplicate check within tier handled by validator
    # expect not equal correct
    for j,m in enumerate(q.get("misconceptions",[])):
        e=m.get("expect")
        if e is not None and approxeq(float(e),float(stored[0]),0.011):
            fails.append(f"{t}[{i}].mc[{j}] expect==correct")
    # last live box lands on solution
    gs=q["guided_steps"]
    # find phase idx
    sub=None
    for k,st in enumerate(gs):
        if st.get("phase")=="substitute": sub=k;break
    live=[st for st in gs[sub:] if st.get("answer") is not None] if sub is not None else []
    if len(live)<2: fails.append(f"{t}[{i}] <2 live boxes")
    if sub is None or sub<1: fails.append(f"{t}[{i}] bad phase idx {sub}")

# preservation
if pe is not None:
    pd=pe.get("practice_data") if "practice_data" in pe else pe
    for field in ("related_videos","topic_links"):
        if json.dumps(pd.get(field),sort_keys=True)!=json.dumps(new.get(field),sort_keys=True):
            fails.append(f"PRESERVE {field} changed")
    # worked_examples: only 2 labels changed
    owe=json.dumps(pd.get("worked_examples"))
    nwe=json.dumps(new.get("worked_examples"))
    if owe!=nwe:
        # allowed: em dash label edits
        import copy
        oc=copy.deepcopy(pd.get("worked_examples"))
        for we in oc:
            for st in we.get("steps",[]):
                if "label" in st: st["label"]=st["label"].replace(" — ",": ").replace("—",":")
        if json.dumps(oc)!=nwe:
            fails.append("PRESERVE worked_examples changed beyond em-dash labels")
        else:
            print("worked_examples: only em-dash label edits (OK)")
else:
    print("WARN: could not locate pre-dump entry to compare preservation")

print("FAILS:",len(fails))
for f in fails: print("  -",f)
