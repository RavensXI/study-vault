# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "7f991a30-4b90-4e0e-8cf8-f37a3210006e"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-aqa_geometry-L04.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
vurl = url + "&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(vreq) as r:
    live = json.load(r)[0]["practice_data"]
print("live top keys:", sorted(live.keys()))
print("has guided:", "guided" in live, "has tier_guides:", "tier_guides" in live)
print("gold[2] opts:", live["problem_bank"]["gold"][2]["options"])
print("silver[2] sol:", live["problem_bank"]["silver"][2]["solutions"],
      "has svg:", "<svg" in live["problem_bank"]["silver"][2]["display"])
print("bronze[0] hint:", live["problem_bank"]["bronze"][0]["hint"])
print("bronze[0] expect:", live["problem_bank"]["bronze"][0]["misconceptions"][0]["expect"])
