# -*- coding: utf-8 -*-
import os, json, io, urllib.request
SUPA = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
LID = "93469b0d-2704-499c-a20b-587a84c2e214"
pd = json.load(io.open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\lesson_maths-eduqas_ratio-proportion-L05.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
url = f"{SUPA}/rest/v1/lessons?id=eq.{LID}"
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status:", r.status)

# verify round-trip
req2 = urllib.request.Request(f"{SUPA}/rest/v1/lessons?id=eq.{LID}&select=practice_data",
    headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req2) as r:
    live = json.load(r)[0]["practice_data"]
print("keys:", list(live.keys()))
print("has guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("bronze sols:", [p["solutions"] for p in live["problem_bank"]["bronze"]])
print("bronze types:", [p["input_type"] for p in live["problem_bank"]["bronze"]])
print("gold types:", [p["input_type"] for p in live["problem_bank"]["gold"]])
print("worked_examples preserved:", len(live["worked_examples"]), "| related_videos:", live["related_videos"])
print("topic_links:", live["topic_links"])
