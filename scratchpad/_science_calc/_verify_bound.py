import json
d=json.load(open('_live2.json',encoding='utf-8'))
def boxcount(steps): return [k for k,s in enumerate(steps) if 'answer' in s]
prob=[]
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(d['problem_bank'][tier]):
        gs=p.get('guided_steps')
        it=p['input_type']
        if it=='multiple_choice':
            print(f'{tier}[{i}] MC (no guided_steps ok):', gs is None); continue
        # find phase index among boxes
        phase_pos=[k for k,s in enumerate(gs) if s.get('phase')=='substitute']
        boxes=[k for k,s in enumerate(gs) if 'answer' in s]
        pj=phase_pos[0] if phase_pos else None
        before=[b for b in boxes if pj is not None and b<pj]
        after=[b for b in boxes if pj is not None and b>=pj]
        ok = pj is not None and len(before)>=1 and len(after)>=2
        print(f'{tier}[{i}] boxes={len(boxes)} before={len(before)} at/after={len(after)} OK={ok}')
        if not ok: prob.append(f'{tier}[{i}]')
# check unit/accept preserved presence
print('problems missing phase or boundary:', prob)
