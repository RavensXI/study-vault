import os, json, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.8b8d72ed-5bdb-44b2-82e8-a7272e91d854&select=practice_data"
req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":"Bearer "+KEY})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd,open("_live_canon_dd.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("fetched live")
