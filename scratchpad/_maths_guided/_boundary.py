import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_pd.json",encoding="utf-8"))
bad=[]
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][t]):
        gs=p.get("guided_steps")
        if not gs:
            if p.get("input_type")!="multiple_choice" and not p.get("guided_skip_reason"):
                bad.append(f"{t}[{i}] no guided_steps")
            continue
        boxes=[s for s in gs if "answer" in s]
        # find first phase substitute index
        pi=None
        for idx,s in enumerate(gs):
            if s.get("phase")=="substitute": pi=idx; break
        before=sum(1 for s in gs[:pi] if True) if pi is not None else None
        live_boxes=sum(1 for s in gs[pi:] if "answer" in s) if pi is not None else 0
        steps_before = pi if pi is not None else len(gs)
        if pi is None:
            bad.append(f"{t}[{i}] NO phase boundary")
        else:
            if steps_before<1: bad.append(f"{t}[{i}] <1 step before boundary")
            if live_boxes<2: bad.append(f"{t}[{i}] only {live_boxes} live boxes at/after boundary")
        # last box must equal a stored solution
        last_box=[s for s in gs if "answer" in s]
        finalans=last_box[-1]["answer"] if last_box else None
        # find the box whose answer equals the solution (the result box, not the check)
        sols=p["solutions"]
        has_sol_box=any(abs(s["answer"]-sols[0])<1e-9 for s in last_box if isinstance(s["answer"],(int,float)))
        if not has_sol_box:
            bad.append(f"{t}[{i}] no box lands on solution {sols}")
        # last step should be a check (done note)
        if not gs[-1].get("done"):
            bad.append(f"{t}[{i}] final step lacks 'done' (check)")
print("BOUNDARY/STRUCTURE ISSUES:")
for b in bad: print("  ",b)
if not bad: print("  none")
