# -*- coding: utf-8 -*-
import os, json, urllib.request

SID = "a6f6c5da-0aa8-437c-b3fe-75b8a48d6714"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{SID}"

pd = json.load(open("lesson_maths-eduqas_ratio-proportion-L01.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(BASE, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify live
req2 = urllib.request.Request(BASE + "&select=practice_data",
                              headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
mA = live["problem_bank"]["gold"][1]["misconceptions"][0]
mB = live["problem_bank"]["silver"][5]["misconceptions"][1]
ok = (mA["pattern"] == "difference_as_share" and mA["expect"] == 2
      and mB["pattern"] == "left_out_own_part" and mB["expect"] == 3)
print("live verify ok:", ok)
