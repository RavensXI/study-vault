# -*- coding: utf-8 -*-
import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "2158f4af-be63-4d5e-a425-c961358999db"
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
pd = json.load(io.open("lesson_probability-statistics-L05_diagrams.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
vurl = URL + "&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
live = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
checks = {
    "silver[1]": "<svg" in live["problem_bank"]["silver"][1]["display"],
    "teach.bronze": "<svg" in live["guided"]["teach"]["bronze"]["display"],
    "teach.silver": "<svg" in live["guided"]["teach"]["silver"]["display"],
    "teach.gold": "<svg" in live["guided"]["teach"]["gold"]["display"],
}
print("live figures present:", checks)
print("all live:", all(checks.values()))
