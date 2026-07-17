# -*- coding: utf-8 -*-
import os, json, io, urllib.request
ID = "24e576f2-0e8a-43bc-bacd-5397b4da617b"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
pd = json.load(urllib.request.urlopen(req))[0]["practice_data"]
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_livepost_numL06.json"
json.dump(pd, io.open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
sil = pd["problem_bank"]["silver"]
print("silver[6] display:", sil[6]["display"], "sol", sil[6]["solutions"])
print("has guided:", "guided" in pd, "| tier_guides:", "tier_guides" in pd)
print("opener has svg:", "<svg" in pd["guided"]["opener"]["display"])
print("worked_examples preserved:", len(pd["worked_examples"]))
