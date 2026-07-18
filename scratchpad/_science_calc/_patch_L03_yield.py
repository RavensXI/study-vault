# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ALL_IDS = ["8767022d-e262-4979-b978-f78b8a249da8"]

pd = json.load(open("lesson_higher-calculations-L03@2a30c22d67.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

def patch(i):
    url = BASE + "?id=eq." + i
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        print("PATCH", i, r.status)

def get(i):
    url = BASE + "?id=eq." + i + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

for i in ALL_IDS:
    patch(i)

mine = json.dumps(pd, sort_keys=True, ensure_ascii=False)
for i in ALL_IDS:
    live = json.dumps(get(i), sort_keys=True, ensure_ascii=False)
    print("BYTE-IDENTICAL", i, live == mine)
