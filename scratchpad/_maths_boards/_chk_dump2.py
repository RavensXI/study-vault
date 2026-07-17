import json,re
d=json.load(open('_chk_live_geoL03.json'))
out=[]
g=d['guided']
out.append('OPENER keys: '+str(list(g.get('opener',{}).keys())))
op=g['opener']
for k,v in op.items():
    if k=='steps':
        for i,s in enumerate(v):
            out.append(f' opener.steps[{i}]: '+json.dumps(s,ensure_ascii=False))
    else:
        out.append(f' opener.{k}: '+json.dumps(v,ensure_ascii=False))
for tier in ['bronze','silver','gold']:
    tw=g.get('teach',{}).get(tier)
    out.append(f'\n===TEACH {tier}===')
    out.append(json.dumps(tw,ensure_ascii=False,indent=1))
out.append('\n===TIER_GUIDES===')
for tier in ['bronze','silver','gold']:
    tg=d['tier_guides'].get(tier)
    out.append(f'--- {tier} ---')
    out.append(json.dumps(tg,ensure_ascii=False,indent=1))
out.append('\n===METHOD_CARD===')
out.append(json.dumps(d.get('method_card'),ensure_ascii=False,indent=1))
open('_chk_dump2.txt','w',encoding='utf-8').write('\n'.join(out))
print('done')
