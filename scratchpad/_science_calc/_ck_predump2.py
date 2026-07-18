import json
pre=json.load(open('_pre_dump_all.json',encoding='utf-8'))
cid="91158ba8-389c-4771-9735-326785654ccb"
entry=[e for e in pre if e.get('id')==cid][0]
print("entry keys",list(entry.keys()))
pdp=entry.get('practice_data') or entry.get('pd') or entry
if 'problem_bank' not in pdp:
    # maybe nested
    for k,v in entry.items():
        if isinstance(v,dict) and 'problem_bank' in v:
            pdp=v; print("pd under",k); break
pb=pdp.get('problem_bank',{})
print("pre pd keys",list(pdp.keys()))
for t in ('bronze','silver','gold'):
    for i,pr in enumerate(pb.get(t,[])):
        print(t,i,"higher_only=",pr.get('higher_only','MISS'),"sol=",pr.get('solutions'),"|",pr.get('display','')[:50])
