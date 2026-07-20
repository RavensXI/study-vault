# -*- coding: utf-8 -*-
import os, io, json, urllib.request

ID = "42fe9f9d-e989-46b1-afef-c70754f8e4d3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "lesson_L01.json"), encoding="utf-8"))

url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq." + ID
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(url, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

# verify
req = urllib.request.Request(url + "&select=practice_data",
                             headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
live = json.load(urllib.request.urlopen(req))[0]["practice_data"]
print("identical:", live == pd)
lpb = live["problem_bank"]
print("guided:", "guided" in live, "| tier_guides:", "tier_guides" in live)
print("descriptions:", all((lpb.get(t + "_description") or "").strip() for t in ("bronze", "silver", "gold")))
print("charts:", sum(1 for t in ("bronze","silver","gold") for p in lpb[t] if p.get("chart")))
print("walks:", sum(1 for t in ("bronze","silver","gold") for p in lpb[t] if p.get("guided_steps")))
print("check-wrong left:", sum(1 for t in ("bronze","silver","gold") for p in lpb[t]
                               for m in (p.get("misconceptions") or []) if m.get("check") == "wrong"))
print("worked_examples/related_videos/topic_links preserved:",
      live["worked_examples"] and live["related_videos"] == [] and "topic_links" in live)
