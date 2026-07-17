import json

ID = "a65d19a4-17d8-4370-ac24-ef8ae364f72d"
pre = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))

# locate pre-dump entry
entry = None
if isinstance(pre, dict):
    if ID in pre:
        entry = pre[ID]
    else:
        for k, v in pre.items():
            if isinstance(v, dict) and (v.get("id") == ID or v.get("lesson_id") == ID):
                entry = v
                break
elif isinstance(pre, list):
    for v in pre:
        if isinstance(v, dict) and v.get("id") == ID:
            entry = v
            break
print("entry found:", entry is not None)
if entry is not None:
    pd_pre = entry.get("practice_data", entry)
    print("pre keys:", list(pd_pre.keys()))
    live = json.load(open("_CHK_numL05_live.json", encoding="utf-8"))
    for f in ("related_videos", "topic_links", "worked_examples"):
        a = json.dumps(pd_pre.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
        print(f, "IDENTICAL" if a == b else "CHANGED")
        if a != b:
            print("  PRE :", a[:400])
            print("  LIVE:", b[:400])
