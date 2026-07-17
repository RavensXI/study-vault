import os, json, urllib.request

LID = "038c2343-8acf-41e4-b02a-914268bc6572"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
with open("_L09eq_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("TOP KEYS:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ("bronze","silver","gold"):
    arr = pb.get(t, [])
    print(f"\n=== {t} ({len(arr)}) ===")
    for i, p in enumerate(arr):
        print(f"  [{i}] disp={p.get('display')!r} sol={p.get('solutions')} it={p.get('input_type')} calc={p.get('calculator')}")
print("\nhas guided:", "guided" in pd)
print("has tier_guides:", "tier_guides" in pd)
print("has method_card:", "method_card" in pd)
