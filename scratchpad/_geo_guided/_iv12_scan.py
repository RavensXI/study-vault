import json, os, re
d=os.path.dirname(os.path.abspath(__file__))
live=json.load(open(os.path.join(d,"_iv12_live.json"),encoding="utf-8"))
pre_all=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_audit\_pre_dump_all.json",encoding="utf-8"))
# find pre entry
ID="3a0b41fb-d6d3-43ac-9d74-08abb8926e8a"
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
print("pre type", type(pre_all), (list(pre_all)[:5] if isinstance(pre_all,dict) else len(pre_all)))
e=find(pre_all)
print("found pre entry:", bool(e), list(e.keys()) if e else None)
json.dump(e, open(os.path.join(d,"_iv12_pre.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
