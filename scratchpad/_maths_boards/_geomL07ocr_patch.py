# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "813488f9-f52c-4d54-8b53-c95eded2df12"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-ocr_geometry-L07.json", encoding="utf-8"))

url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
gurl = url + "&select=practice_data"
greq = urllib.request.Request(gurl, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(greq) as r:
    live = json.load(r)[0]["practice_data"]
print("live bronze sols:", [p["solutions"] for p in live["problem_bank"]["bronze"]])
print("live silver sols:", [p["solutions"] for p in live["problem_bank"]["silver"]])
print("live gold sols:", [p["solutions"] for p in live["problem_bank"]["gold"]])
print("has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("bronze[3] has svg:", "<svg" in live["problem_bank"]["bronze"][3]["display"])
print("match written:", json.dumps(live, sort_keys=True) == json.dumps(pd, sort_keys=True))
