# -*- coding: utf-8 -*-
import os, json, io, urllib.request, hashlib
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS = ["81a530c1-42dc-444f-bcff-64698040356b", "e0a376c7-e9e3-4af7-8d5a-658c322c24c9"]
pd = json.load(io.open("lesson_physics-calculations-L06@5d1494be41.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
for cid in IDS:
    req = urllib.request.Request(BASE + "?id=eq." + cid, data=body, method="PATCH", headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        print("PATCH", cid, r.status)
h0 = hashlib.sha1(json.dumps(pd, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
for cid in IDS:
    req = urllib.request.Request(BASE + "?id=eq." + cid + "&select=practice_data",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        live = json.load(r)[0]["practice_data"]
    h = hashlib.sha1(json.dumps(live, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    print("VERIFY", cid, "match" if h == h0 else "MISMATCH")
