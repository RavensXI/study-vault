# -*- coding: utf-8 -*-
import os, json, io, urllib.request
SK = os.environ["SUPABASE_SERVICE_KEY"]
ALL = ["7876f55a-694d-4932-9bb9-43372697d1d9"]
pd = json.load(io.open("lesson_higher-calculations-L05@b2761124fc.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
for ID in ALL:
    url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": SK, "Authorization": f"Bearer {SK}",
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    r = urllib.request.urlopen(req)
    print(ID, r.status)

# verify byte-identical read-back
for ID in ALL:
    url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": SK, "Authorization": f"Bearer {SK}"})
    live = json.load(urllib.request.urlopen(req))[0]["practice_data"]
    same = json.dumps(live, sort_keys=True, ensure_ascii=False) == json.dumps(pd, sort_keys=True, ensure_ascii=False)
    print("readback identical:", ID, same)
