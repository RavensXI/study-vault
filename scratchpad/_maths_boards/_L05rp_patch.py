# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "ddbb6863-36ab-4898-8090-16df440a9d85"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-ocr_ratio-proportion-L05.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)
# verify round-trip
v = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(v))[0]["practice_data"]
print("live has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("bronze[4] sol:", live["problem_bank"]["bronze"][4]["solutions"],
      "| bronze[6] sol:", live["problem_bank"]["bronze"][6]["solutions"],
      "| gold[4] sol:", live["problem_bank"]["gold"][4]["solutions"])
print("live == shard:", json.dumps(live, sort_keys=True) == json.dumps(pd, sort_keys=True))
