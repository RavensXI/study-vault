import os, json, urllib.request

ID = "ee2766ef-5043-457b-b6b3-4e38d5ed9d0e"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_L09ocr_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ["bronze","silver","gold"]:
    probs = pb.get(tier, [])
    print(f"\n=== {tier} ({len(probs)}) ===")
    for i,p in enumerate(probs):
        print(f"[{i}] {p.get('input_type')} calc={p.get('calculator')} sol={p.get('solutions')}  {p.get('display')}")
print("\ndescriptions:", {k:v for k,v in pb.items() if k.endswith('_description')})
print("\nhas guided:", "guided" in pd, "tier_guides:", "tier_guides" in pd)
