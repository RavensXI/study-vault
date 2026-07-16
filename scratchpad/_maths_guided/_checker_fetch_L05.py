import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "2158f4af-be63-4d5e-a425-c961358999db"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_checker_live_L05.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("top-level keys:", list(pd.keys()))
