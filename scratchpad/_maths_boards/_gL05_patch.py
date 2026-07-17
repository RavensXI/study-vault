# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "acf8619c-92bc-4778-b29c-dd0cb973f59c"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-ocr_graphs-L05.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
resp = urllib.request.urlopen(req)
print("PATCH status:", resp.status)
# verify round-trip
g = urllib.request.Request(url + "&select=practice_data", headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
live = json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("round-trip equal:", live == pd)
