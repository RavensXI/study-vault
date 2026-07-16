import json
ID="33559430-93a0-4565-971b-65b8fc2cc53d"
d=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
# find entry
def find(o):
    if isinstance(o,dict):
        if o.get("id")==ID: return o
        for v in o.values():
            r=find(v)
            if r: return r
    if isinstance(o,list):
        for v in o:
            r=find(v)
            if r: return r
    return None
e=find(d)
if e:
    pd=e.get("practice_data")
    open("_CHK_graphsL08_predump.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
    print("found predump, keys:", list(pd.keys()) if pd else None)
else:
    print("not found; top-level type", type(d), list(d.keys())[:5] if isinstance(d,dict) else len(d))
