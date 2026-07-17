import os, json, urllib.request
key = os.environ.get("SUPABASE_SERVICE_KEY")
ID="df1cb4b9-09d1-4692-8674-2427dfe4c393"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_chk_live_ps5.json","w",encoding="utf-8").write(json.dumps(data[0],ensure_ascii=False,indent=1))
print("title:",data[0].get("title"),"slug:",data[0].get("slug"))
print("bytes:", len(json.dumps(data[0])))
