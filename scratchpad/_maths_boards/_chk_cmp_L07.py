import json
pre=json.load(open("_pre_L07_pd.json",encoding="utf-8"))
live=json.load(open("_live_algebra-L07_CHK.json",encoding="utf-8"))["practice_data"]
# worked_examples
print("worked_examples equal:", pre["worked_examples"]==live["worked_examples"])
print("related_videos equal:", pre["related_videos"]==live["related_videos"])
print("topic_links equal:", pre["topic_links"]==live["topic_links"])
# method_card: spec allows trimming. compare
print("method_card equal:", pre.get("method_card")==live.get("method_card"))
print("--- pre method_card ---"); print(json.dumps(pre.get("method_card"),ensure_ascii=False)[:600])
print("--- problem displays pre vs live ---")
for tier in ["bronze","silver","gold"]:
    pb_pre=pre["problem_bank"].get(tier,[])
    pb_live=live["problem_bank"].get(tier,[])
    print(tier, "pre count", len(pb_pre), "live count", len(pb_live))
    for i,(a,b) in enumerate(zip(pb_pre,pb_live)):
        if a.get("display")!=b.get("display") or a.get("solutions")!=b.get("solutions"):
            print(f"  [{i}] display pre={a.get('display')} sol={a.get('solutions')} | live={b.get('display')} sol={b.get('solutions')}")
