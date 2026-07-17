import os, json, urllib.request

ID = "d15fddc3-0766-4882-bfc8-15a0b7208d89"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
with open("_CHK_numL06_live.json", "w", encoding="utf-8") as f:
    json.dump(row, f, indent=2, ensure_ascii=False)
pd = row["practice_data"]
print("title:", row.get("title"), "slug:", row.get("slug"))
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb and isinstance(pb[t], list):
        print(t, "count:", len(pb[t]))
