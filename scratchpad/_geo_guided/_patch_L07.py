# -*- coding: utf-8 -*-
import json, io, os, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
K = os.environ["SUPABASE_SERVICE_KEY"]
ID = "a2b1558e-5fe8-4dbe-b645-f6508e527216"
URL = ("https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq." + ID
       + "&select=practice_data")
pd = json.load(io.open(os.path.join(HERE, "lesson_L07.json"), encoding="utf-8"))

body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": K, "Authorization": "Bearer " + K,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

req = urllib.request.Request(URL, headers={"apikey": K,
                                           "Authorization": "Bearer " + K})
live = json.load(urllib.request.urlopen(req))[0]["practice_data"]
print("round-trip identical:", live == pd)
print("has guided:", "guided" in live,
      "| tier_guides:", "tier_guides" in live,
      "| bronze_desc:", bool(live["problem_bank"].get("bronze_description")))
