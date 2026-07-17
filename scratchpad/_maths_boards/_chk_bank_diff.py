import json
ID="32acb3ec-b5ac-410b-984c-d9008683af8e"
live=json.load(open("_live_algL06_eduqas.json",encoding="utf-8"))["practice_data"]
dump=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
entry=[r for r in dump if r.get("id")==ID][0]
pre=entry["practice_data"]
for tier in ["bronze","silver","gold"]:
    lb=live["problem_bank"][tier]; pb=pre["problem_bank"][tier]
    print(f"=== {tier}: pre {len(pb)} live {len(lb)} ===")
    for i,(p,l) in enumerate(zip(pb,lb)):
        dchg = p.get("display")!=l.get("display")
        schg = p.get("solutions")!=l.get("solutions")
        ochg = p.get("options")!=l.get("options")
        if dchg or schg or ochg:
            print(f" [{i}] display {'CHG' if dchg else ''} sol {'CHG' if schg else ''} opts {'CHG' if ochg else ''}")
            if dchg: print("    pre:",p.get("display"),"| live:",l.get("display"))
            if schg: print("    pre sol:",p.get("solutions"),"| live:",l.get("solutions"))
            if ochg: print("    pre opts:",p.get("options"),"\n    live opts:",l.get("options"))
