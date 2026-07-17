import json, os, urllib.request
LID='fc1f101a-9d1b-4eab-8bf8-8159f78caea2'
key=os.environ['SUPABASE_SERVICE_KEY']
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data'
req=urllib.request.Request(url,headers={'apikey':key,'Authorization':f'Bearer {key}'})
d=json.load(urllib.request.urlopen(req))[0]['practice_data']
json.dump(d,open('_fixL03_live.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('pd keys',list(d.keys()))
print('=== LIVE worked_examples ===')
print(json.dumps(d.get('worked_examples'),ensure_ascii=False,indent=1))
print('=== LIVE topic_links ===')
print(json.dumps(d.get('topic_links'),ensure_ascii=False,indent=1))
