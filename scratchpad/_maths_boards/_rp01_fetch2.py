import os, json, urllib.request

ID = "a6f6c5da-0aa8-437c-b3fe-75b8a48d6714"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
pd = json.load(urllib.request.urlopen(req))[0]["practice_data"]
with open("_rp01_live2.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("Top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()) if isinstance(pb, dict) else type(pb))
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier) if isinstance(pb, dict) else None
    if isinstance(probs, list):
        print(f"{tier}: {len(probs)}")
print("has guided:", "guided" in pd, "| tier_guides:", "tier_guides" in pd)
