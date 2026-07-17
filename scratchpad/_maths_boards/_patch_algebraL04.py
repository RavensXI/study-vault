# -*- coding: utf-8 -*-
import json, os, io, urllib.request

ID = "431cf470-df7f-4654-8c83-df7aeb1e0322"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
SHARD = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\lesson_maths-aqa_algebra-L04.json"

pd = json.load(io.open(SHARD, encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = BASE + "?id=eq." + ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# read-back verify
vurl = BASE + "?id=eq." + ID + "&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(vreq) as r:
    got = json.load(r)[0]["practice_data"]
print("readback keys:", sorted(got.keys()))
print("silver[1] sol:", got["problem_bank"]["silver"][1]["solutions"])
print("gold[0] sol:", got["problem_bank"]["gold"][0]["solutions"])
print("has guided:", "guided" in got, "has tier_guides:", "tier_guides" in got)
print("bronze desc:", got["problem_bank"].get("bronze_description"))
print("MATCHES SHARD:", json.dumps(got, sort_keys=True) == json.dumps(pd, sort_keys=True))
