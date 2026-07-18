# -*- coding: utf-8 -*-
import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
CANON = "fc32b93d-51c8-4260-a199-7268fa33979d"

def get(rid):
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

data = get(CANON)
pd = data[0]["practice_data"]
with open("_canon_L04_fetched.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("fetched, top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t, [])))
