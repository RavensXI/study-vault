import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "98e99005-69e2-4131-bd6b-6018ebac6e9d"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
row = data[0]
with open("_b5d_live.json", "w", encoding="utf-8") as f:
    json.dump(row["practice_data"], f, indent=1, ensure_ascii=False)
print("title:", row.get("title"))
print("slug:", row.get("slug"))
print("unit_slug:", row.get("unit_slug"))
pd = row["practice_data"]
print("top keys:", list(pd.keys()))
print("has guided:", "guided" in pd)
print("has tier_guides:", "tier_guides" in pd)
pb = pd.get("problem_bank", {})
for t in ("bronze","silver","gold"):
    print(t, len(pb.get(t, [])))
