import os,json,urllib.request
key=os.environ['SUPABASE_SERVICE_KEY']
CID='98e99005-69e2-4131-bd6b-6018ebac6e9d'
def get(cid):
    url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{cid}&select=practice_data'
    req=urllib.request.Request(url,headers={'apikey':key,'Authorization':'Bearer '+key})
    return json.load(urllib.request.urlopen(req))[0]['practice_data']
d=get(CID)
json.dump(d,open('_canon_b5d94e42c2.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
title=d.get('method_card',{}).get('title')
print('TITLE:',title)
pb=d['problem_bank']
for t in ['bronze','silver','gold']:
    for i,p in enumerate(pb[t]):
        print(t,i,'sol',p['solutions'],'unit',p.get('unit'),'accept',p.get('accept'))
