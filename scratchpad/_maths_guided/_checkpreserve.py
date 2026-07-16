import json
ID="bc1ac13e-1cc0-42b3-a805-a8a3f35cbabb"
live=json.load(open("_live_ratio_L01.json",encoding="utf-8"))
dump=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
# find entry
entry=None
if isinstance(dump,list):
    for e in dump:
        if e.get("id")==ID: entry=e; break
elif isinstance(dump,dict):
    entry=dump.get(ID) or (dump.get("lessons") and next((x for x in dump["lessons"] if x.get("id")==ID),None))
print("entry found:", entry is not None)
if entry:
    pd=entry.get("practice_data") or entry
    for f in ["related_videos","topic_links","worked_examples"]:
        same=json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f, "PRESERVED" if same else "CHANGED")
    print("pre-dump keys:", list(pd.keys()))
