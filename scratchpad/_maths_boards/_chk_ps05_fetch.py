import json, os, urllib.request

SUPA = "https://baipckgywpnwapobwtsy.supabase.co"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "2e75898f-577a-42bd-b94e-f1435e89ace3"

url = f"{SUPA}/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_chk_ps05_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("keys:", list(pd.keys()))
print("wrote _chk_ps05_live.json")
