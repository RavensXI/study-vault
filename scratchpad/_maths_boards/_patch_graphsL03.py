# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "c8bc060f-c094-4b04-abec-5577523f8667"
key = os.environ["SUPABASE_SERVICE_KEY"]
pd = json.load(io.open("lesson_maths-aqa_graphs-L03.json", encoding="utf-8"))
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}"
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": key, "Authorization": f"Bearer {key}",
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)
# verify roundtrip
g = urllib.request.Request(url + "&select=practice_data", headers={"apikey": key, "Authorization": f"Bearer {key}"})
live = json.load(urllib.request.urlopen(g))[0]["practice_data"]
print("live keys:", sorted(live.keys()))
print("bronze n:", len(live["problem_bank"]["bronze"]), "silver n:", len(live["problem_bank"]["silver"]), "gold n:", len(live["problem_bank"]["gold"]))
print("has guided:", "guided" in live, "has tier_guides:", "tier_guides" in live)
print("charts:", sum(1 for t in ("bronze","silver","gold") for p in live["problem_bank"][t] if p.get("chart")))
print("opener svg present:", "<svg" in live["guided"]["opener"]["display"])
