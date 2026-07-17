import json

pre_all = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
ID = "e023770a-3bf9-43e4-9718-fc2da08eda49"
pre = next(r for r in pre_all if r["id"] == ID)["practice_data"]
live = json.load(open("_CHK_num01_live.json", encoding="utf-8"))

# Preservation fields per SPEC section 9 / checker brief item 6
for f in ["related_videos", "topic_links", "worked_examples"]:
    same = json.dumps(pre.get(f), sort_keys=True) == json.dumps(live.get(f), sort_keys=True)
    print(f"{f}: preserved={same}")
    if not same:
        print("  PRE :", json.dumps(pre.get(f))[:400])
        print("  LIVE:", json.dumps(live.get(f))[:400])

# What top-level keys exist pre vs live
print("pre keys:", sorted(pre.keys()))
print("live keys:", sorted(live.keys()))

# Any other pre field present in live but changed?
for k in pre:
    if k in ("related_videos","topic_links","worked_examples","guided","tier_guides","method_card","problem_bank"):
        continue
    same = json.dumps(pre.get(k), sort_keys=True) == json.dumps(live.get(k), sort_keys=True)
    if not same:
        print(f"OTHER CHANGED: {k}")
        print("  PRE :", json.dumps(pre.get(k))[:300])
        print("  LIVE:", json.dumps(live.get(k))[:300])

# Preserved problem displays/solutions vs pre (numbers shouldn't silently change unless repaired)
def bank_summary(pd):
    out={}
    pb=pd.get("problem_bank",{})
    for t in ("bronze","silver","gold"):
        arr=pb.get(t,[])
        out[t]=[(p.get("display"),p.get("solutions")) for p in arr]
    return out
pre_b=bank_summary(pre); live_b=bank_summary(live)
for t in ("bronze","silver","gold"):
    print(f"--- {t}: pre {len(pre_b[t])} live {len(live_b[t])}")
    for i,(pd_,ld_) in enumerate(zip(pre_b[t],live_b[t])):
        if pd_!=ld_:
            print(f"  [{i}] display/sol changed")
            print("    PRE :", pd_)
            print("    LIVE:", ld_)
