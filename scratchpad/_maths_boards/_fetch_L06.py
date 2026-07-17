import os, json, urllib.request

ID = "4e8ba0ab-6dca-4615-98e2-2fac39408f5c"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_live_L06.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb, dict) else type(pb))
for t in ["bronze","silver","gold"]:
    probs = pb.get(t) if isinstance(pb,dict) else None
    if isinstance(probs, list):
        print(f"  {t}: {len(probs)} problems")
print("has guided:", "guided" in pd, "has tier_guides:", "tier_guides" in pd)
