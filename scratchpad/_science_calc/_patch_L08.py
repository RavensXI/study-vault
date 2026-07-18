# -*- coding: utf-8 -*-
import os, json, io, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ALL_IDS = [
    "539110f5-5600-4dde-bee7-54fb60554f18",
    "06772e71-a44d-47fa-967d-7ae17524126b",
    "550f4c75-d1fa-4f6e-a2de-2a0f0b317bd8",
    "d8149466-9dcb-46b2-9599-bfe559f3bd36",
    "87deed73-6660-4019-bb2a-57f708b45ed8",
    "b18f7be8-c8d8-44e6-ac6d-4246b0a7fc27",
    "1cc093ed-5247-4a15-b162-fcc764763d2b",
]
pd = json.load(io.open("lesson_physics-calculations-L08@8ebcc02072.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

def patch(rid):
    url = BASE + "?id=eq." + rid
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        return r.status

for rid in ALL_IDS:
    print(rid, patch(rid))

# propagation check: fetch 2 rows, byte-compare canonical json
def get(rid):
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

canon = json.dumps(get(ALL_IDS[0]), sort_keys=True, ensure_ascii=False)
for rid in (ALL_IDS[1], ALL_IDS[4]):
    other = json.dumps(get(rid), sort_keys=True, ensure_ascii=False)
    print("byte-identical to canonical:", rid, other == canon)
