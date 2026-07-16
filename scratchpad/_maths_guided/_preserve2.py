import json
live = json.load(open("_live_geometry-L05.json",encoding="utf-8"))
dump = json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
pre=None
for e in dump:
    if isinstance(e,dict):
        if e.get("id")=="75d6eee2-25e6-4977-b549-e965ddd6c735" or e.get("key")=="geometry-L05":
            pre=e; break
if pre is None:
    print("sample keys:", list(dump[0].keys()))
else:
    print("matched via", "id" if pre.get("id") else "key")
    ppd = pre.get("practice_data",pre)
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(ppd.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
        print(f, "PRESERVED" if same else "CHANGED")
        if not same:
            print("  PRE :",json.dumps(ppd.get(f))[:400])
            print("  LIVE:",json.dumps(live.get(f))[:400])
    # also report whether bank displays/solutions changed
    lb=live["problem_bank"]; pb=ppd.get("problem_bank",{})
    for tier in ["bronze","silver","gold"]:
        for i,(lp,pp) in enumerate(zip(lb.get(tier,[]),pb.get(tier,[]))):
            if lp.get("display")!=pp.get("display") or lp.get("solutions")!=pp.get("solutions"):
                print(f"BANK CHANGE {tier}[{i}]: disp {pp.get('display')!r} -> {lp.get('display')!r}; sol {pp.get('solutions')} -> {lp.get('solutions')}")
