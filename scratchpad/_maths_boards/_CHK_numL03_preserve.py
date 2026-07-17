import json

LID = "c8596747-22a3-47f0-8fe7-f0bc6c6d1101"
pre = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
# pre-dump structure: find entry
entry = None
if isinstance(pre, dict):
    if LID in pre:
        entry = pre[LID]
    else:
        for k,v in pre.items():
            if isinstance(v, dict) and v.get("id")==LID:
                entry = v; break
elif isinstance(pre, list):
    for v in pre:
        if v.get("id")==LID:
            entry = v; break
print("entry found:", entry is not None)
if entry is None:
    # inspect shape
    print("type", type(pre))
    if isinstance(pre, list):
        print("len", len(pre), "sample keys", list(pre[0].keys())[:10])
    else:
        print("keys sample", list(pre.keys())[:5])
else:
    pd = entry.get("practice_data") if "practice_data" in entry else entry
    print("pre keys:", list(pd.keys()))
    print("pre related_videos:", json.dumps(pd.get("related_videos")))
    print("pre topic_links:", json.dumps(pd.get("topic_links")))
    we = pd.get("worked_examples")
    print("pre worked_examples count:", len(we) if we else we)
    print(json.dumps(we, ensure_ascii=False)[:1500])
