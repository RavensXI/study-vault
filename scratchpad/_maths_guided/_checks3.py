import json
live = json.load(open("_live_L02.json", encoding="utf-8"))
pre = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
lid = "fe5f6191-4452-4313-934d-8e5d16ba1032"
e = [x for x in pre if x["id"]==lid][0]
ppd = e["practice_data"]

print("=== PRE worked_examples ===")
print(json.dumps(ppd["worked_examples"], ensure_ascii=False, indent=1))
print("\n=== LIVE worked_examples ===")
print(json.dumps(live["worked_examples"], ensure_ascii=False, indent=1))
