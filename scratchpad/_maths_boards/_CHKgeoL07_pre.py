import json
ID="f3574e2a-651d-42a7-af75-8ee52eeb48d8"
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
# pre may be list or dict
if isinstance(pre,list):
    entry=[e for e in pre if e.get("id")==ID]
    entry=entry[0] if entry else None
elif isinstance(pre,dict):
    entry=pre.get(ID)
print("found entry:",entry is not None)
if entry:
    pd=entry.get("practice_data") if "practice_data" in entry else entry
    print("pre keys:",list(pd.keys()) if isinstance(pd,dict) else type(pd))
    for k in ("related_videos","topic_links","worked_examples"):
        json.dump(pd.get(k),open(f"_pre_{k}.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
    live=json.load(open("_CHKgeoL07_live.json",encoding="utf-8"))
    for k in ("related_videos","topic_links","worked_examples"):
        same = json.dumps(pd.get(k),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(k),sort_keys=True,ensure_ascii=False)
        print(f"{k}: preserved={same}")
    # also list pre problem counts
    ppb=pd.get("problem_bank",{})
    for t in ("bronze","silver","gold"):
        print("pre",t,len(ppb.get(t,[])))
