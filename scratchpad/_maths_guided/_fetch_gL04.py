# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "0b5aef96-fa58-45be-a8fe-6d63c2baf002"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_gL04_live_diag.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=2)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze", "silver", "gold"):
    print(t, "->", len(pb.get(t) or []), "problems")
