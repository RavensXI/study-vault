# -*- coding: utf-8 -*-
import json, io, os, urllib.request
ID = "5f629e65-9b8c-4fcb-a334-93ee7e25d4ff"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-ocr_number-L03.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)
# verify round-trip
URL2 = URL + "&select=practice_data"
req2 = urllib.request.Request(URL2, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    got = json.loads(r.read().decode("utf-8"))[0]["practice_data"]
assert "guided" in got and "tier_guides" in got
assert got["problem_bank"]["bronze"][0]["guided_steps"][1]["answer"] == 8
assert got["guided"]["opener"]["steps"][0]["answer"] == 4
print("VERIFY live: guided+tier_guides present; opener box=4; bronze[0] box=8. OK")
