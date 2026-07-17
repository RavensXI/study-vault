import os, json, urllib.request
ID="d6cc3827-bbe2-42ae-b116-7c8398b1bf70"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_L03.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("keys:", list(pd.keys()))
