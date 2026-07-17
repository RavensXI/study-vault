import json
live=json.load(open("_CHKR_L01_live.json",encoding="utf-8"))
pd=live["practice_data"]

# em dash scan
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            yield from walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            yield from walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        yield path,o

emdash=[(p,s) for p,s in walk(pd) if "—" in s]
print("EM DASHES:",len(emdash))
for p,s in emdash: print("  ",p,repr(s[:80]))

# non-numeric guided box answers
bad=[]
for p,s in walk(pd):
    if p.endswith(".answer"):
        pass
# check all answer fields are numeric
def chkans(o,path=""):
    if isinstance(o,dict):
        if "answer" in o and "pre" in o:
            a=o["answer"]
            if not isinstance(a,(int,float)):
                bad.append((path,a))
        for k,v in o.items(): chkans(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): chkans(v,f"{path}[{i}]")
chkans(pd)
print("NON-NUMERIC BOXES:",bad)

# tier guide word counts
for tier,g in pd["tier_guides"].items():
    words=sum(len(s.split()) for s in g["steps"])
    print(f"tier_guides.{tier} steps words:",words)

# preservation vs pre-dump
predump=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# find L01 entry
entry=None
if isinstance(predump,list):
    for e in predump:
        if e.get("id")=="d8a78aa2-a642-4dcd-9cb0-1aa5990761e7" or e.get("slug")=="simplifying-expressions":
            entry=e;break
elif isinstance(predump,dict):
    entry=predump.get("d8a78aa2-a642-4dcd-9cb0-1aa5990761e7")
print("PREDUMP entry found:",entry is not None, "top type:", type(predump).__name__)
if entry:
    print("predump keys:", list(entry.keys()))
