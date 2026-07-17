import json
pre=json.load(open('_pre_dump_maths-eduqas.json',encoding='utf-8'))
live=json.load(open('_chk_live_geoL03.json',encoding='utf-8'))
row=[r for r in pre if r['id']=='1e9d6465-1ec1-40a3-8138-958197366837'][0]
ppd=row['practice_data']
out=[]
out.append('PRE worked_examples:')
out.append(json.dumps(ppd.get('worked_examples'),ensure_ascii=False,indent=1))
out.append('\nLIVE worked_examples:')
out.append(json.dumps(live.get('worked_examples'),ensure_ascii=False,indent=1))
open('_chk_we.txt','w',encoding='utf-8').write('\n'.join(out))
print('n pre', len(ppd.get('worked_examples') or []), 'n live', len(live.get('worked_examples') or []))
