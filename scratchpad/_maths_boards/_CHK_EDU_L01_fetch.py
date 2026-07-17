import os, json, urllib.request
ID="89062264-f404-4e8e-8959-06c7a9fd0b7a"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_CHK_EDU_L01_live.json","w",encoding="utf-8").write(json.dumps(data[0],ensure_ascii=False,indent=1))
print("title:",data[0]["title"])
print("slug:",data[0]["slug"])
pd=data[0]["practice_data"]
print("top keys:",list(pd.keys()))
