# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "65e7a745-9820-431a-8b99-d96cd7514bf3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-ocr_probability-statistics-L03.json", encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)
