import json
pd = json.load(open("_CHK_L02_live.json",encoding="utf-8"))[0]["practice_data"]
g = pd["guided"]
print("guided keys:", list(g.keys()))
print("\n===== OPENER =====")
print(json.dumps(g.get("opener"), indent=1, ensure_ascii=False))
