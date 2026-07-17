import os, json, urllib.request

ID = "5ead70d6-f265-4790-86b5-573b9b16606a"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
json.dump(pd, open("_L07e_live.json","w"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()))
for tier in ["bronze","silver","gold"]:
    probs = pb.get(tier) or pd.get(tier)
    if isinstance(probs, list):
        print(tier, "count", len(probs))
