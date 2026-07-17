# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "a65d19a4-17d8-4370-ac24-ef8ae364f72d"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data,title,slug" % ID
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer " + key})
data = json.load(urllib.request.urlopen(req))
row = data[0]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_number-L05.json"
open(out, "w", encoding="utf-8").write(json.dumps(row["practice_data"], ensure_ascii=False, indent=2))
pd = row["practice_data"]
print("title:", row.get("title"), "slug:", row.get("slug"))
print("top keys:", sorted(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    probs = pb.get(t) or []
    print("\n=== %s (%d) desc=%r ===" % (t, len(probs), pb.get(t+"_description")))
    for i,p in enumerate(probs):
        print(" [%d] it=%s sols=%s cal=%s" % (i, p.get("input_type"), p.get("solutions"), p.get("calculator")))
        print("     disp:", (p.get("display") or "")[:200])
