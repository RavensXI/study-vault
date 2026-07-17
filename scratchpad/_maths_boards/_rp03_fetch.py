import os, json, urllib.request

ID = "2351f9ce-12fd-4b0e-95ac-c89fb8adc612"
KEY = os.environ["SUPABASE_SERVICE_KEY"]
url = f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req = urllib.request.Request(url, headers={
    "apikey": KEY, "Authorization": f"Bearer {KEY}"})
data = json.load(urllib.request.urlopen(req))
pd = data[0]["practice_data"]
json.dump(pd, open("_rp03_live.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("fetched. top keys:", list(pd.keys()))
pb = pd.get("problem_bank", {})
print("problem_bank keys:", list(pb.keys()))
for t in ["bronze","silver","gold"]:
    tb = pb.get(t)
    if isinstance(tb, list):
        print(t, "count:", len(tb))
print("has guided:", "guided" in pd, "has tier_guides:", "tier_guides" in pd)
