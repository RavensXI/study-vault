import json

ID = "bbbab852-7730-4d87-a2db-9ba6413f97b1"
base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
live = json.load(open(base+"_CHK_algL02ocr_live.json", encoding="utf-8"))
pre_all = json.load(open(base+"_pre_dump_maths-ocr.json", encoding="utf-8"))
pre = next((r for r in pre_all if r["id"] == ID), None)
print("pre found:", pre is not None)
if pre:
    pd0 = pre["practice_data"]
    print("pre title:", pre["title"], "lesson_number:", pre["lesson_number"])
    print("pre top keys:", sorted(pd0.keys()))
    # Preservation checks
    for f in ["related_videos", "topic_links", "worked_examples"]:
        a = json.dumps(pd0.get(f), sort_keys=True, ensure_ascii=False)
        b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
        print(f"PRESERVE {f}: {'SAME' if a==b else 'CHANGED'}")
        if a != b:
            print("  PRE :", a[:400])
            print("  LIVE:", b[:400])
    # Problem display/solution/options preservation (should be same unless a fix noted)
    pb0 = pd0.get("problem_bank", {}); pb1 = live.get("problem_bank", {})
    for tier in ["bronze","silver","gold"]:
        p0 = pb0.get(tier, []); p1 = pb1.get(tier, [])
        print(f"\n{tier}: pre {len(p0)} vs live {len(p1)}")
        for i in range(max(len(p0),len(p1))):
            d0 = p0[i].get("display") if i < len(p0) else None
            d1 = p1[i].get("display") if i < len(p1) else None
            s0 = p0[i].get("solutions") if i < len(p0) else None
            s1 = p1[i].get("solutions") if i < len(p1) else None
            o0 = p0[i].get("options") if i < len(p0) else None
            o1 = p1[i].get("options") if i < len(p1) else None
            flag = ""
            if d0 != d1: flag += " DISPLAY-CHANGED"
            if s0 != s1: flag += " SOLUTION-CHANGED"
            if o0 != o1: flag += " OPTIONS-CHANGED"
            if flag:
                print(f"  [{i}]{flag}")
                print(f"     pre disp={d0} sol={s0}")
                print(f"     liv disp={d1} sol={s1}")
