import os, json, urllib.request, io
key=os.environ["SUPABASE_SERVICE_KEY"]
cid="b4864848-f50f-4481-9af7-983e8f3d20d8"
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{cid}&select=practice_data"
req=urllib.request.Request(url,headers={"apikey":key,"Authorization":f"Bearer {key}"})
data=json.load(urllib.request.urlopen(req))
with io.open("_live_L03.json","w",encoding="utf-8") as f:
    json.dump(data[0]["practice_data"], f, indent=1, ensure_ascii=False)
print("fetched, keys:", list(data[0]["practice_data"].keys()))
