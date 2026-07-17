import json

base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
ID = "e0a5f715-f25c-4afd-b0c1-c71ea7f743e3"
live = json.load(open(base+"_CHK_L13_live.json", encoding="utf-8"))
pre = json.load(open(base+"_pre_dump_maths-aqa.json", encoding="utf-8"))
entry = next(e for e in pre if e.get("id")==ID)
pdp = entry["practice_data"]

for tier in ["bronze","silver","gold"]:
    lp = live["problem_bank"][tier]
    pp = pdp["problem_bank"].get(tier, [])
    print(f"\n=== {tier}: live {len(lp)} / pre {len(pp)} ===")
    for i,(a,b) in enumerate(zip(lp,pp)):
        da, db = a.get("display"), b.get("display")
        sa, sb = a.get("solutions"), b.get("solutions")
        oa, ob = a.get("options"), b.get("options")
        flags=[]
        if da!=db: flags.append("DISPLAY")
        if sa!=sb: flags.append(f"SOL {sb}->{sa}")
        if oa!=ob: flags.append("OPTS")
        print(f"  [{i}] {'|'.join(flags) if flags else 'unchanged-core'}  sol={sa}")
        if da!=db:
            print("      PRE :", db)
            print("      LIVE:", da)
