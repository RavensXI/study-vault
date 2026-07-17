import os, json, urllib.request

ID = "df1cb4b9-09d1-4692-8674-2427dfe4c393"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
})
with urllib.request.urlopen(req) as r:
    data = json.load(r)
pd = data[0]["practice_data"]
json.dump(pd, open("_live_ps05.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("fetched. top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()) if isinstance(pb, dict) else type(pb))
for t in ["bronze","silver","gold"]:
    probs = pb.get(t) if isinstance(pb, dict) else None
    if isinstance(probs, list):
        print(f"{t}: {len(probs)} problems")
