import json

ID = "89689a46-7251-4c2a-900e-5fdc240dafd3"
live = json.load(open("_chk_gL01_live.json", encoding="utf-8"))["practice_data"]

pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
# pre may be dict keyed by id or list
entry = None
if isinstance(pre, dict):
    if ID in pre:
        entry = pre[ID]
    else:
        for k, v in pre.items():
            if isinstance(v, dict) and v.get("id") == ID:
                entry = v; break
elif isinstance(pre, list):
    for v in pre:
        if v.get("id") == ID:
            entry = v; break
print("pre entry found:", entry is not None)
if entry is None:
    print("pre type:", type(pre))
    if isinstance(pre, dict):
        print("sample keys:", list(pre.keys())[:5])
    raise SystemExit

pd = entry.get("practice_data", entry)
for field in ["related_videos", "topic_links", "worked_examples"]:
    a = json.dumps(pd.get(field), sort_keys=True, ensure_ascii=False)
    b = json.dumps(live.get(field), sort_keys=True, ensure_ascii=False)
    print(f"{field}: {'SAME' if a==b else 'DIFF'}")
    if a != b:
        print("  PRE :", a[:400])
        print("  LIVE:", b[:400])
print("pre top keys:", list(pd.keys()))
