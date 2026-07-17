# -*- coding: utf-8 -*-
import os, json, urllib.request

LID = "7f417926-0bef-4875-a7ad-7eb71bd15506"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data,title,slug,unit_id" % LID
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": "Bearer " + KEY})
data = json.load(urllib.request.urlopen(req))
row = data[0]
with open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_ps02_live.json", "w", encoding="utf-8") as f:
    json.dump(row["practice_data"], f, ensure_ascii=False, indent=1)
print("title:", row.get("title"))
print("slug:", row.get("slug"))
pd = row["practice_data"]
print("top keys:", sorted(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze","silver","gold"):
    probs = pb.get(t) or []
    print("\n=== %s (%d) desc=%r" % (t, len(probs), pb.get(t+"_description")))
    for i,p in enumerate(probs):
        print(" [%d] it=%s calc=%s sol=%s" % (i, p.get("input_type"), p.get("calculator"), p.get("solutions")))
        print("     disp:", (p.get("display") or "")[:200])
