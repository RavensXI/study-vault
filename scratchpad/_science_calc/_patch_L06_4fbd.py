# -*- coding: utf-8 -*-
import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ALL_IDS = ["8e511d1b-d282-4835-9969-c20a995cc72e"]

pd = json.load(io.open("lesson_higher-calculations-L06@4fbd5cf5b9.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

for rid in ALL_IDS:
    req = urllib.request.Request(BASE + "?id=eq." + rid, data=body, method="PATCH",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                 "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        print("PATCH", rid, r.status)

# verify byte-identical readback
for rid in ALL_IDS:
    req = urllib.request.Request(BASE + "?id=eq." + rid + "&select=practice_data",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        live = json.load(r)[0]["practice_data"]
    same = json.dumps(live, sort_keys=True, ensure_ascii=False) == json.dumps(pd, sort_keys=True, ensure_ascii=False)
    print("READBACK", rid, "identical:", same)
