import json
# find pre-dump entry
d = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
LID = "0b095025-37bb-49e4-94da-6f898ad6f3e7"
def find(o):
    if isinstance(o, list):
        for x in o:
            r=find(x)
            if r: return r
    elif isinstance(o, dict):
        if o.get("id")==LID: return o
        for v in o.values():
            r=find(v)
            if r: return r
    return None
print(type(d), list(d.keys()) if isinstance(d,dict) else len(d))
e = find(d)
if e:
    pd = e.get("practice_data", e)
    json.dump(pd, open("_CHK_geomL08_predump.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
    print("found predump, keys:", list(pd.keys()) if isinstance(pd,dict) else "n/a")
else:
    print("NOT FOUND by id; trying key search")
