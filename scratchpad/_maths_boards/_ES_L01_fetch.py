import os, json, urllib.request
ID="a28fddf4-3ee1-48dc-b138-aa17facad15d"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
open("_ES_L01_live.json","w",encoding="utf-8").write(json.dumps(data[0],ensure_ascii=False,indent=1))
print("title:",data[0]["title"])
print("slug:",data[0]["slug"])
pd=data[0]["practice_data"]
print("top keys:",list(pd.keys()))
