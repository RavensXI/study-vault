import json
live=json.load(open('_chk_L04_de190166.json',encoding='utf-8'))
issues=[]
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='note': continue
            scan(v,f'{path}.{k}')
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,f'{path}[{i}]')
    elif isinstance(o,str):
        if '—' in o: issues.append(('EMDASH',path,o[:70]))
        if '–' in o: issues.append(('ENDASH',path,o[:70]))
scan(live,'')
print('dash issues:',issues)
def cb(steps,path):
    for i,s in enumerate(steps):
        if 'answer' in s and not isinstance(s['answer'],(int,float)):
            print('NON-NUMERIC',f'{path}[{i}]',s['answer'])
for t in ['bronze','silver','gold']:
    cb(live['guided']['teach'][t]['steps'],f'teach.{t}')
cb(live['guided']['opener']['steps'],'opener')
def last_box(steps):
    vals=[s['answer'] for s in steps if 'answer' in s]
    return vals[-1] if vals else None
for t in ['bronze','silver']:
    for j,p in enumerate(live['problem_bank'][t]):
        sol=p['solutions'][0]
        gs=p.get('guided_steps',[])
        lb=last_box(gs)
        phase_idx=[i for i,s in enumerate(gs) if s.get('phase')=='substitute']
        bb=sum(1 for s in gs[:phase_idx[0]] if 'answer' in s) if phase_idx else 'NO-PHASE'
        ba=sum(1 for s in gs[phase_idx[0]:] if 'answer' in s) if phase_idx else 'NO-PHASE'
        print(f'{t}[{j}] sol={sol} last={lb} match={lb==sol} before={bb} after={ba}')
