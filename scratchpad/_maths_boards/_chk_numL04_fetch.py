import json, os, urllib.request

ID = "83d542e3-c94b-4365-b8a9-070845b779ec"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
row = data[0]
pd = row["practice_data"]
json.dump(pd, open("_chk_numL04_live.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("title:", row.get("title"), "slug:", row.get("slug"))
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ["bronze","silver","gold"]:
    probs = pb.get(tier, [])
    if isinstance(probs, list):
        print(tier, "n=", len(probs))
