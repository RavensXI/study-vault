import json
pd=json.load(open("_CHKR_live.json",encoding="utf-8"))["practice_data"]
g=pd["guided"]
print("GUIDED keys:",list(g.keys()))
print("\n=== OPENER ===")
print(json.dumps(g.get("opener"),ensure_ascii=False,indent=1))
