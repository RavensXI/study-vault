import os, json, urllib.request
key = os.environ["SUPABASE_SERVICE_KEY"]
ID = "993821d6-eb39-4c71-9dcf-c733f6ce81a4"
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer "+key})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_L10_live.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t) or []))
