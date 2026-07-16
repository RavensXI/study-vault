import json
live=json.load(open("_live_graphs_l04.json",encoding="utf-8"))
pb=live["problem_bank"]
issues=[]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        sol=p.get("solutions")
        if p.get("input_type")=="multiple_choice":
            if gs: issues.append(f"{tier}[{i}] MC has guided_steps")
            continue
        # last numeric box that is the "answer" phase should equal solution somewhere
        boxes=[s for s in gs if "answer" in s]
        # find the box that computes the solution
        final_reached = any(abs(b["answer"]-sol[0])<1e-9 for b in boxes)
        if not final_reached:
            issues.append(f"{tier}[{i}] no box hits solution {sol}")
        # boundary check
        phase_idx=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        live_after=[s for s in gs[phase_idx[0]:] if "answer" in s] if phase_idx else []
        before=[s for j,s in enumerate(gs[:phase_idx[0]]) if "answer" in s] if phase_idx else []
        if not phase_idx:
            issues.append(f"{tier}[{i}] no phase boundary")
        elif len(live_after)<2 or len(before)<1:
            issues.append(f"{tier}[{i}] boundary: before={len(before)} after={len(live_after)}")
print("ISSUES:", issues if issues else "none")
