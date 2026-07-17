import os, json, urllib.request

ID = "4feee23f-c960-4264-a828-cde0f9080d45"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
url = f"{BASE}?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_L04eq_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier, [])
    print(f"\n=== {tier}: {len(probs)} problems ===")
    for i,p in enumerate(probs):
        print(f"[{i}] disp={p.get('display')!r}")
        print(f"     sol={p.get('solutions')} input={p.get('input_type')} calc={p.get('calculator')}")
