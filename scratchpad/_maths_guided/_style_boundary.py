import json,io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
live=json.load(open('_live_l06.json',encoding='utf-8'))

# 1. em dash scan across all strings
emfound=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='note': continue
            walk(v,f'{path}.{k}')
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f'{path}[{i}]')
    elif isinstance(o,str):
        if '—' in o or '–' in o:
            emfound.append((path,o))
walk(live,'')
print('EM/EN DASH hits:',len(emfound))
for p,s in emfound: print('  ',p,'|',s[:80])

# 2. boundary check per bank problem
print('\n--- boundary check ---')
for tier,probs in live['problem_bank'].items():
    if not isinstance(probs,list): continue
    for i,p in enumerate(probs):
        gs=p.get('guided_steps')
        if not gs: 
            print(f'{tier}[{i}] NO guided_steps (input {p.get("input_type")})'); continue
        # boxes = steps with 'answer'
        boxidx=[j for j,s in enumerate(gs) if 'answer' in s]
        phaseidx=[j for j,s in enumerate(gs) if s.get('phase')=='substitute']
        if not phaseidx:
            print(f'{tier}[{i}] NO phase tag'); continue
        ph=phaseidx[0]
        before=[j for j in boxidx if j<ph]
        after=[j for j in boxidx if j>=ph]
        flag='' if (len(before)>=1 and len(after)>=2) else '  <<< VIOLATION'
        print(f'{tier}[{i}] boxes_before={len(before)} boxes_at/after={len(after)}{flag}')
