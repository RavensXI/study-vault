import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
LID = "a33d3e1a-9399-4ea4-9132-b391a705d6a7"
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
with open("_l13_live.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze", "silver", "gold"):
    ps = pb.get(tier, [])
    print(f"\n=== {tier} ({len(ps)}) ===")
    for i, p in enumerate(ps):
        print(f"[{i}] disp={p.get('display')!r}")
        print(f"     sol={p.get('solutions')} input={p.get('input_type')} calc={p.get('calculator')}")
