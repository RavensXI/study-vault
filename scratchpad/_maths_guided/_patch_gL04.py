# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "0b5aef96-fa58-45be-a8fe-6d63c2baf002"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_geometry-L04_diagrams.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify: refetch and count figures live
req2 = urllib.request.Request(url + "&select=practice_data", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
n = 0
if "<svg" in live["guided"]["opener"].get("display", ""):
    n += 1
for t in ("bronze", "silver", "gold"):
    if "<svg" in live["guided"]["teach"][t].get("display", ""):
        n += 1
    for p in live["problem_bank"][t]:
        if "<svg" in p.get("display", ""):
            n += 1
print("live figures:", n)
