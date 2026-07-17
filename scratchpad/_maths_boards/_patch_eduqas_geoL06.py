# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "a36e47ae-bd22-4127-af9d-5b37e34c0b64"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-eduqas_geometry-L06.json", encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)
# verify readback
req2 = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    got = json.load(r)[0]["practice_data"]
pb = got["problem_bank"]
print("readback tiers:", {t: len(pb[t]) for t in ("bronze","silver","gold")})
print("silver[6] sol:", pb["silver"][6]["solutions"], "gold[0] sol:", pb["gold"][0]["solutions"], "gold[2] sol:", pb["gold"][2]["solutions"])
print("has guided:", "guided" in got, "tier_guides:", "tier_guides" in got)
print("worked_examples preserved count:", len(got["worked_examples"]), "related_videos:", got["related_videos"])
