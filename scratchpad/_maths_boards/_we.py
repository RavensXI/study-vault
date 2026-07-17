import json
ID="d6cc3827-bbe2-42ae-b116-7c8398b1bf70"
live=json.load(open("_live_L03.json",encoding="utf-8"))
dump=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
pre=[e for e in dump if e.get("id")==ID][0]["practice_data"]
print("=== PRE worked_examples ===")
print(json.dumps(pre.get("worked_examples"),indent=1,ensure_ascii=False))
print("=== LIVE worked_examples ===")
print(json.dumps(live.get("worked_examples"),indent=1,ensure_ascii=False))
print("=== PRE method_card ===")
print(json.dumps(pre.get("method_card"),indent=1,ensure_ascii=False)[:1200])
