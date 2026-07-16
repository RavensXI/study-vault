import json
ID="bc1ac13e-1cc0-42b3-a805-a8a3f35cbabb"
live=json.load(open("_live_ratio_L01.json",encoding="utf-8"))
dump=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
entry=None
if isinstance(dump,list):
    for e in dump:
        if e.get("id")==ID: entry=e; break
pd=entry.get("practice_data") or entry
print("=== PRE-DUMP worked_examples ===")
print(json.dumps(pd["worked_examples"],indent=1,ensure_ascii=False))
print("=== LIVE worked_examples ===")
print(json.dumps(live["worked_examples"],indent=1,ensure_ascii=False))
