# -*- coding: utf-8 -*-
import os, json, urllib.request, hashlib

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ids = ["1fcee1e4-25c6-422a-9b32-539ba52df304","97b8c30d-92e4-4a2c-9d98-4b5533563d78",
"8f183752-953f-4302-a53d-41fe21b79cc9","63de7fc1-1f7d-4629-9a0a-979c331b3c2f",
"11894e88-663d-40f5-aba8-dedfaad457b2","b9dc061d-677f-4436-9f91-c2dcd5aab429",
"becf88af-5466-4d94-9507-c0f6efdd69c2"]
def get(rid):
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]
for rid in ids:
    pd = get(rid)
    h = hashlib.md5(json.dumps(pd, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    print(rid, h)
