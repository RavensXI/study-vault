import json,os
d=os.path.dirname(os.path.abspath(__file__))
pre=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_audit\_pre_dump_all.json",encoding="utf-8"))
ID="3a0b41fb-d6d3-43ac-9d74-08abb8926e8a"
row=None
if isinstance(pre,dict):
    print("dict keys sample:", list(pre.keys())[:5])
    row=pre.get(ID)
    if row is None:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: row=v;break
else:
    for r in pre:
        if r.get("id")==ID or r.get("lesson_id")==ID: row=r;break
print("found:",row is not None, type(row))
json.dump(row,open(os.path.join(d,"_CK12_pre.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
