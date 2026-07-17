# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "c8596747-22a3-47f0-8fe7-f0bc6c6d1101"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer " + key})
live = json.load(urllib.request.urlopen(req))[0]["practice_data"]
built = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-aqa_number-L03.json", encoding="utf-8"))
print("live == built:", json.dumps(live, sort_keys=True) == json.dumps(built, sort_keys=True))
orig = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_number-L03.json", encoding="utf-8"))
for f in ("related_videos", "topic_links", "worked_examples"):
    print("preserved %s:" % f, json.dumps(live.get(f), sort_keys=True) == json.dumps(orig.get(f), sort_keys=True))
# solutions unchanged
for t in ("bronze", "silver", "gold"):
    a = [p["solutions"] for p in orig["problem_bank"][t]]
    b = [p["solutions"] for p in live["problem_bank"][t]]
    print("solutions %s unchanged:" % t, a == b)
open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_after_num3.json", "w", encoding="utf-8").write(json.dumps(live, ensure_ascii=False, indent=2))
