import json
ID="fe589e29-485c-4272-94df-41687f398c1b"
live=json.load(open("_CHK_L02_livefresh.json",encoding="utf-8"))["practice_data"]
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre-dump structure?
if isinstance(pre,list):
    entry=[x for x in pre if x.get("id")==ID]
    entry=entry[0] if entry else None
elif isinstance(pre,dict):
    entry=pre.get(ID) or (pre.get("lessons") and next((x for x in pre["lessons"] if x.get("id")==ID),None))
else:
    entry=None
print("pre-dump type:",type(pre).__name__, "keys/len:", (list(pre.keys())[:5] if isinstance(pre,dict) else len(pre)))
if entry is None:
    # try find by scanning
    print("could not locate entry directly")
else:
    pp = entry.get("practice_data") if "practice_data" in entry else entry
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pp.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
        if not same:
            print("   PRE:",json.dumps(pp.get(f),ensure_ascii=False)[:300])
            print("   LIVE:",json.dumps(live.get(f),ensure_ascii=False)[:300])
