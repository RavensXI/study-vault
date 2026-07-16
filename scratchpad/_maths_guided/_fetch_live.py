import os, json, urllib.request
ID="560ef2dd-cbbd-4c48-a03c-192449cc74a6"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
key=os.environ["SUPABASE_SERVICE_KEY"]
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_probstats_L01.json","w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=2))
print("keys:", list(pd.keys()))
