import json, io, sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_live_L07_CHECKER.json",encoding="utf-8"))
pb=live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        it=p.get("input_type")
        gs=p.get("guided_steps")
        if it=="multiple_choice":
            print(f"{tier}[{i}] MC, sol={p['solutions']}, no guided (ok)" if not gs else f"{tier}[{i}] MC HAS guided")
            continue
        boxes=[s for s in gs if "answer" in s]
        before=[]; after=[]; seen=False
        for s in gs:
            if s.get("phase")=="substitute": seen=True
            if "answer" in s:
                (after if seen else before).append(s["answer"])
        sol=p["solutions"][0]
        lands = sol in [s["answer"] for s in boxes]
        print(f"{tier}[{i}] sol={sol} boxes={[s['answer'] for s in boxes]} before={len(before)} after={len(after)} lands={lands}")
