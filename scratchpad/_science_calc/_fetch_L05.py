import os, json, urllib.request
KEY=os.environ['SUPABASE_SERVICE_KEY']
ID='5145c094-e59a-4b76-b50f-368197215ca4'
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug'
req=urllib.request.Request(url, headers={'apikey':KEY,'Authorization':f'Bearer {KEY}'})
data=json.load(urllib.request.urlopen(req))[0]
json.dump(data['practice_data'], open('_live_L05.json','w',encoding='utf-8'), indent=2, ensure_ascii=False)
pb=data['practice_data']['problem_bank']
print('title', data['title'])
for t in ('bronze','silver','gold'):
    print(t, len(pb.get(t,[])), [ (p['solutions'], p.get('unit')) for p in pb[t] ])
