# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "f4a69507-b194-4751-ae27-c657ddd23113"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-ocr_ratio-proportion-L04.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# verify readback
r2 = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(r2))[0]["practice_data"]
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("live bronze[6] sol:", live["problem_bank"]["bronze"][6]["solutions"],
      "silver[1] sol:", live["problem_bank"]["silver"][1]["solutions"],
      "silver[4] sol:", live["problem_bank"]["silver"][4]["solutions"])
