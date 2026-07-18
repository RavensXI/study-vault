import os, json, urllib.request
key=os.environ['SUPABASE_SERVICE_KEY']
cid="6c88ea75-6f77-4815-aaf3-4097ee027d91"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{cid}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
d=json.load(urllib.request.urlopen(req))
pd=d[0]['practice_data']
json.dump(pd, open('_live_canonical.json','w',encoding='utf-8'), indent=1, ensure_ascii=False)
print("fetched, keys:", list(pd.keys()))
