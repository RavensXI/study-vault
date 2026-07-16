# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "fe5f6191-4452-4313-934d-8e5d16ba1032"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_geomL02_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=2)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze", "silver", "gold"):
    print(tier, len(pb.get(tier, [])))
