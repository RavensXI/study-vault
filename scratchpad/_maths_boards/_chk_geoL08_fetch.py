import os, json, urllib.request

LID = "7f378aaa-68dc-4420-b952-f56d8349b1ed"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
with open("_chk_geoL08_live.json", "w", encoding="utf-8") as f:
    json.dump(row, f, ensure_ascii=False, indent=2)
pd = row["practice_data"]
print("title:", row.get("title"), "slug:", row.get("slug"))
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb:
        probs = pb[t]
        if isinstance(probs, dict):
            print(t, "dict keys:", list(probs.keys()))
        else:
            print(t, "count:", len(probs))
