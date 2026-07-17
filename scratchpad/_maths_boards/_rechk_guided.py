import json
pd=json.load(open("_rechk_live.json",encoding="utf-8"))
g=pd["guided"]
print("GUIDED keys:",list(g.keys()))
op=g.get("opener",{})
print("\n===== OPENER =====")
print(json.dumps(op,ensure_ascii=False,indent=1))
