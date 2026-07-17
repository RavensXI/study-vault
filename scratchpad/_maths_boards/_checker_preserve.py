import json
ID="063c867c-7ba6-4879-9747-c3546382aaf2"
pre=json.load(open('_pre_dump_maths-aqa.json',encoding='utf-8'))
# find entry
entry=None
if isinstance(pre,dict):
    for k,v in pre.items():
        if isinstance(v,dict) and (v.get('id')==ID or k==ID):
            entry=v; break
    if entry is None and ID in pre:
        entry=pre[ID]
if entry is None and isinstance(pre,list):
    for v in pre:
        if v.get('id')==ID: entry=v;break
print("type:", type(pre).__name__)
if isinstance(pre,dict):
    print("keys sample:", list(pre.keys())[:5])
print("found entry:", entry is not None)
if entry: print(json.dumps(entry,ensure_ascii=False)[:500])
