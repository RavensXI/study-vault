# -*- coding: utf-8 -*-
import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ALL = ["5bcd7990-52a4-49b0-8e2e-f3d0344df114", "37bd5221-58cb-47ff-8411-b45c3589c868"]

pd = json.load(io.open("lesson_biology-data-skills-L03@86a105121c.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

for i in ALL:
    req = urllib.request.Request(BASE + "?id=eq." + i, data=body, method="PATCH",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                 "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        print("PATCH", i, r.status)

# verify propagation: refetch and compare byte-identical
def get(i):
    req = urllib.request.Request(BASE + "?id=eq." + i + "&select=practice_data",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

live = [get(i) for i in ALL]
canon = json.dumps(live[0], sort_keys=True, ensure_ascii=False)
ok = all(json.dumps(x, sort_keys=True, ensure_ascii=False) == canon for x in live)
print("ALL ROWS BYTE-IDENTICAL:", ok)
print("matches shard:", json.dumps(pd, sort_keys=True, ensure_ascii=False) == canon)
print("gold[0] live solution:", live[0]["problem_bank"]["gold"][0]["solutions"])
