import os, json, urllib.request

ID = "9f5d0097-caa6-464c-9f1c-05ce6b836cc9"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))[0]
with open("_g04_live.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
pd = data["practice_data"]
print("title:", data.get("title"), "slug:", data.get("slug"))
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for tier in ["bronze","silver","gold"]:
    probs = pb.get(tier, [])
    print(f"\n=== {tier} ({len(probs)}) ===")
    for i,p in enumerate(probs):
        print(f"[{i}] it={p.get('input_type')} calc={p.get('calculator')} sol={p.get('solutions')}")
        print("    display:", p.get('display','')[:200])
