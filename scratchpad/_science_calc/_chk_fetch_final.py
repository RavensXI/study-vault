import os, json, io, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
base = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
def fetch(rid):
    url = base + "?id=eq." + rid + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer "+key})
    with urllib.request.urlopen(req) as r:
        return json.load(r)[0]["practice_data"]
cid = "cbf5f791-862e-496e-8ecf-65c4cf27002c"
pd = fetch(cid)
io.open("_LIVE_canon_final.json","w",encoding="utf-8").write(json.dumps(pd, indent=1, ensure_ascii=False))
print("keys:", list(pd.keys()))
print("pb tiers:", {t: len(pd.get("problem_bank",{}).get(t,[])) for t in ("bronze","silver","gold")})
