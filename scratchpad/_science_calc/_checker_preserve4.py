import json
pre = json.load(open("_pre_dump_all.json", encoding="utf-8"))
live = json.load(open("_live_3c4aa292.json", encoding="utf-8"))
cid = "3c4aa292-cf3a-4cda-876d-25b030880bb5"
e=[x for x in pre if x.get("id")==cid][0]
pdp=e["pd"]
print("pre pd keys:", sorted(pdp.keys()))
print("live keys:  ", sorted(live.keys()))
print()
for f in ("related_videos","worked_examples","topic_links","exam_context","method_card"):
    same=json.dumps(pdp.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f"{f}: preserved={same}")
    if not same:
        print("   PRE :", json.dumps(pdp.get(f),ensure_ascii=False)[:250])
        print("   LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:250])

# Compare bank problem displays & solutions (should mostly be preserved unless a fix)
print("\n--- bank display/solutions changes ---")
for tier in ("bronze","silver","gold"):
    prep=pdp.get("problem_bank",{}).get(tier,[])
    livp=live.get("problem_bank",{}).get(tier,[])
    print(f"{tier}: pre {len(prep)} live {len(livp)}")
    for i in range(max(len(prep),len(livp))):
        ps=prep[i] if i<len(prep) else {}
        ls=livp[i] if i<len(livp) else {}
        if ps.get("display")!=ls.get("display") or ps.get("solutions")!=ls.get("solutions"):
            print(f"  {tier}[{i}] CHANGED")
            print("    pre disp:", (ps.get('display') or '')[:120], "sol", ps.get('solutions'))
            print("    liv disp:", (ls.get('display') or '')[:120], "sol", ls.get('solutions'))
