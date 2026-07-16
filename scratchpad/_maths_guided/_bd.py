import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_live_L01.json",encoding="utf-8"))
prob=0
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        gs=p.get("guided_steps")
        if not gs: 
            print(f"{tier}[{i}] NO guided_steps (input {p.get('input_type')})"); continue
        boxes=[s for s in gs if "answer" in s]
        before=[]; after=[]; seen=False
        for s in gs:
            if s.get("phase")=="substitute": seen=True
            if "answer" in s:
                (after if seen else before).append(s)
        pre_boxes=len(before); post_boxes=len(after)
        ok = pre_boxes>=1 and post_boxes>=2
        # main (non-check) answer among boxes: the box producing solution
        sols=p["solutions"]
        # find a box whose answer equals solution
        lands = any(b["answer"]==sols[0] for b in boxes)
        flag = "" if (ok and lands) else "  <<< PROBLEM"
        print(f"{tier}[{i}] before={pre_boxes} after={post_boxes} lands_on_sol={lands} sol={sols}{flag}")
