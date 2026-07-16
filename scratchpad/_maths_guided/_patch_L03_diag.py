# -*- coding: utf-8 -*-
import os, json, io, urllib.request

LID = "08c3ded7-4862-4609-b4bb-dee8b46b8329"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_probability-statistics-L03_diagrams.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % LID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)
