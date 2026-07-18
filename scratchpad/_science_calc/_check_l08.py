# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

def fetch(rowid):
    url = BASE + "?id=eq." + rowid + "&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY,
        "Authorization": "Bearer " + KEY,
    })
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    return data[0]["practice_data"]

canonical = "539110f5-5600-4dde-bee7-54fb60554f18"
others = ["06772e71-a44d-47fa-967d-7ae17524126b", "1cc093ed-5247-4a15-b162-fcc764763d2b"]

pd = fetch(canonical)
with open("_live_canonical.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)

can_str = json.dumps(pd, ensure_ascii=False, sort_keys=True)
for oid in others:
    opd = fetch(oid)
    ostr = json.dumps(opd, ensure_ascii=False, sort_keys=True)
    print(oid, "IDENTICAL" if ostr == can_str else "DIFFERENT")

print("canonical bytes:", len(can_str))
