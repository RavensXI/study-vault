# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "bba25423-da94-4b3e-8415-2e9161014760"
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
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_eduqas_L02.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze", "silver", "gold"):
    probs = pb.get(t) or []
    print("\n===", t, "(", len(probs), ")===")
    for i, p in enumerate(probs):
        print(i, "|", p.get("input_type"), "| calc=", p.get("calculator"), "| sol=", p.get("solutions"), "|", (p.get("display") or "")[:80])
