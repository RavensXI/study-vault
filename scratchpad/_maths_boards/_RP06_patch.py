# -*- coding: utf-8 -*-
import json, os, urllib.request
ID = "ca643606-adf3-40c8-a4dd-8dfb8c25a21f"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(open("lesson_maths-eduqas_ratio-proportion-L06.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# read back and confirm the new structure landed
gurl = f"{url}&select=practice_data"
greq = urllib.request.Request(gurl, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(greq) as r:
    got = json.load(r)[0]["practice_data"]
print("has guided:", "guided" in got, "| has tier_guides:", "tier_guides" in got)
print("bronze/silver/gold:", len(got["problem_bank"]["bronze"]), len(got["problem_bank"]["silver"]), len(got["problem_bank"]["gold"]))
print("gold[1] solution:", got["problem_bank"]["gold"][1]["solutions"])
print("matches shard:", got == pd)
