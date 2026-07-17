import os, json, urllib.request
ID="d84411dc-60b7-4f96-8f42-35486f5d7129"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_ADVCHK_L13_live.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
print("keys:", list(pd.keys()))
