import json
pre = json.load(open("_pre_dump_all.json", encoding="utf-8"))
live = json.load(open("_live_3c4aa292.json", encoding="utf-8"))
cid = "3c4aa292-cf3a-4cda-876d-25b030880bb5"
entry=None
for e in pre:
    if isinstance(e,dict):
        if e.get("id")==cid or cid in json.dumps(e)[:200]:
            entry=e; break
if entry is None:
    # find by any id field
    print("sample entry keys:", list(pre[0].keys()) if pre else None)
    # search all
    for e in pre:
        s=json.dumps(e)
        if cid in s:
            entry=e; break
if entry:
    pdp = entry.get("practice_data", entry)
    for f in ("related_videos","worked_examples","topic_links","exam_context"):
        same = json.dumps(pdp.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
        print(f"{f}: preserved={same}")
        if not same:
            print("   PRE :", json.dumps(pdp.get(f))[:300])
            print("   LIVE:", json.dumps(live.get(f))[:300])
else:
    print("no pre entry for canonical id; searching all ids in family")
    fam=["48cb4395-c42b-4faa-9a71-44653a691790","3c4aa292-cf3a-4cda-876d-25b030880bb5","36c7ea77-c3be-464d-b057-4e7baf5754f5"]
    for e in pre:
        s=json.dumps(e)
        for f in fam:
            if f in s: print("found id", f, "keys", list(e.keys())[:6])
