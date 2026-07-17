import json, re
live = json.load(open('_live_pd_only.json', encoding='utf-8'))
issues=[]

def walk_boxes(steps):
    return [s for s in steps if 'answer' in s]

# check em dashes in student-facing strings
def scan_emdash(obj, path):
    if isinstance(obj, str):
        if '—' in obj:
            issues.append(f'EM DASH at {path}: {obj[:60]}')
    elif isinstance(obj, dict):
        for k,v in obj.items():
            if k=='note': continue
            scan_emdash(v, f'{path}.{k}')
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            scan_emdash(v, f'{path}[{i}]')
scan_emdash(live, 'pd')

# verify each bank problem: last guided box == solution; phase boundary count
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(live['problem_bank'][tier]):
        gs=p.get('guided_steps')
        sol=p.get('solutions')
        it=p.get('input_type')
        if gs:
            boxes=walk_boxes(gs)
            # boundary
            bidx=[j for j,s in enumerate(gs) if s.get('phase')=='substitute']
            if not bidx:
                issues.append(f'{tier}[{i}] no phase boundary')
            else:
                b=bidx[0]
                before=[s for s in gs[:b] if 'answer' in s]
                after=[s for s in gs[b:] if 'answer' in s]
                if len(before)<1: issues.append(f'{tier}[{i}] <1 box before boundary')
                if len(after)<2: issues.append(f'{tier}[{i}] <2 boxes after boundary ({len(after)})')
            # last box vs solution (single_value/fraction)
            if it=='single_value' and sol:
                if boxes[-1]['answer'] != sol[0] and not any(bx['answer']==sol[0] for bx in boxes):
                    issues.append(f'{tier}[{i}] no box equals solution {sol}')
        elif it!='multiple_choice':
            issues.append(f'{tier}[{i}] non-mc without guided_steps')

# print a solve table for manual confirm
print('=== BANK SOLVE (independent) ===')
def show(tier):
    for i,p in enumerate(live['problem_bank'][tier]):
        d=re.sub('<[^>]+>','',p['display'])[:70]
        print(f'{tier}[{i}] sol={p.get("solutions")} it={p.get("input_type")}  {d}')
        for m in p.get('misconceptions',[]):
            print(f'      expect={m.get("expect")} pat={m.get("pattern")}')
for t in ['bronze','silver','gold']: show(t)

print()
print('=== ISSUES ===')
for x in issues: print(x)
if not issues: print('none from automated pass')
