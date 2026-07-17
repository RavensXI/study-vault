# -*- coding: utf-8 -*-
import json, io, os, urllib.request
LID = "4a7608b6-4426-4d97-97b4-551e408f6951"
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
DIR = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards"
pd = json.load(io.open(DIR + r"\lesson_maths-aqa_algebra-L12.json", encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
req = urllib.request.Request(BASE + "?id=eq." + LID, data=body, method="PATCH",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
             "Content-Type": "application/json", "Prefer": "return=minimal"})
r = urllib.request.urlopen(req)
print("PATCH status", r.status)
# readback verify
req2 = urllib.request.Request(BASE + "?id=eq." + LID + "&select=practice_data",
    headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
live = json.load(urllib.request.urlopen(req2))[0]["practice_data"]
match = json.dumps(live, sort_keys=True) == json.dumps(pd, sort_keys=True)
print("READBACK MATCH:", match)
print("has guided/tier_guides:", "guided" in live, "tier_guides" in live)
print("teach svgs:", all("<svg" in live["guided"]["teach"][t]["display"] for t in ("bronze","silver","gold")))
