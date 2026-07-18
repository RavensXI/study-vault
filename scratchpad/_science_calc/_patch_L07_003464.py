# -*- coding: utf-8 -*-
import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS = [
    "3c4aa292-cf3a-4cda-876d-25b030880bb5",
    "36c7ea77-c3be-464d-b057-4e7baf5754f5",
]

pd = json.load(io.open("lesson_physics-calculations-L07@003464e169.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

def patch(rid):
    url = BASE + "?id=eq." + rid
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json", "Prefer": "return=minimal",
    })
    with urllib.request.urlopen(req) as r:
        return r.status

def get(rid):
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

for rid in IDS:
    print(rid, "PATCH", patch(rid))

# verify byte-identical
ref = json.dumps(pd, sort_keys=True, ensure_ascii=False)
for rid in IDS:
    live = json.dumps(get(rid), sort_keys=True, ensure_ascii=False)
    print(rid, "identical to shard:", live == ref)
