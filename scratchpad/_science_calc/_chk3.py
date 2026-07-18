import json
pre=json.load(open('_pre_dump_all.json',encoding='utf-8'))
print("type",type(pre))
cid='4ef45adc-b491-4025-9906-f541fa8a7a8f'
if isinstance(pre,dict):
    print("top keys sample:",list(pre)[:4])
    v=pre.get(cid)
    print("direct get cid:",type(v))
    if isinstance(v,dict): print("  subkeys:",list(v)[:8])
