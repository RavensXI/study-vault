import os, json, urllib.request

ID = "7f378aaa-68dc-4420-b952-f56d8349b1ed"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_L08_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()))
for tier in ["bronze","silver","gold"]:
    probs = pb.get(tier, [])
    print(f"\n=== {tier}: {len(probs)} problems ===")
    for i,p in enumerate(probs):
        print(f"[{i}] input_type={p.get('input_type')} calc={p.get('calculator')}")
        print("   display:", repr(p.get('display'))[:300])
        print("   solutions:", p.get('solutions'))
