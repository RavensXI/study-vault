# -*- coding: utf-8 -*-
import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ALL_IDS = ["98e99005-69e2-4131-bd6b-6018ebac6e9d"]
pd = json.load(io.open("lesson_higher-calculations-L01@b5d94e42c2.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

for ID in ALL_IDS:
    url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    })
    with urllib.request.urlopen(req) as r:
        print("PATCH", ID, r.status)

# verify byte-identical propagation on every id
import hashlib
target = hashlib.sha256(json.dumps(pd, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
for ID in ALL_IDS:
    url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        live = json.load(r)[0]["practice_data"]
    h = hashlib.sha256(json.dumps(live, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    print("VERIFY", ID, "MATCH" if h == target else "MISMATCH")
