import os,urllib.request,json
key=os.environ['SUPABASE_SERVICE_KEY']
url='https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.8767022d-e262-4979-b978-f78b8a249da8&select=id,title,slug,practice_data'
req=urllib.request.Request(url, headers={'apikey':key,'Authorization':'Bearer '+key})
d=json.load(urllib.request.urlopen(req))[0]
print("TITLE:",d['title'],"| SLUG:",d['slug'])
pd=d['practice_data']
open('_live_fresh.json','w',encoding='utf-8').write(json.dumps(pd,ensure_ascii=False,indent=1))
pb=pd['problem_bank']
for tier in ('bronze','silver','gold'):
    for i,p in enumerate(pb[tier]):
        print(tier,i,'sol=',p.get('solutions'),'|',p['display'][:70])
