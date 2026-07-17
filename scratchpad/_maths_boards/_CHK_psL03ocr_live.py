# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "65e7a745-9820-431a-8b99-d96cd7514bf3"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
pd = json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd, open("_CHK_psL03ocr_livepost.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
local = json.load(open("lesson_maths-ocr_probability-statistics-L03.json", encoding="utf-8"))
print("round-trip identical:", json.dumps(pd, sort_keys=True, ensure_ascii=False) == json.dumps(local, sort_keys=True, ensure_ascii=False))
print("has guided:", "guided" in pd, "| tier_guides:", "tier_guides" in pd)
print("related_videos preserved (empty):", pd["related_videos"] == [])
print("worked_examples count:", len(pd["worked_examples"]))
