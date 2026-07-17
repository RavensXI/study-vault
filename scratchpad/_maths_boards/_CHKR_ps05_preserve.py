import json

ID = "b063ea7d-cb1c-40ca-a28b-ea79c429361f"
live = json.load(open("_CHKR_ps05_live.json", encoding="utf-8"))
pre = json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
row = [r for r in pre if r["id"]==ID]
if not row:
    print("PRE-DUMP: no matching id! titles:")
    for r in pre:
        print(" ", r["id"], r.get("title"))
    raise SystemExit
pdold = row[0]["practice_data"]
print("pre title:", row[0]["title"])
print("pre keys:", list(pdold.keys()))

# Fields that must be preserved byte-for-byte (spec section 9 / checker item 6)
for f in ["related_videos","topic_links","worked_examples"]:
    a = json.dumps(pdold.get(f), sort_keys=True, ensure_ascii=False)
    b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False)
    print(f"{f}: {'SAME' if a==b else 'DIFFERENT'}")
    if a!=b:
        print("  OLD:", a[:400])
        print("  NEW:", b[:400])

# Compare problem displays / solutions to see what changed in the bank
print("\n=== bank solution comparison ===")
for tier in ["bronze","silver","gold"]:
    old_t = pdold.get("problem_bank",{}).get(tier,[])
    new_t = live.get("problem_bank",{}).get(tier,[])
    print(f"{tier}: old {len(old_t)} new {len(new_t)}")
    for i in range(max(len(old_t),len(new_t))):
        os_ = old_t[i].get("solutions") if i<len(old_t) else None
        ns_ = new_t[i].get("solutions") if i<len(new_t) else None
        od = (old_t[i].get("display","")[:70]) if i<len(old_t) else "MISSING"
        if os_!=ns_:
            print(f"  [{i}] SOL CHANGED old={os_} new={ns_}")
