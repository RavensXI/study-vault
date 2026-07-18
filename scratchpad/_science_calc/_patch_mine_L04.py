# -*- coding: utf-8 -*-
import os, json, io, urllib.request

SB = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
IDS = [
    "e6963758-b327-488c-87b4-177b336f29e9",
    "07e5d6c1-74ac-4da9-9942-7f440105e339",
    "5d2257b8-5623-4832-8653-d33cbc36e417",
    "60250fe9-465d-4667-9e15-4a601759e100",
    "17bbd05b-fda5-4bde-9932-fe62b9670913",
    "3dfe27ee-0fe0-4042-91f6-023c5d626e5b",
    "ca3b27a3-d2a5-4735-bb3e-507167e7ff77",
]
pd = json.load(io.open("lesson_chemistry-calculations-L04@b7b54666b8.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

for rid in IDS:
    url = "%s/rest/v1/lessons?id=eq.%s" % (SB, rid)
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json", "Prefer": "return=minimal",
    })
    r = urllib.request.urlopen(req)
    print(rid, r.status)
print("patched", len(IDS))
