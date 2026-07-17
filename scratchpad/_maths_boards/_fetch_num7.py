import os, json, urllib.request

ID = "8696e75e-f9fd-40ef-b3a4-df27f5811c73"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(URL, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_live_number-L07.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier) or pd.get(tier)
    if isinstance(probs, list):
        print(f"{tier}: {len(probs)} problems")
