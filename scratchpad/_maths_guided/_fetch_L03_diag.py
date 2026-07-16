# -*- coding: utf-8 -*-
import os, json, urllib.request

LID = "08c3ded7-4862-4609-b4bb-dee8b46b8329"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % LID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_L03_live_fresh.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=2)
print("saved. top keys:", list(pd.keys()))
