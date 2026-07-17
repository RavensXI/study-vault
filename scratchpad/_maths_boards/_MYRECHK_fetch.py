import os, json, urllib.request
ID = "fc1f101a-9d1b-4eab-8bf8-8159f78caea2"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug,unit_id"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
row = json.load(urllib.request.urlopen(req))[0]
with open("_MYRECHK_live.json", "w", encoding="utf-8") as f:
    json.dump(row["practice_data"], f, indent=2, ensure_ascii=False)
print("title:", row.get("title"), "slug:", row.get("slug"))
pd = row["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
if isinstance(pb, dict):
    print("pb keys:", list(pb.keys()))
    for t in ["bronze","silver","gold"]:
        v = pb.get(t)
        if isinstance(v, list):
            print(t, "count:", len(v))
