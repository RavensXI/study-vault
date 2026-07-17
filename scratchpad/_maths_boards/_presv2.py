import json
ID="e40e80e4-666f-4cce-a8b3-5f7bb6b5c490"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
entry=[e for e in pre if e["id"]==ID][0]
ppd=entry["practice_data"]
live=json.load(open("_live_gl02.json",encoding="utf-8"))
print("TITLE:",entry["title"])
print("PRE keys:",sorted(ppd.keys()))
print("LIVE keys:",sorted(live.keys()))
# Preservation fields
for f in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(ppd.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
    print(f"{f}: preserved={same}")
    if not same:
        print("  PRE:",json.dumps(ppd.get(f))[:400])
        print("  LIVE:",json.dumps(live.get(f))[:400])
# Compare problem displays & solutions preserved
def bank(pd): return pd.get("problem_bank",{})
pb_pre=bank(ppd); pb_live=bank(live)
for tier in ["bronze","silver","gold"]:
    pr=pb_pre.get(tier,[]); lv=pb_live.get(tier,[])
    print(f"\n{tier}: pre={len(pr)} live={len(lv)}")
    for i in range(max(len(pr),len(lv))):
        dp = pr[i]["display"] if i<len(pr) else "<none>"
        dl = lv[i]["display"] if i<len(lv) else "<none>"
        sp = pr[i].get("solutions") if i<len(pr) else None
        sl = lv[i].get("solutions") if i<len(lv) else None
        flag = "" if (dp==dl and sp==sl) else "  <-- CHANGED"
        if flag:
            print(f"  [{i}] sol pre={sp} live={sl}{flag}")
            print(f"      disp pre: {dp[:120]}")
            print(f"      disp liv: {dl[:120]}")
