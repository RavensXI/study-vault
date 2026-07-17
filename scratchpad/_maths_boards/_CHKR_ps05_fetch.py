import json, os, urllib.request

ID = "b063ea7d-cb1c-40ca-a28b-ea79c429361f"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_CHKR_ps05_live.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("pb keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    if t in pb:
        print(t, "count", len(pb[t]))
g = pd.get("guided", {})
print("guided keys:", list(g.keys()))
tg = pd.get("tier_guides", {})
print("tier_guides keys:", list(tg.keys()))
