# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID="44ac4c68-828c-4d38-888a-37758fefde57"
KEY=os.environ["SUPABASE_SERVICE_KEY"]
pd=json.load(io.open(r"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_algebra-L13.json", encoding="utf-8"))
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body=json.dumps({"practice_data":pd}).encode("utf-8")
req=urllib.request.Request(url, data=body, method="PATCH", headers={
 "apikey":KEY,"Authorization":f"Bearer {KEY}",
 "Content-Type":"application/json","Prefer":"return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)
# verify round-trip
req2=urllib.request.Request(url+"&select=practice_data", headers={"apikey":KEY,"Authorization":f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    live=json.load(r)[0]["practice_data"]
print("has guided:", "guided" in live, "| has tier_guides:", "tier_guides" in live)
print("bronze count:", len(live["problem_bank"]["bronze"]), "silver:", len(live["problem_bank"]["silver"]), "gold:", len(live["problem_bank"]["gold"]))
print("bronze[0] display:", live["problem_bank"]["bronze"][0]["display"][:40])
print("opener has svg:", "<svg" in live["guided"]["opener"]["display"])
