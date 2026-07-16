import json
live=json.load(open("_live_L04.json",encoding="utf-8"))
print("KEYS:", list(live.keys()))
print("has guided:", "guided" in live, "| has tier_guides:", "tier_guides" in live)
pb=live["problem_bank"]
for t in ["bronze","silver","gold"]:
    print(f"\n=== {t} ({len(pb[t])}) ===")
    for i,p in enumerate(pb[t]):
        print(f"[{i}] {p.get('display','')[:70]}")
        print(f"     sols={p.get('solutions')} calc={p.get('calculator')} itype={p.get('input_type')} has_guided_steps={'guided_steps' in p}")
