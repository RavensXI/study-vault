import os, json, urllib.request

ID = "014f2f50-be82-4870-a8e7-d15963b39e8f"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=title,slug,practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"
})
data = json.load(urllib.request.urlopen(req))
row = data[0]
print("title:", row.get("title"))
print("slug:", row.get("slug"))
pd = row["practice_data"]
with open("_MYCHK_L05_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb and isinstance(pb[t], list):
        print(t, "count", len(pb[t]))
