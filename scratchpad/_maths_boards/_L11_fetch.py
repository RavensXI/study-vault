import os, json, urllib.request

ID = "8e823cb5-7ee7-49af-b403-2c96a246c229"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_L11_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze","silver","gold"):
    arr = pb.get(tier, [])
    print(f"\n=== {tier}: {len(arr)} problems ===")
    for i,p in enumerate(arr):
        print(f"[{i}] disp={p.get('display')!r}")
        print(f"     sol={p.get('solutions')} input={p.get('input_type')} calc={p.get('calculator')}")
