import os, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "a2b1558e-5fe8-4dbe-b645-f6508e527216"
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer "+key})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_chk_L07_live.json")
json.dump(pd, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t) or []))
