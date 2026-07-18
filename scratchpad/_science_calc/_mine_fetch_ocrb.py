# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ids = ["5bcd7990-52a4-49b0-8e2e-f3d0344df114", "37bd5221-58cb-47ff-8411-b45c3589c868"]

def get(i):
    url = BASE + "?id=eq." + i + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

canon = get(ids[0]); other = get(ids[1])
with open("_mine_ocrb_live.json", "w", encoding="utf-8") as f:
    json.dump(canon, f, ensure_ascii=False, indent=1)
print("canon keys:", list(canon.keys()))
print("BYTE IDENTICAL 2 rows:", json.dumps(canon, sort_keys=True) == json.dumps(other, sort_keys=True))
pb = canon.get("problem_bank", {})
for t in ("bronze", "silver", "gold"):
    print(t, len(pb.get(t, [])))
print("has guided:", "guided" in canon, "has tier_guides:", "tier_guides" in canon)
