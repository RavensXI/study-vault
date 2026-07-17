import json, os, urllib.request
LID='fc1f101a-9d1b-4eab-8bf8-8159f78caea2'
key=os.environ['SUPABASE_SERVICE_KEY']
shard=json.load(open('lesson_maths-ocr_graphs-L03.json',encoding='utf-8'))
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}'
body=json.dumps({'practice_data':shard}).encode('utf-8')
req=urllib.request.Request(url,data=body,method='PATCH',headers={
    'apikey':key,'Authorization':f'Bearer {key}',
    'Content-Type':'application/json','Prefer':'return=minimal'})
r=urllib.request.urlopen(req)
print('PATCH status',r.status)
# re-fetch and confirm
url2=url+'&select=practice_data'
req2=urllib.request.Request(url2,headers={'apikey':key,'Authorization':f'Bearer {key}'})
live=json.load(urllib.request.urlopen(req2))[0]['practice_data']
print('roundtrip == shard:', json.dumps(live,sort_keys=True,ensure_ascii=False)==json.dumps(shard,sort_keys=True,ensure_ascii=False))
print('live worked_examples count:', len(live['worked_examples']))
print('live topic_links:', json.dumps(live['topic_links'],ensure_ascii=False))
