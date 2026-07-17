import json, os, urllib.request

ID = "e16ccba1-6dc0-4321-835b-98ec18acce00"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_L07ocr_live.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()))
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier, [])
    print(f"\n=== {tier} ({len(probs)}) ===")
    for i,p in enumerate(probs):
        print(f"[{i}] input={p.get('input_type')} calc={p.get('calculator')}")
        print("   display:", p.get('display'))
        print("   solutions:", p.get('solutions'))
