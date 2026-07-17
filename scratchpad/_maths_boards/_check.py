import json, re
live=json.load(open("_live_ratio-proportion-L01.json",encoding="utf-8"))

# Load pre-dump entry
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
ID="9a6f1e85-41b4-4b82-87c6-e919e48362a9"
entry=None
if isinstance(pre,list):
    for r in pre:
        if r.get("id")==ID: entry=r; break
elif isinstance(pre,dict):
    entry=pre.get(ID) or pre.get("ratio-proportion-L01")
    if entry is None and "lessons" in pre:
        for r in pre["lessons"]:
            if r.get("id")==ID: entry=r
print("pre-dump type:", type(pre).__name__, "keys sample:", (list(pre.keys())[:5] if isinstance(pre,dict) else "list len "+str(len(pre))))
if entry:
    ppd = entry.get("practice_data", entry)
    print("PRE keys:", sorted(ppd.keys()))
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(ppd.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
        print(f"preserve {f}: {'SAME' if same else 'CHANGED'}")
else:
    print("NO PRE ENTRY FOUND")

# em dash / en dash scan in student-facing strings
def walk(o,path=""):
    out=[]
    if isinstance(o,dict):
        for k,v in o.items():
            out+=walk(v,path+"/"+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o):
            out+=walk(v,path+f"[{i}]")
    elif isinstance(o,str):
        if "—" in o: out.append(("EMDASH",path,o))
    return out
# exclude note fields
issues=[x for x in walk(live) if "/note" not in x[1]]
print("EM DASHES (excl note):", len(issues))
for x in issues[:20]: print("  ",x[1],repr(x[2][:60]))
