# -*- coding: utf-8 -*-
import os, json, io, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "9a6f1e85-41b4-4b82-87c6-e919e48362a9"
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
pd = json.load(io.open("lesson_maths-ocr_ratio-proportion-L01.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
vurl = URL + "&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(vreq) as r:
    got = json.load(r)[0]["practice_data"]
print("has guided:", "guided" in got, "| tier_guides:", "tier_guides" in got)
print("bronze b1 display:", got["problem_bank"]["bronze"][1]["display"])
print("bronze b6 display:", got["problem_bank"]["bronze"][6]["display"])
print("silver s3 display:", got["problem_bank"]["silver"][3]["display"], "sol", got["problem_bank"]["silver"][3]["solutions"])
print("live == shard:", json.dumps(got, sort_keys=True) == json.dumps(pd, sort_keys=True))
