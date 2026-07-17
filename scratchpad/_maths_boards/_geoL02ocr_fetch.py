import os, json, urllib.request

ID = "7134e062-5209-4de5-894e-c315dc3ee9d0"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_geoL02ocr_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier, [])
    print(f"\n=== {tier} ({len(probs)}) ===")
    for i,p in enumerate(probs):
        print(f"[{i}] itype={p.get('input_type')} calc={p.get('calculator')} sol={p.get('solutions')}")
        print("   display:", p.get('display','')[:200])
