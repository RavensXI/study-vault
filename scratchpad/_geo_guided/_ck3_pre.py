import json
ID="0d2298c0-fb7d-447b-80ee-0cf8468366f2"
d=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_audit\_pre_dump_all.json",encoding="utf-8"))
if isinstance(d,dict):
    rows=d.get("rows") or d.get("lessons") or list(d.values())
else: rows=d
def find(rows):
    for r in rows:
        if isinstance(r,dict) and r.get("id")==ID: return r
    return None
r=find(rows)
print("found" if r else "NOT FOUND", type(d), (list(d.keys())[:5] if isinstance(d,dict) else len(rows)))
if r: json.dump(r.get("practice_data",r),open("_ck3_pre.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
