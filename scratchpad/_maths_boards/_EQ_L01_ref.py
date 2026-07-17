import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
AQA = "f4f1368e-d7c2-41f1-8459-de2c0d500c3b"
req = urllib.request.Request(f"{BASE}?id=eq.{AQA}&select=practice_data",
    headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req) as r:
    pd = json.load(r)[0]["practice_data"]
with open("_EQ_L01_aqaref.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("AQA ref keys:", list(pd.keys()))
print("has guided:", "guided" in pd, "tier_guides:", "tier_guides" in pd)
