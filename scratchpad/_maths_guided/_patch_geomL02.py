# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "fe5f6191-4452-4313-934d-8e5d16ba1032"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_geometry-L02_diagrams.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify live
vreq = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(vreq) as r:
    live = json.load(r)[0]["practice_data"]
n = 0
for t in ("bronze", "silver", "gold"):
    for p in live["problem_bank"][t]:
        if "<svg" in p["display"]:
            n += 1
for t in ("bronze", "silver", "gold"):
    if "<svg" in live["guided"]["teach"][t]["display"]:
        n += 1
print("live figures present:", n)
