import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_live_l04.json",encoding="utf-8"))
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        gs=p.get("guided_steps")
        if not gs:
            print(f"{tier}[{i}] NO guided_steps, input={p.get('input_type')}"); continue
        pidx=[j for j,s in enumerate(gs) if isinstance(s,dict) and s.get("phase")=="substitute"]
        boxes=[j for j,s in enumerate(gs) if isinstance(s,dict) and "answer" in s]
        if not pidx:
            print(f"{tier}[{i}] NO phase tag!"); continue
        pj=pidx[0]
        boxes_before=[b for b in boxes if b<pj]
        boxes_at_after=[b for b in boxes if b>=pj]
        last=gs[-1]
        has_check_done = isinstance(last,dict) and "done" in last
        final_ans=gs[boxes[-1]]["answer"] if boxes else None
        sol=p["solutions"]
        # find the box that lands on solution (the substitute/main answer box, not the check)
        landing=[gs[b]["answer"] for b in boxes]
        ok_land = sol[0] in landing
        flag=""
        if len(boxes_before)<1: flag+=" <1-before!"
        if len(boxes_at_after)<2: flag+=" <2-after!"
        if not has_check_done: flag+=" no-done-last!"
        if not ok_land: flag+=" SOL-NOT-IN-BOXES!"
        print(f"{tier}[{i}] before={len(boxes_before)} at/after={len(boxes_at_after)} sol={sol} landings={landing}{flag}")
