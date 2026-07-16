import os, json, urllib.request
ID="7120daae-b81f-4fc3-9ae8-e6be798f1e06"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
key=os.environ["SUPABASE_SERVICE_KEY"]
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_l07.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
print("keys:", list(pd.keys()))
