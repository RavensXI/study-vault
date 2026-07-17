import json, os, urllib.request

ID = "fe05d231-ed67-4625-aa4d-791c6b1d9887"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
pd = row["practice_data"]
json.dump(pd, open("_CHKR_L06_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("title:", row.get("title"), "slug:", row.get("slug"))
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb:
        print(t, "count", len(pb[t]))
