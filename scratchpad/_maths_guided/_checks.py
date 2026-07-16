import json
live=json.load(open("_live_graphs_l01.json",encoding="utf-8"))

# pre-dump
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
ID="a7d027ed-f9a9-427f-aa1d-83c6459954b0"
entry=None
if isinstance(pre,dict):
    if ID in pre: entry=pre[ID]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get('id')==ID: entry=v; break
            if isinstance(v,list):
                for it in v:
                    if isinstance(it,dict) and it.get('id')==ID: entry=it
elif isinstance(pre,list):
    for it in pre:
        if isinstance(it,dict) and it.get('id')==ID: entry=it
print("pre entry found:", entry is not None)
if entry:
    print("pre keys:", list(entry.keys()))
    pd = entry.get('practice_data', entry)
    print("pd keys:", list(pd.keys()) if isinstance(pd,dict) else type(pd))
    open("_pre_pd.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
