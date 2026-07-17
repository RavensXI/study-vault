# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "99a85546-e8a4-455d-b1eb-1f9e25808cea"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

pd = json.load(open("lesson_maths-aqa_number-L04.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = BASE + "?id=eq." + ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# read back and confirm
req2 = urllib.request.Request(url + "&select=practice_data",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    back = json.load(r)[0]["practice_data"]
print("has guided:", "guided" in back, "has tier_guides:", "tier_guides" in back)
print("silver S3 solution:", back["problem_bank"]["silver"][3]["solutions"],
      "display:", back["problem_bank"]["silver"][3]["display"])
print("gold G4 solution:", back["problem_bank"]["gold"][4]["solutions"])
print("worked_examples preserved:", len(back["problem_bank"]["bronze"]),
      "bronze /", len(back["worked_examples"]), "worked")
