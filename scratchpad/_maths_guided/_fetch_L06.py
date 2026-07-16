import os, json, urllib.request
ID="622f7959-f9e9-45aa-b2bd-8a5b6698e357"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_L06.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
print("top keys:", list(pd.keys()))
