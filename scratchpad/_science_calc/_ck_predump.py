import json
pre=json.load(open('_pre_dump_all.json',encoding='utf-8'))
# find canonical entry
cid="91158ba8-389c-4771-9735-326785654ccb"
def find(o):
    if isinstance(o,dict):
        if o.get('id')==cid: return o
        for v in o.values():
            r=find(v)
            if r: return r
    elif isinstance(o,list):
        for v in o:
            r=find(v)
            if r: return r
    return None
if isinstance(pre,dict) and cid in pre:
    entry=pre[cid]
else:
    entry=find(pre)
print("type",type(pre), "found" if entry else "NOTFOUND")
if isinstance(pre,dict):
    print("top keys sample",list(pre.keys())[:3])
