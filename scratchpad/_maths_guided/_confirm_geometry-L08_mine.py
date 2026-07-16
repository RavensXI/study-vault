import os, json, io, urllib.request
ID="0b095025-37bb-49e4-94da-6f898ad6f3e7"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})
live=json.load(urllib.request.urlopen(req))[0]["practice_data"]
mine=json.load(io.open("lesson_geometry-L08.json",encoding="utf-8"))
print("LIVE == FILE:", json.dumps(live,sort_keys=True,ensure_ascii=False)==json.dumps(mine,sort_keys=True,ensure_ascii=False))
