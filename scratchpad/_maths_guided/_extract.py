import json
dump = json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
ID = "a769c80a-697d-4ae1-a042-6299738f9021"
# dump might be list or dict
def find(o):
    if isinstance(o, list):
        for e in o:
            if isinstance(e,dict) and e.get("id")==ID: return e
    if isinstance(o, dict):
        if o.get("id")==ID: return o
        for v in o.values():
            r=find(v)
            if r: return r
    return None
e = find(dump)
if e:
    pd = e.get("practice_data")
    json.dump(pd, open("_pre_L12.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
    print("found; keys:", list(pd.keys()) if pd else None)
else:
    print("NOT FOUND; top type", type(dump))
    if isinstance(dump,dict): print(list(dump.keys())[:20])
    if isinstance(dump,list): print(len(dump), dump[0].keys() if dump else None)
