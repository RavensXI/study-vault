import json
ID="9f0126b9-ab85-4cbc-bc94-5d1214d5c4c2"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre could be list or dict
entry=None
if isinstance(pre,list):
    for e in pre:
        if e.get("id")==ID: entry=e; break
elif isinstance(pre,dict):
    entry=pre.get(ID) or (pre.get("data") and None)
    if entry is None:
        # maybe keyed by id
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: entry=v;break
print("found entry:",entry is not None, "type pre:",type(pre).__name__)
if entry is None and isinstance(pre,dict):
    print("dict keys sample:",list(pre.keys())[:5])
