import os, json, urllib.request

ID = "5f629e65-9b8c-4fcb-a334-93ee7e25d4ff"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
data = json.load(urllib.request.urlopen(req))
row = data[0]
with open("_chk_numL03_live.json", "w", encoding="utf-8") as f:
    json.dump(row["practice_data"], f, indent=1, ensure_ascii=False)
print("title:", row["title"], "| slug:", row.get("slug"))
pd = row["practice_data"]
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ("bronze","silver","gold"):
    probs = pb.get(t)
    if isinstance(probs, list):
        print(f"{t}: {len(probs)} problems")
