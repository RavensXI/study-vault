# -*- coding: utf-8 -*-
import os, json, urllib.request

LID = "89689a46-7251-4c2a-900e-5fdc240dafd3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

pd = json.load(open("lesson_maths-ocr_graphs-L01.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(BASE + "?id=eq." + LID, data=body, method="PATCH",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
             "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# read back and diff
url = BASE + "?id=eq." + LID + "&select=practice_data"
req2 = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
print("live == shard:", json.dumps(live, sort_keys=True) == json.dumps(pd, sort_keys=True))
