# -*- coding: utf-8 -*-
import os, io, json, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "993821d6-eb39-4c71-9dcf-c733f6ce81a4"
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq." + ID

pd = json.load(io.open(os.path.join(HERE, "lesson_L10.json"), encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": "Bearer " + key,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

req = urllib.request.Request(URL + "&select=practice_data",
                             headers={"apikey": key, "Authorization": "Bearer " + key})
back = json.load(urllib.request.urlopen(req))[0]["practice_data"]
print("round-trip identical:", json.dumps(back, sort_keys=True) == json.dumps(pd, sort_keys=True))
print("has guided:", "guided" in back, "| tier_guides:", "tier_guides" in back,
      "| bronze_description:", bool(back["problem_bank"].get("bronze_description")))
