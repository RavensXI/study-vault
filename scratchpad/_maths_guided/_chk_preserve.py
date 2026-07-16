import json

ID = "2603a7c5-7660-4a4c-943d-78f2a112009e"
KEY = "algebra-L01"

dump = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
# find entry
entry = None
if isinstance(dump, dict):
    for k, v in dump.items():
        if k == ID or k == KEY:
            entry = v; break
    if entry is None and "lessons" in dump:
        dump = dump["lessons"]
if entry is None and isinstance(dump, list):
    for row in dump:
        if row.get("id") == ID or row.get("key") == KEY or row.get("lesson_key") == KEY:
            entry = row; break
print("entry found:", entry is not None)
if entry is None:
    # show shape
    print("dump type", type(dump))
    if isinstance(dump, dict):
        print("top keys sample", list(dump.keys())[:5])
    elif isinstance(dump, list):
        print("list len", len(dump), "first keys", list(dump[0].keys()) if dump else None)
    raise SystemExit

pre = entry.get("practice_data") or entry.get("practice_data_json") or entry
live = json.load(open("_chk_L01_live.json", encoding="utf-8"))

for f in ["related_videos", "topic_links", "worked_examples"]:
    same = json.dumps(pre.get(f), sort_keys=True, ensure_ascii=False) == json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
    print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
    if not same:
        print("  PRE :", json.dumps(pre.get(f), ensure_ascii=False)[:400])
        print("  LIVE:", json.dumps(live.get(f), ensure_ascii=False)[:400])

# method_card: legitimately trimmable
print("\npre keys:", sorted(pre.keys()))
print("live keys:", sorted(live.keys()))
