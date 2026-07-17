# -*- coding: utf-8 -*-
import os, json, io, urllib.request

LID = "80de6f33-3b1d-40af-9068-8e6fc132c36d"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-aqa_algebra-L07.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)

# verify round-trip
url2 = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data"
req2 = urllib.request.Request(url2, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
pb = live["problem_bank"]
print("live tiers:", {t: len(pb[t]) for t in ("bronze","silver","gold")})
print("has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("gold[0] display:", pb["gold"][0]["display"])
print("gold[0] sol:", pb["gold"][0]["solutions"])
print("worked_examples preserved:", live.get("worked_examples") == pd["worked_examples"])
