import json
live=json.load(open("_live_graphs_l04.json",encoding="utf-8"))
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
lid="d9ac5103-221b-441e-81f2-d95e77269ea3"
# pre may be dict keyed by id or list
entry=None
if isinstance(pre,dict):
    if lid in pre: entry=pre[lid]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==lid: entry=v; break
elif isinstance(pre,list):
    for v in pre:
        if v.get("id")==lid: entry=v; break
print("pre type",type(pre).__name__)
if entry is None:
    print("keys sample:", list(pre.keys())[:5] if isinstance(pre,dict) else pre[0].keys())
else:
    ppd=entry.get("practice_data",entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f, "UNCHANGED" if same else "CHANGED")
    # show problem displays pre vs live to check number edits
    print("pre keys:", list(ppd.keys()))
