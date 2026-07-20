import json,io,sys
live=json.load(open('_CHK_L01_live.json',encoding='utf-8'))
out=io.open('_chk_L01_dump.txt','w',encoding='utf-8')
def w(*a): out.write(' '.join(str(x) for x in a)+'\n')
for t in ['bronze','silver','gold']:
    w('#'*70); w('TIER',t)
    for i,p in enumerate(live['problem_bank'][t]):
        w('-'*60); w(f'{t}[{i}]  input_type={p.get("input_type")}')
        w(' display:',p.get('display'))
        if 'options' in p: w(' options:',json.dumps(p['options'],ensure_ascii=False))
        w(' solutions:',json.dumps(p.get('solutions'),ensure_ascii=False))
        w(' hint:',p.get('hint'))
        if 'chart' in p: w(' chart:',json.dumps(p['chart'],ensure_ascii=False))
        if 'image' in p: w(' image:',p['image'])
        for j,m in enumerate(p.get('misconceptions',[])):
            w(f'  misc[{j}]:',json.dumps(m,ensure_ascii=False))
        for j,s in enumerate(p.get('guided_steps',[])):
            w(f'  gs[{j}]:',json.dumps(s,ensure_ascii=False))
        if 'guided_skip_reason' in p: w('  SKIP:',p['guided_skip_reason'])
        for k in p:
            if k not in ('display','options','solutions','hint','chart','image','misconceptions','guided_steps','input_type','guided_skip_reason','id','ruler'):
                w('  otherfield',k,':',json.dumps(p[k],ensure_ascii=False)[:300])
w('#'*70); w('GUIDED')
w(json.dumps(live['guided'],ensure_ascii=False,indent=1))
w('#'*70); w('TIER_GUIDES')
w(json.dumps(live['tier_guides'],ensure_ascii=False,indent=1))
w('#'*70); w('METHOD_CARD')
w(json.dumps(live['method_card'],ensure_ascii=False,indent=1))
w('#'*70); w('DESCRIPTIONS')
for k in live['problem_bank']:
    if k.endswith('_description'): w(k,':',live['problem_bank'][k])
out.close()
print('done')
