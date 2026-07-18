import os,json,io,urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
req=urllib.request.Request("https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.3d8807c5-5c59-40c2-b5d5-dd2ca7d7fb92&select=practice_data",headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd,io.open("_live_dfb.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("fetched live canonical")
