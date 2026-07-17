import os, json, urllib.request
ID="da768b8a-d62b-4701-8423-7988dc8325a7"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
pd=data[0]["practice_data"]
open("_live_L14.json","w",encoding="utf-8").write(json.dumps(pd,ensure_ascii=False,indent=2))
print("keys:", list(pd.keys()))
print("bytes:", len(json.dumps(pd)))
