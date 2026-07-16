# -*- coding: utf-8 -*-
import os, json, io, urllib.request

LID = "08c3ded7-4862-4609-b4bb-dee8b46b8329"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % LID
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
pd = json.load(urllib.request.urlopen(req))[0]["practice_data"]
json.dump(pd, io.open("_L03_live_after.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
g = pd["guided"]
print("opener display has <svg:", "<svg" in g["opener"]["display"])
for t in ("bronze", "silver", "gold"):
    d = g["teach"][t]["display"]
    print("teach", t, "has <svg:", "<svg" in d, "| degrees:", d.count("°"))
