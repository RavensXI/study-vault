import os, json, urllib.request
ID="bc1ac13e-1cc0-42b3-a805-a8a3f35cbabb"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_check.json","w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=2))
print("TOP KEYS:", list(pd.keys()))
