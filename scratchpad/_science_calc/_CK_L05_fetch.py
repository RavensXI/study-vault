import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ids = ["a5bc928e-98eb-4dcb-ae0f-b5003a4397d6"]

for i, rid in enumerate(ids):
    url = f"{BASE}?id=eq.{rid}&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    })
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    pd = data[0]["practice_data"]
    with open(f"_CK_L05_row{i}.json", "w", encoding="utf-8") as f:
        json.dump(pd, f, ensure_ascii=False, indent=2)
    print(rid, "written, keys:", list(pd.keys()))
