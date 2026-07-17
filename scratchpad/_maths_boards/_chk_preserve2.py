import json
pre=json.load(open('_pre_dump_maths-eduqas.json',encoding='utf-8'))
live=json.load(open('_chk_live_geoL03.json',encoding='utf-8'))
row=[r for r in pre if r['id']=='1e9d6465-1ec1-40a3-8138-958197366837'][0]
ppd=row['practice_data']
print('PRE top keys:', sorted(ppd.keys()))
print('LIVE top keys:', sorted(live.keys()))
for f in ['related_videos','topic_links','worked_examples']:
    a=json.dumps(ppd.get(f),ensure_ascii=False,sort_keys=True)
    b=json.dumps(live.get(f),ensure_ascii=False,sort_keys=True)
    print(f, 'IDENTICAL' if a==b else 'CHANGED', '(pre present=%s live present=%s)'%(f in ppd, f in live))
# check problem counts pre vs live
for t in ['bronze','silver','gold']:
    pc=len(ppd.get('problem_bank',{}).get(t,[]))
    lc=len(live.get('problem_bank',{}).get(t,[]))
    print(t,'pre',pc,'live',lc)
