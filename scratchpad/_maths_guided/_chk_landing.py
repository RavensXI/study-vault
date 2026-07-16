import json
live=json.load(open("_CHK_geomL08_live.json",encoding="utf-8"))
pb=live["problem_bank"]
issues=[]
for tier in ["bronze","silver","gold"]:
    probs=pb[tier]
    seen={}
    for i,p in enumerate(probs):
        sol=p.get("solutions")
        # duplicate answer check
        key=json.dumps(sol)
        if key in seen: issues.append(f"{tier}[{i}] duplicate solution {sol} (also {tier}[{seen[key]}])")
        seen[key]=i
        gs=p.get("guided_steps")
        if not gs:
            if p.get("input_type")!="multiple_choice" and "guided_skip_reason" not in p:
                issues.append(f"{tier}[{i}] missing guided_steps")
            continue
        boxes=[s for s in gs if "answer" in s]
        if boxes:
            last=boxes[-1]["answer"]
            # last box should match a solution component (final landing) - check membership
            solvals=sol if isinstance(sol,list) else [sol]
            # for fraction [num,den] final boxes are num and den; for single last box == sol[0] typically
            # just report last box value + solution for manual read
        # count live boxes at/after phase
        phase_idx=None
        for j,s in enumerate(gs):
            if s.get("phase")=="substitute":
                phase_idx=j; break
        live_after=sum(1 for s in gs[phase_idx:] if "answer" in s) if phase_idx is not None else None
        before=sum(1 for s in gs[:phase_idx] if "answer" in s) if phase_idx is not None else None
        print(f"{tier}[{i}] sol={sol} nboxes={len(boxes)} lastbox={boxes[-1]['answer'] if boxes else None} before_phase={before} live_after={live_after}")
        if phase_idx is None: issues.append(f"{tier}[{i}] no phase:substitute tag")
        elif live_after<2: issues.append(f"{tier}[{i}] <2 live boxes after boundary ({live_after})")
        elif before<1: issues.append(f"{tier}[{i}] no box before boundary")
print("\nISSUES:", issues if issues else "NONE")
