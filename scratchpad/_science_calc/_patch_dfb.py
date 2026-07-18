# -*- coding: utf-8 -*-
import os, json, io, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS = ["3d8807c5-5c59-40c2-b5d5-dd2ca7d7fb92",
       "35080b85-8978-4a88-809b-a49c00a737d9"]
pd = json.load(io.open("lesson_biology-data-skills-L01@dfb8522d32.json", encoding="utf-8"))

def patch(rid):
    body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(BASE + "?id=eq." + rid, data=body, method="PATCH",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                 "Content-Type": "application/json", "Prefer": "return=minimal"})
    r = urllib.request.urlopen(req)
    return r.status

def get(rid):
    req = urllib.request.Request(BASE + "?id=eq." + rid + "&select=practice_data",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    return json.load(urllib.request.urlopen(req))[0]["practice_data"]

for rid in IDS:
    print("PATCH", rid, "->", patch(rid))

target = json.dumps(pd, ensure_ascii=False, sort_keys=True)
for rid in IDS:
    live = json.dumps(get(rid), ensure_ascii=False, sort_keys=True)
    print(rid, "byte-identical to shard:", live == target)
