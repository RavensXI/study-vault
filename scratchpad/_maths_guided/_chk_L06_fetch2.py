import os, json, urllib.request

ID = "4aa9afe1-7e47-4f0f-b7e6-da22be472716"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_CHK_L06_LIVE_fresh.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("keys:", list(pd.keys()))
print("bank tiers:", list(pd.get("problem_bank", {}).keys()) if isinstance(pd.get("problem_bank"), dict) else "n/a")
