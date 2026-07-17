import json, re
live = json.load(open("_ADVCHK_L05rp_live.json", encoding="utf-8"))["practice_data"]
for i,w in enumerate(live["worked_examples"]):
    print(f"\n=== WE[{i}] [{w.get('difficulty')}] {w['question']}")
    for s in w["steps"]:
        c=re.sub('<[^>]+>','',s.get('content',''))
        print(f"   {s.get('label')}: {c}")
