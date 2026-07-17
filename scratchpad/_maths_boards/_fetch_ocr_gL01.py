# -*- coding: utf-8 -*-
import os, json, urllib.request

LID = "89689a46-7251-4c2a-900e-5fdc240dafd3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
url = BASE + "?id=eq." + LID + "&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
out = os.path.join(os.path.dirname(__file__), "_live_ocr_gL01.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze", "silver", "gold"):
    probs = pb.get(t, [])
    print("\n===", t, len(probs), "===")
    for i, p in enumerate(probs):
        print(i, "|", repr(p.get("display")), "| sols", p.get("solutions"),
              "| it", p.get("input_type"), "| calc", p.get("calculator"),
              "| chart" if p.get("chart") else "")
