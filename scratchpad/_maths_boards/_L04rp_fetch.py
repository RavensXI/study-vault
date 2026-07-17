import os, json, urllib.request

ID = "f4a69507-b194-4751-ae27-c657ddd23113"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"
})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_L04rp_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("bank keys:", list(pb.keys()) if isinstance(pb, dict) else type(pb))
for t in ["bronze","silver","gold"]:
    probs = pb.get(t) if isinstance(pb, dict) else None
    if isinstance(probs, list):
        print(f"{t}: {len(probs)} problems")
print("has guided:", "guided" in pd, "| tier_guides:", "tier_guides" in pd)
