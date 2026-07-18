# -*- coding: utf-8 -*-
import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ALL_IDS = ["123bb55f-1fc8-41fd-9b44-759bc466b766"]

pd = json.load(io.open("lesson_higher-calculations-L04@3c4fcb4f45.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")

for rid in ALL_IDS:
    req = urllib.request.Request(f"{BASE}?id=eq.{rid}", data=body, method="PATCH", headers={
        "apikey": KEY, "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        print("PATCH", rid, r.status)

# verify readback byte-identical
canon = json.dumps(pd, sort_keys=True, ensure_ascii=False)
for rid in ALL_IDS:
    req = urllib.request.Request(f"{BASE}?id=eq.{rid}&select=practice_data",
        headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        live = json.load(r)[0]["practice_data"]
    match = json.dumps(live, sort_keys=True, ensure_ascii=False) == canon
    print("READBACK", rid, "IDENTICAL" if match else "MISMATCH")
