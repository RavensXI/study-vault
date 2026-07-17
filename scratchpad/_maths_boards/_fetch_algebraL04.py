# -*- coding: utf-8 -*-
import json, os, urllib.request

ID = "431cf470-df7f-4654-8c83-df7aeb1e0322"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
url = BASE + "?id=eq." + ID + "&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
out = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_live_algebra-L04.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("wrote", out)
print("top-level keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze", "silver", "gold"):
    probs = pb.get(t) or []
    print("==", t, "n=", len(probs), "desc=", repr(pb.get(t + "_description")))
    for i, p in enumerate(probs):
        print("  [%d]" % i, "sol=", p.get("solutions"), "it=", p.get("input_type"),
              "calc=", p.get("calculator"))
        print("       disp:", (p.get("display") or "")[:120])
