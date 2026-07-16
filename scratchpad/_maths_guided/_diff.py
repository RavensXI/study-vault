import json
live=json.load(open("_live_L07.json",encoding="utf-8"))
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
ID="6623fba3-fb9e-4353-80c4-35ed1d88f47e"
print("pre type:", type(pre))
entry=None
for e in pre:
    if e.get("id")==ID or e.get("key")=="graphs-L07": entry=e
pdp=entry.get("practice_data",entry)
print("pdp keys:", list(pdp.keys()))
for f in ["related_videos","topic_links","worked_examples"]:
    a=json.dumps(pdp.get(f),sort_keys=True,ensure_ascii=False)
    b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
    print("="*30, f, "match:", a==b)
    if a!=b:
        print("PRE :",a[:1000])
        print("LIVE:",b[:1000])
