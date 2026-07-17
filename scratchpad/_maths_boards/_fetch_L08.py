import os, json, urllib.request

ID = "3e214279-84c2-41dc-a639-94bda78e2da8"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(URL, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
json.dump(pd, open("_live_L08.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("TOP KEYS:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    arr = pb.get(t, [])
    print(f"\n=== {t}: {len(arr)} problems ===")
    for i,p in enumerate(arr):
        print(f"  [{i}] it={p.get('input_type')} calc={p.get('calculator')} sol={p.get('solutions')}")
        print(f"      disp={p.get('display')}")
        if p.get('misconceptions'):
            for m in p['misconceptions']:
                print(f"      MISC expect={m.get('expect')} msg={m.get('message')}")
print("\nhas guided?", 'guided' in pd)
print("has tier_guides?", 'tier_guides' in pd)
print("has method_card?", 'method_card' in pd)
for k in ['bronze_description','silver_description','gold_description']:
    print(k, "=", pb.get(k))
