# -*- coding: utf-8 -*-
import os, json, urllib.request

ID = "06eb8087-b07f-4bfa-8bc2-af97e3e06ebf"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": "Bearer " + KEY,
})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_ocr_L01_live.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier, [])
    print("=== %s (%d) ===" % (tier, len(probs)))
    for i,p in enumerate(probs):
        print(" [%d] %r sols=%s calc=%s it=%s" % (i, p.get("display"), p.get("solutions"), p.get("calculator"), p.get("input_type")))
print("has guided:", "guided" in pd, "has tier_guides:", "tier_guides" in pd)
print("worked_examples:", len(pd.get("worked_examples") or []))
print("related_videos:", pd.get("related_videos"))
print("topic_links:", pd.get("topic_links"))
