import json, io
ID="6623fba3-fb9e-4353-80c4-35ed1d88f47e"
d=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
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
    # maybe keyed by id
    if ID in d: e=d[ID]
print("found:", e is not None)
if e:
    pd=e.get("practice_data", e)
    json.dump(pd, io.open("_pre_L07.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
    print("pre keys:", list(pd.keys()))
