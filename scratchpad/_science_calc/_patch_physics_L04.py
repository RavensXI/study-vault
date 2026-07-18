# -*- coding: utf-8 -*-
import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ROWS = [
 "fc32b93d-51c8-4260-a199-7268fa33979d",  # canonical science-ocr-b
 "d2088054-e987-4e06-8480-34549a015d79",  # separate-sciences-ocr-b
]

pd = json.load(io.open("lesson_physics-calculations-L04@6ac34b4fe4.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

for rid in ROWS:
    url = BASE + "?id=eq." + rid
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        print("PATCH", rid, r.status)

# verify propagation: fetch back and compare byte-identical
canon = None
for rid in ROWS:
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        got = json.load(r)[0]["practice_data"]
    ser = json.dumps(got, sort_keys=True, ensure_ascii=False)
    if canon is None:
        canon = ser
        print("canonical serialized len", len(ser))
    else:
        print(rid, "byte-identical:" , ser == canon)
    # also confirm it matches what we wrote
    print(rid, "matches shard:", json.dumps(got, sort_keys=True, ensure_ascii=False) ==
          json.dumps(pd, sort_keys=True, ensure_ascii=False))
