import json,re
live = json.load(open("_live_geometry-L07.json",encoding="utf-8"))
pd = json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
ID="aee11210-c33f-4e61-a25e-1ef101e95ab3"
old=[e for e in pd if e.get("id")==ID][0]["practice_data"]
print("OLD method_card:"); print(json.dumps(old["method_card"],ensure_ascii=False,indent=1))
print("\nNEW method_card content word count:", len(re.sub('<[^>]+>','',live["method_card"]["content"]).split()))
print("NEW steps:", live["method_card"]["steps"])
# tier_guides word budget
for t in ["bronze","silver","gold"]:
    wc=sum(len(re.sub('<[^>]+>','',s).split()) for s in live["tier_guides"][t]["steps"])
    print(f"tier_guides {t} steps words: {wc}, title: {live['tier_guides'][t]['title']}")
