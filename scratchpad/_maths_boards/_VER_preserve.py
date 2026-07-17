import json

LID = "32c2c2c1-056b-4d78-b025-7e1e6f7ab3f3"
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
live = json.load(open("_VER_live_pd.json", encoding="utf-8"))

# pre-dump could be dict keyed by id, or list of rows
entry = None
if isinstance(pre, dict):
    if LID in pre:
        entry = pre[LID]
    else:
        # maybe dict with 'lessons' etc
        print("pre top keys:", list(pre.keys())[:10])
elif isinstance(pre, list):
    for r in pre:
        if r.get("id") == LID:
            entry = r.get("practice_data", r)
            break
print("entry found:", entry is not None)
if entry is None:
    raise SystemExit

pd = entry.get("practice_data", entry) if isinstance(entry, dict) else entry
print("pre pd keys:", list(pd.keys()))

for field in ["related_videos", "topic_links", "worked_examples"]:
    a = json.dumps(pd.get(field), sort_keys=True, ensure_ascii=False)
    b = json.dumps(live.get(field), sort_keys=True, ensure_ascii=False)
    print(f"{field}: {'SAME' if a==b else 'DIFFERENT'}")
    if a != b:
        print("  PRE :", a[:400])
        print("  LIVE:", b[:400])
