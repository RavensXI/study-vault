import json
pd = json.load(open("_CHK_L02_live.json",encoding="utf-8"))[0]["practice_data"]
teach = pd["guided"]["teach"]
for tier in ["bronze","silver","gold"]:
    print("="*60); print("TEACH", tier); print("="*60)
    print(json.dumps(teach.get(tier), indent=1, ensure_ascii=False))
