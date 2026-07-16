import json
ID='f6f5708d-edf9-42e6-81d8-49c3cf282310'
wl=json.load(open('_worklist.json',encoding='utf-8'))
# worklist may be list
def find(o):
    s=json.dumps(o)
    return ID in s
print('WORKLIST entries matching id:')
if isinstance(wl,list):
    for e in wl:
        if ID in json.dumps(e):
            print(json.dumps(e,ensure_ascii=False))
else:
    print(type(wl), list(wl.keys())[:5] if isinstance(wl,dict) else '')
    for k,v in (wl.items() if isinstance(wl,dict) else []):
        if ID in json.dumps(v) or ID in str(k):
            print(k, json.dumps(v,ensure_ascii=False)[:300])
