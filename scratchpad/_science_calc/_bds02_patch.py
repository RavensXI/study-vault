# -*- coding: utf-8 -*-
import os, json, io, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS = [
 "cc2d2229-8dc3-496f-abf9-5e3f9b2d14ec",
 "9b8be3c0-223a-45eb-a7b7-60fb472d3bc3",
 "0cd5633c-4eb9-4774-9b4c-9b3284f1fe97",
 "447cb61b-3a09-43e5-8afe-73aff0aad717",
 "64873952-6334-4961-bd24-f71c463ee5ac",
 "b4a888f7-b03f-4c51-b2e0-3146fc2e98b9",
 "63b9f62a-e314-4e79-abe3-6f430bbe459a",
]
pd = json.load(io.open("lesson_biology-data-skills-L02@551b362537.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

def patch(rid):
    url = BASE + "?id=eq." + rid
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        return r.status

def get(rid):
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

for rid in IDS:
    print("patch", rid, patch(rid))

# propagation check: canonical + 2 others byte-identical
canon = json.dumps(get(IDS[0]), ensure_ascii=False, sort_keys=True)
allok = True
for rid in IDS:
    live = json.dumps(get(rid), ensure_ascii=False, sort_keys=True)
    same = (live == canon)
    if not same: allok = False
    print("match", rid, same)
# also confirm live canonical equals the shard we built
shard = json.dumps(pd, ensure_ascii=False, sort_keys=True)
print("live==shard", canon == shard)
print("ALL_IDENTICAL", allok)
