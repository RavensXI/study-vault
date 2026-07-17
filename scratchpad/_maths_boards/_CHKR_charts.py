import json
pd=json.load(open("_CHKR_live.json",encoding="utf-8"))["practice_data"]
pb=pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        if p.get("chart"):
            print(f"\n===== {t}[{i}] : {p['display'][:120]}")
            print(json.dumps(p["chart"],ensure_ascii=False))
