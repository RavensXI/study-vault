import os,json,urllib.request
KEY=os.environ["SUPABASE_SERVICE_KEY"]
ID="aee11210-c33f-4e61-a25e-1ef101e95ab3"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd, open("_geomL07_LIVE_NOW.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("saved live", len(json.dumps(pd)))
