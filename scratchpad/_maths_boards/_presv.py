import json
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
live=json.load(open("_live_gl02.json",encoding="utf-8"))
ID="96f5aef3-e4c8-4faf-ba82-1d587dc4e10e"
# pre may be list or dict keyed by id
entry=None
if isinstance(pre,list):
    for r in pre:
        if r.get("id")==ID: entry=r.get("practice_data"); break
elif isinstance(pre,dict):
    if ID in pre: entry=pre[ID]
    elif "lessons" in pre:
        for r in pre["lessons"]:
            if r.get("id")==ID: entry=r.get("practice_data"); break
print("found pre entry:", entry is not None)
if entry:
    for f in ["topic_links","related_videos","worked_examples"]:
        same = json.dumps(entry.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: preserved={same}")
        if not same:
            print("  PRE:",json.dumps(entry.get(f),ensure_ascii=False)[:400])
            print("  LIVE:",json.dumps(live.get(f),ensure_ascii=False)[:400])
    # also check bank displays/solutions preservation summary
    print("pre keys:",list(entry.keys()))
