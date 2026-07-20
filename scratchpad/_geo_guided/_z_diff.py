import json
pre=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_audit\_pre_dump_all.json",encoding='utf-8'))
ID="2aeee60b-5e2f-4781-8455-e81739317bf9"
if isinstance(pre,dict):
    keys=list(pre.keys())[:3]; print("dict keys sample",keys)
    ent=pre.get(ID)
    if ent is None:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get('id')==ID: ent=v
else:
    ent=None
    for v in pre:
        if v.get('id')==ID: ent=v
print("found",bool(ent), list(ent.keys()) if ent else None)
json.dump(ent,open('_z_L09_pre.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
