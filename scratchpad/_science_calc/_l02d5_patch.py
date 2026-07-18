# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
pd = json.load(open("lesson_physics-calculations-L02@d5abd25397.json", encoding="utf-8"))
ids = ["1fcee1e4-25c6-422a-9b32-539ba52df304","97b8c30d-92e4-4a2c-9d98-4b5533563d78",
"8f183752-953f-4302-a53d-41fe21b79cc9","63de7fc1-1f7d-4629-9a0a-979c331b3c2f",
"11894e88-663d-40f5-aba8-dedfaad457b2","b9dc061d-677f-4436-9f91-c2dcd5aab429",
"becf88af-5466-4d94-9507-c0f6efdd69c2"]
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
for rid in ids:
    url = BASE + "?id=eq." + rid
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        print(rid, r.status)
