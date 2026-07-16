import os, json, urllib.request
ID="ee087e5f-7971-4f5d-b6e0-2fe13585d6f4"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_L03.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
print("top keys:", list(pd.keys()))
