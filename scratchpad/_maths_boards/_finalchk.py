import os, json, urllib.request
ID="689bc7ff-0d4c-4f20-a83c-9476935f2ac9"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url,headers={"apikey":key,"Authorization":"Bearer "+key})
pd=json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd, open("_live_rp03_after.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("fetched live -> _live_rp03_after.json")
