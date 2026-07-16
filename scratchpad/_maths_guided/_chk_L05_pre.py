import json
ID="ea8d68a2-63b8-40e9-87de-f879156e0d93"
d=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
# find entry
def find(o):
    if isinstance(o,dict):
        if o.get("id")==ID: return o
        for v in o.values():
            r=find(v)
            if r: return r
    elif isinstance(o,list):
        for v in o:
            r=find(v)
            if r: return r
    return None
e=find(d)
if e is None:
    print("top type", type(d))
    if isinstance(d,dict): print("keys", list(d.keys())[:20])
    if isinstance(d,list): print("len",len(d),"first keys", list(d[0].keys()) if d else None)
else:
    pd=e.get("practice_data",e)
    json.dump(pd, open("_CHK_L05_predump.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
    print("found; pd keys:", list(pd.keys()))
