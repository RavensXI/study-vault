import json

ID = "70586def-170c-4aa7-947b-2b961cfadec2"
live = json.load(open("_CHK_gL03_live.json", encoding="utf-8"))[0]["practice_data"]
pre_all = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))

# pre_all may be a list of rows or dict keyed by id
pre = None
if isinstance(pre_all, list):
    for r in pre_all:
        if r.get("id") == ID:
            pre = r.get("practice_data"); break
elif isinstance(pre_all, dict):
    if ID in pre_all:
        pre = pre_all[ID]
        if isinstance(pre, dict) and "practice_data" in pre:
            pre = pre["practice_data"]
print("pre found:", pre is not None)
if pre is None:
    print("keys sample:", (list(pre_all.keys())[:3] if isinstance(pre_all,dict) else "list len "+str(len(pre_all))))
    raise SystemExit

for field in ["related_videos", "topic_links", "worked_examples"]:
    a = json.dumps(pre.get(field), sort_keys=True, ensure_ascii=False)
    b = json.dumps(live.get(field), sort_keys=True, ensure_ascii=False)
    print(f"\n{field}: {'UNCHANGED' if a==b else 'CHANGED'}")
    if a != b:
        print("  PRE :", a[:400])
        print("  LIVE:", b[:400])

print("\npre top keys:", sorted(pre.keys()))
print("live top keys:", sorted(live.keys()))
