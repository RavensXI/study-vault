import json
c=json.load(open('_live_canonical.json',encoding='utf-8'))
pb=c['problem_bank']
for tier,arr in pb.items():
    if not isinstance(arr,list): continue
    for i,p in enumerate(arr):
        if 'accept' in p:
            print(tier,i,'accept=',p['accept'],'sol=',p['solutions'],'unit=',repr(p.get('unit')))
print('scan done')
