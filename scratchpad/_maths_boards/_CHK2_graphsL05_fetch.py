import os, json, urllib.request

ID = "295660a5-6ee6-40a4-9c32-c6aa0de7a590"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,slug,title"
req = urllib.request.Request(url, headers={
    "apikey": key,
    "Authorization": f"Bearer {key}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
row = data[0]
with open("_CHK2_graphsL05_LIVE.json", "w", encoding="utf-8") as f:
    json.dump(row, f, indent=2, ensure_ascii=False)
print("slug:", row.get("slug"))
print("title:", row.get("title"))
pd = row["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    probs = pb.get(t)
    if isinstance(probs, list):
        print(f"{t}: {len(probs)} problems")
