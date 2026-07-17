# -*- coding: utf-8 -*-
import os, json, io, urllib.request

LID = "7f378aaa-68dc-4420-b952-f56d8349b1ed"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
SHARD = "lesson_maths-eduqas_geometry-L08.json"

pd = json.load(io.open(SHARD, encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")

url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % LID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# read back and verify the fix landed
url2 = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % LID
req2 = urllib.request.Request(url2, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
m = live["problem_bank"]["bronze"][5]["misconceptions"][0]
print("READBACK pattern:", m["pattern"], "| expect:", m["expect"])
print("READBACK message:", m["message"])
assert m["pattern"] == "partial_scalar" and m["expect"] == 1
print("VERIFIED live.")
