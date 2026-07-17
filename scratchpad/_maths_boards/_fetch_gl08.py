import os, json, urllib.request

ID = "2ce07c9f-af5f-4162-ae95-544d91a71830"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
URL = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(URL, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
json.dump(pd, open("_live_gl08.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for t in ["bronze","silver","gold"]:
    arr = pb.get(t, [])
    print(f"--- {t}: {len(arr)} problems")
    for i,p in enumerate(arr):
        print(f"  [{i}] it={p.get('input_type')} calc={p.get('calculator')} sol={p.get('solutions')}")
        print(f"      disp={p.get('display')}")
