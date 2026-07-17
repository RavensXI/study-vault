import os, json, urllib.request
ID="80de6f33-3b1d-40af-9068-8e6fc132c36d"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_live_algebra-L07_CHK.json","w",encoding="utf-8").write(json.dumps(data[0], indent=1, ensure_ascii=False))
print("title:", data[0]["title"], "| slug:", data[0]["slug"])
pd=data[0]["practice_data"]
print("top keys:", list(pd.keys()))
