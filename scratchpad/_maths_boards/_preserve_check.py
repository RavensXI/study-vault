import json

ID = "f4f1368e-d7c2-41f1-8459-de2c0d500c3b"
live = json.load(open("_LIVE_L01.json", encoding="utf-8"))
pre = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))

# pre-dump may be list of rows or dict keyed by id
entry = None
if isinstance(pre, list):
    for r in pre:
        if r.get("id") == ID or r.get("slug") == "simplifying-expressions":
            entry = r; break
elif isinstance(pre, dict):
    entry = pre.get(ID) or pre.get("simplifying-expressions")
    if entry is None and "practice_data" in pre:
        entry = pre

print("pre type:", type(pre), "found entry:", entry is not None)
if entry is None:
    # show structure
    if isinstance(pre, list):
        print("list len", len(pre), "sample keys", list(pre[0].keys())[:10] if pre else None)
        for r in pre[:5]:
            print("  ", r.get("id"), r.get("slug"), r.get("title"))
    else:
        print("dict keys", list(pre.keys())[:20])
    raise SystemExit

pd_pre = entry.get("practice_data", entry)
for f in ["related_videos","topic_links","worked_examples"]:
    a = json.dumps(pd_pre.get(f), sort_keys=True, ensure_ascii=False)
    b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
    print(f, "PRESERVED" if a==b else "CHANGED")
    if a!=b:
        print("  PRE :", a[:400])
        print("  LIVE:", b[:400])
print("pre top keys:", list(pd_pre.keys()))
