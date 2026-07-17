import os, json, urllib.request

ID = "4d1cbe2a-483a-400a-9fee-5166ebde6a1b"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_LIVE_L11.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze", "silver", "gold"):
    ps = pb.get(tier, [])
    print(f"\n=== {tier} ({len(ps)}) ===")
    for i, p in enumerate(ps):
        print(f"[{i}] it={p.get('input_type')} calc={p.get('calculator')} sol={p.get('solutions')}")
        print("     disp:", p.get("display"))
        if p.get("input_type") == "multiple_choice":
            print("     opts:", p.get("options"))
print("\nguided keys:", list(pd.get("guided", {}).keys()))
print("tier_guides:", list(pd.get("tier_guides", {}).keys()))
