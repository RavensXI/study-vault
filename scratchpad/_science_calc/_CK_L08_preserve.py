import json

CANON = "af432bd7-94b6-4601-a30d-4356767061bb"
pre = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/_pre_dump_all.json", encoding="utf-8"))
live = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/_CK_L08_canonical.json", encoding="utf-8"))

entry = next(r for r in pre if r["id"] == CANON)
pd = entry["pd"]

print("=== PRE-DUMP keys ===", sorted(pd.keys()))
print("=== LIVE keys ===", sorted(live.keys()))
print()
# Preservation of untouched fields
for f in ["related_videos", "topic_links", "worked_examples", "exam_context", "method_card"]:
    same = json.dumps(pd.get(f), sort_keys=True) == json.dumps(live.get(f), sort_keys=True)
    print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
print()
# problem count and display/solution preservation per tier
for tier in ["bronze","silver","gold"]:
    pp = pd.get("problem_bank",{}).get(tier,[])
    lp = live.get("problem_bank",{}).get(tier,[])
    print(f"--- {tier}: pre={len(pp)} live={len(lp)}")
    for i in range(max(len(pp),len(lp))):
        pd_disp = pp[i].get("display","")[:50] if i < len(pp) else "MISSING"
        lv_disp = lp[i].get("display","")[:50] if i < len(lp) else "MISSING"
        pd_sol = pp[i].get("solutions") if i < len(pp) else None
        lv_sol = lp[i].get("solutions") if i < len(lp) else None
        flag = "" if (pd_disp==lv_disp and pd_sol==lv_sol) else "  <-- DIFF"
        print(f"  [{i}] sol pre={pd_sol} live={lv_sol}{flag}")
        if pd_disp != lv_disp:
            print(f"       PRE : {pd_disp}")
            print(f"       LIVE: {lv_disp}")
