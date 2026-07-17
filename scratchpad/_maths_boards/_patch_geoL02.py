# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "09fd71ca-ab66-4ea3-bf5b-0005f5ae5b6e"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-aqa_geometry-L02.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)
