import json
pd = json.load(open("_ADVCHK_L05rp_live.json", encoding="utf-8"))["practice_data"]

print("###### GOLD[0] full:")
print(json.dumps(pd["problem_bank"]["gold"][0], indent=2, ensure_ascii=False))

g = pd.get("guided", {})
print("\n###### OPENER:")
print(json.dumps(g.get("opener"), indent=2, ensure_ascii=False))

print("\n###### TEACH:")
for tier in ["bronze","silver","gold"]:
    tw = g.get("teach", {}).get(tier)
    print(f"\n--- teach.{tier}:")
    print(json.dumps(tw, indent=2, ensure_ascii=False))

print("\n###### TIER_GUIDES:")
print(json.dumps(pd.get("tier_guides"), indent=2, ensure_ascii=False))
