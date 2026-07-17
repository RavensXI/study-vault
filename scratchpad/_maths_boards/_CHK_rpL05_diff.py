import json
base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
ID = "47e48001-4c4f-45ab-a400-ba16648b2569"
live = json.load(open(base+"_CHK_rpL05_LIVE.json", encoding="utf-8"))
pre_all = json.load(open(base+"_pre_dump_maths-aqa.json", encoding="utf-8"))
entry = next(it for it in pre_all if it["id"]==ID)
prepb = entry["practice_data"]["problem_bank"]
livepb = live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,(p,l) in enumerate(zip(prepb[tier], livepb[tier])):
        d_same = p.get("display")==l.get("display")
        s_same = p.get("solutions")==l.get("solutions")
        if not d_same or not s_same:
            print(f"{tier}[{i}] display_same={d_same} sol_same={s_same}")
            if not d_same:
                print("   PRE disp:", p.get("display"))
                print("   LIVE disp:", l.get("display"))
            if not s_same:
                print("   PRE sol:", p.get("solutions"), " LIVE sol:", l.get("solutions"))
    print(f"{tier}: pre n={len(prepb[tier])} live n={len(livepb[tier])}")
# Check for duplicate answers within tier
for tier in ["bronze","silver","gold"]:
    sols = [tuple(p["solutions"]) for p in livepb[tier]]
    dups = [s for s in set(sols) if sols.count(s)>1]
    print(f"{tier} dup solutions: {dups}")
