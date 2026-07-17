import json
d=json.load(open('_fixL03_live.json',encoding='utf-8'))
pb=d['problem_bank']
issues=[]
for t in ['bronze','silver','gold']:
    for i,p in enumerate(pb[t]):
        sol=p.get('solutions') or p.get('solution')
        gs=p.get('guided_steps')
        disp=p.get('display','').replace(chr(10),' ')
        # collect final numeric box(es) in guided_steps
        boxes=[s for s in (gs or []) if 'answer' in s]
        finals=[b['answer'] for b in boxes[-2:]] if boxes else []
        print(f"{t}[{i}] sol={sol} finalboxes={[b['answer'] for b in boxes]} :: {disp[:55]}")
        # check misconception expects present shape
        for mc in p.get('misconceptions',[]):
            if 'expect' not in mc:
                issues.append(f"{t}[{i}] misconception missing expect key")
        # boundary check
        if gs:
            phase_idx=[j for j,s in enumerate(gs) if s.get('phase')=='substitute']
            live_boxes_after=[s for s in gs[phase_idx[0]:] if 'answer' in s] if phase_idx else []
            before_boxes=[s for s in gs[:phase_idx[0]] if 'answer' in s] if phase_idx else []
            if p.get('input_type')!='multiple_choice' and not p.get('guided_skip_reason'):
                if not phase_idx:
                    issues.append(f"{t}[{i}] no phase:substitute boundary")
                else:
                    if len(before_boxes)<1: issues.append(f"{t}[{i}] <1 setup box before boundary")
                    if len(live_boxes_after)<2: issues.append(f"{t}[{i}] <2 live boxes at/after boundary")
print('\n=== boundary/expect issues ===')
print('\n'.join(issues) if issues else 'none')
