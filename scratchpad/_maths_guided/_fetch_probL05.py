# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "2158f4af-be63-4d5e-a425-c961358999db"
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(URL, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_probL05_fresh_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=2)
print("fetched, top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze", "silver", "gold"):
    print(t, len(pb.get(t, [])))
