# -*- coding: utf-8 -*-
import os, json, io, urllib.request

ID = "15c509ec-bdaf-466b-b9e4-1f1803fc4b3d"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-eduqas_algebra-L14.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

greq = urllib.request.Request(url + "&select=practice_data",
                              headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(greq) as r:
    live = json.load(r)[0]["practice_data"]
print("has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("bronze/silver/gold n:", len(live["problem_bank"]["bronze"]),
      len(live["problem_bank"]["silver"]), len(live["problem_bank"]["gold"]))
print("B5 sol:", live["problem_bank"]["bronze"][5]["solutions"])
print("B7 sol:", live["problem_bank"]["bronze"][7]["solutions"])
print("B6 has svg:", "<svg" in live["problem_bank"]["bronze"][6]["display"])
print("opener has svg:", "<svg" in live["guided"]["opener"]["display"])
print("worked_examples preserved:", live["worked_examples"] == pd["worked_examples"])
json.dump(live, io.open("_L14_livecheck.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
