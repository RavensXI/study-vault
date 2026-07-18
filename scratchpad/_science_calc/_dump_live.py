import os,json,io,urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="6c88ea75-6f77-4815-aaf3-4097ee027d91"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url,headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
json.dump(json.load(urllib.request.urlopen(req))[0]["practice_data"],io.open("_live_L06.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("dumped")
