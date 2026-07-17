# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "5c10e089-e2cc-4a61-b6b3-951a8994a1a0"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-eduqas_geometry-L02.json", encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq." + ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)
# round-trip verify
rurl = url + "&select=practice_data"
rreq = urllib.request.Request(rurl, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(rreq) as r:
    live = json.load(r)[0]["practice_data"]
print("live has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("bronze0 single_value:", live["problem_bank"]["bronze"][0]["input_type"] == "single_value")
print("bronze0 svg:", "<svg" in live["problem_bank"]["bronze"][0]["display"])
print("silver5 sol (S5):", live["problem_bank"]["silver"][5]["solutions"])
print("gold3 sol (G3):", live["problem_bank"]["gold"][3]["solutions"])
print("gold0 svg:", "<svg" in live["problem_bank"]["gold"][0]["display"])
