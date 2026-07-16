import json

LID = "ab716e12-4427-45e8-9796-a9343073968a"
live = json.load(open("_live_l14.json", encoding="utf-8"))
pre = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
entry = next(e for e in pre if e["id"] == LID)
prepd = entry["practice_data"]

print("PRE practice_data keys:", list(prepd.keys()))
print()
for field in ["related_videos", "topic_links", "worked_examples"]:
    same = json.dumps(prepd.get(field), sort_keys=True) == json.dumps(live.get(field), sort_keys=True)
    print(f"{field}: preserved={same}")
    if not same:
        print("  PRE:", json.dumps(prepd.get(field))[:400])
        print("  LIVE:", json.dumps(live.get(field))[:400])

print("\n--- PROBLEM BANK compare (display+solutions) ---")
for tier in ["bronze","silver","gold"]:
    prep = prepd.get("problem_bank",{}).get(tier,[])
    livp = live.get("problem_bank",{}).get(tier,[])
    print(f"\n{tier}: pre={len(prep)} live={len(livp)}")
    for i,(a,b) in enumerate(zip(prep,livp)):
        da, db = a.get("display"), b.get("display")
        sa, sb = a.get("solutions"), b.get("solutions")
        oa, ob = a.get("options"), b.get("options")
        flag = ""
        if da!=db: flag+=" DISPLAY-CHANGED"
        if sa!=sb: flag+=" SOL-CHANGED"
        if oa!=ob: flag+=" OPTIONS-CHANGED"
        print(f"  [{i}] sol {sa}->{sb}{flag}")
        if da!=db:
            print(f"       preD: {da}")
            print(f"       livD: {db}")
