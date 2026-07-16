import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "c6b90b84-f603-4dea-8d46-f7205879bc89"
URL = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(URL, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Accept": "application/json",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_live_graphs-L03.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze","silver","gold"):
    arr = pb.get(tier, [])
    print(tier, len(arr))
