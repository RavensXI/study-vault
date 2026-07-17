import json, os, urllib.request
ID="f4f1368e-d7c2-41f1-8459-de2c0d500c3b"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
json.dump(pd, open("_live_fetch_algebra-L01.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("fetched keys:", list(pd.keys()))
