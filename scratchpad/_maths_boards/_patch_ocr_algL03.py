# -*- coding: utf-8 -*-
import json, os, io, urllib.request
ID = "44ea1f33-8979-4e3e-83b8-d2bfd93e3ee5"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-ocr_algebra-L03.json", encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)

# verify round-trip
g = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
back = json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("guided present:", "guided" in back, "| tier_guides:", "tier_guides" in back,
      "| bronze desc:", bool(back["problem_bank"].get("bronze_description")),
      "| we count:", len(back.get("worked_examples", [])))
