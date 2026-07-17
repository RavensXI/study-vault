import json
ID="66a1ec53-d20f-4b82-b436-1b31fc88e998"
live=json.load(open("_LIVE_eduqas_L12.json",encoding="utf-8"))["practice_data"]
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
# pre may be dict keyed by id or list
entry=None
if isinstance(pre,dict):
    if ID in pre: entry=pre[ID]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: entry=v; break
elif isinstance(pre,list):
    for v in pre:
        if v.get("id")==ID: entry=v; break
print("pre entry found:", entry is not None)
if entry:
    pd = entry.get("practice_data", entry)
    print("pre keys:", list(pd.keys()))
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: preserved={same}")
        if not same:
            print("  PRE:", json.dumps(pd.get(f),ensure_ascii=False)[:400])
            print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:400])
    # problem count / displays / solutions preserved?
    prepb=pd.get("problem_bank",{}); livepb=live.get("problem_bank",{})
    for tier in ["bronze","silver","gold"]:
        pl=prepb.get(tier,[]); ll=livepb.get(tier,[])
        print(f"{tier}: pre {len(pl)} live {len(ll)}")
