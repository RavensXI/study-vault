# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
CID = "4ef45adc-b491-4025-9906-f541fa8a7a8f"

url = BASE + "?id=eq." + CID + "&select=practice_data,title,slug,unit_id"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)

with open("_canonical_live.json", "w", encoding="utf-8") as f:
    json.dump(data[0], f, ensure_ascii=False, indent=1)

pd = data[0]["practice_data"]
print("title:", data[0]["title"])
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze", "silver", "gold"):
    print(t, "count:", len(pb.get(t, [])))
    print("  desc:", repr(pb.get(t + "_description")))
