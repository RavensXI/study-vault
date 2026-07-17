import json
ID="8e823cb5-7ee7-49af-b403-2c96a246c229"
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
# pre may be list or dict
entry=None
if isinstance(pre,list):
    for r in pre:
        if r.get("id")==ID: entry=r; break
elif isinstance(pre,dict):
    if ID in pre: entry=pre[ID]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: entry=v; break
print("type",type(pre).__name__, "found", entry is not None)
if entry is None and isinstance(pre,dict):
    print("dict keys sample:", list(pre.keys())[:5])
if entry:
    ppd = entry.get("practice_data", entry)
    live=json.load(open("_CHK_algL11_live.json",encoding="utf-8"))
    for f in ["related_videos","worked_examples","topic_links"]:
        same = json.dumps(ppd.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
        print(f, "PRESERVED" if same else "CHANGED")
        if not same:
            print("  PRE:",json.dumps(ppd.get(f),ensure_ascii=False)[:300])
            print("  LIVE:",json.dumps(live.get(f),ensure_ascii=False)[:300])
    # check pre solutions vs live solutions per tier
    ppb=ppd.get("problem_bank",{}); lpb=live.get("problem_bank",{})
    for t in ["bronze","silver","gold"]:
        for i,(a,b) in enumerate(zip(ppb.get(t,[]),lpb.get(t,[]))):
            if json.dumps(a.get("solutions"))!=json.dumps(b.get("solutions")) or a.get("display")!=b.get("display"):
                print(f"{t}[{i}] display/solution changed:")
                print("   pre disp:",a.get("display")," sol:",a.get("solutions"))
                print("   live disp:",b.get("display")," sol:",b.get("solutions"))
