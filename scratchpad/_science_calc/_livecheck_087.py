import os,json,io,urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
url="https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.e68bcd00-8b3f-47d3-9a5b-e327a9ddde48&select=practice_data"
req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
d=json.load(urllib.request.urlopen(req))
io.open("_live_087.json","w",encoding="utf-8").write(json.dumps(d[0]["practice_data"],ensure_ascii=False))
