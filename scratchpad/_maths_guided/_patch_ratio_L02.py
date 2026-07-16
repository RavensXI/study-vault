# -*- coding: utf-8 -*-
import os, io, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_ratio-proportion-L02.json", encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.8cea4310-541d-499d-a7e6-a8d82348cffd"
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": "Bearer " + key,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status", resp.status)

# verify round-trip
vurl = url + "&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": key, "Authorization": "Bearer " + key})
got = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
print("bronze[2].display:", got["problem_bank"]["bronze"][2]["display"])
print("bronze[4].display:", got["problem_bank"]["bronze"][4]["display"])
print("silver[5].solution:", got["problem_bank"]["silver"][5]["solutions"])
print("has guided:", "guided" in got, "has tier_guides:", "tier_guides" in got)
print("gold count:", len(got["problem_bank"]["gold"]),
      "opener boxes:", sum(1 for s in got["guided"]["opener"]["steps"] if s.get("answer") is not None))
