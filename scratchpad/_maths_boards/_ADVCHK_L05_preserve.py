import json

ID = "2e75898f-577a-42bd-b94e-f1435e89ace3"
pre = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))

# pre may be list of rows or dict keyed by id
entry = None
if isinstance(pre, list):
    for r in pre:
        if r.get("id") == ID:
            entry = r.get("practice_data")
            break
elif isinstance(pre, dict):
    if ID in pre:
        entry = pre[ID]
        if isinstance(entry, dict) and "practice_data" in entry:
            entry = entry["practice_data"]
    else:
        # maybe keyed by key like probability-statistics-L05
        for k, v in pre.items():
            vid = v.get("id") if isinstance(v, dict) else None
            if vid == ID:
                entry = v.get("practice_data")
                break

live = json.load(open("_ADVCHK_L05_live.json", encoding="utf-8"))

if entry is None:
    print("PRE ENTRY NOT FOUND; pre type:", type(pre))
    if isinstance(pre, dict):
        print("sample keys:", list(pre.keys())[:5])
else:
    for f in ["related_videos", "topic_links", "worked_examples"]:
        pv = json.dumps(entry.get(f), sort_keys=True, ensure_ascii=False)
        lv = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
        print(f, "UNCHANGED" if pv == lv else "CHANGED")
        if pv != lv:
            print("  PRE:", pv[:400])
            print("  LIVE:", lv[:400])
    print("pre keys:", list(entry.keys()))
