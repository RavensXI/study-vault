# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "a48ad66b-78c0-46f9-9db0-828173e35d1f"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer " + key})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_eduqas_ratioL04.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze","silver","gold"):
    print("---", t, "desc:", (pb.get(t+"_description") or "")[:80])
    for i,p in enumerate(pb.get(t) or []):
        print(t, i, "| it:", p.get("input_type"), "| sols:", p.get("solutions"), "| calc:", p.get("calculator"))
        print("    disp:", (p.get("display") or "")[:160])
