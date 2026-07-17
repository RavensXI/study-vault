# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "24e576f2-0e8a-43bc-bacd-5397b4da617b"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_number-L06.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)
