import os, json, urllib.request

ID = "68997180-8486-4551-ab42-0a1b98384336"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_live_number_L01.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("TOP KEYS:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ["bronze","silver","gold"]:
    arr = pb.get(tier, [])
    print(f"\n=== {tier} ({len(arr)}) ===")
    for i,p in enumerate(arr):
        print(f"[{i}] disp={p.get('display')!r} sol={p.get('solutions')} it={p.get('input_type')} calc={p.get('calculator')}")
