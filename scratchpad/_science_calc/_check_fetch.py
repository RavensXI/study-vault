import os, json, urllib.request

KEY = os.environ["SUPABASE_SERVICE_KEY"]
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"

def fetch(rid):
    url = f"{BASE}?id=eq.{rid}&select=id,slug,practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)

rid = "fee04afb-d041-4b63-8f67-73da3b882d74"
data = fetch(rid)
with open("_live_canonical.json", "w", encoding="utf-8") as f:
    json.dump(data[0], f, indent=1, ensure_ascii=False)
print("slug:", data[0]["slug"])
pd = data[0]["practice_data"]
print("keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
for tier in ["bronze","silver","gold"]:
    print(tier, len(pb.get(tier, [])))
