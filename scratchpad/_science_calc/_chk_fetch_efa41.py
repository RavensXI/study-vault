import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
ID = "3f80b91f-2691-4e55-a47d-83318e6b8f5c"

def get(id):
    url = f"{BASE}?id=eq.{id}&select=practice_data"
    req = urllib.request.Request(url, headers={
        "apikey": KEY,
        "Authorization": f"Bearer {KEY}",
    })
    with urllib.request.urlopen(req) as r:
        return json.load(r)

data = get(ID)
pd = data[0]["practice_data"]
with open("_chk_live_efa41.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("WROTE _chk_live_efa41.json")
print("top keys:", list(pd.keys()))
