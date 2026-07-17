# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "660796ad-070d-4a2d-af11-900e5a5af1c1"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_eduqas_graphs-L07.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", out)
# quick summary
pb = pd.get("problem_bank", {})
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier, [])
    print("\n=== %s (%d) ===" % (tier, len(probs)))
    for i,p in enumerate(probs):
        print(" [%d] it=%s sols=%s calc=%s" % (i, p.get("input_type"), p.get("solutions"), p.get("calculator")))
        print("      display:", (p.get("display") or "")[:160])
        if p.get("options"): print("      options:", p.get("options"))
print("\nTop keys:", sorted(pd.keys()))
print("has guided:", "guided" in pd, "| tier_guides:", "tier_guides" in pd, "| method_card:", "method_card" in pd)
