# -*- coding: utf-8 -*-
import os, json, urllib.request, sys
sys.stdout.reconfigure(encoding="utf-8")
ID = "d6cc3827-bbe2-42ae-b116-7c8398b1bf70"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": f"Bearer {key}"})
livepd = json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(livepd, open("_ps03e_livepost.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
shard = json.load(open("_ps03e_shard.json", encoding="utf-8"))
a = json.dumps(livepd, ensure_ascii=False, sort_keys=True)
b = json.dumps(shard, ensure_ascii=False, sort_keys=True)
print("LIVE == shard:", a == b)
print("has guided:", "guided" in livepd, "| tier_guides:", "tier_guides" in livepd)
