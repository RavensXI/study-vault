import json
live=json.load(open("_CHK_LIVE_fresh.json",encoding="utf-8"))["practice_data"]
# find pre-dump entry
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
ID="39bdcd12-eb3d-45b1-b0c5-d8e2257610df"
entry=None
if isinstance(pre,list):
    for e in pre:
        if e.get("id")==ID or e.get("slug")=="quadratic-graphs":
            entry=e;break
elif isinstance(pre,dict):
    entry=pre.get(ID) or pre.get("quadratic-graphs")
    if entry is None:
        for k,v in pre.items():
            if isinstance(v,dict) and (v.get("id")==ID or v.get("slug")=="quadratic-graphs"):
                entry=v;break
print("pre type:",type(pre), "found entry:",entry is not None)
if entry is None:
    if isinstance(pre,list):
        print("sample keys:",list(pre[0].keys())[:10] if pre else "empty")
        print("ids:",[e.get("id") for e in pre][:5])
    else:
        print("top keys:",list(pre.keys())[:10])
else:
    ppd=entry.get("practice_data",entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(ppd.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
        print(f, "PRESERVED" if same else "CHANGED")
        if not same:
            print("  PRE:",json.dumps(ppd.get(f))[:300])
            print("  LIVE:",json.dumps(live.get(f))[:300])
