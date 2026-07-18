# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

def get(rid):
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY,
        "Authorization": "Bearer " + KEY,
    })
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    return data[0]["practice_data"]

ids = [
    "3c4aa292-cf3a-4cda-876d-25b030880bb5",
    "36c7ea77-c3be-464d-b057-4e7baf5754f5",
]
pds = {}
for rid in ids:
    pds[rid] = get(rid)

with open("_canonical_L07.json", "w", encoding="utf-8") as f:
    json.dump(pds["3c4aa292-cf3a-4cda-876d-25b030880bb5"], f, ensure_ascii=False, indent=1)

# byte-identical check
a = json.dumps(pds[ids[0]], sort_keys=True, ensure_ascii=False)
b = json.dumps(pds[ids[1]], sort_keys=True, ensure_ascii=False)
print("rows equal (semantically):", a == b)
print("canonical keys:", list(pds[ids[0]].keys()))
