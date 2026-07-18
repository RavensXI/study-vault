import json, os, urllib.request, io
KEY=os.environ['SUPABASE_SERVICE_KEY']
ID='9733399d-1134-4649-8166-74c5b738c4a3'
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data'
req=urllib.request.Request(url, headers={'apikey':KEY,'Authorization':f'Bearer {KEY}'})
data=json.load(urllib.request.urlopen(req))
pd=data[0]['practice_data']
with io.open('_live_canon_fresh.json','w',encoding='utf-8') as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print('fetched, keys:', list(pd.keys()))
print('prereqs:', json.dumps(pd.get('topic_links',{}).get('prerequisites'), ensure_ascii=False))
