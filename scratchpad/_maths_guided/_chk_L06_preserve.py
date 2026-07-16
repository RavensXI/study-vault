import json

ID = "4aa9afe1-7e47-4f0f-b7e6-da22be472716"
live = json.load(open("_CHK_L06_LIVE_fresh.json", encoding="utf-8"))

# find pre-dump entry
pre_all = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
entry = None
if isinstance(pre_all, list):
    for e in pre_all:
        if e.get("id") == ID:
            entry = e; break
elif isinstance(pre_all, dict):
    entry = pre_all.get(ID)
    if entry is None:
        # maybe keyed differently
        for k,v in pre_all.items():
            if isinstance(v, dict) and v.get("id")==ID:
                entry=v; break
print("found entry:", entry is not None, "type", type(pre_all).__name__)
if entry:
    pd = entry.get("practice_data", entry)
    for field in ["related_videos", "topic_links", "worked_examples"]:
        a = json.dumps(pd.get(field), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(field), sort_keys=True, ensure_ascii=False)
        print(f"{field}: {'SAME' if a==b else 'DIFFERENT'}")
        if a!=b:
            print("  PRE :", a[:500])
            print("  LIVE:", b[:500])
    print("PRE keys:", sorted(pd.keys()))
    print("LIVE keys:", sorted(live.keys()))
