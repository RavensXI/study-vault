import os, json, urllib.request
ID = "6a2afcf8-1c03-4b07-b228-3999deb3d402"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
pd = row["practice_data"]
json.dump(pd, open("_chk_live_L04.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("title:", row.get("title"), "| slug:", row.get("slug"))
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ["bronze","silver","gold"]:
    probs = pb.get(tier)
    if isinstance(probs, list):
        print(f"{tier}: {len(probs)} problems")
