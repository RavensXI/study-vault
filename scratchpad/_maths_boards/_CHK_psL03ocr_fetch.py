# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "65e7a745-9820-431a-8b99-d96cd7514bf3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_live_psL03ocr.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze", "silver", "gold"):
    print(t, len(pb.get(t, [])), "| desc:", repr(pb.get(t + "_description")))
print("has guided:", "guided" in pd)
print("has tier_guides:", "tier_guides" in pd)
