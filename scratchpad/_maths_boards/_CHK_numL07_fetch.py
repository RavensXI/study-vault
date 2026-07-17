import os, json, urllib.request
ID="8696e75e-f9fd-40ef-b3a4-df27f5811c73"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug,unit_id"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_CHK_numL07_live.json","w",encoding="utf-8").write(json.dumps(data[0], indent=1, ensure_ascii=False))
print("title:", data[0]["title"], "| slug:", data[0]["slug"])
pd=data[0]["practice_data"]
print("top keys:", list(pd.keys()))
