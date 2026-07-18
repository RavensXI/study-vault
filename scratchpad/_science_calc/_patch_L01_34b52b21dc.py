import os, json, urllib.request
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ALL_IDS = ["b88f80db-f004-4ed4-8853-32992a306402"]
SHARD = "lesson_higher-calculations-L01@34b52b21dc.json"
pd = json.load(open(SHARD, encoding="utf-8"))
body = json.dumps({"practice_data": pd}).encode("utf-8")
for rid in ALL_IDS:
    req = urllib.request.Request(BASE + "?id=eq." + rid, data=body, method="PATCH",
        headers={"apikey": KEY, "Authorization": "Bearer " + KEY,
                 "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        print("PATCH", rid, r.status)
# verify byte-identical
canon = json.dumps(pd, sort_keys=True, ensure_ascii=False)
for rid in ALL_IDS:
    url = BASE + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req) as r:
        live = json.load(r)[0]["practice_data"]
    match = json.dumps(live, sort_keys=True, ensure_ascii=False) == canon
    print("VERIFY", rid, "identical" if match else "MISMATCH")
