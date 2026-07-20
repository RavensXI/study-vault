import json
pre=json.load(open('../_geo_audit/_pre_dump_all.json',encoding='utf-8'))
e=[x for x in pre if x['id']=='42fe9f9d-e989-46b1-afef-c70754f8e4d3']
print(len(e))
p=e[0]['pd']
json.dump(p,open('_CHK_L01_pre.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
live=json.load(open('_CHK_L01_live.json',encoding='utf-8'))
for t in ['bronze','silver','gold']:
    a=p['problem_bank'][t]; b=live['problem_bank'][t]
    print(t,len(a),len(b))
    for i,(x,y) in enumerate(zip(a,b)):
        for f in ['chart','image','ruler','options','input_type','display','solutions']:
            if (f in x) != (f in y):
                print('  FIELD PRESENCE DIFF',t,i,f,f in x,f in y)
            elif f in x and x[f]!=y[f]:
                print('  DIFF',t,i,f)
                print('   old:',json.dumps(x[f],ensure_ascii=False)[:600])
                print('   new:',json.dumps(y[f],ensure_ascii=False)[:600])
for k in p:
    if k not in ('problem_bank',):
        same = k in live and live[k]==p[k]
        print('topkey',k,'same' if same else 'CHANGED')
print('live-only keys:',[k for k in live if k not in p])
