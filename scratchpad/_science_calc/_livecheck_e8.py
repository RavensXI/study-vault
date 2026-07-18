import os, json, io, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.d9384cf5-c3b4-4d2d-8f46-346f2c9a8ac6&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    pd = json.load(r)[0]["practice_data"]
json.dump(pd, io.open("_livecanon_e8.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved live canonical")
