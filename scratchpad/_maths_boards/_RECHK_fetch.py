import os, json, urllib.request
ID="7f378aaa-68dc-4420-b952-f56d8349b1ed"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_rechk_live.json","w",encoding="utf-8").write(json.dumps(data[0]["practice_data"],ensure_ascii=False,indent=2))
print("title:",data[0].get("title"),"slug:",data[0].get("slug"))
pd=data[0]["practice_data"]
print("top keys:",list(pd.keys()))
