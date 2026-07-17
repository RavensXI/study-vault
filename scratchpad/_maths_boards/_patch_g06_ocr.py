# -*- coding: utf-8 -*-
import os, json, urllib.request
LID = "fe05d231-ed67-4625-aa4d-791c6b1d9887"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % LID
pd = json.load(open("lesson_maths-ocr_geometry-L06.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)
# read back and confirm
req2 = urllib.request.Request(URL + "&select=practice_data", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    back = json.load(r)[0]["practice_data"]
print("readback keys:", sorted(back.keys()))
print("bronze n:", len(back["problem_bank"]["bronze"]),
      "silver n:", len(back["problem_bank"]["silver"]),
      "gold n:", len(back["problem_bank"]["gold"]))
print("silver[0] sol:", back["problem_bank"]["silver"][0]["solutions"],
      "gold[3] sol:", back["problem_bank"]["gold"][3]["solutions"])
print("has guided:", "guided" in back, "has tier_guides:", "tier_guides" in back)
print("worked_examples preserved:", len(back["worked_examples"]) == 3)
