import os, json, urllib.request

ID = "d15fddc3-0766-4882-bfc8-15a0b7208d89"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_L06e_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ("bronze","silver","gold"):
    probs = pb.get(tier, [])
    print(f"\n=== {tier}: {len(probs)} problems ===")
    for i,p in enumerate(probs):
        print(f"[{i}] input_type={p.get('input_type')} calc={p.get('calculator')}")
        print("   display:", p.get("display"))
        print("   solutions:", p.get("solutions"))
