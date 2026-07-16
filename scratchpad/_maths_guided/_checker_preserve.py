import json, io
ID="76260360-c757-49f2-a1c6-cf0e389564c3"
live=json.load(io.open("_checker_live.json",encoding="utf-8"))
dump=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
# find pre entry
entry=None
if isinstance(dump,list):
    for e in dump:
        if e.get("id")==ID: entry=e; break
elif isinstance(dump,dict):
    entry=dump.get(ID) or dump.get("lessons",{}).get(ID)
print("pre entry found:", entry is not None, "| dump type:", type(dump).__name__)
if entry:
    pre = entry.get("practice_data", entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
        if not same:
            print("  PRE :", json.dumps(pre.get(f),ensure_ascii=False)[:400])
            print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:400])
    # keys present pre but missing live
    print("pre keys:", sorted(pre.keys()))
    print("live keys:", sorted(live.keys()))
