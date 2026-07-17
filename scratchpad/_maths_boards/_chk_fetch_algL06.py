import os, json, urllib.request
ID="32acb3ec-b5ac-410b-984c-d9008683af8e"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_live_algL06_eduqas.json","w",encoding="utf-8").write(json.dumps(data[0], indent=1, ensure_ascii=False))
print("title:", data[0]["title"], "| slug:", data[0]["slug"])
pd=data[0]["practice_data"]
print("top keys:", list(pd.keys()))
