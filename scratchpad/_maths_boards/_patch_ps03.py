# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "74d5f6d6-9036-4da3-adf3-d7e2c86fc6b4"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-aqa_probability-statistics-L03.json", encoding="utf-8"))
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status", resp.status)

# confirm round-trip
r = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
back = json.load(urllib.request.urlopen(r))[0]["practice_data"]
print("keys back:", sorted(back.keys()))
print("bronze[3] sol:", back["problem_bank"]["bronze"][3]["solutions"])
print("has guided:", "guided" in back, "| tier_guides:", "tier_guides" in back)
print("gold[1] opt0:", back["problem_bank"]["gold"][1]["options"][0])
