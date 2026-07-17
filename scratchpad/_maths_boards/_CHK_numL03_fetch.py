import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
LID = "c8596747-22a3-47f0-8fe7-f0bc6c6d1101"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data,title,slug,unit_id"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
with open("_CHK_numL03_live.json", "w", encoding="utf-8") as f:
    json.dump(row["practice_data"], f, indent=2, ensure_ascii=False)
print("title:", row.get("title"), "slug:", row.get("slug"))
pd = row["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    probs = pb.get(t) if isinstance(pb.get(t), list) else pb.get(t)
    if isinstance(probs, list):
        print(t, "count:", len(probs))
