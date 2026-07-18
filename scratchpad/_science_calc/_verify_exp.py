import json
d=json.load(open('_live2.json',encoding='utf-8'))
bad=[]
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(d['problem_bank'][tier]):
        if p['input_type']=='multiple_choice': continue
        sol=p['solutions'][0]; acc=p.get('accept',0)
        for k,m in enumerate(p.get('misconceptions',[])):
            e=m.get('expect')
            if e is None: continue
            dist=abs(e-sol)
            if dist<=max(acc,0.005):
                bad.append((f'{tier}[{i}].misconceptions[{k}]',e,sol,acc,dist))
print('DEAD EXPECTS (inside accept window):',len(bad))
for x in bad: print(x)
