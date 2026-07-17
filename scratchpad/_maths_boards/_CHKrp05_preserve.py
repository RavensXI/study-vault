import json

live = json.load(open("_CHKrp05_live.json", encoding="utf-8"))[0]["practice_data"]
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))

ID = "ddbb6863-36ab-4898-8090-16df440a9d85"
# pre may be dict keyed by id, or list
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
        if v.get("id") == ID or v.get("slug") == "proportion-equations-and-powers":
            entry = v; break
print("pre entry found:", entry is not None)
if entry is None:
    # show shape
    print("type", type(pre))
    if isinstance(pre, dict):
        print("sample keys", list(pre.keys())[:3])
        first = pre[list(pre.keys())[0]]
        print("first val keys", list(first.keys()) if isinstance(first,dict) else type(first))
    raise SystemExit

ppd = entry.get("practice_data", entry)
print("pre pd keys:", list(ppd.keys()))

for field in ["related_videos", "topic_links", "worked_examples"]:
    a = json.dumps(ppd.get(field), sort_keys=True, ensure_ascii=False)
    b = json.dumps(live.get(field), sort_keys=True, ensure_ascii=False)
    print(f"\n{field}: {'UNCHANGED' if a==b else 'CHANGED'}")
    if a != b:
        print(" PRE :", a[:400])
        print(" LIVE:", b[:400])
