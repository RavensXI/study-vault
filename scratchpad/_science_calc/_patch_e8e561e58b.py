# -*- coding: utf-8 -*-
import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ALL = ["d9384cf5-c3b4-4d2d-8f46-346f2c9a8ac6", "7227fd03-247e-4573-bd70-9ef85155bc5a"]

pd = json.load(io.open("lesson_physics-calculations-L05@e8e561e58b.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

def patch(id):
    url = BASE + "?id=eq." + id
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        return r.status

for id in ALL:
    print("PATCH", id, "->", patch(id))

# verify byte-identical readback
def get(id):
    url = BASE + "?id=eq.%s&select=practice_data" % id
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

dumps = [json.dumps(get(id), sort_keys=True, ensure_ascii=False) for id in ALL]
local = json.dumps(pd, sort_keys=True, ensure_ascii=False)
print("all rows byte-identical:", len(set(dumps)) == 1)
print("match local shard:", all(d == local for d in dumps))
