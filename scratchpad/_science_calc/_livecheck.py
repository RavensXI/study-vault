import os,json,io,urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
req=urllib.request.Request("https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.bbd5ca5d-b290-4754-9d0a-bd5f5085c82c&select=practice_data",headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd,io.open("_live_canon.json","w",encoding="utf-8"),ensure_ascii=False)
print("fetched live")
