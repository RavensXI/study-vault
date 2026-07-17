# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "24e576f2-0e8a-43bc-bacd-5397b4da617b"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_numL06_ocr.json"
json.dump(pd, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("fetched, keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t, [])), "|", (pb.get(t+"_description") or "")[:60])
