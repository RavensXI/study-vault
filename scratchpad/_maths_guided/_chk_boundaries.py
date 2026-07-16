import json, io
pd=json.load(io.open("_CHK_numL04_live.json",encoding="utf-8"))
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        gs=p.get("guided_steps")
        if not gs:
            print(f"{tier}[{i}] NO guided_steps (input_type={p.get('input_type')})"); continue
        # find phase boundary
        bidx=None
        for j,s in enumerate(gs):
            if s.get("phase")=="substitute": bidx=j; break
        boxes_before=sum(1 for s in gs[:bidx] if "answer" in s) if bidx is not None else None
        live_boxes=sum(1 for s in gs[bidx:] if "answer" in s) if bidx is not None else None
        last=gs[-1]
        has_check_done = "done" in last and "answer" in last
        flag=""
        if bidx is None: flag+=" NO-PHASE"
        else:
            if boxes_before<1: flag+=" <1-BEFORE"
            if live_boxes<2: flag+=" <2-LIVE"
        if not has_check_done: flag+=" NO-CHECK-DONE-LAST"
        # last answer must equal a stored solution? last is a check, not necessarily solution
        print(f"{tier}[{i}] sol={p['solutions']} before={boxes_before} live={live_boxes}{flag}")
