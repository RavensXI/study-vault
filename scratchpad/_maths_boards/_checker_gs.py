import json
live=json.load(open("_LIVE_eduqas_L12.json",encoding="utf-8"))["practice_data"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        has=("guided_steps" in p); it=p.get("input_type")
        if has:
            gs=p["guided_steps"]
            boxes=[s for s in gs if "answer" in s]
            subidx=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
            first_sub=subidx[0] if subidx else None
            before=len([s for j,s in enumerate(gs) if "answer" in s and (first_sub is None or j<first_sub)])
            after=len([s for j,s in enumerate(gs) if "answer" in s and first_sub is not None and j>=first_sub])
            print(f"{tier}[{i}] {it} guided_steps: {len(boxes)} boxes, boundary@{first_sub}, before={before} after={after}, finals={[s['answer'] for s in boxes]}, sol={p['solutions']}")
        else:
            print(f"{tier}[{i}] {it} NO guided_steps")
