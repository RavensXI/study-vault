# -*- coding: utf-8 -*-
import json, io, os, urllib.request

KEY_ID = "d168ac22-370f-4c9f-a647-85febc0e8213"
SK = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_geometry-L03.json", encoding="utf-8"))

url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{KEY_ID}"
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": SK, "Authorization": "Bearer " + SK,
    "Content-Type": "application/json", "Prefer": "return=minimal",
})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
vurl = url + "&select=practice_data"
vreq = urllib.request.Request(vurl, headers={"apikey": SK, "Authorization": "Bearer " + SK})
with urllib.request.urlopen(vreq) as r:
    live = json.load(r)[0]["practice_data"]
pb = live["problem_bank"]
print("bronze:", [p["solutions"] for p in pb["bronze"]])
print("silver:", [p["solutions"] for p in pb["silver"]])
print("gold:", [p["solutions"] for p in pb["gold"]])
print("has guided:", "guided" in live, "| has tier_guides:", "tier_guides" in live)
print("related_videos count:", len(live.get("related_videos", [])))
print("worked_examples count:", len(live.get("worked_examples", [])))
print("B7 display:", pb["bronze"][7]["display"])
print("match:", json.dumps(live, ensure_ascii=False, sort_keys=True) == json.dumps(pd, ensure_ascii=False, sort_keys=True))
