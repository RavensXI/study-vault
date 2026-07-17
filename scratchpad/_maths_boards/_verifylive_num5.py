# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "a65d19a4-17d8-4370-ac24-ef8ae364f72d"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer " + key})
live = json.load(urllib.request.urlopen(req))[0]["practice_data"]
shard = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-aqa_number-L05.json", encoding="utf-8"))
out = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_after_num5.json"
json.dump(live, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("live == shard:", json.dumps(live,sort_keys=True)==json.dumps(shard,sort_keys=True))
print("wrote", out)
