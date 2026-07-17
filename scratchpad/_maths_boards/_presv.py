import json
ID="e40e80e4-666f-4cce-a8b3-5f7bb6b5c490"
KEY="graphs-L02"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre could be list or dict
def find(pre):
    if isinstance(pre,dict):
        # maybe keyed by id
        if ID in pre: return pre[ID]
        for v in pre.values():
            if isinstance(v,dict) and v.get("id")==ID: return v
    if isinstance(pre,list):
        for e in pre:
            if e.get("id")==ID: return e
            pd=e.get("practice_data") or {}
    return None
entry=find(pre)
print("type:",type(pre).__name__, "len:", len(pre))
if entry is None:
    # try scanning
    if isinstance(pre,list):
        for e in pre[:2]:
            print("sample keys:",list(e.keys()))
    elif isinstance(pre,dict):
        ks=list(pre.keys())[:3]
        print("sample dict keys:",ks)
else:
    print("found entry keys:",list(entry.keys()))
