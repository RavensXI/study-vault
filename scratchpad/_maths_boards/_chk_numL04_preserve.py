import json

ID = "83d542e3-c94b-4365-b8a9-070845b779ec"
live = json.load(open("_chk_numL04_live.json", encoding="utf-8"))

pre = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
# figure out structure
print("pre type:", type(pre))
entry = None
if isinstance(pre, dict):
    if ID in pre:
        entry = pre[ID]
    elif "number-L04" in pre:
        entry = pre["number-L04"]
    else:
        # search
        for k, v in pre.items():
            if isinstance(v, dict):
                if v.get("id") == ID:
                    entry = v.get("practice_data", v)
                    break
        else:
            print("keys sample:", list(pre.keys())[:10])
elif isinstance(pre, list):
    for v in pre:
        if v.get("id") == ID:
            entry = v.get("practice_data")
            break

if entry is None:
    print("NO PRE ENTRY FOUND")
else:
    # entry might be the practice_data or a wrapper
    ppd = entry.get("practice_data", entry) if isinstance(entry, dict) else entry
    for f in ["related_videos", "topic_links", "worked_examples"]:
        a = json.dumps(ppd.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
        print(f, "PRESERVED" if a == b else "CHANGED")
        if a != b:
            print("  PRE:", a[:400])
            print("  LIVE:", b[:400])
    print("pre practice_data keys:", list(ppd.keys()))
