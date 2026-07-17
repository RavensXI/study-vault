import json
d=json.load(open('_chk_live_geoL03.json',encoding='utf-8'))
pb=d['problem_bank']
out=[]
for t in ['bronze','silver','gold']:
    for i,p in enumerate(pb[t]):
        h=p.get('hint','')
        flag=''
        if '\(' in h or '\frac' in h or '<' in h:
            flag=' <<< LATEX/HTML IN HINT'
        out.append(f"{t}[{i}] hint: {h}{flag}")
open('_chk_hints.txt','w',encoding='utf-8').write('\n'.join(out))
print('done')
