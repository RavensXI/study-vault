import json
ID="4fd08300-e0fe-44c5-93cd-76b6d900c72d"
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
# pre may be list of rows or dict keyed
row=None
if isinstance(pre,list):
    for r in pre:
        if r.get("id")==ID: row=r; break
elif isinstance(pre,dict):
    row=pre.get(ID)
    if row is None:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==ID: row=v; break
print("row found:",row is not None)
if row:
    ppd=row.get("practice_data",row)
    print("pre keys:",list(ppd.keys()) if isinstance(ppd,dict) else type(ppd))
    live=json.load(open("_CHK_L05n_live.json",encoding="utf-8"))
    for f in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False) if isinstance(ppd,dict) else None
        b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f, "SAME" if a==b else "DIFF")
        if a!=b:
            print("  pre:",str(a)[:300])
            print("  live:",str(b)[:300])
    # bank displays/solutions preserved?
    if isinstance(ppd,dict) and "problem_bank" in ppd:
        for t in ["bronze","silver","gold"]:
            pb=ppd["problem_bank"].get(t,[]); lb=live["problem_bank"].get(t,[])
            print(f"{t}: pre {len(pb)} live {len(lb)}")
            for i in range(min(len(pb),len(lb))):
                if pb[i].get("display")!=lb[i].get("display"):
                    print(f"  [{i}] DISPLAY CHANGED\n    pre:{pb[i].get('display')}\n    live:{lb[i].get('display')}")
                if json.dumps(pb[i].get("solutions"))!=json.dumps(lb[i].get("solutions")):
                    print(f"  [{i}] SOLUTIONS CHANGED pre:{pb[i].get('solutions')} live:{lb[i].get('solutions')}")
