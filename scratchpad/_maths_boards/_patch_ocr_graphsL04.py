# -*- coding: utf-8 -*-
import json, io, os, urllib.request

LID = "fb13c12c-f5c1-4832-871b-40440d729361"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq." + LID

pd = json.load(io.open("lesson_maths-ocr_graphs-L04.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

# verify round-trip
req2 = urllib.request.Request(URL + "&select=practice_data", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    live = json.loads(r.read().decode("utf-8"))[0]["practice_data"]
print("live has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("bronze[5] sol:", live["problem_bank"]["bronze"][5]["solutions"],
      "| silver[2] sol:", live["problem_bank"]["silver"][2]["solutions"],
      "| gold[4] sol:", live["problem_bank"]["gold"][4]["solutions"])
print("gold[0] has chart:", "chart" in live["problem_bank"]["gold"][0],
      "| gold[3] display has svg:", "<svg" in live["problem_bank"]["gold"][3]["display"])
print("match written == live:", json.dumps(live, ensure_ascii=False, sort_keys=True)==json.dumps(pd, ensure_ascii=False, sort_keys=True))
