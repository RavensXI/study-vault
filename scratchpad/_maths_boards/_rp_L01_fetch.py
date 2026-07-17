# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "9a6f1e85-41b4-4b82-87c6-e919e48362a9"
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(URL, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_rp_L01_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze", "silver", "gold"):
    probs = pb.get(t) or []
    print(t, "count", len(probs))
    print("  desc:", (pb.get(t+"_description") or "")[:80])
print("has guided:", "guided" in pd)
print("has tier_guides:", "tier_guides" in pd)
print("has method_card:", "method_card" in pd)
