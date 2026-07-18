# -*- coding: utf-8 -*-
import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS = [
 "67263d26-a899-4186-80ff-9f2d3ce8644e",
 "7d6a58c5-221a-4bf2-a4f8-fc2117125689",
 "17aa3fd9-0629-487b-91dd-97d207cab4a1",
 "6f3c8be8-8ccb-4e43-b8b2-64a04c0794b9",
 "159ad6f2-648d-4cb4-a7a0-81916be3ac14",
 "2b4b11fe-0694-41d4-bffa-9ef883b6aea1",
 "121dda89-35f5-46c6-8b6b-4646c12e0fe0",
]
pd = json.load(io.open("lesson_biology-data-skills-L01@d923f94f54.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

for rid in IDS:
    url = BASE + "?id=eq." + rid
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        print("PATCH", rid, r.status)

# verify propagation: fetch two ids, compare byte-identical to shard
canon_str = json.dumps(pd, ensure_ascii=False, sort_keys=True)
for rid in [IDS[0], IDS[3], IDS[6]]:
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        got = json.load(r)[0]["practice_data"]
    same = json.dumps(got, ensure_ascii=False, sort_keys=True) == canon_str
    print("VERIFY", rid, "identical" if same else "MISMATCH")
