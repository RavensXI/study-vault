import json
live=json.load(open("_live_graphs_l04.json",encoding="utf-8"))
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
lid="d9ac5103-221b-441e-81f2-d95e77269ea3"
entry=[v for v in pre if v.get("id")==lid][0]
ppd=entry["practice_data"]
print("=== PRE worked_examples ===")
print(json.dumps(ppd["worked_examples"],indent=1,ensure_ascii=False))
print("=== LIVE worked_examples ===")
print(json.dumps(live["worked_examples"],indent=1,ensure_ascii=False))
