import json
ID="0b095025-37bb-49e4-94da-6f898ad6f3e7"
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
# find entry
entry=None
if isinstance(pre,dict):
    if ID in pre: entry=pre[ID]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: entry=v; break
            if isinstance(v,dict) and v.get("lesson_id")==ID: entry=v; break
if entry is None and isinstance(pre,list):
    for v in pre:
        if v.get("id")==ID or v.get("lesson_id")==ID: entry=v; break
print("type pre:", type(pre))
if isinstance(pre,dict): print("pre keys sample:", list(pre.keys())[:5])
print("entry found:", entry is not None)
if entry is not None:
    pd = entry.get("practice_data", entry)
    print("pre pd keys:", list(pd.keys()) if isinstance(pd,dict) else "n/a")
    json.dump(pd, open("_pre_pd.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
