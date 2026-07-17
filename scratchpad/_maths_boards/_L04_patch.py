# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "da15f5f9-2162-4b08-b990-ac2efa64f13a"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open(r"lesson_maths-ocr_algebra-L04.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status", resp.status)

# read-back verify
req2 = urllib.request.Request(url+"&select=practice_data", headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
back = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
print("readback keys:", list(back.keys()))
print("has tier_guides:", "tier_guides" in back, "has guided:", "guided" in back)
print("gold[2] last box:", [s for s in back["problem_bank"]["gold"][2]["guided_steps"] if s.get("answer") is not None][-1]["answer"])
