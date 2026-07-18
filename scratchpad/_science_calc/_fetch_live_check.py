import os,json,urllib.request
KEY=os.environ['SUPABASE_SERVICE_KEY']
ID='5145c094-e59a-4b76-b50f-368197215ca4'
url=f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data'
req=urllib.request.Request(url, headers={'apikey':KEY,'Authorization':f'Bearer {KEY}'})
pd=json.load(urllib.request.urlopen(req))[0]['practice_data']
json.dump(pd, open('_live_after_L05.json','w',encoding='utf-8'), indent=2, ensure_ascii=False)
print("fetched live")
