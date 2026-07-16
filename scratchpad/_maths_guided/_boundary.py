import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_live_geometry-L08.json",encoding="utf-8"))
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        gs=p.get("guided_steps")
        if not gs:
            print(f"{tier}[{i}] NO guided_steps (input={p.get('input_type')})"); continue
        boxes=[s for s in gs if "answer" in s]
        # find first phase substitute
        firstphase=None
        for j,s in enumerate(gs):
            if s.get("phase")=="substitute": firstphase=j;break
        boxes_before=sum(1 for s in gs[:firstphase] if "answer" in s) if firstphase is not None else len(boxes)
        boxes_after=sum(1 for s in gs[firstphase:] if "answer" in s) if firstphase is not None else 0
        # non-numeric answers
        nonnum=[s.get("answer") for s in boxes if not isinstance(s.get("answer"),(int,float))]
        flag=""
        if firstphase is None: flag+=" NO_PHASE"
        if boxes_before<1: flag+=" <1_BEFORE"
        if boxes_after<2: flag+=" <2_AFTER"
        if nonnum: flag+=f" NONNUM{nonnum}"
        print(f"{tier}[{i}] boxes={len(boxes)} before={boxes_before} after={boxes_after}{flag}")
