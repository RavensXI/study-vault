# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "c8596747-22a3-47f0-8fe7-f0bc6c6d1101"
key = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-aqa_number-L03.json", encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": "Bearer " + key,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status:", r.status)
