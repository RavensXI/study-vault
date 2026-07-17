# -*- coding: utf-8 -*-
import json

ID = "4d1cbe2a-483a-400a-9fee-5166ebde6a1b"
live = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_L11_live.json", encoding="utf-8"))
pre = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_pre_dump_maths-aqa.json", encoding="utf-8"))
prerow = next(r for r in pre if r.get("id") == ID)
pd = prerow["practice_data"]

print("PRE title:", prerow.get("title"))
print("PRE practice_data top keys:", list(pd.keys()))

# preserved: related_videos, topic_links, worked_examples
for f in ("related_videos", "topic_links", "worked_examples"):
    same = json.dumps(pd.get(f), sort_keys=True) == json.dumps(live.get(f), sort_keys=True)
    print(f"{f}: preserved={same}")
    if not same:
        print("   PRE:", json.dumps(pd.get(f))[:400])
        print("   LIVE:", json.dumps(live.get(f))[:400])

# compare each bank problem display/options/solutions/input_type
def bank(o):
    b = o.get("problem_bank", {})
    return {t: b.get(t, []) for t in ("bronze","silver","gold")}
pb_pre, pb_live = bank(pd), bank(live)
for t in ("bronze","silver","gold"):
    lp, ll = pb_pre[t], pb_live[t]
    print(f"\n== {t}: pre={len(lp)} live={len(ll)} ==")
    for i in range(max(len(lp), len(ll))):
        pp = lp[i] if i < len(lp) else None
        pl = ll[i] if i < len(ll) else None
        for key in ("display","options","solutions","input_type","calculator"):
            a = pp.get(key) if pp else None
            b = pl.get(key) if pl else None
            if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
                print(f"  [{i}].{key}:")
                print(f"      PRE : {a}")
                print(f"      LIVE: {b}")
