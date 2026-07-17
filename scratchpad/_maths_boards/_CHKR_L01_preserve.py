import json
live=json.load(open("_CHKR_L01_live.json",encoding="utf-8"))["practice_data"]
predump=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
for e in predump:
    if e.get("id")=="d8a78aa2-a642-4dcd-9cb0-1aa5990761e7":
        old=e["practice_data"];break
print("OLD top keys:",list(old.keys()))
for f in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(old.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f"{f}: preserved={same}")
    if not same:
        print("  OLD:",json.dumps(old.get(f),ensure_ascii=False)[:300])
        print("  NEW:",json.dumps(live.get(f),ensure_ascii=False)[:300])

# Check problem_bank displays/solutions preserved (numbers unchanged) vs predump
print("\n--- problem_bank display/solutions diff ---")
ob=old.get("problem_bank",{}); nb=live.get("problem_bank",{})
for tier in ["bronze","silver","gold"]:
    o=ob.get(tier,[]); n=nb.get(tier,[])
    print(f"{tier}: old {len(o)} new {len(n)}")
    for i in range(max(len(o),len(n))):
        od=o[i]["display"] if i<len(o) else None
        nd=n[i]["display"] if i<len(n) else None
        osol=o[i].get("solutions") if i<len(o) else None
        nsol=n[i].get("solutions") if i<len(n) else None
        oopt=o[i].get("options") if i<len(o) else None
        nopt=n[i].get("options") if i<len(n) else None
        if od!=nd or osol!=nsol or oopt!=nopt:
            print(f"  [{i}] DIFF")
            print(f"      display old:{od} new:{nd}")
            print(f"      opts old:{oopt}")
            print(f"      opts new:{nopt}")
            print(f"      sol old:{osol} new:{nsol}")
