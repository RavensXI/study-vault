# -*- coding: utf-8 -*-
import os, io, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_831aee1062.json", encoding="utf-8"))
ids = ["d148ded7-a7ce-47a7-b9a0-ab4de8d5ca05"]
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
for rid in ids:
    url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq." + rid
    req = urllib.request.Request(url, data=body, method="PATCH", headers={
        "apikey": key, "Authorization": "Bearer " + key,
        "Content-Type": "application/json", "Prefer": "return=minimal"})
    r = urllib.request.urlopen(req)
    print("PATCH", rid, r.status)
