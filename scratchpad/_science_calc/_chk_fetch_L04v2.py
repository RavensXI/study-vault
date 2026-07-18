# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
cid = "123bb55f-1fc8-41fd-9b44-759bc466b766"

def fetch(rid):
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]

pd = fetch(cid)
with open("_chk_live_L04v2.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("fetched canonical, top keys:", sorted(pd.keys()))
