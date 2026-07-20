import os, json, urllib.request
ID = "3a0b41fb-d6d3-43ac-9d74-08abb8926e8a"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
d = os.path.dirname(os.path.abspath(__file__))
json.dump(pd, open(os.path.join(d,"_CK12_live.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank") or {}
for t in ("bronze","silver","gold"): print(t, len(pb.get(t) or []))
