# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "1d039d5e-b358-4864-b935-b3334ba99d20"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_diag_L04_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=2)
print("saved; top keys:", list(pd.keys()))
