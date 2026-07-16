import json
live=json.load(open("_live_geometry-L04.json",encoding="utf-8"))
pre=json.load(open("_predump_geometry-L04.json",encoding="utf-8"))
for f in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(pre.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
    print(f, "PRESERVED" if same else "CHANGED")
    if not same:
        print("  PRE:", json.dumps(pre.get(f))[:500])
        print("  LIVE:", json.dumps(live.get(f))[:500])
# method_card allowed to be trimmed
print("method_card pre keys:", list(pre.get("method_card",{}).keys()))
print("method_card live keys:", list(live.get("method_card",{}).keys()))
# problem_bank comparison: displays/solutions/options/input_type
for tier in ["bronze","silver","gold"]:
    pl=pre["problem_bank"][tier]; ll=live["problem_bank"][tier]
    print(f"\n== {tier}: pre {len(pl)} live {len(ll)} ==")
    for i,(p,l) in enumerate(zip(pl,ll)):
        for key in ["display","solutions","options","input_type"]:
            if json.dumps(p.get(key))!=json.dumps(l.get(key)):
                print(f"  [{i}] {key} CHANGED")
                print(f"      pre : {json.dumps(p.get(key))}")
                print(f"      live: {json.dumps(l.get(key))}")
