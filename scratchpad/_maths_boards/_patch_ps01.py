# -*- coding: utf-8 -*-
import os, json, io, urllib.request

LID = "aa2fb8d9-f47f-4412-8231-28085ce43740"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-aqa_probability-statistics-L01.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % LID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# read back and confirm
req2 = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    got = json.load(r)[0]["practice_data"]
print("has guided:", "guided" in got, "has tier_guides:", "tier_guides" in got)
print("bronze[4] sols:", got["problem_bank"]["bronze"][4]["solutions"])
print("silver[2] has svg:", "<svg" in got["problem_bank"]["silver"][2]["display"])
print("related_videos preserved:", len(got.get("related_videos", [])), "worked_examples:", len(got.get("worked_examples", [])))
