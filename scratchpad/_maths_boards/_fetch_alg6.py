import os, json, urllib.request

LID = "7104a3b3-00b8-40c8-a875-0f55043cc6b8"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{LID}&select=practice_data,title,slug"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
row = data[0]
print("TITLE:", row.get("title"), "| SLUG:", row.get("slug"))
pd = row["practice_data"]
json.dump(pd, open("_live_aqa_algL06.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("Top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ("bronze","silver","gold"):
    arr = pb.get(tier, [])
    print(f"\n=== {tier}: {len(arr)} problems | desc={pb.get(tier+'_description')!r} ===")
    for i,p in enumerate(arr):
        print(f"  [{i}] disp={p.get('display')!r} sol={p.get('solutions')} it={p.get('input_type')} calc={p.get('calculator')}")
        for j,m in enumerate(p.get("misconceptions") or []):
            print(f"        mc[{j}] pattern={m.get('pattern')!r} expect={m.get('expect')!r} msg={m.get('message')!r}")
