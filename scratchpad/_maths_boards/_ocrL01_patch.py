# -*- coding: utf-8 -*-
import os, json, io, urllib.request

LID = "d8a78aa2-a642-4dcd-9cb0-1aa5990761e7"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-ocr_algebra-L01.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# round-trip verify
g = urllib.request.Request(url + "&select=practice_data",
    headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(g) as r:
    got = json.load(r)[0]["practice_data"]
print("guided present:", "guided" in got, "| tier_guides:", "tier_guides" in got)
print("bronze[0] hint:", got["problem_bank"]["bronze"][0].get("hint"))
print("round-trip equal:", got == pd)
