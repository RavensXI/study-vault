# -*- coding: utf-8 -*-
import os, json, urllib.request

BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
LID = "7ccfb7aa-adfd-4f9d-9679-35d805ddd77a"
KEY = os.environ["SUPABASE_SERVICE_KEY"]

pd = json.load(open("lesson_maths-eduqas_algebra-L03.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")

req = urllib.request.Request(
    BASE + "?id=eq." + LID, data=body, method="PATCH",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
             "Content-Type": "application/json", "Prefer": "return=minimal"})
with urllib.request.urlopen(req) as r:
    print("PATCH status", r.status)

vreq = urllib.request.Request(
    BASE + "?id=eq." + LID + "&select=practice_data",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(vreq) as r:
    live = json.load(r)[0]["practice_data"]
print("live top keys:", sorted(live.keys()))
print("has guided:", "guided" in live, "tier_guides:", "tier_guides" in live)
print("bronze[0] has guided_steps:", bool(live["problem_bank"]["bronze"][0].get("guided_steps")))
print("worked_examples preserved:", len(live.get("worked_examples", [])))
print("descs:", bool(live["problem_bank"].get("bronze_description")), bool(live["problem_bank"].get("gold_description")))
