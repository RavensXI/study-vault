import json
data = json.load(open("_CHK_gL03_live.json", encoding="utf-8"))
pd = data[0]["practice_data"]

print("===== OPENER =====")
op = pd["guided"].get("opener")
print(json.dumps(op, ensure_ascii=False, indent=1))

print("\n===== TEACH =====")
for tier in ["bronze","silver","gold"]:
    t = pd["guided"]["teach"].get(tier)
    print(f"\n--- teach.{tier} ---")
    print(json.dumps(t, ensure_ascii=False, indent=1))

print("\n===== TIER_GUIDES =====")
print(json.dumps(pd.get("tier_guides"), ensure_ascii=False, indent=1))

print("\n===== METHOD_CARD =====")
print(json.dumps(pd.get("method_card"), ensure_ascii=False, indent=1))
