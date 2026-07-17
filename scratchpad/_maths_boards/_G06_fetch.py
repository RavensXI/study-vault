# -*- coding: utf-8 -*-
import json, os, urllib.request

ID = "683b816a-4d56-4d3d-911b-58cb3bca5efd"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(URL, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
json.dump(pd, open("_G06_live.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    print(t, "count:", len(pb.get(t, [])), "| desc:", repr(pb.get(t+"_description")))
print("has guided:", "guided" in pd, "| tier_guides:", "tier_guides" in pd, "| method_card:", "method_card" in pd)
