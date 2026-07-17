import os, json, urllib.request

ID = "15c509ec-bdaf-466b-b9e4-1f1803fc4b3d"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
json.dump(pd, open("_L14_live.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ("bronze","silver","gold"):
    t = pb.get(tier)
    if isinstance(t, list):
        print(tier, "problems:", len(t))
