# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "0c881c07-49bb-49cd-8c89-41b971335061"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-aqa_algebra-L10.json", encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)
# read back to confirm
r2 = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
back = json.load(urllib.request.urlopen(r2))[0]["practice_data"]
print("readback bronze/silver/gold:", len(back["problem_bank"]["bronze"]), len(back["problem_bank"]["silver"]), len(back["problem_bank"]["gold"]))
print("has guided:", "guided" in back, "| has tier_guides:", "tier_guides" in back)
print("silver[1] has svg:", "<svg" in back["problem_bank"]["silver"][1]["display"])
print("matches file:", back == pd)
