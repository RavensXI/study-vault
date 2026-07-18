import os, json, io, urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
rid="d42fee71-d641-4f20-90c6-8bde5e185595"
req=urllib.request.Request(f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{rid}&select=practice_data",headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd, io.open("_live_MY_readback.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("saved live readback")
