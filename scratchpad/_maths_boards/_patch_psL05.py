# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "b063ea7d-cb1c-40ca-a28b-ea79c429361f"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-ocr_probability-statistics-L05.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# verify round-trip
vurl = url + "&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
back = json.load(urllib.request.urlopen(vreq))[0]["practice_data"]
print("live keys:", sorted(back.keys()))
print("guided?", "guided" in back, "tier_guides?", "tier_guides" in back)
print("bronze n:", len(back["problem_bank"]["bronze"]), "G3 sol:", back["problem_bank"]["gold"][3]["solutions"])
print("worked_examples preserved:", back["worked_examples"] == pd["worked_examples"])
