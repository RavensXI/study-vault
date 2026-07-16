# -*- coding: utf-8 -*-
import os, json, io, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "007f6c38-d280-4dd8-801d-5bb62c612eb2"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
pd = json.load(io.open("lesson_number-L04.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
  "apikey": key, "Authorization": "Bearer "+key,
  "Content-Type": "application/json", "Prefer": "return=minimal",
})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)
