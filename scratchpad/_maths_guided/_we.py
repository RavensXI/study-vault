import json, io
ID="6623fba3-fb9e-4353-80c4-35ed1d88f47e"
d=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
pre=[o for o in d if isinstance(o,dict) and o.get("id")==ID][0]["practice_data"]
live=json.load(io.open("_live_graphs_L07.json",encoding="utf-8"))
print("PRE worked_examples:")
print(json.dumps(pre["worked_examples"],ensure_ascii=False,indent=1))
print("\nLIVE worked_examples:")
print(json.dumps(live["worked_examples"],ensure_ascii=False,indent=1))
print("\nmethod_card CHANGED:", json.dumps(pre["method_card"],sort_keys=True,ensure_ascii=False)!=json.dumps(live["method_card"],sort_keys=True,ensure_ascii=False))
