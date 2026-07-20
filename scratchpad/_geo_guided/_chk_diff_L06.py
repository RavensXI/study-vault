import json
pre=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_audit\_pre_dump_all.json",encoding="utf-8"))
ID="64b88a88-ec47-40c2-9478-1f7ba7572096"
if isinstance(pre,dict):
    print("dict keys sample", list(pre.keys())[:5])
    entry=pre.get(ID)
else:
    entry=None
    for e in pre:
        if e.get("id")==ID: entry=e
print(type(entry))
json.dump(entry, open("_chk_pre_L06.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
