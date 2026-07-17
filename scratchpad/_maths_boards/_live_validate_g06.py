import os,json,io,urllib.request
ID="9f0126b9-ab85-4cbc-bc94-5d1214d5c4c2"; KEY=os.environ["SUPABASE_SERVICE_KEY"]
u=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(u,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd,io.open("_live_g06ocr_check.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("fetched live -> _live_g06ocr_check.json")
