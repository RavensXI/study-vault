import json, io
ID="d9df7fae-d515-4c06-94b6-9068029bd037"
dump=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
entry=next(v for v in dump if v.get("id")==ID)
pre=entry["practice_data"]
live=json.load(io.open("_CHK_L03_fresh.json",encoding="utf-8"))
print("TITLE:", entry.get("title"), "LNUM:", entry.get("lesson_number"))
print("PRE keys:", sorted(pre.keys()))
print("LIVE keys:", sorted(live.keys()))
for f in ["related_videos","topic_links","worked_examples"]:
    same = json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print(f, "UNCHANGED" if same else "*** CHANGED ***")
# print pre problem displays/solutions to cross-check numbers weren't silently changed
pb=pre.get("problem_bank",{})
for tier in ["bronze","silver","gold"]:
    print("---PRE",tier,"---")
    for i,p in enumerate(pb.get(tier,[])):
        print(i, p.get("solutions"), "|", p.get("display","")[:70])
