# -*- coding: utf-8 -*-
import os, json, urllib.request

key = os.environ["SUPABASE_SERVICE_KEY"]
lid = "1d34f8fe-3649-4053-8b54-1c4e843d7669"
pd = json.load(open("lesson_graphs-L05_diagrams.json", encoding="utf-8"))

url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{lid}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
vurl = f"{url}&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": key, "Authorization": f"Bearer {key}"})
with urllib.request.urlopen(vreq) as r:
    live = json.load(r)[0]["practice_data"]
n = sum(1 for t in ("bronze", "silver", "gold") for p in live["problem_bank"][t] if "chart" in p)
print("charts live:", n)
