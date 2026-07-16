import os, json, urllib.request
key = os.environ['SUPABASE_SERVICE_KEY']
ID = 'f6f5708d-edf9-42e6-81d8-49c3cf282310'
url = f'https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data'
req = urllib.request.Request(url, headers={'apikey':key,'Authorization':f'Bearer {key}'})
data = json.load(urllib.request.urlopen(req))
pd = data[0]['practice_data']
with open('_live_l06.json','w',encoding='utf-8') as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print('keys:', list(pd.keys()))
