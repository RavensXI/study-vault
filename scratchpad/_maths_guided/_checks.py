import json, re
live=json.load(open("_live_L07.json",encoding="utf-8"))

# Pre-dump
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
KEY="graphs-L07"
ID="6623fba3-fb9e-4353-80c4-35ed1d88f47e"
# find entry
entry=None
if isinstance(pre,dict):
    for k,v in pre.items():
        if k==ID or k==KEY: entry=v
    if entry is None and ID in pre: entry=pre[ID]
if entry is None and isinstance(pre,list):
    for e in pre:
        if e.get("id")==ID or e.get("key")==KEY: entry=e
print("pre entry found:", entry is not None)
if entry is not None:
    # entry may itself be practice_data or have practice_data
    pdp = entry.get("practice_data", entry) if isinstance(entry,dict) else entry
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pdp.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f} preserved:", same)
    print("pre keys:", list(pdp.keys()) if isinstance(pdp,dict) else type(pdp))

# Em dash search in student-facing (exclude note fields)
emdash_hits=[]
def walk(obj,path):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k=="note": continue
            walk(v,path+"."+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            walk(v,f"{path}[{i}]")
    elif isinstance(obj,str):
        if "—" in obj or "–" in obj:
            emdash_hits.append((path,obj))
walk(live,"pd")
print("emdash/endash hits:", len(emdash_hits))
for p,s in emdash_hits: print("  ",p,repr(s[:60]))

# HTML entities in plain-text fields
ent=[]
def walk2(obj,path):
    if isinstance(obj,dict):
        for k,v in obj.items(): walk2(v,path+"."+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj): walk2(v,f"{path}[{i}]")
    elif isinstance(obj,str):
        if re.search(r"&[a-zA-Z]+;|&#\d+;",obj): ent.append((path,obj))
walk2(live,"pd")
print("html entity hits:", len(ent))
for p,s in ent[:20]: print("  ",p,repr(s[:60]))
