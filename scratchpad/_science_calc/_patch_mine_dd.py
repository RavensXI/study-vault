# -*- coding: utf-8 -*-
import os, json, io, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
IDS = [
    "8b8d72ed-5bdb-44b2-82e8-a7272e91d854",
    "bac68e76-4566-4e8d-abf9-dfc663d025c9",
    "96d403a1-e64b-4825-a7ff-65024b56a797",
    "4e49ce91-9170-40f1-9003-4874980679ec",
    "0cca9081-c7cf-434b-96ad-49b07dfe47b7",
    "e9e20197-3642-4e15-8859-0254705f3b39",
    "e6ccebe9-cd02-442f-be9c-e257fe791f66",
]
H = {"apikey": KEY, "Authorization": "Bearer " + KEY}

def get(i):
    req = urllib.request.Request(BASE + "?id=eq." + i + "&select=practice_data", headers=H)
    return json.load(urllib.request.urlopen(req))[0]["practice_data"]

# 1) propagation sanity: all 7 identical pre-patch
canon = json.dumps(get(IDS[0]), sort_keys=True, ensure_ascii=False)
for i in IDS[1:]:
    same = json.dumps(get(i), sort_keys=True, ensure_ascii=False) == canon
    print("pre-identical", i, same)

# 2) patch all with the new practice_data
new = json.load(io.open("lesson_chemistry-calculations-L01@dd9dbc80e5.json", encoding="utf-8"))
body = json.dumps({"practice_data": new}, ensure_ascii=False).encode("utf-8")
for i in IDS:
    req = urllib.request.Request(BASE + "?id=eq." + i, data=body, method="PATCH",
        headers={**H, "Content-Type": "application/json", "Prefer": "return=minimal"})
    r = urllib.request.urlopen(req)
    print("patched", i, r.status)

# 3) verify: re-fetch two rows and confirm byte-identical to shard
target = json.dumps(new, sort_keys=True, ensure_ascii=False)
for i in (IDS[0], IDS[3], IDS[6]):
    ok = json.dumps(get(i), sort_keys=True, ensure_ascii=False) == target
    print("post-identical-to-shard", i, ok)
