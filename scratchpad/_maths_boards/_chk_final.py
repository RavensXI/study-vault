import json
live=json.load(open('_live_ps_L03.json',encoding='utf-8'))[0]['practice_data']
lp=live['problem_bank']
issues=[]
for t in ['bronze','silver','gold']:
    for i,p in enumerate(lp[t]):
        sol=p.get('solutions',[None])[0]
        # misconception expect vs solution collision
        for j,m in enumerate(p.get('misconceptions',[])):
            e=m.get('expect')
            if e is not None and e==sol:
                issues.append(f"{t}[{i}].misconceptions[{j}] expect {e} == solution {sol}")
        gs=p.get('guided_steps')
        if not gs:
            if p.get('input_type')!='multiple_choice':
                issues.append(f"{t}[{i}] no guided_steps and not MC")
            continue
        # final numeric box must equal solution
        numboxes=[s for s in gs if 'answer' in s]
        # boundary check
        phis=[k for k,s in enumerate(gs) if s.get('phase')=='substitute']
        if not phis:
            issues.append(f"{t}[{i}] no phase:substitute")
        else:
            bi=phis[0]
            before=[s for s in gs[:bi] if 'answer' in s]
            after=[s for s in gs[bi:] if 'answer' in s]
            if len(before)<1: issues.append(f"{t}[{i}] <1 box before boundary")
            if len(after)<2: issues.append(f"{t}[{i}] <2 live boxes at/after boundary ({len(after)})")
print("ISSUES:", len(issues))
for x in issues: print("  ", x)
print("OK" if not issues else "SEE ABOVE")
