import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
ID = "f6f5708d-edf9-42e6-81d8-49c3cf282310"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_fresh_number_L06.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("TOP KEYS:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ["bronze","silver","gold"]:
    arr = pb.get(tier, [])
    print(f"\n===== {tier} ({len(arr)}) =====")
    for i,p in enumerate(arr):
        print(f"[{i}] itype={p.get('input_type')} calc={p.get('calculator')} sol={p.get('solutions')} opts={p.get('options')}")
        print("    display:", p.get("display"))
