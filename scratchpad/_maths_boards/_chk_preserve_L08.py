import json

ID = "1d30ba6e-3b9a-41a9-b192-23cab4fd0d5f"
live = json.load(open("_chk_live_L08.json", encoding="utf-8"))
pre = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))

# find pre entry
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
    print("pre top-level type:", type(pre))
    if isinstance(pre, dict):
        print("sample keys:", list(pre.keys())[:5])
    raise SystemExit

pd_pre = entry.get("practice_data", entry)
for f in ("related_videos", "topic_links", "worked_examples"):
    a = json.dumps(pd_pre.get(f), sort_keys=True, ensure_ascii=False)
    b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
    print(f, "PRESERVED" if a == b else "CHANGED")
    if a != b:
        print("  pre:", a[:300])
        print("  live:", b[:300])
print("pre keys:", sorted(pd_pre.keys()))
print("live keys:", sorted(live.keys()))
