# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
CANON = "8767022d-e262-4979-b978-f78b8a249da8"

def get(i):
    url = BASE + "?id=eq." + i + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

canon = get(CANON)
with open("_L03yield_live.json", "w", encoding="utf-8") as f:
    json.dump(canon, f, ensure_ascii=False, indent=1)
print("canon keys:", list(canon.keys()))
pb = canon.get("problem_bank", {})
for t in ("bronze", "silver", "gold"):
    print(t, len(pb.get(t, [])))
print("has guided:", "guided" in canon, "has tier_guides:", "tier_guides" in canon)
