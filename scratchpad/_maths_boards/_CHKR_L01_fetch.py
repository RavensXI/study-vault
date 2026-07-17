import os, json, urllib.request
ID="d8a78aa2-a642-4dcd-9cb0-1aa5990761e7"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_CHKR_L01_live.json","w",encoding="utf-8").write(json.dumps(data[0],ensure_ascii=False,indent=1))
print("title:",data[0]["title"])
print("slug:",data[0]["slug"])
pd=data[0]["practice_data"]
print("top keys:",list(pd.keys()))
