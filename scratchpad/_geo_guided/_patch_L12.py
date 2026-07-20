# -*- coding: utf-8 -*-
import io, json, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ID = "3a0b41fb-d6d3-43ac-9d74-08abb8926e8a"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq." + ID

pd = json.load(io.open(os.path.join(HERE, "lesson_L12.json"), encoding="utf-8"))
body = json.dumps({"practice_data": pd}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(URL, data=body, method="PATCH", headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY,
    "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)

req = urllib.request.Request(URL + "&select=practice_data",
                             headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
live = json.load(urllib.request.urlopen(req))[0]["practice_data"]
same = json.dumps(live, sort_keys=True, ensure_ascii=False) == json.dumps(pd, sort_keys=True, ensure_ascii=False)
print("round-trip identical:", same)
pb = live["problem_bank"]
print("tier descs:", all(pb.get(t + "_description") for t in ("bronze", "silver", "gold")))
print("guided keys:", sorted((live.get("guided") or {}).keys()))
print("walks:", sum(1 for t in ("bronze", "silver", "gold") for p in pb[t] if p.get("guided_steps")))
