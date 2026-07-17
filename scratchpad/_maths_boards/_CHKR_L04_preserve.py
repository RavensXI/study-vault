import json
ID="6e383a58-7e5b-4917-a28d-2881938a3def"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
live=json.load(open("_CHKR_L04_live.json",encoding="utf-8"))["practice_data"]

# find the pre-dump entry for this id
entry=None
if isinstance(pre,dict):
    if ID in pre: entry=pre[ID]
    elif "lessons" in pre:
        for l in pre["lessons"]:
            if l.get("id")==ID: entry=l
    else:
        # maybe dict keyed by id with practice_data
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: entry=v
elif isinstance(pre,list):
    for l in pre:
        if l.get("id")==ID: entry=l
print("entry found:",entry is not None)
if entry is None:
    print("keys sample:",list(pre)[:3] if isinstance(pre,dict) else pre[0].keys())
else:
    ppd=entry.get("practice_data",entry)
    for f in ["related_videos","topic_links","worked_examples","method_card"]:
        same = json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: preserved={same}")
        if not same:
            print("  PRE :",json.dumps(ppd.get(f),ensure_ascii=False)[:300])
            print("  LIVE:",json.dumps(live.get(f),ensure_ascii=False)[:300])
    # opener entities in pre?
    print("pre top keys:",list(ppd.keys()))
    og=ppd.get("guided",{})
    print("pre had guided:",bool(og), "pre guided keys:", list(og.keys()) if isinstance(og,dict) else None)
    print("pre opener:",json.dumps(og.get("opener") if isinstance(og,dict) else None,ensure_ascii=False)[:500])
