import json
live = json.load(open("_live_geometry-L07.json",encoding="utf-8"))
pd = json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
ID="aee11210-c33f-4e61-a25e-1ef101e95ab3"
entry=[e for e in pd if e.get("id")==ID][0]
old=entry["practice_data"]
for tier in ["bronze","silver","gold"]:
    ob=old["problem_bank"][tier]; nb=live["problem_bank"][tier]
    print(f"=== {tier}: old {len(ob)} new {len(nb)} ===")
    for i,(o,n) in enumerate(zip(ob,nb)):
        d = "SAME" if o.get("display")==n.get("display") else "DISPLAY CHANGED"
        s = "SAME" if o.get("solutions")==n.get("solutions") else f"SOL {o.get('solutions')}->{n.get('solutions')}"
        print(f" [{i}] {d} | {s}")
        if o.get("display")!=n.get("display"):
            print("    OLD:", o.get("display"))
            print("    NEW:", n.get("display"))
# method_card compare
print("method_card same:", json.dumps(old.get("method_card"),sort_keys=True)==json.dumps(live.get("method_card"),sort_keys=True))
