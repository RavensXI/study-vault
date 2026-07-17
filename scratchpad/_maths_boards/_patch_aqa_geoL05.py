# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "93f6b9f1-7ae6-4f12-945b-a5b0c096dc09"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-aqa_geometry-L05.json", encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
gurl = url + "&select=practice_data"
greq = urllib.request.Request(gurl, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(greq) as r:
    live = json.load(r)[0]["practice_data"]
print("live has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("bronze[6] sol:", live["problem_bank"]["bronze"][6]["solutions"])
print("gold[0] sol:", live["problem_bank"]["gold"][0]["solutions"])
print("svg on bronze[0]:", "<svg" in live["problem_bank"]["bronze"][0]["display"])
print("match:", json.dumps(live, sort_keys=True) == json.dumps(pd, sort_keys=True))
