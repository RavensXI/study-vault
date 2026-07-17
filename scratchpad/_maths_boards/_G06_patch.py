# -*- coding: utf-8 -*-
import json, io, os, urllib.request, shutil

ID = "683b816a-4d56-4d3d-911b-58cb3bca5efd"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s" % ID

pd = json.load(io.open("_G06_final.json", encoding="utf-8"))

# ship-gate shard copy
shutil.copyfile("_G06_final.json", "lesson_maths-eduqas_graphs-L06.json")

body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(BASE + "&select=practice_data", data=body, method="PATCH",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
             "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
req2 = urllib.request.Request(BASE + "&select=practice_data",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req2) as r:
    got = json.load(r)[0]["practice_data"]
print("has guided:", "guided" in got, "| tier_guides:", "tier_guides" in got)
print("round-trip identical:", json.dumps(got, sort_keys=True, ensure_ascii=False) ==
                                json.dumps(pd, sort_keys=True, ensure_ascii=False))
# count charts live
n = sum(1 for t in ("bronze","silver","gold") for p in got["problem_bank"][t] if p.get("chart"))
print("charts live:", n)
