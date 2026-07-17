# -*- coding: utf-8 -*-
import os, json, io, urllib.request
LID = "7f417926-0bef-4875-a7ad-7eb71bd15506"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\lesson_maths-eduqas_probability-statistics-L02.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % LID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status", resp.status)
