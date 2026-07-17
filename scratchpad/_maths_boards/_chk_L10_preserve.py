import json
pre=json.load(open('_pre_dump_maths-eduqas.json',encoding='utf-8'))
ID="27ec4539-cb68-4e60-ad0d-fa0828706d80"
row=None
for r in pre:
    if r.get('id')==ID: row=r; break
if not row:
    # maybe keyed differently
    print("keys of first:", list(pre[0].keys()))
else:
    ppd=row.get('practice_data') or {}
    print("pre keys:", list(ppd.keys()))
    live=json.load(open('_CHK_L10_live.json',encoding='utf-8'))
    for fld in ['related_videos','topic_links','worked_examples']:
        pv=ppd.get(fld,'__MISSING__'); lv=live.get(fld,'__MISSING__')
        same = json.dumps(pv,sort_keys=True)==json.dumps(lv,sort_keys=True)
        print(f"{fld}: preserved={same}")
        if not same:
            print("  PRE:",json.dumps(pv)[:300])
            print("  LIVE:",json.dumps(lv)[:300])
