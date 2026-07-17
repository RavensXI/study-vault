import json,re
pd=json.load(open("_CHK_graphsL04_LIVE.json",encoding="utf-8"))
pb=pd["problem_bank"]
issues=[]

# 1. Check em dashes anywhere student-facing
def walk_strings(o,path=""):
    if isinstance(o,str):
        yield path,o
    elif isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            yield from walk_strings(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o):
            yield from walk_strings(v,path+f"[{i}]")
for p,s in walk_strings(pd):
    if "—" in s: issues.append(("EMDASH",p,s[:60]))

# 2. verify chart points against x/y axis maxima etc - just dump each problem chart pts
for tier in ["bronze","silver","gold"]:
    for i,prob in enumerate(pb[tier]):
        ch=prob.get("chart")
        if ch:
            ds=ch["data"]["datasets"][0]["data"]
            labels=ch["data"].get("labels")
            if labels is not None:
                pts=list(zip(labels,ds))
            else:
                pts=[(d["x"],d["y"]) for d in ds]
            print(f"{tier}[{i}] chart pts:",pts,"sol:",prob.get("solutions"))

# 3. preservation vs pre-dump
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
# find this lesson
ID="b73c61cf-00b8-44c8-9e08-9f7f6f84c60a"
def findpre(pre):
    if isinstance(pre,dict):
        if ID in pre: return pre[ID]
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: return v
    if isinstance(pre,list):
        for v in pre:
            if isinstance(v,dict) and v.get("id")==ID: return v
    return None
pe=findpre(pre)
print("\npre-dump found:",pe is not None, "type", type(pre).__name__)
if isinstance(pre,dict): print("pre keys sample:",list(pre.keys())[:3])
if pe:
    ppd=pe.get("practice_data") if "practice_data" in pe else pe
    for fld in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(ppd.get(fld),sort_keys=True)
        b=json.dumps(pd.get(fld),sort_keys=True)
        print(f"PRESERVE {fld}: {'SAME' if a==b else 'CHANGED'}")
        if a!=b:
            print("  pre:",a[:300]); print("  live:",b[:300])

for x in issues: print("ISSUE",x)
print("emdash count:",len(issues))
