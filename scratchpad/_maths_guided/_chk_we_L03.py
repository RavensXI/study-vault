import json, io
ID="d9df7fae-d515-4c06-94b6-9068029bd037"
dump=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
entry=next(v for v in dump if v.get("id")==ID)
pre=entry["practice_data"]
live=json.load(io.open("_CHK_L03_fresh.json",encoding="utf-8"))
print("=== PRE worked_examples ===")
print(json.dumps(pre["worked_examples"],ensure_ascii=False,indent=1))
print("=== LIVE worked_examples ===")
print(json.dumps(live["worked_examples"],ensure_ascii=False,indent=1))
