# -*- coding: utf-8 -*-
import os, io, json, urllib.request

ID = "32c2c2c1-056b-4d78-b025-7e1e6f7ab3f3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq." + ID
pd = json.load(io.open("lesson_maths-ocr_probability-statistics-L01.json", encoding="utf-8"))

body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(BASE, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
vreq = urllib.request.Request(BASE + "&select=practice_data", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(vreq) as r:
    got = json.load(r)[0]["practice_data"]
print("live has guided:", "guided" in got, "| tier_guides:", "tier_guides" in got)
print("live bronze_description:", repr(got["problem_bank"].get("bronze_description"))[:60])
gs = got["problem_bank"]["gold"][0].get("guided_steps")
print("gold[0] guided_steps:", len(gs) if gs else None, "| svg in display:", "<svg" in got["problem_bank"]["gold"][0]["display"])
print("live == shard:", json.dumps(got, sort_keys=True) == json.dumps(pd, sort_keys=True))
