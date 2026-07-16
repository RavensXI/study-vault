import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ID = "2603a7c5-7660-4a4c-943d-78f2a112009e"
live = json.load(open("_ck_L01_live.json", encoding="utf-8"))
dump = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
pre = None
for e in dump:
    if e.get("id") == ID:
        pre = e.get("practice_data"); break

pw = pre.get("worked_examples")
lw = live.get("worked_examples")
print("PRE count:", len(pw), "LIVE count:", len(lw))
print("\n=== PRE worked_examples ===")
print(json.dumps(pw, indent=1, ensure_ascii=False))
print("\n=== LIVE worked_examples ===")
print(json.dumps(lw, indent=1, ensure_ascii=False))
