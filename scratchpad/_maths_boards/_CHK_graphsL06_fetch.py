import os, json, urllib.request
ID="de6bd262-7fb6-4392-a5a3-e0cda56ea7ba"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_CHK_graphsL06_LIVE.json","w",encoding="utf-8").write(json.dumps(pd,indent=2,ensure_ascii=False))
print("keys:", list(pd.keys()))
