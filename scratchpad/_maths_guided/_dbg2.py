import json
live=json.load(open("_live_L04.json",encoding="utf-8"))
for tier in ["gold","bronze","silver"]:
    for j,prob in enumerate(live["problem_bank"][tier]):
        gs=prob.get("guided_steps",[])
        nlen=len(gs)
        nans=sum(1 for s in gs if "answer" in s)
        pidx=[i for i,s in enumerate(gs) if s.get("phase")=="substitute"]
        first=pidx[0] if pidx else None
        liveb=sum(1 for i,s in enumerate(gs) if first is not None and i>=first and "answer" in s)
        # last box lands on solution?
        lastans=[s["answer"] for s in gs if "answer" in s]
        print(f"{tier}[{j}] len={nlen} ans={nans} phase@{first} liveboxes={liveb} sols={prob.get('solutions')}")
