import os, json, urllib.request

ID = "1d30ba6e-3b9a-41a9-b192-23cab4fd0d5f"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": key, "Authorization": f"Bearer {key}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_chk_live_L08.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier)
    if isinstance(probs, list):
        print(tier, "count", len(probs))
