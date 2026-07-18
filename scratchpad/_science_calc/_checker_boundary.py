import json
pd=json.load(open("_live_1fcee1e4.json",encoding="utf-8"))
issues=[]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        gs=p.get("guided_steps")
        if not gs:
            if p.get("input_type")!="multiple_choice" and "guided_skip_reason" not in p:
                issues.append(f"{tier}[{i}] missing guided_steps, no skip reason")
            continue
        boxes=[s for s in gs if "answer" in s]
        # find first phase index
        first_phase=None
        for j,s in enumerate(gs):
            if s.get("phase")=="substitute":
                first_phase=j; break
        if first_phase is None:
            issues.append(f"{tier}[{i}] NO phase boundary"); continue
        before=[s for s in gs[:first_phase] if "answer" in s]
        after=[s for s in gs[first_phase:] if "answer" in s]
        if len(before)<1: issues.append(f"{tier}[{i}] <1 box before boundary")
        if len(after)<2: issues.append(f"{tier}[{i}] <2 live boxes at/after boundary (has {len(after)})")
        # final box must land on solution (for numeric single_value) - check last box vs a computed check
# MC indices sanity
mc=[("gold",4,0),("gold",5,2),("bronze",7,1)]
for t,idx,exp in mc:
    got=pd["problem_bank"][t][idx]["solutions"][0]
    if got!=exp: issues.append(f"{t}[{idx}] MC solution {got}!={exp}")
# higher_only present & false everywhere (efficiency is foundation)
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        if p.get("higher_only") is True:
            issues.append(f"{tier}[{i}] flagged higher_only (efficiency is foundation)")
print("BOUNDARY/MC ISSUES:", issues if issues else "NONE")
# count problems per tier
print({t:len(pd["problem_bank"][t]) for t in ("bronze","silver","gold")})
