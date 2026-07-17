import os, json, urllib.request

ID = "a1bdc834-74b8-41cf-8671-c1e3e5270619"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_RECHK_L02_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("keys:", list(pd.keys()))
print("bank tiers:", list(pd.get("problem_bank", {}).keys()) if "problem_bank" in pd else "NO BANK")
