# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "a6f6c5da-0aa8-437c-b3fe-75b8a48d6714"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-eduqas_ratio-proportion-L01.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# verify round-trip
vurl = f"{url}&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
print("live has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("live gold[0] hint set:", bool(live["problem_bank"]["gold"][0].get("hint")))
print("live gold[0] expect0:", live["problem_bank"]["gold"][0]["misconceptions"][0].get("expect"))
