import os,json,io,urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="6dc6da50-6253-4e4d-9806-83c34bc567cb"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd,io.open("_LIVE_L01.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print("fetched live")
