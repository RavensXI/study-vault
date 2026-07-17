# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "06eb8087-b07f-4bfa-8bc2-af97e3e06ebf"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_number-L01.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# read back and confirm
req2 = urllib.request.Request(url + "&select=practice_data", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("has guided:", "guided" in live, "has tier_guides:", "tier_guides" in live)
print("bronze[4] sols:", live["problem_bank"]["bronze"][4]["solutions"],
      "silver[6] sols:", live["problem_bank"]["silver"][6]["solutions"])
print("worked_examples preserved:", len(live["worked_examples"]),
      "related_videos:", live["related_videos"], "topic_links:", live["topic_links"])
