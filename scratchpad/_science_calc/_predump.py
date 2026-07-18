import json,io
d=json.load(io.open('_pre_dump_all.json',encoding='utf-8'))
cid="6dc6da50-6253-4e4d-9806-83c34bc567cb"
row=[r for r in d if r.get('id')==cid][0]
pd=row['pd']
io.open('_pre_canonical.json','w',encoding='utf-8').write(json.dumps(pd,ensure_ascii=False,indent=1))
print('pre keys:', list(pd.keys()))
pb=pd['problem_bank']
for t in ['bronze','silver','gold']:
    print(t, len(pb.get(t,[])))
    for i,p in enumerate(pb[t]):
        print('  ',t,i,'sol=',p.get('solutions'),'ho=',p.get('higher_only'),'unit=',p.get('unit'),'accept=',p.get('accept'))
