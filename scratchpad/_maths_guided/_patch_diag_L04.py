# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "1d039d5e-b358-4864-b935-b3334ba99d20"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_probability-statistics-L04_diagrams.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status", resp.status)

# verify
url2 = url + "&select=practice_data"
req2 = urllib.request.Request(url2, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
n = sum(1 for t in ("bronze", "silver", "gold") for p in live["problem_bank"][t] if "<svg" in p.get("display", ""))
n += sum(1 for t in ("silver", "gold") if "<svg" in live["guided"]["teach"][t].get("display", ""))
print("live displays containing <svg>:", n)
