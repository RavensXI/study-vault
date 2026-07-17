# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "9f5d0097-caa6-464c-9f1c-05ce6b836cc9"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-ocr_geometry-L04.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# verify round-trip
g = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("live bronze count:", len(live["problem_bank"]["bronze"]),
      "silver svg:", sum("<svg" in p["display"] for p in live["problem_bank"]["silver"]),
      "gold svg:", sum("<svg" in p["display"] for p in live["problem_bank"]["gold"]))
